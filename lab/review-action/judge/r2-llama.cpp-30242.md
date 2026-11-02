# PR diff (the real change)

```diff
diff --git a/common/jinja/value.cpp b/common/jinja/value.cpp
index 0840e05b828..f1e4e6b5ddf 100644
--- a/common/jinja/value.cpp
+++ b/common/jinja/value.cpp
@@ -6,6 +6,7 @@
 #include "json.h"
 
 #include <sstream>
+#include <stdexcept>
 #include <string>
 #include <cctype>
 #include <cfloat>
@@ -1460,7 +1461,10 @@ const func_builtins & value_undefined_t::get_builtins() const {
 //////////////////////////////////
 
 
-static value from_json(const common_json & j, bool mark_input) {
+// the runtime walks values with recursion, a deeper input overflows the stack
+static constexpr int FROM_JSON_MAX_DEPTH = 128;
+
+static value from_json(const common_json & j, bool mark_input, int depth = 0) {
     if (j.is_null()) {
         return mk_val<value_none>();
     } else if (j.is_boolean()) {
@@ -1475,16 +1479,18 @@ static value from_json(const common_json & j, bool mark_input) {
             str->mark_input();
         }
         return str;
+    } else if ((j.is_array() || j.is_object()) && depth >= FROM_JSON_MAX_DEPTH) {
+        throw std::invalid_argument("JSON is nested more than " + std::to_string(FROM_JSON_MAX_DEPTH) + " levels deep");
     } else if (j.is_array()) {
         auto arr = mk_val<value_array>();
         for (const auto & item : j) {
-            arr->push_back(from_json(item, mark_input));
+            arr->push_back(from_json(item, mark_input, depth + 1));
         }
         return arr;
     } else if (j.is_object()) {
         auto obj = mk_val<value_object>();
         for (auto it = j.begin(); it != j.end(); ++it) {
-            obj->insert(it.key(), from_json(it.value(), mark_input));
+            obj->insert(it.key(), from_json(it.value(), mark_input, depth + 1));
         }
         return obj;
     } else {
diff --git a/common/json-schema.cpp b/common/json-schema.cpp
index 6898840e7d1..e1bfa79dfdc 100644
--- a/common/json-schema.cpp
+++ b/common/json-schema.cpp
@@ -224,7 +224,21 @@ class common_chat_schema_builder {
         return node;
     }
 
+    // the builder and the code that walks the built schema recurse once per level, a deeper schema overflows the stack
+    static constexpr int max_depth = 128;
+    int                  depth_    = 0;
+
     common_chat_schema_ptr build_node(const common_json & schema, const std::string & path) {
+        if (depth_ >= max_depth) {
+            throw std::invalid_argument("JSON schema is nested more than " + std::to_string(max_depth) + " levels deep");
+        }
+        depth_++;
+        auto node = build_node_impl(schema, path);
+        depth_--;
+        return node;
+    }
+
+    common_chat_schema_ptr build_node_impl(const common_json & schema, const std::string & path) {
         if (!schema.is_object()) {
             fail(path, "schema must be an object");
         }
diff --git a/tests/test-chat.cpp b/tests/test-chat.cpp
index 49519eecab1..c6f841ae3cd 100644
--- a/tests/test-chat.cpp
+++ b/tests/test-chat.cpp
@@ -10,6 +10,8 @@
 #include "../tools/server/server-chat.h"
 #include "chat-auto-parser.h"
 #include "chat.h"
+#include "json-schema-to-grammar.h"
+#include "json-schema.h"
 #include "common.h"
 #include "ggml.h"
 #include "log.h"
@@ -7931,6 +7933,58 @@ static void test_chat_session() {
     }
 }
 
+static void test_chat_json_depth() {
+    LOG_DBG("%s\n", __func__);
+    const auto arrays = [](size_t n) {
+        return std::string(n, '[') + std::string(n, ']');
+    };
+    // a schema of n nested array types
+    const auto schema = [](size_t n) {
+        std::string s;
+        for (size_t i = 0; i < n; i++) {
+            s += R"({"type": "array", "items": )";
+        }
+        return s + R"({"type": "string"})" + std::string(n, '}');
+    };
+    const auto rejected = [](const std::function<void()> & fn) {
+        try {
+            fn();
+        } catch (const std::invalid_argument & e) {
+            return std::string(e.what()).find("nested more than 128 levels deep") != std::string::npos;
+        }
+        return false;
+    };
+
+    // the schema builder stops at 128 levels, the root schema is one of them
+    assert_equals(false, rejected([&] { common_chat_schema_from_json(json::parse(schema(127))); }));
+    assert_equals(true, rejected([&] { common_chat_schema_from_json(json::parse(schema(128))); }));
+    assert_equals(true, rejected([&] { json_schema_to_grammar(json::parse(schema(1000))); }));
+
+    // the jinja engine and the schema builder reject the inputs before they recurse too deep
+    auto         tmpls = read_templates("models/templates/Qwen3.5-4B.jinja");
+    const size_t deep  = 1000;
+
+    common_chat_templates_inputs tool_schema;
+    tool_schema.messages = { message_user };
+    tool_schema.tools    = { { "f", "", R"({"type": "object", "properties": {"x": )" + schema(deep) + "}}" } };
+    assert_equals(true, rejected([&] { common_chat_templates_apply(tmpls.get(), tool_schema); }));
+
+    common_chat_templates_inputs tool_args;
+    tool_args.messages = { message_user, simple_assist_msg("", "", "special_function", R"({"arg1": )" + arrays(deep) + "}") };
+    tool_args.tools    = { special_function_tool };
+    assert_equals(true, rejected([&] { common_chat_templates_apply(tmpls.get(), tool_args); }));
+
+    common_chat_templates_inputs kwargs;
+    kwargs.messages                     = { message_user };
+    kwargs.chat_template_kwargs["deep"] = arrays(deep);
+    assert_equals(true, rejected([&] { common_chat_templates_apply(tmpls.get(), kwargs); }));
+
+    common_chat_templates_inputs json_schema;
+    json_schema.messages    = { message_user };
+    json_schema.json_schema = schema(deep);
+    assert_equals(true, rejected([&] { common_chat_templates_apply(tmpls.get(), json_schema); }));
+}
+
 static void test_reasoning_budget_tokens_per_request() {
     LOG_DBG("%s\n", __func__);
     // Use Qwen3 template which has <think>...</think> reasoning markers.
@@ -8179,6 +8233,7 @@ int main(int argc, char ** argv) {
         test_reasoning_effort_caps();
         test_prompt_parts();
         test_chat_session();
+        test_chat_json_depth();
         test_reasoning_budget_tokens_per_request();
         test_reasoning_budget_message_per_request();
         test_template_output_peg_parsers(detailed_debug);
diff --git a/tests/test-server-component.cpp b/tests/test-server-component.cpp
index 18e0cdc2fe0..92eeec055b4 100644
--- a/tests/test-server-component.cpp
+++ b/tests/test-server-component.cpp
@@ -464,6 +464,32 @@ static void test_rerank_template(testing & t) {
     }
 }
 
+//
+// server_decision_context: the recursive functions stop at RECURSIVE_LIMIT
+//
+
+static void test_decision_depth(testing & t) {
+    const auto prepare = [](size_t depth) {
+        server_decision_context ctx;
+        ctx.type = COMMON_DECISION_TYPE_H2O_LIGHTNING; // the state goes through decision_py_dump
+        std::string error;
+        try {
+            ctx.prepare_state(json::parse(std::string(depth, '[') + std::string(depth, ']')));
+        } catch (const std::invalid_argument & e) {
+            error = e.what();
+        }
+        return error;
+    };
+    t.test("state at the limit", [&](testing & t) {
+        const std::string error = prepare(128);
+        t.assert_true("accepted: " + error, error.empty());
+    });
+    t.test("deep state", [&](testing & t) {
+        const std::string error = prepare(1000);
+        t.assert_true("rejected as nested: " + error, error.find("nested more than 128 levels deep") != std::string::npos);
+    });
+}
+
 int main(int argc, char ** argv) {
     testing t;
 
@@ -484,6 +510,7 @@ int main(int argc, char ** argv) {
     t.test("server_pipe",   test_server_pipe);
     t.test("decision_escape", test_decision_escape);
     t.test("rerank_template", test_rerank_template);
+    t.test("decision_depth",  test_decision_depth);
 
     return t.summary();
 }
diff --git a/tools/server/server-decision.cpp b/tools/server/server-decision.cpp
index ce4cb4d0910..5fd7585ff6c 100644
--- a/tools/server/server-decision.cpp
+++ b/tools/server/server-decision.cpp
@@ -23,6 +23,9 @@ static const size_t DECISION_LEV_N_RATINGS = 9;
 // a longer state keeps its head and its tail
 static const size_t DECISION_H2O_MAX_STATE_TOKENS = 32000;
 
+// the recursive functions of this file walk request JSON, a deeper value would overflow the stack
+static const int RECURSIVE_LIMIT = 128;
+
 static std::string decision_meta_str(const llama_model * model, const std::string & key) {
     char buf[256];
     const int32_t n = llama_model_meta_val_str(model, key.c_str(), buf, sizeof(buf));
@@ -417,7 +420,10 @@ json server_decision_context::parse_state(const json & body, std::vector<raw_buf
 //
 
 // replace text in all strings of a JSON value
-static json decision_replace_text(const json & val, const std::string & search, const std::string & replace) {
+static json decision_replace_text(const json & val, const std::string & search, const std::string & replace, int depth = 0) {
+    if (depth >= RECURSIVE_LIMIT) {
+        throw std::invalid_argument("JSON is nested more than " + std::to_string(RECURSIVE_LIMIT) + " levels deep");
+    }
     if (val.is_string()) {
         std::string str = val.get<std::string>();
         string_replace_all(str, search, replace);
@@ -426,14 +432,14 @@ static json decision_replace_text(const json & val, const std::string & search,
     if (val.is_array()) {
         json out = json::array();
         for (const auto & item : val) {
-            out.push_back(decision_replace_text(item, search, replace));
+            out.push_back(decision_replace_text(item, search, replace, depth + 1));
         }
         return out;
     }
     if (val.is_object()) {
         json out = json::object();
         for (const auto & [key, item] : val.items()) {
-            out[key] = decision_replace_text(item, search, replace);
+            out[key] = decision_replace_text(item, search, replace, depth + 1);
         }
         return out;
     }
@@ -441,18 +447,21 @@ static json decision_replace_text(const json & val, const std::string & search,
 }
 
 // sort the keys of all objects of a JSON value
-static json decision_sort_keys(const json & val) {
+static json decision_sort_keys(const json & val, int depth = 0) {
+    if (depth >= RECURSIVE_LIMIT) {
+        throw std::invalid_argument("JSON is nested more than " + std::to_string(RECURSIVE_LIMIT) + " levels deep");
+    }
     if (val.is_array()) {
         json out = json::array();
         for (const auto & item : val) {
-            out.push_back(decision_sort_keys(item));
+            out.push_back(decision_sort_keys(item, depth + 1));
         }
         return out;
     }
     if (val.is_object()) {
         std::map<std::string, json> sorted;
         for (const auto & [key, item] : val.items()) {
-            sorted[key] = decision_sort_keys(item);
+            sorted[key] = decision_sort_keys(item, depth + 1);
         }
         json out = json::object();
         for (const auto & [key, item] : sorted) {
@@ -464,7 +473,10 @@ static json decision_sort_keys(const json & val) {
 }
 
 // kev flattens a JSON value into text, the keys of an object are kept as labels (kev/api.py: render)
-static std::string decision_kev_render(const json & val, int indent = 0) {
+static std::string decision_kev_render(const json & val, int indent = 0, int depth = 0) {
+    if (depth >= RECURSIVE_LIMIT) {
+        throw std::invalid_argument("JSON is nested more than " + std::to_string(RECURSIVE_LIMIT) + " levels deep");
+    }
     const std::string pad(2 * indent, ' ');
     if (val.is_null()) {
         return "";
@@ -478,7 +490,7 @@ static std::string decision_kev_render(const json & val, int indent = 0) {
     if (val.is_array()) {
         std::string out;
         for (const auto & item : val) {
-            const std::string text = decision_kev_render(item, indent + 1);
+            const std::string text = decision_kev_render(item, indent + 1, depth + 1);
             out += (out.empty() ? "" : "\n") + pad + "- " + text.substr(std::min(text.size(), text.find_first_not_of(" \t\n\r")));
         }
         return out;
@@ -487,7 +499,7 @@ static std::string decision_kev_render(const json & val, int indent = 0) {
         std::string out;
         for (const auto & [key, item] : val.items()) {
             const bool is_nested = item.is_object() || item.is_array();
-            out += (out.empty() ? "" : "\n") + pad + key + (is_nested ? ":\n" : ": ") + decision_kev_render(item, is_nested ? indent + 1 : 0);
+            out += (out.empty() ? "" : "\n") + pad + key + (is_nested ? ":\n" : ": ") + decision_kev_render(item, is_nested ? indent + 1 : 0, depth + 1);
         }
         return out;
     }
@@ -528,21 +540,24 @@ static std::string decision_kev_text(const json & val) {
 }
 
 // lfm2-d1-omni: special tokens written in the input must not be parsed as such, in keys too (d1-omni prompt.py: escape)
-static json decision_d1omni_escape(const json & val) {
+static json decision_d1omni_escape(const json & val, int depth = 0) {
+    if (depth >= RECURSIVE_LIMIT) {
+        throw std::invalid_argument("JSON is nested more than " + std::to_string(RECURSIVE_LIMIT) + " levels deep");
+    }
     if (val.is_string()) {
         return server_decision_escape_special_tokens(val.get<std::string>());
     }
     if (val.is_array()) {
         json out = json::array();
         for (const auto & item : val) {
-            out.push_back(decision_d1omni_escape(item));
+            out.push_back(decision_d1omni_escape(item, depth + 1));
         }
         return out;
     }
     if (val.is_object()) {
         json out = json::object();
         for (const auto & [key, item] : val.items()) {
-            out[server_decision_escape_special_tokens(key)] = decision_d1omni_escape(item);
+            out[server_decision_escape_special_tokens(key)] = decision_d1omni_escape(item, depth + 1);
         }
         return out;
     }
@@ -669,6 +684,9 @@ static void decision_py_str(std::string & out, const std::string & s, bool ensur
 
 // json.dumps() of Python: indent < 0 is no indent, keys stay in their order
 static void decision_py_dump(std::string & out, const json & val, int indent, int level, const std::string & item_sep, const std::string & key_sep, bool ensure_ascii) {
+    if (level >= RECURSIVE_LIMIT) {
+        throw std::invalid_argument("JSON is nested more than " + std::to_string(RECURSIVE_LIMIT) + " levels deep");
+    }
     const auto newline = [&](int lvl) {
         return indent < 0 ? std::string() : "\n" + std::string(indent * lvl, ' ');
     };

```

