#!/usr/bin/env python3
"""How often do real repos rerun the same CI agent job? Counts runs and the median gap between runs of one workflow.

Usage: python3 -I analysis/rerun-gap.py OWNER/REPO WORKFLOW_FILE SINCE UNTIL     (dates as YYYY-MM-DD, UTC)
Needs the gh CLI (public GitHub API, any token). Example:
  python3 -I analysis/rerun-gap.py anthropics/claude-code claude-issue-triage.yml 2026-10-25 2026-11-01
Only runs that finished as success or failure count (a skipped run ran no agent).
Output: runs, median gap in minutes, share of gaps under 5 minutes and under 60 minutes. No regex.
"""
import json, statistics as st, subprocess, sys
from datetime import datetime, timedelta


def days(since, until):
    a, b = datetime.strptime(since, "%Y-%m-%d"), datetime.strptime(until, "%Y-%m-%d")
    while a < b:
        yield a.strftime("%Y-%m-%d"), (a + timedelta(days=1)).strftime("%Y-%m-%d")
        a += timedelta(days=1)


def runs(repo, wf, since, until):
    """One query per day (the API returns at most 1000 runs per query), so a busy repo is not cut off."""
    out = []
    for d0, d1 in days(since, until):
        page = 1
        while True:
            url = f"repos/{repo}/actions/workflows/{wf}/runs?per_page=100&page={page}&created={d0}..{d1}"
            r = subprocess.run(["gh", "api", url], capture_output=True, text=True)
            if r.returncode:
                sys.exit(r.stderr)
            got = json.loads(r.stdout).get("workflow_runs", [])
            out += [x["created_at"] for x in got if x.get("conclusion") in ("success", "failure")]  # skipped and cancelled runs ran no job
            if len(got) < 100 or page >= 10:
                break
            page += 1
    return sorted(set(out))


def main():
    repo, wf, since, until = sys.argv[1:5]
    t = sorted(datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ") for x in runs(repo, wf, since, until))
    gaps = [(b - a).total_seconds() / 60 for a, b in zip(t, t[1:])]
    if not gaps:
        print(repo, wf, "runs", len(t)); return
    print(f"{repo} {wf} {since}..{until}: runs {len(t)}, median gap {st.median(gaps):.1f} min, "
          f"gaps under 5 min {100 * sum(g < 5 for g in gaps) / len(gaps):.0f}%, under 60 min {100 * sum(g < 60 for g in gaps) / len(gaps):.0f}%")


main()
