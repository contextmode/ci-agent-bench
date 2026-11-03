# Reproduce the headless-CI benchmark

Run our CI cost benchmark in your own GitHub account, with your own keys, in one click.

## One click

1. Click **Use this template** on https://github.com/contextmode/ci-agent-bench and create your copy.
2. In your copy, add two secrets (Settings > Secrets and variables > Actions):
   - `ANTHROPIC_API_KEY`: your Anthropic API key.
   - `CONTEXT_MODE_KEY`: run `npx @context-mode/cli ci key create --repo OWNER/NAME --gh`. It stores the key as a secret and never shows it.
3. Open **Actions > reproduce > Run workflow**. Pick:
   - `task_set`: `night-1101-r2` (the specs in `reproduce/tasks/`) or `confirm-1101` (the specs in `confirm-1101/tasks/`).
   - `area`: one area or `all`.
   - `model`: default `claude-sonnet-5-5`.
   - `tasks`: how many tasks per area (the first N of the spec). 7 is the full set.

The job writes the result table to its summary page. It also uploads `state.json` (every run id) and `results.json`.

Cost guide (Sonnet 5.5, both arms, per task): $0.05 to $0.35. A full area of 7 tasks costs about $0.5 to $2.5.

## What the job does

For each area, `reproduce/run.py` dispatches the area workflow twice per task: arm `direct-ts` and arm `gateway`. The two runs of a task start back to back, in a seeded random order. Tasks start 150 s apart. This is the schedule of the published round. Then it waits, downloads each run's artifact and runs `reproduce/analyze.py`.

The two arms differ only in three env lines. Everything else (the agent, the prompt, the tools, the model) is the same.

- `direct-ts`: Claude Code calls the Anthropic API directly, with `ENABLE_TOOL_SEARCH=true`.
- `gateway`: the same, plus the gateway lines below.

## The gateway env lines

These are the lines `npx @context-mode/cli ci init` writes. Paste them into the `env:` of any job that runs Claude Code:

```yaml
env:
  ANTHROPIC_BASE_URL: https://gateway.contextmode.ai
  ANTHROPIC_CUSTOM_HEADERS: |
    x-cm-device-key: ${{ secrets.CONTEXT_MODE_KEY }}
    x-context-mode-banner: off
    x-cm-ci-repo: ${{ github.repository }}
    x-cm-ci-ref: pr-${{ github.event.pull_request.number }}
    x-cm-ci-run: ${{ github.run_id }}
  ENABLE_TOOL_SEARCH: "true"
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

The gateway removes every `x-cm-*` header before it forwards, so your Context Mode key never reaches Anthropic. A CI key has no personal memory.

Install Claude Code with its native installer:

```yaml
- run: |
    curl -fsSL https://claude.ai/install.sh | bash
    echo "$HOME/.local/bin" >> "$GITHUB_PATH"
```

## How the table is computed

`reproduce/analyze.py`, the same code that gives our published numbers:

- Cost per run: `total_cost_usd` as Claude Code reports it.
- Pair: the direct-ts run and the gateway run of the same task.
- Saving: `-(exp(mean(log(gateway / direct))) - 1)`. Positive means the gateway was cheaper.
- 95% range: bootstrap that resamples tasks, 10,000 draws, seed 1.
- Cheaper: pairs where the gateway run cost less.
- Net: mean direct cost minus mean gateway cost minus $0.0009 per gateway API request.
- Run 1 of each area is cold (empty cache). We publish the warm runs (2 and later). The table also shows all runs.

A pair counts only when both runs finish without error.

## Use-cases

Each spec file lists the tasks: the upstream repo, the issue or PR number, and the pinned commit or tag.

### CI-failure fix

- Job: a real merged bug-fix commit is reverted, so the real test suite fails. Claude Code reads the log and fixes the code. Pass: the suite passes with the test files restored.
- Workflow: `.github/workflows/triage.yml`. Tasks: `reproduce/tasks/triage.json`.

### @claude fix

- Job: the repo at the parent of a real merged fix PR, with the linked issue as the `@claude` request. Pass: the PR's own held-back tests pass.
- Workflow: `.github/workflows/mention.yml`. Tasks: `reproduce/tasks/mention.json`.

### Issue triage and labels

- Job: label a real new issue from the repo's own label set. Score: F1 against the labels the maintainers set.
- Workflow: `.github/workflows/labels.yml`. Tasks: `reproduce/tasks/labels.json`.

### Issue dedupe

- Job: find the original of a real issue that a maintainer closed as a duplicate. Score: the original is in the top 3.
- Workflow: `.github/workflows/dedupe.yml`. Tasks: `reproduce/tasks/dedupe.json`.
- Note: in our round the gateway arm made far fewer tool calls, so the two arms did not do the same work. We do not publish this number.

### Release notes

- Job: write the notes for a real release from the commits and PRs between two tags.
- Workflow: `.github/workflows/release.yml`. Tasks: `reproduce/tasks/release.json`.

### PR review (official claude-code-action)

- Job: `anthropics/claude-code-action@v1` reviews a real merged PR. It prints the review and posts nothing.
- Workflow: `.github/workflows/review-action.yml`. Tasks: `reproduce/tasks/review-action.json`.

### PR review (community template)

- Job: a common community `claude -p` review template reviews a real merged PR. It prints the review and posts nothing.
- Workflow: `.github/workflows/pr-review.yml`. Tasks: `reproduce/tasks/pr-review.json`.

## Safety

All workflows run on `workflow_dispatch` only, so code from a fork never sees a secret. No workflow writes to an upstream repo. No key is printed; the workflows check their artifacts for keys before upload.

## Published data

- Round: `docs/ci-night-1101-r2.md`, raw table `lab/ci-night/results-r2.json` (run ids per pair).
- Run artifacts: https://github.com/contextmode/ci-agent-bench/actions
