# CI night round 1, live gateway, cross-run traffic (2026-11-01)

Lab tenant `t_ci_lab_1`. Baseline arm `direct-ts` (direct API + ENABLE_TOOL_SEARCH). Gateway arm uses the CI headers from `lab/path-env.sh`. Clients as in the 1031 docs: `claude -p` / official `claude-code-action@v1` per workflow.

## Result: no area reaches 60%, and none reaches 50%

Headline = warm saving (runs 2..n of each sequence). Saving is `-(exp(mean log-ratio) - 1)`, so positive = gateway cheaper. CI = bootstrap resampling tasks, 10,000, seed 1.

| lane | n pairs (warm/all) | cold (run 1) | warm saving | warm CI | all-runs saving | all CI | cheaper pairs (all) | net per run after $0.0009/req | valid |
|---|---|---|---|---|---|---|---|---|---|
| review-action-sonnet | 7/8 | 26.7% | 18.4% | 1.9% to 33.5% | 19.5% | 5.4% to 33.2% | 7/8 | $0.012 | yes |
| review-action-opus | 5/6 | 15.3% | 12.2% | -5.7% to 29.8% | 12.7% | -1.9% to 27.6% | 4/6 | $0.0192 | yes |
| mention-sonnet | 7/8 | -2.9% | 37.3% | 22.8% to 51.5% | 33.3% | 17.4% to 48.1% | 7/8 | $0.0288 | yes |
| mention-opus | 5/6 | -15.5% | 17.4% | -4.8% to 34.8% | 12.6% | -7.0% to 31.1% | 3/6 | $0.0212 | yes |
| triage-sonnet | 7/8 | 25.0% | 23.9% | 19.0% to 28.8% | 24.1% | 19.6% to 28.2% | 8/8 | $0.0046 | yes |
| triage-opus | 5/6 | 16.9% | 30.6% | 18.7% to 38.0% | 28.5% | 17.9% to 36.8% | 6/6 | $0.0207 | yes |
| pr-review-sonnet | 7/8 | 36.6% | 8.7% | -15.4% to 26.1% | 12.7% | -8.7% to 28.5% | 6/8 | $0.0041 | yes |
| labels-sonnet | 7/8 | 29.9% | 27.5% | 23.1% to 33.2% | 27.8% | 23.8% to 32.8% | 8/8 | $0.0065 | yes |
| dedupe-sonnet | 7/8 | 71.8% | -1.9% | -104.3% to 37.1% | 13.2% | -72.0% to 48.5% | 6/8 | $0.032 | yes |
| release-sonnet | 5/6 | 9.2% | 13.3% | -14.5% to 35.0% | 12.6% | -9.9% to 31.4% | 3/6 | $0.0068 | yes |

