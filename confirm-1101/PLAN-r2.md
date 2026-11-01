# confirm-1101 round 2 plan (pre-registered; pushed before any paid round-2 run)

Goal: tighten the confidence intervals of round 1 and fill the rows round 1 did not run
(Opus fix-mention, OpenCode, Pi, Codex, release and review judges).

Naming: the folder `r2/` and `RESULTS.md` (commit 501c3c9) are the re-analysis of all 150 round-1 runs.
They are NOT this round. This round writes its data to `run2/` and its report to `RESULTS-r2.md`.

## 1. Tasks (new only)

- Used set U = every task id in the 150 round-1 runs (`r2/runs.json`). No task in U runs in round 2.
- `pick_r2.py` (seed `confirm-1101-r2`, no model, no regex) writes `tasks-r2/<area>.json` and `tasks-r2/schedule.json`.
- fix-ci, fix-mention: round-1 task order minus U, then the extended pool `pools/r2/fix-*.json`
  (`build_fix.py` with PER_REPO=10, rule F8; it reproduces byte for byte from `pools/cache`). A task is valid only if
  `validation.json` (latest row per task and mode, free `confirm-validate` runs) has baseline fail and control pass.
  The first N valid candidates are the tasks.
- labels, release, review: `pools/<area>.json` in sha256 draw order (seed confirm-1101) minus U.

## 2. Sample size

n per lane = min(n for a 95% CI half-width of about 10 points, unused valid tasks). From the round-1 spread of
log(gateway/direct): n_hw10 = (1.96 x sd / 0.10)^2.

| lane | agent | model | area | r1 sd | n_hw10 | pool | n |
|---|---|---|---|---|---|---|---|
| cc-sonnet-fix-ci | claude-code | sonnet 5.5 | fix-ci | 0.228 | 21 | 16 | 16 |
| cc-sonnet-fix-mention | claude-code | sonnet 5.5 | fix-mention | 0.348 | 47 | 19 | 19 |
| cc-sonnet-labels | claude-code | sonnet 5.5 | labels | 0.377 | 55 | 26 | 26 |
| cc-sonnet-release | claude-code | sonnet 5.5 | release | 0.203 | 16 | 20 | 16 |
| action-sonnet-review | claude-code-action | sonnet 5.5 | review | 0.303 | 36 | 26 | 26 |
| cc-opus-fix-ci | claude-code | opus 5.5 | fix-ci | 0.363 | 51 | - | 8 (fixed) |
| cc-opus-fix-mention | claude-code | opus 5.5 | fix-mention | - | - | - | 8 (fixed) |
| opencode-sonnet-fix-ci | opencode | sonnet 5.5 | fix-ci | - | - | - | 8 (fixed) |
| pi-sonnet-fix-ci | pi | sonnet 5.5 | fix-ci | - | - | - | 8 (fixed) |
| codex-gpt5mini-fix-ci | codex | gpt-5-mini | fix-ci | - | - | - | 6 (fixed) |

Where the pool is smaller than n_hw10, the half-width will be wider than 10 points. The pooled row (section 7) helps there.
OpenCode, Pi and Codex run because the wiring fix (gateway 29164aeab, lab fe36d91) proved their x-cm-ci-* headers
arrive: dry runs 41331719510 (OpenCode), 41331722514 (Pi), 41331867795 (Codex).

## 3. Arms, orgs, order, spacing

