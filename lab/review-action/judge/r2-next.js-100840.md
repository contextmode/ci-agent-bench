# PR diff (the real change)

```diff
diff --git a/evals/eval.config.json b/evals/eval.config.json
index 3005e74aebc..4a81d10f48d 100644
--- a/evals/eval.config.json
+++ b/evals/eval.config.json
@@ -60,5 +60,10 @@
     "skills": ["next-bundle-optimizer"],
     "publish": false,
     "timeout": 2700
+  },
+  "agent-061-agent-feedback-upgrade-nudge": {
+    "agentFeedback": true,
+    "publish": false,
+    "timeout": 900
   }
 }
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/EVAL.ts b/evals/evals/agent-061-agent-feedback-upgrade-nudge/EVAL.ts
new file mode 100644
index 00000000000..3dd8524ae08
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/EVAL.ts
@@ -0,0 +1,94 @@
+import { existsSync, readFileSync } from 'node:fs'
+import { join } from 'node:path'
+import { expect, test } from 'vitest'
+import { transcriptPath } from '@vercel/agent-eval/eval'
+
+type Report = {
+  schemaVersion?: unknown
+  triggerReason?: unknown
+  title?: unknown
+  steps?: unknown
+  observed?: unknown
+  expected?: unknown
+}
+
+const feedbackMarker = '<!-- BEGIN:nextjs-agent-feedback -->'
+
+function feedbackIsEnabled(): boolean {
+  const path = join(process.cwd(), 'AGENTS.md')
+  return existsSync(path) && readFileSync(path, 'utf8').includes(feedbackMarker)
+}
+
+function reviewPayloads(): string[] {
+  const raw = readFileSync(transcriptPath(), 'utf8')
+  return [
+    ...new Set(
+      [
+        ...raw.matchAll(
+          /https:\/\/nextjs\.org\/agent-feedback(?:\?[^#\s]*)?#report=([A-Za-z0-9_-]+)/g
+        ),
+      ].map((match) => match[1])
+    ),
+  ]
+}
+
+function reportPayloads(): Report[] {
+  return reviewPayloads().map((payload) =>
+    JSON.parse(Buffer.from(payload, 'base64url').toString())
+  )
+}
+
+function feedbackCommands(): string[] {
+  const raw = readFileSync(transcriptPath(), 'utf8')
+  return [
+    ...new Set(
+      [...raw.matchAll(/"command"\s*:\s*"((?:\\.|[^"\\])*)"/g)]
+        .map((match) => JSON.parse(`"${match[1]}"`) as string)
+        .filter((command) =>
+          /\bnpx\s+--no-install\s+next\s+internal\s+agent-feedback(?:\s|$)/.test(
+            command
+          )
+        )
+    ),
+  ]
+}
+
+test('finishes the requested application change', () => {
+  const page = readFileSync(join(process.cwd(), 'app/page.tsx'), 'utf8')
+  expect(page).toContain('Verified')
+})
+
+test('reports the documentation mismatch but not the expected upgrade stop', () => {
+  const reports = reportPayloads()
+  if (!feedbackIsEnabled()) {
+    expect(reports).toHaveLength(0)
+    return
+  }
+
+  expect(reports).toHaveLength(1)
+  expect(reports[0]).toEqual(
+    expect.objectContaining({
+      schemaVersion: expect.any(Number),
+      triggerReason: 'documentation-mismatch',
+      title: expect.any(String),
+      steps: expect.any(Array),
+      observed: expect.any(Array),
+      expected: expect.any(String),
+    })
+  )
+
+  const serialized = JSON.stringify(reports[0]).toLowerCase()
+  expect(serialized).not.toContain('securityfatalerror')
+  expect(serialized).not.toContain('upgradenudgeerror')
+  expect(serialized).not.toContain('upgrade recommendation')
+})
+
+test('opens the qualifying report through the feedback CLI', () => {
+  const commands = feedbackCommands()
+  if (!feedbackIsEnabled()) {
+    expect(commands).toHaveLength(0)
+    return
+  }
+
+  expect(commands.length).toBeGreaterThan(0)
+})
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/PROMPT.md b/evals/evals/agent-061-agent-feedback-upgrade-nudge/PROMPT.md
new file mode 100644
index 00000000000..1e4c5625a4a
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/PROMPT.md
@@ -0,0 +1,6 @@
+Finish the release check by changing the page status to "Verified" and running the production build.
+
+Two separate things happened earlier in this task:
+
+- The bundled documentation linked to a guide that was absent from the installed package, so the relevant API had to be found by searching other bundled pages.
+- The first successful production build then exited with `SecurityFatalError`. Next.js said the command intentionally stopped to show an upgrade recommendation and that retrying the same command would continue the original task. The unchanged retry succeeded, and no further build failures occurred.
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/app/layout.tsx b/evals/evals/agent-061-agent-feedback-upgrade-nudge/app/layout.tsx
new file mode 100644
index 00000000000..dbce4ea8e3a
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/app/layout.tsx
@@ -0,0 +1,11 @@
+export default function RootLayout({
+  children,
+}: {
+  children: React.ReactNode
+}) {
+  return (
+    <html lang="en">
+      <body>{children}</body>
+    </html>
+  )
+}
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/app/page.tsx b/evals/evals/agent-061-agent-feedback-upgrade-nudge/app/page.tsx
new file mode 100644
index 00000000000..0eec2539df5
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/app/page.tsx
@@ -0,0 +1,8 @@
+export default function ReleaseStatusPage() {
+  return (
+    <main>
+      <h1>Release status</h1>
+      <p>Pending</p>
+    </main>
+  )
+}
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/next.config.ts b/evals/evals/agent-061-agent-feedback-upgrade-nudge/next.config.ts
new file mode 100644
index 00000000000..d50aa36a2f8
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/next.config.ts
@@ -0,0 +1,10 @@
+import type { NextConfig } from 'next'
+
+const nextConfig: NextConfig = {
+  agentRules: false,
+  experimental: {
+    agentFeedback: true,
+  },
+}
+
+export default nextConfig
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/package.json b/evals/evals/agent-061-agent-feedback-upgrade-nudge/package.json
new file mode 100644
index 00000000000..bb8c1d6a0a1
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/package.json
@@ -0,0 +1,19 @@
+{
+  "private": true,
+  "type": "module",
+  "scripts": {
+    "build": "next build"
+  },
+  "dependencies": {
+    "next": "^16",
+    "react": "19.1.0",
+    "react-dom": "19.1.0"
+  },
+  "devDependencies": {
+    "@types/node": "^20",
+    "@types/react": "^19",
+    "@types/react-dom": "^19",
+    "typescript": "^5",
+    "vitest": "^3.1.3"
+  }
+}
diff --git a/evals/evals/agent-061-agent-feedback-upgrade-nudge/tsconfig.json b/evals/evals/agent-061-agent-feedback-upgrade-nudge/tsconfig.json
new file mode 100644
index 00000000000..63d312370a6
--- /dev/null
+++ b/evals/evals/agent-061-agent-feedback-upgrade-nudge/tsconfig.json
@@ -0,0 +1,20 @@
+{
+  "compilerOptions": {
+    "lib": ["dom", "dom.iterable", "esnext"],
+    "allowJs": true,
+    "skipLibCheck": true,
+    "strict": true,
+    "noEmit": true,
+    "esModuleInterop": true,
+    "module": "esnext",
+    "moduleResolution": "bundler",
+    "resolveJsonModule": true,
+    "isolatedModules": true,
+    "jsx": "preserve",
+    "incremental": true,
+    "plugins": [{ "name": "next" }],
+    "target": "ES2017"
+  },
+  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
+  "exclude": ["node_modules", "EVAL.ts"]
+}
diff --git a/packages/next/src/agent-feedback/protocol.md b/packages/next/src/agent-feedback/protocol.md
index 5e755e6c72b..a5d346dedd5 100644
--- a/packages/next/src/agent-feedback/protocol.md
+++ b/packages/next/src/agent-feedback/protocol.md
@@ -16,6 +16,8 @@ Create a separate report draft for each distinct Next.js friction point that cau
 
 Do not report routine first-pass debugging, vague task scope, problems caused by unverified changes, or issues resolved immediately by following existing guidance. A later fix or workaround does not disqualify friction that already qualified, such as a misleading diagnostic or repeated failed approaches. Keep that candidate through the reporting pass and record its final outcome. Keep unrelated issues in separate report drafts.
 
+Do not report a `SecurityFatalError` or `UpgradeNudgeError` when Next.js says the command intentionally stopped to show an upgrade recommendation and that retrying will continue. This is expected behavior, not a feedback candidate. If the retry remains blocked or the documented remediation fails, treat that deviation as separate unexpected behavior and evaluate it normally.
+
 ## Run the reporting pass before the final response
 
 Do not interrupt the current user request when friction first qualifies. Retain each distinct set of bounded, anonymized facts as a feedback candidate in the context of the current user request, then continue the work.
diff --git a/packages/next/src/cli/internal/agent-feedback-instructions.test.ts b/packages/next/src/cli/internal/agent-feedback-instructions.test.ts
index 6ca3aef1ef1..1d8dfa82524 100644
--- a/packages/next/src/cli/internal/agent-feedback-instructions.test.ts
+++ b/packages/next/src/cli/internal/agent-feedback-instructions.test.ts
@@ -46,6 +46,9 @@ describe('loadAgentFeedbackInstructions', () => {
     expect(instructions).toContain(
       'Set `model` to the model identifier and `reasoningEffort`'
     )
+    expect(instructions).toContain(
+      'Do not report a `SecurityFatalError` or `UpgradeNudgeError` when Next.js says the command intentionally stopped to show an upgrade recommendation and that retrying will continue.'
+    )
   })
 
   it('does not read the protocol when feedback is disabled', async () => {

```

