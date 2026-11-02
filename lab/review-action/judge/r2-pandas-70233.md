# PR diff (the real change)

```diff
diff --git a/doc/source/whatsnew/v3.1.0.rst b/doc/source/whatsnew/v3.1.0.rst
index 8944a89964899..e2e171d14d057 100644
--- a/doc/source/whatsnew/v3.1.0.rst
+++ b/doc/source/whatsnew/v3.1.0.rst
@@ -1239,6 +1239,7 @@ Groupby/resample/rolling
 - :meth:`DataFrame.ewm` and :meth:`Series.ewm` now raise an informative ``NotImplementedError`` instead of a confusing ``AttributeError`` when ``agg``/``aggregate`` is passed an arbitrary callable (:issue:`41700`)
 - Bug in :class:`.ExponentialMovingWindow` with ``online`` ignoring the decay for a single-column :class:`DataFrame`, returning the unweighted cumulative mean (:issue:`66522`)
 - Bug in :class:`PeriodIndex` resampling to a finer frequency where aggregation methods returned the original values instead of aggregating, e.g. ``count`` returned the data values rather than the number of observations per bin; empty bins now contain the method's identity value (e.g. ``0`` for ``sum`` instead of ``NaN``), consistent with :class:`DatetimeIndex` resampling (:issue:`42763`)
+- Bug in :meth:`.DataFrameGroupBy.agg` and :meth:`.SeriesGroupBy.agg` raising when the function returns values the column's dtype cannot hold, e.g. an integer too large for int64 on a pyarrow-backed or :class:`StringDtype` column, or ``NaT`` on a nullable integer, float or boolean column (:issue:`70233`)
 - Bug in :meth:`.DataFrameGroupBy.agg` when there are no groups, multiple keys, and ``group_keys=False`` (:issue:`51445`)
 - Bug in :meth:`.DataFrameGroupBy.agg` would operate on the group as a whole when ``args`` or ``kwargs`` are supplied for the provided ``func``; now this method only operates on each Series of the group (:issue:`39169`)
 - Bug in :meth:`.DataFrameGroupBy.any`, :meth:`.DataFrameGroupBy.all`, :meth:`.DataFrameGroupBy.std`, :meth:`.DataFrameGroupBy.var`, :meth:`.DataFrameGroupBy.sem`, :meth:`.DataFrameGroupBy.skew`, and :meth:`.DataFrameGroupBy.kurt` (and :class:`Series` variants) not propagating ``attrs`` to the result, unlike the other groupby reductions (:issue:`28283`)
diff --git a/pandas/core/arrays/arrow/array.py b/pandas/core/arrays/arrow/array.py
index b94ea8d319fc7..4ffd47b1587a7 100644
--- a/pandas/core/arrays/arrow/array.py
+++ b/pandas/core/arrays/arrow/array.py
@@ -731,10 +731,11 @@ def _cast_pointwise_result(self, values) -> ArrayLike:
                     )
             else:
                 arr = pa.array(values, from_pandas=True)
-        except (ValueError, TypeError):
+        except (ValueError, TypeError, OverflowError):
             # e.g. test_by_column_values_with_same_starting_value with nested
             #  values, one entry of which is an ArrowStringArray
             #  or test_agg_lambda_complex128_dtype_conversion for complex values
+            #  or OverflowError for e.g. 2**70, GH#70233
             values = np.asarray(values, dtype=object)
             return lib.maybe_convert_objects(values, convert_non_numeric=True)
 
diff --git a/pandas/core/arrays/masked.py b/pandas/core/arrays/masked.py
index b9671d741d483..9ab90f0cba1b3 100644
--- a/pandas/core/arrays/masked.py
+++ b/pandas/core/arrays/masked.py
@@ -172,7 +172,11 @@ def _from_sequence(cls, scalars, *, dtype=None, copy: bool = False) -> Self:
 
     def _cast_pointwise_result(self, values) -> ArrayLike:
         if isna(values).all():
-            return type(self)._from_sequence(values, dtype=self.dtype)
+            try:
+                return type(self)._from_sequence(values, dtype=self.dtype)
+            except TypeError:
+                # e.g. NaT goes through inference instead, GH#70233
+                pass
         if not (isinstance(values, np.ndarray) and values.dtype == object):
             values = construct_1d_object_array_from_listlike(values)
         result = lib.maybe_convert_objects(values, convert_to_nullable_dtype=True)
diff --git a/pandas/core/arrays/string_arrow.py b/pandas/core/arrays/string_arrow.py
index ab1fa17ebb24f..52662b5906fb1 100644
--- a/pandas/core/arrays/string_arrow.py
+++ b/pandas/core/arrays/string_arrow.py
@@ -188,9 +188,13 @@ def _cast_pointwise_result(self, values) -> ArrayLike:
 
         try:
             arr = pa.array(values, from_pandas=True)
-        except (ValueError, TypeError):
+        except (ValueError, TypeError, OverflowError):
+            # OverflowError for e.g. 2**70; safe=True so
+            #  [nan, 2**64 - 1] stays object instead of rounding, GH#70233
             values = construct_1d_object_array_from_listlike(values)
-            return lib.maybe_convert_objects(values, convert_non_numeric=True)
+            return lib.maybe_convert_objects(
+                values, convert_non_numeric=True, safe=True
+            )
         if pa.types.is_string(arr.type) or pa.types.is_large_string(arr.type):
             return self._from_pyarrow_array(arr)
         if self.dtype.na_value is np.nan:
diff --git a/pandas/tests/groupby/aggregate/test_aggregate.py b/pandas/tests/groupby/aggregate/test_aggregate.py
index b0ac7f01596ae..4d049090e90ed 100644
--- a/pandas/tests/groupby/aggregate/test_aggregate.py
+++ b/pandas/tests/groupby/aggregate/test_aggregate.py
@@ -2040,6 +2040,30 @@ def test_agg_lambda_complex128_dtype_conversion():
     tm.assert_frame_equal(result, expected)
 
 
+@pytest.mark.parametrize(
+    "dtype, value, expected_dtype",
+    [
+        (pd.StringDtype(na_value=np.nan), 2**70, object),
+        pytest.param("string[pyarrow]", 2**70, object, marks=td.skip_if_no("pyarrow")),
+        pytest.param("int64[pyarrow]", 2**70, object, marks=td.skip_if_no("pyarrow")),
+        ("Int64", pd.NaT, "M8[s]"),
+        ("Float64", pd.NaT, "M8[s]"),
+        ("boolean", pd.NaT, "M8[s]"),
+    ],
+)
+def test_agg_lambda_result_dtype_cannot_hold(dtype, value, expected_dtype):
+    # GH#70233 used to raise instead of inferring the result dtype
+    df = pd.DataFrame({"key": [1, 1, 2], "val": pd.Series([1, 0, 1], dtype=dtype)})
+    result = df.groupby("key")["val"].agg(lambda x: value)
+    expected = pd.Series(
+        [value, value],
+        index=pd.Index([1, 2], name="key"),
+        name="val",
+        dtype=expected_dtype,
+    )
+    tm.assert_series_equal(result, expected)
+
+
 @td.skip_if_no("pyarrow")
 def test_agg_lambda_numpy_uint64_to_pyarrow_dtype_conversion():
     # GH#59601
diff --git a/pandas/tests/indexing/test_loc.py b/pandas/tests/indexing/test_loc.py
index 206686ec85d20..427fa5b618640 100644
--- a/pandas/tests/indexing/test_loc.py
+++ b/pandas/tests/indexing/test_loc.py
@@ -2606,6 +2606,8 @@ def test_loc_setitem_with_expansion_pyarrow_finer_resolution(self):
             #  then coerced back into the int64 column
             ("int64[pyarrow]", pd.Period("2021-01-01", freq="D")),
             ("int64[pyarrow]", pd.Interval(5, 6)),
+            # used to raise in _post_expansion_casting, GH#70233
+            ("int64[pyarrow]", 2**70),
         ],
     )
     def test_loc_setitem_with_expansion_lossy_pre_cast(self, dtype, item):
@@ -2622,6 +2624,41 @@ def test_loc_setitem_with_expansion_lossy_pre_cast(self, dtype, item):
         expected = pd.DataFrame({"a": pd.Series([*original, item], dtype=object)})
         tm.assert_frame_equal(df, expected)
 
+    @pytest.mark.parametrize(
+        "dtype, item",
+        [
+            (pd.StringDtype(na_value=np.nan), 2**70),
+            ("Int64", pd.NaT),
+            ("boolean", pd.NaT),
+            ("int64[pyarrow]", 2**70),
+        ],
+    )
+    def test_loc_setitem_with_expansion_series_cannot_hold(self, dtype, item):
+        # GH#70233 a value the dtype cannot hold used to raise instead of
+        #  widening to object
+        if "pyarrow" in str(dtype):
+            pytest.importorskip("pyarrow")
+        ser = pd.Series([1, 0], dtype=dtype)
+        original = list(ser)
+
+        with tm.assert_produces_warning(Pandas4Warning, match="incompatible dtype"):
+            ser.loc[2] = item
+
+        expected = pd.Series([*original, item], dtype=object)
+        tm.assert_series_equal(ser, expected)
+
+    def test_loc_setitem_with_expansion_all_na_str_large_int(self):
+        # GH#70233 the value must not be rounded through float64
+        pytest.importorskip("pyarrow")
+        dtype = pd.StringDtype("pyarrow", na_value=np.nan)
+        ser = pd.Series([np.nan, np.nan], dtype=dtype)
+
+        with tm.assert_produces_warning(Pandas4Warning, match="incompatible dtype"):
+            ser.loc[2] = 2**64 - 1
+
+        expected = pd.Series([np.nan, np.nan, 2**64 - 1], dtype=object)
+        tm.assert_series_equal(ser, expected)
+
     def test_loc_setitem_with_expansion_sparse_na(self):
         # GH#65431 pre-casting NaN gives Sparse[float64, nan], not the column's
         #  Sparse[int64, 0]; adopting it used to turn the appended NaN into 0
diff --git a/pandas/tests/series/methods/test_map.py b/pandas/tests/series/methods/test_map.py
index a56e603c84d1f..3a273d775b86d 100644
--- a/pandas/tests/series/methods/test_map.py
+++ b/pandas/tests/series/methods/test_map.py
@@ -759,3 +759,28 @@ def test_map_datetime_series_passes_scalar_timestamps():
         seen = []
         getattr(ser, method)(lambda ts: seen.append(type(ts).__name__))
         assert set(seen) == {"Timestamp"}
+
+
+@pytest.mark.parametrize(
+    "dtype",
+    [
+        pd.StringDtype(na_value=np.nan),
+        pytest.param("string[pyarrow]", marks=td.skip_if_no("pyarrow")),
+        pytest.param("int64[pyarrow]", marks=td.skip_if_no("pyarrow")),
+    ],
+)
+def test_map_result_overflows_int64(dtype):
+    # GH#70233 used to raise OverflowError instead of inferring object
+    ser = pd.Series([1, 0], dtype=dtype)
+    result = ser.map(lambda x: 2**70)
+    expected = pd.Series([2**70, 2**70], dtype=object)
+    tm.assert_series_equal(result, expected)
+
+
+@pytest.mark.parametrize("dtype", ["Int64", "Float64", "boolean"])
+def test_map_masked_result_all_nat(dtype):
+    # GH#70233 used to raise TypeError trying to cast NaT to the masked dtype
+    ser = pd.Series([1, 0], dtype=dtype)
+    result = ser.map(lambda x: pd.NaT)
+    expected = pd.Series([pd.NaT, pd.NaT], dtype="M8[s]")
+    tm.assert_series_equal(result, expected)

```

