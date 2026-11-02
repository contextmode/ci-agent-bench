# PR diff (the real change)

```diff
diff --git a/doc/source/whatsnew/v3.2.0.rst b/doc/source/whatsnew/v3.2.0.rst
index 791947382c3a6..2391401e1c8a7 100644
--- a/doc/source/whatsnew/v3.2.0.rst
+++ b/doc/source/whatsnew/v3.2.0.rst
@@ -29,6 +29,7 @@ enhancement2
 Other enhancements
 ^^^^^^^^^^^^^^^^^^
 - :func:`read_csv` and :func:`read_table` with ``sep=None`` now sniff the separator with the C engine instead of falling back to the slower python engine (:issue:`9645`)
+- :func:`read_csv` with the ``"c"`` and ``"python"`` engines now accepts a :class:`DatetimeTZDtype` in ``dtype`` (:issue:`24542`)
 - :meth:`.DataFrameGroupBy.rank` and :meth:`.SeriesGroupBy.rank` now accept a ``numeric_only`` argument, matching :meth:`DataFrame.rank` (:issue:`44438`)
 - Display formatting for complex numbers in ``object`` dtype and for ``interval`` dtype values with float endpoints now respects the ``display.precision`` and ``display.float_format`` options (:issue:`25920`).
 - The :class:`ExtensionArray` base tests in ``pandas.tests.extension.base`` now issue a :class:`errors.PerformanceWarning` when the array uses the default, possibly slow, implementation of ``unique``, ``factorize``, ``argsort``, ``argmin``, ``argmax``, or ``searchsorted`` (:issue:`24433`)
@@ -189,6 +190,7 @@ MultiIndex
 
 I/O
 ^^^
+- Bug in :func:`read_csv` with ``engine="python"`` and ``index_col`` reading a date like ``"20180101"`` as nanoseconds since the epoch when ``dtype`` is a pyarrow timestamp dtype (:issue:`24542`)
 - Bug in :func:`read_csv`, :func:`read_excel`, :func:`read_fwf` and :func:`read_html` returning wrong column labels and treating header rows as data when ``header`` was a list not in increasing order, such as ``header=[1, 0]`` (:issue:`47011`)
 - Bug in :func:`read_csv`, :meth:`DataFrame.to_csv` and other I/O functions raising ``URLError`` for ``sftp://`` URLs instead of reading or writing them with ``fsspec`` (:issue:`46765`)
 - Bug in :func:`read_excel` raising ``ValueError`` when ``header`` is a list and ``index_col`` consumes all columns (:issue:`66372`)
diff --git a/pandas/core/arrays/datetimes.py b/pandas/core/arrays/datetimes.py
index e78b9efdd7009..4caa948287222 100644
--- a/pandas/core/arrays/datetimes.py
+++ b/pandas/core/arrays/datetimes.py
@@ -319,6 +319,12 @@ def _simple_new(  # type: ignore[override]
     def _from_sequence(cls, scalars, *, dtype=None, copy: bool = False) -> Self:
         return cls._from_sequence_not_strict(scalars, dtype=dtype, copy=copy)
 
+    @classmethod
+    def _from_sequence_of_strings(
+        cls, strings, *, dtype: ExtensionDtype, copy: bool = False
+    ) -> Self:
+        return cls._from_sequence(strings, dtype=dtype, copy=copy)
+
     @classmethod
     def _from_sequence_not_strict(
         cls,
diff --git a/pandas/io/parsers/base_parser.py b/pandas/io/parsers/base_parser.py
index 1f9147a71ff9f..7492458ee9d7f 100644
--- a/pandas/io/parsers/base_parser.py
+++ b/pandas/io/parsers/base_parser.py
@@ -29,6 +29,7 @@
 )
 from pandas.util._exceptions import find_stack_level
 
+from pandas.core.dtypes.base import ExtensionDtype
 from pandas.core.dtypes.common import (
     is_bool_dtype,
     is_dict_like,
@@ -38,6 +39,7 @@
     is_list_like,
     is_object_dtype,
     is_string_dtype,
+    pandas_dtype,
 )
 from pandas.core.dtypes.missing import isna
 
@@ -384,7 +386,19 @@ def _agg_index(self, index) -> Index:
                     index_converter = converters.get(self.index_names[i]) is not None
 
             try_num_bool = not (
-                (cast_type and is_string_dtype(cast_type)) or index_converter
+                (
+                    cast_type
+                    and (
+                        is_string_dtype(cast_type)
+                        # GH#24542 avoid reading "20180101" as epoch ns; numpy
+                        # datetime64 still infers, matching the column path
+                        or (
+                            isinstance(pandas_dtype(cast_type), ExtensionDtype)
+                            and pandas_dtype(cast_type).kind == "M"
+                        )
+                    )
+                )
+                or index_converter
             )
 
             arr, _ = self._infer_types(
diff --git a/pandas/tests/io/parser/dtypes/test_dtypes_basic.py b/pandas/tests/io/parser/dtypes/test_dtypes_basic.py
index 4c1ba1a6fadda..0233f62c6d102 100644
--- a/pandas/tests/io/parser/dtypes/test_dtypes_basic.py
+++ b/pandas/tests/io/parser/dtypes/test_dtypes_basic.py
@@ -572,6 +572,43 @@ def test_explicit_arrow_temporal_dtype(all_parsers):
     tm.assert_frame_equal(result, expected)
 
 
+def test_datetimetz_dtype(all_parsers):
+    # GH#24542 offsets span a DST change, which parse_dates leaves as strings
+    parser = all_parsers
+    dtype = pd.DatetimeTZDtype("ns", "US/Eastern")
+    data = "a,b\n2018-01-01 00:00:00-05:00,1\n,2\n2018-07-01 00:00:00-04:00,3\n"
+    result = parser.read_csv(StringIO(data), dtype={"a": dtype})
+    expected = pd.DataFrame(
+        {
+            "a": pd.array(
+                ["2018-01-01 00:00:00-05:00", None, "2018-07-01 00:00:00-04:00"],
+                dtype=dtype,
+            ),
+            "b": [1, 2, 3],
+        }
+    )
+    tm.assert_frame_equal(result, expected)
+
+
+@xfail_pyarrow  # reads "20180101" as int64, then as epoch nanoseconds
+@pytest.mark.parametrize("dtype_name", ["datetimetz", "arrow_timestamp"])
+def test_datetime_dtype_index_col(all_parsers, dtype_name):
+    # GH#24542
+    parser = all_parsers
+    if dtype_name == "arrow_timestamp":
+        pa = pytest.importorskip("pyarrow")
+        dtype = pd.ArrowDtype(pa.timestamp("ns", tz="UTC"))
+    else:
+        dtype = pd.DatetimeTZDtype("ns", "US/Eastern")
+    data = "a,b\n20180101,1\n,2\n"
+    result = parser.read_csv(StringIO(data), dtype={"a": dtype}, index_col="a")
+    expected = pd.DataFrame(
+        {"b": [1, 2]},
+        index=pd.Index(["2018-01-01", None], dtype=dtype, name="a"),
+    )
+    tm.assert_frame_equal(result, expected)
+
+
 @xfail_pyarrow  # true_values/false_values not supported by the pyarrow engine
 def test_nullable_boolean_dtype_with_true_false_values(all_parsers):
     # User-supplied true_values/false_values augment the default token set.

```

