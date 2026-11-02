# PR diff (the real change)

```diff
diff --git a/storage/remote/read_handler.go b/storage/remote/read_handler.go
index 28244f97e5b..9265793b85f 100644
--- a/storage/remote/read_handler.go
+++ b/storage/remote/read_handler.go
@@ -22,6 +22,7 @@ import (
 	"slices"
 	"strings"
 	"sync"
+	"time"
 
 	"github.com/prometheus/client_golang/prometheus"
 
@@ -41,6 +42,7 @@ type readHandler struct {
 	remoteReadMaxBytesInFrame int
 	remoteReadGate            *gate.Gate
 	queries                   prometheus.Gauge
+	gateWaitDuration          prometheus.Histogram
 	marshalPool               *sync.Pool
 }
 
@@ -63,16 +65,30 @@ func NewReadHandler(logger *slog.Logger, r prometheus.Registerer, queryable stor
 			Name:      "queries",
 			Help:      "The current number of remote read queries that are either in execution or queued on the handler.",
 		}),
+		gateWaitDuration: prometheus.NewHistogram(prometheus.HistogramOpts{
+			Namespace:                       namespace,
+			Subsystem:                       "remote_read_handler",
+			Name:                            "gate_wait_duration_seconds",
+			Help:                            "How long a remote read request spent waiting for the concurrency gate, including requests canceled while waiting.",
+			NativeHistogramBucketFactor:     1.1,
+			NativeHistogramMaxBucketNumber:  100,
+			NativeHistogramMinResetDuration: 1 * time.Hour,
+		}),
 	}
 	if r != nil {
-		r.MustRegister(h.queries)
+		r.MustRegister(h.queries, h.gateWaitDuration)
 	}
 	return h
 }
 
 func (h *readHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
 	ctx := r.Context()
-	if err := h.remoteReadGate.Start(ctx); err != nil {
+	gateStart := time.Now()
+	err := h.remoteReadGate.Start(ctx)
+	// Observe before checking the error so requests that are canceled while waiting on the gate
+	// are recorded too.
+	h.gateWaitDuration.Observe(time.Since(gateStart).Seconds())
+	if err != nil {
 		http.Error(w, err.Error(), http.StatusInternalServerError)
 		return
 	}
diff --git a/storage/remote/read_handler_test.go b/storage/remote/read_handler_test.go
index d0148965000..988567241b0 100644
--- a/storage/remote/read_handler_test.go
+++ b/storage/remote/read_handler_test.go
@@ -957,3 +957,125 @@ func addNativeHistogramsToTestSuite(t *testing.T, storage *teststorage.TestStora
 
 	require.NoError(t, app.Commit())
 }
+
+func TestRemoteReadGateWaitDurationObserved(t *testing.T) {
+	store := promqltest.LoadedStorage(t, `
+		load 1m
+			test_metric1{foo="bar"} 1
+	`)
+	defer store.Close()
+
+	newRequest := func(t *testing.T) *http.Request {
+		matcher, err := labels.NewMatcher(labels.MatchEqual, "__name__", "test_metric1")
+		require.NoError(t, err)
+		query, err := ToQuery(0, 1, []*labels.Matcher{matcher}, &storage.SelectHints{Step: 0, Func: "avg"})
+		require.NoError(t, err)
+		data, err := proto.Marshal(&prompb.ReadRequest{Queries: []*prompb.Query{query}})
+		require.NoError(t, err)
+		request, err := http.NewRequest(http.MethodPost, "", bytes.NewBuffer(snappy.Encode(nil, data)))
+		require.NoError(t, err)
+		return request
+	}
+
+	gateWaitHistogram := func(t *testing.T, reg *prometheus.Registry) (count uint64, sum float64) {
+		mfs, err := reg.Gather()
+		require.NoError(t, err)
+		for _, mf := range mfs {
+			if mf.GetName() == "prometheus_remote_read_handler_gate_wait_duration_seconds" {
+				hist := mf.GetMetric()[0].GetHistogram()
+				return hist.GetSampleCount(), hist.GetSampleSum()
+			}
+		}
+		t.Fatal("expected gate wait duration histogram to be registered")
+		return 0, 0
+	}
+	gateWaitSampleCount := func(t *testing.T, reg *prometheus.Registry) uint64 {
+		count, _ := gateWaitHistogram(t, reg)
+		return count
+	}
+
+	t.Run("successful acquisition", func(t *testing.T) {
+		reg := prometheus.NewRegistry()
+		h := NewReadHandler(nil, reg, store, func() config.Config {
+			return config.Config{}
+		}, 1e6, 1, 0)
+
+		recorder := httptest.NewRecorder()
+		h.ServeHTTP(recorder, newRequest(t))
+		require.Equal(t, 2, recorder.Code/100)
+
+		require.Equal(t, uint64(1), gateWaitSampleCount(t, reg))
+	})
+
+	t.Run("canceled acquisition", func(t *testing.T) {
+		reg := prometheus.NewRegistry()
+		// A concurrency limit of zero means the gate never opens, so a canceled context
+		// deterministically loses the race in Gate.Start and returns an error.
+		h := NewReadHandler(nil, reg, store, func() config.Config {
+			return config.Config{}
+		}, 1e6, 0, 0)
+
+		ctx, cancel := context.WithCancel(context.Background())
+		cancel()
+
+		recorder := httptest.NewRecorder()
+		h.ServeHTTP(recorder, newRequest(t).WithContext(ctx))
+		require.Equal(t, http.StatusInternalServerError, recorder.Code)
+
+		// The wait is still observed even though the request was canceled at the gate.
+		require.Equal(t, uint64(1), gateWaitSampleCount(t, reg))
+	})
+
+	// holdWait fills the single gate slot, starts a request that has to queue behind it and
+	// calls finish after the request has been waiting for the returned interval.
+	holdWait := func(t *testing.T, finish func(cancel context.CancelFunc, rh *readHandler)) (reg *prometheus.Registry, recorder *httptest.ResponseRecorder, wait time.Duration) {
+		reg = prometheus.NewRegistry()
+		h := NewReadHandler(nil, reg, store, func() config.Config {
+			return config.Config{}
+		}, 1e6, 1, 0)
+		rh := h.(*readHandler)
+		require.NoError(t, rh.remoteReadGate.Start(context.Background()))
+
+		ctx, cancel := context.WithCancel(context.Background())
+		defer cancel()
+
+		wait = 200 * time.Millisecond
+		recorder = httptest.NewRecorder()
+		started := make(chan struct{})
+		done := make(chan struct{})
+		go func() {
+			defer close(done)
+			close(started)
+			h.ServeHTTP(recorder, newRequest(t).WithContext(ctx))
+		}()
+		<-started
+		time.Sleep(wait)
+		finish(cancel, rh)
+		<-done
+		return reg, recorder, wait
+	}
+
+	// The request only starts waiting once the goroutine is scheduled, which can be slightly
+	// after the sleep begins, so allow for half the interval as slack.
+	t.Run("contended acquisition", func(t *testing.T) {
+		reg, recorder, wait := holdWait(t, func(_ context.CancelFunc, rh *readHandler) {
+			rh.remoteReadGate.Done()
+		})
+		require.Equal(t, 2, recorder.Code/100)
+
+		count, sum := gateWaitHistogram(t, reg)
+		require.Equal(t, uint64(1), count)
+		require.GreaterOrEqual(t, sum, (wait / 2).Seconds())
+	})
+
+	t.Run("contended canceled acquisition", func(t *testing.T) {
+		reg, recorder, wait := holdWait(t, func(cancel context.CancelFunc, _ *readHandler) {
+			cancel()
+		})
+		require.Equal(t, http.StatusInternalServerError, recorder.Code)
+
+		count, sum := gateWaitHistogram(t, reg)
+		require.Equal(t, uint64(1), count)
+		require.GreaterOrEqual(t, sum, (wait / 2).Seconds())
+	})
+}

```

