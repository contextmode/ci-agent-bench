# PR diff (the real change)

```diff
diff --git a/pkg/storage/unified/resource/errors.go b/pkg/storage/unified/resource/errors.go
index 945e5c5409a71..895b522e357c8 100644
--- a/pkg/storage/unified/resource/errors.go
+++ b/pkg/storage/unified/resource/errors.go
@@ -21,6 +21,7 @@ import (
 // Package-level errors.
 var (
 	ErrNotImplementedYet = errors.New("not implemented yet")
+	errQueueTimeout      = errors.New("request timed out in QOS queue")
 
 	ErrResourceAlreadyExists error = &apierrors.StatusError{
 		ErrStatus: metav1.Status{
diff --git a/pkg/storage/unified/resource/errors_test.go b/pkg/storage/unified/resource/errors_test.go
index faf702d4e0b33..b8d47a03d26d8 100644
--- a/pkg/storage/unified/resource/errors_test.go
+++ b/pkg/storage/unified/resource/errors_test.go
@@ -82,6 +82,99 @@ func TestAsErrorResult_NamespaceMismatchIsForbidden(t *testing.T) {
 	}
 }
 
+func TestAsErrorResult_ContextErrors(t *testing.T) {
+	t.Parallel()
+
+	for _, tc := range []struct {
+		name     string
+		err      error
+		httpCode int32
+		grpcCode codes.Code
+	}{
+		{"canceled", context.Canceled, 499, codes.Canceled},
+		{"deadline exceeded", context.DeadlineExceeded, http.StatusGatewayTimeout, codes.DeadlineExceeded},
+		{"grpc canceled", status.Error(codes.Canceled, "canceled read"), 499, codes.Canceled},
+		{"grpc deadline exceeded", status.Error(codes.DeadlineExceeded, "expired read"), http.StatusGatewayTimeout, codes.DeadlineExceeded},
+		{"backend failure", errors.New("storage failed"), http.StatusInternalServerError, codes.Internal},
+	} {
+		t.Run(tc.name, func(t *testing.T) {
+			t.Parallel()
+			for name, err := range map[string]error{
+				"bare":        tc.err,
+				"wrapped":     fmt.Errorf("reading resource: %w", tc.err),
+				"joined":      errors.Join(tc.err),
+				"both joined": errors.Join(tc.err, fmt.Errorf("reading body: %w", tc.err)),
+				"nested join": fmt.Errorf("reading resource: %w", errors.Join(errors.Join(tc.err))),
+			} {
+				t.Run(name, func(t *testing.T) {
+					got := AsErrorResult(err)
+					require.Equal(t, tc.httpCode, got.Code)
+					require.Equal(t, err.Error(), got.Message)
+					require.Equal(t, tc.grpcCode, status.Code(errorResultStatus(got)))
+				})
+			}
+		})
+	}
+}
+
+func TestAsErrorResult_MixedJoinedErrors(t *testing.T) {
+	t.Parallel()
+
+	backendErr := errors.New("storage failed")
+	withDetails := func(code codes.Code, httpCode int32) error {
+		st, err := status.New(code, "canceled read with details").WithDetails(&resourcepb.ErrorResult{Code: httpCode})
+		require.NoError(t, err)
+		return st.Err()
+	}
+	for _, cancellation := range []error{
+		context.Canceled,
+		context.DeadlineExceeded,
+		status.Error(codes.Canceled, "canceled read"),
+		status.Error(codes.DeadlineExceeded, "expired read"),
+		withDetails(codes.Canceled, 499),
+		withDetails(codes.DeadlineExceeded, http.StatusGatewayTimeout),
+	} {
+		t.Run(cancellation.Error(), func(t *testing.T) {
+			t.Parallel()
+			for name, err := range map[string]error{
+				"failure first":      errors.Join(backendErr, cancellation),
+				"cancellation first": errors.Join(cancellation, backendErr),
+				"nested join":        fmt.Errorf("reading resource: %w", errors.Join(cancellation, errors.Join(backendErr, cancellation))),
+			} {
+				t.Run(name, func(t *testing.T) {
+					got := AsErrorResult(err)
+					require.Equal(t, int32(http.StatusInternalServerError), got.Code)
+					require.Equal(t, err.Error(), got.Message)
+					require.Equal(t, codes.Internal, status.Code(errorResultStatus(got)))
+					require.Equal(t, int32(http.StatusInternalServerError), AsErrorResult(StatusErrorFromResponse(nil, err)).Code)
+				})
+			}
+		})
+	}
+}
+
+func TestHandleQueueError_ContextErrors(t *testing.T) {
+	t.Parallel()
+
+	for _, tc := range []struct {
+		err  error
+		want codes.Code
+	}{
+		{context.Canceled, codes.Canceled},
+		{context.DeadlineExceeded, codes.DeadlineExceeded},
+	} {
+		t.Run(tc.want.String(), func(t *testing.T) {
+			t.Parallel()
+			queueErr := fmt.Errorf("failed to enqueue for tenant stacks-13: %w", tc.err)
+			response, err := HandleQueueError(queueErr, func(e *resourcepb.ErrorResult) *resourcepb.ReadResponse {
+				return &resourcepb.ReadResponse{Error: e}
+			})
+			require.NoError(t, err)
+			require.Equal(t, tc.want, status.Code(errorResultStatus(response.Error)))
+		})
+	}
+}
+
 func TestErrorFromResponse(t *testing.T) {
 	t.Parallel()
 
diff --git a/pkg/storage/unified/resource/server.go b/pkg/storage/unified/resource/server.go
index 2bde3eeeff86b..21ed6957695de 100644
--- a/pkg/storage/unified/resource/server.go
+++ b/pkg/storage/unified/resource/server.go
@@ -3072,7 +3072,7 @@ func (s *server) getBlobReferences(ctx context.Context, key *resourcepb.Resource
 
 func (s *server) runInQueue(ctx context.Context, tenantID, operation string, runnable func(ctx context.Context)) error {
 	// Enforce a timeout for the entire operation, including queueing and execution.
-	queueCtx, cancel := context.WithTimeout(ctx, s.queueConfig.Timeout)
+	queueCtx, cancel := context.WithTimeoutCause(ctx, s.queueConfig.Timeout, errQueueTimeout)
 	defer cancel()
 
 	// Allow cluster-scoped resources to be enqueued with an empty tenantID.
@@ -3121,6 +3121,11 @@ func (s *server) runInQueue(ctx context.Context, tenantID, operation string, run
 		s.log.Warn("failed to enqueue runnable, retrying", "tenantID", tenantID, "error", err)
 		if !boff.Ongoing() {
 			// Backoff finished (retries exhausted or context canceled).
+			if errors.Is(context.Cause(queueCtx), errQueueTimeout) {
+				err = errQueueTimeout
+			} else if queueCtx.Err() != nil {
+				err = queueCtx.Err()
+			}
 			err = fmt.Errorf("failed to enqueue for tenant %s: %w", tenantID, err)
 			finishWait(err)
 			return err
@@ -3128,15 +3133,17 @@ func (s *server) runInQueue(ctx context.Context, tenantID, operation string, run
 		boff.Wait()
 	}
 
-	// Wait for the runnable to complete or for the context to be done.
+	// Inline work can finish after the timeout, so check the cause after either case.
 	select {
 	case <-done:
-		return nil // Completed successfully.
 	case <-queueCtx.Done():
-		err := queueCtx.Err()
-		finishWait(err)
-		return err
 	}
+	err := queueCtx.Err()
+	if errors.Is(context.Cause(queueCtx), errQueueTimeout) {
+		err = fmt.Errorf("tenant %s: %w", tenantID, errQueueTimeout)
+	}
+	finishWait(err)
+	return err
 }
 
 // RebuildIndexes implements ResourceIndexServer.
diff --git a/pkg/storage/unified/resource/server_test.go b/pkg/storage/unified/resource/server_test.go
index f2ced0409f980..17d1d7a796edf 100644
--- a/pkg/storage/unified/resource/server_test.go
+++ b/pkg/storage/unified/resource/server_test.go
@@ -671,17 +671,20 @@ func TestRunInQueue(t *testing.T) {
 	})
 
 	t.Run("should time out if a task is sitting in the queue beyond the timeout", func(t *testing.T) {
-		s, _ := newTestServerWithQueue(t, 1, 1)
-		executed := make(chan struct{}, 1)
-		runnable := func(ctx context.Context) {
-			time.Sleep(1 * time.Second)
-			executed <- struct{}{}
-		}
+		synctest.Test(t, func(t *testing.T) {
+			s, _ := newTestServerWithQueue(t, 1, 1)
+			executed := make(chan struct{})
+			runnable := func(ctx context.Context) {
+				<-ctx.Done()
+				close(executed)
+			}
 
-		err := s.runInQueue(context.Background(), testTenantID, "read", runnable)
-		require.Error(t, err)
-		assert.Equal(t, context.DeadlineExceeded, err)
-		<-executed
+			err := s.runInQueue(t.Context(), testTenantID, "read", runnable)
+			require.ErrorIs(t, err, errQueueTimeout)
+			require.NotErrorIs(t, err, context.DeadlineExceeded)
+			require.NoError(t, t.Context().Err())
+			<-executed
+		})
 	})
 
 	t.Run("should use cluster-scoped tenant for empty tenantID", func(t *testing.T) {
@@ -5100,6 +5103,106 @@ func TestResourceServerQOSTenantIsolation(t *testing.T) {
 	})
 }
 
+func TestResourceServerQOSTimeoutStatus(t *testing.T) {
+	for _, mode := range []string{"enqueue", "queued", "executing", "inline"} {
+		t.Run(mode, func(t *testing.T) {
+			for _, tc := range []struct {
+				name     string
+				httpCode int32
+				grpcCode codes.Code
+			}{
+				{"server timeout", http.StatusInternalServerError, codes.Internal},
+				{"caller deadline", http.StatusGatewayTimeout, codes.DeadlineExceeded},
+				{"caller cancellation", 499, codes.Canceled},
+			} {
+				t.Run(tc.name, func(t *testing.T) {
+					synctest.Test(t, func(t *testing.T) {
+						access := &callbackAccessClient{}
+						srv := &server{
+							backend:     &internalReadBackend{},
+							access:      access,
+							log:         log.NewNopLogger(),
+							queueConfig: QueueConfig{Timeout: time.Second, MinBackoff: time.Second, MaxBackoff: time.Second, MaxRetries: 10},
+						}
+						ctx := authlib.WithAuthInfo(t.Context(), newWatchTestUser())
+						key := &resourcepb.ResourceKey{Group: watchTestGroup, Resource: watchTestResource, Namespace: watchTestNamespace, Name: "timeout-test"}
+						if mode == "inline" {
+							srv.queue = scheduler.NewNoopQueue()
+						} else {
+							q := scheduler.NewQueue(&scheduler.QueueOptions{MaxSizePerTenant: 1})
+							startQOSTestService(t, q)
+							srv.queue = q
+							if mode == "enqueue" {
+								require.NoError(t, q.Enqueue(t.Context(), watchTestNamespace, func() { t.Error("queued work ran") }))
+							}
+							if mode == "executing" {
+								worker, err := scheduler.NewScheduler(q, &scheduler.Config{NumWorkers: 1})
+								require.NoError(t, err)
+								startQOSTestService(t, worker)
+							}
+						}
+
+						release := make(chan struct{})
+						unblock := sync.OnceFunc(func() { close(release) })
+						t.Cleanup(unblock)
+						started := make(chan struct{}, 1)
+						access.fn = func(authlib.CheckRequest, string) (authlib.CheckResponse, error) {
+							started <- struct{}{}
+							<-release
+							return authlib.CheckResponse{Allowed: true}, nil
+						}
+						callerCtx, cancel := context.WithCancel(ctx)
+						defer cancel()
+						if tc.name == "caller deadline" {
+							var deadlineCancel context.CancelFunc
+							callerCtx, deadlineCancel = context.WithTimeout(callerCtx, 100*time.Millisecond)
+							defer deadlineCancel()
+						}
+						type result struct {
+							rsp *resourcepb.ReadResponse
+							err error
+						}
+						results := make(chan result, 1)
+						go func() {
+							rsp, err := srv.Read(callerCtx, &resourcepb.ReadRequest{Key: key})
+							results <- result{rsp, err}
+						}()
+						synctest.Wait()
+						if mode == "executing" || mode == "inline" {
+							require.Len(t, started, 1)
+						} else {
+							require.Empty(t, started)
+						}
+						if tc.name == "caller cancellation" {
+							cancel()
+						}
+
+						// Keep execution blocked until the server budget has expired too.
+						time.Sleep(2 * time.Second)
+						if tc.name == "server timeout" {
+							require.NoError(t, callerCtx.Err())
+							_, hasDeadline := callerCtx.Deadline()
+							require.False(t, hasDeadline)
+						}
+						unblock()
+						r := awaitQOSTestResult(t, results)
+						require.NoError(t, r.err)
+						require.NotNil(t, r.rsp)
+						require.NotNil(t, r.rsp.Error)
+						require.Equal(t, tc.httpCode, r.rsp.Error.Code)
+						_, err := UnaryErrorResultInterceptor()(callerCtx, nil, nil, func(context.Context, any) (any, error) {
+							return r.rsp, nil
+						})
+						require.Equal(t, tc.grpcCode, status.Code(err))
+						require.True(t, proto.Equal(r.rsp.Error, AsErrorResult(err)))
+						synctest.Wait()
+					})
+				})
+			}
+		})
+	}
+}
+
 func TestResourceServerQOSQueueWaitSpan(t *testing.T) {
 	t.Run("ends before execution", func(t *testing.T) {
 		recorder := newQOSTestSpanRecorder(t)
diff --git a/pkg/storage/unified/resource/storage_backend.go b/pkg/storage/unified/resource/storage_backend.go
index cd2bd82e54144..67f9395f3576c 100644
--- a/pkg/storage/unified/resource/storage_backend.go
+++ b/pkg/storage/unified/resource/storage_backend.go
@@ -25,8 +25,6 @@ import (
 	"go.opentelemetry.io/otel/attribute"
 	otelcodes "go.opentelemetry.io/otel/codes"
 	"go.opentelemetry.io/otel/trace"
-	"google.golang.org/grpc/codes"
-	"google.golang.org/grpc/status"
 	apierrors "k8s.io/apimachinery/pkg/api/errors"
 	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
 	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
@@ -38,6 +36,7 @@ import (
 	"github.com/grafana/grafana/pkg/setting"
 	"github.com/grafana/grafana/pkg/storage/unified/resource/kv"
 	"github.com/grafana/grafana/pkg/storage/unified/resource/lease"
+	"github.com/grafana/grafana/pkg/storage/unified/resourceclient/resourceutil"
 	"github.com/grafana/grafana/pkg/storage/unified/resourcepb"
 	"github.com/grafana/grafana/pkg/storage/unified/sql/db"
 	"github.com/grafana/grafana/pkg/storage/unified/sql/db/dbimpl"
@@ -811,7 +810,7 @@ func (b *kvStorageBackend) collectBlobs(ctx context.Context) {
 	}
 	dryRun := b.garbageCollection.DryRun || b.garbageCollection.BlobDryRun
 	count, err := b.blobGC.Collect(ctx, time.Now(), b.garbageCollection.MaxAge, dryRun, b.blobReferenced)
-	if err != nil && ctx.Err() != nil && onlyCancellationErrors(err) {
+	if err != nil && ctx.Err() != nil && resourceutil.OnlyCancellationErrors(err) {
 		b.blobGCMetrics.RecordInterrupted(count, dryRun)
 		b.log.Debug("blob garbage collection interrupted", "error", err)
 		return
@@ -830,33 +829,6 @@ func (b *kvStorageBackend) collectBlobs(ctx context.Context) {
 	b.log.Info("blob garbage collection finished", logArgs...)
 }
 
-// onlyCancellationErrors checks every branch of a joined error so a storage
-// failure collected before cancellation is still reported.
-func onlyCancellationErrors(err error) bool {
-	if err == nil {
-		return false
-	}
-	if joined, ok := err.(interface{ Unwrap() []error }); ok {
-		children := joined.Unwrap()
-		if len(children) == 0 {
-			return false
-		}
-		for _, child := range children {
-			if !onlyCancellationErrors(child) {
-				return false
-			}
-		}
-		return true
-	}
-	if wrapped, ok := err.(interface{ Unwrap() error }); ok && wrapped.Unwrap() != nil {
-		return onlyCancellationErrors(wrapped.Unwrap())
-	}
-	if errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded) {
-		return true
-	}
-	return status.Code(err) == codes.Canceled || status.Code(err) == codes.DeadlineExceeded
-}
-
 // runGarbageCollection identifies deleted resources that are safe
 // to be fully removed from the datastore and deletes them in batches.
 func (b *kvStorageBackend) runGarbageCollection(ctx context.Context, cutoffTimeStamp int64) {
@@ -1476,10 +1448,7 @@ func (k *kvStorageBackend) ReadResource(ctx context.Context, req *resourcepb.Rea
 		latestRV, latestErr := k.latestResourceVersion(ctx)
 		err = latestErr
 		if err != nil {
-			return &BackendReadResponse{Error: &resourcepb.ErrorResult{
-				Code:    http.StatusInternalServerError,
-				Message: fmt.Sprintf("failed to fetch latest resource version: %v", err),
-			}}
+			return &BackendReadResponse{Error: AsErrorResult(fmt.Errorf("failed to fetch latest resource version: %w", err))}
 		}
 
 		// Check if the requested RV is higher than the latest available RV
@@ -1512,7 +1481,7 @@ func (k *kvStorageBackend) ReadResource(ctx context.Context, req *resourcepb.Rea
 	if errors.Is(err, ErrNotFound) {
 		return &BackendReadResponse{Error: NewNotFoundError(req.Key)}
 	} else if err != nil {
-		return &BackendReadResponse{Error: &resourcepb.ErrorResult{Code: http.StatusInternalServerError, Message: err.Error()}}
+		return &BackendReadResponse{Error: AsErrorResult(err)}
 	}
 	data, err := k.dataStore.Get(ctx, DataKey{
 		Group:           req.Key.Group,
@@ -1529,11 +1498,11 @@ func (k *kvStorageBackend) ReadResource(ctx context.Context, req *resourcepb.Rea
 		return &BackendReadResponse{Error: NewNotFoundError(req.Key)}
 	}
 	if err != nil {
-		return &BackendReadResponse{Error: &resourcepb.ErrorResult{Code: http.StatusInternalServerError, Message: err.Error()}}
+		return &BackendReadResponse{Error: AsErrorResult(err)}
 	}
 	value, err := kv.ReadAllAndClose(data)
 	if err != nil {
-		return &BackendReadResponse{Error: &resourcepb.ErrorResult{Code: http.StatusInternalServerError, Message: err.Error()}}
+		return &BackendReadResponse{Error: AsErrorResult(err)}
 	}
 	return &BackendReadResponse{
 		Key:             req.Key,
diff --git a/pkg/storage/unified/resource/storage_backend_test.go b/pkg/storage/unified/resource/storage_backend_test.go
index c267c9c7a33cb..0aedd94e5dbf3 100644
--- a/pkg/storage/unified/resource/storage_backend_test.go
+++ b/pkg/storage/unified/resource/storage_backend_test.go
@@ -20,6 +20,8 @@ import (
 
 	"github.com/stretchr/testify/assert"
 	"github.com/stretchr/testify/require"
+	"google.golang.org/grpc/codes"
+	"google.golang.org/grpc/status"
 	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
 
 	"github.com/grafana/grafana-app-sdk/logging"
@@ -916,10 +918,13 @@ func (k *unreadableValueKV) BatchGet(ctx context.Context, section string, keys [
 	}
 }
 
-type failingReadCloser struct{ err error }
+type failingReadCloser struct {
+	err      error
+	closeErr error
+}
 
 func (f failingReadCloser) Read([]byte) (int, error) { return 0, f.err }
-func (f failingReadCloser) Close() error             { return nil }
+func (f failingReadCloser) Close() error             { return f.closeErr }
 
 // TestKvStorageBackend_WatchWriteEvents_ReadFailuresAreNotReportedAsMissing
 // guards the error paths of resolving a batch. A failed batch read returns no
@@ -1228,6 +1233,110 @@ func TestKvStorageBackend_ReadResource_Success(t *testing.T) {
 	require.Equal(t, objectToJSONBytes(t, testObj), response.Value)
 }
 
+func TestKvStorageBackend_ReadResource_ErrorStatus(t *testing.T) {
+	for _, stage := range []string{"latest resource version", "resolve key", "get body", "read body"} {
+		t.Run(stage, func(t *testing.T) {
+			for _, tc := range []struct {
+				name string
+				err  error
+				want codes.Code
+			}{
+				{"canceled", context.Canceled, codes.Canceled},
+				{"deadline exceeded", context.DeadlineExceeded, codes.DeadlineExceeded},
+				{"grpc canceled", status.Error(codes.Canceled, "canceled read"), codes.Canceled},
+				{"grpc deadline exceeded", status.Error(codes.DeadlineExceeded, "expired read"), codes.DeadlineExceeded},
+				{"backend failure", errors.New("storage failed"), codes.Internal},
+			} {
+				t.Run(tc.name, func(t *testing.T) {
+					store := &readErrorKV{stage: stage, err: tc.err}
+					backend := setupTestStorageBackend(t, func(opts *KVBackendOptions) {
+						store.KV = opts.KvStore
+						opts.KvStore = store
+					})
+					_, rv := createAndWriteTestObject(t, backend)
+					store.fail.Store(true)
+
+					req := &resourcepb.ReadRequest{Key: storageTestKey("test-resource")}
+					if stage == "latest resource version" {
+						req.ResourceVersion = rv
+					}
+					response := backend.ReadResource(t.Context(), req)
+					require.NotNil(t, response.Error)
+					require.Contains(t, response.Error.Message, tc.err.Error())
+					require.Equal(t, tc.want, grpcCodeFromErrorResult(response.Error))
+					_, err := UnaryErrorResultInterceptor()(t.Context(), req, nil, func(context.Context, any) (any, error) {
+						return &resourcepb.ReadResponse{Error: response.Error}, nil
+					})
+					require.Equal(t, tc.want, status.Code(err))
+				})
+			}
+		})
+	}
+}
+
+func TestKvStorageBackend_ReadResource_JoinedReadCloseErrors(t *testing.T) {
+	backendErr := errors.New("storage failed")
+	for _, tc := range []struct {
+		name     string
+		readErr  error
+		closeErr error
+		want     codes.Code
+	}{
+		{"canceled read and failed close", context.Canceled, backendErr, codes.Internal},
+		{"failed read and canceled close", backendErr, context.Canceled, codes.Internal},
+		{"expired read and failed close", context.DeadlineExceeded, backendErr, codes.Internal},
+		{"failed read and expired close", backendErr, context.DeadlineExceeded, codes.Internal},
+		{"grpc canceled read and failed close", status.Error(codes.Canceled, "canceled read"), backendErr, codes.Internal},
+		{"failed read and grpc canceled close", backendErr, status.Error(codes.Canceled, "canceled close"), codes.Internal},
+		{"both canceled", context.Canceled, context.Canceled, codes.Canceled},
+		{"both expired", context.DeadlineExceeded, context.DeadlineExceeded, codes.DeadlineExceeded},
+		{"only close canceled", io.EOF, context.Canceled, codes.Canceled},
+	} {
+		t.Run(tc.name, func(t *testing.T) {
+			store := &readErrorKV{stage: "read body", err: tc.readErr, closeErr: tc.closeErr}
+			backend := setupTestStorageBackend(t, func(opts *KVBackendOptions) {
+				store.KV = opts.KvStore
+				opts.KvStore = store
+			})
+			createAndWriteTestObject(t, backend)
+			store.fail.Store(true)
+
+			response := backend.ReadResource(t.Context(), &resourcepb.ReadRequest{Key: storageTestKey("test-resource")})
+			require.NotNil(t, response.Error)
+			require.Contains(t, response.Error.Message, tc.closeErr.Error())
+			require.Equal(t, tc.want, grpcCodeFromErrorResult(response.Error))
+			require.Equal(t, tc.want, status.Code(errorResultStatus(response.Error)))
+		})
+	}
+}
+
+type readErrorKV struct {
+	KV
+	stage    string
+	err      error
+	closeErr error
+	fail     atomic.Bool
+}
+
+func (k *readErrorKV) Keys(ctx context.Context, section string, opts ListOptions) iter.Seq2[string, error] {
+	if k.fail.Load() && (k.stage == "resolve key" && section == kv.DataSection || k.stage == "latest resource version" && section == kv.EventsSection) {
+		return func(yield func(string, error) bool) { yield("", k.err) }
+	}
+	return k.KV.Keys(ctx, section, opts)
+}
+
+func (k *readErrorKV) Get(ctx context.Context, section, key string) (io.ReadCloser, error) {
+	if k.fail.Load() && section == kv.DataSection {
+		switch k.stage {
+		case "get body":
+			return nil, k.err
+		case "read body":
+			return failingReadCloser{err: k.err, closeErr: k.closeErr}, nil
+		}
+	}
+	return k.KV.Get(ctx, section, key)
+}
+
 func TestKvStorageBackend_ReadResource_SpecificVersion(t *testing.T) {
 	backend := setupTestStorageBackend(t)
 	ctx := context.Background()
diff --git a/pkg/storage/unified/resourceclient/resourceutil/errors.go b/pkg/storage/unified/resourceclient/resourceutil/errors.go
index 2e23d21ace436..27718871ca7fe 100644
--- a/pkg/storage/unified/resourceclient/resourceutil/errors.go
+++ b/pkg/storage/unified/resourceclient/resourceutil/errors.go
@@ -106,6 +106,15 @@ func AsErrorResult(err error) *resourcepb.ErrorResult {
 		}
 	}
 
+	st, ok := grpcstatus.FromError(err)
+	if !ok {
+		st = grpcstatus.FromContextError(err)
+	}
+	code := st.Code()
+	if (code == grpccodes.Canceled || code == grpccodes.DeadlineExceeded) && !OnlyCancellationErrors(err) {
+		return &resourcepb.ErrorResult{Code: http.StatusInternalServerError, Message: err.Error()}
+	}
+
 	// Structured results attached to a gRPC error keep their reason/code across
 	// the wire, so prefer them over the generic mapping below.
 	if res := ErrorResultFromGRPCDetails(err); res != nil {
@@ -139,17 +148,37 @@ func AsErrorResult(err error) *resourcepb.ErrorResult {
 		return res
 	}
 
-	code := 500
-
-	st, ok := grpcstatus.FromError(err)
-	if ok {
-		code = runtime.HTTPStatusFromCode(st.Code())
-	}
-
 	return &resourcepb.ErrorResult{
 		Message: err.Error(),
-		Code:    int32(code),
+		Code:    int32(runtime.HTTPStatusFromCode(code)),
+	}
+}
+
+// OnlyCancellationErrors checks every branch of a joined error so a storage
+// failure collected before cancellation is still reported.
+func OnlyCancellationErrors(err error) bool {
+	if err == nil {
+		return false
+	}
+	if joined, ok := err.(interface{ Unwrap() []error }); ok {
+		children := joined.Unwrap()
+		if len(children) == 0 {
+			return false
+		}
+		for _, child := range children {
+			if !OnlyCancellationErrors(child) {
+				return false
+			}
+		}
+		return true
+	}
+	if wrapped, ok := err.(interface{ Unwrap() error }); ok && wrapped.Unwrap() != nil {
+		return OnlyCancellationErrors(wrapped.Unwrap())
+	}
+	if errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded) {
+		return true
 	}
+	return grpcstatus.Code(err) == grpccodes.Canceled || grpcstatus.Code(err) == grpccodes.DeadlineExceeded
 }
 
 // StatusError converts an ErrorResult into a Kubernetes StatusError, preserving the HTTP code, reason, details and
@@ -202,7 +231,7 @@ func StatusErrorFromResponse(respErr *resourcepb.ErrorResult, err error) error {
 		return StatusError(respErr)
 	}
 	// In-process calls can return context errors instead of gRPC statuses.
-	localContextErr := errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded)
+	localContextErr := (errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded)) && OnlyCancellationErrors(err)
 	if localContextErr {
 		err = grpcstatus.FromContextError(err).Err()
 	}

```

