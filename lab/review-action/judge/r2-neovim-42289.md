# PR diff (the real change)

```diff
diff --git a/runtime/doc/repeat.txt b/runtime/doc/repeat.txt
index e8f8c4a1693751..91fd06ebf8fd55 100644
--- a/runtime/doc/repeat.txt
+++ b/runtime/doc/repeat.txt
@@ -350,6 +350,7 @@ context), multicursor replays actions "semantically" (|CmdAtom|).
   instead of skipping over them. The primary cursor keeps the usual
   |fold-behavior|.
 - Cursors are per-buffer, and cascade only while their buffer is current.
+  Use |v:cascading| to check if cascade is in action.
 - Multicursors are presented as |hl-MCursor| highlights, unless your
   (terminal) UI supports the Kitty multiple-cursors protocol.
 - CTRL-C interrupts the cascade.
diff --git a/runtime/doc/vvars.txt b/runtime/doc/vvars.txt
index ecd205aeeb4f5e..10e70bbcf60dff 100644
--- a/runtime/doc/vvars.txt
+++ b/runtime/doc/vvars.txt
@@ -33,6 +33,11 @@ v:argv
 		See |v:progpath| to get the full path to Nvim.
 		See |v:argf| to get only file args, without other options.
 
+				*v:cascading* *cascading-variable*
+v:cascading
+		|v:true| during |mcursor| cascade, |v:false| otherwise.
+		Read-only.
+
 						*v:char* *char-variable*
 v:char
 		Argument for evaluating 'formatexpr' and used for the typed
diff --git a/runtime/lua/vim/_meta/api.gen.lua b/runtime/lua/vim/_meta/api.gen.lua
index 72155d78d3314a..8a3fbd1cad80f4 100644
--- a/runtime/lua/vim/_meta/api.gen.lua
+++ b/runtime/lua/vim/_meta/api.gen.lua
@@ -119,12 +119,6 @@ function vim.api.nvim__inspect_cell(grid, row, col) end
 --- reach, so this function can be used to force a cache clear in a test.
 function vim.api.nvim__invalidate_glyph_cache() end
 
---- WARNING: This feature is experimental/unstable.
----
---- Returns true if a multicursor cascade is in-progress.
---- @return boolean
-function vim.api.nvim__mcursor_cascading() end
-
 --- WARNING: This feature is experimental/unstable.
 ---
 --- Get the properties for namespace
diff --git a/runtime/lua/vim/_meta/vvars.gen.lua b/runtime/lua/vim/_meta/vvars.gen.lua
index f404eaabe8c3b8..667ce2c382cb0f 100644
--- a/runtime/lua/vim/_meta/vvars.gen.lua
+++ b/runtime/lua/vim/_meta/vvars.gen.lua
@@ -30,6 +30,11 @@ vim.v.argf = ...
 --- @type string[]
 vim.v.argv = ...
 
+--- `v:true` during `mcursor` cascade, `v:false` otherwise.
+--- Read-only.
+--- @type boolean
+vim.v.cascading = ...
+
 --- Argument for evaluating 'formatexpr' and used for the typed
 --- character when using <expr> in an abbreviation `:map-<expr>`.
 --- It is also used by the `InsertCharPre`, `InsertEnter`,
diff --git a/runtime/lua/vim/hl.lua b/runtime/lua/vim/hl.lua
index 54c167c765eea6..9d374503e3b030 100644
--- a/runtime/lua/vim/hl.lua
+++ b/runtime/lua/vim/hl.lua
@@ -207,7 +207,7 @@ function M.hl_op(opts)
 
   local state = hl_op_state[state_key]
   -- Multicursor cascade: accumulate per-cursor, don't cancel the previous event's highlight.
-  local cascading = api.nvim__mcursor_cascading()
+  local cascading = vim.v.cascading
   if state ~= nil and state.timer and not state.timer:is_closing() and not cascading then
     state.timer:close()
     assert(state.clear)
diff --git a/src/nvim/api/vim.c b/src/nvim/api/vim.c
index 022982063ab0fc..e4760a9b5a1c39 100644
--- a/src/nvim/api/vim.c
+++ b/src/nvim/api/vim.c
@@ -2083,14 +2083,6 @@ void nvim__invalidate_glyph_cache(void)
   must_redraw = UPD_CLEAR;
 }
 
-/// @nodoc
-/// Returns true if a multicursor cascade is in-progress.
-Boolean nvim__mcursor_cascading(void)
-  FUNC_API_SINCE(15) FUNC_API_FAST
-{
-  return mc_replaying();
-}
-
 /// @nodoc
 Object nvim__unpack(String str, Arena *arena, Error *err)
   FUNC_API_FAST
diff --git a/src/nvim/eval/vars.c b/src/nvim/eval/vars.c
index f2b02499387c8a..41b6a891c8331a 100644
--- a/src/nvim/eval/vars.c
+++ b/src/nvim/eval/vars.c
@@ -221,6 +221,7 @@ static struct vimvar {
   VV(VV_EXITREASON,       "exitreason",       VAR_STRING, VV_RO),
   VV(VV_USERACTIVE,       "useractive",       VAR_NUMBER, VV_RO),
   VV(VV_STARTREASON,      "startreason",      VAR_STRING, VV_RO),
+  VV(VV_CASCADING,        "cascading",        VAR_BOOL,   VV_RO),
 };
 #undef VV
 
diff --git a/src/nvim/eval_defs.h b/src/nvim/eval_defs.h
index a09793582bc098..777dad693863aa 100644
--- a/src/nvim/eval_defs.h
+++ b/src/nvim/eval_defs.h
@@ -139,4 +139,5 @@ typedef enum {
   VV_EXITREASON,
   VV_USERACTIVE,
   VV_STARTREASON,
+  VV_CASCADING,
 } VimVarIndex;
diff --git a/src/nvim/mcursor.c b/src/nvim/mcursor.c
index a84c3f83c92f08..8306283acab672 100644
--- a/src/nvim/mcursor.c
+++ b/src/nvim/mcursor.c
@@ -26,6 +26,7 @@
 #include "nvim/drawscreen.h"
 #include "nvim/errors.h"
 #include "nvim/eval/typval_defs.h"
+#include "nvim/eval/vars.h"
 #include "nvim/ex_docmd.h"
 #include "nvim/extmark.h"
 #include "nvim/gettext_defs.h"
@@ -236,6 +237,7 @@ static void mc_sandbox_enter(McSandbox *sb, bool save_regs)
 {
   assert(!mc_replay);
   mc_replay = true;  // Capture hooks will ignore keys fed during the sandbox.
+  set_vim_var_bool(VV_CASCADING, kBoolVarTrue);
   sb->primary = (Context)CONTEXT_INIT;
   // Change/Visual marks belong to the primary cursor's (already executed) operation.
   // (jumplist/changelist are owned by the primary.)
@@ -285,6 +287,7 @@ static void mc_sandbox_leave(McSandbox *sb)
   }
   ctx_free(&sb->primary);
   mc_replay = false;
+  set_vim_var_bool(VV_CASCADING, kBoolVarFalse);
 }
 
 /// Cascade step: replays an atom at `cursoridx` and updates Context.
diff --git a/src/nvim/vvars.lua b/src/nvim/vvars.lua
index 103b2b40670b63..2ba1a5f4bd7ab0 100644
--- a/src/nvim/vvars.lua
+++ b/src/nvim/vvars.lua
@@ -27,6 +27,13 @@ M.vars = {
       See |v:argf| to get only file args, without other options.
     ]=],
   },
+  cascading = {
+    type = 'boolean',
+    desc = [=[
+      |v:true| during |mcursor| cascade, |v:false| otherwise.
+      Read-only.
+    ]=],
+  },
   char = {
     type = 'string',
     desc = [=[
diff --git a/test/functional/editor/mcursor_spec.lua b/test/functional/editor/mcursor_spec.lua
index 404f0a0aad2f24..864032b588fea3 100644
--- a/test/functional/editor/mcursor_spec.lua
+++ b/test/functional/editor/mcursor_spec.lua
@@ -713,7 +713,7 @@ describe('multicursor', function()
         _G.keys_seen, _G.cascading_seen = 0, false
         vim.on_key(function()
           _G.keys_seen = _G.keys_seen + 1
-          _G.cascading_seen = _G.cascading_seen or vim.api.nvim__mcursor_cascading()
+          _G.cascading_seen = _G.cascading_seen or vim.v.cascading
           if _G.keys_seen == 1000 then
             vim.fn.interrupt()
           end
@@ -3056,9 +3056,7 @@ describe('multicursor', function()
 
     it('TextYankPost fires per cursor with per-cursor contents', function()
       command('let g:yanks = []')
-      command(
-        'autocmd TextYankPost * let g:yanks += [[v:event.regcontents, luaeval("vim.api.nvim__mcursor_cascading()")]]'
-      )
+      command('autocmd TextYankPost * let g:yanks += [[v:event.regcontents, v:cascading]]')
       cursors({ 'aaa', 'bbb' }, 'Qj')
       feed('yy')
       -- The primary's own yank fires first and is not a replay.
@@ -4171,4 +4169,33 @@ describe('multicursor', function()
       eq({ 'aa', 'b' }, get_lines())
     end)
   end)
+
+  it('v:cascading', function()
+    n.exec_lua(function()
+      _G.cascade_log = {}
+      vim.keymap.set('n', 'gh', function()
+        local cur = vim.api.nvim_win_get_cursor(0)
+        table.insert(_G.cascade_log, { vim.v.cascading, cur })
+        vim.api.nvim_buf_set_text(0, cur[1] - 1, cur[2], cur[1] - 1, cur[2], { 'x' })
+      end)
+    end)
+
+    local function assert(mcursor_init)
+      cursors({ 'aaa', 'bbb', 'ccc' }, mcursor_init)
+      eq(false, api.nvim_get_vvar('cascading'))
+      feed('gh')
+      eq({ 'xaaa', 'xbbb', 'xccc' }, get_lines())
+      eq(
+        { { false, { 3, 0 } }, { true, { 1, 0 } }, { true, { 2, 0 } } },
+        n.exec_lua('return _G.cascade_log')
+      )
+      eq(false, api.nvim_get_vvar('cascading'))
+
+      clear_cursors()
+      n.exec_lua('_G.cascade_log = {}')
+    end
+
+    assert('QjQj')
+    assert('QjQjQ')
+  end)
 end)

```

