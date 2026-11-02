# PR diff (the real change)

```diff
diff --git a/storage/errors_test.go b/storage/errors_test.go
index 706719d137d..22837200247 100644
--- a/storage/errors_test.go
+++ b/storage/errors_test.go
@@ -30,12 +30,16 @@ func TestAppendPartialErrorToError(t *testing.T) {
 	require.NoError(t, emptyErr.ToError())
 
 	// Also test explicitly empty slice.
-	emptySliceErr := &AppendPartialError{ExemplarErrors: []error{}}
+	emptySliceErr := &AppendPartialError{ExemplarErrors: []ExemplarError{}}
 	require.NoError(t, emptySliceErr.ToError())
 
 	// Non-empty ExemplarErrors returns the error.
-	nonEmptyErr := &AppendPartialError{ExemplarErrors: []error{ErrOutOfOrderExemplar}}
+	nonEmptyErr := &AppendPartialError{ExemplarErrors: []ExemplarError{{Index: 1, Err: ErrOutOfOrderExemplar}}}
 	require.ErrorIs(t, nonEmptyErr.ToError(), nonEmptyErr)
+
+	// Exemplar errors match their cause, and only causes are part of the message.
+	require.ErrorIs(t, nonEmptyErr.ExemplarErrors[0], ErrOutOfOrderExemplar)
+	require.EqualError(t, nonEmptyErr, ErrOutOfOrderExemplar.Error())
 }
 
 func TestErrDuplicateSampleForTimestamp(t *testing.T) {
diff --git a/storage/fanout_test.go b/storage/fanout_test.go
index f3714251ff3..d0df297acc1 100644
--- a/storage/fanout_test.go
+++ b/storage/fanout_test.go
@@ -669,6 +669,10 @@ func TestFanoutAppenderV2(t *testing.T) {
 				// This is because in V2 flow we must append sample even when first append partially failed with exemplars.
 				// Filtering out exemplars is neither feasible, nor important.
 				require.Len(t, pErr.ExemplarErrors, 2)
+				// Both errors refer to the same, only exemplar.
+				for _, eErr := range pErr.ExemplarErrors {
+					require.Equal(t, 0, eErr.Index)
+				}
 			default:
 				require.NoError(t, err)
 			}
@@ -738,7 +742,11 @@ func TestFanoutAppenderV2_AppendExemplars(t *testing.T) {
 			case tt.expectExemplarError:
 				var pErr *storage.AppendPartialError
 				require.ErrorAs(t, err, &pErr)
+				// One for primary, one for secondary, both for the only exemplar.
 				require.Len(t, pErr.ExemplarErrors, 2)
+				for _, eErr := range pErr.ExemplarErrors {
+					require.Equal(t, 0, eErr.Index)
+				}
 			default:
 				require.NoError(t, err)
 			}
diff --git a/storage/interface_append.go b/storage/interface_append.go
index 231e7a61028..5fdef0243c5 100644
--- a/storage/interface_append.go
+++ b/storage/interface_append.go
@@ -86,7 +86,30 @@ type AppendV2Options struct {
 // It's up to the caller to decide if it's an ignorable error or not, plus
 // it allows extra reporting (e.g. for Remote Write 2.0 X-Remote-Write-Written headers).
 type AppendPartialError struct {
-	ExemplarErrors []error
+	// ExemplarErrors reports the exemplars that were not written. Several
+	// entries can share an Index when more than one storage rejects the same
+	// exemplar, e.g. behind a fanout storage.
+	ExemplarErrors []ExemplarError
+}
+
+// ExemplarError reports why an exemplar was not written.
+type ExemplarError struct {
+	// Index is the position of the exemplar in the slice passed to
+	// AppenderV2.Append (AppendV2Options.Exemplars) or
+	// ExemplarAppenderV2.AppendExemplars.
+	Index int
+	// Err is why the exemplar was not written. It must not be nil.
+	Err error
+}
+
+// Error returns the message of Err.
+func (e ExemplarError) Error() string {
+	return e.Err.Error()
+}
+
+// Unwrap returns Err.
+func (e ExemplarError) Unwrap() error {
+	return e.Err
 }
 
 // Error returns combined error string.
@@ -95,11 +118,15 @@ func (e *AppendPartialError) Error() string {
 		return "<nil>"
 	}
 
-	errs := errors.Join(e.ExemplarErrors...)
-	if errs == nil {
+	errs := make([]error, 0, len(e.ExemplarErrors))
+	for _, eErr := range e.ExemplarErrors {
+		errs = append(errs, eErr.Err)
+	}
+	joined := errors.Join(errs...)
+	if joined == nil {
 		return ""
 	}
-	return errs.Error()
+	return joined.Error()
 }
 
 // ToError returns AppendPartialError as error, returning nil
@@ -181,7 +208,8 @@ type AppenderV2 interface {
 	// TODO(bwplotka): We plan to experiment on using generics for complex sampleType, but do it after we unify interface (derisk) and before we add native summaries.
 	//
 	// Implementations MUST attempt to append sample even if metadata, exemplar or (st) start timestamp appends fail.
-	// Implementations MAY return AppendPartialError as an error. Use errors.As to detect.
+	// Implementations MAY return AppendPartialError as an error to report which of the
+	// given opts.Exemplars failed. Use errors.As to detect.
 	// For the successful Append, Implementations MUST return valid SeriesRef that represents ls.
 	//   NOTE(bwplotka): Given OTLP and native histograms and the relaxation of the requirement for
 	//   type and unit suffixes in metric names we start to hit cases of ls being not enough for id
diff --git a/storage/remote/write_handler.go b/storage/remote/write_handler.go
index b9cc3bc019f..90f830f0350 100644
--- a/storage/remote/write_handler.go
+++ b/storage/remote/write_handler.go
@@ -531,9 +531,12 @@ func (app *timeLimitAppenderV2) Append(ref storage.SeriesRef, ls labels.Labels,
 	return ref, partialErr.ToError()
 }
 
+// limitExemplars returns the exemplars that are not too far in the future, and
+// reports the index of each one it drops. Exemplars are sorted by timestamp, so the
+// dropped ones come last and the kept ones keep their indexes.
 func (app *timeLimitAppenderV2) limitExemplars(exemplars []exemplar.Exemplar) ([]exemplar.Exemplar, *storage.AppendPartialError) {
 	var (
-		futureErrs []error
+		futureErrs []storage.ExemplarError
 		valid      = exemplars
 	)
 	for i, e := range exemplars {
@@ -542,7 +545,10 @@ func (app *timeLimitAppenderV2) limitExemplars(exemplars []exemplar.Exemplar) ([
 				valid = make([]exemplar.Exemplar, 0, len(exemplars)-1)
 				valid = append(valid, exemplars[:i]...)
 			}
-			futureErrs = append(futureErrs, fmt.Errorf("%w: timestamp is too far in the future", storage.ErrOutOfBounds))
+			futureErrs = append(futureErrs, storage.ExemplarError{
+				Index: i,
+				Err:   fmt.Errorf("%w: timestamp is too far in the future", storage.ErrOutOfBounds),
+			})
 			continue
 		}
 		if futureErrs != nil {
diff --git a/storage/remote/write_handler_test.go b/storage/remote/write_handler_test.go
index b77ed8220ae..32875508fd1 100644
--- a/storage/remote/write_handler_test.go
+++ b/storage/remote/write_handler_test.go
@@ -1496,10 +1496,10 @@ func (a *mockAppenderV2) AppendExemplars(ref storage.SeriesRef, l labels.Labels,
 		return 0, fmt.Errorf("unknown series ref %d: %w", ref, storage.ErrNotFound)
 	}
 	ref = storage.SeriesRef(hash)
-	var errs []error
-	for _, e := range exemplars {
+	var errs []storage.ExemplarError
+	for i, e := range exemplars {
 		if _, err := m.AppendExemplar(ref, l, e); err != nil && !errors.Is(err, storage.ErrDuplicateExemplar) {
-			errs = append(errs, err)
+			errs = append(errs, storage.ExemplarError{Index: i, Err: err})
 		}
 	}
 	if len(errs) > 0 {
@@ -2114,8 +2114,8 @@ func TestRemoteWriteHandler_V2ExemplarOrderingAndRejectedSeries(t *testing.T) {
 
 	t.Run("AppendPartialError from Append still counts sample and histogram as written", func(t *testing.T) {
 		appendable := &mockAppendable{
-			appendSampleErr:    &storage.AppendPartialError{ExemplarErrors: []error{errors.New("some non-OOO exemplar error")}},
-			appendHistogramErr: &storage.AppendPartialError{ExemplarErrors: []error{storage.ErrOutOfOrderExemplar}},
+			appendSampleErr:    &storage.AppendPartialError{ExemplarErrors: []storage.ExemplarError{{Err: errors.New("some non-OOO exemplar error")}}},
+			appendHistogramErr: &storage.AppendPartialError{ExemplarErrors: []storage.ExemplarError{{Err: storage.ErrOutOfOrderExemplar}}},
 		}
 		handler := NewWriteHandler(
 			promslog.NewNopLogger(),
@@ -2163,8 +2163,8 @@ func TestTimeLimitAppenderV2_LimitExemplars(t *testing.T) {
 		}
 
 		input := []exemplar.Exemplar{
-			{Labels: labels.FromStrings("id", "1"), Value: 1, Ts: 2000}, // future (> maxTime)
-			{Labels: labels.FromStrings("id", "2"), Value: 2, Ts: 400},  // out of order (< 500)
+			{Labels: labels.FromStrings("id", "1"), Value: 1, Ts: 400},  // out of order (< 500)
+			{Labels: labels.FromStrings("id", "2"), Value: 2, Ts: 2000}, // future (> maxTime)
 			{Labels: labels.FromStrings("id", "3"), Value: 3, Ts: 900},  // valid (<= maxTime)
 		}
 		origFirstID := input[0].Labels.Get("id")
@@ -2176,7 +2176,9 @@ func TestTimeLimitAppenderV2_LimitExemplars(t *testing.T) {
 		require.ErrorAs(t, err, &pErr)
 		require.Len(t, pErr.ExemplarErrors, 2)
 		require.ErrorIs(t, pErr.ExemplarErrors[0], storage.ErrOutOfBounds)
+		require.Equal(t, 1, pErr.ExemplarErrors[0].Index)
 		require.ErrorIs(t, pErr.ExemplarErrors[1], storage.ErrOutOfOrderExemplar)
+		require.Equal(t, 0, pErr.ExemplarErrors[1].Index)
 
 		// Caller's input slice must not be mutated in place.
 		require.Equal(t, origFirstID, input[0].Labels.Get("id"))
diff --git a/tsdb/agent/db_append_v2.go b/tsdb/agent/db_append_v2.go
index 97858c2479c..c1af0bfb025 100644
--- a/tsdb/agent/db_append_v2.go
+++ b/tsdb/agent/db_append_v2.go
@@ -157,15 +157,15 @@ func (a *appenderV2) Rollback() error {
 }
 
 func (a *appenderV2) appendExemplars(s *memSeries, exemplar []exemplar.Exemplar) error {
-	var errs []error
-	for _, e := range exemplar {
+	var errs []storage.ExemplarError
+	for i, e := range exemplar {
 		// Ensure no empty labels have gotten through.
 		e.Labels = e.Labels.WithoutEmpty()
 
 		if err := a.validateExemplar(s.ref, e); err != nil {
 			if !errors.Is(err, storage.ErrDuplicateExemplar) {
 				// Except duplicates, return partial errors.
-				errs = append(errs, err)
+				errs = append(errs, storage.ExemplarError{Index: i, Err: err})
 				continue
 			}
 			if !errors.Is(err, storage.ErrOutOfOrderExemplar) {
diff --git a/tsdb/agent/db_append_v2_test.go b/tsdb/agent/db_append_v2_test.go
index 08d29d8d277..4a5317a4bd4 100644
--- a/tsdb/agent/db_append_v2_test.go
+++ b/tsdb/agent/db_append_v2_test.go
@@ -74,12 +74,13 @@ func TestDB_InvalidSeries_AppendV2(t *testing.T) {
 
 		e = exemplar.Exemplar{Labels: labels.FromStrings("a_somewhat_long_trace_id", "nYJSNtFrFTY37VR7mHzEE/LIDt7cdAQcuOzFajgmLDAdBSRHYPDzrxhMA4zz7el8naI/AoXFv9/e/G0vcETcIoNUi3OieeLfaIRQci2oa")}
 		_, err = app.Append(0, labels.FromStrings("a", "2"), 0, 0, 0, nil, nil, storage.AOptions{
-			Exemplars: []exemplar.Exemplar{e},
+			Exemplars: []exemplar.Exemplar{{Labels: labels.FromStrings("a", "1")}, e},
 		})
 		partErr = &storage.AppendPartialError{}
 		require.ErrorAs(t, err, &partErr)
 		require.Len(t, partErr.ExemplarErrors, 1)
 		require.ErrorIs(t, partErr.ExemplarErrors[0], storage.ErrExemplarLabelLength, "should reject too long label length")
+		require.Equal(t, 1, partErr.ExemplarErrors[0].Index, "should report the position of the rejected exemplar")
 
 		// Inverse check.
 		e = exemplar.Exemplar{Labels: labels.FromStrings("a", "1"), Value: 20, Ts: 10, HasTs: true}
diff --git a/tsdb/head_append_v2.go b/tsdb/head_append_v2.go
index b4acb257978..012f8a1abcf 100644
--- a/tsdb/head_append_v2.go
+++ b/tsdb/head_append_v2.go
@@ -361,15 +361,14 @@ func (a *headAppenderV2) appendFloatHistogram(s *memSeries, st, t int64, fh *his
 }
 
 func (a *headAppenderV2) appendExemplars(s *memSeries, exemplars []exemplar.Exemplar) error {
-	var errs []error
-	for _, e := range exemplars {
+	var errs []storage.ExemplarError
+	for i, e := range exemplars {
 		// Ensure no empty labels have gotten through.
 		e.Labels = e.Labels.WithoutEmpty()
 		if err := a.head.exemplars.ValidateExemplar(s.labels(), e); err != nil {
 			if !errors.Is(err, storage.ErrDuplicateExemplar) && !errors.Is(err, storage.ErrExemplarsDisabled) {
 				// Except duplicates, return partial errors.
-				// TODO(bwplotka): Add exemplar info into error.
-				errs = append(errs, err)
+				errs = append(errs, storage.ExemplarError{Index: i, Err: err})
 				continue
 			}
 			if !errors.Is(err, storage.ErrOutOfOrderExemplar) {
diff --git a/tsdb/head_append_v2_test.go b/tsdb/head_append_v2_test.go
index 4f5e2e7efb4..20e99331d80 100644
--- a/tsdb/head_append_v2_test.go
+++ b/tsdb/head_append_v2_test.go
@@ -5331,11 +5331,13 @@ func TestHeadAppenderV2_ExemplarAppenderV2(t *testing.T) {
 	tooLongLabel := strings.Repeat("x", exemplar.ExemplarMaxLabelSetLength+1)
 	invalidEx := exemplar.Exemplar{Labels: labels.FromStrings("trace_id", tooLongLabel), Value: 3, Ts: 250, HasTs: true}
 	ex3 := exemplar.Exemplar{Labels: labels.FromStrings("trace_id", "t3"), Value: 3, Ts: 300, HasTs: true}
-	retRef, err = headApp.AppendExemplars(0, lsetWithEmpty, []exemplar.Exemplar{invalidEx, ex3})
+	// The ignored duplicate ex2 still counts towards the index of invalidEx.
+	retRef, err = headApp.AppendExemplars(0, lsetWithEmpty, []exemplar.Exemplar{ex2, invalidEx, ex3})
 	var pErr *storage.AppendPartialError
 	require.ErrorAs(t, err, &pErr)
 	require.Len(t, pErr.ExemplarErrors, 1)
 	require.ErrorIs(t, pErr.ExemplarErrors[0], storage.ErrExemplarLabelLength)
+	require.Equal(t, 1, pErr.ExemplarErrors[0].Index)
 	require.Equal(t, ref, retRef)
 
 	// Unknown series must return ErrNotFound even when exemplars is empty.
diff --git a/util/teststorage/appender.go b/util/teststorage/appender.go
index 23b47466523..f276e33e32d 100644
--- a/util/teststorage/appender.go
+++ b/util/teststorage/appender.go
@@ -590,9 +590,9 @@ func (a *appenderV2) Append(ref storage.SeriesRef, ls labels.Labels, st, t int64
 
 		if len(opts.Exemplars) > 0 {
 			if a.a.appendExemplarsError != nil {
-				var exErrs []error
-				for range opts.Exemplars {
-					exErrs = append(exErrs, a.a.appendExemplarsError)
+				var exErrs []storage.ExemplarError
+				for i := range opts.Exemplars {
+					exErrs = append(exErrs, storage.ExemplarError{Index: i, Err: a.a.appendExemplarsError})
 				}
 				if len(exErrs) > 0 {
 					partialErr = &storage.AppendPartialError{ExemplarErrors: exErrs}
@@ -683,9 +683,9 @@ func (a *appenderV2) AppendExemplars(ref storage.SeriesRef, l labels.Labels, exe
 
 	if !a.a.skipRecording && len(exemplars) > 0 {
 		if a.a.appendExemplarsError != nil {
-			exErrs := make([]error, len(exemplars))
+			exErrs := make([]storage.ExemplarError, len(exemplars))
 			for i := range exemplars {
-				exErrs[i] = a.a.appendExemplarsError
+				exErrs[i] = storage.ExemplarError{Index: i, Err: a.a.appendExemplarsError}
 			}
 			partialErr, _ = partialErr.Handle(&storage.AppendPartialError{ExemplarErrors: exErrs})
 		} else {

```

