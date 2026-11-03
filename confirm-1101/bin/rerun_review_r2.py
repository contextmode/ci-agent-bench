#!/usr/bin/env python3
"""Round-2 review re-run (RESULTS-r2.md Deviations). The mert2 org cannot run the claude-code-action entrypoint
("Credit balance is too low"; sdk-cli on mert2 works), so every round-2 review run on mert2 failed in both arms.
This re-dispatches exactly those runs on bmksglu, the round-1 review org. One run every 60 s, arms interleaved,
so runs of one arm start >= 120 s apart. Quota guard before and after. Never reads a key. No regex.
Usage (repo root): python3 confirm-1101/bin/rerun_review_r2.py"""
import json, os, subprocess, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "contextmode/ci-agent-bench"
LOG = open(os.path.join(HERE, "run2", "dispatch-review-rerun.jsonl"), "a")
def log(**kw):
    LOG.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **kw}) + "\n"); LOG.flush()
def guard():
    r = subprocess.run(["python3", "/tmp/ci-quota-guard.py", "--need", "500"], capture_output=True, text=True)
    return r.stdout.strip().splitlines()[-1][-300:] if r.stdout.strip() else ""
D = [json.loads(l) for l in open(os.path.join(HERE, "run2", "dispatch.jsonl"))]
fail = [x for x in D if x.get("wf") == "confirm-review.yml" and x.get("org") == "mert2"]
g = [x for x in fail if x["arm"] == "gateway"]; d = [x for x in fail if x["arm"] == "direct-ts"]
seq = [y for pair in zip(g, d) for y in pair] + g[len(d):] + d[len(g):]
log(start=True, n=len(seq), guard_before=guard())
for x in seq:
    a = ["gh", "workflow", "run", "confirm-review.yml", "-R", R, "-f", "repo=" + x["repo"], "-f", "pr=" + str(x["pr"]),
         "-f", "arm=" + x["arm"], "-f", "model=" + x["model"], "-f", "org=bmksglu"]
    rc = subprocess.run(a, capture_output=True, text=True).returncode
    log(wf="confirm-review.yml", title=x["title"], arm=x["arm"], repo=x["repo"], pr=x["pr"], org="bmksglu", rc=rc, replaces_org="mert2")
    time.sleep(60)
log(end_dispatch=True, guard_after=guard())