# REVIEW A

This review covers only part of the diff. The tool output was truncated, and I couldn't page through the omitted middle. That part includes the rest of `test_chat_json_depth` and the other `common/chat.cpp` hunks. The `value.cpp`, `json-schema.cpp`, and `decision_*` hunks and the start of the test were visible.

## Summary
The PR adds a nesting-depth cap of 128 to the places that walk JSON recursively: `from_json` in the Jinja runtime, the schema builder, and the `decision_kev_render`, `decision_d1omni_escape`, and `decision_py_dump` helpers in chat. A deeper input now throws `std::invalid_argument` instead of overflowing the stack. The goal is sound, since untrusted request JSON can otherwise crash the server. It also matches the earlier commit that added `RECURSIVE_LIMIT` ("chat : reject JSON nested more than 128 levels before walking it").

## Code quality
- **Duplicated limit.** There are now three separate constants for the same policy: `RECURSIVE_LIMIT` in chat, `FROM_JSON_MAX_DEPTH` in `value.cpp`, and `max_depth` in `json-schema.cpp`. The error message string is also copy-pasted at each site. Putting one limit and one throw helper in a shared header, such as `common/json-*.h`, would stop them drifting apart. The test hard-codes `"nested more than 128 levels deep"`, so a drift would be caught only by the test.
- **Not exception-safe.** In `common/json-schema.cpp`, `build_node` does `depth_++; ...; depth_--;` by hand. If `build_node_impl` throws, which `fail()` does for ordinary schema errors, `depth_` is never decremented. This is harmless only while the builder is discarded after any exception. If a caller ever catches an error and keeps using the builder, for example to try an alternative branch, the depth will be wrong. A small RAII guard, or `depth_` handled via a scoped counter, is safer and costs almost nothing.
- **Check order in `from_json`.** The depth check sits after the scalar branches and tests `is_array() || is_object()` again. It works. A single early `if (depth >= MAX && (j.is_array() || j.is_object()))` at the top would be easier to read.
- **Default argument on `decision_d1omni_escape`.** `depth = 0` is fine for a static function. In `decision_py_dump`, the existing `level` parameter doubles as the depth. That is neat, but it ties the nesting limit to the indentation level, so add a short comment.