# REVIEW A

## Review of PR 70233: setitem-with-expansion, `map` and `groupby.agg` raising for a value the dtype cannot hold

The PR is already merged, so this is a retrospective review. I read the diff and checked that `lib.maybe_convert_objects` has a `safe` parameter (`pandas/_libs/lib.pyx:2870`). I didn't build pandas or run the tests.

### Summary
The PR fixes `_cast_pointwise_result` in three places so it falls back to inference instead of raising:
- **`arrow/array.py`**: also catches `OverflowError`.
- **`string_arrow.py`**: also catches `OverflowError`, and the fallback now passes `safe=True`.
- **`masked.py`**: the all-NA cast is wrapped in `try/except TypeError`, so `NaT` falls through to inference.

Fixing this at the source is better than adding more call-site guards, as GH-67974 did. One change covers `Series.loc` expansion, `Series.map` and `groupby.agg`.

### Code quality
- The changes are minimal, targeted and commented with the GH number.
- `safe=True` in the string fallback is a good catch. The `[nan, 2**64-1]` case would otherwise be rounded through float64, and `test_loc_setitem_with_expansion_all_na_str_large_int` covers it.
- **Inconsistency:** the generic arrow fallback in `arrow/array.py` calls `maybe_convert_objects` without `safe=True`. Taking the same overflow path there with NaN next to a large uint64 could lose precision. This is probably an edge case, but the string and arrow paths should behave the same way, or the PR should say why they differ.
- **Narrow `except`:** `masked.py` catches only `TypeError`. Other types, such as `ValueError` from the all-NA `_from_sequence`, would still raise. The test matrix only exercises `NaT`, so I can't tell whether that is enough.
- **Issue reference:** the whatsnew entry uses `:issue:\`70233\``, which is the PR number. pandas convention is to cite an issue number, and the PR text itself refers to GH-67974 and GH-62523. Confirm this is deliberate.

