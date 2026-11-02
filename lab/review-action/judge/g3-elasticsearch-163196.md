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

# Review of PR 163196: `[9.6] ES|QL|DS: End source quietly on closed registry` (backport of #163128)

This PR is already merged. I read the diff only and did not build it or run the tests.

## Summary
A driver can finish, for example when a `LIMIT` is reached, while the async external source is still opening its next unit. The driver closes the source and then the `SourceExtractors` registry. When the producer then registers the newly created extractor, `register` throws `IllegalStateException("SourceExtractors is closed")`. That used to surface as a query failure. The PR makes three changes:
- It adds a dedicated `SourceExtractors.ClosedException`.
- It treats that exception as a quiet end of the source, but only when the buffer has already finished (`buffer.noMoreInputs()`).
- It closes the extractor that never got registered.

## What's good
- **Narrow suppression.** The exception is dropped only if `ClosedException` and `buffer.noMoreInputs()` both hold. A closed registry with a live buffer still fails the query, so results can't be silently truncated. The `DEBUG` log keeps the race visible.
- **Typed exception.** A subclass of `IllegalStateException` is source-compatible with existing callers. Both `register` and `materialize` use it, and the tests were updated to match.
- **No leak on failed registration.** `registerExtractorFromProducer` closes the extractor on any exception, and that close runs outside the registry monitor. The `ColumnExtractorProducer` Javadoc now says `close()` must not depend on registration, which documents the contract for implementers.
- **Good tests.**
  - They cover all four open paths: slice queue, multi-file, sync single file and native async single file.
  - There is both a positive case (quiet end) and a negative case (closed registry with a live buffer still fails).
  - They check that each extractor is closed exactly once, that no unit opens after the close, and that `removeAsyncAction` is called once.
  - They check that the extractor is not closed while holding the registry monitor.
  - The `DriverContext` mock has an explanatory comment, as `AGENTS.md` asks.

## Points to check or consider (none blocking)
1. **`materialize` also throws `ClosedException`.** The new handlers sit only on producer paths, so a driver-thread `materialize` after close still fails as before. That seems right, but the `ClosedException` Javadoc only mentions `register`. A one-line note would stop someone later widening the catch.
2. **Catch scope in `registerExtractorFromProducer`.** It catches `Exception` and closes the extractor, which also covers the id-space-exhaustion `IllegalStateException`. That is correct. Narrowing to `RuntimeException` would be slightly more precise, but `register` has no checked exceptions, so this is cosmetic.
3. **Iterator release in `advanceToNextUnit`.** The new comment says "the open paths already released the iterator". The tests assert extractor closure, but I see no assertion that the page iterator itself is closed on this path. Consider asserting that on the `ProducerIterator`, or confirming it in the code.
4. **Dependence on shutdown ordering.** `isRegistryClosedAfterBufferFinished` assumes the registry is only closed after the buffer has finished. The Javadoc states this, but it isn't enforced anywhere. If `Driver` or `ExternalFieldExtractOperator` close ordering changes, the symptom would be a failing query again, which is loud and therefore safe. A short comment at the `registry.close()` call site pointing to this invariant would help.
5. **Test style.** The `FormatReader_RowPositionEmitting` underscore name already existed. `runWithDriverFinishingWhileOpening` is long and does a lot, and the `FinishDuringOpen` record doubles as a helper object. That is acceptable for a test, but splitting setup from the trigger hook would read more easily.
6. **Backport hygiene.** The PR is labeled `>non-issue` and `auto-merge-without-approval`, which is fine for a clean cherry-pick. It adds no transport or serialization changes, so no transport version is needed. I saw no entitlement or dependency changes.

## Verdict
This is a correct and well-scoped fix. The failure-mode asymmetry is deliberate: a real wiring bug still fails loudly. Test coverage is thorough, and the remaining notes are documentation-level suggestions.

# REVIEW B

**Review of #163196, the 9.6 backport of #163128 (ES|QL|DS: end source quietly on closed registry)**

The PR is already merged. I read the diff only and didn't build it or run any tests. Overall it looks good.

**What it does**
- `SourceExtractors.register` and `materialize` now throw a dedicated `ClosedException`. It extends `IllegalStateException`, so existing catchers still work.
- `AsyncExternalSourceOperatorFactory` treats that exception as an expected shutdown race, but only when `buffer.noMoreInputs()` is true. That means the driver closed the source before the registry closed.
- A closed registry with a live buffer still fails the query, so results can't be silently truncated.
- `registerExtractorFromProducer` now closes the extractor if registration fails. This also fixes a leak, and the close happens outside the registry monitor.

**Code quality**
- The `isRegistryClosedAfterBufferFinished` guard is well designed. Requiring the buffer to be finished is the right way to avoid masking wiring bugs.
- The DEBUG log is cheap, since the message is constant and has no concatenation. That matches the logging guidance in CLAUDE.md.
- `ClosedException` extends `IllegalStateException`, so it stays source-compatible. Its constructor is package-private, which is appropriate.
- The Javadoc says why, not how. The `ColumnExtractorProducer` contract note, that `close()` must not depend on registration, is a useful addition.

**Potential issues (minor)**
1. `registerExtractorFromProducer` catches `Exception` and closes the extractor on any registration failure, including id-space exhaustion. That is correct, since the extractor is unreferenced in both cases. Catching `RuntimeException` would be slightly more precise, but it isn't a problem as written.
2. `ClosedException` can also come from `materialize`. The new catch sites sit on the producer side. That is fine, but the extract-operator side should still surface the exception as a failure. The existing `testMaterializeAfterCloseFails` covers it.
3. `advanceToNextUnit` relies on the comment "the open paths already released the iterator". I couldn't confirm that from the diff alone. The test's `assertClosedUnregisteredExtractor` checks the extractor, not the page iterator. If any open path doesn't release the iterator, the new catch would leak it. It's worth a quick check.

**Performance**
There is no hot-path change. The only additions are a `try/catch` and an `instanceof` check on the failure paths.

**Security**
There are no concerns.

**Tests**
- Coverage is thorough. It exercises all four open modes (slice queue, multi-file, sync single file, native async single file) in both directions: finished buffer ends quietly, live buffer still fails.
- It checks that each extractor is closed exactly once, that none is closed under the registry monitor, that `removeAsyncAction` is called exactly once, and that no further unit is opened after the registry closes.
- `SourceExtractorsTests` now asserts the exception type and that the registry never closes an extractor it rejected.
- `DriverContext` is mocked, and the test comment explains why. That follows the repo's guidance on documenting mocks.
- Nit: `testProducerEndsQuietlyWhenDriverFinishesWhileOpeningNextUnit` loops over modes inside one test method. A failure message includes the mode, so this is acceptable. Separate methods or `randomFrom` would make failures easier to reproduce by seed.
- The test relies on a hook inside `FormatReader.read` to simulate the race deterministically. That avoids flakiness.

**Backport**
The diff is self-contained, touches only x-pack ES|QL, and has no transport or wire changes. It is labeled `>non-issue` and `v9.6.1`, which fits.

**Verdict:** Approve. The only follow-up I'd suggest is confirming point 3.
