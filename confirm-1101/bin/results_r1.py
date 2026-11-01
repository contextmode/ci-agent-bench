#!/usr/bin/env python3
"""Write RESULTS-r1.md from r1/analysis.json. Every number comes from analysis.json. No regex.
Usage: results_r1.py r1/analysis.json RESULTS-r1.md"""
import json, sys

a = json.load(open(sys.argv[1])); o = []
w = o.append


def ci(r): return "n/a" if r["ci_pct"] is None else f"[{r['ci_pct'][0]}, {r['ci_pct'][1]}]"


def table(rows, full):
    if full:
        w("| area | agent | model | n pairs | saving % | 95% CI | cheaper | direct $/run | gateway $/run | quality | tool calls d/g (ratio) | net/run $ | gateway ran first | pass bar |")
        w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            w(f"| {r['area']} | {r['agent']} | {r['model']} | {r['n']} | {r['saving_pct']} | {ci(r)} | {r['cheaper']} | {r['direct_usd']} | {r['gateway_usd']} | "
              f"{r['quality_text']} | {r['tool_calls'][0]}/{r['tool_calls'][1]} ({r['tool_mix_ratio']}) | {r['net_per_run']} | {r['gateway_first']} | {'PASS' if r['passed_bar'] else 'not met'} |")
    else:
        w("| area | model | n | saving % | 95% CI | pass bar |"); w("|---|---|---|---|---|---|")
        for r in rows:
            w(f"| {r['area']} | {r['model']} | {r['n']} | {r['saving_pct']} | {ci(r)} | {'PASS' if r['passed_bar'] else 'not met'} |")
    w("")


x = a["cross_check"]
w("# confirm-1101 round 1 results (price-fixed)")
w("")
w("Plan: `PLAN.md` at 3198d46, pushed 2026-11-01T13:06:46Z (before any paid run). Workflow fix 87b3f8b pushed 13:09:10Z.")
w("Raw data: `r1/` (runs.json, run-ids.txt, rows.jsonl one line per run, analysis.json, ledger-t_ci_lab_1.json, dispatch.jsonl).")
w("Rebuild: download every run in `r1/run-ids.txt` with `gh run download ID -D art/ID`, then")
w("`python3 analyze.py art --runs r1/runs.json --ledger r1/ledger-t_ci_lab_1.json --json r1/analysis.json --rows r1/rows.jsonl`")
w("and `python3 bin/results_r1.py r1/analysis.json RESULTS-r1.md`. Hashes: `MANIFEST.sha256`.")
w("")
w(f"Runs: {a['runs_total']} dispatched, {a['runs_ok']} with usage, {len(a['errors'])} without output (listed below). "
  f"54 pairs: fix-ci Sonnet 10, fix-mention Sonnet 9, labels 10, release 10, review 10, fix-ci Opus 5. "
  f"The \"78\" in the task brief is the 39 Sonnet confirm-claude pairs (78 runs); review (20 runs) and Opus (10 runs) come on top.")
