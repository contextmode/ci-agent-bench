# PR diff (the real change)

```diff
diff --git a/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactory.java b/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactory.java
index 9a0461e2d291a..c70eb460cf7d0 100644
--- a/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactory.java
+++ b/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactory.java
@@ -1055,10 +1055,34 @@ public boolean deferredExtractionEnabled() {
      * pre-encode every {@code _rowPosition} value it emits with that id. Caller must ensure the
      * reader implements {@link ColumnExtractorAware}; this is validated at
      * {@link Builder#build} time.
+     * <p>
+     * If registration fails (notably {@link SourceExtractors.ClosedException} when the driver finished while this
+     * unit was being opened), the extractor is closed here, outside the registry's monitor, because nothing else
+     * references it.
      */
     private int registerExtractorFromProducer(ColumnExtractorProducer producer, DriverContext driverContext) throws IOException {
         ColumnExtractor extractor = producer.createColumnExtractor(driverThreadInformationalWarningSink(driverContext));
-        return sourceExtractorsFor(driverContext).register(extractor);
+        try {
+            return sourceExtractorsFor(driverContext).register(extractor);
+        } catch (Exception e) {
+            Releasables.closeWhileHandlingException(extractor);
+            throw e;
+        }
+    }
+
+    /**
+     * Whether {@code e} is the expected race of a driver that finished while this producer was opening its next
+     * unit: the extract operator closed the {@link SourceExtractors} registry, which only happens after the driver
+     * closed the source and so finished {@code buffer}. A closed registry with a live buffer is a wiring bug and
+     * is not matched, so it still fails the query instead of silently truncating results. A match is logged at
+     * {@code DEBUG} so the frequency of the race stays observable even though the exception is dropped.
+     */
+    private static boolean isRegistryClosedAfterBufferFinished(Throwable e, AsyncExternalSourceBuffer buffer) {
+        if (e instanceof SourceExtractors.ClosedException && buffer.noMoreInputs()) {
+            logger.debug("driver finished while the source was opening its next unit; ending the source without a failure");
+            return true;
+        }
+        return false;
     }
 
     /**
@@ -2351,9 +2375,22 @@ private void deliverPage(Page page, AsyncExternalSourceBuffer buffer) {
     /**
      * Advance the iteration position to the next unit (slice-queue leaf or multi-file file) and
      * open a fresh page iterator for it. Returns {@code false} if iteration is exhausted or the
-     * buffer has been finished externally.
+     * buffer has been finished externally, including when the driver finished while this unit was opening and its
+     * extractor could no longer be registered.
      */
     private boolean advanceToNextUnit(ProducerState state) throws IOException {
+        try {
+            return advanceToNextUnitUnguarded(state);
+        } catch (SourceExtractors.ClosedException e) {
+            // The driver finished while this unit was opening (the open paths already released the iterator).
+            if (isRegistryClosedAfterBufferFinished(e, state.buffer)) {
+                return false;
+            }
+            throw e;
+        }
+    }
+
+    private boolean advanceToNextUnitUnguarded(ProducerState state) throws IOException {
         while (true) {
             if (noFurtherCandidates()) {
                 return false;
@@ -3061,7 +3098,9 @@ private void consumePagesInBackground(
         final CloseableIterator<Page> capturing = StatsCapturingIterator.wrap(pages, buffer.capturedSourceMetadataSink());
         ActionListener<Void> failureListener = ActionListener.wrap(v -> {}, e -> {
             closeQuietly(capturing);
-            buffer.onFailure(e);
+            if (isRegistryClosedAfterBufferFinished(e, buffer) == false) {
+                buffer.onFailure(e);
+            }
             driverContext.removeAsyncAction();
             releaseOperator();
         });
@@ -3153,7 +3192,9 @@ private static List<ExternalSplit> flattenToLeaves(ExternalSplit split) {
      */
     private ActionListener<Void> failureListener(AsyncExternalSourceBuffer buffer, DriverContext driverContext) {
         return ActionListener.wrap(v -> {}, e -> {
-            buffer.onFailure(e);
+            if (isRegistryClosedAfterBufferFinished(e, buffer) == false) {
+                buffer.onFailure(e);
+            }
             driverContext.removeAsyncAction();
             releaseOperator();
         });
diff --git a/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/SourceExtractors.java b/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/SourceExtractors.java
index 325f5c5155e63..bcc6cb3513a03 100644
--- a/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/SourceExtractors.java
+++ b/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/SourceExtractors.java
@@ -114,6 +114,17 @@ public static long decodeLocalPosition(long encoded) {
         return encoded & MAX_LOCAL_POSITION;
     }
 
+    /**
+     * Thrown by {@link #register} when the registry was already closed. A driver that finishes before the
+     * source producer runs out of units closes the registry while the producer may still be opening the next
+     * unit, so the caller can tell this expected shutdown race apart from other {@link IllegalStateException}s.
+     */
+    public static final class ClosedException extends IllegalStateException {
+        ClosedException() {
+            super("SourceExtractors is closed");
+        }
+    }
+
     private final List<ColumnExtractor> extractors = new ArrayList<>();
     /**
      * Resources whose lifecycle must extend beyond the source operator's, because the deferred
@@ -132,14 +143,15 @@ public static long decodeLocalPosition(long encoded) {
      * pack into the {@code _rowPosition} values they emit for rows coming from this extractor's
      * file.
      *
-     * @throws IllegalStateException if the table is closed or if the id space is exhausted
+     * @throws ClosedException       if the table is closed
+     * @throws IllegalStateException if the id space is exhausted
      */
     public synchronized int register(ColumnExtractor extractor) {
         if (extractor == null) {
             throw new IllegalArgumentException("extractor must not be null");
         }
         if (closed) {
-            throw new IllegalStateException("SourceExtractors is closed");
+            throw new ClosedException();
         }
         int id = extractors.size();
         if (id > MAX_EXTRACTOR_ID) {
@@ -243,7 +255,7 @@ public Block[] materialize(long[] encodedRefs, int count, List<String> columns,
         final List<ColumnExtractor> snapshot;
         synchronized (this) {
             if (closed) {
-                throw new IllegalStateException("SourceExtractors is closed");
+                throw new ClosedException();
             }
             snapshot = new ArrayList<>(extractors);
         }
diff --git a/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/spi/ColumnExtractorProducer.java b/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/spi/ColumnExtractorProducer.java
index 2d05592ec7cbd..a9ec3bb9e1542 100644
--- a/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/spi/ColumnExtractorProducer.java
+++ b/x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/datasources/spi/ColumnExtractorProducer.java
@@ -44,7 +44,9 @@
  * Implementations should construct the extractor lazily — typically on the first call to
  * {@link #createColumnExtractor(Consumer)} and may return the same instance on subsequent calls.
  * Lifetime is owned by the caller via {@code SourceExtractors} (the registry calls
- * {@link ColumnExtractor#close()} when the driver finishes).
+ * {@link ColumnExtractor#close()} when the driver finishes). If the registry is already closed when the
+ * extractor is about to be registered (the driver finished while the source was opening this unit), the
+ * caller closes the extractor without ever registering it, so {@code close()} must not depend on registration.
  */
 public interface ColumnExtractorProducer {
 
diff --git a/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactoryDeferredExtractionTests.java b/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactoryDeferredExtractionTests.java
index a48440c7fd154..34ea2eba6ba1a 100644
--- a/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactoryDeferredExtractionTests.java
+++ b/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/AsyncExternalSourceOperatorFactoryDeferredExtractionTests.java
@@ -32,6 +32,7 @@
 import org.elasticsearch.xpack.esql.datasources.spi.ColumnExtractor;
 import org.elasticsearch.xpack.esql.datasources.spi.ColumnExtractorAware;
 import org.elasticsearch.xpack.esql.datasources.spi.ColumnExtractorProducer;
+import org.elasticsearch.xpack.esql.datasources.spi.ExternalSplit;
 import org.elasticsearch.xpack.esql.datasources.spi.FileList;
 import org.elasticsearch.xpack.esql.datasources.spi.FormatReadContext;
 import org.elasticsearch.xpack.esql.datasources.spi.FormatReader;
@@ -48,20 +49,28 @@
 import java.io.IOException;
 import java.io.InputStream;
 import java.time.Instant;
+import java.util.ArrayDeque;
 import java.util.ArrayList;
 import java.util.Collections;
+import java.util.Deque;
 import java.util.Iterator;
 import java.util.List;
 import java.util.Map;
+import java.util.concurrent.atomic.AtomicBoolean;
 import java.util.concurrent.atomic.AtomicInteger;
+import java.util.concurrent.atomic.AtomicReference;
 import java.util.function.Consumer;
+import java.util.function.IntConsumer;
 
+import static org.hamcrest.Matchers.containsString;
 import static org.hamcrest.Matchers.equalTo;
 import static org.hamcrest.Matchers.hasItem;
 import static org.hamcrest.Matchers.hasSize;
 import static org.mockito.ArgumentMatchers.any;
 import static org.mockito.Mockito.doAnswer;
 import static org.mockito.Mockito.mock;
+import static org.mockito.Mockito.times;
+import static org.mockito.Mockito.verify;
 import static org.mockito.Mockito.when;
 
 /**
@@ -168,6 +177,163 @@ public void testDeferredExtractionRegistersExtractorPerFileAndEncodesRowPosition
         }
     }
 
+    /** The ways a scan can open its units; each one registers the extractor on a different code path. */
+    private enum OpenMode {
+        /** Slice-queue leaves. */
+        SLICE_QUEUE,
+        MULTI_FILE,
+        /** Single file through {@code startSyncWrapperRead}. */
+        SYNC_SINGLE_FILE,
+        /** Single file through {@code startNativeAsyncRead} / {@code consumePagesInBackground}. */
+        NATIVE_ASYNC_SINGLE_FILE;
+
+        boolean singleFile() {
+            return this == SYNC_SINGLE_FILE || this == NATIVE_ASYNC_SINGLE_FILE;
+        }
+    }
+
+    /**
+     * A driver that finishes (e.g. a {@code LIMIT} reached) while the producer is still opening the next unit closes the
+     * source and then the registry, so registering the newly opened unit's extractor hits a closed registry. That race is
+     * expected: the producer must end quietly, close the extractor it just created and not open any further unit.
+     */
+    public void testProducerEndsQuietlyWhenDriverFinishesWhileOpeningNextUnit() {
+        for (OpenMode mode : OpenMode.values()) {
+            int triggerUnit = mode.singleFile() ? 0 : randomIntBetween(0, UNITS - 1);
+            runWithDriverFinishingWhileOpening(mode, triggerUnit, true).assertEndedQuietly(triggerUnit + 1);
+        }
+    }
+
+    /**
+     * A closed registry while the source buffer is still live is not the shutdown race: it must still fail the query
+     * instead of silently truncating results. The unregistered extractor is closed in every case.
+     */
+    public void testClosedRegistryWithLiveBufferStillFails() {
+        for (OpenMode mode : OpenMode.values()) {
+            int triggerUnit = mode.singleFile() ? 0 : randomIntBetween(0, UNITS - 1);
+            runWithDriverFinishingWhileOpening(mode, triggerUnit, false).assertFailedClosedRegistry(triggerUnit + 1);
+        }
+    }
+
+    /** Units (files or splits) a multi-unit scan has; a single-file scan has one. */
+    private static final int UNITS = 3;
+
+    private record FinishDuringOpen(
+        OpenMode mode,
+        FormatReader_RowPositionEmitting reader,
+        AsyncExternalSourceOperator operator,
+        AtomicInteger readCount,
+        DriverContext driverContext
+    ) {
+
+        void assertEndedQuietly(int expectedReads) {
+            assertNull(mode + ": a driver that finished first must not leave a failure", operator.status().failure());
+            verify(driverContext, times(1)).removeAsyncAction();
+            assertClosedUnregisteredExtractor(expectedReads);
+        }
+
+        void assertFailedClosedRegistry(int expectedReads) {
+            Throwable failure = operator.status().failure();
+            assertNotNull(mode + ": a closed registry under a live buffer must fail the query", failure);
+            // Pins that the failure is the closed registry and not an unrelated error.
+            assertThat(mode.toString(), failure.getMessage(), containsString("SourceExtractors is closed"));
+            verify(driverContext, times(1)).removeAsyncAction();
+            assertClosedUnregisteredExtractor(expectedReads);
+        }
+
+        private void assertClosedUnregisteredExtractor(int expectedReads) {
+            assertEquals(mode + ": no unit is opened after the registry closed", expectedReads, readCount.get());
+            assertEquals(mode.toString(), expectedReads, reader.createdExtractors.size());
+            for (InMemoryColumnExtractor extractor : reader.createdExtractors) {
+                assertEquals(mode + ": every extractor is closed exactly once", 1, extractor.closeCount.get());
+            }
+            InMemoryColumnExtractor unregistered = reader.createdExtractors.getLast();
+            assertFalse(
+                mode + ": the unregistered extractor must not be closed under the registry monitor",
+                unregistered.closedWhileHoldingMonitor.get()
+            );
+        }
+    }
+
+    /**
+     * Runs a deferred-extraction scan over {@link #UNITS} units (one for the single-file modes) on a manually driven executor.
+     * While the producer opens unit {@code triggerUnit}, after its reader returned and before its extractor is
+     * registered, the "driver" finishes: it optionally closes the operator (finishing the buffer, as {@code Driver} does
+     * first) and then closes the registry (what {@code ExternalFieldExtractOperator} does).
+     */
+    private FinishDuringOpen runWithDriverFinishingWhileOpening(OpenMode mode, int triggerUnit, boolean finishBuffer) {
+        AtomicInteger readCount = new AtomicInteger();
+        FormatReader_RowPositionEmitting reader = new FormatReader_RowPositionEmitting(readCount, new AtomicInteger(), 3);
+        reader.nativeAsync(mode == OpenMode.NATIVE_ASYNC_SINGLE_FILE);
+
+        List<Attribute> attributes = List.of(field("value", DataType.INTEGER), field(ColumnExtractor.ROW_POSITION_COLUMN, DataType.LONG));
+        // DriverContext is mocked, as in the sibling tests, because a real one needs a full driver; the mock also lets
+        // the test count removeAsyncAction() calls. Stop hooks and waitForAsyncActions callbacks are irrelevant here.
+        DriverContext driverContext = mock(DriverContext.class);
+        when(driverContext.blockFactory()).thenReturn(BLOCK_FACTORY);
+        doAnswer(inv -> null).when(driverContext).addAsyncAction();
+        doAnswer(inv -> null).when(driverContext).removeAsyncAction();
+
+        // Tasks only run when the test drains them, so the hook below can use the operator returned by get().
+        Deque<Runnable> tasks = new ArrayDeque<>();
+        StoragePath path = StoragePath.of("s3://bucket/data/f1.parquet");
+        var builder = AsyncExternalSourceOperatorFactory.builder(
+            new StubStorageProvider(),
+            reader,
+            path,
+            attributes,
+            100,
+            10,
+            (Runnable r) -> tasks.add(r)
+        ).deferredExtraction(true);
+        switch (mode) {
+            case MULTI_FILE -> {
+                List<StorageEntry> entries = new ArrayList<>();
+                for (int i = 1; i <= UNITS; i++) {
+                    entries.add(new StorageEntry(StoragePath.of("s3://bucket/data/f" + i + ".parquet"), 100L * i, Instant.EPOCH));
+                }
+                builder.fileList(GlobExpander.fileListOf(entries, "s3://bucket/data/*.parquet"));
+            }
+            case SLICE_QUEUE -> {
+                List<ExternalSplit> splits = new ArrayList<>();
+                for (int i = 1; i <= UNITS; i++) {
+                    Map<String, Object> config = i == UNITS ? Map.of(FileSplitProvider.LAST_SPLIT_KEY, "true") : Map.of();
+                    splits.add(
+                        new FileSplit("test", StoragePath.of("s3://bucket/data/f" + i + ".parquet"), 0, 100, "parquet", config, Map.of())
+                    );
+                }
+                builder.sliceQueue(new ExternalSliceQueue(splits));
+            }
+            case SYNC_SINGLE_FILE, NATIVE_ASYNC_SINGLE_FILE -> {
+            }
+        }
+        AsyncExternalSourceOperatorFactory factory = builder.build();
+
+        SourceExtractors registry = factory.sourceExtractorsFor(driverContext);
+        reader.registryMonitor = registry;
+        AtomicReference<SourceOperator> operatorRef = new AtomicReference<>();
+        reader.onRead(idx -> {
+            if (idx == triggerUnit) {
+                if (finishBuffer) {
+                    operatorRef.get().close();
+                }
+                registry.close();
+            }
+        });
+
+        AsyncExternalSourceOperator operator = (AsyncExternalSourceOperator) factory.get(driverContext);
+        operatorRef.set(operator);
+        Runnable task;
+        while ((task = tasks.poll()) != null) {
+            task.run();
+        }
+        if (finishBuffer == false) {
+            // Releases the pages the live buffer still holds.
+            operator.close();
+        }
+        return new FinishDuringOpen(mode, reader, operator, readCount, driverContext);
+    }
+
     /**
      * The deferred extractor's warning sink must deposit into the driver's {@link DriverContext}, which
      * {@code DriverCompletionInfo} ships back from whatever node ran the scan, rather than into the emitting
@@ -990,6 +1156,26 @@ public RowPositionStrategy rowPositionStrategy() {
         private final int rowsPerFile;
         /** Sinks handed to {@link ColumnExtractorProducer#createColumnExtractor}; empty unless a test wants them. */
         private final List<Consumer<String>> capturedSinks;
+        /** Every extractor handed out by {@link ColumnExtractorProducer#createColumnExtractor}, in creation order. */
+        final List<InMemoryColumnExtractor> createdExtractors = Collections.synchronizedList(new ArrayList<>());
+        /** When set, extractors created afterwards record whether {@code close()} ran while holding this monitor. */
+        volatile Object registryMonitor;
+        /** Invoked with the file index at the end of {@link #read}, i.e. while the producer is still opening that unit. */
+        private volatile IntConsumer onRead = idx -> {};
+        private volatile boolean nativeAsync = false;
+
+        void onRead(IntConsumer onRead) {
+            this.onRead = onRead;
+        }
+
+        void nativeAsync(boolean nativeAsync) {
+            this.nativeAsync = nativeAsync;
+        }
+
+        @Override
+        public boolean supportsNativeAsync() {
+            return nativeAsync;
+        }
 
         FormatReader_RowPositionEmitting(AtomicInteger readCount, AtomicInteger extractorsCreated, int rowsPerFile) {
             this(readCount, extractorsCreated, rowsPerFile, Collections.synchronizedList(new ArrayList<>()));
@@ -1015,7 +1201,9 @@ public SourceMetadata metadata(StorageObject object) {
         @Override
         public CloseableIterator<Page> read(StorageObject object, FormatReadContext context) {
             int idx = readCount.getAndIncrement();
-            return new ProducerIterator(idx, extractorsCreated, rowsPerFile, capturedSinks);
+            CloseableIterator<Page> pages = new ProducerIterator(idx, extractorsCreated, rowsPerFile, capturedSinks, this);
+            onRead.accept(idx);
+            return pages;
         }
 
         @Override
@@ -1042,14 +1230,22 @@ private static final class ProducerIterator implements CloseableIterator<Page>,
         private final AtomicInteger extractorsCreated;
         private final int rowsPerFile;
         private final List<Consumer<String>> capturedSinks;
+        private final FormatReader_RowPositionEmitting owner;
         private boolean emitted = false;
         private long rowPositionEncodingHighBits = -1L;
 
-        ProducerIterator(int fileIndex, AtomicInteger extractorsCreated, int rowsPerFile, List<Consumer<String>> capturedSinks) {
+        ProducerIterator(
+            int fileIndex,
+            AtomicInteger extractorsCreated,
+            int rowsPerFile,
+            List<Consumer<String>> capturedSinks,
+            FormatReader_RowPositionEmitting owner
+        ) {
             this.fileIndex = fileIndex;
             this.extractorsCreated = extractorsCreated;
             this.rowsPerFile = rowsPerFile;
             this.capturedSinks = capturedSinks;
+            this.owner = owner;
         }
 
         @Override
@@ -1085,7 +1281,9 @@ public ColumnExtractor createColumnExtractor(@Nullable Consumer<String> driverTh
             if (driverThreadWarningSink != null) {
                 capturedSinks.add(driverThreadWarningSink);
             }
-            return new InMemoryColumnExtractor(rowsPerFile);
+            InMemoryColumnExtractor extractor = new InMemoryColumnExtractor(rowsPerFile, owner.registryMonitor);
+            owner.createdExtractors.add(extractor);
+            return extractor;
         }
 
         @Override
@@ -1131,9 +1329,17 @@ public void close() {}
     /** Trivial {@link ColumnExtractor} stub — never invoked by these tests, just registered. */
     private static final class InMemoryColumnExtractor implements ColumnExtractor {
         private final int totalRows;
+        private final Object monitorToCheck;
+        final AtomicInteger closeCount = new AtomicInteger();
+        final AtomicBoolean closedWhileHoldingMonitor = new AtomicBoolean();
 
         InMemoryColumnExtractor(int totalRows) {
+            this(totalRows, null);
+        }
+
+        InMemoryColumnExtractor(int totalRows, @Nullable Object monitorToCheck) {
             this.totalRows = totalRows;
+            this.monitorToCheck = monitorToCheck;
         }
 
         @Override
@@ -1147,7 +1353,12 @@ public Block[] extract(String[] columnNames, DataType[] targetTypes, long[] loca
         }
 
         @Override
-        public void close() {}
+        public void close() {
+            if (monitorToCheck != null && Thread.holdsLock(monitorToCheck)) {
+                closedWhileHoldingMonitor.set(true);
+            }
+            closeCount.incrementAndGet();
+        }
     }
 
     /** Storage provider that fabricates {@link StorageObject}s for arbitrary paths. */
diff --git a/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/SourceExtractorsTests.java b/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/SourceExtractorsTests.java
index 6e75077392742..184a1b67e973e 100644
--- a/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/SourceExtractorsTests.java
+++ b/x-pack/plugin/esql/src/test/java/org/elasticsearch/xpack/esql/datasources/SourceExtractorsTests.java
@@ -88,7 +88,11 @@ public void testRegisterRejectsNullAndAfterClose() {
         SourceExtractors registry = new SourceExtractors();
         expectThrows(IllegalArgumentException.class, () -> registry.register(null));
         registry.close();
-        expectThrows(IllegalStateException.class, () -> registry.register(new IntListExtractor(new int[] { 1 })));
+        IntListExtractor late = new IntListExtractor(new int[] { 1 });
+        var e = expectThrows(SourceExtractors.ClosedException.class, () -> registry.register(late));
+        assertEquals("SourceExtractors is closed", e.getMessage());
+        assertEquals("a rejected extractor is not added", 0, registry.size());
+        assertEquals("the registry does not close an extractor it never accepted", 0, late.closeCount());
     }
 
     public void testGetRejectsOutOfRange() {
@@ -512,7 +516,10 @@ public void testMaterializeAfterCloseFails() {
         registry.register(new IntListExtractor(new int[] { 1 }));
         registry.close();
         long[] refs = new long[] { SourceExtractors.encode(0, 0) };
-        expectThrows(IllegalStateException.class, () -> registry.materialize(refs, refs.length, List.of("col"), null, blockFactory));
+        expectThrows(
+            SourceExtractors.ClosedException.class,
+            () -> registry.materialize(refs, refs.length, List.of("col"), null, blockFactory)
+        );
     }
 
     public void testRegisterIdSpaceExhaustion() {

```

