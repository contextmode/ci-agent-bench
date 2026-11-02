# PR diff (the real change)

```diff
diff --git a/pkg/storage/unified/resource/bleve_index_metrics.go b/pkg/storage/unified/resource/bleve_index_metrics.go
index 5c276df42e587..15bf9c4a914c5 100644
--- a/pkg/storage/unified/resource/bleve_index_metrics.go
+++ b/pkg/storage/unified/resource/bleve_index_metrics.go
@@ -20,6 +20,10 @@ type BleveIndexMetrics struct {
 	SearchUpdateWaitTime *prometheus.HistogramVec
 	RebuildQueueLength   prometheus.Gauge
 
+	GlobalUpdateRoundDuration prometheus.Histogram
+	GlobalUpdateRoundIndexes  prometheus.Gauge
+	GlobalReconcileDuration   *prometheus.HistogramVec
+
 	IndexSnapshotDownloadAttempts         *prometheus.CounterVec
 	IndexSnapshotDownloadDuration         prometheus.Histogram
 	IndexSnapshotUploads                  *prometheus.CounterVec
@@ -135,6 +139,24 @@ func ProvideIndexMetrics(reg prometheus.Registerer) *BleveIndexMetrics {
 			Name: "grafana_index_server_rebuild_queue_length",
 			Help: "Number of indexes waiting for rebuild",
 		}),
+		GlobalUpdateRoundDuration: promauto.With(reg).NewHistogram(prometheus.HistogramOpts{
+			Name:                            "grafana_index_server_global_update_round_duration_seconds",
+			Help:                            "Time to update every open global search index once in the background. A round close to the update interval means the indexes fall behind.",
+			NativeHistogramBucketFactor:     1.1,
+			NativeHistogramMaxBucketNumber:  160,
+			NativeHistogramMinResetDuration: time.Hour,
+		}),
+		GlobalUpdateRoundIndexes: promauto.With(reg).NewGauge(prometheus.GaugeOpts{
+			Name: "grafana_index_server_global_update_round_indexes",
+			Help: "Number of global search indexes the last background update round covered",
+		}),
+		GlobalReconcileDuration: promauto.With(reg).NewHistogramVec(prometheus.HistogramOpts{
+			Name:                            "grafana_index_server_global_reconcile_duration_seconds",
+			Help:                            "Time to compare one global search index with storage and repair what differs",
+			NativeHistogramBucketFactor:     1.1,
+			NativeHistogramMaxBucketNumber:  160,
+			NativeHistogramMinResetDuration: time.Hour,
+		}, []string{"result"}),
 		IndexSnapshotDownloadAttempts: promauto.With(reg).NewCounterVec(prometheus.CounterOpts{
 			Name: "grafana_index_server_snapshot_download_attempts_total",
 			Help: "Number of remote index snapshot download attempts at index build time, by selection policy and outcome.",
diff --git a/pkg/storage/unified/resource/global_search.go b/pkg/storage/unified/resource/global_search.go
index 563e957bdce84..d13f6b7f72ed4 100644
--- a/pkg/storage/unified/resource/global_search.go
+++ b/pkg/storage/unified/resource/global_search.go
@@ -366,9 +366,21 @@ func (s *searchServer) reconcileGlobalIndex(ctx context.Context, key NamespacedR
 		return nil
 	}
 	startedAt := time.Now()
+	var reindexed, removed, failed int
 	var errs []error
+	defer func() {
+		result := "success"
+		if len(errs) > 0 {
+			result = "failure"
+		}
+		elapsed := time.Since(startedAt)
+		s.indexMetrics.GlobalReconcileDuration.WithLabelValues(result).Observe(elapsed.Seconds())
+		s.log.Info("Reconciled global search index", "namespace", key.Namespace, "result", result, "duration", elapsed,
+			"reindexed", reindexed, "removed", removed, "failed", failed)
+	}()
 	for _, src := range indexSources(key) {
 		if ctx.Err() != nil {
+			errs = append(errs, ctx.Err())
 			return ctx.Err()
 		}
 		res, err := s.reconcileResourceType(ctx, idx, key, src)
@@ -377,6 +389,9 @@ func (s *searchServer) reconcileGlobalIndex(ctx context.Context, key NamespacedR
 			errs = append(errs, fmt.Errorf("reconciling %s: %w", src.GroupResource(), err))
 			continue
 		}
+		reindexed += res.Reindexed
+		removed += res.Removed
+		failed += res.Failed
 		if res.Reindexed > 0 || res.Removed > 0 || res.Failed > 0 {
 			s.log.Info("reconciled a resource type of the global search index", "namespace", key.Namespace, "resource", src.GroupResource(),
 				"reindexed", res.Reindexed, "removed", res.Removed, "failed", res.Failed)
diff --git a/pkg/storage/unified/resource/global_search_lifecycle_test.go b/pkg/storage/unified/resource/global_search_lifecycle_test.go
index 2b3cfe4853025..cce7e761b4c7b 100644
--- a/pkg/storage/unified/resource/global_search_lifecycle_test.go
+++ b/pkg/storage/unified/resource/global_search_lifecycle_test.go
@@ -1357,7 +1357,7 @@ func TestUpdateGlobalIndexes(t *testing.T) {
 			dashboards: dashboardsIdx,
 		},
 	}
-	s := &searchServer{search: backend, log: log.NewNopLogger(), ownsIndexFn: func(NamespacedResource) (bool, error) { return true, nil }}
+	s := &searchServer{search: backend, log: log.NewNopLogger(), indexMetrics: ProvideIndexMetrics(nil), ownsIndexFn: func(NamespacedResource) (bool, error) { return true, nil }}
 
 	s.updateGlobalIndexes(t.Context())
 
@@ -1682,3 +1682,34 @@ func TestFailedReconcileIsNotRecorded(t *testing.T) {
 	require.Error(t, server.reconcileGlobalIndex(t.Context(), GlobalSearchKey("ns")))
 	assert.Zero(t, idx.reconciledAt)
 }
+
+// A round reports how many indexes it covered, so a pod falling behind shows
+// up as rounds that take as long as the interval.
+func TestUpdateRoundReportsItsIndexes(t *testing.T) {
+	backend := &mockSearchBackend{
+		openIndexes: []NamespacedResource{GlobalSearchKey("a"), GlobalSearchKey("b"), dashboardType("a")},
+		cache: map[NamespacedResource]ResourceIndex{
+			GlobalSearchKey("a"): &MockResourceIndex{},
+			GlobalSearchKey("b"): &MockResourceIndex{},
+			dashboardType("a"):   &MockResourceIndex{},
+		},
+	}
+	metrics := ProvideIndexMetrics(nil)
+	s := &searchServer{search: backend, log: log.NewNopLogger(), indexMetrics: metrics, ownsIndexFn: func(NamespacedResource) (bool, error) { return true, nil }}
+
+	s.updateGlobalIndexes(t.Context())
+
+	assert.Equal(t, 2.0, testutil.ToFloat64(metrics.GlobalUpdateRoundIndexes))
+	assert.Equal(t, 1, testutil.CollectAndCount(metrics.GlobalUpdateRoundDuration))
+}
+
+// Every reconcile is timed, by whether it compared every type.
+func TestReconcileIsTimedByResult(t *testing.T) {
+	server, idx := repairServer(t, &reconcileStorage{}, nil)
+
+	require.NoError(t, server.reconcileGlobalIndex(t.Context(), GlobalSearchKey("ns")))
+	idx.documentRefsErr = errors.New("index unavailable")
+	require.Error(t, server.reconcileGlobalIndex(t.Context(), GlobalSearchKey("ns")))
+
+	assert.Equal(t, 2, testutil.CollectAndCount(server.indexMetrics.GlobalReconcileDuration), "one series for success, one for failure")
+}
diff --git a/pkg/storage/unified/resource/search.go b/pkg/storage/unified/resource/search.go
index 007cff9b036cf..6e71bc519cd65 100644
--- a/pkg/storage/unified/resource/search.go
+++ b/pkg/storage/unified/resource/search.go
@@ -1720,6 +1720,14 @@ func (s *searchServer) runPeriodicGlobalIndexUpdate(ctx context.Context) {
 // date. An index that is not open is left alone: it is brought up to date when it
 // is next opened.
 func (s *searchServer) updateGlobalIndexes(ctx context.Context) {
+	start := time.Now()
+	updated := 0
+	defer func() {
+		elapsed := time.Since(start)
+		s.indexMetrics.GlobalUpdateRoundDuration.Observe(elapsed.Seconds())
+		s.indexMetrics.GlobalUpdateRoundIndexes.Set(float64(updated))
+		s.log.Debug("Updated global search indexes", "indexes", updated, "duration", elapsed)
+	}()
 	for _, key := range s.search.GetOpenIndexes() {
 		if !key.IsGlobal() || !s.ownsGlobalIndex(key) {
 			continue
@@ -1731,6 +1739,7 @@ func (s *searchServer) updateGlobalIndexes(ctx context.Context) {
 		if idx == nil {
 			continue
 		}
+		updated++
 		if _, err := idx.UpdateIndex(ctx); err != nil {
 			// Logged and left for the next tick: the index keeps serving what it has.
 			s.log.Warn("failed to update global search index", "namespace", key.Namespace, "error", err)
@@ -2326,6 +2335,10 @@ func (s *searchServer) build(ctx context.Context, nsr NamespacedResource, size i
 
 		// indexSource indexes every live object of one resource type, and returns
 		// the resource version the listing was taken at, even when it fails.
+		// How many documents each type contributed, logged once the build is done,
+		// so the cost of a build can be read against the size of what it built.
+		indexedDocs := map[string]int{}
+
 		indexSource := func(src NamespacedResource) (int64, error) {
 			builder, err := getBuilder(ctx, src)
 			if err != nil {
@@ -2391,6 +2404,7 @@ func (s *searchServer) build(ctx context.Context, nsr NamespacedResource, size i
 					if err := batch.add(&BulkIndexItem{Action: ActionIndex, Doc: doc}); err != nil {
 						return err
 					}
+					indexedDocs[src.GroupResource()]++
 				}
 
 				if err := batch.flush(); err != nil {
@@ -2438,6 +2452,8 @@ func (s *searchServer) build(ctx context.Context, nsr NamespacedResource, size i
 			}
 		}
 
+		logger.Info("Listed documents for index", "documents", indexedDocs)
+
 		// A namespace-wide index holds only live documents, so it has no trash to
 		// restore.
 		if nsr.IsGlobal() {

```