# REVIEW A

# Review of PR 136242: preserve cancellation status in unified storage reads

The PR is already merged, so this is post-merge feedback. I read the diff only and did not run the tests.

## Summary
Context cancellations and deadline errors in `ReadResource` and `runInQueue` used to surface as `Internal` (500). They now map to `Canceled` (499) and `DeadlineExceeded` (504). A mixed joined error, such as a storage failure plus a cancellation, still reports `Internal`. The queue's own timeout is tagged with `errQueueTimeout`, so it is no longer confused with a caller deadline. I think the approach is sound, and the regression coverage is thorough.

## What works well
- `context.WithTimeoutCause` with `errQueueTimeout` separates a server QoS timeout from a caller deadline. That separation is what lets the server timeout stay `Internal` while a caller deadline becomes 504.
- `OnlyCancellationErrors` checks every branch of a joined error. A real backend failure joined with a cancellation therefore isn't hidden.
- Moving the helper into `resourceutil` removes the duplicate that lived in `storage_backend.go`.
- `ReadResource` now builds its errors with `AsErrorResult`, and `%w` replaces `%v` when wrapping the latest-resource-version error. This keeps the error chain intact, which the classification depends on.
- The tests cover each read stage, bare, wrapped and joined errors, and all four queue modes. They use `synctest`, as `AGENTS.md` asks.

