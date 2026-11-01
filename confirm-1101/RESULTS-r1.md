# confirm-1101 round 1 results (price-fixed)

Plan: `PLAN.md` at 3198d46, pushed 2026-11-01T13:06:46Z (before any paid run). Workflow fix 87b3f8b pushed 13:09:10Z.
Raw data: `r1/` (runs.json, run-ids.txt, rows.jsonl one line per run, analysis.json, ledger-t_ci_lab_1.json, dispatch.jsonl).
Rebuild: download every run in `r1/run-ids.txt` with `gh run download ID -D art/ID`, then
`python3 analyze.py art --runs r1/runs.json --ledger r1/ledger-t_ci_lab_1.json --json r1/analysis.json --rows r1/rows.jsonl`
and `python3 bin/results_r1.py r1/analysis.json RESULTS-r1.md`. Hashes: `MANIFEST.sha256`.

Runs: 110 dispatched, 108 with usage, 2 without output (listed below). 54 pairs: fix-ci Sonnet 10, fix-mention Sonnet 9, labels 10, release 10, review 10, fix-ci Opus 5. The "78" in the task brief is the 39 Sonnet confirm-claude pairs (78 runs); review (20 runs) and Opus (10 runs) come on top.
Total model spend, list prices: $7.7798 (client-reported total $7.7728).

## Main table (all rows, pass or fail)

Cost = provider token usage x list price (`prices/anthropic-pricing-2026-11-01.md`). Direct arm: the client's per-model usage (`modelUsage`).
Gateway arm: the gateway ledger usage for the run's session (every upstream call), same prices. Saving = -(exp(mean ln(gw/direct)) - 1).
CI: bootstrap over tasks, 10,000 draws, seed 1. Pass bar = CI upper bound below 0 cost change AND quality not lower AND tool calls >= 70%.

| area | agent | model | n pairs | saving % | 95% CI | cheaper | direct $/run | gateway $/run | quality | tool calls d/g (ratio) | net/run $ | gateway ran first | pass bar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fix-ci | claude-code | claude-opus-5-5 | 5 | 4.5 | [-29.9, 26.9] | 3/5 | 0.1172 | 0.1283 | pass 5/5 -> 5/5, McNemar p=1.0 | 28/36 (1.286) | -0.0179 | 5/5 | not met |
| fix-ci | claude-code | claude-sonnet-5-5 | 10 | 18.0 | [4.7, 26.5] | 9/10 | 0.0479 | 0.0391 | pass 10/10 -> 10/10, McNemar p=1.0 | 54/52 (0.963) | 0.0039 | 9/10 | PASS |
| fix-mention | claude-code | claude-sonnet-5-5 | 9 | 7.5 | [-17.5, 23.1] | 7/9 | 0.0904 | 0.0862 | pass 6/9 -> 7/9, McNemar p=1.0 | 77/83 (1.078) | -0.0042 | 9/9 | not met |
| labels | claude-code | claude-sonnet-5-5 | 10 | 17.7 | [-6.3, 31.4] | 8/10 | 0.03 | 0.0276 | F1 0.444 -> 0.531 | 12/13 (1.083) | 0.0004 | 10/10 | not met |
| release | claude-code | claude-sonnet-5-5 | 10 | 14.7 | [3.8, 24.1] | 8/10 | 0.128 | 0.1079 | not judged (judge not run) | 78/103 (1.321) | 0.0118 | 10/10 | not met |
| review | claude-code-action | claude-sonnet-5-5 | 10 | 9.8 | [-7.0, 24.8] | 7/10 | 0.0602 | 0.0555 | not judged (judge not run) | 13/17 (1.308) | 0.0015 | 10/10 | not met |

Only **fix-ci, Sonnet 5.5** meets the full pass bar: 18.0% cheaper [4.7, 26.5], 10/10 tests pass on both arms.
Release is cheaper with a CI above 0 (14.7% [3.8, 24.1]) but its quality judge was not run, so the bar is not met.
Labels, fix-mention, review and fix-ci Opus: the CI crosses 0. We do not claim a saving for them from this round.

## Sensitivity (same pairs, other cost sources)

Client-reported `total_cost_usd` for both arms:

| area | model | n | saving % | 95% CI | pass bar |
|---|---|---|---|---|---|
| fix-ci | claude-opus-5-5 | 5 | 4.5 | [-29.9, 26.9] | not met |
| fix-ci | claude-sonnet-5-5 | 10 | 18.0 | [4.7, 26.5] | PASS |
| fix-mention | claude-sonnet-5-5 | 9 | 7.5 | [-17.5, 23.1] | not met |
| labels | claude-sonnet-5-5 | 10 | 17.7 | [-6.3, 31.4] | not met |
| release | claude-sonnet-5-5 | 10 | 15.6 | [5.9, 24.3] | not met |
| review | claude-sonnet-5-5 | 10 | 8.0 | [-8.5, 22.9] | not met |