# REVIEW A

**Review of PR 134038: global index update and reconcile metrics**

This PR is already merged. I read the diff but didn't run the tests. Overall it's a small, focused change and it follows the repo's conventions. I found a few issues, none of them blocking.

**Bugs and correctness**

1. **A misplaced comment in `search.go`.** The new `indexedDocs` declaration sits between the existing `// indexSource indexes every live object...` doc comment and the `indexSource` closure. That comment now reads as if it describes `indexedDocs`, and the `indexSource` comment is cut off. Move the new block above the `indexSource` comment.

2. **Possible data race on `indexedDocs`.** The map is written inside the `indexSource` closure. If any code path runs `indexSource` from multiple goroutines, for example one per resource type, the unguarded `map[string]int` will panic with "concurrent map writes". I didn't confirm how `indexSource` is called, so check that before relying on it. Otherwise this is fine.

3. **The "indexes covered" gauge counts attempts, not successes.** `updated++` runs before `UpdateIndex`, so indexes whose update fails are still counted. That is acceptable for "indexes covered", but the help text should say so. It also matters for the duration metric: a failing index can finish fast and make the round look healthy.

4. **Context cancellation is recorded as a reconcile failure.** The new `errs = append(errs, ctx.Err())` makes shutdown or cancellation show up as `result="failure"`. That will add noise to any alert built on that label. Consider a separate `result="canceled"` label, or skip observing the metric when `ctx` is done.