# REVIEW A

## Review of PR #70960: support `DatetimeTZDtype` in `read_csv` `dtype`

The PR is already merged. I read the diff and did not build it or run the tests.

**Summary:** The change adds `DatetimeArray._from_sequence_of_strings`, which delegates to `_from_sequence`. This is the same pattern `PeriodArray` uses. It also stops the python engine's `index_col` path from numerically inferring values like `"20180101"` when the target dtype is an extension datetime dtype. The scope is small and the reasoning is clear.

### Code quality
- The `_from_sequence_of_strings` delegation is minimal and consistent with the existing `PeriodArray` code.
- In `_agg_index` (`base_parser.py`), `pandas_dtype(cast_type)` is called twice in the same expression. Compute it once, for example `dtype = pandas_dtype(cast_type)`, and reuse it. The nested boolean is also hard to read, so a small helper or a pre-computed `skip_inference` variable would make it clearer.
- `.kind == "M"` is a reasonable way to detect datetime-like extension dtypes. A comment noting that this deliberately covers `DatetimeTZDtype` and `ArrowDtype` timestamps would help. `ArrowDtype.kind` returns `"M"` for timestamps, but it would also be true for pyarrow `date32` and `date64` types. I haven't checked that, so it is worth confirming whether they should be treated the same way.
- The `cast_type and ...` guard runs before `pandas_dtype(cast_type)`. If `cast_type` is an invalid string, `pandas_dtype` would raise here instead of at the later cast. Please check that the error message and location are still sensible.
- `_from_sequence_of_strings` ignores `copy` semantics for string input, which is harmless. The `dtype: ExtensionDtype` annotation is required, but `_from_sequence` accepts `dtype=None`. That is fine here because the parser always passes a dtype.