# REVIEW A

**Review of neovim/neovim#42289: add `v:cascading`**

**Summary:** The PR replaces the experimental `nvim__mcursor_cascading()` API function with a read-only `v:cascading` variable. The variable is set at the two places `mc_replay` is toggled, in `mc_sandbox_enter` and `mc_sandbox_leave`. I read the diff and grepped the tree but didn't build it or run the tests. It looks correct and small.

**Correctness**
- `mc_replay` is written only at `mcursor.c:239` and `:289`. The new `set_vim_var_bool` calls sit next to those writes, so `v:cascading` and `mc_replaying()` stay in sync. I checked this with grep.
- The variable is declared `VAR_BOOL` with `VV_RO`. It reads as `v:true`/`v:false` in Vimscript and as a Lua `boolean`, which matches the `@type boolean` in the generated meta file. `hl.lua` now uses it directly.
- Removing the API function is a breaking change. That is acceptable because it was `nvim__`-prefixed and experimental, and the "drop nvim__mcursor_cascading" commit is marked `!`. The only in-tree callers (`hl.lua` and the tests) are updated.

**Issues and suggestions**
1. **Description and docs contradict each other.** The PR description says it follows Vim's "integer, 0 meaning false" approach. The code, docs and tests use real booleans (`VAR_BOOL`, `v:true`/`v:false`, `eq(false, ...)`). The implementation is the better choice, so the description is what should change. Also note that `v:cascading` is the first boolean vvar that Vim doesn't have.
2. **Non-local exit during the sandbox (minor).** If a cascade step can exit non-locally (error, interrupt or `longjmp`) without going through `mc_sandbox_leave`, `mc_replay` and `v:cascading` would both stay stuck. The PR doesn't make this worse, since both are set at the same places. Ctrl-C is covered by an existing test. It would still be worth confirming that every path leaves through `mc_sandbox_leave`.
3. **No nesting guard.** `mc_sandbox_enter` already asserts `!mc_replay`, so nesting is not expected and the plain true/false toggle is fine.
4. **Doc placement.** The `v:cascading` entry in `vvars.txt` sits between `argv` and `char`. That matches the alphabetical order, so no change is needed. The doc could say which scope this covers, for example that autocommands and mappings run during replay (e.g. `TextYankPost`) see `v:true`. The tests show this behavior but the doc doesn't state it.
5. **Doc wording.** "Use |v:cascading| to check if cascade is in action" could read "is in progress" instead.

