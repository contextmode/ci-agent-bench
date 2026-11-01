# confirm-1101 results (round 2, all 150 runs)

Plan: PLAN.md at 3198d46, pushed 2026-11-01T13:06:46Z. First paid run 13:07:24Z (one smoke run); the main batch started 13:11Z.
Runs: 150 dispatched (98+1 confirm-claude, 21 review incl. 1 cancelled, 30 confirm-agents). Keys used: ANTHROPIC_API_KEY_D (mert2), ANTHROPIC_API_KEY_C (bmksglu), OPENAI_API_KEY. No other key.
Computed spend by org (list prices): {'mert2': 4.78, 'bmksglu': 5.3, 'openai': 0.32}. Caps: $45 Anthropic, $4 OpenAI (not reached).
Quota guard before and after: used_paused 0 throughout.

## Main table (every row, pass or fail)

| area | agent | model | n | saving % | 95% CI | cheaper | direct $/run | gateway $/run | quality | tool calls ratio | net/run $ | passed bar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fix-ci | claude-code | claude-opus-5-5 | 5 | 4.5 | [-29.9, 26.9] | 3/5 | 0.1172 | 0.1283 | pass 5/5 -> 5/5, McNemar p=1.0 | 1.286 | -0.0179 | not met |
| fix-ci | claude-code | claude-sonnet-5-5 | 10 | 18.0 | [4.7, 26.5] | 9/10 | 0.0479 | 0.0391 | pass 10/10 -> 10/10, McNemar p=1.0 | 0.963 | 0.0039 | PASS |
| fix-mention | claude-code | claude-opus-5-5 | 5 | 23.0 | [9.8, 33.3] | 5/5 | 0.2632 | 0.2071 | pass 4/5 -> 4/5, McNemar p=1.0 | 0.721 | 0.0473 | PASS |
| fix-mention | claude-code | claude-sonnet-5-5 | 9 | 7.5 | [-17.5, 23.1] | 7/9 | 0.0904 | 0.0862 | pass 6/9 -> 7/9, McNemar p=1.0 | 1.078 | -0.0042 | not met |
| labels | claude-code | claude-sonnet-5-5 | 10 | 17.7 | [-6.3, 31.4] | 8/10 | 0.03 | 0.0276 | F1 0.444 -> 0.531 | 1.083 | 0.0004 | not met |
| release | claude-code | claude-sonnet-5-5 | 10 | 14.7 | [3.8, 24.1] | 8/10 | 0.128 | 0.1079 | not judged (judge not run) | 1.321 | 0.0118 | not met |
| review | claude-code-action | claude-sonnet-5-5 | 10 | 9.8 | [-7.0, 24.8] | 7/10 | 0.0602 | 0.0555 | not judged (judge not run) | 1.308 | 0.0015 | not met |
| fix-ci | opencode | claude-sonnet-5-5 | 5 | 22.4 | [16.6, 27.6] | 5/5 | 0.0472 | 0.0364 | pass 4/5 -> 4/5, McNemar p=1.0 | 0.893 | n/a | PASS |
| fix-ci | pi | claude-sonnet-5-5 | 5 | -67.3 | [-97.5, -37.5] | 0/5 | 0.0326 | 0.057 | pass 5/5 -> 5/5, McNemar p=1.0 | 1.069 | n/a | not met |
| fix-ci | codex | gpt-5-mini | 0 | n/a | n/a | 0/5 | direct ran 5/5 | gateway 400 on all 5 | n/a | n/a | n/a | not met (gateway arm failed) |

Blind judge (release, review) was not run; those rows cannot meet the quality part of the bar. The cost columns stand.

## Deviations

1. Price table: PLAN.md said Sonnet 3/15, Opus 5/25 per Mtok. The committed analyze.py (ea9813a) uses the live list prices saved in prices/ (Sonnet 2/10, Opus 4/20, Haiku 0.10/0.50, 5m and 1h writes apart), counts every model in modelUsage, and prices the gateway arm from the gateway ledger. Old-price and client-cost variants are in r2/an.json (rows_old_prices_3_15, rows_client_cost).
2. Codex: every gateway-arm request returned HTTP 400 (`reasoning.context = all_turns` unsupported by gpt-5-mini, seen in usage.jsonl). Direct arm ran. There is no paired Codex result. This is a gateway/Codex compatibility defect to fix, not a saving.
3. Pi: gateway arm cost more on 5/5 tasks (CI upper bound below 0 on cost increase). Reported as a failed row, not removed.
4. Workflow fixes after the plan: 87b3f8b (verify step cwd). A smoke run (echo-3158 direct, bmksglu) is the first run and is a counted run; its first attempt failed in the verify step and has no output (run 41309715920).
5. Review dispatches: the first two driver dispatches failed (rc 1, wrong input `org`), one stray run was cancelled (41322736512). No paid run was lost; the arm was re-dispatched. Pi lo-778 direct-ts needed one re-dispatch after a GitHub API EOF.
6. Review rows come from lab-metrics.json; Haiku side calls are priced as part of the run.
7. Opus fix-mention: 5 pairs, pass 4/5 both arms. OpenCode and Pi use n=5 (first 5 of fix-ci), as planned.
8. Gateway ran first in most pairs (arrival gap 150 s as planned), so the cache-cold side is the gateway arm in most pairs.

Rebuild: `gh run download ID -D art/ID` for r2/run-ids.txt, then `python3 analyze.py art --runs r2/runs.json --ledger r1/ledger-t_ci_lab_1.json --json r2/an.json --rows r2/rows.jsonl` and `python3 bin/agents_rows.py art r2/agents.json`.
