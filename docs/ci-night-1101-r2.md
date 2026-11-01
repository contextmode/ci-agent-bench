# CI night round 2, live gateway after #27 and dedup min 256 B (2026-11-01)

Lab tenant `t_ci_lab_1`. Baseline arm `direct-ts` (direct API + ENABLE_TOOL_SEARCH). Gateway arm uses the CI headers from `lab/path-env.sh`. Sonnet 5.5 only. Driver: `lab/ci-night/orch2.py` (round 1 driver, Opus lanes removed, 7 tasks per lane). Stats: `lab/ci-night/stats.py`, raw output `lab/ci-night/results-r2.json`.

Gateway at the time: #27 (cross-run prefix and adaptive TTL, live since fb5b5004e) and the dedup minimum run of 256 B (87291cf5a), both live.

## Method

Each lane is a sequence of 7 tasks. Both arms run the same task together, one task every 150 s, so the cross-run cache is used. Run 1 is cold; runs 2..7 are warm. Saving = `-(exp(mean log-ratio) - 1)`, positive = gateway cheaper. CI = bootstrap that resamples tasks (10,000, seed 1). Net = mean direct cost - mean gateway cost - $0.0009 x API requests of the gateway run.

## Result: one area reaches 60%? No. Best is dedupe at 52.5% warm.

| area | n pairs (warm/all) | cold (run 1) | warm saving | warm CI | cheaper pairs (warm) | net per run after fee (warm) | valid |
|---|---|---|---|---|---|---|---|
| review-action | 6/7 | 22.1% | 10.5% | -5.4% to 26.8% | 3/6 | $0.0029 | yes |
| mention | 6/7 | 0.2% | 23.7% | 11.4% to 35.7% | 6/6 | $0.0080 | yes |
| triage | 6/7 | 27.4% | 33.9% | 25.1% to 43.6% | 6/6 | $0.0111 | yes |
| pr-review | 6/7 | 24.6% | 7.0% | -26.0% to 29.0% | 4/6 | -$0.0025 | yes |
| labels | 6/7 | -57.7% | 29.6% | 21.1% to 38.8% | 6/6 | $0.0060 | yes |
| dedupe | 6/7 | 74.0% | 52.5% | 24.4% to 71.4% | 6/6 | $0.0761 | yes |
| release | 5/6 | -13.6% | 25.7% | 7.2% to 42.7% | 4/5 | $0.0287 | yes |

Cold is one pair per area, so it has no CI. All-runs numbers (cold + warm): review-action 12.2% (-1.7..26.5), mention 20.7% (8.7..32.8), triage 33.0% (25.4..41.6), pr-review 9.7% (-17.1..28.9), labels 21.0% (-3.2..35.5), dedupe 56.4% (32.9..72.4), release 20.3% (0.4..37.4).

Warm CI excludes zero for: mention, triage, labels, dedupe, release. Not for review-action and pr-review. No area has a warm CI that clears 60%. dedupe has the highest point and the widest CI.

Against round 1 (Sonnet, warm): review-action 18.4 -> 10.5, mention 37.3 -> 23.7, triage 23.9 -> 33.9, pr-review 8.7 -> 7.0, labels 27.5 -> 29.6, dedupe -1.9 -> 52.5, release 13.3 -> 25.7. Mixed. Four areas went up (triage, labels, dedupe, release), three down (review-action, mention, pr-review), and most of the moves are inside the CIs. Only dedupe moved by more than its noise, and its round 1 number had a CI of -104..37. n is 6 per area, so read these as a range.

## Round validity

Quota guard before and after each lane: no request ran paused, mode `full`. Failed workflow runs: 0 of 98. No worker or DO exceeded-memory events in the round window.

## Per area

Quality is what the lab workflow scores. review-action, pr-review and release have no automatic check, so they are not scored. Tool mix is the count of tool calls over the paired runs.

| area | quality direct-ts / gateway | tool mix direct-ts | tool mix gateway | gateway cost split |
|---|---|---|---|---|
| review-action | not scored | Bash 7 | Bash 8 | prefix writes 48.2%, new tool results 21.4%, prefix reads 8.0%, output 23.1% |
| mention | passed 5/7 / 5/7 | Bash 42, Grep 11, Read 10, Edit 5 | Bash 55, Edit 4, Read 3 | prefix writes 10.6%, new tool results 18.6%, prefix reads 35.5%, thinking 6.9%, output 28.7% |
| triage | passed 7/7 / 7/7 | not captured (result-only artifact) | not captured | n/a |
| pr-review | not scored | Bash 7 | Bash 8 | prefix writes 46.4%, new tool results 20.5%, prefix reads 9.0%, output 24.5% |
| labels | f1 pass 5/7 / 4/7 | Bash 9 | Bash 7 | prefix writes 35.3%, new tool results 36.5%, prefix reads 16.7%, output 11.3% |
| dedupe | top3 6/7 / 4/7 | Bash 125, Agent 46, 4 others | Bash 51, Agent 25 | new tool results 54.7%, prefix reads 31.9%, prefix writes 5.5% |
| release | not scored | Bash 60, Write 6, Edit 2 | Bash 38, Write 6 | prefix writes 24.4%, new tool results 22.2%, prefix reads 24.4%, output 27.7% |

Mean cost per run (direct-ts -> gateway): review-action $0.0612 -> $0.0548, mention $0.0864 -> $0.0722, triage $0.0428 -> $0.0276, pr-review $0.0578 -> $0.0558, labels $0.0256 -> $0.0208, dedupe $0.2105 -> $0.1130, release $0.1215 -> $0.0941.

## Read this before quoting the dedupe number

dedupe's saving is partly the gateway arm doing less work: gateway made 76 Bash/Agent calls, direct-ts 175 across the same 7 task pairs, and the gateway arm's top3 score was lower (4/7 against 6/7). A cheaper run that does less and scores lower is not a pure saving. Same flag for labels (f1 pass 4/7 against 5/7). With n = 7 neither quality gap is significant, but we cannot call these savings free.

## Where the remaining cost is

- review-action and pr-review: prefix writes are about 46-48% of the gateway bill and they are single-shot Bash-only runs, so there is little tool output to dedup and little reuse inside a run. These two areas stay near 10%.
- mention and release: prefix reads and output are the big blocks; the per-run tool results are small.
- dedupe: new tool results are 54.7%, so tool-output work still pays there.

## Spend

CI runs of this round: $7.09 (sum of `total_cost_usd` over all 98 workflow runs; cap $20). Tau3 (task 2) spend is in `docs/bench/tau3-n2-1101.md` in the gateway repo.

## Caveats

- n = 6 warm pairs per area (5 for release); one task set, one night.
- Warm vs cold is by position in the sequence; a cold gap of 150 s is not the same as a production gap.
- Quality is the lab's own check, absent for three areas.
- Triage tool mix and cost split are not available (the artifact has no per-message usage).
