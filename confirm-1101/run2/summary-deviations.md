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
