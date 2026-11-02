# confirm-1101 round 2 results

Plan: PLAN-r2.md (commit a4770f7, GitHub push 2026-11-01T23:39:27Z, before any paid run).

Saving = 1 - exp(mean log(gateway/direct)) over tasks; CI = paired bootstrap, 10000 draws, seed 1. Positive = gateway cheaper.
Cost = provider usage x list price; gateway arm from the gateway ledger when it has rows for the session.

## Summary

- Primary round-2 rows that pass the pre-registered bar (CI upper bound below 0 cost change, quality not lower, tool mix >= 0.7):
  Claude Code Sonnet 5.5 fix-ci 22.8% [11.6, 32.2], fix-mention 21.8% [10.3, 32.1], labels 22.4% [15.5, 27.7];
  Claude Code Opus 5.5 fix-ci 19.7% [4.1, 31.5], fix-mention 21.4% [7.1, 35.4]; OpenCode fix-ci 20.8% [0.3, 36.1].
- Rows that do not pass: release 14.1% [-6.8, 27.7] (CI crosses 0; judge gateway 9 / direct 3 / tie 4);
  review 5.5% [-2.9, 12.8] (CI crosses 0, and the blind judge prefers direct 12 / 5); Pi -2.8% [-20.9, 11.0];
  Codex gpt-5-mini -3.2% [-45.1, 22.9] (n 5).
- Review quality: the blind Opus judge prefers the direct arm in round 1 (9 / 0, p 0.004), in round 2 (12 / 5, p 0.143)
  and pooled (21 / 5, p 0.0025). Gateway reviews carry more false claims (32 vs 20 over 36 pairs). We claim no review saving.

## Deviations

1. Review org. The mert2 org cannot run the claude-code-action entrypoint: all 26 round-2 review runs on mert2 (13 per arm)
   ended in about 2 s with "Credit balance is too low" and 0 tokens. A local 1-token probe with the mert2 key worked with the
   sdk-cli entrypoint. We re-dispatched exactly those 26 runs on bmksglu (bin/rerun_review_r2.py, run2/dispatch-review-rerun.jsonl),
   the round-1 review org. So review has no org swap: both arms ran on bmksglu. The failed run ids are in
   run2/runs-review-mert2-failed.json; their spend is $0.
2. Spacing. The plan said runs of one arm start >= 150 s apart. Measured per lane and arm: median 173-215 s, but the minimum is
   88-93 s (the driver waits for a free slot, then dispatches). See the Spacing section. Arm order is balanced: the gateway ran
   first in 50% of pairs in every Claude Code lane (fix-mention Sonnet 10/19).
3. Sample sizes follow the PLAN-r2.md table (fix-mention Sonnet 19, labels 26, review 26, release 16), not the brief's flat 16.
   Codex has 5 usable pairs, not 6: both arms of scrapy-8312 hit the 45-minute job timeout and were cancelled.
4. Cross-check target (3%) is not met for 7 of 119 gateway runs. Our price x client usage equals the client total in all 238
   runs (max gap 0.0). Our price x ledger usage equals ledger billed_usd in all 119 gateway runs (max gap 0.0). Client vs ledger:
   mean 0.86%, max 26.3%. Causes: release bun-1.4.4 (41364799639): 47 upstream calls for 22 client requests, client cost 26% low;
   labels ruff-29395 and fix-ci commander.js-2630: one upstream call the client does not see; 4 review runs: a
   claude-haiku-4-5 side call that the action client counts at Sonnet price (1-4%). The tables use the ledger cost, which is
   the higher figure for the gateway arm, so the gap works against the gateway.
5. Ledger fetch. The first fetch ended at 01:00Z and missed the review re-run; we fetched again to 01:55Z (1006 rows, 2 pages,
   unique = total). One fetch passed the page cursor without URL encoding and looped on page 1; we found it by the unique count
   and discarded it.
6. OpenCode, Pi and Codex costs come from the usage proxy in the runner (norm.json), not from the gateway ledger.
7. Labels: the gateway arm made more tool calls (mix 1.556); F1 0.499 -> 0.478 is inside the 0.05 margin.
8. Pooled rows mix setups: round-1 fix tasks ran before the S1 setup fix, and round-1 Pi ran before the CLI wiring fix (Pi
   request 1 was 3.2x bigger then). Pooled Pi (-23.9%) is therefore not a fair view of the current wiring; use the round-2 row.