Higher of client-based and ledger-based cost for the gateway arm (the least favourable choice for the gateway):

| area | model | n | saving % | 95% CI | pass bar |
|---|---|---|---|---|---|
| fix-ci | claude-opus-5-5 | 5 | 4.5 | [-29.9, 26.9] | not met |
| fix-ci | claude-sonnet-5-5 | 10 | 18.0 | [4.7, 26.5] | PASS |
| fix-mention | claude-sonnet-5-5 | 9 | 7.5 | [-17.5, 23.1] | not met |
| labels | claude-sonnet-5-5 | 10 | 17.7 | [-6.3, 31.4] | not met |
| release | claude-sonnet-5-5 | 10 | 14.7 | [3.8, 24.1] | not met |
| review | claude-sonnet-5-5 | 10 | 7.9 | [-8.8, 22.9] | not met |

Round-1 analyze.py prices (wrong, Sonnet 3/15, Opus 5/25, 1.25x write, 0.1x read; shown only to make the fix visible):

| area | model | n | saving % | 95% CI | pass bar |
|---|---|---|---|---|---|
| fix-ci | claude-opus-5-5 | 5 | 6.9 | [-24.5, 28.5] | not met |
| fix-ci | claude-sonnet-5-5 | 10 | 22.3 | [11.5, 29.0] | PASS |
| fix-mention | claude-sonnet-5-5 | 9 | 9.1 | [-18.4, 26.0] | not met |
| labels | claude-sonnet-5-5 | 10 | 22.3 | [6.5, 32.1] | PASS |
| release | claude-sonnet-5-5 | 10 | 18.8 | [12.2, 25.9] | not met |
| review | claude-sonnet-5-5 | 10 | 10.2 | [-2.5, 22.9] | not met |

## Cross-check (3% rule)

- Our price x client usage vs client `total_cost_usd`: 108 runs, mean gap 0.0, max 0.0, over 3%: 0. The client bills at the same list prices.
- Our price x ledger usage vs ledger `billed_usd`: 54 gateway runs, max gap 0.0. The gateway bills at the same list prices.
- Client-based vs ledger, gateway arm: 54 runs, mean gap 0.0059, max 0.0976, over 3%: 3. Why they differ:
  1. Side call model. In 10 review gateway runs the ledger shows a `claude-haiku-4-5-20251001` side call (about 1,014 input tokens, $0.01092 in total). The action's client counts those tokens under Sonnet 5.5, so the client over-counts by about 1-4% on these small runs (2 of them are over 3%). The ledger is the true bill; the cost table uses it.
  2. Gateway-side upstream loops. In one release run the gateway made more upstream calls than the client sent requests; the client does not see them, so it under-counts. The ledger includes them; the cost table uses it (this makes the gateway arm dearer, not cheaper).
  3. Cache 5m/1h split: client and ledger agree on the split in every run (both read the provider usage). Long-context tier: none applies (Sonnet/Opus 5.5 have one price over the full 1M window; no Haiku 5.5 prompt was over 100k). Inference geo: global in all runs.

Runs over 3% (client-based vs ledger):

| run | area | task | client-based $ | ledger $ | gap | ledger rows | upstream calls | client requests | ledger side models |
|---|---|---|---|---|---|---|---|---|---|
| 41319314359 | release | valkey-9.0.7 | 0.14556 | 0.1613 | -0.098 | 11 | 13 | 11 | {} |
| 41322977604 | review | kafka-23804 | 0.03145 | 0.03037 | 0.036 | 3 | 3 | 2 | {'claude-haiku-4-5-20251001': 1} |
| 41323649721 | review | vscode-343624 | 0.03347 | 0.03238 | 0.034 | 3 | 3 | 2 | {'claude-haiku-4-5-20251001': 1} |

## Per-pair rows

