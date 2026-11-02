# PR diff (the real change)

```diff
diff --git a/tests/repo_utils/test_tests_fetcher.py b/tests/repo_utils/test_tests_fetcher.py
index e63f775d18b2..aefbbeef21de 100644
--- a/tests/repo_utils/test_tests_fetcher.py
+++ b/tests/repo_utils/test_tests_fetcher.py
@@ -669,60 +669,29 @@ def test_multimodal_in_create_reverse_dependency_map(self):
         as impacted file from reverse dependency
         """
         reverse_map = create_reverse_dependency_map()
-        models_dir = str(tests_fetcher.PATH_TO_TRANSFORMERS / "models")
-
-        # impact of CLIP modeling file to all models where it is a backbone
-        expected_clip_multimodals = {
-            f"{models_dir}/video_llava/configuration_video_llava.py",
-            f"{models_dir}/llava/modeling_llava.py",
-            f"{models_dir}/vipllava/configuration_vipllava.py",
-            f"{models_dir}/granite4_vision/modeling_granite4_vision.py",
-            f"{models_dir}/llava/configuration_llava.py",
-            f"{models_dir}/sam3/configuration_sam3.py",
-            f"{models_dir}/llava_next/configuration_llava_next.py",
-            f"{models_dir}/sam3/modeling_sam3.py",
-            f"{models_dir}/llava_next/modeling_llava_next.py",
-            f"{models_dir}/llava_next_video/configuration_llava_next_video.py",
-            f"{models_dir}/llava_next_video/modeling_llava_next_video.py",
-            f"{models_dir}/vipllava/modeling_vipllava.py",
-            f"{models_dir}/video_llava/modeling_video_llava.py",
-            f"{models_dir}/granite4_vision/configuration_granite4_vision.py",
+        models_dir = "src/transformers/models"
+
+        # impact of CLIP modeling file: changing clip must trigger tests for composite models that use it
+        expected_tests_for_clip = {
+            "tests/models/llava/test_modeling_llava.py",
+            "tests/models/llava_next/test_modeling_llava_next.py",
+            "tests/models/vipllava/test_modeling_vipllava.py",
+            "tests/models/video_llava/test_modeling_video_llava.py",
         }
-        assert expected_clip_multimodals.issubset(set(reverse_map[f"{models_dir}/clip/modeling_clip.py"]))
-        assert expected_clip_multimodals.issubset(set(reverse_map[f"{models_dir}/clip/configuration_clip.py"]))
+        assert expected_tests_for_clip.issubset(set(reverse_map[f"{models_dir}/clip/modeling_clip.py"]))
+        assert expected_tests_for_clip.issubset(set(reverse_map[f"{models_dir}/clip/configuration_clip.py"]))
 
         # reverse backbone mapping works only if modeling or configuration files are modified
         # because multimodals re-use only config/model of its backbone
-        assert expected_clip_multimodals.isdisjoint(set(reverse_map[f"{models_dir}/clip/image_processing_clip.py"]))
+        assert expected_tests_for_clip.isdisjoint(set(reverse_map[f"{models_dir}/clip/image_processing_clip.py"]))
 
         # Also lets check with a random text backbone
-        expected_qwen2_multimodals = {
-            f"{models_dir}/got_ocr2/configuration_got_ocr2.py",
-            f"{models_dir}/qwen2_audio/modeling_qwen2_audio.py",
-            f"{models_dir}/musicflamingo/modeling_musicflamingo.py",
-            f"{models_dir}/video_llama_3/configuration_video_llama_3.py",
-            f"{models_dir}/vibevoice_asr/modeling_vibevoice_asr.py",
-            f"{models_dir}/qwen2_audio/configuration_qwen2_audio.py",
-            f"{models_dir}/got_ocr2/modeling_got_ocr2.py",
-            f"{models_dir}/vibevoice/configuration_vibevoice.py",
-            f"{models_dir}/musicflamingo/configuration_musicflamingo.py",
-            f"{models_dir}/fast_vlm/modeling_fast_vlm.py",
-            f"{models_dir}/audioflamingo3/modeling_audioflamingo3.py",
-            f"{models_dir}/pp_chart2table/configuration_pp_chart2table.py",
-            f"{models_dir}/video_llama_3/modeling_video_llama_3.py",
-            f"{models_dir}/fast_vlm/configuration_fast_vlm.py",
-            f"{models_dir}/internvl/configuration_internvl.py",
-            f"{models_dir}/llava_onevision/configuration_llava_onevision.py",
-            f"{models_dir}/audioflamingo3/configuration_audioflamingo3.py",
-            f"{models_dir}/vibevoice/modeling_vibevoice.py",
-            f"{models_dir}/internvl/modeling_internvl.py",
-            f"{models_dir}/vibevoice_asr/configuration_vibevoice_asr.py",
-            f"{models_dir}/ovis2/configuration_ovis2.py",
-            f"{models_dir}/ovis2/modeling_ovis2.py",
-            f"{models_dir}/llava_onevision/modeling_llava_onevision.py",
+        expected_tests_for_qwen2 = {
+            "tests/models/qwen2_audio/test_modeling_qwen2_audio.py",
+            "tests/models/got_ocr2/test_modeling_got_ocr2.py",
         }
-        assert expected_qwen2_multimodals.issubset(set(reverse_map[f"{models_dir}/qwen2/modeling_qwen2.py"]))
-        assert expected_qwen2_multimodals.isdisjoint(set(reverse_map[f"{models_dir}/qwen2/tokenization_qwen2.py"]))
+        assert expected_tests_for_qwen2.issubset(set(reverse_map[f"{models_dir}/qwen2/modeling_qwen2.py"]))
+        assert expected_tests_for_qwen2.isdisjoint(set(reverse_map[f"{models_dir}/qwen2/tokenization_qwen2.py"]))
 
     @unittest.skip("Broken for now TODO @ArthurZucker")
     def test_infer_tests_to_run(self):
diff --git a/utils/tests_fetcher.py b/utils/tests_fetcher.py
index 8bf1a0bb30c3..895e66743d11 100644
--- a/utils/tests_fetcher.py
+++ b/utils/tests_fetcher.py
@@ -910,7 +910,10 @@ def create_reverse_dependency_map() -> dict[str, list[str]]:
             for child_model in children_models:
                 child_file = PATH_TO_TRANSFORMERS / "models" / child_model / f"{kind}_{child_model}.py"
                 if (PATH_TO_REPO / child_file).is_file():
-                    reverse_map.setdefault(child_file.as_posix(), []).extend(existing_backbone_files(parent_model))
+                    child_file_posix = child_file.relative_to(PATH_TO_REPO).as_posix()
+                    for parent_file in existing_backbone_files(parent_model):
+                        parent_file_posix = Path(parent_file).relative_to(PATH_TO_REPO).as_posix()
+                        reverse_map.setdefault(child_file_posix, []).extend(reverse_map.get(parent_file_posix, []))
 
     return reverse_map
 

```