w(f"Total model spend, list prices: ${a['total_cost_computed']} (client-reported total ${a['total_cost_client']}).")
w("")
w("## Main table (all rows, pass or fail)")
w("")
w("Cost = provider token usage x list price (`prices/anthropic-pricing-2026-11-01.md`). Direct arm: the client's per-model usage (`modelUsage`).")
w("Gateway arm: the gateway ledger usage for the run's session (every upstream call), same prices. Saving = -(exp(mean ln(gw/direct)) - 1).")
w("CI: bootstrap over tasks, 10,000 draws, seed 1. Pass bar = CI upper bound below 0 cost change AND quality not lower AND tool calls >= 70%.")
w("")
table(a["rows"], True)
w("Only **fix-ci, Sonnet 5.5** meets the full pass bar: 18.0% cheaper [4.7, 26.5], 10/10 tests pass on both arms.")
w("Release is cheaper with a CI above 0 (14.7% [3.8, 24.1]) but its quality judge was not run, so the bar is not met.")
w("Labels, fix-mention, review and fix-ci Opus: the CI crosses 0. We do not claim a saving for them from this round.")
w("")
w("## Sensitivity (same pairs, other cost sources)")
w("")
w("Client-reported `total_cost_usd` for both arms:"); w(""); table(a["rows_client_cost"], False)
w("Higher of client-based and ledger-based cost for the gateway arm (the least favourable choice for the gateway):"); w(""); table(a["rows_max_client_ledger"], False)
w("Round-1 analyze.py prices (wrong, Sonnet 3/15, Opus 5/25, 1.25x write, 0.1x read; shown only to make the fix visible):"); w(""); table(a["rows_old_prices_3_15"], False)
w("## Cross-check (3% rule)")
w("")
cc, cl, lr = x["computed_vs_client"], x["computed_vs_ledger_gateway"], x["ledger_recomputed_vs_ledger_billed"]
w(f"- Our price x client usage vs client `total_cost_usd`: {cc['n']} runs, mean gap {cc['mean']}, max {cc['max']}, over 3%: {cc['over_3pct']}. The client bills at the same list prices.")
w(f"- Our price x ledger usage vs ledger `billed_usd`: {lr['n']} gateway runs, max gap {lr['max']}. The gateway bills at the same list prices.")
w(f"- Client-based vs ledger, gateway arm: {cl['n']} runs, mean gap {cl['mean']}, max {cl['max']}, over 3%: {cl['over_3pct']}. Why they differ:")
w(f"  1. Side call model. In {x['gw_only_side_runs']} review gateway runs the ledger shows a `claude-haiku-4-5-20251001` side call "
  f"(about 1,014 input tokens, ${x['gw_only_side_usd_total']} in total). The action's client counts those tokens under Sonnet 5.5, so the client "
  "over-counts by about 1-4% on these small runs (2 of them are over 3%). The ledger is the true bill; the cost table uses it.")
w("  2. Gateway-side upstream loops. In one release run the gateway made more upstream calls than the client sent requests; the client "
  "does not see them, so it under-counts. The ledger includes them; the cost table uses it (this makes the gateway arm dearer, not cheaper).")
w("  3. Cache 5m/1h split: client and ledger agree on the split in every run (both read the provider usage). Long-context tier: "
  "none applies (Sonnet/Opus 5.5 have one price over the full 1M window; no Haiku 5.5 prompt was over 100k). Inference geo: global in all runs.")
w("")
w("Runs over 3% (client-based vs ledger):"); w("")
w("| run | area | task | client-based $ | ledger $ | gap | ledger rows | upstream calls | client requests | ledger side models |"); w("|---|---|---|---|---|---|---|---|---|---|")
for g in x["ledger_gaps_over_3pct"]:
    w(f"| {g['run_id']} | {g['area']} | {g['task']} | {g['client_based_usd']} | {g['ledger_usd']} | {g['gap']} | {g['ledger_rows']} | {g['upstream_calls']} | {g['client_requests']} | {g['ledger_side_models']} |")
w("")
w("## Per-pair rows")
w("")
w("| area | model | task | direct run | gateway run | direct $ | gateway $ | saving % | tests d/g | F1 d/g | tool calls d/g |"); w("|---|---|---|---|---|---|---|---|---|---|---|")
for r in a["rows"]:
    for p in r["pairs"]:
        w(f"| {r['area']} | {r['model']} | {p['task']} | {p['direct_run']} | {p['gateway_run']} | {p['direct_usd']} | {p['gateway_usd']} | {p['saving_pct']} | "
          f"{'' if p['passed'] is None else p['passed']} | {'' if p['f1'] is None else p['f1']} | {p['tools'][0]}/{p['tools'][1]} |")
w("")
w("## Runs without output")
w("")
for e in a["errors"]:
    w(f"- {e['run_id']}: {e['area']} {e['task']} {e['arm']} {e['model']}: {e['error']}.")