# REVIEW A

I've read most of the diff, including the production changes and the start of the tests, so I'm writing up the review now.

## Review: #163196 `[9.6] ES|QL|DS: End source quietly on closed registry` (backport of #163128)

The PR is already merged. The review is based on the production changes and most of the test diff. I didn't see the last part of the new test helpers, and I didn't build or run anything.

### Summary
A driver can finish (for example, a `LIMIT` is reached) while the async external source is still opening its next unit. The driver closes the `SourceExtractors` registry, and the producer's later `register()` call then throws `IllegalStateException`. That failed the query even though the result was already complete. The PR adds a dedicated `SourceExtractors.ClosedException`. The producer swallows it only when the buffer has also finished, and it closes the extractor that never got registered.

### What's good
- **Narrow suppression.** `isRegistryClosedAfterBufferFinished` requires both `ClosedException` and `buffer.noMoreInputs()`. A closed registry with a live buffer still fails the query, so a wiring bug can't silently truncate results. The new test `testClosedRegistryWithLiveBufferStillFails` covers this.
- **No leaked extractor.** `registerExtractorFromProducer` closes the extractor on any registration failure, outside the registry's monitor. The SPI Javadoc in `ColumnExtractorProducer` now says `close()` must not depend on registration.
- **Observable.** The swallowed case is logged at DEBUG, and the logging is parameterless, which is fine.
- **Backward compatible.** `ClosedException` extends `IllegalStateException`, so existing catch sites keep working.
- **Good test coverage.** The tests exercise all four open paths: slice queue, multi-file, sync single file and native async single file. They assert that the extractor is closed and that no further unit is opened. `SourceExtractorsTests` also checks that a rejected extractor isn't added or closed by the registry.