## Potential issues

1. **`runInQueue` can report a completed job as failed** (`server.go`, around line 3136). The new code waits on `done` or `queueCtx.Done()`, then always reads `queueCtx.Err()` and returns it. Before, the `<-done` branch returned `nil` unconditionally.
   - If `done` is selected while the context has also just expired or been cancelled, the runnable has finished but the caller still gets an error.
   - The comment says inline work can finish after the timeout, so some of this is intentional. The caller-cancellation-after-success case deserves an explicit decision, though. If the result is already complete, returning `nil` may be better, or at least a test should lock in the intended behaviour.

2. **`finishWait(err)` is now called on the success path.** Before, it ran only on the timeout and enqueue-failure paths. Please confirm it is idempotent and doesn't double-end the queue-wait span when `done` fires. `TestResourceServerQOSQueueWaitSpan` may cover this, but the diff doesn't show it.

3. **The server timeout maps to 500.** A QoS queue timeout is a transient overload signal, and 503 or 504 would be more accurate and retry-friendly. Clients and alerts that treat 500 as a server bug will also count it. This looks like a deliberate choice, since the tests assert `Internal`. A short comment on why would help.

4. **`AsErrorResult` now checks cancellation before `ErrorResultFromGRPCDetails`.** The mixed-error tests cover details-bearing cancellation errors. A gRPC error with a `Canceled` status but a more specific detail reason, such as a structured not-found, now takes the generic mapping if it is only cancellation errors. That seems fine but is a subtle precedence change.