# REVIEW A

**Review of PR #18355: `storage/remote: add wait duration histogram for the remote read gate`**

The PR is already merged and has an approval from aknuds1. Overall it is a small, well-scoped change. I have a few suggestions, none of them blocking.

**What it does well**
- It observes the duration around `Gate.Start()` and does so before the error check. Requests canceled while queued are therefore recorded, and the help text and PR body say so.
- It leaves `util/gate` untouched and changes no exported API, which fits the API-stability guidance.
- The PR title uses the `area: description` format. The body includes a `release-notes` block and a closing keyword. The PR body is also unusually clear about how to interpret the metric and where it falls short: uncontended and canceled attempts are counted, and requests still waiting are not.
- The metric name follows the existing `prometheus_remote_read_handler_*` naming.

**Issues and suggestions**

1. **Native-only histogram.** No classic `Buckets` are configured. With the client_golang defaults, `HistogramOpts` without `Buckets` still exposes the default classic buckets, so I would expect the classic series to exist alongside the native one. That contradicts "no classic histogram bucket boundaries are configured" in the PR body. Please check the actual `/metrics` output. If you want native-only, set `Buckets: nil` explicitly in an upstream-recommended way, or document that classic buckets are also exposed. The default buckets run from 5ms to 10s, which is reasonable for gate waits.

2. **Test timing.** The contended tests use `time.Sleep(200ms)`.
   - The assertion is `sum >= wait/2`, which is lenient, so flakiness is unlikely. Even so, it adds about 400ms of wall time.
   - The `started` channel is closed before `ServeHTTP` is called, so it doesn't prove the request has reached the gate. That is why the `wait/2` slack is needed.
   - `testing/synctest` would make this deterministic and instant. It is available in recent Go versions, so check whether the repo's minimum Go version supports it. A smaller alternative is to poll for the gate being contended before sleeping.

3. **Test structure versus AGENTS.md.**
   - The guidance prefers table-driven tests and inlining one-off helpers. The `holdWait` closure, the `gateWaitHistogram` helper and the `gateWaitSampleCount` helper are a lot of scaffolding for four cases. A table with `{limit, preCancel, holdGate, finish}` fields would be tighter.
   - The success and cancel cases could also be folded into one table.
   - `gateWaitHistogram` returns `(0, 0)` after `t.Fatal`, which is unreachable. `prometheus/client_golang/prometheus/testutil` (`CollectAndCount` or `GatherAndCompare`) could replace the hand-rolled gathering.

