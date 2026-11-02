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

The PR is already merged and has approvals from chunhtai and victorsanni. My overall view is positive. The diagnosis is sound and the fix is small and targeted. It invalidates at the point where the decision changes instead of patching the stale child list afterwards.

**Code quality**
- The fix fits in one function, `_marksConflictsInMergeGroup`, and adds no extra pass over `mergeGroup`.
- Snapshotting `wasConflicting` before the reset is the right design. The reset has to stay because `configToMergeUp` reads `shouldFormSemanticsNode`. The PR description explains this well.
- The set logic is correct:
  - `wasConflicting.remove(fragment)` returns false for a fragment that is newly conflicting, so it gets `markNeedsBuild()`.
  - A fragment that was conflicting and still is has its entry removed and is left alone.
  - Whatever remains in the set stopped conflicting and is marked in the second loop.
- Nit: `remove` inside a condition is a side-effecting check. It is compact but slightly subtle, and the comment helps. A reader could still trip on it. A small comment on the `remove` call itself, or a pair of boolean locals, would be clearer.
- Nit: two sets are now allocated on every merge-group pass, even when nothing conflicts. Allocating `wasConflicting` lazily, or only when a fragment was conflicting, would avoid that. The cost is likely negligible, but this runs on every semantics flush.

**Potential bugs and risks**
- The PR relies on `markNeedsBuild` being legal at this point. It runs in the parent data phase before the build loop, which the author states and tested (16171 tests pass). It is worth keeping an eye on whether `_marksConflictsInMergeGroup` is ever called from the build phase. If so, the same "dirtied during flush" assertions would apply.
- The author says they could not rule out the same invalidation gap in the other three branches of `shouldFormSemanticsNode`. That is honestly flagged. It is reasonable to leave as is.
- The PR notes that `attach` lacks the guard that `detach` has, and that several `_children` walkers assert on `child.owner`. Leaving those out is fine for this PR, but a follow-up issue to track the hardening would be useful.
- The PR only partially addresses #187198. The `will not be in the tree` AXTree error from #182444 still reproduces with or without this change. Keeping that issue open, and splitting out the `computeChildGeometry` report from #189902 as the author requested, is the right call.

**Performance**
- Extra `markNeedsBuild` calls only happen when the conflict flag actually flips, so steady-state frames are unaffected.
- The two small set allocations per pass are the only overhead, as noted above.

**Security**
- No concerns.

**Test coverage**
- The regression test is well targeted. It needs two anchors, fails on master with `'!child.attached'`, and passes with the fix. The comment explains why two round trips are needed.
- The test has no semantics expectations of its own, so it only catches the framework assertion. The author offered to add some. I'd encourage adding an assertion on the resulting tree, for example that the sibling's node is present and parented correctly after hide. That would also protect the release-mode orphan-node behaviour, which asserts cannot catch.
- A lower-level unit test in `test/rendering` or `test/semantics` for the conflict flip would be a useful complement. It would not depend on `OverlayPortal`.
- Release-mode behaviour (the AXTree error) is not verified. The author is upfront about this.

**Summary:** This is a correct, minimal fix with good documentation of its limits. I'd suggest two optional follow-ups. One is tightening the test with tree assertions. The other is filing a hardening issue for the unguarded `_children` walkers.

# REVIEW B

## Review of flutter/flutter#190431: Rebuild a semantics fragment when its sibling conflict changes

The PR is already merged with two approvals. This review is based on the diff and description only. I did not check out or run the code.

### Summary
`shouldFormSemanticsNode` reads `_hasSiblingConflict`, but nothing invalidated the fragment when that flag changed. A fragment could keep `built == true` and a stale `cachedSemanticsNode` and child list. It could then re-enter the tree holding children that an ancestor had taken, which leaves an attached `SemanticsNode` with no parent. The fix snapshots the previous flag before `_marksConflictsInMergeGroup` resets it, then calls `markNeedsBuild()` on any fragment whose flag changed.

### Code quality
**What's good**
- The fix is in the right place. It invalidates when the decision changes, not at the moment of the child theft, where `markNeedsBuild` is rejected mid-flush. The description explains why a before/after comparison is needed: the reset to `false` is load-bearing, because `configToMergeUp` reads `shouldFormSemanticsNode`.
- Both directions are handled (gaining and losing a conflict).
- There is no extra pass over `mergeGroup`.
- The comments explain why the invalidation is needed.