9. Human check: 5 pairs per area are listed below by the pre-registered sha256 rule. No human has read them yet. They do not
   change any pass/fail.
10. Code written after the plan push: bin/mkjudge_r2.py, bin/results_r2.py, bin/rerun_review_r2.py, per-pair output in
    bin/agents_rows.py. They follow the plan's metric; no metric or bar changed.
11. Judges: Opus 5.5 on mert2, 62 verdicts (release r1 10 + r2 16, review r1 10 + r2 26), 0 parse failures, $5.69.
12. Quota guard: used_paused was 0 before and after every phase, lane, re-run and judge batch.

## Spend

Anthropic: lab runs $22.16 (list price x provider usage) + judges $5.69 = $27.85 of the $45 cap.
OpenAI: Codex runs $0.35 of the $4 cap. No area reached its share of the cap.

## Round-2 rows (primary)

| area | agent | model | n | saving % | 95% CI | cheaper | direct $/run | gateway $/run | quality | tool mix gw/direct | bar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fix-ci | claude-code | claude-opus-5-5 | 8 | 19.7 | [4.1, 31.5] | 6/8 | 0.1691 | 0.132 | pass 8/8 -> 8/8, McNemar p=1.0 | 0.857 | PASS |
| fix-ci | claude-code | claude-sonnet-5-5 | 16 | 22.8 | [11.6, 32.2] | 14/16 | 0.0502 | 0.042 | pass 16/16 -> 15/16, McNemar p=1.0 | 0.978 | PASS |
| fix-mention | claude-code | claude-opus-5-5 | 8 | 21.4 | [7.1, 35.4] | 7/8 | 0.335 | 0.2759 | pass 3/8 -> 3/8, McNemar p=1.0 | 0.917 | PASS |
| fix-mention | claude-code | claude-sonnet-5-5 | 19 | 21.8 | [10.3, 32.1] | 16/19 | 0.1113 | 0.0872 | pass 9/19 -> 10/19, McNemar p=1.0 | 0.783 | PASS |
| labels | claude-code | claude-sonnet-5-5 | 26 | 22.4 | [15.5, 27.7] | 24/26 | 0.0281 | 0.0223 | F1 0.499 -> 0.478 | 1.556 | PASS |
| release | claude-code | claude-sonnet-5-5 | 16 | 14.1 | [-6.8, 27.7] | 11/16 | 0.1039 | 0.126 | judge (Opus 5.5, blind) gateway 9 / direct 3 / tie 4, sign p=0.146 | 1.023 | no |
| review | claude-code-action | claude-sonnet-5-5 | 26 | 5.5 | [-2.9, 12.8] | 17/26 | 0.0587 | 0.0569 | judge (Opus 5.5, blind) gateway 5 / direct 12 / tie 9, sign p=0.143 | 1.25 | no |
| fix-ci | codex | gpt-5-mini | 5 | -3.2 | [-45.1, 22.9] | 3/5 | 0.0369 | 0.0334 | pass 5/5 -> 5/5, McNemar p=1.0 | 1.19 | no |
| fix-ci | opencode | claude-sonnet-5-5 | 8 | 20.8 | [0.3, 36.1] | 6/8 | 0.0732 | 0.056 | pass 8/8 -> 8/8, McNemar p=1.0 | 0.931 | PASS |
| fix-ci | pi | claude-sonnet-5-5 | 8 | -2.8 | [-20.9, 11.0] | 4/8 | 0.0366 | 0.0369 | pass 8/8 -> 8/8, McNemar p=1.0 | 1.02 | no |

## Round-1 rows, same analysis (for reference)

