# PR diff (the real change)

```diff
diff --git a/runtime/doc/lua-async.txt b/runtime/doc/lua-async.txt
index 3f3971e07da15f..fabf1aa4924beb 100644
--- a/runtime/doc/lua-async.txt
+++ b/runtime/doc/lua-async.txt
@@ -61,6 +61,10 @@ Awaiting a task observes that task's result; it does not attach the task to
 the awaiter or change which task owns it. Ownership is decided when the task
 is created.
 
+A task stays alive until it and its attached children finish cleanup. Dropping
+its handle does not stop the work. Keep the handle and call |Task:close()|
+when work is no longer needed, then observe completion to wait for cleanup.
+
 Scheduling is cooperative. When a task awaits a timer, I/O operation,
 callback, or another task, `vim.async` saves the Lua stack and returns control
 to the event loop. Other callbacks can run while the task is paused. Nothing
@@ -215,6 +219,17 @@ await({...})                                               *vim.async.await()*
         end)
 <
 
+    If Lua collects the callback (because it is unreachable) before it is
+    called, the task fails with "await callback was discarded". The failure is
+    queued for a later event-loop turn. Normal await cleanup runs before the
+    error is delivered. If cleanup fails, its error is reported instead.
+    |vim.async.pawait()| can handle this error and continue the task instead.
+
+    A callback held in the task's own data or returned handle remains
+    reachable, so the wait can stay pending. GC timing is unpredictable; use
+    |Task:close()| or |vim.async.timeout()| to request cancellation without
+    relying on GC.
+
     Parameters: ~
       • {...}  (`any`) see overloads
 
@@ -490,6 +505,11 @@ Task:on_complete({callback})                              *Task:on_complete()*
     If the Task is already done when this method is called, the callback is
     called immediately with the results.
 
+    Callback errors are reported through the runtime scheduler with their
+    traceback. They do not change the task result, interrupt other callbacks,
+    or propagate to the caller that completes the task or registers a
+    callback. Catch errors inside the callback to handle them locally.
+
     This only observes completion. It does not start a pending task.
 
     Parameters: ~
@@ -520,7 +540,8 @@ Task:raise_on_error()                                  *Task:raise_on_error()*
 
     Use this for detached or top-level fire-and-forget tasks whose completion
     will not otherwise be observed. Attached task errors already propagate to
-    their parent.
+    their parent. The error is reported through the runtime scheduler, as for
+    errors in |Task:on_complete()| callbacks.
 
     Detached tasks do not raise errors automatically. Detaching changes
     ownership only; their completion can still be handled with
diff --git a/runtime/lua/vim/_core/util.lua b/runtime/lua/vim/_core/util.lua
index 19a992c725c538..ac42b3ee48e81a 100644
--- a/runtime/lua/vim/_core/util.lua
+++ b/runtime/lua/vim/_core/util.lua
@@ -23,6 +23,25 @@ function M._stringify_error(err)
 end
 -- Generated from async.nvim/lua/async/_errors.lua: end
 
+-- Generated from async.nvim/lua/async/_util.lua: start
+--- Create a function that runs a function when it is garbage collected.
+--- @generic F : function
+--- @param f F
+--- @param gc fun()
+--- @return F
+--- @private
+function M._gc_fun(f, gc)
+  local proxy = newproxy(true)
+  local proxy_mt = getmetatable(proxy)
+  proxy_mt.__gc = gc
+
+  return function(...)
+    local _ = proxy
+    return f(...)
+  end
+end
+-- Generated from async.nvim/lua/async/_util.lua: end
+
 --- Adds one or more blank lines above or below the cursor.
 --- @param above? boolean Place blank line(s) above the cursor
 local function add_blank(above)
diff --git a/runtime/lua/vim/async.lua b/runtime/lua/vim/async.lua
index b261e04664d049..66935a73e91922 100644
--- a/runtime/lua/vim/async.lua
+++ b/runtime/lua/vim/async.lua
@@ -63,6 +63,11 @@ local F = vim.F
 --- the awaiter or change which task owns it. Ownership is decided when the task
 --- is created.
 ---
+--- A task stays alive until it and its attached children finish cleanup.
+--- Dropping its handle does not stop the work. Keep the handle and call
+--- [Task:close()] when work is no longer needed, then observe completion to
+--- wait for cleanup.
+---
 --- Scheduling is cooperative. When a task awaits a timer, I/O operation,
 --- callback, or another task, `vim.async` saves the Lua stack and returns
 --- control to the event loop. Other callbacks can run while the task is paused.
diff --git a/runtime/lua/vim/async/_core.lua b/runtime/lua/vim/async/_core.lua
index f33e69ccce822e..6144ce1a6b8c97 100644
--- a/runtime/lua/vim/async/_core.lua
+++ b/runtime/lua/vim/async/_core.lua
@@ -25,14 +25,14 @@ local unpack_len = vim.F.unpack_len
 --- @nodoc
 local M = {}
 
---- Weak table to keep track of running tasks
+--- Keep unfinished tasks and their resources alive until completion.
 --- @type table<thread, vim.async.Task<any>?>
-local threads = setmetatable({}, { __mode = 'k' })
+local threads = {}
 
 --- Returns the currently running task.
 --- @return vim.async.Task<any>?
 local function running()
-  --- @diagnostic disable-next-line: invisible, undefined-field
+  --- @diagnostic disable-next-line: access-invisible, undefined-field
   local task = threads[coroutine_running()]
   if task and not task:completed() then
     return task
@@ -166,6 +166,11 @@ do --- Task
   --- If the Task is already done when this method is called, the callback is
   --- called immediately with the results.
   ---
+  --- Callback errors are reported through the runtime scheduler with their
+  --- traceback. They do not change the task result, interrupt other callbacks,
+  --- or propagate to the caller that completes the task or registers a callback.
+  --- Catch errors inside the callback to handle them locally.
+  ---
   --- This only observes completion. It does not start a pending task.
   --- @param callback fun(err?: any, ...: R...)
   --- @return fun() unsubscribe
@@ -300,7 +305,7 @@ do --- Task
       msg = awaiting:traceback(msg, level + 1)
     end
 
-    local tblvl = is_task(awaiting) and 2 or nil
+    local tblvl = is_task(awaiting) and 2 or 0
     local tb = debug.traceback(self._thread, '', tblvl) or ''
     msg = (msg == nil and '' or tostring(msg)) .. tb:gsub('\n\t', '\n\t' .. thread)
 
@@ -320,6 +325,8 @@ do --- Task
   --- Use this for detached or top-level fire-and-forget tasks whose completion
   --- will not otherwise be observed. Attached task errors already propagate to
   --- their parent.
+  --- The error is reported through the runtime scheduler, as for errors in
+  --- [Task:on_complete()] callbacks.
   ---
   --- Detached tasks do not raise errors automatically. Detaching changes
   --- ownership only; their completion can still be handled with
@@ -384,9 +391,10 @@ do --- Task
   --- @package
   --- @param err any
   function Task:_raise(err)
-    if self:status() == 'running' then
-      -- A running coroutine cannot be resumed recursively, so deliver the
-      -- error on a later event-loop turn after the current stack unwinds.
+    local status = self:status()
+    if status == 'running' or status == 'normal' then
+      -- A running coroutine, or one beneath it (`normal`), cannot be resumed
+      -- recursively. Deliver the error after the current stack unwinds.
       runtime.schedule(function()
         if not self:completed() then
           self:_resume(err)
@@ -630,7 +638,16 @@ do --- Task
         -- Callback setup has one result: the optional closable.
         --- @type fun(callback: fun(err?: any, ...: any)): vim.async.Closable?
         local awaitable = yielded
-        setup_ok, setup_result = pcall(awaitable, complete_await)
+        local callback = util._gc_fun(complete_await, function()
+          if not settled and not task:completed() then
+            -- A collected callback can never finish this wait. Keep the task
+            -- and its resources alive, and deliver the failure outside GC.
+            runtime.schedule(function()
+              complete_await('await callback was discarded')
+            end)
+          end
+        end)
+        setup_ok, setup_result = pcall(awaitable, callback)
       end
 
       if not setup_ok then
@@ -900,16 +917,19 @@ local function norm_cb_fun(argc, fun, ...)
     end
   end
 
-  local args = pack_len(...)
+  local args = pack_len(...) --[[@as { [integer]: any, n: integer }? ]]
 
   --- @param callback fun(...: any)
   --- @return any?
   return function(callback)
-    args[argc] = function(...)
+    -- The thunk must not retain the inserted callback after setup returns.
+    local call_args = assert(args)
+    args = nil
+    call_args[argc] = function(...)
       callback(nil, ...)
     end
-    args.n = math.max(args.n, argc)
-    return fun(unpack_len(args))
+    call_args.n = math.max(call_args.n, argc)
+    return fun(unpack_len(call_args))
   end
 end
 
@@ -982,6 +1002,16 @@ end
 ---   render(lines)
 --- end)
 --- ```
