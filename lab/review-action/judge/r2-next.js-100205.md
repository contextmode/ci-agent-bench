# PR diff (the real change)

```diff
diff --git a/turbopack/crates/turbopack-trace-server/src/reader/turbopack.rs b/turbopack/crates/turbopack-trace-server/src/reader/turbopack.rs
index e486048ddf8..6f5270dc11d 100644
--- a/turbopack/crates/turbopack-trace-server/src/reader/turbopack.rs
+++ b/turbopack/crates/turbopack-trace-server/src/reader/turbopack.rs
@@ -65,8 +65,9 @@ pub struct TurbopackFormat {
     remaining_ids_to_drop: usize,
     queued_rows: FxHashMap<u64, Vec<InternalRow>>,
     outdated_spans: FxHashSet<SpanIndex>,
-    thread_stacks: FxHashMap<u64, Vec<u64>>,
-    self_time_started: FxHashMap<(u64, u64), Timestamp>,
+    // Each entry is a separate enter, even when the same span re-enters itself.
+    // Only the top frame has an active self-time start; suspended frames have None.
+    thread_stacks: FxHashMap<u64, Vec<(u64, Option<Timestamp>)>>,
     interner: RcStrInterning,
 }
 
@@ -84,7 +85,6 @@ impl TurbopackFormat {
             queued_rows: FxHashMap::with_capacity_and_hasher(1_024, Default::default()),
             outdated_spans: FxHashSet::with_capacity_and_hasher(8_192, Default::default()),
             thread_stacks: FxHashMap::with_capacity_and_hasher(64, Default::default()),
-            self_time_started: FxHashMap::with_capacity_and_hasher(256, Default::default()),
             interner: RcStrInterning::new(),
         }
     }
@@ -162,27 +162,19 @@ impl TurbopackFormat {
                 }
                 let ts = Timestamp::from_micros(ts);
                 let stack = self.thread_stacks.entry(thread_id).or_default();
-                if let Some(&parent) = stack.last() {
-                    if let Some(parent_start) = self.self_time_started.remove(&(parent, thread_id))
-                    {
-                        stack.push(id);
-                        self.process_internal_row(
-                            store,
-                            InternalRow {
-                                id: Some(parent),
-                                ty: InternalRowType::SelfTime {
-                                    start: parent_start,
-                                    end: ts,
-                                },
-                            },
-                        );
-                    } else {
-                        stack.push(id);
-                    }
-                } else {
-                    stack.push(id);
+                let parent_slice = stack
+                    .last_mut()
+                    .and_then(|(parent, start)| start.take().map(|start| (*parent, start)));
+                stack.push((id, Some(ts)));
+                if let Some((parent, start)) = parent_slice {
+                    self.process_internal_row(
+                        store,
+                        InternalRow {
+                            id: Some(parent),
+                            ty: InternalRowType::SelfTime { start, end: ts },
+                        },
+                    );
                 }
-                self.self_time_started.insert((id, thread_id), ts);
             }
             TraceRow::Exit {
                 ts,
@@ -196,22 +188,24 @@ impl TurbopackFormat {
                 }
                 let ts = Timestamp::from_micros(ts);
                 let stack = self.thread_stacks.entry(thread_id).or_default();
-                if let Some(pos) = stack.iter().rev().position(|&x| x == id) {
-                    let stack_index = stack.len() - pos - 1;
-                    stack.remove(stack_index);
-                    if stack_index > 0 {
-                        let parent = stack[stack_index - 1];
-                        self.self_time_started.insert((parent, thread_id), ts);
+                if let Some(stack_index) = stack.iter().rposition(|&(frame_id, _)| frame_id == id) {
+                    let (_, start) = stack.remove(stack_index);
+                    // A non-LIFO exit removes a suspended frame. The current top
+                    // keeps running, so no other frame should be resumed yet.
+                    if stack_index == stack.len()
+                        && let Some((_, parent_start)) = stack.last_mut()
+                    {
+                        *parent_start = Some(ts);
+                    }
+                    if let Some(start) = start {
+                        self.process_internal_row(
+                            store,
+                            InternalRow {
+                                id: Some(id),
+                                ty: InternalRowType::SelfTime { start, end: ts },
+                            },
+                        );
                     }
-                }
-                if let Some(start) = self.self_time_started.remove(&(id, thread_id)) {
-                    self.process_internal_row(
-                        store,
-                        InternalRow {
-                            id: Some(id),
-                            ty: InternalRowType::SelfTime { start, end: ts },
-                        },
-                    );
                 }
             }
             TraceRow::Event { ts, parent, values } => {
@@ -274,7 +268,7 @@ impl TurbopackFormat {
         allocations: Allocations,
     ) {
         let stack = self.thread_stacks.entry(thread_id).or_default();
-        if let Some(&id) = stack.last() {
+        if let Some(&(id, _)) = stack.last() {
             if allocations.allocations > 0 {
                 self.process_internal_row(
                     store,
@@ -507,7 +501,9 @@ mod tests {
 
     use crate::{
         reader::{TraceFormat, turbopack::TurbopackFormat},
+        span::SpanEvent,
         store_container::StoreContainer,
+        timestamp::Timestamp,
     };
 
     fn start(id: u64, parent: Option<u64>, name: &'static str) -> TraceRow<'static> {
@@ -559,6 +555,334 @@ mod tests {
             .collect()
     }
 
+    fn enter(ts: u64, id: u64, thread_id: u64) -> TraceRow<'static> {
+        TraceRow::Enter {
+            ts,
+            id,
+            thread_id,
+            allocations: None,
+        }
+    }
+
+    fn exit(ts: u64, id: u64, thread_id: u64) -> TraceRow<'static> {
+        TraceRow::Exit {
+            ts,
+            id,
+            thread_id,
+            allocations: None,
+        }
+    }
+
+    fn encode(rows: &[TraceRow<'_>]) -> Vec<u8> {
+        rows.iter()
+            .flat_map(|row| postcard::to_stdvec(row).unwrap())
+            .collect()
+    }
+
+    fn ingest(format: &mut TurbopackFormat, rows: &[TraceRow<'_>]) {
+        let data = encode(rows);
+        assert_eq!(
+            format
+                .read(&data, &mut TurbopackFormat::create_reused())
+                .unwrap(),
+            data.len()
+        );
+    }
+
+    /// Check both representations of the positive slices, their per-span self-time,
+    /// and the total CPU time used by the flame view. Timestamps are in microseconds.
+    fn assert_slices(format: &TurbopackFormat, expected: &[(u64, u64, u64)]) {
+        let store = format.store.read();
+        let mut expected: Vec<_> = expected
+            .iter()
+            .map(|&(id, start, end)| {
+                (
+                    format.id_mapping[&id].get(),
+                    Timestamp::from_micros(start),
+                    Timestamp::from_micros(end),
+                )
+            })
+            .collect();
+        expected.sort_unstable();
+        let mut events = Vec::new();
+        for i in 0..store.spans.len() {
+            let span = &store.spans[i];
+            for event in span.events.iter() {
+                if let SpanEvent::SelfTime(slice) = event {
+                    events.push((i, slice.start, slice.end()));
+                }
+            }
+            let self_time: Timestamp = expected
+                .iter()
+                .filter(|&&(id, _, _)| id == i)
+                .map(|&(_, start, end)| end - start)
+                .sum();
+            assert_eq!(span.time_data.self_time, self_time, "span {i}");
+        }
+        events.sort_unstable();
+        assert_eq!(events, expected, "stored self-time events");
+        let mut tree_slices = Vec::new();
+        store.self_time_tree.as_ref().unwrap().for_each_in_range(
+            Timestamp::ZERO,
+            Timestamp::MAX,
+            &mut |start, end, id| tree_slices.push((id.get(), start, end)),
+        );
+        tree_slices.sort_unstable();
+        assert_eq!(tree_slices, expected, "self-time tree");
+        let total: Timestamp = expected.iter().map(|&(_, start, end)| end - start).sum();
+        assert_eq!(store.root_span().total_time(), total, "flame CPU total");
+    }
+
+    #[test]
+    fn same_span_reentry_keeps_every_frame_slice() {
+        for depth in [2, 3] {
+            let store = Arc::new(StoreContainer::new());
+            let mut format = TurbopackFormat::new(store);
+            let mut rows = vec![start(1, None, "span")];
+            for i in 0..depth {
+                rows.push(enter(10 + i * 10, 1, 1));
+            }
+            for i in 0..depth {
+                rows.push(exit(10 + (depth + i) * 10, 1, 1));
+            }
+            ingest(&mut format, &rows);
+            let expected: Vec<_> = (0..depth * 2 - 1)
+                .map(|i| (1, 10 + i * 10, 20 + i * 10))
+                .collect();
+            assert_slices(&format, &expected);
+        }
+    }
+
+    #[test]
+    fn same_span_reentry_interleaved_with_child() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "parent"),
+                start(2, Some(1), "child"),
+                enter(10, 1, 1),
+                enter(20, 1, 1),
+                enter(30, 2, 1),
+                exit(40, 2, 1),
+                exit(50, 1, 1),
+                exit(60, 1, 1),
+            ],
+        );
+        assert_slices(
+            &format,
+            &[
+                (1, 10, 20),
+                (1, 20, 30),
+                (2, 30, 40),
+                (1, 40, 50),
+                (1, 50, 60),
+            ],
+        );
+    }
+
+    #[test]
+    fn same_span_on_two_threads_has_independent_frames() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "span"),
+                enter(10, 1, 1),
+                enter(15, 1, 2),
+                enter(20, 1, 1),
+                exit(30, 1, 1),
+                exit(35, 1, 2),
+                exit(40, 1, 1),
+            ],
+        );
+        assert_slices(
+            &format,
+            &[(1, 10, 20), (1, 20, 30), (1, 30, 40), (1, 15, 35)],
+        );
+        let store = format.store.read();
+        assert_eq!(
+            store.root_span().corrected_total_time(),
+            Timestamp::from_micros(30)
+        );
+    }
+
+    #[test]
+    fn non_lifo_exit_does_not_resume_a_suspended_parent() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "outer"),
+                start(2, Some(1), "middle"),
+                start(3, Some(2), "inner"),
+                enter(10, 1, 1),
+                enter(20, 2, 1),
+                enter(30, 3, 1),
+                exit(40, 2, 1),
+                exit(50, 3, 1),
+                exit(60, 1, 1),
+            ],
+        );
+        assert_slices(
+            &format,
+            &[(1, 10, 20), (2, 20, 30), (3, 30, 50), (1, 50, 60)],
+        );
+    }
+
+    #[test]
+    fn non_lifo_exit_removes_the_most_recent_matching_frame() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "outer"),
+                start(2, Some(1), "inner"),
+                enter(10, 1, 1),
+                enter(20, 1, 1),
+                enter(30, 2, 1),
+                exit(40, 1, 1),
+                exit(50, 2, 1),
+                exit(60, 1, 1),
+            ],
+        );
+        assert_slices(
+            &format,
+            &[(1, 10, 20), (1, 20, 30), (2, 30, 50), (1, 50, 60)],
+        );
+    }
+
+    #[test]
+    fn non_lifo_exit_can_remove_the_bottom_frame() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "outer"),
+                start(2, Some(1), "inner"),
+                enter(10, 1, 1),
+                enter(20, 2, 1),
+                start(3, Some(2), "child"),
+                enter(30, 3, 1),
+                exit(40, 2, 1),
+                exit(45, 1, 1),
+                exit(50, 3, 1),
+            ],
+        );
+        assert_slices(&format, &[(1, 10, 20), (2, 20, 30), (3, 30, 50)]);
+    }
+
+    #[test]
+    fn unmatched_exit_leaves_active_frames_unchanged() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "span"),
+                exit(5, 1, 1),
+                enter(10, 1, 1),
+                exit(20, 99, 1),
+                exit(25, 1, 2),
+                exit(30, 1, 1),
+                exit(40, 1, 1),
+            ],
+        );
+        assert_slices(&format, &[(1, 10, 30)]);
+    }
+
+    #[test]
+    fn live_trace_with_partial_exit_preserves_the_resumed_frame() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        let mut reuse = TurbopackFormat::create_reused();
+        let prefix = encode(&[
+            start(1, None, "span"),
+            enter(10, 1, 1),
+            enter(20, 1, 1),
+            exit(30, 1, 1),
+        ]);
+        let final_row = encode(&[exit(40, 1, 1)]);
+        let mut data = prefix.clone();
+        data.extend_from_slice(&final_row[..final_row.len() - 1]);
+        let consumed = format.read(&data, &mut reuse).unwrap();
+        assert_eq!(consumed, prefix.len());
+        assert_slices(&format, &[(1, 10, 20), (1, 20, 30)]);
+        assert_eq!(format.read(&[], &mut reuse).unwrap(), 0);
+        data.push(*final_row.last().unwrap());
+        assert_eq!(
+            format.read(&data[consumed..], &mut reuse).unwrap(),
+            final_row.len()
+        );
+        assert_slices(&format, &[(1, 10, 20), (1, 20, 30), (1, 30, 40)]);
+    }
+
+    #[test]
+    fn reentry_self_time_waits_for_queued_parent() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        ingest(
+            &mut format,
+            &[
+                start(2, Some(1), "child"),
+                enter(10, 2, 1),
+                enter(20, 2, 1),
+                exit(30, 2, 1),
+                exit(40, 2, 1),
+            ],
+        );
+        assert!(!format.queued_rows.is_empty());
+        ingest(&mut format, &[start(1, None, "parent")]);
+        assert!(format.queued_rows.is_empty());
+        assert_slices(&format, &[(2, 10, 20), (2, 20, 30), (2, 30, 40)]);
+    }
+
+    #[test]
+    fn dropped_reentered_span_does_not_contribute_self_time() {
+        let mut format = TurbopackFormat::new(Arc::new(StoreContainer::new()));
+        // Exercise DROP_SPANS without changing the process-wide environment.
+        format.remaining_ids_to_drop = 1;
+        ingest(
+            &mut format,
+            &[
+                start(1, None, "parent"),
+                start(2, Some(1), "dropped"),
+                enter(10, 1, 1),
+                enter(20, 2, 1),
+                enter(30, 2, 1),
+                exit(40, 2, 1),
+                exit(50, 2, 1),
+                exit(60, 1, 1),
+            ],
+        );
+        assert!(format.dropped_ids.contains(&2));
+        assert_slices(&format, &[(1, 10, 20), (1, 50, 60)]);
+    }
+
+    #[test]
+    fn attributes_allocations_during_same_span_reentry() {
+        let rows = [
+            start(1, None, "span"),
+            enter(10, 1, 1),
+            TraceRow::Enter {
+                ts: 20,
+                id: 1,
+                thread_id: 1,
+                allocations: allocations(100, 20),
+            },
+            TraceRow::Exit {
+                ts: 30,
+                id: 1,
+                thread_id: 1,
+                allocations: allocations(50, 30),
+            },
+            TraceRow::Exit {
+                ts: 40,
+                id: 1,
+                thread_id: 1,
+                allocations: allocations(70, 40),
+            },
+        ];
+        assert_eq!(read(&rows, &["span"]), vec![(220, 22, 90)]);
+    }
+
     #[test]
     fn attributes_allocations_of_enter_and_exit_rows() {
         let enter = |ts, id, allocations| TraceRow::Enter {

```