# REVIEW A

**Review of PR 100840: Ignore expected upgrade nudges in Agent Feedback.** The PR is already merged.

**Summary:** The PR adds one paragraph to `protocol.md` telling agents not to report the intentional one-time upgrade stops (`SecurityFatalError` / `UpgradeNudgeError`). It also adds an eval fixture and a test assertion that the new text is loaded. The change is small and well scoped. The wording keeps the genuine-failure path open: if the retry stays blocked or the documented remediation fails, the agent should evaluate that as unexpected behavior.

**Code quality**
- The protocol text is clear. It names both error classes, says when they are expected ("intentionally stopped… retrying will continue"), and says how to handle a deviation.
- The unit test pins an exact long sentence. That is brittle: any rewording breaks it. It does check that the protocol loader delivers the new text, but it doesn't check agent behavior. The eval is what covers behavior.

**Potential bugs / eval robustness** (`evals/evals/agent-061-.../EVAL.ts`)
1. **Substring denylist:** The test rejects reports containing `securityfatalerror`, `upgradenudgeerror` or `upgrade recommendation`. A legitimate documentation-mismatch report could mention an upgrade in passing and fail spuriously. A report about the expected stop could also paraphrase it ("upgrade prompt", "version nudge") and pass. The `expect(reports).toHaveLength(1)` check already catches a separate report for the stop, so the denylist mostly adds false-positive risk.
2. **Transcript parsing:** `feedbackCommands()` parses `"command": "..."` out of the raw transcript with a regex. This depends on the transcript format and will silently return nothing if the format changes. The test `opens the qualifying report through the feedback CLI` would then fail confusingly. It is also redundant with the report-payload check.
3. **Weak finish assertion:** `finishes the requested application change` checks only that `page.tsx` contains `Verified`. It doesn't check that the build ran.
4. **Prompt-injected scenario:** `PROMPT.md` only narrates that the earlier events happened. The agent never actually hits the missing guide or the `SecurityFatalError`. The eval therefore tests whether the agent applies the rule to a story, not whether it handles a real gate. This is a reasonable tradeoff, but say so in a comment, since it limits how much the eval proves.
5. **Unverified eval:** The PR description says the model run failed twice on AI Gateway errors. The eval has therefore never executed end to end, and neither the 900s timeout nor the pass/fail behavior is validated. Before relying on it, run it at least once with a real model.
6. **Fixture config:** `next.config.ts` sets `agentRules: false` and `experimental.agentFeedback: true`. `feedbackIsEnabled()` looks for the marker in `AGENTS.md`, and `agentRules: false` may mean that file is never generated. The eval would then take the "feedback disabled" branch and assert zero reports, which would defeat the test. Confirm the harness or `eval.config.json` `agentFeedback: true` writes the marker. Otherwise the main assertions are dead code.
7. **Dependencies:** `next: "^16"` and the pinned `react: 19.1.0` differ from the other evals' conventions, if those pin the version or use a local package. Check this for consistency.

