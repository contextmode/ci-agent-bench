#!/usr/bin/env python3
"""Round-2 task selection and run schedule for confirm-1101 (PLAN-r2.md). Fixed seeds; no model; no regex.
Usage: python3 pick_r2.py            writes tasks-r2/<area>.json and tasks-r2/schedule.json

Used set U: every task id dispatched in round 1 (run titles in r2/runs.json). No task in U is ever picked.
fix-ci, fix-mention: candidate order = round-1 task order (tasks/<area>.json) minus U, then the round-2 pool
  (pools/r2/fix-<area>.json: build_fix.py with PER_REPO=10, F8). A candidate is valid only if validation.json
  (latest row per task and mode) has baseline valid and control valid. The first N valid candidates are the tasks.
labels, release, review: pools/<area>.json in sha256 draw order (seed confirm-1101), minus U.
Lanes (agent, model, area, n) are in LANES. Each lane uses the first n tasks of its area.
Orgs: in each lane, task i < ceil(n/2) runs gateway on mert2 and direct-ts on bmksglu; the rest swap.
  Codex uses OPENAI_API_KEY in both arms (org is recorded but not used).
Arm order: in each lane, rank tasks by sha256("confirm-1101-r2|<lane>|<id>"); even rank -> gateway first,
  odd rank -> direct-ts first. This gives an exact half/half split."""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "pools"))
from common import draw_key  # noqa: E402

SEED2 = "confirm-1101-r2"
ORGS = ("mert2", "bmksglu")
S, O, G = "claude-sonnet-5-5", "claude-opus-5-5", "gpt-5-mini"
N = {"fix-ci": 16, "fix-mention": 16, "labels": 16, "release": 16, "review": 16}
LANES = [  # lane id, agent, model, area, n
    ("cc-sonnet-fix-ci", "claude-code", S, "fix-ci", 16),
    ("cc-sonnet-fix-mention", "claude-code", S, "fix-mention", 16),
    ("cc-sonnet-labels", "claude-code", S, "labels", 16),
    ("cc-sonnet-release", "claude-code", S, "release", 16),
    ("action-sonnet-review", "claude-code-action", S, "review", 16),
    ("cc-opus-fix-ci", "claude-code", O, "fix-ci", 8),
    ("cc-opus-fix-mention", "claude-code", O, "fix-mention", 8),
    ("opencode-sonnet-fix-ci", "opencode", S, "fix-ci", 8),
    ("pi-sonnet-fix-ci", "pi", S, "fix-ci", 8),
    ("codex-gpt5mini-fix-ci", "codex", G, "fix-ci", 6),
]
KEY = {"labels": "number", "release": "tag", "review": "pr"}


def used_r1():
    u = set()
    for r in json.load(open(os.path.join(HERE, "r2", "runs.json"))):
        t = r["displayTitle"].split()
        if t[0] == "cc":
            u.add((t[1], t[2]))
        elif t[0] == "review":
            rp, pr = t[2].split("#")
            u.add(("review", rp.split("/")[1] + "-" + pr))
        else:
            u.add(("fix-ci", t[1]))
    return u


def validity():
    st = {}
    for v in json.load(open(os.path.join(HERE, "validation.json"))):
        st.setdefault((v["area"], v["task"]), {})[v["mode"]] = v["valid"]
    return st


def main():
    U, st = used_r1(), validity()
    picked = {}
    for area, n in N.items():
        if area.startswith("fix"):
            r1 = json.load(open(os.path.join(HERE, "tasks", area + ".json")))["tasks"]
            r2 = json.load(open(os.path.join(HERE, "pools", "r2", area + ".json")))["candidates"]
            cands = [dict(t, origin="r1-pool") for t in r1] + [dict(t, origin="r2-pool") for t in r2]
        else:
            c = json.load(open(os.path.join(HERE, "pools", area + ".json")))["candidates"]
            cands = [dict(t, origin="pool") for t in sorted(c, key=lambda x: draw_key(x["repo"], x[KEY[area]]))]
        out, seen = [], set()
        for t in cands:
            if (area, t["id"]) in U or t["id"] in seen:
                continue
            seen.add(t["id"])
            for k in ("seq", "reserve", "orgs"):
                t.pop(k, None)
            s = st.get((area, t["id"]), {})
            t["valid"] = (s.get("baseline") is True and s.get("control") is True) if area.startswith("fix") else True
            t["validated"] = ("baseline" in s and "control" in s) if area.startswith("fix") else True
            out.append(t)
        sel = [t["id"] for t in out if t["valid"]][:n]
        for i, t in enumerate(out):
            t["cand_seq"] = i + 1
            t["selected"] = t["id"] in sel
        picked[area] = sel
        json.dump({"area": area, "seed": SEED2, "n": n, "used_r1_excluded": sorted(x[1] for x in U if x[0] == area),
                   "selected": sel, "tasks": out}, open(os.path.join(HERE, "tasks-r2", area + ".json"), "w"), indent=1)
        print(area, "candidates", len(out), "valid", sum(t["valid"] for t in out), "selected", len(sel))
    sched = []
    for lane, agent, model, area, n in LANES:
        ids = picked[area][:n]
        rank = {i: r for r, i in enumerate(sorted(ids, key=lambda i: hashlib.sha256(f"{SEED2}|{lane}|{i}".encode()).hexdigest()))}
        half = (n + 1) // 2
        for i, tid in enumerate(ids):
            first = i < half
            sched.append({"lane": lane, "agent": agent, "model": model, "area": area, "task": tid, "seq": i + 1,
                          "orgs": {"gateway": ORGS[0] if first else ORGS[1], "direct-ts": ORGS[1] if first else ORGS[0]},
                          "first_arm": "gateway" if rank[tid] % 2 == 0 else "direct-ts"})
        print(lane, len(ids), "of", n)
    json.dump({"seed": SEED2, "lanes": LANES, "runs": sched}, open(os.path.join(HERE, "tasks-r2", "schedule.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
