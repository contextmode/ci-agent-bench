# Analysis: the numbers in the Headless CI posts

Every number in the posts below can be rebuilt from public data with the scripts in this folder.
Date of the recompute: 2026-11-02. Scripts use no regex and no key. Python 3 and the `gh` CLI are enough.

Posts: `how-context-mode-cuts-ci-agent-cost`, `where-the-money-goes-in-a-ci-agent-run`,
`what-we-learned-measuring-ai-agents-in-ci` on https://contextmode.ai/blog.

## Inputs

- Actions artifacts of the confirm-1101 runs (round 1 and round 2). Run ids: `confirm-1101/r1/rows.jsonl`, `confirm-1101/run2/rows.jsonl`.
- GitHub API, for how often real repos rerun a job.
- The saved provider price page: `confirm-1101/prices/anthropic-pricing-2026-11-01.md`.

Scope: Sonnet 5.5, Claude Code, the three jobs the website shows (CI failure fix, @claude fix, issue labels). The cost split uses the
direct arm only (no Context Mode). Request 1 compares the direct arm with the gateway arm. Add `--all` to include the other jobs in the rows.

## Run it

```
python3 -I analysis/fetch.py art                      # download the artifacts (about 350 runs)
python3 -I analysis/cost-split.py art --json analysis/results/cost-split.json
python3 -I analysis/request1.py art --json analysis/results/request1.json
python3 -I analysis/price-ratio.py
python3 -I analysis/rerun-gap.py anthropics/claude-code claude-issue-triage.yml 2026-10-25 2026-11-01
```

Output of each command is saved in `analysis/results/`.

## Results

### 1. Cost split of a direct run (`cost-split.py`)

| Job | Runs | Requests per run | Fixed prefix | Tool results and history | Thinking | Answer | Cache writes, share of bill |
|---|---|---|---|---|---|---|---|
| CI failure fix | 26 | 6.3 | 48.3% | 25.4% | 4.3% | 22.0% | 47.2% |
| @claude fix | 28 | 9.4 | 44.3% | 22.2% | 5.2% | 28.2% | 42.2% |
| Issue labels | 36 | 2.3 | 58.0% | 32.4% | 0.8% | 8.8% | 78.3% |
| Mean over the three jobs | | | 50.2% | 26.7% | 3.4% | 19.7% | |

Method. Each request is priced from the provider's token counts at list price. Fixed prefix = the request-1 cache write and input,
plus every cache read (reads re-read the prefix). Tool results and history = cache writes and uncached input after request 1.
Thinking = `thinking_tokens` of the result event, priced as output. Answer = the rest of the output. The mean is the plain mean of the three jobs.

The earlier posts said 33 / 33 / 7 / 27 and "65% to 78%". Those came from a private run. The posts now use the table above.

### 2. Request 1 size (`request1.py`)

| Job | Direct | Gateway | Smaller |
|---|---|---|---|
| CI failure fix | 18,683 | 11,574 | 38.1% |
| @claude fix | 22,836 | 15,722 | 31.2% |
| Issue labels | 16,771 | 11,341 | 32.4% |

Size = input + cache write + cache read tokens of the first main-agent request, mean over runs. The earlier "30% to 42%" came from a
private round and the posts now say 31% to 38%.

### 3. Rerun gaps of real repos (`rerun-gap.py`, GitHub API)

| Repo and workflow | Runs in 7 days | Median gap | Under 5 min | Under 60 min |
|---|---|---|---|---|
| anthropics/claude-code, Claude Issue Triage | 3,853 | 1.8 min | 81% | 100% |
| lobehub/lobehub, Claude PR Assign | 475 | 11.6 min | 27% | 92% |
| pytorch/pytorch, Claude Code | 324 | 11.4 min | 38% | 89% |

Window 2026-10-25 to 2026-11-01 UTC, read on 2026-11-02. The API keeps history, so a later read of the same window gives the same
counts, with small changes when GitHub prunes runs. The earlier "985 runs, 1.9 min" counted fewer runs and is replaced.

### 4. Cache write and read prices (`price-ratio.py`)

Sonnet 5.5, USD per million tokens: input 2.00, 5-minute write 2.50, 1-hour write 4.00, read 0.10.

- 5-minute write / read = 25 to 1. 1-hour write / read = 40 to 1.
- Break-even for removing n tokens inside a cached prefix of P tokens when the cut breaks the cache: n x later turns > 24 x P (5 minutes), > 39 x P (1 hour).
- In the lab, 336 of 346 run artifacts show only 5-minute cache writes; the other 10 wrote some 1-hour cache.

The earlier "20 to 1" came from older prices and is replaced.

### 5. Removed: "run 2 read 10,543 tokens and wrote 0"

That number was measured on one local run, and the raw usage rows are not in this lab. It cannot be rebuilt here, so it is removed from the post.