### Issues and suggestions
1. **`materialize()` now throws `ClosedException`, but only `register()` handles it.** The race is only handled in the producer's open path. If the extract operator calls `materialize` after close, the exception still propagates as a failure. That is probably intended, since `materialize` after close is a real bug. Add a comment saying so, so no one later widens the catch.
2. **Possible TOCTOU between the buffer check and the registry close.** The check assumes the buffer finishes before the registry closes, as the Javadoc says. If any path closes the registry first (a failure or cancellation path, for example), the check could return false and the query would fail spuriously. Failing is the safe direction, but it would be worth confirming that the ordering is guaranteed.
3. **`closeWhileHandlingException` plus rethrow.** `catch (Exception e)` with `throw e` works because of precise rethrow. Catching `RuntimeException | IOException` explicitly would be a little clearer. This is a nit.
4. **`removeAsyncAction()` and `releaseOperator()` still run when the failure is swallowed.** The test verifies `removeAsyncAction` exactly once, which is good. I couldn't see an equivalent assertion for `releaseOperator`.
5. **Test style.** The tests use Mockito for `DriverContext` and others. This is acceptable in the existing file, but AGENTS.md prefers real classes, with documented reasons where a mock is needed. A short comment on why the mock is needed would help.
6. **Backport hygiene.** The PR is labeled `>non-issue`. The user-visible fix, a spurious failure on `LIMIT` queries, might merit a changelog entry or a release-notes label on the original PR.