### Potential bugs
- Catching `OverflowError` inside a broad `try` around `pa.array(...)` could mask unrelated overflow errors. It then widens to object silently, apart from the `Pandas4Warning`. This matches 3.0 behaviour, so I think it's acceptable.
- The masked fix covers `NaT`, but other values that `_from_sequence` rejects with `TypeError` now take the inference path too. That seems intended.

### Performance
- No concerns. The `try/except` costs nothing on the success path. The fallback was already the slow object path.

### Security
- None.

### Tests
Coverage is good: the parametrized matrix covers `Series.loc` expansion, `map`, `groupby.agg` and the DataFrame `_post_expansion_casting` path, across the string, pyarrow and masked dtypes.

Gaps I'd suggest closing:
- **`Index.insert`:** `pandas/core/indexes/base.py` also calls `_cast_pointwise_result` (lines 6939 and 7014), but there are no tests for it. If it is affected, it needs coverage.
- **`uint64`:** only `2**70` is tested for the pyarrow int path, not a value in the uint64 range such as `2**64-1`, which would exercise the `safe` question above.
- **Warning check:** the `groupby` and `map` tests don't assert on warnings. That is fine if none is emitted, but it would be good to confirm.
- **`string[pyarrow]` in `test_loc`:** the `string[pyarrow]` dtype is covered in `map` and `groupby` but not in the `loc` expansion test, which uses only `StringDtype(na_value=np.nan)`.