| area | agent | model | n | saving % | 95% CI | cheaper | direct $/run | gateway $/run | quality | tool mix gw/direct | bar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fix-ci | claude-code | claude-opus-5-5 | 5 | 4.5 | [-29.9, 26.9] | 3/5 | 0.1172 | 0.1283 | pass 5/5 -> 5/5, McNemar p=1.0 | 1.286 | no |
| fix-ci | claude-code | claude-sonnet-5-5 | 10 | 18.0 | [4.7, 26.5] | 9/10 | 0.0479 | 0.0391 | pass 10/10 -> 10/10, McNemar p=1.0 | 0.963 | PASS |
| fix-mention | claude-code | claude-opus-5-5 | 5 | 23.0 | [9.8, 33.3] | 5/5 | 0.2632 | 0.2071 | pass 4/5 -> 4/5, McNemar p=1.0 | 0.721 | PASS |
| fix-mention | claude-code | claude-sonnet-5-5 | 9 | 7.5 | [-17.5, 23.1] | 7/9 | 0.0904 | 0.0862 | pass 6/9 -> 7/9, McNemar p=1.0 | 1.078 | no |
| labels | claude-code | claude-sonnet-5-5 | 10 | 17.7 | [-6.3, 31.4] | 8/10 | 0.03 | 0.0276 | F1 0.444 -> 0.531 | 1.083 | no |
| release | claude-code | claude-sonnet-5-5 | 10 | 14.7 | [3.8, 24.1] | 8/10 | 0.128 | 0.1079 | judge (Opus 5.5, blind) gateway 4 / direct 3 / tie 3, sign p=1.0 | 1.321 | PASS |
| review | claude-code-action | claude-sonnet-5-5 | 10 | 9.8 | [-7.0, 24.8] | 7/10 | 0.0602 | 0.0555 | judge (Opus 5.5, blind) gateway 0 / direct 9 / tie 1, sign p=0.004 | 1.308 | no |
| fix-ci | opencode | claude-sonnet-5-5 | 5 | 22.4 | [16.6, 27.6] | 5/5 | 0.0472 | 0.0364 | pass 4/5 -> 4/5, McNemar p=1.0 | 0.893 | PASS |
| fix-ci | pi | claude-sonnet-5-5 | 5 | -67.3 | [-97.5, -37.5] | 0/5 | 0.0326 | 0.057 | pass 5/5 -> 5/5, McNemar p=1.0 | 1.069 | no |

## Pooled rows, round 1 + round 2 (secondary)

| area | agent | model | n | saving % | 95% CI | cheaper | direct $/run | gateway $/run | pairs r1 + r2 | tool mix |
|---|---|---|---|---|---|---|---|---|---|---|
| fix-ci | claude-code | claude-opus-5-5 | 13 | 14.2 | [-1.3, 25.9] | 9/13 | 0.1491 | 0.1306 | 5 + 8 | 0.971 |
| fix-ci | claude-code | claude-sonnet-5-5 | 26 | 21.0 | [12.9, 28.2] | 23/26 | 0.0493 | 0.0409 | 10 + 16 | 0.972 |
| fix-ci | codex | gpt-5-mini | 5 | -3.2 | [-45.1, 22.9] | 3/5 | 0.0369 | 0.0334 | 0 + 5 | 1.19 |
| fix-ci | opencode | claude-sonnet-5-5 | 13 | 21.4 | [8.8, 31.7] | 11/13 | 0.0632 | 0.0484 | 5 + 8 | 0.919 |
| fix-ci | pi | claude-sonnet-5-5 | 13 | -23.9 | [-47.9, -4.8] | 4/13 | 0.035 | 0.0446 | 5 + 8 | 1.038 |
| fix-mention | claude-code | claude-opus-5-5 | 13 | 22.0 | [12.1, 32.0] | 12/13 | 0.3074 | 0.2494 | 5 + 8 | 0.841 |
| fix-mention | claude-code | claude-sonnet-5-5 | 28 | 17.4 | [6.5, 26.6] | 23/28 | 0.1046 | 0.0869 | 9 + 19 | 0.862 |
| labels | claude-code | claude-sonnet-5-5 | 36 | 21.1 | [13.7, 26.9] | 32/36 | 0.0287 | 0.0238 | 10 + 26 | 1.438 |
| release | claude-code | claude-sonnet-5-5 | 26 | 14.3 | [1.3, 23.6] | 19/26 | 0.1132 | 0.1191 | 10 + 16 | 1.134 |
| review | claude-code-action | claude-sonnet-5-5 | 36 | 6.7 | [-1.0, 13.8] | 24/36 | 0.0591 | 0.0565 | 10 + 26 | 1.268 |

## Cross-check

