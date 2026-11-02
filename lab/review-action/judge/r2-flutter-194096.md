# PR diff (the real change)

```diff
diff --git a/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/composition_aware_mixin.dart b/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/composition_aware_mixin.dart
index 776c04c55cebc..54bb6357208d9 100644
--- a/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/composition_aware_mixin.dart
+++ b/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/composition_aware_mixin.dart
@@ -62,23 +62,24 @@ mixin CompositionAwareMixin {
     domElement.removeEventListener(_kCompositionStart, _compositionStartListener);
     domElement.removeEventListener(_kCompositionUpdate, _compositionUpdateListener);
     domElement.removeEventListener(_kCompositionEnd, _compositionEndListener);
+    // Composition can't be observed ending anymore.
+    resetComposition();
   }
 
-  void _handleCompositionStart(DomEvent event) {
+  void resetComposition() {
     composingText = null;
     composingBase = null;
   }
 
+  void _handleCompositionStart(DomEvent event) => resetComposition();
+
   void _handleCompositionUpdate(DomEvent event) {
     if (event.isA<DomCompositionEvent>()) {
       composingText = (event as DomCompositionEvent).data;
     }
   }
 
-  void _handleCompositionEnd(DomEvent event) {
-    composingText = null;
-    composingBase = null;
-  }
+  void _handleCompositionEnd(DomEvent event) => resetComposition();
 
   EditingState determineCompositionState(EditingState editingState) {
     if (composingText == null) {
diff --git a/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/text_editing.dart b/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/text_editing.dart
index c85e34f40586b..e80e43d6903ee 100644
--- a/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/text_editing.dart
+++ b/engine/src/flutter/lib/web_ui/lib/src/engine/text_editing/text_editing.dart
@@ -1773,10 +1773,18 @@ abstract class DefaultTextEditingStrategy
 
   @override
   void setEditingState(EditingState? editingState) {
+    final String? previousText = lastEditingState?.text;
     lastEditingState = editingState;
     if (!isEnabled || !editingState!.isValid) {
       return;
     }
+    // Writing different text into the element ends any composition in
+    // progress, and Chrome does so without a `compositionend` event. This
+    // happens when an input formatter rejects a dead key character. Forget the
+    // composition so its stale range is not reported back to the framework.
+    if (editingState.text != previousText) {
+      resetComposition();
+    }
     lastEditingState!.applyToDomElement(domElement);
   }
 
diff --git a/engine/src/flutter/lib/web_ui/test/engine/composition_test.dart b/engine/src/flutter/lib/web_ui/test/engine/composition_test.dart
index 80125879a5012..8fb7c12efb022 100644
--- a/engine/src/flutter/lib/web_ui/test/engine/composition_test.dart
+++ b/engine/src/flutter/lib/web_ui/test/engine/composition_test.dart
@@ -294,6 +294,143 @@ Future<void> testMain() async {
             ),
       );
     });
+
+    // Regression test for https://github.com/flutter/flutter/issues/189056.
+    test('should be cleared when the framework removes the composing text', () {
+      _inputElement.value = 'AAA';
+      _inputElement.setSelectionRange(3, 3);
+
+      // Dead key `^` starts a composition.
+      _inputElement.dispatchEvent(
+        createDomCompositionEvent(
+          _MockWithCompositionAwareMixin._kCompositionUpdate,
+          <Object?, Object?>{'data': '^'},
+        ),
+      );
+      _inputElement.value = 'AAA^';
+      _inputElement.setSelectionRange(4, 4);
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(editingStrategy.lastEditingState?.composingBaseOffset, 3);
+      expect(editingStrategy.lastEditingState?.composingExtentOffset, 4);
+
+      // An input formatter rejects `^`. Chrome drops the composition without
+      // firing compositionend.
+      editingStrategy.setEditingState(EditingState(text: 'AAA', baseOffset: 3, extentOffset: 3));
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(
+        editingStrategy.lastEditingState,
+        EditingState(text: 'AAA', baseOffset: 3, extentOffset: 3),
+      );
+
+      // Typing afterwards must not mark the new character as composing.
+      _inputElement.value = 'AAAB';
+      _inputElement.setSelectionRange(4, 4);
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(
+        editingStrategy.lastEditingState,
+        EditingState(text: 'AAAB', baseOffset: 4, extentOffset: 4),
+      );
+    });
+
+    test('should be cleared when the framework removes composing text mid-text', () {
+      _inputElement.value = 'AB';
+      _inputElement.setSelectionRange(1, 1);
+
+      _inputElement.dispatchEvent(
+        createDomCompositionEvent(
+          _MockWithCompositionAwareMixin._kCompositionUpdate,
+          <Object?, Object?>{'data': '^'},
+        ),
+      );
+      _inputElement.value = 'A^B';
+      _inputElement.setSelectionRange(2, 2);
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(editingStrategy.lastEditingState?.composingBaseOffset, 1);
+      expect(editingStrategy.lastEditingState?.composingExtentOffset, 2);
+
+      // The stale range 1..2 still fits the new text, so it must not be
+      // reported as `B` composing.
+      editingStrategy.setEditingState(EditingState(text: 'AB', baseOffset: 1, extentOffset: 1));
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(
+        editingStrategy.lastEditingState,
+        EditingState(text: 'AB', baseOffset: 1, extentOffset: 1),
+      );
+    });
+
+    test('should be kept when the framework sets the same text', () {
+      _inputElement.value = 'AAA';
+      _inputElement.setSelectionRange(3, 3);
+
+      _inputElement.dispatchEvent(
+        createDomCompositionEvent(
+          _MockWithCompositionAwareMixin._kCompositionUpdate,
+          <Object?, Object?>{'data': '^'},
+        ),
+      );
+      _inputElement.value = 'AAA^';
+      _inputElement.setSelectionRange(4, 4);
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      // Writing unchanged text does not end the composition in the browser.
+      editingStrategy.setEditingState(
+        EditingState(
+          text: 'AAA^',
+          baseOffset: 4,
+          extentOffset: 4,
+          composingBaseOffset: 3,
+          composingExtentOffset: 4,
+        ),
+      );
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(editingStrategy.lastEditingState?.composingBaseOffset, 3);
+      expect(editingStrategy.lastEditingState?.composingExtentOffset, 4);
+    });
+
+    test('should not carry over to the next text field', () {
+      _inputElement.value = 'A';
+      _inputElement.setSelectionRange(1, 1);
+
+      // The first field is mid-composition when focus moves away.
+      _inputElement.dispatchEvent(
+        createDomCompositionEvent(
+          _MockWithCompositionAwareMixin._kCompositionUpdate,
+          <Object?, Object?>{'data': '^'},
+        ),
+      );
+      _inputElement.value = 'A^';
+      _inputElement.setSelectionRange(2, 2);
+      _inputElement.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(editingStrategy.lastEditingState?.composingBaseOffset, 1);
+      expect(editingStrategy.lastEditingState?.composingExtentOffset, 2);
+
+      // The framework connects the second field: it sends its state while
+      // the strategy is disabled, then shows the keyboard.
+      editingStrategy.disable();
+      editingStrategy.setEditingState(EditingState(text: 'B', baseOffset: 1, extentOffset: 1));
+      editingStrategy.enable(
+        InputConfiguration(viewId: kImplicitViewId),
+        onChange: (_, _) {},
+        onAction: (_) {},
+      );
+
+      final input = editingStrategy.activeDomElement as DomHTMLInputElement;
+      input.value = 'BC';
+      input.setSelectionRange(2, 2);
+      input.dispatchEvent(createDomEvent('Event', 'input'));
+
+      expect(
+        editingStrategy.lastEditingState,
+        EditingState(text: 'BC', baseOffset: 2, extentOffset: 2),
+      );
+    });
   });
 
   group('Text Editing Delta Model', () {

```