### Potential bugs
- **Mixed offsets.** The test covers `-05:00` and `-04:00` in one column. I don't see coverage for what happens with naive strings, or with a `Z` or UTC offset converted into a non-UTC target tz. `pd.array(strings, dtype=tz)` has particular semantics here: naive strings are localized, and aware strings are converted. A short test pinning this behavior would document it.
- **Other `na_values` or `""`.** The test covers the empty string becoming `NaT`. Custom `na_values` that reach the cast as `NaN` rather than `None` are not covered. They probably work, but they are untested.
- **Unit mismatch.** The tests only use `"ns"`. A `DatetimeTZDtype("s", ...)` or `"us"` case would confirm that the resolution is preserved.
- **`index_col` with a list or MultiIndex.** The `_agg_index` change applies per level, but only a single `index_col` is tested.
- **Skipped inference scope.** The PR notes that skipping inference for all extension dtypes would break `boolean` and `category`. The narrower `kind == "M"` check is the right choice. `Period` and `Interval` index dtypes may have the same epoch-style problem, but that is outside this PR.

### Performance
No concerns. `pandas_dtype` is called once or twice per index column, not per row, and string parsing goes through the existing `_from_sequence` path.

### Security
No concerns.

### Tests
- `test_datetimetz_dtype` runs on all parsers, and `xfail_pyarrow` is correctly applied only to the index test. The pyarrow engine already supported this dtype.
- `test_datetime_dtype_index_col` is parametrized over tz-aware and arrow timestamp dtypes, which covers both branches of the new condition. It would help to add a regression test confirming that numpy `datetime64` still infers, as the code comment claims, along with `boolean` and `category` `index_col` cases. The PR description says these would break, but no new test guards them. Existing tests may cover them, and I didn't check.
- The `xfail_pyarrow` comment is slightly confusing. The pyarrow engine reading `"20180101"` as int64 is the behavior being avoided, so please state plainly why it fails there.

### Docs
- The whatsnew entries are in the right sections.
- The I/O bug entry is specific to the python engine with pyarrow timestamps, which matches the behavior change.
- The enhancement entry could use double-backtick formatting for `"c"` and `"python"`, which it already has. It might also link `DatetimeTZDtype` with the `~pandas.DatetimeTZDtype` role if that doesn't resolve.

### Process
The AI disclosure is present and includes the model and reasoning level, as AGENTS.md asks.

### Verdict
This is a reasonable, well-scoped change. The suggestions are minor: avoid the duplicate `pandas_dtype` call, extend the tests (naive and non-ns inputs, and regression guards for the inference skip), and check how `date32` and `date64` Arrow types behave under the `kind == "M"` check.

# REVIEW B

# Review of PR #70960: `read_csv` support for `DatetimeTZDtype` (GH#24542)