# REVIEW A

# Review of PR #100205: Fix binary trace self-time on same-span re-entry

The PR is already merged and has an approval from sokra. This is a retrospective review. I read the diff and PR description but didn't build the code or run the tests.

## Summary
The old reader kept self-time start times in `self_time_started`, keyed by `(span_id, thread_id)`. When a span re-entered itself on one thread, the inner Exit restarted the outer frame's clock under that same key and then removed the key right away. The outer frame's remaining work was lost. The PR removes that map. Each per-thread stack frame is now `(span_id, Option<Timestamp>)`, and only the top frame holds an active start.

## Code quality
- **The fix addresses the root cause.** Tying the clock to the frame instead of to a shared map key removes the aliasing, so the design is simpler and more robust than a patch on the old structure. It also drops one hash map and two lookups from the Enter/Exit hot path.
- **The invariant is easy to check.** Enter closes the top's slice and pushes a new running frame. Exit removes the most recent matching frame (`rposition`). It resumes the new top only when the removed frame was the top (`stack_index == stack.len()` after removal). Non-LIFO exits remove a suspended frame (`start == None`) without emitting a row or touching other clocks. Unmatched exits do nothing.
- **Order of operations in Enter is safe.** The new frame is pushed before `process_internal_row` is called. That call can queue rows for a parent that hasn't arrived yet, and it doesn't read `thread_stacks`.
- **Comments are helpful.** The struct comment and the non-LIFO comment explain the non-obvious invariants.
- **The `if … && let …` chain** needs Rust edition 2024. The crate evidently builds with it, since the PR reports passing cargo test and clippy.