# REVIEW A

## Review of #20026: report which exemplars failed in `AppendPartialError`

Overall this is a clean, well-scoped change. I only read the diff and didn't build it or run the tests. The truncated middle of the diff was visible only in part, so I didn't see the rest of `head_append_v2.go`. I also couldn't see how `limitExemplars` merges downstream errors.

### What works well
- **Type design.** `ExemplarError{Index, Err}` with `Error()` and `Unwrap()` keeps `errors.Is` working. `AppendPartialError.Error()` still joins only the causes, so messages are unchanged, and `errors_test.go` pins both behaviours.
- **Docs.** The doc comments say what `Index` refers to and that several entries can share an index behind a fanout. The `AppenderV2` interface comment is updated too.
- **Tests.** They mostly use realistic multi-exemplar inputs so a nonzero index is actually checked:
  - The head and agent tests put the failing exemplar at index 1.
  - The head test deliberately includes an ignored duplicate to show it still counts towards the index.
  - The fanout tests assert that both entries share index 0.
- It also resolves the `TODO(bwplotka)` in the head appender.

### Issues and suggestions

1. **`limitExemplars` assumes sorted input, and the test contradicts it.**
   - The new doc comment says "Exemplars are sorted by timestamp, so the dropped ones come last and the kept ones keep their indexes."
   - The test was reordered so the future exemplar (`Ts: 2000`) comes before a valid one (`Ts: 900`). That input is not sorted by timestamp.
   - The behaviour matters because the downstream appender is handed the filtered `valid` slice. Any `Index` it reports is relative to that slice, not to the caller's original slice.
   - If a future exemplar is followed by kept ones, those downstream indexes shift. They would no longer match the caller's `opts.Exemplars`, which breaks the contract documented on `ExemplarError.Index`.
   - Please either:
     - make the test input sorted, so it matches the documented invariant, or
     - remap downstream indexes back to the original positions.
   - The follow-up commit `ddf8dd253` ("drop exemplar index remapping and dedup") suggests remapping was considered and removed. If so, the sorted-input guarantee should be stated and tested. For example, assert that the handler sorts exemplars before this appender sees them.