### Overall
This is a solid, well-scoped fix with good tests and an honest AI disclosure. The main follow-ups are consistency of `safe=True` in the arrow path, `Index.insert` coverage, and the issue number in the whatsnew entry.

# REVIEW B

# Review of PR #70233 (merged)

I read the diff only and did not run the tests.

**Verdict:** The fix is small, targeted and correct in approach. The notes below are minor.

## What it does
It fixes the `_cast_pointwise_result` implementations in three places instead of guarding each call site:
- **`ArrowExtensionArray`** (`arrow/array.py`): also catches `OverflowError` and falls back to object inference.
- **`ArrowStringArray`** (`string_arrow.py`): catches `OverflowError` and retries with `safe=True`. This keeps `[nan, 2**64-1]` as object instead of rounding it through float64. `test_loc_setitem_with_expansion_all_na_str_large_int` covers this.
- **`BaseMaskedArray`** (`masked.py`): if the all-NA cast raises `TypeError` (for example on `NaT`), it falls through to inference.

One fix covers setitem-with-expansion, `Series.map` and `groupby.agg`. Fixing the shared hook is better than the earlier GH-67974 approach of guarding only the DataFrame `_append_internal` pre-cast.

## Code quality
- **Masked fallback.** It catches only `TypeError`, which matches the reported `NaT` case. If `_from_sequence` can raise `ValueError` or `OverflowError` for other all-NA inputs, those would still escape. A quick check of that would help. For example, an all-`pd.NA` list or an all-`NaT` array with a datetime64 dtype.
- **Comment wording.** The comment in the masked fix ("e.g. NaT goes through inference instead") is fine. The `string_arrow.py` comment mixes the cause and the reason for `safe=True`, but it's readable.
- **Inconsistent `safe=True`.** The `ArrowExtensionArray` fallback doesn't pass `safe=True`, but the string one does. The two cases differ: the string path may hold NaN alongside ints. It may still be worth confirming that `[nan, 2**64-1]` on a numeric pyarrow dtype can't round through float64. If it can't, a short comment saying why would help.
- **Whatsnew.** `:issue:`70233`` points at this PR number rather than an issue. That's a repo convention question. If there's no separate issue, `:pr:` or the original issue number would be more accurate.

## Potential bugs
- No new regressions are apparent. The new `except` paths only run where the code raised before, so behaviour for values that previously worked is unchanged.
- `Float64` and `boolean` with `NaT` are tested through `map` and `agg`. `Float64` is not in the setitem test, so that is a small gap.

## Performance
- The only added cost is a `try` block, which is free on the success path. `isna(values).all()` was already there, and the earlier commit `b205534899` avoided a per-element NA check, so there is no new regression.

## Security
- None. The change only widens exception handling and falls back to object inference.

## Tests
Coverage is good. It has regression tests across `loc` setitem, `Series.map` and `groupby.agg`, including the float64-rounding edge case. Suggestions:
- Add `Float64` to the Series setitem parametrization for parity with `map` and `agg`.
- Add a `DataFrame.loc` expansion case for the masked/`NaT` path. The pyarrow `2**70` DataFrame case is covered.
- In `test_loc_setitem_with_expansion_series_cannot_hold`, the `"pyarrow" in str(dtype)` check works but is a bit fragile. Using `pytest.param(..., marks=td.skip_if_no("pyarrow"))` would match the style of the other tests.
- Assert that `Pandas4Warning` is raised in the `map` and `agg` tests too, if that warning applies there. The tests currently only check the result.

## Process
- The PR discloses the AI use and says it was reviewed. It notes the backport to 3.1.x.