+---
+--- If Lua collects the callback (because it is unreachable) before it is
+--- called, the task fails with "await callback was discarded". The failure is
+--- queued for a later event-loop turn. Normal await cleanup runs before the
+--- error is delivered. If cleanup fails, its error is reported instead.
+--- [vim.async.pawait()] can handle this error and continue the task instead.
+---
+--- A callback held in the task's own data or returned handle remains reachable,
+--- so the wait can stay pending. GC timing is unpredictable; use [Task:close()]
+--- or [vim.async.timeout()] to request cancellation without relying on GC.
 --- @async
 --- @generic T, R
 --- @param ... any see overloads
diff --git a/runtime/lua/vim/async/_future.lua b/runtime/lua/vim/async/_future.lua
index 4c6e73f3205ad1..97df0bbe8a1d46 100644
--- a/runtime/lua/vim/async/_future.lua
+++ b/runtime/lua/vim/async/_future.lua
@@ -1,18 +1,37 @@
 local F = vim.F
 local util = require('vim._core.util')
+local runtime = require('vim.async._runtime')
 
+--- Future objects are used to bridge low-level callback-based code with
+--- high-level async/await code.
 --- @class (internal) vim.async.Future<R>
 --- @field private _callbacks table<integer, fun(err?: any, ...: R...)>
 --- @field private _callback_pos integer
