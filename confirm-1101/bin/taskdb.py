"""Find a task by id: confirm-1101/tasks/<area>.json (round 1), then confirm-1101/tasks-r2/<area>.json (round 2). No regex."""
import json, os


def find(area, tid):
    for f in (f"confirm-1101/tasks/{area}.json", f"confirm-1101/tasks-r2/{area}.json"):
        if os.path.exists(f):
            for x in json.load(open(f))["tasks"]:
                if x["id"] == tid:
                    return x
    raise SystemExit(f"unknown task {area} {tid}")