## Potential bugs
- **Callers must handle `std::invalid_argument`.** I couldn't confirm that every path reaching `from_json` (template rendering, `common_chat_templates_apply`, tool-schema conversion) turns this into a 4xx response. Otherwise it could surface as a 500 or a server crash. The test only covers the throw, so add a test through the server or chat-params entry point that checks the error becomes a client error.
- **Off-by-one semantics.** The limit is checked with `depth >= 128`, so 128 levels is accepted and 129 is rejected. The schema builder counts the root as a level. The test appears to probe these boundaries, which is good. Make sure the message wording ("more than 128") agrees with all three sites.
- **Stack use per level.** 128 levels is safe for the lightweight `from_json` frames. The Jinja runtime's `execute`, `to_string`, and `tojson` paths use much larger frames. Debug builds, ASan, and small thread stacks, such as server worker threads on musl or Windows (1 MB), could still overflow well below 128 when a template recurses over the value. The comment on `FROM_JSON_MAX_DEPTH` claims that the cap prevents overflow. Check it with a deep input in a debug or ASan build.
- **Other recursive walkers.** Check that nothing else walks request JSON before these guards run: the nlohmann parser itself, `json.dump()`, and the destructor of deeply nested values. Check `common/peg-parser` and `json-partial` too. Recent nlohmann versions limit parser recursion only for SAX consumers, so the guard has to come before any `dump()`.