# REVIEW A

# Review of flutter/flutter#194096: drop the stale composing range after text is replaced mid-composition

The PR is already merged and approved. The fix is small, targeted and well explained, and I'd have approved it too. I have a few non-blocking observations.

## What it does
- It factors the composition reset into `CompositionAwareMixin.resetComposition()`. `compositionstart`, `compositionend` and `removeCompositionEventHandlers` all call it. The `removeCompositionEventHandlers` call is new.
- `DefaultTextEditingStrategy.setEditingState` now calls `resetComposition()` when the incoming text differs from the previous `lastEditingState.text`.

## Code quality
- Pulling out `resetComposition()` removes duplication, and the comment on the new call explains why it is needed.
- The `setEditingState` comment is clear about the Chrome-specific behavior.
- `resetComposition` is public on a mixin. Making it `@protected` or private to the library would keep it off the public surface, but the other members of the mixin are exposed the same way.

## Potential bugs and edge cases
1. **Text comparison uses `lastEditingState`, not the DOM.** `previousText` is the last state the engine cached. Suppose a DOM `input` event hasn't been processed yet and the user has typed more. The framework's text could then differ from the DOM, or equal the stale cache. In practice the framework echoes engine-reported state, so this is probably fine. Comparing against `domElement.value` would be more faithful to "different text is written".
2. **Changed text doesn't always end a composition.** The reset fires on any text difference. Suppose the framework sends text that includes the composing character but is otherwise different, such as a formatter that uppercases. Chrome may still end the composition, and for IMEs that keep composing across a value write, the engine would drop `composingText` while the browser continues. The next `compositionupdate` sets `composingText` again, but `composingBase` is only set later, when the state is determined. I couldn't see how it is recomputed, so it's worth checking that the base is recovered properly. The new tests don't cover this case.
3. **Early return and `lastEditingState`.** `lastEditingState` is assigned before the `!isEnabled` check, and the reset sits after that check. When the strategy is disabled, `disable()` has already cleared the composition, so this works. It does rely on that ordering, though.
4. **A null `editingState`.** `editingState!.isValid` is only reached when `isEnabled` is true, which is existing behavior, and the new code sits after it, so it adds no new risk.

