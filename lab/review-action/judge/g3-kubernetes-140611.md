# PR diff (the real change)

```diff
diff --git a/test/integration/scheduler_perf/podgroup/tas/performance-config.yaml b/test/integration/scheduler_perf/podgroup/tas/performance-config.yaml
index 4b429331e5b30..842617db1e84f 100644
--- a/test/integration/scheduler_perf/podgroup/tas/performance-config.yaml
+++ b/test/integration/scheduler_perf/podgroup/tas/performance-config.yaml
@@ -56,6 +56,10 @@
       CompositePodGroup: true
   - name: 5000Nodes_750Gangs_3000Pods
     labels: [performance]
+    # SLO: minimum pod scheduling throughput (pods/sec, SchedulingThroughput average).
+    # Calibrated from a benchmark run (adaptive ~630 pods/sec vs ~113 with the limit disabled);
+    # set well above the no-limit baseline and below normal variance to catch a real regression.
+    threshold: 400
     params:
       initNodes: 5000
       initPodGroups: 750
@@ -70,6 +74,8 @@
       CompositePodGroup: true
   - name: 5000Nodes_1500Gangs_6000Pods
     labels: [performance]
+    # Calibrated (adaptive ~574 pods/sec vs ~111 with the limit disabled).
+    threshold: 350
     params:
       initNodes: 5000
       initPodGroups: 1500
@@ -84,6 +90,8 @@
       CompositePodGroup: true
   - name: 5000Nodes_2250Gangs_9000Pods
     labels: [performance]
+    # Calibrated (adaptive ~547 pods/sec vs ~109 with the limit disabled).
+    threshold: 350
     params:
       initNodes: 5000
       initPodGroups: 2250
@@ -98,6 +106,8 @@
       CompositePodGroup: true
   - name: 5000Nodes_3Gangs_3000Pods_1000PerGroup
     labels: [performance]
+    # Calibrated (adaptive ~975 pods/sec vs ~224 with the limit disabled).
+    threshold: 550
     params:
       initNodes: 5000
       initPodGroups: 3
@@ -112,6 +122,9 @@
       CompositePodGroup: true
   - name: 5000Nodes_6Gangs_6000Pods_1000PerGroup
     labels: [performance]
+    # Calibrated (adaptive ~625 pods/sec vs ~139 with the limit disabled); conservative due to
+    # higher run-to-run variance on the low-gang-count workloads.
+    threshold: 350
     params:
       initNodes: 5000
       initPodGroups: 6
@@ -126,6 +139,9 @@
       CompositePodGroup: true
   - name: 5000Nodes_9Gangs_9000Pods_1000PerGroup
     labels: [performance]
+    # Calibrated (adaptive ~642 pods/sec vs ~132 with the limit disabled); conservative due to
+    # higher run-to-run variance on the low-gang-count workloads.
+    threshold: 350
     params:
       initNodes: 5000
       initPodGroups: 9
@@ -139,4 +155,76 @@
     featureGates:
       CompositePodGroup: true
 
-
+# Baseline for measuring the performance impact of the adaptive placement limit. This test case mirrors
+# the TopologyAwareScheduling workloads but disables the limit (percentageOfPlacementsToScore: 100), so
+# every generated placement is scored. Comparing its throughput against TopologyAwareScheduling shows
+# the impact of the limit.
+- name: TopologyAwareSchedulingScoreAllPlacements
+  featureGates:
+    GenericWorkload: true
+    TopologyAwareWorkloadScheduling: true
+  schedulerConfigPath: scheduler-config-score-all-placements.yaml
+  workloadTemplate:
+  - opcode: createNodes
+    countParam: $initNodes
+    nodeTemplatePath: templates/node.yaml
+  - opcode: createNamespaces
+    prefix: tas-ns
+    count: 1
+  - opcode: createPodGroups
+    countParam: $initPodGroups
+    namespace: tas-ns-0
+    templatePath: templates/podgroup.yaml
+    templateParams:
+      podsPerGroup: $podsPerGroup
+  - opcode: createPods
+    countParam: $initPodGroups
+    countMultiplierParam: $podsPerGroup
+    namespace: tas-ns-0
+    podTemplatePath: templates/gang-pod.yaml
+    collectMetrics: true
+    templateParams:
+      podsPerGroup: $podsPerGroup
+  workloads:
+  - name: 10Nodes_3Gangs
+    labels: [integration-test, short]
+    params:
+      initNodes: 10
+      initPodGroups: 3
+      podsPerGroup: 3
+  - name: 5000Nodes_750Gangs_3000Pods
+    labels: [performance]
+    params:
+      initNodes: 5000
+      initPodGroups: 750
+      podsPerGroup: 4
+  - name: 5000Nodes_1500Gangs_6000Pods
+    labels: [performance]
+    params:
+      initNodes: 5000
+      initPodGroups: 1500
+      podsPerGroup: 4
+  - name: 5000Nodes_2250Gangs_9000Pods
+    labels: [performance]
+    params:
+      initNodes: 5000
+      initPodGroups: 2250
+      podsPerGroup: 4
+  - name: 5000Nodes_3Gangs_3000Pods_1000PerGroup
+    labels: [performance]
+    params:
+      initNodes: 5000
+      initPodGroups: 3
+      podsPerGroup: 1000
+  - name: 5000Nodes_6Gangs_6000Pods_1000PerGroup
+    labels: [performance]
+    params:
+      initNodes: 5000
+      initPodGroups: 6
+      podsPerGroup: 1000
+  - name: 5000Nodes_9Gangs_9000Pods_1000PerGroup
+    labels: [performance]
+    params:
+      initNodes: 5000
+      initPodGroups: 9
+      podsPerGroup: 1000
diff --git a/test/integration/scheduler_perf/podgroup/tas/scheduler-config-score-all-placements.yaml b/test/integration/scheduler_perf/podgroup/tas/scheduler-config-score-all-placements.yaml
new file mode 100644
index 0000000000000..077ead257dcac
--- /dev/null
+++ b/test/integration/scheduler_perf/podgroup/tas/scheduler-config-score-all-placements.yaml
@@ -0,0 +1,6 @@
+apiVersion: kubescheduler.config.k8s.io/v1
+kind: KubeSchedulerConfiguration
+# Disable the placement limit by scoring every generated placement. Used as the baseline to measure
+# the performance impact of the adaptive placement limit (which the default TopologyAwareScheduling
+# test case exercises).
+percentageOfPlacementsToScore: 100

```