5. **Error-message detail.** In the enqueue retry path, `err` is replaced with the context error. The last enqueue failure, such as queue full, is dropped from the message and survives only in the earlier warn log. Consider joining or wrapping it for debuggability.

## Test quality
- `TestResourceServerQOSTimeoutStatus` is hard to follow. It has nested loops over mode and case, branching on `tc.name ==` string comparisons, and a lot of inline setup. Replacing those string checks with typed fields, such as a `callerDeadline bool` or a setup func per case, would make it clearer. Extracting a helper for the server setup would also help.
- The `time.Sleep(2 * time.Second)` is fine under `synctest`.
- Consider a direct test for item 1, covering completion and cancellation racing.

## Security and performance
I see no security concerns. The change adds no new allocations on hot paths beyond error classification, and the recursive walk in `OnlyCancellationErrors` only runs on error paths.

## Style
The code follows the repo conventions, and the comments explain why rather than what.

# REVIEW B

# Review of PR 136242: Unified storage: preserve cancellation status in reads

The PR is already merged. This review is based on the diff alone. I didn't check out the code or run the tests.

## Summary
The PR stops cancellations and deadline expirations in the read path from being reported as `Internal`. It does this in three ways:
- **Error mapping.** `AsErrorResult` now maps `context.Canceled`, `context.DeadlineExceeded` and their gRPC-status equivalents to 499 and 504 (`codes.Canceled` and `codes.DeadlineExceeded` on the wire).
- **Joined errors.** When a cancellation is joined with a real backend failure, the result is still `Internal`.
- **Queue timeout.** `runInQueue` now uses `WithTimeoutCause(errQueueTimeout)`. The server's own QoS timeout is reported as a server error. Caller deadlines and cancellations stay as client-side codes.