## Potential bugs and edge cases
These are minor, and none of them blocks the change.
1. **Stacks can still grow without bound.** If an Enter never gets a matching Exit, for example from a truncated live trace or a lost row, the frame stays on the thread stack. Its `Option<Timestamp>` also stays set if it was on top. This behaviour existed before, and the tests cover live input with a partial final row. A debug assertion or a metric for unexpectedly deep stacks might still be worth adding.
2. **The same non-LIFO case has a visible side effect.** If a non-top frame exits, the new top keeps its existing clock, which is the intended behaviour. But the exiting frame's own slice ends at `ts` even though it was suspended (`start == None`), so no slice is emitted for it. This follows from "suspended frames have no active clock" and the tests lock it in, but it could be called out in the docs for the format.
3. **Metrics will shift.** As the PR notes, flame CPU, self time, corrected time and concurrency numbers all change for existing traces that contain re-entry. That is the intent, but anything that compares trace output across versions, such as dashboards or snapshot tests elsewhere, may need a heads-up.

## Performance
- The hash map is gone, which is a small win. `Vec<(u64, Option<Timestamp>)>` entries are bigger than the old `u64` entries (probably 24 bytes against 8), but stacks are shallow, so this has no practical effect.
- `rposition` scans from the top. It is O(1) in the usual LIFO case and linear only for non-LIFO exits.
- The PR reports about 109k same-span re-entries across 652k pairs in a real trace, so the new path is exercised heavily and the validation was meaningful.

