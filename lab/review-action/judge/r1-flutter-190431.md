# PR diff (the real change)

```diff
diff --git a/packages/flutter/lib/src/rendering/object.dart b/packages/flutter/lib/src/rendering/object.dart
index e5e8d8a47d1c6..67f55e61b22f1 100644
--- a/packages/flutter/lib/src/rendering/object.dart
+++ b/packages/flutter/lib/src/rendering/object.dart
@@ -6599,9 +6599,13 @@ class _RenderObjectSemantics extends _SemanticsFragment with DiagnosticableTreeM
   }
 
   void _marksConflictsInMergeGroup(List<_SemanticsFragment> mergeGroup, {bool isMergeUp = false}) {
+    final wasConflicting = <_RenderObjectSemantics>{};
     final hasSiblingConflict = <_SemanticsFragment>{};
     for (var i = 0; i < mergeGroup.length; i += 1) {
       final _SemanticsFragment fragment = mergeGroup[i];
+      if (fragment is _RenderObjectSemantics && fragment._hasSiblingConflict) {
+        wasConflicting.add(fragment);
+      }
       // Remove old value
       fragment.markSiblingConfigurationConflict(false);
       if (fragment.configToMergeUp == null) {
@@ -6619,8 +6623,18 @@ class _RenderObjectSemantics extends _SemanticsFragment with DiagnosticableTreeM
         }
       }
     }
+    // A sibling conflict feeds shouldFormSemanticsNode, so gaining or losing one
+    // changes whether the fragment produces a semantics node of its own. What it
+    // has cached is stale until it is rebuilt.
     for (final fragment in hasSiblingConflict) {
       fragment.markSiblingConfigurationConflict(true);
+      if (fragment is _RenderObjectSemantics && !wasConflicting.remove(fragment)) {
+        fragment.markNeedsBuild();
+      }
+    }
+    // Whatever is left in wasConflicting stopped conflicting in this pass.
+    for (final fragment in wasConflicting) {
+      fragment.markNeedsBuild();
     }
   }
 
diff --git a/packages/flutter/test/widgets/overlay_portal_test.dart b/packages/flutter/test/widgets/overlay_portal_test.dart
index 04f2152e7912f..b88231ef1cc7f 100644
--- a/packages/flutter/test/widgets/overlay_portal_test.dart
+++ b/packages/flutter/test/widgets/overlay_portal_test.dart
@@ -3242,6 +3242,60 @@ void main() {
         ),
       );
     });
+
+    // Regression test for https://github.com/flutter/flutter/issues/189902 and
+    // https://github.com/flutter/flutter/issues/187198.
+    testWidgets('toggling an overlay child does not leave a parentless attached semantics node', (
+      WidgetTester tester,
+    ) async {
+      final controller = OverlayPortalController();
+      final siblingController = OverlayPortalController();
+
+      // A second anchor is required: the fragment whose conflict changes is the
+      // sibling's, not the one belonging to the portal being toggled.
+      final Widget sibling = OverlayPortal.overlayChildLayoutBuilder(
+        controller: siblingController,
+        overlayChildBuilder: (BuildContext context, OverlayChildLayoutInfo info) =>
+            const SizedBox.shrink(),
+        child: Semantics(explicitChildNodes: true, child: const Text('sibling')),
+      );
+
+      Widget portal = OverlayPortal.overlayChildLayoutBuilder(
+        controller: controller,
+        overlayChildBuilder: (BuildContext context, OverlayChildLayoutInfo info) =>
+            const Align(alignment: Alignment.topLeft, child: Text('overlay child')),
+        child: Semantics(explicitChildNodes: true, child: const Text('anchor')),
+      );
+      portal = Overlay.wrap(child: ExcludeSemantics(child: portal));
+      portal = SizedBox(width: 200, height: 100, child: portal);
+
+      await tester.pumpWidget(
+        Directionality(
+          textDirection: TextDirection.ltr,
+          child: Overlay.wrap(
+            child: Semantics(container: true, child: Column(children: <Widget>[sibling, portal])),
+          ),
+        ),
+      );
+
+      // Showing the overlay child gives the sibling anchor a sibling conflict,
+      // and hiding it takes that conflict away again. The conflict feeds
+      // shouldFormSemanticsNode, so the sibling's fragment stops producing a
+      // node of its own while keeping the one it cached. Its children are taken
+      // by an ancestor while it is out of the tree, and it used to be handed
+      // back in still holding them, leaving a SemanticsNode that was attached
+      // but had no parent. That only becomes observable on the second round
+      // trip.
+      for (var i = 0; i < 2; i += 1) {
+        controller.show();
+        await tester.pumpAndSettle();
+        expect(find.text('overlay child'), findsOneWidget);
+
+        controller.hide();
+        await tester.pumpAndSettle();
+        expect(find.text('overlay child'), findsNothing);
+      }
+    });
   });
 
   testWidgets(

```

