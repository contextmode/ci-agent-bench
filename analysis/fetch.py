#!/usr/bin/env python3
"""Download the public Actions artifacts of the confirm-1101 runs (both rounds) into ART_DIR/<run_id>/.

Usage: python3 -I analysis/fetch.py ART_DIR [JOBS]
Needs the gh CLI. Run ids come from confirm-1101/r1/rows.jsonl and confirm-1101/run2/rows.jsonl (successful runs).
GitHub keeps artifacts for 90 days; after that, use the rows files and the ledgers in confirm-1101/. No regex.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def one(args):
    rid, art = args
    d = os.path.join(art, rid)
    if os.path.isdir(d) and os.listdir(d):
        return 0
    return subprocess.run(["gh", "run", "download", rid, "-R", "contextmode/ci-agent-bench", "-D", d], capture_output=True).returncode


def main():
    art, jobs = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ids = set()
    for f in ("confirm-1101/r1/rows.jsonl", "confirm-1101/run2/rows.jsonl"):
        for l in open(os.path.join(LAB, f)):
            r = json.loads(l)
            if r.get("conclusion") == "success":
                ids.add(r["run_id"])
    with ThreadPoolExecutor(jobs) as ex:
        bad = sum(1 for rc in ex.map(one, [(i, art) for i in sorted(ids)]) if rc)
    print(len(ids), "runs,", bad, "failed")


main()