## Security
Nothing of concern. The change only touches the parsing of a local trace file, and it takes no new input and reads no headers. Indexing goes through `rposition` and `remove`, with no unchecked indexing.

## Test coverage
Coverage is strong:
- It covers same-span nesting at depth 2 and 3, and interleaving with a child span.
- It covers two threads running the same span, including the `corrected_total_time` check.
- It covers non-LIFO exits: suspended parent, most-recent-match, and removing the bottom frame.
- It covers unmatched exits, a live trace with a partial final row, and queued parents.
- It covers `DROP_SPANS`, done by setting `remaining_ids_to_drop` directly, which avoids mutating the process-wide environment.
- It covers allocation attribution during re-entry.
- The `assert_slices` helper checks four things at once: stored events, the self-time tree, per-span self time, and total CPU. This makes the tests hard to pass by accident.
- The PR says five of the new cases failed against the old reader, and it independently reconciled 1.1M slices against a standalone decoder.

Possible additions:
- A test with a longer mixed sequence of enter and exit orders, such as a small randomized or property test checking that total slice time never exceeds wall time per thread.
- A check that slices on one thread never overlap.

## Verdict
This is a good fix. The root cause is addressed, the code is simpler, and the tests are thorough. I have no blocking concerns. The suggestions above are optional follow-ups.