2. **Third-party constructors fail silently.**
   - The PR notes that outside code must now set `Index`. A zero value compiles and silently reports index 0.
   - `write_handler_test.go` does exactly this, with `{Err: ...}` and no index. That's fine for those tests, but it shows how easy it is to get wrong.
   - A short mention in the release notes or a changelog "[CHANGE]" entry would help downstream projects such as Mimir, Thanos and Cortex. The notes currently say `NONE`. This is a Go API break for library users, but it is not user-facing.

3. **Nil `Err` panics.**
   - `ExemplarError.Error()` dereferences `Err`, and the doc says "must not be nil". `AppendPartialError.Error()` also calls `e.Err` in `errors.Join`, where nil is silently dropped instead of panicking.
   - The two paths behave inconsistently. Consider making `ExemplarError.Error()` nil-safe, or leave it and accept the documented contract.

4. **Minor points.**
   - In `AppendPartialError.Error()`, the `joined == nil` branch is now reachable only when every `Err` is nil. It's harmless, but it's a hint that nil handling is worth deciding on (see 3).
   - In `teststorage/appender.go`, `if len(exErrs) > 0` is redundant after a loop over a non-empty `opts.Exemplars`. This is pre-existing and not worth a change here.
   - The agent `appendExemplars` code has `if !errors.Is(err, storage.ErrOutOfOrderExemplar)` nested inside a branch where the error is already known to be a duplicate. That looks pre-existing, but it's worth a look while you're in this code.