---- @field private _err? any
+--- Error result of the task is an error occurs.
+--- Must use `await` to get the result.
+--- @field package _err? any
+---
+--- Result of the task.
+--- Must use `await` to get the result.
 --- @field private _result? R[] & { n: integer }
 local Future = {}
 Future.__index = Future
 
+--- Return `true` if the Future is completed.
+--- @return boolean
 function Future:completed()
   return self._err ~= nil or self._result ~= nil
 end
 
+--- Return the result of the Future.
+---
+--- If the Future is done and has a result set by the `complete()` method, the
+--- result is returned.
+---
+--- If the Future’s result isn’t yet available, this method raises a
+--- "Future has not completed" error.
+--- @return boolean stat true if the Future completed successfully, false otherwise.
+--- @return any ... error or result
 function Future:result()
   if not self:completed() then
     error('Future has not completed', 2)
@@ -25,17 +44,43 @@ function Future:result()
   end
 end
 
+--- Invoke an observer without letting its error escape through completion.
+--- @private
 --- @param callback fun(err?: any, ...: R...)
---- @return fun()
-function Future:on_complete(callback)
-  if self:completed() then
-    -- Already completed or closed
+function Future:_invoke(callback)
+  local ok, traceback = xpcall(function()
     if self._err ~= nil then
       callback(self._err)
     else
       assert(self._result)
       callback(nil, F.unpack_len(self._result))
     end
+  end, function(err)
+    return debug.traceback(util._stringify_error(util._normalize_error(err)), 2)
+  end)
+  if not ok then
+    runtime.schedule(function()
+      error(traceback, 0)
+    end)
+  end
+end
+
+--- Add a callback to be run when the Future is done.
+---
+--- The callback is called with the arguments:
+--- - (`err: string`) - if the Future completed with an error.
+--- - (`nil`, `...:any`) - the results of the Future if it completed successfully.
+---
+--- If the Future is already done when this method is called, the callback is
+--- called immediately with the results.
+--- Callback errors are reported through the runtime scheduler with their
+--- traceback. Other observers still run and the Future's result is unchanged.
+--- @param callback fun(err?: any, ...: R...)
+--- @return fun() unsubscribe
+function Future:on_complete(callback)
+  if self:completed() then
+    -- Already completed or closed
+    self:_invoke(callback)
     return function() end
   end
 