One process note: the PR says `pnpm build-all` couldn't run because `node_modules` was missing. That's fine here, since the change is Rust-only and the relevant cargo checks passed.

# REVIEW B

# Review of PR #100205: Fix binary trace self-time on same-span re-entry

The PR is already merged and approved by sokra. I read the diff only and did not build or run the tests.

## Summary
The old reader kept self-time clocks in `self_time_started: FxHashMap<(span_id, thread_id), Timestamp>`. When a span re-entered itself on one thread, the inner Exit removed the key the outer frame was also using. The outer frame's remaining slice was lost. The PR drops that map. Each per-thread stack frame is now `(span_id, Option<Timestamp>)`, and the `Option` holds the active slice start.

## Correctness
The new logic looks right to me.
- **Enter:** the current top's slice is closed at `ts` and a new frame is pushed with `Some(ts)`. `stack.last_mut()...start.take()` is read before the push, so the borrow and ordering are fine.
- **Exit:** `rposition` finds the most recent matching frame, matching the old `rev().position()` semantics.
  - Exiting a suspended frame (`start == None`) emits nothing and resumes nothing, which fixes the old behavior of restarting a parent's clock out of order.
  - The parent is resumed only when `stack_index == stack.len()` after the removal, meaning the exited frame was on top. This also covers removing the bottom frame, since `stack.last_mut()` is `None` when the stack becomes empty.
  - The slice for the exiting frame is emitted after the resume, so the parent's start is `ts` and the exiting slice ends at `ts`. There is no overlap and no gap.