# REVIEW A

# Review of PR #49742: Fix tests_fetcher backbone step

The PR is already merged, so this review is retrospective. I read the diff and the surrounding code in `utils/tests_fetcher.py`. I did not run the tests.

## Summary
The fix is correct and the diagnosis matches the code. `create_reverse_dependency_map()` had three separate bugs in the backbone step, and the PR fixes all three:
- **Absolute key:** `child_file.as_posix()` produced an absolute path, but every other key in the map is repo-relative. The new code uses `relative_to(PATH_TO_REPO)`.
- **Absolute lookup:** `existing_backbone_files()` returns `PATH_TO_TRANSFORMERS`-based paths, which are absolute (`utils/tests_fetcher.py:600`). The new code relativizes them before calling `reverse_map.get`.
- **Source files instead of tests:** the old code stored source files, which `create_module_to_test_map` filters out. The new code propagates the parent's existing reverse-map entries, which include its tests.

The naming is easy to misread. In this loop `parent_model` is the composite (such as `llava`) and `children_models` are its backbones (such as `clip`). The new code does what the comment says: a change to `clip` now triggers `llava`'s tests and everything that depends on `llava`.

## Suggestions (none blocking)

1. **Duplicates and ordering** (`utils/tests_fetcher.py:913-916`)
   - `extend` adds duplicates. If a backbone is used by several composites, or a file appears under both the `configuration` and `modeling` kinds, the same test path is added more than once.
   - Downstream code probably dedupes. Still, building a set and assigning `list(set(...))` is cheap and keeps the map clean.
   - The result also depends on iteration order, because the loop reads `reverse_map` entries that it may itself have extended. This matters for chained backbones such as A→B→C. A composite whose parent is itself a backbone may or may not see the extended entries, depending on dict order. The old code's intent was one level of propagation, so this is probably fine. A short comment, or a snapshot of the original map to read from, would make that explicit.

2. **Loop structure**
   - `child_file_posix` and the `Path(...).relative_to(...)` calls are recomputed inside nested loops.
   - Computing the parent's test list once per `parent_model`, then extending each child key, would be clearer. It would also drop the `kind` / `parent_file` cross-product that adds the same lists repeatedly.

3. **Possible `ValueError`**
   - `Path(parent_file).relative_to(PATH_TO_REPO)` raises if `existing_backbone_files` ever returns a non-absolute path.
   - It is fine today, because `PATH_TO_TRANSFORMERS` is absolute. It couples two helpers through an implicit contract, though.
   - A cleaner option is to have `existing_backbone_files` return repo-relative paths. `create_backbone_edges` also uses it, so check that caller before changing it.

4. **Tests** (`tests/repo_utils/test_tests_fetcher.py`)
   - The rewritten test now checks the thing that matters: the map yields test files, not source files. That is a real improvement over the old assertions, which could never fail meaningfully.
   - The expected sets are much smaller than before, which is reasonable.
   - The `isdisjoint` checks for `image_processing_clip.py` and `tokenization_qwen2.py` are still valuable.
   - Consider one end-to-end assertion through `create_module_to_test_map`, or `infer_tests_to_run`, with a modified backbone file. That would guard against the filtering issue (bug 3) coming back. `test_infer_tests_to_run` is currently skipped, so the unit test on the map is the only guard.
   - The `modernvbert` / `colmodernvbert` case from the PR description is the real-world repro. It is not covered by a test, and adding one would make it a regression test.