@@ -48,8 +93,16 @@ function Future:on_complete(callback)
   end
 end
 
+--- Mark the Future as complete and set its result.
+---
+--- If an error is provided, the Future is marked as failed. Otherwise, it is
+--- marked as successful with the provided result.
+---
+--- A Future can only be completed once.
+---
+--- This will trigger any callbacks that are waiting on the Future.
 --- @param err? any
---- @param ... R...
+--- @param ... R... result
 function Future:complete(err, ...)
   if self:completed() then
     error('Future is already completed', 2)
@@ -64,19 +117,16 @@ function Future:complete(err, ...)
   local callbacks = self._callbacks
   self._callbacks = {}
 
-  local errs = {} -- Need to use pairs to avoid gaps caused by removed callbacks
+  -- Need to use pairs to avoid gaps caused by removed callbacks
   for _, cb in pairs(callbacks) do
-    local ok, cb_err = pcall(cb, err, ...)
-    if not ok then
-      errs[#errs + 1] = util._stringify_error(util._normalize_error(cb_err))
-    end
-  end
-
-  if #errs > 0 then
-    error(table.concat(errs, '\n'), 0)
+    self:_invoke(cb)
   end
 end
 
+--- Create a new future.
+---
+--- A Future is a low-level awaitable that is not intended to be used in
+--- application-level code.
 --- @return vim.async.Future<any>
 return function()
   return setmetatable({
diff --git a/test/functional/lua/async_spec.lua b/test/functional/lua/async_spec.lua
index 4a2c56348a93d4..45cd8add19716e 100644
--- a/test/functional/lua/async_spec.lua
+++ b/test/functional/lua/async_spec.lua
@@ -236,6 +236,111 @@ describe('async', function()
       }, results)
     end)
 
+    it_exec('on_complete reports callback errors separately from completion', function()
+      for _, already_completed in ipairs({ false, true }) do
+        local scheduled = {}
+        AsyncRuntime.config({
+          schedule = function(callback)
+            scheduled[#scheduled + 1] = callback
+          end,
+        })
+
+        local release --- @type fun(...)
+        local task = run(function()
+          return await(function(callback)
+            release = callback
+          end)
+        end)
+        if already_completed then
+          release('done', nil, 'last', nil)
+        end
+
+        task:on_complete(function()
+          error('CALLBACK_ERROR', 0)
+        end)
+        local observed
+        task:on_complete(function(...)
+          observed = vim.F.pack_len(...)
+        end)
+
+        if not already_completed then
+          local ok, err = pcall(release, 'done', nil, 'last', nil)
+          eq(true, ok, tostring(err))
+        end
+
+        eq({ n = 5, [2] = 'done', [4] = 'last' }, observed)
+        eq({ n = 4, [1] = 'done', [3] = 'last' }, vim.F.pack_len(task:wait(100)))
+        eq(1, #scheduled)
+        local ok, err = pcall(scheduled[1])
+        eq(false, ok)
+        assert(tostring(err):match('CALLBACK_ERROR'), tostring(err))
+        assert(tostring(err):match('stack traceback:'), tostring(err))
+        assert(tostring(err):match('async_spec.lua:%d+'), tostring(err))
+      end
+    end)
+
+    it_exec('on_complete callback errors do not fail the completing task', function()
+      local scheduled = {}
+      AsyncRuntime.config({
+        schedule = function(callback)
+          scheduled[#scheduled + 1] = callback
+        end,
+      })
+
+      local release --- @type fun()
+      local task = run(function()
+        await(function(callback)
+          release = callback
+        end)
+        error('TASK_ERROR', 0)
+      end)
+      task:raise_on_error()
+
+      eq(
+        'delivered',
+        run(function()
+          release()
+          return 'delivered'
+        end):wait(100)
+      )
+      check_task_err(task, 'TASK_ERROR')
+      eq(1, #scheduled)
+      local ok, err = pcall(scheduled[1])
+      eq(false, ok)
+      assert(tostring(err):match('TASK_ERROR'), tostring(err))
+    end)
+
+    it_exec('on_complete reports non-string callback errors', function()
+      local scheduled = {}
+      AsyncRuntime.config({
+        schedule = function(callback)
+          scheduled[#scheduled + 1] = callback
+        end,
+      })
+      local task = run(function() end)
+      task:on_complete(function()
+        error()
+      end)
+      task:on_complete(function()
+        error(false)
+      end)
+      task:on_complete(function()
+        error(setmetatable({}, {
+          __tostring = function()
+            error('TOSTRING_ERROR')
+          end,
+        }))
+      end)
+
+      eq(3, #scheduled)
+      for i, pattern in ipairs({ 'error%(nil%)', 'false', '<unprintable error>' }) do
+        local ok, err = pcall(scheduled[i])
+        eq(false, ok)
+        assert(tostring(err):match(pattern), tostring(err))
+      end
+      task:wait(100)
+    end)
+
     it_exec('child tasks start when the parent reaches a checkpoint', function()
       local results = {}
 
@@ -416,6 +521,109 @@ stack traceback:
     end)
   end)
 
+  describe('abandoned await callbacks', function()
+    it_exec('fails an abandoned await and frees the task after cleanup', function()
+      local holder = {}
+      local weak = setmetatable({}, { __mode = 'k' })
+      local result = {}
+      local limit = Async.semaphore(1)
+
+      local task = run(function()
+        local payload = {}
+        weak[payload] = true
+        limit:with(function()
+          await(function(cb)
+            holder.cb = cb
+            return add_handle('abandoned', vim.uv.new_timer())
+          end)
+        end)
+        return payload
+      end)
+      weak[task] = true
+      task:on_complete(function(err)
+        result.completed = true
+        result.err = err
+      end)
+
+      task = nil
+      holder.cb = nil
+      collectgarbage('collect')
+      collectgarbage('collect')
+      assert(
+        vim.wait(100, function()
+          return result.completed
+        end),
+        'abandoned await did not finish'
+      )
+      eq(p('^await callback was discarded'), result.err)
+      run(function()
+        limit:with(function() end)
+      end):wait(100)
+
+      -- LuaJIT traces can retain the completed task.
+      if jit then
+        jit.flush()
+      end
+      collectgarbage('collect')
+      collectgarbage('collect')
+      eq(nil, (next(weak)))
+      eq('', Async._inspect_tree())
+    end)
+
+    it_exec('can recover from an abandoned await while keeping resources usable', function()
+      local holder = {}
+      local file = assert(io.tmpfile())
+      local task = run(function(owned_file)
+        local ok, err = Async.pawait(2, function(value, cb)
+          eq('request', value)
+          holder.cb = cb
+        end, 'request')
+        eq(false, ok)
+        eq(p('^await callback was discarded'), err)
+        eq(false, Async.is_closing())
+        Async.checkpoint()
+
+        local written = owned_file:write('cleanup')
+        owned_file:close()
+        return written ~= nil
+      end, file)
+
+      file = nil
+      holder.cb = nil
+      collectgarbage('collect')
+      collectgarbage('collect')
+      eq(true, task:wait(100))
+    end)
+
+    it_exec('retains a task scope while a child callback can resume it', function()
+      local holder = {}
+      local result = {}
+
+      run('parent', function()
+        run('child', function()
+          result.value = await(function(cb)
+            holder.cb = cb
+          end)
+          collectgarbage('collect')
+          collectgarbage('collect')
+          Async.checkpoint()
+        end)
+      end):on_complete(function(err)
+        result.completed = true
+        result.err = err
+      end)
+
+      collectgarbage('collect')
+      collectgarbage('collect')
+      eq('parent [awaiting]\n└─ child [awaiting]', Async._inspect_tree())
+
+      holder.cb('done')
+      holder.cb = nil
+      eq({ value = 'done', completed = true }, result)
+      eq('', Async._inspect_tree())
+    end)
+  end)
+
   describe('task cancellation and closing', function()
     it_exec('can close tasks', function()
       local task = run(eternity)
@@ -463,6 +671,31 @@ stack traceback:
       check_task_err(child, 'closed')
     end)
 
+    it_exec('can cancel a task while it completes another task', function()
+      local resume_closer --- @type fun()
+      local closer --- @type vim.async.Task
+      local task = run(function()
+        local child = run(function()
+          await(function() end)
+        end)
+        closer = run(function()
+          await(function(callback)
+            resume_closer = callback
+          end)
+          child:close()
+        end)
+
+        Async.pawait(child)
+        -- The closer is still inside child:close() when this task resumes.
+        closer:close()
+        Async.pawait(closer)
+        return 'done'
+      end)
+      resume_closer()
+      eq('done', task:wait(100))
+      check_task_err(closer, 'closed')
+    end)
+
     it_exec('can timeout tasks', function()
       local task = run(eternity)
       check_task_err(task, 'timeout')
@@ -806,7 +1039,7 @@ stack traceback:
       --- @param task vim.async.Task
       --- @return integer
       local function get_task_callback_count(task)
-        --- @diagnostic disable-next-line: invisible
+        --- @diagnostic disable-next-line: access-invisible
         return vim.tbl_count(task._future._callbacks)
       end
 
@@ -861,7 +1094,7 @@ stack traceback:
         waiter:close()
         check_task_err(waiter, 'closed')
 
-        --- @diagnostic disable-next-line: invisible
+        --- @diagnostic disable-next-line: access-invisible
         local callback_count = vim.tbl_count(external._future._callbacks)
         external:close()
         check_task_err(external, 'closed')
@@ -883,7 +1116,7 @@ stack traceback:
 
         check_task_err(waiter, 'child error: .*async_spec.lua:%d+: CHILD ERROR')
 
-        --- @diagnostic disable-next-line: invisible
+        --- @diagnostic disable-next-line: access-invisible
         local callback_count = vim.tbl_count(external._future._callbacks)
         external:close()
         check_task_err(external, 'closed')
@@ -909,7 +1142,7 @@ stack traceback:
         check_task_err(parent, 'closed')
         eq(false, child:completed())
 
-        --- @diagnostic disable-next-line: invisible
+        --- @diagnostic disable-next-line: access-invisible
         local callback_count = vim.tbl_count(child._future._callbacks)
         child:close()
         check_task_err(child, 'closed')
@@ -2572,21 +2805,33 @@ stack traceback:
     end)
 
     it_exec('normalizes nil future callback errors', function()
+      local report --- @type fun()
+      AsyncRuntime.config({
+        schedule = function(callback)
+          report = callback
+        end,
+      })
       local future = require('vim.async._future')()
       future:on_complete(function()
         error()
       end)
 
-      local ok, err = pcall(function()
-        future:complete(nil, 'value')
-      end)
+      future:complete(nil, 'value')
+      eq({ true, 'value' }, { future:result() })
 
+      local ok, err = pcall(report)
       eq(false, ok)
       --- @cast err string
       assert(err:match('error%(nil%)'), 'Unexpected error: ' .. tostring(err))
     end)
 
     it_exec('continues future callbacks after an unprintable error', function()
+      local report --- @type fun()
+      AsyncRuntime.config({
+        schedule = function(callback)
+          report = callback
+        end,
+      })
       local future = require('vim.async._future')()
       local observed = false
       local unprintable = setmetatable({}, {
@@ -2602,12 +2847,12 @@ stack traceback:
         observed = true
       end)
 
-      local ok, err = pcall(function()
-        future:complete(nil, 'value')
-      end)
+      future:complete(nil, 'value')
+      eq({ true, 'value' }, { future:result() })
+      eq(true, observed)
 
+      local ok, err = pcall(report)
       eq(false, ok)
-      eq(true, observed)
       assert(tostring(err):match('<unprintable error>'), 'Unexpected error: ' .. tostring(err))
     end)
 

```

# REVIEW A

# Review of neovim/neovim#42595: handle async completion errors and discarded callbacks

The PR is already merged with one approval. I read the diff only and did not run the tests. The three fixes are well-scoped, each is documented, and each has tests. The notes below are mostly follow-ups.

## What the PR does well
- **Nested cancellation:** `Task:_raise` now defers when the status is `normal` as well as `running`. This closes the "resume a coroutine that is still active beneath another" bug. The regression test, "can cancel a task while it completes another task", reproduces the nesting.
- **Callback errors:** `Future:_invoke` runs each observer under `xpcall`. A throwing observer no longer escapes into the code that completes the task, no longer stops later observers, and no longer changes the result. The old code collected errors and rethrew them after the loop. The traceback is captured at the throw site, and non-string errors (`nil`, `false`, an unprintable `__tostring`) are normalized. Tests cover both the already-completed and the pending paths.
- **Discarded callbacks:** `threads` is no longer weak, so an unfinished task can't be collected out from under its resources. A GC proxy fails the wait if the callback is collected.
- **Documentation:** The user-facing docs say plainly that GC timing is unpredictable and that `Task:close()` or `timeout()` is the reliable way to cancel.

## Potential issues and questions

1. **`norm_cb_fun` thunk is now single-use** (`_core.lua`, around line 920).
   - The thunk sets `args = nil` and calls `assert(args)`, so a second invocation fails with a bare assertion error.
   - That is fine if each `await(argc, fun, ...)` builds a fresh thunk. I couldn't confirm from the diff that no caller can reuse one. `Async.wrap`-style helpers, retries and `pawait` loops are the places to check.
   - If reuse is possible, `args` needs to be copied rather than consumed.
   - If it isn't, `assert(args, 'callback thunk can only be invoked once')` would give a clearer failure.

2. **`runtime.schedule` is called from inside a `__gc` finalizer** (`_core.lua`, around line 641).
   - The comment says the failure is delivered "outside GC", but the schedule call itself runs in the finalizer.
   - With the default `vim.schedule` that is cheap and safe. `AsyncRuntime.config({ schedule = ... })` accepts a user-supplied function, which would then run arbitrary Lua during GC.
   - Either document that the scheduler must be GC-safe, or have the finalizer only set a flag or enqueue to a plain table that something else drains.

3. **Strong `threads` table needs an explicit removal on every exit path.**
   - The diff doesn't show where entries are removed. I'd confirm that completion, close, error and setup-failure paths all clear the entry.
   - The new `_inspect_tree() == ''` assertions cover only the paths the tests exercise.
   - A pending wait whose callback is still reachable (for example stored in task data) now leaks by design. That is documented, but it is a behavior change from the weak table.

4. **The scheduled `complete_await('await callback was discarded')` is unguarded.**
   - It checks `settled` and `task:completed()` when the finalizer runs, but not again when the scheduled function runs.
   - Something could settle the await in between, such as `close()` or a timeout. This is safe only if `complete_await` is idempotent, so it's worth confirming or adding a recheck.

5. **Minor doc and annotation nits** (`_future.lua`):
   - "Error result of the task is an error occurs" should read "if an error occurs".
   - The comments say "task" where they mean "Future".
   - A typographic apostrophe appears in "Future’s".
   - Because these blocks are "Generated from async.nvim", the fixes belong upstream, or the sync will overwrite them.

6. **Diagnostic rename:** `invisible` became `access-invisible` across the file. It's a harmless sync from the lua-ls version, but it is unrelated churn.

## Performance
- Each `await` now allocates a `newproxy` userdata, one closure and a metatable. That is small, but it sits on a hot path.
- `Future:_invoke` adds an `xpcall` and a closure per observer. That is negligible next to the correctness gain.

## Security
There are no security concerns. Errors are reported rather than swallowed, and no new external input is handled.

## Test coverage
- Coverage is good for the error paths, nested cancellation, discarded-callback recovery via `pawait`, and scope retention while a child callback is live.
- **Possible flakiness:** the GC tests depend on `collectgarbage('collect')` running twice and on LuaJIT trace retention. The `jit.flush()` fix suggests this was already hit once. Running them under both LuaJIT and PUC Lua in CI, ideally repeated, would give more confidence.
- **Missing tests:**
  - A reused `norm_cb_fun` thunk (issue 1).
  - The race in issue 4, where a task is closed or settled between GC and the scheduled failure.
  - A custom `schedule` that throws or reenters.

## Verdict
This is a sound, well-documented fix. The only item I'd chase is issue 1, because it could be a latent regression. Issues 2 and 4 are small hardening changes.

# REVIEW B

# Review of neovim/neovim#42595: handle async completion errors and discarded callbacks

The PR is already merged and approved. This review is based on reading the diff only. I did not build it or run the tests.

## Summary
The PR ports three fixes from async.nvim:
- **Nested cancellation:** `Task:_raise` now defers when the task status is `normal`, not only `running`.
- **Completion callback errors:** `Future:_invoke` catches them and reports them through `runtime.schedule` with a traceback. They no longer escape into the code that completes the task.
- **Discarded await callbacks:** the callback handed to an await is wrapped in a GC sentinel. If it is collected before it is called, the task fails with "await callback was discarded". The `threads` table is now strong so unfinished tasks stay alive.

The design is coherent, the commits are split sensibly, and the docs match the behavior.

## Correctness and potential issues
1. **`norm_cb_fun` is now single-use** (`_core.lua`, around the `args = nil` line).
   - The thunk sets `args = nil` on its first call, so a second call hits `assert(args)` and fails with an unhelpful "assertion failed!".
   - Calling it twice is unusual. It could still happen if something retries the setup function.
   - A clearer `error('await setup called more than once')` would be easier to debug.
   - A comment saying the thunk is single-use would also help.

2. **The `threads` table is now strong.**
   - This is intentional, but any task that never completes and never has its callback collected stays in `threads` for the life of the session.
   - A `Future:on_complete` callback or a `vim.uv` handle holds its callback strongly, so a task waiting on a live handle behaves as expected.
   - I could not see in the diff that `threads[co]` is cleared when a task finishes. Please confirm that cleanup happens on every completion path, including close and error. Otherwise this becomes a leak. `Async._inspect_tree()` returning `''` in the tests suggests it works.

3. **GC-triggered failure ordering.**
   - The `__gc` handler checks `not settled and not task:completed()`, then schedules `complete_await(...)`.
   - If the task is closed between the GC and the scheduled turn, `complete_await` has to be a safe no-op. The `settled` guard probably covers this, but there is no direct test for "closed after GC, before delivery".

4. **`newproxy`-based `_gc_fun`.**
   - This only works on LuaJIT and PUC Lua 5.1, which is fine for Neovim today.
   - `util.lua` is marked "Generated from async.nvim", so keep it in sync there. Any future Lua 5.2+ support would need `__gc` on a table instead.

5. **Error reporting changes `Future:complete` semantics.**
   - Callers that relied on `complete()` throwing when an observer failed no longer get that.
   - The tests were updated, and I saw no other in-tree users in the diff. This is a behavior change that goes beyond a bugfix, so it is worth a mention in the changelog or `news.txt` if `vim.async` is user-facing.

6. **Minor points.**
   - `_err` changed from `private` to `package` in the annotations. Ideally that is explained.
   - The `invisible` to `access-invisible` diagnostic rename and the added Future doc comments are unrelated drive-by changes. They are harmless, and they come from the upstream sync.
   - `debug.traceback(..., 2)` in the xpcall handler: the traceback level is relative to the handler, so the trace may include a frame or two of internals. The test asserts `async_spec.lua:%d+` is present, which is good.

## Performance
- Each await now allocates a userdata proxy, a metatable and a wrapper closure. That is small, but it applies to every `await(function(cb) ...)`.
- Error handling uses `xpcall` plus a closure per observer on every completion. This is negligible next to the event-loop cost.
- `pairs(callbacks)` iteration is unchanged.

## Security
No concerns. The change is internal scheduling and error plumbing. The only new surface is `newproxy`/`__gc`, and the finalizer defers real work to the scheduler instead of running it inside GC. That is the right approach.

## Tests
Coverage is good:
- on_complete errors, both when the task is already complete and when it completes later
- non-string, `nil` and unprintable errors
- a completing task not failing because an observer failed
- nested cancel while completing another task
- abandoned-callback failure with resource and semaphore cleanup
- `pawait` recovery
- retention while a child can still resume

Concerns and gaps:
- **GC tests may be flaky.** They depend on `collectgarbage` and JIT traces. The `jit.flush()` mitigation is a good sign, but watch CI on PUC Lua, ASAN and other slow configurations. The two `collectgarbage('collect')` calls are a common idiom, but they are not a guarantee for finalizers, which can run one cycle late.
- **Missing tests:**
  - `norm_cb_fun` with a callback that is called normally and then collected, to confirm there is no spurious failure.
  - A callback called twice.
  - A task closed after the GC but before the scheduled error.
- **Nit:** the `scheduled` capture pattern is repeated in several tests. A small helper would reduce the duplication.

## Verdict
This is a solid fix with good docs and thorough tests. I would address two things in a follow-up:
- Give a clear error for repeated calls of the `norm_cb_fun` thunk.
- Add a test for the callback-called-then-collected path.

I would also confirm that `threads` entries are removed on every completion path.