- **Allocations:** `stack.last()` is destructured as `&(id, _)`, so attribution is unchanged.
- **Unmatched exit:** it is a no-op. The old code might have removed a stale `self_time_started` entry in that case, but with the new structure nothing is left to go stale.

## Quality
- Removing the second map means one lookup instead of several per Enter/Exit, and the state can no longer be inconsistent between the stack and the clock map. That is both simpler and faster on a hot path. For non-LIFO exits, `Vec::remove` is O(depth), which is the same as before.
- The let-chain in the Exit branch (`if ... && let Some(..)`) needs edition 2024. The repo already uses that, and the PR reports clippy and fmt passing.
- The comment on `thread_stacks` explains the invariant that only the top frame has an active start, which is helpful.

## Tests
Coverage is strong, and `assert_slices` checks several things at once:
- stored events
- the per-span `self_time`
- `self_time_tree`
- the flame CPU total

The cases cover:
- depth 2 and 3 re-entry
- child interleaving
- cross-thread independence, including `corrected_total_time`
- three non-LIFO variants
- unmatched exits
- a partial trailing row on a live trace
- queued parents
- `DROP_SPANS`
- allocations

Nits, none blocking:
- The `DROP_SPANS` test sets `remaining_ids_to_drop` directly instead of going through the env var. The comment explains why, but the env-var parsing path stays untested.
- `assert_slices` is O(spans × slices), which is fine at this size.
- The allocation test uses the existing `read` helper and a single magic tuple, `(220, 22, 90)`. A short comment on how that value is derived would help future readers.

## Other
- **Performance:** no concerns, as noted above.
- **Security:** none. This is an offline trace-reader change and adds no new header or input surface.
- **Behavior change:** the PR says flame CPU, self-time, and concurrency metrics will shift because lost slices are now counted. It states this up front. A changelog or release note for the trace-viewer consumers would be useful if such a place exists.
- **Verification:** the independent decoder cross-check, a 1.1M-slice multiset match, is unusually thorough.

I found no blocking issues.
