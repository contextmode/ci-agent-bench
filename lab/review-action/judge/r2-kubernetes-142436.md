# PR diff (the real change)

```diff
diff --git a/staging/src/k8s.io/kubectl/pkg/cmd/label/label.go b/staging/src/k8s.io/kubectl/pkg/cmd/label/label.go
index 1d16f9aee43e1..5c17f6fe9dc88 100644
--- a/staging/src/k8s.io/kubectl/pkg/cmd/label/label.go
+++ b/staging/src/k8s.io/kubectl/pkg/cmd/label/label.go
@@ -317,7 +317,7 @@ func (o *LabelOptions) RunLabel() error {
 			}
 			for _, label := range o.removeLabels {
 				if _, ok := accessor.GetLabels()[label]; !ok {
-					fmt.Fprintf(o.Out, "label %q not found.\n", label)
+					fmt.Fprintf(o.ErrOut, "label %q not found.\n", label)
 				}
 			}
 
diff --git a/staging/src/k8s.io/kubectl/pkg/cmd/label/label_test.go b/staging/src/k8s.io/kubectl/pkg/cmd/label/label_test.go
index 1485dd650e771..7c34501a4f193 100644
--- a/staging/src/k8s.io/kubectl/pkg/cmd/label/label_test.go
+++ b/staging/src/k8s.io/kubectl/pkg/cmd/label/label_test.go
@@ -31,6 +31,7 @@ import (
 	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
 	"k8s.io/apimachinery/pkg/runtime"
 	"k8s.io/apimachinery/pkg/runtime/schema"
+	"k8s.io/apimachinery/pkg/util/yaml"
 	"k8s.io/cli-runtime/pkg/genericiooptions"
 	"k8s.io/cli-runtime/pkg/resource"
 	"k8s.io/client-go/rest/fake"
@@ -643,12 +644,14 @@ func TestRunLabelMsg(t *testing.T) {
 	tf.ClientConfigVal = cmdtesting.DefaultClientConfig()
 
 	testCases := []struct {
-		name          string
-		args          []string
-		overwrite     bool
-		dryRun        string
-		expectedOut   string
-		expectedError error
+		name           string
+		args           []string
+		overwrite      bool
+		dryRun         string
+		output         string
+		expectedOut    string
+		expectedErrOut string
+		expectedError  error
 	}{
 		{
 			name:        "set new label",
@@ -672,11 +675,36 @@ func TestRunLabelMsg(t *testing.T) {
 			expectedOut: "pod/foo unlabeled\n",
 		},
 		{
-			name: "unset nonexisting label",
-			args: []string{"pods/foo", "foo-"},
-			expectedOut: `label "foo" not found.
-pod/foo not labeled
-`,
+			name:           "unset nonexisting label",
+			args:           []string{"pods/foo", "foo-"},
+			expectedOut:    "pod/foo not labeled\n",
+			expectedErrOut: "label \"foo\" not found.\n",
+		},
+		{
+			name:           "unset nonexisting label with name output",
+			args:           []string{"pods/foo", "foo-"},
+			output:         "name",
+			expectedOut:    "pod/foo\n",
+			expectedErrOut: "label \"foo\" not found.\n",
+		},
+		{
+			name:           "unset nonexisting label with JSON output",
+			args:           []string{"pods/foo", "foo-"},
+			output:         "json",
+			expectedErrOut: "label \"foo\" not found.\n",
+		},
+		{
+			name:           "unset nonexisting label with YAML output",
+			args:           []string{"pods/foo", "foo-"},
+			output:         "yaml",
+			expectedErrOut: "label \"foo\" not found.\n",
+		},
+		{
+			name:           "unset nonexisting label with server dry run",
+			args:           []string{"pods/foo", "foo-"},
+			dryRun:         "server",
+			expectedOut:    "pod/foo not labeled (server dry run)\n",
+			expectedErrOut: "label \"foo\" not found.\n",
 		},
 		{
 			name:        "set new label with server dry run",
@@ -706,14 +734,18 @@ pod/foo not labeled
 
 	for _, tc := range testCases {
 		t.Run(tc.name, func(t *testing.T) {
-			iostreams, _, bufOut, _ := genericiooptions.NewTestIOStreams()
+			iostreams, _, bufOut, bufErr := genericiooptions.NewTestIOStreams()
 			cmd := NewCmdLabel(tf, iostreams)
 			cmd.SetOut(bufOut)
-			cmd.SetErr(bufOut)
+			cmd.SetErr(bufErr)
 			if tc.dryRun != "" {
 				cmd.Flags().Set("dry-run", tc.dryRun)
 			}
 			options := NewLabelOptions(iostreams)
+			if err := cmd.Flags().Set("output", tc.output); err != nil {
+				t.Fatal(err)
+			}
+			*options.PrintFlags.OutputFormat = tc.output
 			if tc.overwrite {
 				options.overwrite = true
 			}
@@ -737,7 +769,25 @@ pod/foo not labeled
 				}
 			}
 
-			if bufOut.String() != tc.expectedOut {
+			if bufErr.String() != tc.expectedErrOut {
+				t.Errorf("unexpected stderr (-want +got):\n%s", cmp.Diff(tc.expectedErrOut, bufErr.String()))
+			}
+			if tc.output == "json" || tc.output == "yaml" {
+				decoder := yaml.NewYAMLOrJSONDecoder(bufOut, 4096)
+				var pod v1.Pod
+				if err := decoder.Decode(&pod); err != nil {
+					t.Fatalf("decode %s output: %v", tc.output, err)
+				}
+				if pod.Name != "foo" || pod.Namespace != "test" {
+					t.Errorf("expected pod test/foo, got %s/%s", pod.Namespace, pod.Name)
+				}
+				if diff := cmp.Diff(map[string]string{"existing": "abc"}, pod.Labels); diff != "" {
+					t.Errorf("unexpected labels (-want +got):\n%s", diff)
+				}
+				if err := decoder.Decode(&v1.Pod{}); err != io.EOF {
+					t.Errorf("expected end of output, got %v", err)
+				}
+			} else if bufOut.String() != tc.expectedOut {
 				t.Fatalf("wrong output\ngot:\n%s\nexpected:\n%s\n", bufOut.String(), tc.expectedOut)
 			}
 		})

```

