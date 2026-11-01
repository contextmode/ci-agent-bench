# Dispatch the paired runs of one or more areas, wait for them, download the artifacts, write state.json.
# Same schedule as the published night round: per area, one task every GAP seconds; for each task both arms
# (direct-ts and gateway) are dispatched back to back, in a seeded random order.
# Usage: python3 reproduce/run.py --repo OWNER/NAME --set night-1101-r2 --areas triage,labels --model claude-sonnet-5-5
#        --tasks 2 --gap 150 --out DIR
# Needs `gh` logged in (in Actions: GH_TOKEN with actions:write). Prints no secret.
import json, os, random, subprocess, sys, threading, time

AREAS = ["triage", "mention", "labels", "release", "review-action", "pr-review", "dedupe"]
SPEC_DIRS = {"night-1101-r2": "reproduce/tasks", "confirm-1101": "confirm-1101/tasks"}


def sh(args):
    return subprocess.run(args, capture_output=True, text=True)


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def spec(task_set, area):
    d = SPEC_DIRS.get(task_set)
    if d is None:
        sys.exit(f"unknown task set {task_set}; known: {', '.join(SPEC_DIRS)}")
    f = f"{d}/{area}.json"
    if not os.path.exists(f):
        return None
    return json.load(open(f))


def dispatch(repo, wf, fields):
    args = ["gh", "workflow", "run", wf, "-R", repo]
    for k, v in fields.items():
        args += ["-f", f"{k}={v}"]
    r = sh(args)
    if r.returncode:
        log("dispatch failed", wf, r.stderr.strip()[:300])
    return r.returncode == 0


def find_run(repo, wf, arm, tag):
    for _ in range(60):
        r = sh(["gh", "run", "list", "-R", repo, "--workflow", wf, "-L", "50", "--json", "databaseId,displayTitle"])
        try:
            rows = json.loads(r.stdout)
        except ValueError:
            rows = []
        for x in rows:
            words = x["displayTitle"].split()
            if tag in words and arm in words:
                return x["databaseId"]
        time.sleep(5)
    return None


def lane(repo, area, sp, model, n, gap, out, state):
    wf = os.path.basename(sp.get("workflow") or f"{area}.yml")
    st = state["lanes"][area] = {"model": model, "wf": wf, "runs": []}
    stamp = os.environ.get("GITHUB_RUN_ID") or str(int(time.time()))
    t0 = time.time()
    for i, task in enumerate(sp["tasks"][:n]):
        if "inputs" not in task:
            task["inputs"] = {k: str(task[k]) for k in ("task", "repo", "pr") if k in task}
        wait = t0 + i * gap - time.time()
        if wait > 0:
            time.sleep(wait)
        tag = f"rp{stamp}-{area}-s{i + 1}"
        arms = ["gateway", "direct-ts"]
        random.Random(f"{area}-{i}").shuffle(arms)
        for arm in arms:
            ok = dispatch(repo, wf, dict(task["inputs"], arm=arm, model=model, tag=tag))
            st["runs"].append({"seq": i + 1, "arm": arm, "task": task["inputs"], "tag": tag, "ok": ok})
        log(area, "task", i + 1, "dispatched", task["inputs"])
    for r in st["runs"]:
        if r["ok"]:
            r["rid"] = find_run(repo, wf, r["arm"], r["tag"])
    for r in st["runs"]:
        if not r.get("rid"):
            continue
        for _ in range(240):
            x = sh(["gh", "run", "view", str(r["rid"]), "-R", repo, "--json", "status,conclusion"])
            try:
                j = json.loads(x.stdout)
            except ValueError:
                j = {}
            if j.get("status") == "completed":
                r["conclusion"] = j.get("conclusion")
                break
            time.sleep(20)
        d = f"{out}/art/{r['rid']}"
        os.makedirs(d, exist_ok=True)
        sh(["gh", "run", "download", str(r["rid"]), "-R", repo, "-D", d])
        log(area, "run", r["rid"], r["arm"], r.get("conclusion"))


def main():
    a = sys.argv[1:]
    o = dict(zip(a[0::2], a[1::2]))
    repo, task_set = o["--repo"], o.get("--set", "night-1101-r2")
    model, n, gap, out = o.get("--model", "claude-sonnet-5-5"), int(o.get("--tasks", "7")), int(o.get("--gap", "150")), o.get("--out", "rp-out")
    areas = AREAS if o.get("--areas", "all") == "all" else o["--areas"].split(",")
    os.makedirs(out, exist_ok=True)
    state = {"repo": repo, "task_set": task_set, "model": model, "lanes": {}}
    ths = []
    for area in areas:
        sp = spec(task_set, area)
        if sp is None:
            log("no task spec for", area, "in", task_set, "- skipped")
            continue
        ths.append(threading.Thread(target=lane, args=(repo, area, sp, model, n, gap, out, state)))
    for t in ths:
        t.start()
        time.sleep(2)
    for t in ths:
        t.join()
    json.dump(state, open(f"{out}/state.json", "w"), indent=1)


if __name__ == "__main__":
    main()
