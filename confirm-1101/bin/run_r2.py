#!/usr/bin/env python3
"""Round-2 driver (PLAN-r2.md section 3 and 8). Reads tasks-r2/schedule.json and dispatches the paired runs.

Usage (from the repo root): python3 confirm-1101/bin/run_r2.py A|B [--dry]
  A: the five Sonnet lanes. B: Opus, OpenCode, Pi, Codex lanes.
Each lane is one thread. It dispatches one run every STEP s, in task order, the pair's first arm (seeded) then the
other arm, so runs of one arm in a lane start >= 2*STEP s apart. A dispatch waits while MAX_FLIGHT lab runs are queued
or running. A lane stops when its spend (finished runs: client cost or proxy usage x list price; in-flight runs: the
round-1 mean) reaches its share. Quota guard before and after each lane; if used_paused grows, every lane stops.
Logs to confirm-1101/run2/dispatch.jsonl. Never reads or prints a key. No regex."""
import json, os, subprocess, sys, threading, time

R = "mksglu/cm-ci-lab"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "run2"); os.makedirs(OUT, exist_ok=True)
ART = "/tmp/cf1101run2/art"; os.makedirs(ART, exist_ok=True)
STEP, MAX_FLIGHT = 75, 18
SHARE = {"cc-sonnet-fix-ci": 3, "cc-sonnet-fix-mention": 6, "cc-sonnet-labels": 3, "cc-sonnet-release": 6,
         "action-sonnet-review": 5, "cc-opus-fix-ci": 4, "cc-opus-fix-mention": 6, "opencode-sonnet-fix-ci": 2,
         "pi-sonnet-fix-ci": 2, "codex-gpt5mini-fix-ci": 4}
EST = {"cc-sonnet-fix-ci": .05, "cc-sonnet-fix-mention": .09, "cc-sonnet-labels": .03, "cc-sonnet-release": .13,
       "action-sonnet-review": .06, "cc-opus-fix-ci": .13, "cc-opus-fix-mention": .26, "opencode-sonnet-fix-ci": .05,
       "pi-sonnet-fix-ci": .06, "codex-gpt5mini-fix-ci": .03}
PHASE = {"A": ["cc-sonnet-fix-ci", "cc-sonnet-fix-mention", "cc-sonnet-labels", "cc-sonnet-release", "action-sonnet-review"],
         "B": ["cc-opus-fix-ci", "cc-opus-fix-mention", "opencode-sonnet-fix-ci", "pi-sonnet-fix-ci", "codex-gpt5mini-fix-ci"]}
# USD per Mtok: input, cache write (5m), cache read, output
PX = {"claude-sonnet-5-5": (2, 2.5, .10, 10), "claude-opus-5-5": (4, 5, .20, 20), "gpt-5-mini": (.25, .25, .025, 2)}
LOCK = threading.Lock(); STOP = threading.Event(); DRY = "--dry" in sys.argv
LOG = open(os.path.join(OUT, "dispatch.jsonl"), "a")
sys.path.insert(0, os.path.join(HERE, "bin"))
from taskdb import find  # noqa: E402


def log(**kw):
    with LOCK:
        LOG.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **kw}) + "\n"); LOG.flush()


def gh(args):
    for i in range(5):
        r = subprocess.run(["gh"] + args, capture_output=True, text=True)
        if r.returncode == 0: return r.stdout
        time.sleep(10 * (i + 1))
    return None


def guard():
    r = subprocess.run(["python3", "/tmp/ci-quota-guard.py", "--need", "500"], capture_output=True, text=True)
    s = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    try: up = json.loads(s.split(" ", 2)[2]).get("used_paused")
    except (ValueError, IndexError, AttributeError): up = None
    return up, s[-300:]


def title(x):
    if x["agent"] == "claude-code": return f"cc {x['area']} {x['task']} {x['arm']} {x['model']}"
    if x["agent"] == "claude-code-action":
        t = find("review", x["task"]); return f"review {x['arm']} {t['repo']}#{t['pr']}"
    return f"{x['agent']} {x['task']} {x['arm']}"


def lane_of_title(sched):
    m = {}
    for r in sched:
        for arm in ("gateway", "direct-ts"):
            m[title(dict(r, arm=arm))] = r["lane"]
    return m


def runs_since(t0):
    s = gh(["run", "list", "-R", R, "-L", "300", "--json", "databaseId,status,conclusion,displayTitle,createdAt,workflowName"])
    return [x for x in json.loads(s or "[]") if x["createdAt"] >= t0]


