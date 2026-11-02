# Judge file r2-polars-1.43.2

## PUBLISHED RELEASE NOTES (written by the maintainers)

## ⚠️ Deprecations

- Deprecate casts from `Categorical` to integer dtypes (#28525)
- Deprecate not setting the `plan_stage` argument in `show_graph()` (#28391)

## 🚀 Performance improvements

- Pushdown `len()` to concat/union inputs (#28570)

## ✨ Enhancements

- Issue FutureWarning on using `from_arrow` of ArrowStreamExportable (#28442)
- Add `infer_schema_files` parameter to `scan_csv` (#28440)

## 🐞 Bug fixes

- Properly propagate enum metadata for iceberg column mapping (#28580)
- Correctly write parquet field IDs for enums and categoricals (#28581)
- Fix arrow C interop binview offset (#28623)
- Fix duplicate hive values in hive pre-partition rewrite (#28621)
- Double-counted offset for Arrow export of sliced `Series(Array)` (#28602)
- Struct/List/Array equality handling in sort and join (#28601)
- More careful slice pushdown into joins (#28578)
- Preserve ordering in sliced unions (#28576)
- Drop input sortedness when casting to a string (#28574)
- Clear sortedness flags in `StringChunked` substring kernels (#28573)
- Bad mask handling when reading optional parquet column (#28547)
- Any operation on `Unknown(Int)` and `Unknown(Float)` should result in `Unknown(Float)` (#28545)
- Flip `nulls_last` after `Expr.reverse()` (#28572)
- Fix high blocking thread use in sink\_parquet with async local path (#28543)
- Serialize LazyFrames backed by bytes (#28568)
- Release GIL in `SQLContext.execute()` (#28549)
- Propagate `nulls_last` in `function_expr_sortedness` (#28544)
- Incorrect slicing when a join requires sorting (#28541)

## 🛠️ Other improvements

- Fix duckdb delta extension install collision (#28607)

Thank you to all our contributors for making this release possible!
@BitWeaverDev, @Matt711, @Samoilov2004, @borchero, @dancsi, @dsprenkels, @kdn36, @masumi-ryugo, @nameexhaustion and @ritchie46


## COMMIT SUBJECTS between the previous tag and the release

feat: Add `infer_schema_files` parameter to `scan_csv` (#28440)
feat(rust): Serialize and deserialize `SinkTypeIR::Partitioned` (#28112)
fix: Incorrect slicing when a join requires sorting (#28541)
feat(python): Issue FutureWarning on using `from_arrow` of ArrowStreamExportable (#28442)
fix: Propagate `nulls_last` in `function_expr_sortedness` (#28544)
fix: Release GIL in `SQLContext.execute()` (#28549)
fix: Serialize LazyFrames backed by bytes (#28568)
depr: Deprecate not setting the `plan_stage` argument in `show_graph()` (#28391)
fix: Fix high blocking thread use in sink_parquet with async local path (#28543)
depr: Deprecate casts from `Categorical` to integer dtypes (#28525)
fix: Flip `nulls_last` after `Expr.reverse()` (#28572)
fix: Any operation on `Unknown(Int)` and `Unknown(Float)` should result in `Unknown(Float)` (#28545)
fix: Bad mask handling when reading optional parquet column (#28547)
fix: Clear sortedness flags in `StringChunked` substring kernels (#28573)
fix: Drop input sortedness when casting to a string (#28574)
fix: Preserve ordering in sliced unions (#28576)
fix: More careful slice pushdown into joins (#28578)
fix(rust): Run type coercion pass on pivot's internally generated group_by (#27897)
fix(rust): Raise ComputeError instead of panicking in repeat_by when output exceeds IdxSize::MAX (#27892)
fix(rust): Use try_new in StructArray construction in polars-json (#27489)
ci: Fix duckdb delta extension install collision (#28607)
fix: Struct/List/Array equality handling in sort and join (#28601)
fix: Double-counted offset for Arrow export of sliced `Series(Array)` (#28602)
fix: Fix duplicate hive values in hive pre-partition rewrite (#28621)
perf: Pushdown `len()` to concat/union inputs (#28570)
fix: Fix arrow C interop binview offset (#28623)
Python Polars 1.43.2 (#28625)
fix: Correctly write parquet field IDs for enums and categoricals (#28581)
fix: Properly propagate enum metadata for iceberg column mapping (#28580)

# CANDIDATE A

## 🚀 Performance improvements
- Push `len()` down into concat/union inputs ([#28570](https://github.com/pola-rs/polars/pull/28570))

## ✨ Enhancements
- Add `infer_schema_files` parameter to `scan_csv` ([#28440](https://github.com/pola-rs/polars/pull/28440))
- Issue a `FutureWarning` when `from_arrow` is given an Arrow stream-exportable object ([#28442](https://github.com/pola-rs/polars/pull/28442))
- Serialize and deserialize partitioned sinks in query plans ([#28112](https://github.com/pola-rs/polars/pull/28112))

## ⚠️ Deprecations
- Deprecate casts from `Categorical` to integer dtypes ([#28525](https://github.com/pola-rs/polars/pull/28525))
- Deprecate not setting the `plan_stage` argument in `show_graph()` ([#28391](https://github.com/pola-rs/polars/pull/28391))

## 🐞 Bug fixes
- Fix `Expr.reverse()` so it correctly flips `nulls_last` ([#28572](https://github.com/pola-rs/polars/pull/28572))
- Fix arithmetic on untyped integer and float literals (e.g. `pl.lit(-1).abs()`) to give a float result ([#28545](https://github.com/pola-rs/polars/pull/28545))
- Fix wrong results when reading optional Parquet columns with a mask ([#28547](https://github.com/pola-rs/polars/pull/28547))
- Fix Parquet field IDs written for Enum and Categorical columns ([#28581](https://github.com/pola-rs/polars/pull/28581))
- Fix Enum metadata handling in Iceberg column mapping ([#28580](https://github.com/pola-rs/polars/pull/28580))
- Fix Arrow C interface export of binview data with an offset ([#28623](https://github.com/pola-rs/polars/pull/28623))
- Fix wrong offset when exporting a sliced `Array` Series to Arrow ([#28602](https://github.com/pola-rs/polars/pull/28602))
- Fix duplicate hive partition values in the hive pre-partition rewrite ([#28621](https://github.com/pola-rs/polars/pull/28621))
- Fix Struct, List and Array equality handling in sorts and joins ([#28601](https://github.com/pola-rs/polars/pull/28601))
- Fix slice pushdown into joins to be more careful ([#28578](https://github.com/pola-rs/polars/pull/28578))
- Fix incorrect slicing when a join requires sorting ([#28541](https://github.com/pola-rs/polars/pull/28541))
- Preserve row order in sliced unions ([#28576](https://github.com/pola-rs/polars/pull/28576))
- Drop stale sortedness information when casting to string ([#28574](https://github.com/pola-rs/polars/pull/28574))
- Clear sortedness flags in string substring operations ([#28573](https://github.com/pola-rs/polars/pull/28573))
- Propagate `nulls_last` correctly when determining expression sortedness ([#28544](https://github.com/pola-rs/polars/pull/28544))
- Fix high blocking-thread usage in `sink_parquet` with async local paths ([#28543](https://github.com/pola-rs/polars/pull/28543))
- Fix serialization of LazyFrames backed by bytes ([#28568](https://github.com/pola-rs/polars/pull/28568))
- Release the GIL in `SQLContext.execute()` ([#28549](https://github.com/pola-rs/polars/pull/28549))
- Run type coercion on the internal `group_by` generated by `pivot` ([#27897](https://github.com/pola-rs/polars/pull/27897))
- Raise a `ComputeError` instead of panicking when `repeat_by` output exceeds the maximum row count ([#27892](https://github.com/pola-rs/polars/pull/27892))
- Return an error instead of panicking when building structs in JSON reading ([#27489](https://github.com/pola-rs/polars/pull/27489))

## 🛠️ Other improvements
- Fix duckdb delta extension install collision in CI ([#28607](https://github.com/pola-rs/polars/pull/28607))
- Release Python Polars 1.43.2 ([#28625](https://github.com/pola-rs/polars/pull/28625))


# CANDIDATE B

## 🏆 Highlights

- Add `infer_schema_files` parameter to `scan_csv` (#28440)

## ⚠️ Deprecations

- Deprecate casts from `Categorical` to integer dtypes (#28525)
- Deprecate not setting the `plan_stage` argument in `LazyFrame.show_graph()`; the default will change from `"ir"` to `"physical"` in Polars 2.0 (#28391)
- Issue a `FutureWarning` when `from_arrow` is used on an Arrow stream-exportable object; use the `DataFrame` constructor instead (#28442)

## 🚀 Performance improvements

- Push `len()` down into concat/union inputs (#28570)
- Fix high blocking-thread use in `sink_parquet` with an async local path (#28543)

## ✨ Enhancements

- Add `infer_schema_files` parameter to `scan_csv` to control how many files are used for schema inference (#28440)
- Support serializing and deserializing partitioned sinks in query plans (#28112)
- Release the GIL in `SQLContext.execute()` (#28549)

## 🐞 Bug fixes

- Fix Arrow C interface export of sliced `Series(Array)`, which double-counted the offset (#28602)
- Fix Arrow C interface binview offset handling (#28623)
- Fix incorrect results from struct, list and array equality in sort and join (#28601)
- Fix incorrect slicing when a join requires sorting (#28541)
- Be more careful when pushing slices down into joins (#28578)
- Preserve ordering in sliced unions (#28576)
- Fix duplicate hive values in the hive partition rewrite (#28621)
- Fix bad mask handling when reading an optional Parquet column (#28547)
- Write correct Parquet field IDs for enums and categoricals (#28581)
- Propagate enum metadata correctly for Iceberg column mapping (#28580)
- Flip `nulls_last` after `Expr.reverse()` (#28572)
- Propagate `nulls_last` when determining expression sortedness (#28544)
- Drop sortedness information when casting to string (#28574)
- Clear sortedness flags in string substring kernels (#28573)
- Make operations on `Unknown(Int)` and `Unknown(Float)` give `Unknown(Float)` (#28545)
- Serialize LazyFrames backed by bytes (#28568)
- Run the type coercion pass on the internal `group_by` generated by `pivot` (#27897)
- Raise a `ComputeError` instead of panicking in `repeat_by` when the output exceeds `IdxSize::MAX` (#27892)
- Return an error instead of panicking when building structs while parsing JSON (#27489)

## 🛠️ Other improvements

- Fix DuckDB delta extension install collision in CI (#28607)
- Replace internal and test usages of `from_arrow()` with `DataFrame()` (#28442)
- Release Python Polars 1.43.2 (#28625)