- Arms: direct-ts (provider direct, no gateway) and gateway (https://gateway.contextmode.ai). Same model, prompt,
  tools, task and setup. Workflows: confirm-claude, confirm-review, confirm-agents (agents installed with their
  native installers).
- Keys: Anthropic only ANTHROPIC_API_KEY_D (mert2) and ANTHROPIC_API_KEY_C (bmksglu). Codex: OPENAI_API_KEY.
- Orgs: in each lane, tasks 1..ceil(n/2) run gateway on mert2 and direct-ts on bmksglu; the rest swap.
- Arm order: rank the lane's tasks by sha256("confirm-1101-r2|lane|task"); even rank runs gateway first, odd rank
  direct-ts first (exact half/half).
- Spacing: each lane dispatches one run every 75 s, alternating the pair's arms, so runs in one arm's sequence
  start at least 150 s apart (2.5 min). At most 18 lab runs in flight; a dispatch waits for a free slot, so some
  gaps are longer. Actual gaps are reported.
- Driver: `bin/run_r2.py` reads `tasks-r2/schedule.json`. Phase A: the five Sonnet lanes. Phase B: the other five.

## 4. Cost

- Cost of a run = provider usage (the usage the provider returned) x list price (prices/anthropic-pricing-2026-11-01.md):
  Sonnet 5.5 in 2, 5m write 2.5, 1h write 4, read 0.10, out 10; Opus 5.5 in 4, 5, 8, 0.20, 20 USD per Mtok.
  gpt-5-mini 0.25 in, 0.025 cached, 2.00 out (OpenAI list price). Every model in the run is counted (side calls too).
- Claude Code / action: usage from the result `modelUsage`. Gateway arm: the gateway ledger (`/__ops-rows`, tenant
  t_ci_lab_1) when it has rows for the session, because it sees every upstream call.
- OpenCode, Pi, Codex: usage from `usageproxy.py`, which logs the provider's own usage per request, in both arms.
- Cross-check: our price x client usage vs client total_cost_usd; client vs ledger on the gateway arm. Target gap
  within 3%; every run over 3% is listed with its cause. The row's pass/fail is also shown with the client cost.
- Saving = 1 - exp(mean over tasks of log(gateway/direct)). 95% CI: paired bootstrap over tasks, 10000 draws, seed 1.

## 5. Quality

- fix-ci, fix-mention: the task's failing tests pass after the run. Exact two-sided McNemar on the pairs.
- labels: F1 against the maintainers' labels (round-1 scorer).
- release, review: blind judge of a different model: Claude Opus 5.5 judges the Sonnet outputs
  (release-judge.yml, review-action-judge.yml). A/B order per pair by a seeded coin (seed confirm-1101-r2-judge).
  The judge sees no tool or arm names. Round-1 release and review pairs are judged the same way for the pooled rows.
  Human check: 5 pairs per area, chosen by sha256("confirm-1101-r2-human|area|task") lowest five. Their judge files
  and verdicts are listed in RESULTS-r2.md for the owner to check; until the owner checks them they are marked
  "pending" and do not change any pass/fail.
- Tool mix per arm: count of tool calls by tool name, from the client output (Claude) or the proxy log (agents).

## 6. Pass bar (all three)

1. CI upper bound of log(gateway/direct) below 0 (the saving CI is fully above 0).
2. Quality not lower: fix: gateway passes >= direct passes, or McNemar p >= 0.05; labels: gateway F1 >= direct F1 - 0.05;
   release, review: judge wins gateway >= direct, or exact sign test (ties dropped) p >= 0.05.
3. Gateway tool calls >= 70% of direct tool calls (sum over the lane's pairs).

Every row is reported, pass or fail. No row is dropped; unusable runs are listed with the reason.

## 7. Pooled rows (secondary)

Per area and agent/model: round-1 complete pairs (all 150 round-1 runs, re-priced by this analyze.py) plus round-2
pairs, same bootstrap. Reported as secondary; the round-2 row is primary.

## 8. Caps and stop rules

- Anthropic cap $45, OpenAI cap $4. Shares (USD): cc-sonnet-fix-ci 3, cc-sonnet-fix-mention 6, cc-sonnet-labels 3,
  cc-sonnet-release 6, action-sonnet-review 5, cc-opus-fix-ci 4, cc-opus-fix-mention 6, opencode 2, pi 2,
  judges 8 (= 45). Codex: OpenAI 4.
- The driver sums each lane's spend from finished artifacts (client cost, or proxy usage x price). A lane stops
  dispatching when it reaches its share. Tasks not run are reported.
- Quota guard `ci-quota-guard.py --need 500` before and after each phase and each lane. A lane is valid only if
  used_paused did not grow. If it grows, all dispatching stops.

## 9. Outputs

RESULTS-r2.md (rows, pooled rows, cross-check, Deviations), run2/ (runs.json, dispatch.jsonl, rows, ledger, judge
verdicts), MANIFEST.sha256 update, run ids. No key is printed or committed; a secret scan runs before each push.
