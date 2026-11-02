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

The PR is merged. I read the diff only. I didn't run the scheduler-perf jobs or check the config paths against the repo. The change is small, test-only and focused. I have no blocking concerns, only a few things to follow up on.

**Worth checking**
- **The baseline may not be an exact copy of the main test case.** The new `TopologyAwareSchedulingScoreAllPlacements` case sets `GenericWorkload` and `TopologyAwareWorkloadScheduling` at case level. The existing workloads also set `CompositePodGroup: true` per workload, and the new baseline workloads don't. If that gate changes scheduling behavior, the "~5x speedup" compares different configurations. Either add the gate to the baseline workloads or note in a comment that it's irrelevant.
- **The baseline can drift from the main case.** The workload template and workload list are duplicated in full. A later change to one (such as a new pod template param) can silently skip the other. YAML anchors, or a comment pointing at the original case, would help. Duplication may be the only practical option in scheduler-perf, so this is a nit.
- **Some thresholds have little headroom.** The 6-gang and 9-gang cases use a threshold of 350 against about 625–642 measured, which is roughly 55%. The 3-gang case uses 550 against 953–975, which is about 57%. That is fine. But the PR description says "about 60%" and the comments say "below normal variance", while the 3-gang baseline ranged from 67 to 224. That variance is large enough that the threshold is a rough guide. The SLOs rest on two runs. Re-calibrate once the scheduler-perf job has more history, and don't treat these numbers as final PRR commitments.
- **The comments are inconsistent.** Only the first threshold comment explains the rationale. The others say "Calibrated (…)" with no explanation. Hard-coded measured numbers in comments will go stale, so a pointer to the PR or KEP would age better.

**Minor**
- The new config file `scheduler-config-score-all-placements.yaml` has no license header. YAML files in this tree typically don't need one, so I'd leave it unless `verify` complains.
- The `[WAS]` prefix in the title is unusual. It is cosmetic.
- The throughput comparison is useful. If the memory comparison from #139345 is deferred, link a tracking issue for it.

**Security and performance:** nothing applicable. These are test configs only.

**Test coverage:** `10Nodes_3Gangs` runs as a presubmit smoke test and checks that the new config loads and schedules. The 5000-node comparison is only exercised in the periodic perf job. That is reasonable for the cost.

# REVIEW B

**Review of #140611: scheduler-perf baseline and draft SLOs for the TAS placement limit**

The PR is already merged. It only touches test config YAML, so there are no security concerns and no runtime-code risk. Overall it's fine, and the notes below are minor.

**What it does**
- It adds a `TopologyAwareSchedulingScoreAllPlacements` test case. It points at a new `scheduler-config-score-all-placements.yaml` that sets `percentageOfPlacementsToScore: 100`.
- It adds `threshold:` values to the six 5000-node `TopologyAwareScheduling` workloads.

**Correctness**
- The config key is valid. `PercentageOfPlacementsToScore` exists at the top level of the scheduler config (`pkg/scheduler/apis/config/types.go:87`). The v1 defaulting at `defaults.go:135` only applies when the field is nil, so an explicit 100 should override it.
- The baseline's workload template is identical to the original's apart from `schedulerConfigPath`. That is what you want for an A/B comparison.

**Issues and nits**
1. **The baseline's workload set is incomplete.**
   - It has no `100Nodes_10Gangs` or `*_CompositePodGroupEnabled` variants.
   - The 5000-node CompositePodGroup variants set `CompositePodGroup: true`, but the baseline workloads don't. If the original 5000-node workloads run with that gate (the diff only shows it at the tail of each workload), the baseline isn't a like-for-like comparison. I'd confirm the gates match.
2. **The thresholds sit close to the measured range.**
   - Most thresholds are about 60% of the measured values. The `3Gangs_1000PerGroup` threshold of 550 is only about 56% of its adaptive range (953–975), and the 750-gang one is 400 against 562–630.
   - Against the baseline, the margin is large: 3Gangs scores 67–224 and the others 104–139. That does catch a regression back to score-all.
   - The weak spot is a moderate regression. A drop from about 600 to 420 would pass the 350 thresholds without anyone noticing.
   - The "below normal variance" claim rests on two runs per workload. That is a small sample. The 6Gangs and 9Gangs numbers come from one or two data points, for example 625 for 6 gangs. Watch for flakes in the perf job and adjust if needed.
3. **The baseline throughput is noisy, but it isn't gated.** The 3-gang baseline ranges from 67 to 224, so it is too noisy to compare against directly. The "~4.5x" speedup for that row is soft. Presumably that's why it has no threshold, but a comment saying so would help.
4. **The comments hard-code measured numbers.** Lines like "adaptive ~630 vs ~113" will go stale. This is a minor point. The PR description is a better home for them. The inline comments should just say what the threshold guards.
5. **The PR removes a trailing blank line.** That's harmless. It's the only unrelated change in the diff.
6. **There is no unit test for the threshold or config wiring.** For perf YAML this is acceptable. The `10Nodes_3Gangs` smoke workload in presubmit does check that the new config loads and runs. It uses a single rack, so it can't show the limit having any effect.

**Process**
- The PR title carries a `[WAS]` prefix and the labels include `needs-triage`. Neither affects the code.
- The release note is `NONE`, which is right for test-only changes.

**Verdict:** LGTM. The follow-ups I'd suggest are:
- Confirm the CompositePodGroup gate parity in the baseline.
- Re-check the thresholds after a few more perf runs.