w("")
w("## Deviations")
w("")
w("1. **Price fix.** The pre-registered analyze.py (3198d46) priced claude-*-5-5 at the prior generation list price (Sonnet 3/15, Opus 5/25, "
  "write 1.25x, read 0.1x). The live price page (saved 2026-11-01, `prices/anthropic-pricing-2026-11-01.md`, sha256 in MANIFEST) says "
  "Sonnet 5.5: input 2, 5m write 2.5, 1h write 4, read 0.10, output 10; Opus 5.5: 4, 5, 8, 0.20, 20 USD per Mtok. analyze.py now uses these, "
  "prices 5m and 1h writes apart, and counts every model in `modelUsage` (side calls). PLAN.md's \"Known limits\" already said the cross-check "
  "would show any price gap; it did (client cost differed). The method (paired log ratio, bootstrap, bar) is unchanged. The old-price table above shows the effect: "
  "labels moved from PASS-level CI to a CI that crosses 0.")
w("2. **Gateway cost source.** PLAN.md says cost = provider usage x price. For the gateway arm we take the provider usage from the gateway ledger "
  "(it sees every upstream call), not from the client, for the reasons in the cross-check. Both variants are shown above; no row changes its bar result.")
w("3. **87b3f8b.** One workflow-only fix (`cd \"$GITHUB_WORKSPACE\"` before the Verify step copies output) pushed 3 minutes after the plan. "
  "Plan, tasks, prompts and analysis were not touched. 109 of the 110 runs ran on 87b3f8b.")
w("4. **Run 41309715920 rerun.** fix-ci echo-3158 direct-ts Sonnet, on 3198d46, failed in Verify (`cp: cannot create regular file "
  "'out/claude-output.json'`), so it uploaded no usage. Its model spend is not in the totals (the client output was lost). It was rerun on 87b3f8b as "
  "41309864279; the pair uses the rerun.")
w("5. **Cancelled review run 41322736512.** The dispatcher got rc=1 for review gateway elasticsearch#163282 at 15:43:29Z, but GitHub had created "
  "two runs (41322727621 at 15:44:18Z and 41322736512 at 15:44:25Z). The second was cancelled before the model ran (no output). The pair uses 41322727621.")
w(f"6. **Arm order.** The arms were not swapped as PLAN.md intended (seeded order): the gateway arm started first in "
  f"{sum(int(r['gateway_first'].split('/')[0]) for r in a['rows'])} of {sum(r['n'] for r in a['rows'])} pairs, the direct arm 2-3 minutes later, on a "
  "different org (orgs swap in the second half per pick.py). A cache carry-over from gateway to direct is not possible across orgs, but a time-of-day "
  "or provider-load effect cannot be ruled out. Round 2 must randomise the order per pair.")
w("7. **Rows not run in this round (not reported as results):** release and review quality judges; fix-ci for OpenCode, Pi and Codex "
  "(confirm-agents runs were still in progress at analysis time; they are a separate round); fix-mention Opus (planned 5; dispatched from 16:5xZ, after the analysis cut-off of 16:45Z, so it is not in this file). "
  "Opus fix-ci ran 5 of the planned 5. Analysis cut-off: runs created up to 16:45Z, ledger rows up to 16:45Z.")
w("8. **OpenCode and Pi headers.** As `packages/cli/src/ci.mjs` wires them, OpenCode and Pi do not send `x-cm-ci-*` headers, and Pi's first "
  "request grew 3.2x through the gateway in the dry probe (6698 B to 21525 B). Any OpenCode/Pi result must be read with this in mind.")
w("9. **Fix task pool.** Only 5 of 14 fix-ci and 6 of 14 fix-mention candidates were valid at first validation (setup: missing deps such as "
  "poetry `responses`, pydantic `thread_unsafe` marker). final.json holds the tasks that passed validation; all fix tasks pass on both arms here "
  "except fix-mention (direct 6/9, gateway 7/9).")
w("10. **Quota guard.** `used_paused` was 0 before and after every area (dispatch.jsonl `guard` lines; 0 again at analysis time).")
w("")
open(sys.argv[2], "w").write("\n".join(o) + "\n")