## Performance
Negligible. It adds one string comparison per `setEditingState` call. It runs on every framework text update, but those strings are short.

## Security
No concerns.

## Test coverage
Coverage is good:
- It covers the reported crash scenario, where the range end exceeds the text length.
- It covers a mid-text case where the stale range still fits, which would otherwise be silently wrong.
- It covers a same-text write that keeps the composition.
- It covers the `disable()` carry-over to the next field.

Suggestions:
- Add a case where the text changes but the composition legitimately continues, such as an IME that rewrites the composing text. That would pin down the behavior for observation 2.
- Add an integration-level test with a real `TextField` and a formatter, if feasible. The engine-level unit tests only simulate Chrome dropping the composition.

## Summary
It's a sound fix that addresses the root cause, which is a cached composition outliving the browser's silent cancel. The tests are thorough, and the remaining concerns are minor.

# REVIEW B

**Review of flutter/flutter#194096: drop the stale composing range after text is replaced mid-composition**

The PR is already merged. I read the diff and the description. I didn't build it or run the tests, and I couldn't find a CLAUDE.md in the working directory, so I judged style from general Flutter conventions.

**Summary:** The fix is small, targeted and well explained. I found no blocking issues.

**What's good**
- `resetComposition()` removes the duplicated reset logic in `_handleCompositionStart` and `_handleCompositionEnd`.
- Calling it from `removeCompositionEventListeners` is correct. Once the listeners are gone, nothing can observe `compositionend`, so the stale state would leak into the next field. This also fixes a bug that exists on master.
- The new tests cover these cases:
  - Removal at the end of the text.
  - Removal mid-text, where the stale range 1..2 still fits the new text. That is the subtle case, and it is good that it is tested.
  - Unchanged text, which keeps the composition.
  - Carry-over between fields.

**Potential issues and suggestions**
1. **The text comparison is a heuristic.** `editingState.text != previousText` assumes Chrome only drops the composition when the text differs.
   - If the framework rewrites the same text with a different selection or composing range, the engine keeps the composition. That seems intended.
   - If the framework writes different text that happens to be a valid continuation of the composition, such as an IME-driven echo of the same update, the composition is reset early. In that case `lastEditingState.text` normally equals the DOM value already, so this should be safe.
   - A short comment on why text equality is a sufficient proxy would help.
2. **`previousText` is read before `lastEditingState` is overwritten, but the reset sits after the `!isEnabled || !isValid` early return.**
   - While the strategy is disabled, the composition is not reset by `setEditingState`. The new reset in `disable()` covers that, and the carry-over test checks it.
   - An invalid state skips the reset. That's probably fine, but it is untested.
3. **`resetComposition` is public on the mixin.** It's reasonable since `text_editing.dart` calls it, but add a doc comment. Consider `@visibleForTesting` or a more specific name if it shouldn't be used elsewhere.
4. **Browser coverage.**
   - The description only says Chrome drops the composition silently. Safari and Firefox may behave differently: they might fire `compositionend`, which makes the reset a harmless no-op, or they might keep the composition.
   - The tests simulate the event sequence with synthetic events, so they don't verify real browser behavior. An integration test with a real dead key isn't practical, so the demo links are a reasonable substitute.
5. **Test nit.** The four tests repeat the same composition setup. A small helper would shorten them. This is minor.

**Performance and security**
- There's no performance concern. The change adds one string comparison per `setEditingState`.
- There are no security implications.

**Verdict:** LGTM. The remaining suggestions are non-blocking: a comment on the text-equality heuristic, a doc comment on `resetComposition`, and optionally a test for the invalid-state path.