`kvStorageBackend.ReadResource` now goes through `AsErrorResult` instead of hand-building 500s. The design is sound, and the distinction between server timeout and caller deadline is the right one to make.

## Strengths
- Treating a joined error as a cancellation only if every branch is a cancellation (`OnlyCancellationErrors`) prevents a storage failure from being hidden behind a cancel.
- `OnlyCancellationErrors` moved into `resourceutil` rather than being duplicated. `StatusErrorFromResponse` now uses it too, so the in-process and gRPC paths agree.
- Test coverage is thorough:
  - every read stage;
  - bare, wrapped, joined and nested-joined errors;
  - the four queue states (enqueue, queued, executing, inline);
  - the three timeout sources;
  - `synctest`, as the repo guidelines ask, and the old `time.Sleep(1s)` test is gone.

## Issues and suggestions

1. **`runInQueue` now returns an error even when the work completed.** The old code returned `nil` on `<-done`. The new code falls through to `queueCtx.Err()` after either branch, with `finishWait(err)` called in both.
   - The comment gives the intent: inline work can finish after the timeout. But if the caller cancels just after `done` closes, or the timeout fires at the same instant, a successful run is reported as failed.
   - Callers that treat a non-nil error as "did not run" may mishandle this.
   - Please confirm that no `runInQueue` caller has side effects (writes) that are unsafe to report as failed. A small change would be to return `nil` if `done` is already closed, and only otherwise inspect the context. It would also remove the ambiguity.