**Performance:** There is no real cost. It is two variable assignments per cascade, not per cursor.

**Security:** No concerns. The variable is read-only and can't be set from scripts.

**Tests**
- The new `v:cascading` test covers three things. It checks the value is `false` before and after the cascade. It checks the value is `true` for the replayed cursors but `false` for the primary. It does this for two cursor setups, `QjQj` and `QjQjQ`.
- The existing tests (on_key and `TextYankPost`) were migrated to the new variable.
- The local function is named `assert`, which shadows the global. Something like `check_cascade` would be clearer.
- The test doesn't cover the interrupt case. It would be worth asserting that `v:cascading` is `false` after a Ctrl-C-interrupted cascade, in the existing interrupt test around line 713.
- There is no test that `v:cascading = 1` fails, to show the variable is read-only. It's low priority because the generic vvar machinery enforces this.

**Verdict:** Approve. The only substantive follow-ups are fixing the PR description and optionally adding an interrupt-case assertion.

# REVIEW B

**Review of neovim/neovim#42289: `v:cascading`** (already merged)

**Summary:** The PR replaces the experimental `nvim__mcursor_cascading()` API with a read-only `v:cascading` vim variable. The variable is set to true in `mc_sandbox_enter` and to false in `mc_sandbox_leave`. Callers in `hl.lua` and the tests are updated, and docs and generated meta files are added. This is a good change: it gives Vimscript and Lua one consistent way to check the state, and it removes an unstable API. I only read the diff and grepped the repo. I did not build or run the tests.