### Security and performance
Neither is a concern. The change adds one `instanceof` check on the failure path only. There are no new resources and no new permissions.

### Verdict
Approve. The change is minimal, well-scoped and well-tested. The items above are only minor follow-ups, mainly comments and confirming the close ordering.

# REVIEW B

# Review: PR #163196, backport to 9.6 of "End source quietly on closed registry" (#163128)

The PR is already merged. This review is based on the diff alone. I did not build it or run the tests.

## Summary
When a driver finishes early (for example a `LIMIT` is reached), `ExternalFieldExtractOperator` closes the `SourceExtractors` registry. The source producer may still be opening its next unit at that moment. Registering that unit's extractor then threw `IllegalStateException`, which failed the query. The PR makes three changes:
- It adds a dedicated `SourceExtractors.ClosedException`.
- It treats that exception as benign only if the buffer has already finished (`buffer.noMoreInputs()`).
- It closes the unregistered extractor outside the registry monitor.

## What's good
- **The guard is narrow.** A closed registry with a live buffer still fails the query, so results aren't silently truncated. `testClosedRegistryWithLiveBufferStillFails` pins this behavior.
- **Resource handling is fixed.** `registerExtractorFromProducer` now closes the extractor if `register` throws. Previously it leaked. The close runs outside the `synchronized` registry, and the test checks this with `Thread.holdsLock`.
- **A typed exception beats matching on the message string.** It also preserves `IllegalStateException` as the supertype, so existing catch sites keep working.
- **The tests are thorough.** They cover all four open paths (slice queue, multi-file, sync single file, native async single file). They also assert that no further unit is opened, that each extractor is closed exactly once, and that `removeAsyncAction` is called once.
- **The Javadoc was updated**, including the `ColumnExtractorProducer` contract that `close()` must not depend on registration.