| area | model | task | direct run | gateway run | direct $ | gateway $ | saving % | tests d/g | F1 d/g | tool calls d/g |
|---|---|---|---|---|---|---|---|---|---|---|
| fix-ci | claude-opus-5-5 | echo-3131 | 41326756134 | 41326538288 | 0.24742 | 0.29462 | -19.1 | [True, True] |  | 9/15 |
| fix-ci | claude-opus-5-5 | echo-3158 | 41326456070 | 41326241678 | 0.1086 | 0.17572 | -61.8 | [True, True] |  | 6/10 |
| fix-ci | claude-opus-5-5 | lo-757 | 41326551159 | 41326341575 | 0.0775 | 0.05352 | 30.9 | [True, True] |  | 4/4 |
| fix-ci | claude-opus-5-5 | lo-778 | 41326855255 | 41326632047 | 0.07376 | 0.05989 | 18.8 | [True, True] |  | 3/3 |
| fix-ci | claude-opus-5-5 | zap-1587 | 41326647144 | 41326441766 | 0.07858 | 0.05766 | 26.6 | [True, True] |  | 6/4 |
| fix-ci | claude-sonnet-5-5 | echo-3131 | 41310519734 | 41310312607 | 0.10507 | 0.07332 | 30.2 | [True, True] |  | 10/8 |
| fix-ci | claude-sonnet-5-5 | echo-3158 | 41309864279 | 41310034811 | 0.07029 | 0.06548 | 6.8 | [True, True] |  | 10/6 |
| fix-ci | claude-sonnet-5-5 | echo-3189 | 41310807874 | 41310603424 | 0.04156 | 0.03131 | 24.7 | [True, True] |  | 5/6 |
| fix-ci | claude-sonnet-5-5 | lo-757 | 41310325069 | 41310131405 | 0.04386 | 0.02939 | 33.0 | [True, True] |  | 5/4 |
| fix-ci | claude-sonnet-5-5 | lo-778 | 41310617751 | 41310410033 | 0.03126 | 0.02426 | 22.4 | [True, True] |  | 3/3 |
| fix-ci | claude-sonnet-5-5 | lo-993 | 41310903490 | 41310694134 | 0.03744 | 0.03078 | 17.8 | [True, True] |  | 5/5 |
| fix-ci | claude-sonnet-5-5 | scrapy-7783 | 41310996245 | 41310794380 | 0.04852 | 0.03926 | 19.1 | [True, True] |  | 4/6 |
| fix-ci | claude-sonnet-5-5 | zap-1567 | 41311086062 | 41310888432 | 0.03696 | 0.02846 | 23.0 | [True, True] |  | 5/6 |
| fix-ci | claude-sonnet-5-5 | zap-1587 | 41310424245 | 41310223606 | 0.03375 | 0.02391 | 29.2 | [True, True] |  | 4/4 |
| fix-ci | claude-sonnet-5-5 | zap-1589 | 41310708684 | 41310507387 | 0.03036 | 0.045 | -48.2 | [True, True] |  | 3/4 |
| fix-mention | claude-sonnet-5-5 | echo-2977 | 41313393697 | 41313201260 | 0.07874 | 0.06199 | 21.3 | [False, True] |  | 9/10 |
| fix-mention | claude-sonnet-5-5 | echo-3006 | 41313852719 | 41313657445 | 0.1401 | 0.11039 | 21.2 | [True, True] |  | 15/13 |
| fix-mention | claude-sonnet-5-5 | echo-3060 | 41313579858 | 41313381259 | 0.13935 | 0.13316 | 4.4 | [False, False] |  | 10/15 |
| fix-mention | claude-sonnet-5-5 | fiber-3988 | 41313304894 | 41313107185 | 0.09689 | 0.08378 | 13.5 | [True, True] |  | 8/4 |
| fix-mention | claude-sonnet-5-5 | lo-796 | 41313670505 | 41313471473 | 0.06592 | 0.03996 | 39.4 | [True, True] |  | 7/4 |
| fix-mention | claude-sonnet-5-5 | lo-799 | 41313485237 | 41313291818 | 0.04938 | 0.0375 | 24.1 | [True, True] |  | 7/6 |
| fix-mention | claude-sonnet-5-5 | mocha-5997 | 41313942674 | 41313748331 | 0.05096 | 0.10463 | -105.3 | [False, False] |  | 3/12 |
| fix-mention | claude-sonnet-5-5 | mocha-6331 | 41313762332 | 41313565015 | 0.1218 | 0.14202 | -16.6 | [True, True] |  | 11/13 |
| fix-mention | claude-sonnet-5-5 | mocha-6361 | 41314054293 | 41313839988 | 0.07086 | 0.06211 | 12.3 | [True, True] |  | 7/6 |
| labels | claude-sonnet-5-5 | flutter-194705 | 41317065687 | 41316858005 | 0.02954 | 0.01836 | 37.8 |  | [0.4, 0.0] | 1/1 |
| labels | claude-sonnet-5-5 | godot-124050 | 41316970332 | 41316762096 | 0.02263 | 0.01463 | 35.4 |  | [0.8, 0.8] | 1/1 |
| labels | claude-sonnet-5-5 | godot-124254 | 41317160892 | 41316956785 | 0.02447 | 0.01688 | 31.0 |  | [0.7272727272727272, 0.7272727272727272] | 2/1 |
| labels | claude-sonnet-5-5 | godot-124534 | 41316578552 | 41316368087 | 0.0192 | 0.0126 | 34.4 |  | [0.8000000000000002, 0.6666666666666665] | 1/1 |
| labels | claude-sonnet-5-5 | rust-163852 | 41316680462 | 41316462331 | 0.03144 | 0.02007 | 36.2 |  | [0.8, 0.4] | 1/1 |
| labels | claude-sonnet-5-5 | rust-164694 | 41316775289 | 41316566001 | 0.02813 | 0.026 | 7.6 |  | [0.0, 0.6666666666666666] | 1/2 |
| labels | claude-sonnet-5-5 | rust-164736 | 41316871864 | 41316662791 | 0.02849 | 0.06174 | -116.7 |  | [0.25, 0.25] | 1/1 |
| labels | claude-sonnet-5-5 | typescript-64677 | 41317254521 | 41317054347 | 0.02681 | 0.02065 | 23.0 |  | [0.0, 1.0] | 1/1 |
| labels | claude-sonnet-5-5 | vscode-340116 | 41316381680 | 41316178504 | 0.06432 | 0.0649 | -0.9 |  | [0.0, 0.0] | 2/3 |
| labels | claude-sonnet-5-5 | vscode-340427 | 41316472482 | 41316275821 | 0.02535 | 0.02003 | 21.0 |  | [0.6666666666666666, 0.8] | 1/1 |
| release | claude-sonnet-5-5 | biome-2.6.4 | 41319738534 | 41319519930 | 0.21878 | 0.17095 | 21.9 |  |  | 5/15 |
| release | claude-sonnet-5-5 | fastapi-0.160.0 | 41319946243 | 41319724273 | 0.06382 | 0.05102 | 20.1 |  |  | 5/5 |
| release | claude-sonnet-5-5 | godot-3.6.3-stable | 41320440888 | 41320225732 | 0.20276 | 0.12422 | 38.7 |  |  | 15/14 |
| release | claude-sonnet-5-5 | mastodon-4.6.7 | 41320047188 | 41319826813 | 0.10329 | 0.10814 | -4.7 |  |  | 8/8 |
| release | claude-sonnet-5-5 | node-26.7.0 | 41320143101 | 41319931763 | 0.16325 | 0.14568 | 10.8 |  |  | 9/18 |
| release | claude-sonnet-5-5 | powershell-7.6.7 | 41320339616 | 41320129068 | 0.13904 | 0.10985 | 21.0 |  |  | 8/11 |
| release | claude-sonnet-5-5 | redis-8.4.6 | 41319842067 | 41319622529 | 0.06619 | 0.06485 | 2.0 |  |  | 6/8 |
| release | claude-sonnet-5-5 | ruff-0.16.2 | 41319637299 | 41319418337 | 0.12556 | 0.08531 | 32.1 |  |  | 13/9 |
| release | claude-sonnet-5-5 | svelte-5.56.10 | 41320237920 | 41320032830 | 0.06507 | 0.058 | 10.9 |  |  | 3/5 |
| release | claude-sonnet-5-5 | valkey-9.0.7 | 41319534228 | 41319314359 | 0.13249 | 0.1613 | -21.7 |  |  | 6/10 |
| review | claude-sonnet-5-5 | elasticsearch-163196 | 41323662538 | 41323460107 | 0.07479 | 0.07436 | 0.6 |  |  | 1/2 |
| review | claude-sonnet-5-5 | elasticsearch-163282 | 41323284107 | 41322727621 | 0.06526 | 0.09744 | -49.3 |  |  | 1/1 |
| review | claude-sonnet-5-5 | flutter-190431 | 41324044704 | 41323839904 | 0.04608 | 0.05609 | -21.7 |  |  | 1/1 |
| review | claude-sonnet-5-5 | kafka-23804 | 41323184457 | 41322977604 | 0.05781 | 0.03037 | 47.5 |  |  | 1/1 |
| review | claude-sonnet-5-5 | kafka-23911 | 41323473369 | 41323270907 | 0.07803 | 0.06921 | 11.3 |  |  | 4/5 |
| review | claude-sonnet-5-5 | kubernetes-140611 | 41323757194 | 41323553706 | 0.04136 | 0.04336 | -4.8 |  |  | 1/1 |
| review | claude-sonnet-5-5 | vscode-342878 | 41323566891 | 41323363660 | 0.04911 | 0.04782 | 2.6 |  |  | 1/2 |
| review | claude-sonnet-5-5 | vscode-343624 | 41323851422 | 41323649721 | 0.04071 | 0.03238 | 20.5 |  |  | 1/1 |
| review | claude-sonnet-5-5 | zed-65129 | 41323377361 | 41323170953 | 0.04857 | 0.0401 | 17.4 |  |  | 1/1 |
| review | claude-sonnet-5-5 | zed-65841 | 41323947229 | 41323743948 | 0.10057 | 0.06344 | 36.9 |  |  | 1/2 |