### Performance and security
No concerns. There's no hot-path allocation change beyond a slightly larger error struct, and it only touches error paths. There's no security impact.

### Conventions
- The title follows `area: description`.
- The release-notes block is present.
- Tests are extended rather than duplicated, and they use the exported API.

### Verdict
Approve in substance. The one item I'd want resolved is (1), where the sorted-input claim, the reordered test and the index semantics for downstream errors need to agree. (The PR is already merged, so this would be a follow-up.)

# REVIEW B

# Review of PR #20026: report which exemplars failed in `AppendPartialError`

This PR is already merged, so these notes are for follow-up. Overall it is a clean, well-scoped change, and it resolves the `TODO(bwplotka)` in the Head appender. I found no correctness bugs in the code paths I read. The one design concern is the index invariant in `limitExemplars`. I only read the diff and did not build or run the tests.

## What works well
- `ExemplarError` implements `Error` and `Unwrap`, so `errors.Is(err, storage.ErrOutOfOrderExemplar)` still works and error messages don't change. The new assertions in `errors_test.go` check both.
- The tests improve on the old ones. The Head test now puts a skipped duplicate before the invalid exemplar, which shows that duplicates still count toward the index. The Agent test puts the bad exemplar at index 1. The fanout tests check that both storages report index 0.
- The `ExemplarError` and `AppendPartialError` doc comments cover duplicate indexes behind a fanout storage, and the `AppenderV2` interface comment is updated.
- The PR description says how downstream code that builds an `AppendPartialError` must change.