# REVIEW A

**Review of #142436: kubectl: write missing label warnings to stderr**

The PR is already merged. I'm reviewing the diff as written. It's a small, correct fix, and I found nothing that blocks it.

**Fix (`label.go:320`)**
- Changing `o.Out` to `o.ErrOut` is the right fix. It keeps `-o json` and `-o yaml` output parseable when piped.
- The change is a single line, which keeps the PR focused.
- The `label "x" not found.` message is still specific and actionable. Nothing else in `RunLabel` writes diagnostics to `o.Out`.

**Behavior change**
- Anything that scraped the "not found" text from stdout will now miss it. That's the intended trade-off, and the release note says so.
- Existing `kubectl label` integration or e2e scripts that grep stdout for this message are the only place this could break. I didn't search for any.

**Tests**
- The new cases cover default, name, JSON, YAML and server dry-run output. Decoding the JSON/YAML and checking for `io.EOF` is a good way to prove stdout holds exactly one object.
- Nits, none blocking:
  - `cmd.Flags().Set("output", tc.output)` runs even when `tc.output` is empty. Setting an empty value is harmless, but the test sets the flag on `cmd` and also writes `*options.PrintFlags.OutputFormat` directly. `options` comes from a separate `NewLabelOptions` call, so the second line looks redundant or confusing. Check whether the direct write is needed. If it is, a comment saying why would help.
  - The JSON and YAML cases leave `expectedOut` unset, because the decode branch skips the string comparison. That's fine, but a short comment would stop someone from adding an `expectedOut` that never gets checked.
  - Swapping `cmd.SetErr(bufOut)` for `bufErr` is correct. It also means any cobra-level errors no longer land in the stdout assertion.
  - The added `yaml` import is `k8s.io/apimachinery/pkg/util/yaml`, which is already in staging, so there's no dependency concern.

**Other concerns**
- Performance: none.
- Security: none.
- Process: the AI disclosure is present, as `AGENTS.md` requires. The description claims the new tests fail before the fix. That fits the diff, though I didn't re-run it.

**Verdict:** LGTM.

# REVIEW B

**Review of #142436: kubectl: write missing label warnings to stderr**

The PR is already merged. The fix is correct and I'd have approved it.

**Fix**

- `label.go:320` changes `o.Out` to `o.ErrOut` for the `label %q not found.` message. That is the right stream for a diagnostic. It also stops the text from landing ahead of the JSON or YAML document in `-o json` and `-o yaml` output.
- The change is minimal, and nothing else in `RunLabel` writes diagnostics to `Out`.
- **Behavior change:** scripts that grep stdout for `not found.` will stop matching. The release note covers this, so I think it is acceptable.

**Tests**

- The new cases cover default, `name`, JSON, YAML and server dry-run output.
- The JSON/YAML cases decode stdout and then check for `io.EOF`. That check catches stray trailing output as well as the leading text this PR fixes.
- `cmd.SetErr(bufErr)` replaces `cmd.SetErr(bufOut)`. Previously cobra errors went to the stdout buffer and could mask this kind of bug.

**Nits (non-blocking)**

1. In the test loop, `cmd.Flags().Set("output", tc.output)` and `*options.PrintFlags.OutputFormat = tc.output` do the same job on two different objects. A short comment on why both are needed would help. If one is redundant, drop it.
2. The `else if bufOut.String() != tc.expectedOut` branch uses `t.Fatalf`, while the new stderr check uses `t.Errorf`. The mix is harmless, but it is inconsistent.
3. The JSON and YAML cases don't set `expectedOut`. That is fine because they are decoded instead of compared as strings, but a short comment would make the intent obvious.
4. The test only covers removal of a missing label. Removing a mix of present and missing labels (`a- missing-`) would confirm that only the missing one is reported. I don't think that blocks anything.

**Other concerns**

- **Security and performance:** none.
- **AI disclosure:** the PR description includes it, as `AGENTS.md` requires.
- **Reminder for the author:** they are responsible for everything they submit. See `CONTRIBUTING.md`.