```
{
 "computed_vs_client": {
  "n": 238,
  "mean": 0.0,
  "max": 0.0,
  "over_3pct": 0
 },
 "computed_vs_ledger_gateway": {
  "n": 119,
  "mean": 0.0086,
  "max": 0.2627,
  "over_3pct": 7
 },
 "ledger_recomputed_vs_ledger_billed": {
  "n": 119,
  "mean": 0.0,
  "max": 0.0,
  "over_3pct": 0
 },
 "gw_only_side_usd_total": 0.02854,
 "gw_only_side_runs": 26,
 "ledger_gaps_over_3pct": [
  {
   "run_id": "41364799639",
   "area": "release",
   "task": "bun-1.4.4",
   "client_based_usd": 0.63474,
   "ledger_usd": 0.86094,
   "gap": -0.263,
   "ledger_rows": 22,
   "upstream_calls": 47,
   "client_requests": 22,
   "ledger_side_models": {}
  },
  {
   "run_id": "41364984686",
   "area": "labels",
   "task": "ruff-29395",
   "client_based_usd": 0.02231,
   "ledger_usd": 0.02357,
   "gap": -0.053,
   "ledger_rows": 4,
   "upstream_calls": 4,
   "client_requests": 3,
   "ledger_side_models": {}
  },
  {
   "run_id": "41365618185",
   "area": "fix-ci",
   "task": "commander.js-2630",
   "client_based_usd": 0.01297,
   "ledger_usd": 0.01506,
   "gap": -0.139,
   "ledger_rows": 2,
   "upstream_calls": 3,
   "client_requests": 2,
   "ledger_side_models": {}
  },
  {
   "run_id": "41366928522",
   "area": "review",
   "task": "godot-118822",
   "client_based_usd": 0.03775,
   "ledger_usd": 0.03664,
   "gap": 0.03,
   "ledger_rows": 3,
   "upstream_calls": 3,
   "client_requests": 2,
   "ledger_side_models": {
    "claude-haiku-4-5-20251001": 1
   }
  },
  {
   "run_id": "41367447043",
   "area": "review",
   "task": "spring-boot-52228",
   "client_based_usd": 0.03604,
   "ledger_usd": 0.03493,
   "gap": 0.032,
   "ledger_rows": 4,
   "upstream_calls": 4,
   "client_requests": 3,
   "ledger_side_models": {
    "claude-haiku-4-5-20251001": 1
   }
  },
  {
   "run_id": "41369538031",
   "area": "review",
   "task": "django-22041",
   "client_based_usd": 0.03191,
   "ledger_usd": 0.03082,
   "gap": 0.035,
   "ledger_rows": 3,
   "upstream_calls": 3,
   "client_requests": 2,
   "ledger_side_models": {
    "claude-haiku-4-5-20251001": 1
   }
  },
  {
   "run_id": "41372483514",
   "area": "review",
   "task": "kubernetes-142436",
   "client_based_usd": 0.02799,
   "ledger_usd": 0.02689,
   "gap": 0.041,
   "ledger_rows": 3,
   "upstream_calls": 3,
   "client_requests": 2,
   "ledger_side_models": {
    "claude-haiku-4-5-20251001": 1
   }
  }
 ]
}
```

## Spacing (seconds between dispatches of the same lane and arm)