2. **`finishWait` is now called on the `done` path.** Previously it wasn't. Check that it is idempotent, or that the span wasn't already ended by the runnable. Otherwise the QoS wait span could be ended twice or end late. The "QueueWaitSpan ends before execution" test covers only part of this.

3. **The enqueue-exhausted path discards the underlying enqueue error.** Any `queueCtx.Err() != nil` overwrites `err`. A "queue full" error that coincides with a cancellation therefore loses its detail. That is probably acceptable, but the original error is still worth logging. The existing `Warn` runs before the overwrite, so it is already logged.

4. **`errQueueTimeout` maps to HTTP 500 and `codes.Internal`.** That is intentional per the tests. `Unavailable` or `ResourceExhausted` would let clients retry and would keep it out of 5xx internal-error alerts. If dashboards or alerts key on `Internal`, this PR now makes server-side queue saturation look like a generic internal error. It is worth confirming that was intended.

5. **`OnlyCancellationErrors` follows `Unwrap() error` before checking the error's own gRPC status.** A type that implements both `GRPCStatus()` and `Unwrap()` is judged by its inner error. This is an edge case, and `grpcstatus.FromError` already prefers the outer status, so the two checks can disagree. Consider checking the node's own status first.

6. **`AsErrorResult` calls `FromError` and then `FromContextError`.** For a non-status, non-context error, `FromContextError` returns `Unknown`, so the later logic is unaffected. A short comment on that fallthrough would help. Per `AGENTS.md`, a comment should only explain why, and this is one of those cases.

7. **Test readability.** The nested table-driven tests use map iteration over anonymous maps, and `TestResourceServerQOSTimeoutStatus` is about 100 lines of nested closures. A helper for building the server and the blocking access client would make it easier to maintain. The `tc.name == "..."` string comparisons inside the test body are brittle. Use a typed enum or boolean fields instead.

8. **Minor.** The `499` literal is repeated across the code and tests. A named constant, if one exists, would be clearer. The `Message` in the cancellation case is `err.Error()`, which for wrapped or joined errors can expose internal wrapping text to clients. That was already true for 500s, so it is not a regression.

## Security
No concerns. There are no new inputs, and the error messages carry no more detail than before.

## Verdict
This is a well-reasoned change with strong tests. Items 1, 2 and 4 are the ones to confirm. They concern the `runInQueue` return semantics, span handling and the chosen code for queue timeouts. The rest are polish.