**Correctness**
- `mc_replay` is only written in `mc_sandbox_enter` and `mc_sandbox_leave` (`src/nvim/mcursor.c:239` and `:289`). The variable therefore stays in sync with `mc_replay`, and no other path needs to update it.
- A grep finds no remaining references to `nvim__mcursor_cascading`.
- **Duplicated state:** `mc_replay` and `v:cascading` now track the same fact. If a future change adds an early return or error path that clears `mc_replay` without going through `mc_sandbox_leave`, the variable will go stale. Consider setting both through one small helper, or having `mc_replaying()` read the vvar.
- **Lost fast-API property:** The old function was `FUNC_API_FAST`. Reading `vim.v.cascading` from a fast context (for example a `vim.uv` callback or `vim.on_key`) is a different question. `vim.v` access in fast events may be restricted, so it's worth checking. The `hl.lua` caller runs in a normal context, so it is fine.
- **Type consistency:** The variable is `VAR_BOOL`, so Lua gets a boolean and Vimscript gets `v:true` or `v:false`. The PR description says "integer with 0 meaning false", which doesn't match the code. The docs and test (`eq(false, ...)`) do match the code. Update the PR description or any release notes.

**Docs**
- The `vvars.txt` entry is placed between `v:argv` and `v:char`, which keeps alphabetical order.
- The `repeat.txt` cross-reference is helpful.
- `|mcursor|` in the vvar description should be a valid tag, but check with `make doc` / `:helptags` that it resolves.
- The `ci:skip-news` label is questionable. This adds a user-visible variable, but removing an experimental `nvim__` API needs no news, so it's defensible.

**Tests**
- The new `v:cascading` test checks the variable is false before and after the cascade. It checks true for the replayed cursors and false for the primary, with cursor positions asserted.
- It covers two cursor setups, `'QjQj'` and `'QjQjQ'`.
- The existing tests (`TextYankPost`, the `on_key` interrupt test) are migrated to the new variable.
- **Local function name:** The helper is named `assert`, which shadows the global `assert`. Use a name like `check_cascade`.
- **Missing coverage:** There is no test that the variable resets after an interrupted cascade (CTRL-C) or after an error inside the callback. These are the paths most likely to leave it stuck at true.
- **Missing coverage:** Nothing tests that assigning to it fails (`VV_RO`).

**Performance and security:** No concerns. Setting a vvar twice per cascade is negligible, and the variable is read-only to scripts.

**Verdict:** LGTM. Suggested follow-ups, all minor: rename the shadowing `assert`, add an interrupt-reset test, and confirm fast-context behavior.