## Performance
The overhead is one integer compare per node and one extra parameter. That is negligible, and the schema builder's counter is trivial.

## Security
This is a hardening change that closes a remote stack-overflow DoS through nested JSON in messages, tool schemas, and `response_format`. The remaining risk is a missed walker, as noted above.

## Tests
- The new `test_chat_json_depth` covers a nested-array input and a nested-schema generator, with boundary checks at the schema builder.
- Add the following if they're not already in the truncated part:
  - A direct `from_json` case through a Jinja render with `mark_input`.
  - Exactly 128 levels accepted and 129 rejected for each of the three layers.
  - Nested objects, not only arrays.
  - A nested case for the `decision_*` helpers: `d1omni_escape` and `py_dump`.
  - A check that the error reaches the HTTP layer as a 400.
- `rejected()` returns false when nothing throws and also when a different `invalid_argument` is thrown. That is correct. Consider printing the actual message on failure to make test failures easier to diagnose.
- The new includes `json-schema.h` and `json-schema-to-grammar.h` are in the middle of the include list. Place them alphabetically, per the repo style.

## Verdict
This is a reasonable and low-risk fix. Before merging, I'd ask for three things: unify the constant and the error message, make the depth counter in `build_node` exception-safe, and confirm the error becomes a client error at the server boundary.

