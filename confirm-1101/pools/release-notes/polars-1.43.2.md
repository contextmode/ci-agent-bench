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