```
{
 "action-sonnet-review direct-ts": {
  "n": 26,
  "min_s": 91.0,
  "median_s": 175.0
 },
 "action-sonnet-review gateway": {
  "n": 26,
  "min_s": 91.0,
  "median_s": 175.0
 },
 "action-sonnet-review-rerun direct-ts": {
  "n": 13,
  "min_s": 124.0,
  "median_s": 125.0
 },
 "action-sonnet-review-rerun gateway": {
  "n": 13,
  "min_s": 124.0,
  "median_s": 125.0
 },
 "cc-opus-fix-ci direct-ts": {
  "n": 8,
  "min_s": 91.0,
  "median_s": 176.0
 },
 "cc-opus-fix-ci gateway": {
  "n": 8,
  "min_s": 90.0,
  "median_s": 177.0
 },
 "cc-opus-fix-mention direct-ts": {
  "n": 8,
  "min_s": 90.0,
  "median_s": 178.0
 },
 "cc-opus-fix-mention gateway": {
  "n": 8,
  "min_s": 89.0,
  "median_s": 176.0
 },
 "cc-sonnet-fix-ci direct-ts": {
  "n": 16,
  "min_s": 91.0,
  "median_s": 176.0
 },
 "cc-sonnet-fix-ci gateway": {
  "n": 16,
  "min_s": 93.0,
  "median_s": 176.0
 },
 "cc-sonnet-fix-mention direct-ts": {
  "n": 19,
  "min_s": 91.0,
  "median_s": 175.0
 },
 "cc-sonnet-fix-mention gateway": {
  "n": 19,
  "min_s": 88.0,
  "median_s": 175.5
 },
 "cc-sonnet-labels direct-ts": {
  "n": 26,
  "min_s": 91.0,
  "median_s": 175.0
 },
 "cc-sonnet-labels gateway": {
  "n": 26,
  "min_s": 91.0,
  "median_s": 175.0
 },
 "cc-sonnet-release direct-ts": {
  "n": 16,
  "min_s": 90.0,
  "median_s": 177.0
 },
 "cc-sonnet-release gateway": {
  "n": 16,
  "min_s": 88.0,
  "median_s": 208.0
 },
 "codex-gpt5mini-fix-ci direct-ts": {
  "n": 6,
  "min_s": 161.0,
  "median_s": 174.0
 },
 "codex-gpt5mini-fix-ci gateway": {
  "n": 6,
  "min_s": 173.0,
  "median_s": 175.0
 },
 "opencode-sonnet-fix-ci direct-ts": {
  "n": 8,
  "min_s": 91.0,
  "median_s": 180.0
 },
 "opencode-sonnet-fix-ci gateway": {
  "n": 8,
  "min_s": 91.0,
  "median_s": 215.0
 },
 "pi-sonnet-fix-ci direct-ts": {
  "n": 8,
  "min_s": 93.0,
  "median_s": 173.0
 },
 "pi-sonnet-fix-ci gateway": {
  "n": 8,
  "min_s": 90.0,
  "median_s": 174.0
 }
}
```

Quota guard used_paused values seen before and after every phase and lane: [0].

## Human check (pending owner review; does not change any pass/fail)

- release r2-next.js-16.4.2: judge says tie wins; file lab/release/judge/r2-next.js-16.4.2.md; pending
- release r2-vite-8.3.3: judge says gateway wins; file lab/release/judge/r2-vite-8.3.3.md; pending
- release r2-terraform-1.16.7: judge says gateway wins; file lab/release/judge/r2-terraform-1.16.7.md; pending
- release r2-pydantic-1.10.27: judge says gateway wins; file lab/release/judge/r2-pydantic-1.10.27.md; pending
- release r2-syncthing-2.1.7: judge says gateway wins; file lab/release/judge/r2-syncthing-2.1.7.md; pending
- review r2-neovim-42289: judge says tie wins; file lab/review-action/judge/r2-neovim-42289.md; pending
- review r2-next.js-100840: judge says tie wins; file lab/review-action/judge/r2-next.js-100840.md; pending
- review r2-spring-boot-52228: judge says direct-ts wins; file lab/review-action/judge/r2-spring-boot-52228.md; pending
- review r2-transformers-49742: judge says direct-ts wins; file lab/review-action/judge/r2-transformers-49742.md; pending
- review r2-grafana-136242: judge says gateway wins; file lab/review-action/judge/r2-grafana-136242.md; pending

## Unusable runs

```
[
 {
  "run_id": "41363619264",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363639842",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363660257",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363735653",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363752714",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363776409",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363861773",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363880224",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363898809",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363969996",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41363987288",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364005895",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364091038",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364108317",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364199612",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364215366",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364333389",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364362361",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364445008",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364453699",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364521563",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364563244",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364611338",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364677903",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364686074",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364715225",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364780168",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364787677",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364838687",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364933612",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364961269",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41364966533",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365080201",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365096647",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365099835",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365220240",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365235218",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365356808",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365359230",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365476746",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365489654",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 },
 {
  "run_id": "41365613561",
  "area": null,
  "task": null,
  "arm": null,
  "model": null,
  "error": "no claude output (success)"
 }
]
```