# REVIEW B

# Review of PR #30242: reject JSON nested more than 128 levels

The PR is already merged. I read the diff and the description, and I didn't build or run anything.

**One thing to check first:** the PR description names `common_chat_check_json_depth` in `chat.cpp` and changes to `server-schema.cpp` and `parse_questions`. The diff I got doesn't include any of those. It covers only `jinja/value.cpp`, `json-schema.cpp`, `server-decision.cpp` and the tests. Either the diff is partial or the description is stale. The tests do call `common_chat_templates_apply`, so please confirm the `chat.cpp` entry point is in the tree.

## Summary
The fix is sound and follows the repo's approach: it rejects over-deep input before any recursion runs, answers 400, and leaves `common/json.cpp` alone. The description gives a reproduction, a before/after table, and the cost of the check, and the tests cover both sides of the limit.

## Code quality
- **The limit of 128 is defined three times.** `FROM_JSON_MAX_DEPTH` is in `value.cpp`, `max_depth` is in `json-schema.cpp`, and `RECURSIVE_LIMIT` is in `server-decision.cpp`. The `chat.cpp` helper presumably has a fourth. The tests hard-code the string `"nested more than 128 levels deep"`. A shared constant, for example in `json.h`, would stop these drifting apart. At the least, add a comment pointing each definition at the others.
- **The depth counter in `json-schema.cpp` is not exception-safe.** `depth_--` is skipped when `build_node_impl` throws. This is harmless if the builder is discarded after any failure. But `fail()` also throws, and if any caller catches and continues with the same builder, `depth_` stays inflated. A small RAII guard or a `try/catch` would remove the risk cheaply.
- **The depth check treats scalars differently in different places.**
  - `from_json` checks only arrays and objects, so a scalar at depth 128 is accepted.
  - `decision_*` and `decision_py_dump` check before looking at the type, so a scalar leaf at depth 128 is rejected.
  - The effective limit therefore differs by one level between code paths.
  - It doesn't matter for safety, but it makes "128 levels" imprecise. The `state at the limit` test passes only because it uses empty arrays.