5. **Style/conventions**
   - Nothing in `CLAUDE.md` is violated. No `# Copied from` blocks or modular files are involved.
   - The final commits renamed variables back and forth. Squash-merge should absorb that.

## Performance and security
- The extra work is a handful of dict lookups per backbone pair, which is negligible next to the dependency-graph build.
- There are no security concerns. The change is CI tooling only.

**Verdict:** a good, well-explained fix. The suggestions above are polish: dedupe, order-dependence, and a regression test.

# REVIEW B

Absolute, so `relative_to` works.

## Review of PR #49742: fix the tests_fetcher backbone step

The PR is already merged, so this is a retrospective review. Overall it's a correct fix with a clear description. I have a few non-blocking suggestions.

### Correctness
- **The three bugs are real, and the fix addresses all of them.** `PATH_TO_REPO`, `PATH_TO_TRANSFORMERS` and `PATH_TO_TESTS` are absolute (`utils/tests_fetcher.py:69-71`). That is why `child_file.as_posix()` and `existing_backbone_files()` produced keys that never matched the repo-relative keys used everywhere else. The `relative_to(PATH_TO_REPO)` calls are safe for the same reason.
- **The direction is right but hard to read.** `_get_backbone_map()` maps `composite → {backbones}`. So in the loop, `parent_model` is the composite (e.g. `llava`) and `child_model` is the backbone (e.g. `clip`). The new code does `reverse_map[clip_file] += reverse_map[llava_file]`. A change to CLIP therefore selects everything that depends on llava, including llava's tests, which is the intent. Copying the *reverse-map values* rather than the source files also fixes the third bug, where only source files were stored and then discarded by the `startswith("tests")` filter.
- **The variable names are misleading.** "parent" here is the composite and "child" is the backbone, which is the opposite of what the names suggest. The code comment says "a modification on `clip` triggers a test of `llava`", but the code never states which side is which. I'd rename them to `composite_model` / `backbone_model`, or add a one-line comment. This is the kind of naming that caused the original bug.

### Minor issues
- **Order dependence in nested composites.** `_get_backbone_map` follows nesting at any depth, so a file can be both a backbone key and a composite. The `extend` calls read `reverse_map[parent_file]` as it exists at that moment. If that entry was already extended earlier in the loop, the result depends on iteration order. The mapping is already transitive, so this is probably harmless, but it's worth a comment or a snapshot of the pre-loop map.
- **Duplicates.** Lists are extended without deduplication, so a single entry can be repeated many times. Downstream code probably builds sets, so this is only a small memory and perf cost. Using `dict.fromkeys` or a set would avoid it.
- **Simplification.** `reverse_map.setdefault(child_file_posix, [])` is inside the inner loop. You could hoist `existing = reverse_map[child_file_posix]` (it's a defaultdict) out of the loop. `Path(parent_file).relative_to(...)` is also repeated for every child. Computing the parent's relative paths once per composite would be cleaner. Both are small.
- **Possible empty-list key.** `setdefault` creates the key even when `reverse_map.get(parent_file_posix)` returns `[]`. That's harmless.

### Tests
- **Good change.** The old test used absolute-path keys and expected `src/` files, which `create_module_to_test_map` always discards. It could never have caught this regression. The new test uses repo-relative keys and expects `tests/...` files, so it now fails on the old code.
- **The expected sets are much smaller.** There are 4 CLIP tests and 2 Qwen2 tests, down from about 14 and 23. That's reasonable for a `issubset` check. A modular-heavy composite such as `colmodernvbert`, the motivating example, isn't covered. A direct assertion that a `modernvbert` change selects the `colmodernvbert` tests would pin the original bug, if a stable fixture exists.
- **The `isdisjoint` assertions are fragile.** If a test file imports the image processor or tokenizer, the disjointness check would fail for reasons unrelated to the backbone step. They pass today, but I'd keep an eye on them.
- **`models_dir` is now a hard-coded `"src/transformers/models"`.** That's fine, but deriving it from `PATH_TO_TRANSFORMERS.relative_to(PATH_TO_REPO)` would be more robust.

### Style, performance and security
- Nothing in the diff needs `make fix-repo`. No model files or `# Copied from` blocks are touched, and the changes are in `utils/` and `tests/` only.
- **Performance:** the new double loop is cheap and runs once per fetcher invocation.
- **Security:** no concerns.

### Behavioral note
The fetcher will now select more tests for backbone changes (CLIP, Qwen2, etc.), which is the intended behavior. It's worth watching CI load for a few days after this lands, since broad backbones like `qwen2` now fan out to many composite models' tests.

**Verdict:** approve, with the naming clarity and dedup suggestions as optional follow-ups.
