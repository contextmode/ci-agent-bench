#!/usr/bin/env python3
"""Final task list per area. Reads tasks/<area>.json (seeded order) and validation.json. A fix task is valid only if
its baseline fails and its control passes; an invalid task is replaced by the next one in seeded order. Writes final.json.
Opus and the OpenCode/Pi lanes use the first K valid tasks of the same list (K set in PLAN.md). No regex."""
import json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import pick  # noqa: E402
val = {(x["area"], x["task"], x["mode"]): x["valid"] for x in json.load(open(os.path.join(HERE, "validation.json")))}
final = {}
for area, (_, _, n) in pick.AREAS.items():
    tasks = json.load(open(os.path.join(HERE, "tasks", area + ".json")))["tasks"]
    if area.startswith("fix"):
        tasks = [t for t in tasks if val.get((area, t["id"], "baseline")) and val.get((area, t["id"], "control"))][:n]
    else:
        tasks = tasks[:n]
    final[area] = [{"id": t["id"], "orgs": pick.orgs_for(i, len(tasks), area)} for i, t in enumerate(tasks)]
    print(area, len(tasks), [t["id"] for t in final[area]])
json.dump(final, open(os.path.join(HERE, "final.json"), "w"), indent=1)