def run_cost(rid):
    d = os.path.join(ART, str(rid))
    if not os.path.isdir(d):
        gh(["run", "download", str(rid), "-R", R, "-D", d])
        os.makedirs(d, exist_ok=True)
    tot = 0.0
    for root, _, fs in os.walk(d):
        if "norm.json" in fs:
            n = json.load(open(os.path.join(root, "norm.json")))
            if n.get("client_cost") is not None: tot += float(n["client_cost"])
            else:
                p = PX.get(n.get("model"), PX["claude-sonnet-5-5"])
                tot += ((n.get("input") or 0) * p[0] + (n.get("cache_write") or 0) * p[1] + (n.get("cache_read") or 0) * p[2]
                        + (n.get("output") or 0) * p[3]) / 1e6
    return tot


class Spend:
    def __init__(self, t0, sched):
        self.t0, self.l2t, self.done = t0, lane_of_title(sched), {}

    def lane(self, lane):
        fin = flight = 0.0
        for x in runs_since(self.t0):
            if self.l2t.get(x["displayTitle"]) != lane: continue
            if x["status"] == "completed":
                if x["databaseId"] not in self.done: self.done[x["databaseId"]] = run_cost(x["databaseId"])
                fin += self.done[x["databaseId"]]
            else: flight += EST[lane]
        return fin + flight


def in_flight(t0):
    return sum(1 for x in runs_since(t0) if x["status"] != "completed")


def dispatch(x, org):
    if x["agent"] == "claude-code":
        wf, kw = "confirm-claude.yml", dict(area=x["area"], task=x["task"], arm=x["arm"], model=x["model"], org=org)
    elif x["agent"] == "claude-code-action":
        t = find("review", x["task"])
        wf, kw = "confirm-review.yml", dict(repo=t["repo"], pr=str(t["pr"]), arm=x["arm"], model=x["model"], org=org)
    else:
        wf, kw = "confirm-agents.yml", dict(agent=x["agent"], task=x["task"], arm=x["arm"], model=x["model"], org=org)
    if DRY:
        log(dry=True, wf=wf, **kw); return 0
    a = ["gh", "workflow", "run", wf, "-R", R] + [v for k, val in kw.items() for v in ("-f", f"{k}={val}")]
    rc = subprocess.run(a, capture_output=True, text=True).returncode
    log(wf=wf, lane=x["lane"], title=title(x), rc=rc, **kw)
    return rc


def run_lane(lane, rows, t0, spend, up0):
    g = guard(); log(lane=lane, guard_before=g[1])
    seq = []
    for r in rows:
        other = "direct-ts" if r["first_arm"] == "gateway" else "gateway"
        seq += [dict(r, arm=r["first_arm"]), dict(r, arm=other)]
    for i, x in enumerate(seq):
        if STOP.is_set(): log(lane=lane, stopped="global stop", left=len(seq) - i); break
        if i % 2 == 0 and not DRY:  # a pair starts only if the lane is under its share
            s = spend.lane(lane)
            if s + 2 * EST[lane] > SHARE[lane]:
                log(lane=lane, stopped="share", spend=round(s, 4), left=len(seq) - i); break
        while not DRY and in_flight(t0) >= MAX_FLIGHT and not STOP.is_set(): time.sleep(30)
        dispatch(x, x["orgs"][x["arm"]])
        time.sleep(0 if DRY else STEP)
    g = guard(); log(lane=lane, guard_after=g[1])
    if g[0] is not None and up0 is not None and g[0] > up0:
        log(lane=lane, alarm="used_paused grew", before=up0, after=g[0]); STOP.set()


def main():
    ph = sys.argv[1]
    sched = json.load(open(os.path.join(HERE, "tasks-r2", "schedule.json")))["runs"]
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    up0, g = guard(); log(phase=ph, start=t0, guard_before=g, dry=DRY)
    if up0 is None and not DRY: raise SystemExit("quota guard gave no used_paused")
    spend = Spend(t0, sched)
    th = [threading.Thread(target=run_lane, args=(ln, [r for r in sched if r["lane"] == ln], t0, spend, up0)) for ln in PHASE[ph]]
    for t in th: t.start(); time.sleep(0 if DRY else 15)
    for t in th: t.join()
    while not DRY and in_flight(t0): time.sleep(60)
    up1, g = guard(); log(phase=ph, end=True, guard_after=g, used_paused_grew=(up1 or 0) > (up0 or 0))


if __name__ == "__main__":
    main()