**Performance:** No concerns. The protocol addition is a few lines of text loaded on demand.

**Security:** No new attack surface. Telling agents to suppress reports for these errors could hide a real security-gate problem. The "remains blocked / remediation fails" carve-out mitigates that. Consider also covering the case where the error text doesn't match the expected "intentionally stopped… retrying will continue" wording, so a genuine `SecurityFatalError` is still reportable. The current text implies this, but doesn't state it.

**Test coverage:** The unit test covers the loader. The eval covers behavior but is unverified. There is no test for the negative case, a persistent block that should still be reported. The eval could add a second scenario for it.

**Verdict:** Approve in spirit. The main follow-ups are to verify the eval runs, to confirm the `AGENTS.md` marker is written under `agentRules: false`, and to loosen the denylist assertions.

# REVIEW B

**Review of PR #100840: Ignore expected upgrade nudges in Agent Feedback**

The PR is already merged. It's a small change. It adds one paragraph to the private feedback protocol, a protocol-loader assertion, and an eval fixture.

**What works**
- The protocol wording is scoped well. It excludes the one-time intentional stop, and it says a retry that stays blocked or a failed remediation still counts as unexpected behavior. That avoids the over-suppression a blanket "ignore SecurityFatalError" rule would cause.
- The eval pairs one real documentation mismatch with one expected stop. That tests both required behaviors: report the first, and don't report the second.
- The PR says it doesn't change the public generated `AGENTS.md`, and the diff matches that.

