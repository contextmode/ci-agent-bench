# confirm-1101 plan (pre-registered; committed before any paid run)

## Areas, models, n
| area | agent | model | n tasks | arms |
|---|---|---|---|---|
| fix-ci | Claude Code | claude-sonnet-5-5 | 10 | direct-ts, gateway |
| fix-mention (@claude fix) | Claude Code | claude-sonnet-5-5 | 9 | direct-ts, gateway |
| labels | Claude Code | claude-sonnet-5-5 | 10 | direct-ts, gateway |
| release | Claude Code | claude-sonnet-5-5 | 10 | direct-ts, gateway |
| review | anthropics/claude-code-action@v1 | claude-sonnet-5-5 | 10 | direct-ts, gateway |
| fix-ci | Claude Code | claude-opus-5-5 | first 5 of fix-ci | direct-ts, gateway |
| fix-mention | Claude Code | claude-opus-5-5 | first 5 of fix-mention | direct-ts, gateway |
| fix-ci | OpenCode, Pi (claude-sonnet-5-5), Codex (gpt-5-mini) | | first 5 of fix-ci | direct-ts, gateway |

Tasks: tasks/<area>.json (seeded by pick.py), filtered by validation.json (bin/final.py -> final.json). A fix task is valid
only if its baseline fails and its control passes; an invalid task is replaced by the next one in seeded order.
Task-count cut: the 10 (or 9) valid tasks are the sample; no task is dropped after a run for any reason.

## Arms
direct-ts vs gateway. Same model, prompt, tools, repo snapshot. direct-ts = ENABLE_TOOL_SEARCH on, no base URL change.
gateway = base URL + x-cm-* headers from lab/path-env.sh. Each agent installs with its own native command.
Non-Claude agents run behind a recording pass-through proxy on both arms (bin/usageproxy.py), which reads the provider usage.
Orgs: as set by pick.py (gateway and direct-ts of a task run on different orgs; the roles swap in the second half). Review: bmksglu.
Keys: ANTHROPIC_API_KEY_D (mert2), ANTHROPIC_API_KEY_C (bmksglu), OPENAI_API_KEY (Codex). No other key.
Arrival: the two arms of a task start 2-3 minutes apart; tasks run in seeded order, a few at a time.

## Metrics
- Primary: per-task paired log cost ratio ln(gateway/direct-ts). Cost = provider usage tokens x published price (analyze.py PRICES).
  Saving % = -(exp(mean) - 1). 95% CI: bootstrap that resamples tasks, 10,000 draws, seed 1.
- Cross-check: client-reported cost (Claude total_cost_usd) vs computed cost, and vs the gateway ledger (admin snapshot delta
  before/after each area), must agree within 3%. Reported either way.
- Net per run = mean direct cost - mean gateway cost - $0.0009 x mean gateway API requests.
- Quality: fix areas = tests pass, exact McNemar on discordant pairs; labels = F1 (lab/labels/extract.py); release and review =
  blind judge from a different model (see judge workflow), win/tie/loss and score diff.
- Tool mix: tool calls per arm by name; ratio gateway/direct total tool calls.

## Pass bar (all three)
1. Upper bound of the 95% cost CI is below 0 (gateway cheaper).
2. Quality not lower (McNemar p >= 0.05 against gateway, F1 mean not lower by more than CI, judge not worse).
3. Gateway tool calls >= 70% of direct-ts.
Every row is reported, pass or fail. Failed runs count at their cost; a run with no usage is reported as an error row, not removed.

## Guards
python3 /tmp/ci-quota-guard.py --need 500 before and after each area (used_paused must not grow).
Caps: $45 Anthropic, $4 OpenAI.

## Known limits (stated before the runs)
- Prices for claude-*-5-5 are taken as the list price of the prior generation (Sonnet 3/15, Opus 5/25 per Mtok; cache write 1.25x,
  cache read 0.1x); the cross-check against client cost shows any gap.
- Codex dry probe reached the gateway (200, device key and x-cm-ci headers sent) but the dry reply did not decode, so "request 1
  changed" is not verified for Codex. OpenCode and Pi: key and headers reached the gateway, request 1 changed. See RESULTS.md.