5. **The "success" label can hide partial work.** `failed` counts resource types that failed to reindex, but `result` is based only on `len(errs)`. If `res.Failed > 0` and `err == nil`, the reconcile is labelled "success". Check whether `res.Failed > 0` should also give `failure`.

**Observability and design**

- The metric descriptions say "Number of global search indexes the last background update round covered". A gauge that is overwritten each round is fine, but it will report 0 for rounds where the pod owns no indexes. That is probably what you want.
- `Reconciled global search index` is logged at Info for every reconcile, in every namespace. The PR states this is deliberate because the metric has no namespace label. On large multi-tenant deployments this could be a lot of log volume, so confirm it's acceptable or add some sampling.
- `logger.Info("Listed documents for index", "documents", indexedDocs)` logs a map. That works, but it is non-deterministic in order and may format awkwardly in some log backends. Consider logging a sorted key=value string, or one field per resource type.
- The log message styles are mixed: some are capitalised ("Reconciled…", "Updated…") and the neighbouring ones are lowercase ("reconciled a resource type…"). Pick one.

**Performance**

The overhead is negligible: one `time.Since`, one histogram observation and one map increment per document. The map increment is on the indexing hot path, but it is cheap compared with doc building and batching.

**Tests**

- `TestUpdateRoundReportsItsIndexes` and `TestReconcileIsTimedByResult` cover the new metrics. Both only check that a series exists, through `CollectAndCount`. They don't check the label values, so they would still pass if "success" and "failure" were swapped. Use `testutil.CollectAndCompare`, or look up the histograms with `WithLabelValues`.
- There is no test for the context-cancellation path that now appends `ctx.Err()`.
- There is no test for the `indexedDocs` build log.
- The existing `TestUpdateGlobalIndexes` needed `indexMetrics: ProvideIndexMetrics(nil)`. Any other place that builds a `searchServer` without `indexMetrics` would now panic with a nil dereference in these deferred blocks. A nil check or a constructor default would be more robust. Make sure no other test or production path leaves `indexMetrics` unset.