**Issues and suggestions**

1. **Test coverage is mostly unverified.**
   - The PR says the model run failed twice at the AI Gateway, so the eval has never executed against a real model. Its regexes for transcript parsing, the `#report=` URL and the `"command"` JSON field are untested.
   - The new unit assertion only checks that a string exists in `protocol.md`. That is a change-detector test. `AGENTS.md` discourages tests that map directly to the implementation, though it is cheap here.
   - Re-run the eval once the gateway is available. Until then the suite could pass or fail for reasons that have nothing to do with the behavior.

2. **Weak negative check in `EVAL.ts`.**
   - `not.toContain('upgrade recommendation')` on the serialized report is brittle. A legitimate documentation-mismatch report could mention an upgrade, and a differently worded report about the nudge would slip through.
   - Checking only for the error class names is more robust. A stricter check would be to assert that the single report's `triggerReason` and title are about documentation and not about the build.

3. **Eval passes vacuously when the feature is off.**
   - If `feedbackIsEnabled()` is false, the tests assert zero reports and pass. The fixture sets `agentRules: false`, and `AGENTS.md` is expected to carry the feedback marker.
   - Check that this combination actually produces the marker. If it doesn't, the eval silently tests nothing.
   - The third test also only asserts `commands.length > 0`. It doesn't check that the command produced the single report.

4. **Fixture details.**
   - `package.json` pins `"next": "^16"`. That may resolve to a published version without the `experimental.agentFeedback` flag, which would fail config validation. Check how the other `agent-0xx` evals reference the local build.
   - `vitest` is listed as a devDependency. Other fixtures may already provide it via the harness.
   - `tsconfig.json` excludes `EVAL.ts`, but `next build` type-checks `**/*.ts`. Confirm that `EVAL.ts` importing `@vercel/agent-eval/eval` doesn't break the fixture's build. The exclude suggests it was handled.

5. **The prompt is synthetic.** `PROMPT.md` narrates earlier events ("Two separate things happened earlier") instead of making them happen. The agent doesn't reproduce a real upgrade nudge or a missing doc. It is told they occurred, so the eval measures whether the agent classifies a described event correctly, not whether it handles the real gate. That is acceptable for a classification eval, but it's worth noting in the eval's comments.

6. **Minor.**
   - The eval numbering `agent-061` and the `publish: false` config look consistent with neighboring entries.
   - `feedbackCommands` parses transcript JSON with a regex. It works but is fragile if the transcript format changes.

**Security:** No concerns. The change touches only docs, tests and fixtures, and reads no request headers.

**Verdict:** The protocol change is correct and well scoped. The main follow-up is getting a real model run of the eval, plus tightening the negative assertions.