**Minor suggestions**
- The `wasConflicting.remove(fragment)` call inside the `if` condition mutates the set as a side effect, then relies on the leftover contents in the next loop. That is correct, but subtle. An explicit `if (wasConflicting.contains(...))` and a separate removal, or a single "changed" computation, would read more clearly. This is style only.
- `wasConflicting` is a new `Set` allocated on every call, including when no fragment ever conflicts. This is on the semantics flush path, and the cost is probably small. You could allocate it lazily, or skip the set when `hasSiblingConflict` is empty and nothing was previously conflicting.
- The check `fragment is _RenderObjectSemantics` appears twice. That is needed because `markNeedsBuild` and `_hasSiblingConflict` are on the subclass. If other `_SemanticsFragment` subtypes can also carry the flag, they would be silently skipped. A short comment saying why this is safe would help.

### Potential bugs and risks
- **Marking during the flush.** The description says this runs in the parent data phase, before the build loop, so the same flush rebuilds the fragment. That is the key assumption, and the diff alone can't confirm it. A debug assertion or a note on the call path would protect it from later refactors. If `_marksConflictsInMergeGroup` ever ran after builds began, `markNeedsBuild` would be rejected or the rebuild deferred.
- **Possible over-invalidation.** `markNeedsBuild` runs whenever the flag changes, even if `shouldFormSemanticsNode` already evaluates true for other reasons, such as `explicitChildNodes`. That is a harmless extra rebuild, but it could be skipped by comparing `shouldFormSemanticsNode` before and after. Doing so would be more fragile, given that the reset interacts with `configToMergeUp`.
- **Unconfirmed branches.** The author says they could not find the same gap in the `isSemanticBoundary`, `isRoot` and `contributesToSemanticsTree` branches, and they flag that as unverified. The reasoning is plausible: everything feeding them goes through `markNeedsUpdate`, which nulls parent data. It would be worth a follow-up audit or an assertion.
- **Release-mode behavior.** The AXTree failure in #187198 is unconfirmed. The description says the `will not be in the tree` error still reproduces with the #182444 shapes (Tooltips in a ListView, MenuAnchor + Tooltip), with or without this change. The PR correctly says "Partially addresses". Make sure that issue stays open and tracked.
- **`computeChildGeometry` variant.** The description asks for the variant @madenvel reported to be split into its own issue. Confirm that was done, otherwise it is lost.
- **Hardening.** The author offered to restore the `attach` guard that `detach` already has. That would be defense in depth, since the other `_children` walkers assert on `child.owner`. I'd keep it as a follow-up.

### Performance
The added cost is one `Set` and a few hash operations per merge group per flush. Extra `markNeedsBuild` calls only happen when the conflict state really flips. OverlayPortal toggles flip it, and each flip now rebuilds a fragment, but the old behavior was wrong, so that is a correctness cost. No concern, but the allocation point above is a cheap micro-optimization.

### Security
No concerns. This is internal semantics-tree bookkeeping with no external input.

### Test coverage
**Strengths**
- The regression test fails on master with `'!child.attached': is not true` and passes with the fix.
- The comments explain why two anchors are required, and why it takes two show/hide round trips.
- The test needs a second portal anchor to fail. It is a narrow reproduction of the bug, not a general one.

**Gaps**
- The test has no semantics expectations. Its only failure mode is a framework assertion. That is brittle:
  - It would pass if the tree were wrong but no assert fired.
  - In release it does not exercise the engine-update path, which is where the user-visible symptom is.
  - I'd add `semantics` expectations, for example with `SemanticsTester` or `tester.getSemantics`, on the tree after each hide/show. I'd also add a check that every attached node has a parent. The author offered to do this and it would be worth taking up.
- There is no lower-level unit test of `_marksConflictsInMergeGroup`, for example in `test/semantics` or `test/rendering`. A direct test that toggling a sibling conflict triggers a rebuild would be less tied to OverlayPortal.
- The test only covers a conflict being gained and then lost via OverlayPortal. A case without OverlayPortal, such as two siblings with conflicting configs where one changes, would show the fix is general.
- The description mentions a recorded-update check against the desktop bridge rules. That check is not in the PR. A test of that kind would help with the open AXTree issue.

### Verdict
The fix is sound, minimal and well-reasoned. The description is candid about what is and isn't verified. Remaining follow-ups:
1. Add semantics-tree expectations to the regression test.
2. Make sure the `computeChildGeometry` and AXTree issues stay open and tracked.
3. Consider the `attach` hardening and the audit of the other three `shouldFormSemanticsNode` branches.