## Issues and suggestions
1. **Race window on `noMoreInputs()`.** The check assumes the driver always finishes the buffer before closing the registry. The Javadoc says this ordering holds. If it ever changed, a legitimate shutdown race would surface as a query failure. That is the safe direction, so this is not a bug. It does couple two components implicitly, so a short assertion or comment at the `ExternalFieldExtractOperator` close site would help.
2. **Closed registry hit in `materialize`.** `materialize` now also throws `ClosedException`, but no production caller handles it specially. That is fine, because it should still fail. The Javadoc for `materialize` doesn't mention the new type, which is a minor gap.
3. **`catch (Exception e)` plus rethrow in `registerExtractorFromProducer`.** This is correct, since Java's precise rethrow keeps the `IOException` signature. `Releasables.closeWhileHandlingException` also stops a close failure from masking the original exception. Nothing to change.
4. **Logging.** The `DEBUG` log is appropriate, bounded, and follows the repo's parameterized-logging convention. The message has no parameters, so there is nothing to wrap in a supplier.
5. **Test style.**
   - The test builds on a mocked `DriverContext`, and the comment explains why. That is consistent with the sibling tests and with the AGENTS.md rule on documenting mocks.
   - `UNITS` is declared mid-class, after its first use. Moving it to the top with the other constants would read better.
   - The empty `case SYNC_SINGLE_FILE, NATIVE_ASYNC_SINGLE_FILE -> {}` is acceptable. A short comment saying that no setup is needed would help.
   - The mode loops run all four modes in one test method. A failure message includes the mode, which helps. Separate tests would give clearer reporting but cost more setup.
6. **Backport hygiene.** The PR has the `>non-issue` label and carries the 9.6.1 version label. No transport-version or serialization changes are involved, so there are no compatibility concerns.

## Performance and security
- **Performance:** The only added work is an `instanceof` check and a volatile read on the failure path. No hot-path impact.
- **Security:** None apparent. The change doesn't touch input parsing, entitlements, or permissions.

## Verdict
This is a correct, well-scoped fix with good tests. The suggestions above are minor and non-blocking.