- **The `decision_*` helpers repeat the same `throw` block six times.** A tiny `decision_check_depth(depth)` helper would be tidier.
- **`decision_py_dump` checks `level` while the others check `depth`.** This is fine, but the mismatch is worth noting.

## Potential bugs and gaps
- **Prefill is not covered.** The PR says so itself: an assistant prefill with 1,000 levels still crashes the PEG output parser (#29728). That should stay open until the parser has its own depth guard.
- **Some templates overflow below 128 levels on macOS.** Jinja macro recursion with the 512 KB HTTP thread stack is the cause. The PR documents this. A limit enforced by a shared constant would make it easy to lower later.
- **Error type and status code.** Please confirm that every call site maps `std::invalid_argument` to HTTP 400. `/v1/systemone` and `/completion` go through different paths. The tests check the exception type, not the HTTP code.

## Performance
The reported cost is negligible: 0.54 ms for a 10 MB request, against 35 ms to parse it. The extra `int` parameter in the recursive functions is trivial.

## Security
This closes a real remote crash (a stack-overflow denial of service) from unauthenticated-style JSON input. I agree with the PR's own list of remaining unfixed recursion, such as `$ref` chains and the prefill path. Each of those is a similar denial of service and deserves a follow-up issue.

## Test coverage
- **Good:** `test_chat_json_depth` checks the schema boundary at 127 and 128. It also checks 1,000 levels in tool parameters, tool-call arguments, `chat_template_kwargs` and `json_schema`. `decision_depth` checks the boundary in the server component test.
- **Missing:**
  - There is no direct test of `from_json`, though it is covered indirectly through `chat_template_kwargs` and tool-call arguments.
  - The `decision_*` helpers are tested only through the H2O state path, so the d1-omni and kev paths have no depth test.
  - There is no HTTP-level test that the response is a 400.
  - The gemma4 "stays text if too deep" behavior from the description has no test.
- **Style:** the tests are fine. Comments are concise and ASCII only, as AGENTS.md asks.

## Verdict
This is a good, narrowly scoped hardening fix. I'd follow up with a shared depth constant and an RAII depth guard. I'd also add a few more tests: the d1-omni and kev paths, the HTTP 400 response, and the gemma4 text fallback.