# REVIEW A

**Review of PR 140611: scheduler-perf baseline and draft SLOs for the TAS placement limit**

The PR is already merged. It's a small, test-only change, and the approach is sound. I have one possible correctness issue and a few nits.

**Possible issue: missing `CompositePodGroup` gate in the baseline**
- Every `5000Nodes_*` workload in the existing `TopologyAwareScheduling` case sets `featureGates: CompositePodGroup: true`.
- The new `TopologyAwareSchedulingScoreAllPlacements` workloads don't set it.
- If that gate changes the code path, such as how gangs are scheduled, the comparison isn't like-for-like. The reported ~5x speedup would then include a gate effect, not just the placement limit.
- If the gate doesn't matter, a short comment saying so would help.
- Only the 10-node smoke test runs in presubmit, so this wouldn't show up in CI.
- I only had the diff, so I couldn't check which gate set the existing workloads use or what the gate changes.

**Thresholds**
- The thresholds are 350–550 pods/sec against measured adaptive throughput of 492–975. That is 55–71% of measured, not a uniform ~60% as the description says.
- The 750-gang threshold of 400 is about 71% of its low observation (562), and 550 for 3 gangs is about 56% of its low observation (953). Neither is a problem, and both sit well above the baseline. The description is just slightly loose.
- They are fixed absolute numbers calibrated from two runs on one CI environment. If CI hardware changes, they may flake or stop catching regressions. Tracking them against a trend would be more robust, but absolute thresholds are the usual convention in scheduler-perf.
- The 3-gang baseline ranged 67–224. That is wide enough that the threshold-to-baseline margin is only meaningful against the upper end. The comments cite ~224, which is fine.
- The comments hard-code measured numbers, such as "adaptive ~630 vs ~113". These will go stale and are already in the PR description. Keeping just the "why" would age better.