# REVIEW A

**Review of flutter/flutter#190431: Rebuild a semantics fragment when its sibling conflict changes**

The PR is already merged. This review is based on the diff and the description. I did not check out or run the code.

**Summary**

`shouldFormSemanticsNode` reads `_hasSiblingConflict`, but changing that flag never invalidated the fragment. A fragment could therefore keep a stale `cachedSemanticsNode` and a stale child list. That could leave an attached `SemanticsNode` with no parent. The PR fixes this by snapshotting which fragments were conflicting before `_marksConflictsInMergeGroup` resets the flag. After recomputing, it calls `markNeedsBuild()` on every fragment whose flag changed.

**Code quality**
- The fix targets the cause, which is the missing invalidation, instead of patching the child list or guarding `attach`. The description explains why it moved away from the first approach.
- Taking the snapshot inside the existing loop avoids an extra pass over `mergeGroup`. Using `Set.remove` to separate "gained" from "lost" is compact. It also leaves the leftover set holding exactly the fragments that lost their conflict.
- The reset-then-recompute structure stays. The description is right that `configToMergeUp` depends on that reset.
- The comments say why the code does this. One small point: `wasConflicting.remove(fragment)` inside an `if` condition mutates the set as a side effect. Its meaning ("still conflicting, so no change") is easy to misread, and a short inline note would help. A clearer alternative is to compute `wasConflicting.contains(...)` and have the second loop iterate a difference.
- `fragment is _RenderObjectSemantics` is checked twice. That is fine if the other `_SemanticsFragment` subtypes should not be marked. A comment saying so would help.

**Potential bugs and risks**
- **Timing.** The description says this runs in the parent-data phase of `flushSemantics`, before the build loop, so `markNeedsBuild` is legal there. That matches the earlier note that dirtying during the build phase is rejected. The correctness of the fix depends on this ordering. A short comment at the call site would protect it from future refactors. An assert that we are not yet in the build phase would be even better.
- **Other `shouldFormSemanticsNode` inputs.** The author says they could not find a gap in `isSemanticBoundary`, `isRoot` or `contributesToSemanticsTree`, because everything that feeds them goes through `markNeedsUpdate`. That is plausible, and they flagged the uncertainty openly. I would still follow up with a debug-only check, run after a build, that asserts a fragment's `built` state is consistent with `shouldFormSemanticsNode`. That would catch any similar gap.
- **Release-mode claim.** The link to the `Failed to update ui::AXTree` error in #187198 is inferred from reading the code, not measured. The PR says so. The issue should stay open or be re-verified on a real device rather than closed on the strength of this test.
- **Possible over-invalidation.** Each flip now forces a rebuild. In `OverlayPortal`, which flips the flag often, that is correct and cheap. It is still worth confirming that semantics-heavy benchmarks did not regress.

**Performance**
- The added cost is one small `Set` allocation per call to `_marksConflictsInMergeGroup`, plus O(n) membership checks. `wasConflicting` is allocated even when nothing was conflicting. Allocating it lazily, or skipping it when no fragment has a conflict, would avoid garbage on a path that runs on every semantics flush. Semantics trees can be large, so this may matter. It is minor but cheap to fix.
- Rebuilds are triggered only on a real change, so there is no thrash in the steady state.

**Security**
- No concerns. This is internal tree bookkeeping with no external input.