**Security**

No concerns.

**Summary**

The metrics are useful and the implementation is simple. The items I'd follow up on are the misplaced comment, the `indexSource` concurrency question, the cancellation and partial-failure labelling, and making the tests assert label values.

# REVIEW B

**Review of PR #134038: global index update and reconcile metrics** (the PR is already merged)

Overall this is a small, focused observability change, and the tests cover the main paths. I found a few things worth fixing, most of them minor.

**Issues**

1. **Misplaced comment in `search.go`.** The new `indexedDocs` declaration was inserted between the existing `// indexSource indexes every live object...` doc comment and the `indexSource` closure. That comment now sits above the wrong declaration. Move the `indexedDocs` block above the comment.

2. **Possible data race on `indexedDocs`.** The map is incremented inside the `indexSource` closure. If any caller runs `indexSource` concurrently, for example one goroutine per resource type, this is a concurrent map write and will panic. I only saw the diff, not the call sites. Please check that the calls are sequential. If they aren't, guard the map or use per-source counters.

3. **Cancellation in `reconcileGlobalIndex`.** The PR appends `ctx.Err()` to `errs` before returning, so the deferred metric records `result="failure"`. That is deliberate, but the function returns `ctx.Err()` directly. The metric and log stay consistent, but shutdown cancellations will count as failures. Consider a separate `canceled` result, or skip observing on cancellation. Otherwise they add noise to the failure series.

4. **The reconcile `Info` log may be noisy.** It now logs once per namespace per reconcile, and the log fires even when nothing changed. The PR notes the metric has no namespace label, which is why the log exists. With many namespaces this could be high-volume, so you could log at Info only when `reindexed/removed/failed > 0` and otherwise use Debug. Per-type logs already follow that pattern.

5. **Early-return paths skip the metric.** The earlier `return nil` before `startedAt` (the "skip" case) is not timed. That is probably intended. It's worth confirming that `result` should only cover reconciles that actually ran.

6. **Gauge semantics.** `GlobalUpdateRoundIndexes` is set to `updated`, and `updated` is incremented before `UpdateIndex`, so it counts indexes attempted, not indexes that succeeded. The help text says "covered", which is fine. But if `ctx` is cancelled mid-round, the duration histogram still gets a partial observation. That could skew the "falling behind" signal downward at shutdown. This is minor.

7. **Nil `indexMetrics` risk.** Both functions now dereference `s.indexMetrics` unconditionally, and the PR had to patch an existing test to supply it. Any other construction of `searchServer` (tests or alternate constructors) that leaves `indexMetrics` nil will now panic. A grep for `&searchServer{` would confirm that all of them set it.

8. **Log field type.** `logger.Info("Listed documents for index", "documents", indexedDocs)` passes a map as a structured value. Depending on the logger backend, this may render as `map[...]` and be hard to query. Flattening to a string or to one key per type is friendlier.

**Positives**
- Metric names follow the `grafana_` full-name convention in `contribute/backend/instrumentation.md`.
- Native histograms are configured consistently with the neighbouring metrics.
- The `defer` approach keeps every exit path measured.
- The tests check both result series and the gauge value.

**Test coverage**
- `TestReconcileIsTimedByResult` only checks the series count, not the observed values or the labels. Asserting that the `success` and `failure` labels exist would be stronger.
- There is no test for the ctx-cancel path, and none for the new `indexedDocs` logging.

I only read the diff and didn't build or run anything.