## Runs without output

- 41309715920: fix-ci echo-3158 direct-ts claude-sonnet-5-5: no claude output (failure).
- 41322736512: review elasticsearch-163282 gateway claude-sonnet-5-5: no claude output (cancelled).

## Deviations

1. **Price fix.** The pre-registered analyze.py (3198d46) priced claude-*-5-5 at the prior generation list price (Sonnet 3/15, Opus 5/25, write 1.25x, read 0.1x). The live price page (saved 2026-11-01, `prices/anthropic-pricing-2026-11-01.md`, sha256 in MANIFEST) says Sonnet 5.5: input 2, 5m write 2.5, 1h write 4, read 0.10, output 10; Opus 5.5: 4, 5, 8, 0.20, 20 USD per Mtok. analyze.py now uses these, prices 5m and 1h writes apart, and counts every model in `modelUsage` (side calls). PLAN.md's "Known limits" already said the cross-check would show any price gap; it did (client cost differed). The method (paired log ratio, bootstrap, bar) is unchanged. The old-price table above shows the effect: labels moved from PASS-level CI to a CI that crosses 0.
2. **Gateway cost source.** PLAN.md says cost = provider usage x price. For the gateway arm we take the provider usage from the gateway ledger (it sees every upstream call), not from the client, for the reasons in the cross-check. Both variants are shown above; no row changes its bar result.
3. **87b3f8b.** One workflow-only fix (`cd "$GITHUB_WORKSPACE"` before the Verify step copies output) pushed 3 minutes after the plan. Plan, tasks, prompts and analysis were not touched. 109 of the 110 runs ran on 87b3f8b.
4. **Run 41309715920 rerun.** fix-ci echo-3158 direct-ts Sonnet, on 3198d46, failed in Verify (`cp: cannot create regular file 'out/claude-output.json'`), so it uploaded no usage. Its model spend is not in the totals (the client output was lost). It was rerun on 87b3f8b as 41309864279; the pair uses the rerun.
5. **Cancelled review run 41322736512.** The dispatcher got rc=1 for review gateway elasticsearch#163282 at 15:43:29Z, but GitHub had created two runs (41322727621 at 15:44:18Z and 41322736512 at 15:44:25Z). The second was cancelled before the model ran (no output). The pair uses 41322727621.
6. **Arm order.** The arms were not swapped as PLAN.md intended (seeded order): the gateway arm started first in 53 of 54 pairs, the direct arm 2-3 minutes later, on a different org (orgs swap in the second half per pick.py). A cache carry-over from gateway to direct is not possible across orgs, but a time-of-day or provider-load effect cannot be ruled out. Round 2 must randomise the order per pair.
7. **Rows not run in this round (not reported as results):** release and review quality judges; fix-ci for OpenCode, Pi and Codex (confirm-agents runs were still in progress at analysis time; they are a separate round); fix-mention Opus (planned 5; dispatched from 16:5xZ, after the analysis cut-off of 16:45Z, so it is not in this file). Opus fix-ci ran 5 of the planned 5. Analysis cut-off: runs created up to 16:45Z, ledger rows up to 16:45Z.
8. **OpenCode and Pi headers.** As `packages/cli/src/ci.mjs` wires them, OpenCode and Pi do not send `x-cm-ci-*` headers, and Pi's first request grew 3.2x through the gateway in the dry probe (6698 B to 21525 B). Any OpenCode/Pi result must be read with this in mind.
9. **Fix task pool.** Only 5 of 14 fix-ci and 6 of 14 fix-mention candidates were valid at first validation (setup: missing deps such as poetry `responses`, pydantic `thread_unsafe` marker). final.json holds the tasks that passed validation; all fix tasks pass on both arms here except fix-mention (direct 6/9, gateway 7/9).
10. **Quota guard.** `used_paused` was 0 before and after every area (dispatch.jsonl `guard` lines; 0 again at analysis time).

