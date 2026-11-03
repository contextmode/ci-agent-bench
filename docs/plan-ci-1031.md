# CI benchmark plan (copy of section 5 of the internal plan)

Source: commit b14009360, 2026-10-31 22:27 +0300 (19:27 UTC). The first run of night round 2 started 2026-11-01 04:22 UTC, so this plan was written before the runs. Copied without edits.

## 5. Proof plan
1. Simulator: capture full CI request sequences, replay through the gateway dry-run (free), count tokens with count_tokens, apply cache rules. Must match real API usage within 3%.
2. Build the levers that the simulator shows reach the target (cross-run stable prefix, adaptive TTL, dedup on CI, earlier fold with docid read). Ship each after review, gates and a profile.
3. Paired real runs, sent with the real run gaps, 8 tasks per area, Sonnet then Opus on the top 3 areas. Quality per area: tests pass, blind judge by a different model plus 5 human checks, label F1, top-3 hit. Tool-use mix must not change.
4. Proof sources must agree: client cost, gateway ledger, Anthropic Console bill (within 2%). Everything public and re-runnable in ci-agent-bench.
Pass bar: task-resampled 95% CI upper bound below the target, quality not lower, 0 errors, net saving after our fee > 0, quota checked before and after every round.

