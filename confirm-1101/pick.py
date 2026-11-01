#!/usr/bin/env python3
"""Pre-registered task selection for confirm-1101. Fixed seed; no model; no regex.
Writes tasks/<area>.json from pools/*.json.
Order inside a pool: sha256("confirm-1101|<repo>|<item>") lowest first (fix pools are already in their
interleaved draw order from build_fix.py and keep it). Each area lists N tasks plus RESERVE reserves; a task that
fails validation (fix areas: baseline must fail, control must pass) is replaced by the next reserve in order.
Org plan: task i (0-based) runs gateway on ORG_A in the first half and on ORG_B in the second half; direct-ts runs
on the other org. The official action (area review) runs on bmksglu only (both arms)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pools"))
from common import draw_key  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESERVE = 4
ORGS = ("mert2", "bmksglu")
AREAS = {  # area: (pool file, item key, N for the largest agent)
    "fix-ci": ("fix-ci.json", "pr", 10),
    "fix-mention": ("fix-mention.json", "pr", 10),
    "labels": ("labels.json", "number", 10),
    "release": ("release.json", "tag", 10),
    "review": ("review.json", "pr", 10),
}


def orgs_for(i, n, area):
    if area == "review":
        return {"gateway": "bmksglu", "direct-ts": "bmksglu"}
    first = i < (n + 1) // 2
    return {"gateway": ORGS[0] if first else ORGS[1], "direct-ts": ORGS[1] if first else ORGS[0]}


def main():
    for area, (pool, key, n) in AREAS.items():
        d = json.load(open(os.path.join(HERE, "pools", pool)))
        c = d["candidates"]
        if not area.startswith("fix"):
            c = sorted(c, key=lambda x: draw_key(x["repo"], x[key]))
        c = c[:n + RESERVE]
        tasks = []
        for i, t in enumerate(c):
            t = dict(t)
            t["seq"] = i + 1
            t["reserve"] = i >= n
            t["orgs"] = orgs_for(i, n, area)
            tasks.append(t)
        out = {"area": area, "seed": "confirm-1101", "pool": pool, "n": n, "reserve": RESERVE, "tasks": tasks}
        json.dump(out, open(os.path.join(HERE, "tasks", area + ".json"), "w"), indent=1)
        print(area, len(tasks), [t["id"] for t in tasks])


if __name__ == "__main__":
    main()