**Maintainability**
- The new test case copies the whole workload template and parameter matrix from `TopologyAwareScheduling`. The two will drift if one changes. If scheduler-perf supports YAML anchors or a shared template, using them would help. Otherwise a comment saying the two must stay in sync would do.
- The baseline has no thresholds, which is stated and intentional. It is not gated, so it measures only.
- The scheduler config file sets only `percentageOfPlacementsToScore: 100`, which is fine. The added comment explains why it exists.
- The PR also removes a trailing blank line at EOF. That's harmless.

**Security and performance**
- No product code is touched, so there are no security or runtime performance concerns.
- Running the baseline in the 5000-node job adds scheduler-perf time. Even at ~110 pods/sec, 9000 pods take about 80 seconds per workload, so that is acceptable.

**Test coverage**
- The 10-node smoke test runs the new config path in presubmit. That confirms the config loads and the case runs, though not that the limit is actually disabled.
- Nothing checks that `percentageOfPlacementsToScore: 100` really scores all placements. The throughput gap in the results is the only evidence.

# REVIEW B

**Review of PR 140611: scheduler-perf baseline and draft SLOs for the TAS placement limit**

The PR is already merged. I read the diff and checked the config field against the repo. The change is small and focused, and I found no blocking issues.

**What's good**
- `percentageOfPlacementsToScore` is a real top-level `KubeSchedulerConfiguration` field (`staging/src/k8s.io/kube-scheduler/config/v1/types.go:86`). The new YAML config is valid.
- The baseline test mirrors the existing workloads, so the two can be compared directly.
- Only `10Nodes_3Gangs` carries the `integration-test` label, so the 5000-node baseline stays out of presubmit.
- The comments explain why each threshold is set where it is.
- The PR description includes measurements, which makes the thresholds easy to check.

**Issues and suggestions**
1. **Missing feature gate (possible mismatch with the original test).** The original `TopologyAwareScheduling` workloads set `featureGates: CompositePodGroup: true`. The diff context shows that gate on the 5000-node workloads, though I didn't check whether it also covers the 10-node one.
   - The new test sets no per-workload gate. If `templates/podgroup.yaml` or `gang-pod.yaml` relies on `CompositePodGroup`, the baseline is not measuring the same thing as the adaptive runs.
   - Please confirm the gate is intentionally omitted. If it isn't intentional, add it.
2. **Thresholds are loose for the 1000-per-group workloads.**
   - 5000Nodes_3Gangs: the threshold is 550 and the measured range is 953-975. The ~60% rule would give about 580, so 550 is actually the tighter of the two.
   - 6Gangs and 9Gangs: the threshold is 350 against measured values of 615-642, which is about 55%.
   - All thresholds sit well above the no-limit baseline (≈110-224 pods/s), so they will catch a loss of the limit. A partial regression, such as scoring 20 of 50 racks, could still pass.
   - The 3Gangs baseline range (67-224) is very noisy. A 224 pods/s run is about 40% of the 550 threshold, so that threshold is safe. Don't treat 224 as a stable baseline figure.
3. **Calibration is thin.** The thresholds come from only two CI runs. The PR title says "draft SLOs", so this is acceptable. After a few weeks of periodic runs, revisit them and drop the "draft" label.
4. **Duplication.** The new test case copies about 70 lines of the workload definitions. Parameter changes to one now have to be made in the other too. YAML anchors would reduce this, but I haven't checked that scheduler-perf's loader handles them. A comment in each block pointing to the other would be a cheap fix.
5. **Comment style.** The comments in `performance-config.yaml` describe how the thresholds were calibrated. That's fine, but "adaptive ~630" in the first comment doesn't match the "562-630" range in the PR table. Use the same figure everywhere.
6. **Trailing whitespace.** The diff removes a blank line at the end of the file, which is a harmless cleanup.

**Security and performance:** Neither applies. This only touches test config, and the baseline runs only in the perf job.

**Test coverage:** The 10-node smoke workload exercises the new config path in presubmit. The `threshold` values are only enforced in the perf job.

**Process:** Per `AGENTS.md`, the PR description should disclose whether AI was used. I didn't see that. The author remains responsible for all submitted changes (see `CONTRIBUTING.md`).

**Verdict:** LGTM. Item 1 is the one worth confirming, and the rest are nits.