The PR is already merged, so this is a retrospective review. I read the diff and description only. I didn't build pandas or run the tests.

## Summary
The change adds `DatetimeArray._from_sequence_of_strings`, which delegates to `_from_sequence` as `PeriodArray` does. That lets the c and python parsers build tz-aware columns from the `dtype=` argument. It also stops the python engine's `index_col` path from running numeric inference on extension datetime dtypes. The approach is small and consistent with existing patterns, and the description explains well why the `index_col` skip is limited to datetime kinds.

## Code quality
- **`base_parser.py` calls `pandas_dtype(cast_type)` twice** in one expression. Resolve it once, for example `dtype = pandas_dtype(cast_type)` before computing `try_num_bool`. Also confirm `cast_type` can't be something `pandas_dtype` rejects here. It is probably already validated upstream, but that is worth a check.
- **The condition is hard to read.** It is nested `and`/`or` inside a `not (...)`. A small helper, or splitting it into two named booleans such as `skip_inference_for_dtype`, would be clearer.
- **The `kind == "M"` check is implicit.** It relies on `ArrowDtype.kind` returning `"M"` for timestamps. That works today, but a short comment saying so would help. `ArrowDtype` date32/date64 and duration types are not covered by this check. That is fine, but the intent should be stated.
- **The `_from_sequence_of_strings` signature** matches the ExtensionArray API, and `copy` is passed through. A one-line docstring or comment saying it is deliberately the same as `_from_sequence` would help the next reader.

## Potential bugs and edge cases
- **Tz semantics are untested.** The new test only uses strings whose offsets are consistent with the target tz, plus a missing value. Behaviour is untested for:
  - tz-naive strings, which `_from_sequence` localizes to the dtype's tz;
  - strings with a different offset or tz than the dtype, which get converted;
  - mixed offsets, which are the stated motivation.

  Add at least a naive-string case and a different-offset case to pin the documented behaviour.
- **Only `unit="ns"` is tested.** `DatetimeTZDtype("us", ...)` and `"s"` should work, and a parametrization would show it.
- **The `index_col` test with `datetimetz` is xfailed for pyarrow** because that engine reads `"20180101"` as int64. The xfail comment is reasonable, but it documents a pyarrow-engine discrepancy rather than fixing it. A follow-up issue would be worth opening if one doesn't exist.
- **The c engine `index_col` path** is exercised by the same test via `all_parsers`. Because `_agg_index` is python-engine specific, the test passing on c depends on the c engine already doing the right thing. That is fine, but the test comment could say so.
- **A column with `dtype` plus `parse_dates` on the same column** is not tested. It would be good to confirm there is no double conversion or conflict.

## Performance
Negligible. The extra `pandas_dtype` calls run once per index column. Delegating to `_from_sequence` goes through the standard datetime string parser, the same as `pd.array(strings, dtype=tz)`.

## Security
No concerns. The change adds no new I/O, deserialization, or eval paths.

## Test coverage
Coverage is reasonable but could be broader:
- Good: tz column with NA, and `index_col` for both `DatetimeTZDtype` and an Arrow timestamp.
- Missing: the edge cases listed above, plus an invalid string, which should raise a clear error. Tests for `DatetimeArray._from_sequence_of_strings` in `pandas/tests/arrays/datetimes` or the extension tests would also be useful, since `PeriodArray` has equivalents.

## Docs
- **The whatsnew enhancement entry is good.** Consider making it `:class:`DatetimeTZDtype`` with the `pandas.` prefix if that is the convention nearby.
- **The I/O bug entry** is accurate. It mentions only pyarrow timestamps, even though tz-aware dtypes were also affected on the python-engine `index_col` path. Since tz-aware `index_col` previously raised `NotImplementedError` anyway, that wording is defensible.

## Verdict
This is a clean, minimal change with a correct approach. The main follow-ups are to resolve `pandas_dtype` once, and to add tests for naive and different-offset strings and for non-ns units.