4. **Test realism.**
   - The "canceled acquisition" case uses a concurrency limit of 0. A limit of 0 is not a valid operating configuration. It works because of how `Gate.Start` selects, but the comment admits it relies on that implementation detail. The "contended canceled" case already covers a realistic cancel, so the limit-0 case adds little.
   - The tests assert on `*readHandler` via a type assertion on `NewReadHandler`'s return value. That is an internal detail, and AGENTS.md prefers exported APIs. It is acceptable here because the test needs to hold the gate.

5. **Existing behavior.** A canceled request returns HTTP 500 (`http.StatusInternalServerError`). This was already the case and is out of scope. A 499 or 503 would be more accurate, but that should go in a separate PR.

6. **Minor.**
   - `NativeHistogramMinResetDuration: 1 * time.Hour` can be written as `time.Hour`.
   - The comment on `gateWaitDuration` in the struct has no doc comment. Unexported fields are fine without one, but a one-liner would help.
   - `docs/` has no metrics listing to update, so nothing is needed there.

**Performance and security**
- Per-request cost is one `time.Now()` pair and one `Observe`, which is negligible next to a remote-read query.
- There are no security concerns. The metric has no labels, so cardinality is fixed.

**Verdict:** the change is good and correct. The main follow-up is to verify the classic-bucket claim (item 1). The rest is optional test tidying (items 2 and 3).

# REVIEW B

# Review of PR #18355: remote-read gate wait duration histogram

The PR is already merged and approved. Overall it is a small, focused change that matches the repo conventions, and I found no blocking issues.

## What's good
- **Placement of the observation.** It sits right after `remoteReadGate.Start()` and before the error check, so canceled waits are recorded too. The comment explains why.
- **Native-histogram configuration.** The bucket factor, max bucket number and min reset duration are all set. This follows the usual Prometheus pattern, and the PR description says no classic buckets are configured.
- **Release notes block.** The block is present, uses the `[ENHANCEMENT]` prefix, and the PR links the issue with `Fixes #11365`.
- **PR description.** It is honest about the metric's limits. Requests still waiting haven't been observed yet, and the count includes uncontended and canceled attempts. It also includes an example query.
- **Tests.** They cover four cases: immediate success, immediate cancel, contended success, and contended cancel. Cancel is made deterministic with a gate limit of 0.

## Issues and suggestions

1. **Timing-based test (minor flakiness risk).**
   - The contended tests use `time.Sleep(200ms)` and assert `sum >= 100ms`. The slack makes this reasonably safe.
   - On a heavily loaded CI runner, though, the goroutine might not reach `Start()` before `finish` runs. In that case the wait would be near zero and the assertion would fail.
   - `started` is closed before `ServeHTTP` is entered, so it doesn't prove the request is blocked in the gate.
   - A more robust approach would be to poll until the request is verifiably queued. For example, check `h.queries` via `testutil.ToFloat64`, assuming it is incremented before `Start`. Another option is to use `synctest`.
   - The last commit on the current branch, "test gate wait duration under contention", is where this lives.

2. **Test structure vs. AGENTS.md.**
   - The guidance prefers table-driven tests and says to inline subtests. This test uses a mix of subtests plus the `holdWait` helper closure.
   - The helper is reused by two cases, so it is justified.
   - The first two subtests (immediate success and cancel) differ only by gate size and context. They could be folded into a small table.

3. **`gateWaitHistogram` helper.**
   - It reads `GetMetric()[0]` without checking the length.
   - It also leaves a dead `return 0, 0` after `t.Fatal`. This is harmless, but `require.Len` would be tidier.
   - `gateWaitSampleCount` is a thin wrapper used in only two places.

4. **Test assertions are weak on upper bounds.**
   - Nothing checks that the uncontended case has a small sum.
   - Nothing checks that the wait excludes query processing time. The description explicitly claims that, but no test covers it.
   - Both are optional.

5. **Metric naming and namespace.**
   - The handler uses `namespace` and subsystem `remote_read_handler`, which is consistent with the existing `queries` gauge.
   - The metric is registered only when `r != nil`, which is fine.
   - Native-only histograms are only exposed with native histogram scraping enabled. The PR notes this, but it may be worth a line in the docs or the CHANGELOG.

6. **Error code.**
   - A context-canceled wait returns HTTP 500. This is pre-existing and out of scope.
   - It does mean canceled client requests show up as server errors, which could be worth a follow-up issue.

7. **Performance.** `time.Now()` plus `Observe` per request is negligible next to a remote-read query. No benchmark is needed, and the PR is not labeled PERF.

## Security
There are no concerns. The metric has no labels, so there is no cardinality risk, and no user input is involved.

## Verdict
LGTM. The main follow-up I'd suggest is making the contended tests deterministic, for example by waiting until the request is queued instead of relying on a fixed sleep.