**Test coverage**
- The regression test reproduces the `OverlayPortal` scenario, with a sibling anchor whose conflict toggles. It runs two show/hide round trips, because the bug only shows up on the second one. The comments explain why a second anchor is needed. That is good practice.
- The test only checks that nothing throws. It would be stronger if it also asserted the semantics tree's shape, for example with `expect(tester, meetsGuideline(...))` or a `SemanticsTester` check. For example, it could confirm that `'sibling'` and `'anchor'` are reachable and that no node is parentless after each hide. The existing assertion may only fire in debug mode, and that is the only mode the test covers.
- There is no direct unit test of `_marksConflictsInMergeGroup`. Both directions (gaining and losing a conflict) are exercised only indirectly. A lower-level test that flips the conflict one way at a time would pin down each direction.
- The description offers to add an `attach` guard as hardening. I would take that as a separate change, since it would also guard against other future causes.

**Verdict**

This is a well-reasoned, minimal fix that addresses the real cause. The suggestions above are small: lazy allocation of the set, clearer comments, stronger test assertions, and a debug consistency check. None of them should have blocked the merge.

# REVIEW B

**Review of flutter/flutter#190431: Rebuild a semantics fragment when its sibling conflict changes**

The PR is already merged. I read the description and most of the diff. The tool output was truncated, so I did not see the middle of the diff, including the production-code hunk. My comments on that code come from the PR description, not from reading the lines.

**Summary**
- `shouldFormSemanticsNode` depends on `_hasSiblingConflict`, but nothing marked the fragment for rebuild when that flag changed.
- A fragment could stop forming a node while keeping `built == true` and its cached node and children. An ancestor could then take those children. When the fragment formed a node again, it was reattached with the stale children, leaving a `SemanticsNode` that was attached but had no parent. That trips `assert(!child.attached)` in `_replaceChildren`.
- The fix snapshots each fragment's conflict flag just before `_marksConflictsInMergeGroup` resets it. It then calls `markNeedsBuild` if the flag differs after the conflicts are re-marked. Both directions are covered.

**Code quality**
- Putting the comparison in the existing loops avoids an extra pass over `mergeGroup`.
- Comparing before and after across the pass is correct. The description explains why the check can't live in `markSiblingConfigurationConflict`: the reset to false is load-bearing, because `configToMergeUp` reads `shouldFormSemanticsNode`.
- The fix invalidates the fragment at its source. The first version patched the stale child list instead, and chunhtai's suggestion to fix the invalidation was the better design.
- The description is thorough. It is also candid about what wasn't verified: the three earlier branches in `shouldFormSemanticsNode`, and the release-mode AXTree failure.

**Potential issues**
- The change runs in the parent-data phase of `flushSemantics`, before the build loop. The PR says the fragment is rebuilt in the same flush. I couldn't check that, but the new test exercises it.
- The extra rebuilds only happen when the flag actually flips, so the cost should be small. The snapshot needs per-fragment storage, either a list or a local variable. I couldn't see which, so check that it doesn't allocate on every flush when `mergeGroup` is large.
- The author declined to restore the `attach` guard that `detach` already has. It would be cheap defense-in-depth against the same corruption reached by another route. A follow-up would be reasonable.
- The author could not confirm that this fixes the release-mode `Failed to update ui::AXTree ... will not be in the tree` error from #187198. The issue should stay open or be re-verified on a real assistive-technology setup.

**Security**
No concerns.

**Test coverage**
- The regression test uses `OverlayPortal` with a sibling anchor. It toggles show and hide over two round trips, which matters because the corruption only shows up on the second one.
- The test comment explains the mechanism.
- The test asserts only that overlay content appears and disappears, and that no assertion fires. It would be stronger if it also checked the semantics tree, for example with `tester.ensureSemantics()` and a check that no node is attached without a parent, or a `SemanticsTester` comparison after each step.
- A direct unit-level test would also help. It would flip a fragment's sibling conflict across two flushes and check that it rebuilds, without depending on `OverlayPortal`.
- The test sets `Overlay.wrap` inside `ExcludeSemantics`, which makes the setup a bit intricate. A short comment on why would help.

**Verdict**
The fix is correct and well-scoped, and it is well argued. The suggestions are optional: stronger semantics assertions in the test, and possibly the `attach` guard as hardening.