The cold column is one pair, so it carries no CI. Warm was not reliably better than cold in this round: the cross-run lever (#27) was not built or deployed before this round; the gateway ran as it was at the start of the night (#19-#25 and #28 live). This round is the baseline for #27. The dedupe lane has a very wide CI because the agent loops differ a lot between runs (Bash 172 vs 85 calls in total).

Areas with a CI that excludes zero on the warm number: mention-sonnet, triage-sonnet, triage-opus, labels-sonnet, review-action-sonnet. Not excluded: review-action-opus, mention-opus, pr-review-sonnet, dedupe-sonnet, release-sonnet.

Note: triage-sonnet has no tool mix or cost split here because my stats script could not read its per-message usage; its saving numbers come from the result totals.

## Round validity (quota guard)

`used_paused` was 0 before every lane and 0 after every lane, and 0 at round start and end. Tenant mode: full. Errors: 0 failed workflow runs of 144. Gateway ops for the tenant over the round hour: 532 requests, exits ok 532, no overloads, no stream cuts.

## Per area

### review-action-sonnet (claude-sonnet-5-5)

- n: 8 pairs (warm 7), mean cost $0.0694 direct-ts vs $0.0553 gateway
- quality: not scored in this round (no automatic check; judge not run)
- tool mix, direct-ts: Bash 9, Read 1
- tool mix, gateway: Bash 11
- gateway-arm cost split: prefix writes 46.0%, new tool results 22.1%, prefix reads 8.7%, thinking 0.2%, output 23.8%
- biggest remaining cost: prefix writes (46.0%)

### review-action-opus (claude-opus-5-5)

- n: 6 pairs (warm 5), mean cost $0.2271 direct-ts vs $0.2026 gateway
- quality: not scored in this round (no automatic check; judge not run)
- tool mix, direct-ts: Bash 28, Read 4, Grep 4
- tool mix, gateway: Bash 28, Read 2
- gateway-arm cost split: prefix writes 25.2%, new tool results 23.3%, prefix reads 19.5%, thinking 7.8%, output 24.5%
- biggest remaining cost: prefix writes (25.2%)

### mention-sonnet (claude-sonnet-5-5)

- n: 8 pairs (warm 7), mean cost $0.094 direct-ts vs $0.0589 gateway
- quality: passed: 6/8 direct-ts, 5/8 gateway
- tool mix, direct-ts: Bash 48, Read 13, Grep 11, Edit 9, bash 1
- tool mix, gateway: Bash 49, Edit 1
- gateway-arm cost split: prefix writes 15.1%, new tool results 19.9%, prefix reads 30.8%, thinking 6.2%, output 28.6%
- biggest remaining cost: prefix reads (30.8%)

### mention-opus (claude-opus-5-5)

- n: 6 pairs (warm 5), mean cost $0.2144 direct-ts vs $0.1836 gateway
- quality: passed: 4/6 direct-ts, 5/6 gateway
- tool mix, direct-ts: Bash 40, Grep 10, Read 8, Edit 3
- tool mix, gateway: Bash 53, Edit 5, Read 3
- gateway-arm cost split: prefix writes 10.7%, new tool results 20.3%, prefix reads 33.1%, thinking 5.3%, output 30.9%
- biggest remaining cost: prefix reads (33.1%)

### triage-sonnet (claude-sonnet-5-5)

- n: 8 pairs (warm 7), mean cost $0.0506 direct-ts vs $0.0398 gateway
- quality: passed: 8/8 direct-ts, 7/8 gateway
- tool mix, direct-ts: not captured (result-only output file)
- tool mix, gateway: not captured (result-only output file)
- gateway-arm cost split: n/a
- biggest remaining cost: not measurable (no per-message usage in artifact)

### triage-opus (claude-opus-5-5)

- n: 6 pairs (warm 5), mean cost $0.1003 direct-ts vs $0.0743 gateway
- quality: passed: 6/6 direct-ts, 6/6 gateway
- tool mix, direct-ts: Bash 25, Edit 6, Read 3, Grep 2
- tool mix, gateway: Bash 26, Edit 6, Read 3
- gateway-arm cost split: prefix writes 5.0%, new tool results 29.5%, prefix reads 34.3%, thinking 7.3%, output 24.7%
- biggest remaining cost: prefix reads (34.3%)

### pr-review-sonnet (claude-sonnet-5-5)

- n: 8 pairs (warm 7), mean cost $0.0604 direct-ts vs $0.0544 gateway
- quality: not scored in this round (no automatic check; judge not run)
- tool mix, direct-ts: Bash 11
- tool mix, gateway: Bash 9
- gateway-arm cost split: prefix writes 40.6%, new tool results 21.2%, prefix reads 9.0%, thinking 0.8%, output 29.3%
- biggest remaining cost: prefix writes (40.6%)

### labels-sonnet (claude-sonnet-5-5)

- n: 8 pairs (warm 7), mean cost $0.0297 direct-ts vs $0.0213 gateway
- quality: label F1 mean 0.670 direct-ts / 0.636 gateway
- tool mix, direct-ts: Bash 9
- tool mix, gateway: Bash 10
- gateway-arm cost split: prefix writes 32.4%, new tool results 39.2%, prefix reads 17.8%, thinking 0.5%, output 11.2%
- biggest remaining cost: new tool results (39.2%)

### dedupe-sonnet (claude-sonnet-5-5)

- n: 8 pairs (warm 7), mean cost $0.2378 direct-ts vs $0.1849 gateway
- quality: top3: 4/8 direct-ts, 6/8 gateway
- tool mix, direct-ts: Bash 172, Agent 51, TaskUpdate 4, TaskCreate 3, Monitor 1, ToolSearch 1
- tool mix, gateway: Bash 85, Agent 45
- gateway-arm cost split: prefix writes 4.6%, new tool results 55.2%, prefix reads 34.9%, thinking 1.0%, output 4.5%
- biggest remaining cost: new tool results (55.2%)

### release-sonnet (claude-sonnet-5-5)

- n: 6 pairs (warm 5), mean cost $0.1183 direct-ts vs $0.1049 gateway
- quality: not scored in this round (no automatic check; judge not run)
- tool mix, direct-ts: Bash 46, Write 6
- tool mix, gateway: Bash 42, Write 6
- gateway-arm cost split: prefix writes 22.7%, new tool results 23.0%, prefix reads 25.4%, thinking 2.2%, output 27.1%
- biggest remaining cost: output (27.1%)

Cost split method: per run, one price per base input token from total_cost = p*(in + 1.25*cache_write + 0.1*cache_read + 5*output), using result totals. Request 1 cache write = prefix writes; later cache writes and uncached input = new tool results; thinking = `thinking_tokens` from the result usage. Prices are the ratios implied by the run, not a price list.

## What this says

- Best warm numbers: mention-sonnet 37%, triage-opus 31%, labels 27%, triage-sonnet 24%. The 60% target is not close in any area.
- Prefix writes dominate the review lanes (review-action-sonnet 46%, pr-review 41%): that is the cross-run prefix (#27) target. Tool results dominate dedupe (55%) and labels (39%): that is the document-level dedup target.
- Opus lanes are noisier at n=6: the warm CI includes zero in review-action-opus and mention-opus, and excludes zero in triage-opus.
- Quality: mention-sonnet 5/8 gateway vs 6/8 direct (n=8, not significant); dedupe top-3 6/8 gateway vs 4/8 direct; others equal or not scored. The blind judge for review/pr-review/release was not run in this round.

## Spend

Round total from `total_cost_usd` of the 144 runs: $15.01, under the $30 cap. Opus ran in 3 areas (review-action, mention, triage) as capped.

## Run ids (tag `c1101-r1-<lane>-s<seq>`)

| lane | seq | arm | run id |
|---|---|---|---|
| review-action-sonnet | 1 | direct-ts | [41255351715](https://github.com/mksglu/cm-ci-lab/actions/runs/41255351715) |
| review-action-sonnet | 1 | gateway | [41255354585](https://github.com/mksglu/cm-ci-lab/actions/runs/41255354585) |
| review-action-sonnet | 2 | direct-ts | [41255533374](https://github.com/mksglu/cm-ci-lab/actions/runs/41255533374) |
| review-action-sonnet | 2 | gateway | [41255536625](https://github.com/mksglu/cm-ci-lab/actions/runs/41255536625) |
| review-action-sonnet | 3 | gateway | [41255724300](https://github.com/mksglu/cm-ci-lab/actions/runs/41255724300) |
| review-action-sonnet | 3 | direct-ts | [41255727210](https://github.com/mksglu/cm-ci-lab/actions/runs/41255727210) |
| review-action-sonnet | 4 | direct-ts | [41255910905](https://github.com/mksglu/cm-ci-lab/actions/runs/41255910905) |
| review-action-sonnet | 4 | gateway | [41255914180](https://github.com/mksglu/cm-ci-lab/actions/runs/41255914180) |
| review-action-sonnet | 5 | gateway | [41256102222](https://github.com/mksglu/cm-ci-lab/actions/runs/41256102222) |
| review-action-sonnet | 5 | direct-ts | [41256104856](https://github.com/mksglu/cm-ci-lab/actions/runs/41256104856) |
| review-action-sonnet | 6 | direct-ts | [41256284750](https://github.com/mksglu/cm-ci-lab/actions/runs/41256284750) |
| review-action-sonnet | 6 | gateway | [41256288021](https://github.com/mksglu/cm-ci-lab/actions/runs/41256288021) |
| review-action-sonnet | 7 | gateway | [41256470134](https://github.com/mksglu/cm-ci-lab/actions/runs/41256470134) |
| review-action-sonnet | 7 | direct-ts | [41256473790](https://github.com/mksglu/cm-ci-lab/actions/runs/41256473790) |
| review-action-sonnet | 8 | gateway | [41256652811](https://github.com/mksglu/cm-ci-lab/actions/runs/41256652811) |
| review-action-sonnet | 8 | direct-ts | [41256657150](https://github.com/mksglu/cm-ci-lab/actions/runs/41256657150) |
| review-action-opus | 1 | gateway | [41255353696](https://github.com/mksglu/cm-ci-lab/actions/runs/41255353696) |
| review-action-opus | 1 | direct-ts | [41255356286](https://github.com/mksglu/cm-ci-lab/actions/runs/41255356286) |
| review-action-opus | 2 | gateway | [41255535898](https://github.com/mksglu/cm-ci-lab/actions/runs/41255535898) |
| review-action-opus | 2 | direct-ts | [41255539339](https://github.com/mksglu/cm-ci-lab/actions/runs/41255539339) |
| review-action-opus | 3 | gateway | [41255726639](https://github.com/mksglu/cm-ci-lab/actions/runs/41255726639) |
| review-action-opus | 3 | direct-ts | [41255729211](https://github.com/mksglu/cm-ci-lab/actions/runs/41255729211) |
| review-action-opus | 4 | gateway | [41255913712](https://github.com/mksglu/cm-ci-lab/actions/runs/41255913712) |
| review-action-opus | 4 | direct-ts | [41255917068](https://github.com/mksglu/cm-ci-lab/actions/runs/41255917068) |
| review-action-opus | 5 | direct-ts | [41256104389](https://github.com/mksglu/cm-ci-lab/actions/runs/41256104389) |
| review-action-opus | 5 | gateway | [41256107214](https://github.com/mksglu/cm-ci-lab/actions/runs/41256107214) |
| review-action-opus | 6 | direct-ts | [41256287480](https://github.com/mksglu/cm-ci-lab/actions/runs/41256287480) |
| review-action-opus | 6 | gateway | [41256291142](https://github.com/mksglu/cm-ci-lab/actions/runs/41256291142) |
| mention-sonnet | 1 | direct-ts | [41255356234](https://github.com/mksglu/cm-ci-lab/actions/runs/41255356234) |
| mention-sonnet | 1 | gateway | [41255358764](https://github.com/mksglu/cm-ci-lab/actions/runs/41255358764) |
| mention-sonnet | 2 | gateway | [41255539583](https://github.com/mksglu/cm-ci-lab/actions/runs/41255539583) |
| mention-sonnet | 2 | direct-ts | [41255542992](https://github.com/mksglu/cm-ci-lab/actions/runs/41255542992) |
| mention-sonnet | 3 | gateway | [41255729762](https://github.com/mksglu/cm-ci-lab/actions/runs/41255729762) |
| mention-sonnet | 3 | direct-ts | [41255732619](https://github.com/mksglu/cm-ci-lab/actions/runs/41255732619) |
| mention-sonnet | 4 | gateway | [41255917103](https://github.com/mksglu/cm-ci-lab/actions/runs/41255917103) |
| mention-sonnet | 4 | direct-ts | [41255920521](https://github.com/mksglu/cm-ci-lab/actions/runs/41255920521) |
| mention-sonnet | 5 | direct-ts | [41256107257](https://github.com/mksglu/cm-ci-lab/actions/runs/41256107257) |
| mention-sonnet | 5 | gateway | [41256109621](https://github.com/mksglu/cm-ci-lab/actions/runs/41256109621) |
| mention-sonnet | 6 | gateway | [41256290551](https://github.com/mksglu/cm-ci-lab/actions/runs/41256290551) |
| mention-sonnet | 6 | direct-ts | [41256294809](https://github.com/mksglu/cm-ci-lab/actions/runs/41256294809) |
| mention-sonnet | 7 | gateway | [41256475975](https://github.com/mksglu/cm-ci-lab/actions/runs/41256475975) |
| mention-sonnet | 7 | direct-ts | [41256479092](https://github.com/mksglu/cm-ci-lab/actions/runs/41256479092) |
| mention-sonnet | 8 | gateway | [41256658373](https://github.com/mksglu/cm-ci-lab/actions/runs/41256658373) |
| mention-sonnet | 8 | direct-ts | [41256663324](https://github.com/mksglu/cm-ci-lab/actions/runs/41256663324) |
| mention-opus | 1 | gateway | [41255358417](https://github.com/mksglu/cm-ci-lab/actions/runs/41255358417) |
| mention-opus | 1 | direct-ts | [41255360884](https://github.com/mksglu/cm-ci-lab/actions/runs/41255360884) |
| mention-opus | 2 | direct-ts | [41255542380](https://github.com/mksglu/cm-ci-lab/actions/runs/41255542380) |
| mention-opus | 2 | gateway | [41255545842](https://github.com/mksglu/cm-ci-lab/actions/runs/41255545842) |
| mention-opus | 3 | gateway | [41255731725](https://github.com/mksglu/cm-ci-lab/actions/runs/41255731725) |
| mention-opus | 3 | direct-ts | [41255734352](https://github.com/mksglu/cm-ci-lab/actions/runs/41255734352) |
| mention-opus | 4 | direct-ts | [41255920445](https://github.com/mksglu/cm-ci-lab/actions/runs/41255920445) |
| mention-opus | 4 | gateway | [41255924350](https://github.com/mksglu/cm-ci-lab/actions/runs/41255924350) |
| mention-opus | 5 | gateway | [41256109100](https://github.com/mksglu/cm-ci-lab/actions/runs/41256109100) |
| mention-opus | 5 | direct-ts | [41256111333](https://github.com/mksglu/cm-ci-lab/actions/runs/41256111333) |
| mention-opus | 6 | gateway | [41256293361](https://github.com/mksglu/cm-ci-lab/actions/runs/41256293361) |
| mention-opus | 6 | direct-ts | [41256297169](https://github.com/mksglu/cm-ci-lab/actions/runs/41256297169) |
| triage-sonnet | 1 | direct-ts | [41256416119](https://github.com/mksglu/cm-ci-lab/actions/runs/41256416119) |
| triage-sonnet | 1 | gateway | [41256419014](https://github.com/mksglu/cm-ci-lab/actions/runs/41256419014) |
| triage-sonnet | 2 | direct-ts | [41256598194](https://github.com/mksglu/cm-ci-lab/actions/runs/41256598194) |
| triage-sonnet | 2 | gateway | [41256600775](https://github.com/mksglu/cm-ci-lab/actions/runs/41256600775) |
| triage-sonnet | 3 | direct-ts | [41256780866](https://github.com/mksglu/cm-ci-lab/actions/runs/41256780866) |
| triage-sonnet | 3 | gateway | [41256783124](https://github.com/mksglu/cm-ci-lab/actions/runs/41256783124) |
| triage-sonnet | 4 | gateway | [41256955463](https://github.com/mksglu/cm-ci-lab/actions/runs/41256955463) |
| triage-sonnet | 4 | direct-ts | [41256958239](https://github.com/mksglu/cm-ci-lab/actions/runs/41256958239) |
| triage-sonnet | 5 | gateway | [41257141437](https://github.com/mksglu/cm-ci-lab/actions/runs/41257141437) |
| triage-sonnet | 5 | direct-ts | [41257144023](https://github.com/mksglu/cm-ci-lab/actions/runs/41257144023) |
| triage-sonnet | 6 | gateway | [41257321081](https://github.com/mksglu/cm-ci-lab/actions/runs/41257321081) |
| triage-sonnet | 6 | direct-ts | [41257324046](https://github.com/mksglu/cm-ci-lab/actions/runs/41257324046) |
| triage-sonnet | 7 | direct-ts | [41257507855](https://github.com/mksglu/cm-ci-lab/actions/runs/41257507855) |
| triage-sonnet | 7 | gateway | [41257511337](https://github.com/mksglu/cm-ci-lab/actions/runs/41257511337) |
| triage-sonnet | 8 | gateway | [41257685350](https://github.com/mksglu/cm-ci-lab/actions/runs/41257685350) |
| triage-sonnet | 8 | direct-ts | [41257688023](https://github.com/mksglu/cm-ci-lab/actions/runs/41257688023) |
| triage-opus | 1 | gateway | [41256472637](https://github.com/mksglu/cm-ci-lab/actions/runs/41256472637) |
| triage-opus | 1 | direct-ts | [41256477029](https://github.com/mksglu/cm-ci-lab/actions/runs/41256477029) |
| triage-opus | 2 | gateway | [41256656077](https://github.com/mksglu/cm-ci-lab/actions/runs/41256656077) |
| triage-opus | 2 | direct-ts | [41256659966](https://github.com/mksglu/cm-ci-lab/actions/runs/41256659966) |
| triage-opus | 3 | direct-ts | [41256835602](https://github.com/mksglu/cm-ci-lab/actions/runs/41256835602) |
| triage-opus | 3 | gateway | [41256838295](https://github.com/mksglu/cm-ci-lab/actions/runs/41256838295) |
| triage-opus | 4 | direct-ts | [41257013756](https://github.com/mksglu/cm-ci-lab/actions/runs/41257013756) |
| triage-opus | 4 | gateway | [41257017396](https://github.com/mksglu/cm-ci-lab/actions/runs/41257017396) |
| triage-opus | 5 | direct-ts | [41257200739](https://github.com/mksglu/cm-ci-lab/actions/runs/41257200739) |
| triage-opus | 5 | gateway | [41257203314](https://github.com/mksglu/cm-ci-lab/actions/runs/41257203314) |
| triage-opus | 6 | direct-ts | [41257378938](https://github.com/mksglu/cm-ci-lab/actions/runs/41257378938) |
| triage-opus | 6 | gateway | [41257381779](https://github.com/mksglu/cm-ci-lab/actions/runs/41257381779) |
| pr-review-sonnet | 1 | direct-ts | [41256775591](https://github.com/mksglu/cm-ci-lab/actions/runs/41256775591) |
| pr-review-sonnet | 1 | gateway | [41256778115](https://github.com/mksglu/cm-ci-lab/actions/runs/41256778115) |
| pr-review-sonnet | 2 | gateway | [41256950199](https://github.com/mksglu/cm-ci-lab/actions/runs/41256950199) |
| pr-review-sonnet | 2 | direct-ts | [41256952732](https://github.com/mksglu/cm-ci-lab/actions/runs/41256952732) |
| pr-review-sonnet | 3 | direct-ts | [41257136513](https://github.com/mksglu/cm-ci-lab/actions/runs/41257136513) |
| pr-review-sonnet | 3 | gateway | [41257139353](https://github.com/mksglu/cm-ci-lab/actions/runs/41257139353) |
| pr-review-sonnet | 4 | direct-ts | [41257314947](https://github.com/mksglu/cm-ci-lab/actions/runs/41257314947) |
| pr-review-sonnet | 4 | gateway | [41257317875](https://github.com/mksglu/cm-ci-lab/actions/runs/41257317875) |
| pr-review-sonnet | 5 | direct-ts | [41257502495](https://github.com/mksglu/cm-ci-lab/actions/runs/41257502495) |
| pr-review-sonnet | 5 | gateway | [41257505861](https://github.com/mksglu/cm-ci-lab/actions/runs/41257505861) |
| pr-review-sonnet | 6 | gateway | [41257680180](https://github.com/mksglu/cm-ci-lab/actions/runs/41257680180) |
| pr-review-sonnet | 6 | direct-ts | [41257682858](https://github.com/mksglu/cm-ci-lab/actions/runs/41257682858) |
| pr-review-sonnet | 7 | direct-ts | [41257864443](https://github.com/mksglu/cm-ci-lab/actions/runs/41257864443) |
| pr-review-sonnet | 7 | gateway | [41257866771](https://github.com/mksglu/cm-ci-lab/actions/runs/41257866771) |
| pr-review-sonnet | 8 | direct-ts | [41258045770](https://github.com/mksglu/cm-ci-lab/actions/runs/41258045770) |
| pr-review-sonnet | 8 | gateway | [41258050383](https://github.com/mksglu/cm-ci-lab/actions/runs/41258050383) |
| labels-sonnet | 1 | direct-ts | [41256778170](https://github.com/mksglu/cm-ci-lab/actions/runs/41256778170) |
| labels-sonnet | 1 | gateway | [41256780922](https://github.com/mksglu/cm-ci-lab/actions/runs/41256780922) |
| labels-sonnet | 2 | gateway | [41256952592](https://github.com/mksglu/cm-ci-lab/actions/runs/41256952592) |
| labels-sonnet | 2 | direct-ts | [41256955318](https://github.com/mksglu/cm-ci-lab/actions/runs/41256955318) |
| labels-sonnet | 3 | direct-ts | [41257139002](https://github.com/mksglu/cm-ci-lab/actions/runs/41257139002) |
| labels-sonnet | 3 | gateway | [41257141562](https://github.com/mksglu/cm-ci-lab/actions/runs/41257141562) |
| labels-sonnet | 4 | gateway | [41257318278](https://github.com/mksglu/cm-ci-lab/actions/runs/41257318278) |
| labels-sonnet | 4 | direct-ts | [41257321063](https://github.com/mksglu/cm-ci-lab/actions/runs/41257321063) |
| labels-sonnet | 5 | direct-ts | [41257505567](https://github.com/mksglu/cm-ci-lab/actions/runs/41257505567) |
| labels-sonnet | 5 | gateway | [41257509062](https://github.com/mksglu/cm-ci-lab/actions/runs/41257509062) |
| labels-sonnet | 6 | direct-ts | [41257683305](https://github.com/mksglu/cm-ci-lab/actions/runs/41257683305) |
| labels-sonnet | 6 | gateway | [41257685704](https://github.com/mksglu/cm-ci-lab/actions/runs/41257685704) |
| labels-sonnet | 7 | gateway | [41257866788](https://github.com/mksglu/cm-ci-lab/actions/runs/41257866788) |
| labels-sonnet | 7 | direct-ts | [41257869409](https://github.com/mksglu/cm-ci-lab/actions/runs/41257869409) |
| labels-sonnet | 8 | gateway | [41258049423](https://github.com/mksglu/cm-ci-lab/actions/runs/41258049423) |
| labels-sonnet | 8 | direct-ts | [41258053178](https://github.com/mksglu/cm-ci-lab/actions/runs/41258053178) |
| dedupe-sonnet | 1 | direct-ts | [41257491630](https://github.com/mksglu/cm-ci-lab/actions/runs/41257491630) |
| dedupe-sonnet | 1 | gateway | [41257495268](https://github.com/mksglu/cm-ci-lab/actions/runs/41257495268) |
| dedupe-sonnet | 2 | direct-ts | [41257668992](https://github.com/mksglu/cm-ci-lab/actions/runs/41257668992) |
| dedupe-sonnet | 2 | gateway | [41257671561](https://github.com/mksglu/cm-ci-lab/actions/runs/41257671561) |
| dedupe-sonnet | 3 | direct-ts | [41257854698](https://github.com/mksglu/cm-ci-lab/actions/runs/41257854698) |
| dedupe-sonnet | 3 | gateway | [41257856935](https://github.com/mksglu/cm-ci-lab/actions/runs/41257856935) |
| dedupe-sonnet | 4 | direct-ts | [41258034060](https://github.com/mksglu/cm-ci-lab/actions/runs/41258034060) |
| dedupe-sonnet | 4 | gateway | [41258037884](https://github.com/mksglu/cm-ci-lab/actions/runs/41258037884) |
| dedupe-sonnet | 5 | gateway | [41258226393](https://github.com/mksglu/cm-ci-lab/actions/runs/41258226393) |
| dedupe-sonnet | 5 | direct-ts | [41258229294](https://github.com/mksglu/cm-ci-lab/actions/runs/41258229294) |
| dedupe-sonnet | 6 | gateway | [41258404674](https://github.com/mksglu/cm-ci-lab/actions/runs/41258404674) |
| dedupe-sonnet | 6 | direct-ts | [41258407351](https://github.com/mksglu/cm-ci-lab/actions/runs/41258407351) |
| dedupe-sonnet | 7 | direct-ts | [41258583637](https://github.com/mksglu/cm-ci-lab/actions/runs/41258583637) |
| dedupe-sonnet | 7 | gateway | [41258586185](https://github.com/mksglu/cm-ci-lab/actions/runs/41258586185) |
| dedupe-sonnet | 8 | gateway | [41258763586](https://github.com/mksglu/cm-ci-lab/actions/runs/41258763586) |
| dedupe-sonnet | 8 | direct-ts | [41258766411](https://github.com/mksglu/cm-ci-lab/actions/runs/41258766411) |
| release-sonnet | 1 | direct-ts | [41258161138](https://github.com/mksglu/cm-ci-lab/actions/runs/41258161138) |
| release-sonnet | 1 | gateway | [41258165203](https://github.com/mksglu/cm-ci-lab/actions/runs/41258165203) |
| release-sonnet | 2 | gateway | [41258341104](https://github.com/mksglu/cm-ci-lab/actions/runs/41258341104) |
| release-sonnet | 2 | direct-ts | [41258344360](https://github.com/mksglu/cm-ci-lab/actions/runs/41258344360) |
| release-sonnet | 3 | direct-ts | [41258525369](https://github.com/mksglu/cm-ci-lab/actions/runs/41258525369) |
| release-sonnet | 3 | gateway | [41258527869](https://github.com/mksglu/cm-ci-lab/actions/runs/41258527869) |
| release-sonnet | 4 | direct-ts | [41258702464](https://github.com/mksglu/cm-ci-lab/actions/runs/41258702464) |
| release-sonnet | 4 | gateway | [41258704990](https://github.com/mksglu/cm-ci-lab/actions/runs/41258704990) |
| release-sonnet | 5 | gateway | [41258886438](https://github.com/mksglu/cm-ci-lab/actions/runs/41258886438) |
| release-sonnet | 5 | direct-ts | [41258889153](https://github.com/mksglu/cm-ci-lab/actions/runs/41258889153) |
| release-sonnet | 6 | direct-ts | [41259067975](https://github.com/mksglu/cm-ci-lab/actions/runs/41259067975) |
| release-sonnet | 6 | gateway | [41259071198](https://github.com/mksglu/cm-ci-lab/actions/runs/41259071198) |