## Issues and suggestions

1. **Fragile index invariant in `limitExemplars` (`storage/remote/write_handler.go`).**
   - The new comment says exemplars are sorted by timestamp, so dropped ones come last and kept ones keep their indexes. The code does not enforce this. The loop still handles a future exemplar followed by valid ones, because it copies later exemplars into `valid`.
   - If that ever happens, the inner appender receives the shortened `valid` slice. Any `ExemplarError.Index` it reports is then relative to `valid`, but the time-limit errors are relative to the original slice. After `Handle` merges them, indexes would be silently wrong. This is the same "indices relative to the caller's slice" contract the PR documents.
   - The test was reordered so the future exemplar comes last, which hides the problem. I'd either:
     - assert the sorted precondition (or sort or partition upstream), or
     - remap the inner indexes back to the original positions when `valid` was compacted. The remapping is cheap, since the dropped indexes are already known.
   - A test with the future exemplar in the middle would document whichever behaviour you choose.

2. **`AppendPartialError.Error()` can now panic on a nil `Err`.**
   - Before, `errors.Join` skipped nil entries. Now `ExemplarError.Error()` and the loop in `AppendPartialError.Error()` dereference `Err` directly. The doc comment says `Err` "must not be nil", but a defensive nil skip in `Error()` costs little. Third-party appenders will have to adapt to the new type anyway, and a nil `Err` there would panic in logging paths.
   - `AppendPartialError.Error()` also allocates a temporary `[]error` on every call. That is negligible, but a `strings.Builder` or an `Unwrap() []error` method would avoid it and let `errors.Is` and `errors.As` work on the partial error directly.

3. **API break for downstream users.**
   - `ExemplarErrors []error` becoming `[]ExemplarError` breaks Cortex, Thanos and Mimir wherever they construct or iterate the field. This is acceptable under the stability policy, and the PR description mentions it. It is worth making sure the CHANGELOG or release notes for the next release call it out. The block currently says `NONE`, which is arguably right for end users, but integrators would want a note.

4. **Minor test points.**
   - Several tests in `write_handler_test.go` build `ExemplarError{Err: ...}` and leave `Index` at 0. That is fine, but a test that checks indexes survive the whole remote-write handler path would be useful.
   - The `teststorage` appender reports every exemplar as failed. That fits its purpose.

## Security and performance
There are no security concerns. Performance impact is negligible: one `int` per failed exemplar and a loop index that already existed.

**Verdict:** Approve, with a follow-up for point 1, which is the only one with potential for wrong data.
