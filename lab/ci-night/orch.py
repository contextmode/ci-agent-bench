# Round 1 orchestrator (2026-11-01). Dispatches lab workflows as sequences, both arms together, one task every GAP seconds.
# Usage: python3 -I orch.py   (state in /tmp/cm-ci-lab-r1/state.json, log in orch.log)
import json, os, random, subprocess, sys, threading, time

REPO = "mksglu/cm-ci-lab"
OUT = "/tmp/cm-ci-lab-r1"
GAP = 150
MAXLANES = 4
BASE = {"review-action": "direct-ts", "pr-review": "direct-ts", "mention": "direct-ts", "triage": "direct-ts",
        "opus-triage": "direct-ts", "labels": "direct-ts", "dedupe": "direct-ts", "release": "direct-ts"}
PRS = [("facebook/react", "38034"), ("microsoft/vscode", "345293"), ("vercel/next.js", "100956"), ("langchain-ai/langchain", "41520"),
       ("astral-sh/uv", "23017"), ("denoland/deno", "37046"), ("facebook/react", "38025"), ("microsoft/vscode", "345283")]
S, O = "claude-sonnet-5-5", "claude-opus-5-5"
LANES = [
    dict(name="review-action-sonnet", wf="review-action", model=S, n=8, tasks=[dict(repo=r, pr=p) for r, p in PRS]),
    dict(name="review-action-opus", wf="review-action", model=O, n=6, tasks=[dict(repo=r, pr=p) for r, p in PRS]),
    dict(name="mention-sonnet", wf="mention", model=S, n=8, tasks=[dict(task=t) for t in "gin flask cobra ripgrep rich chalk fd dayjs".split()]),
    dict(name="mention-opus", wf="mention", model=O, n=6, tasks=[dict(task=t) for t in "gin flask cobra ripgrep rich chalk".split()]),
    dict(name="triage-sonnet", wf="triage", model=S, n=8, tasks=[dict(task=t) for t in "requests flask express koa cobra ripgrep rich black".split()]),
    dict(name="triage-opus", wf="opus-triage", model=O, n=6, tasks=[dict(task=t) for t in "requests flask express koa cobra ripgrep".split()]),
    dict(name="pr-review-sonnet", wf="pr-review", model=S, n=8, tasks=[dict(repo=r, pr=p) for r, p in PRS]),
    dict(name="labels-sonnet", wf="labels", model=S, n=8, tasks=[dict(task=t) for t in "godot-124950 zed-66189 tauri-16340 bun-47090 rust-165173 vscode-345117 godot-124937 zed-66163".split()]),
    dict(name="dedupe-sonnet", wf="dedupe", model=S, n=8, tasks=[dict(task=t) for t in "bun-37251 claude-code-104074 codex-52463 gemini-cli-25559 uptime-kuma-6474 bun-37028 claude-code-103661 codex-50880".split()]),
    dict(name="release-sonnet", wf="release", model=S, n=6, tasks=[dict(task=t) for t in "gemini-66 uv-135 mcp-21 rg-152 zod-466 ruff-173".split()]),
]
lock = threading.Lock()
state = {"lanes": {}}

def log(*a):
    with lock:
        with open(f"{OUT}/orch.log", "a") as f:
            f.write(time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a) + "\n")

def save():
    with lock:
        json.dump(state, open(f"{OUT}/state.json", "w"), indent=1)

def sh(args, check=False):
    return subprocess.run(args, capture_output=True, text=True)

def guard():
    r = sh(["python3", "/tmp/ci-quota-guard.py", "--need", "500"])
    line = (r.stdout.strip().splitlines() or [""])[-1]
    try: j = json.loads(line[line.index("{"):])
    except Exception: j = {"raw": line}
    return j

def dispatch(wf, fields):
    args = ["gh", "workflow", "run", f"{wf}.yml", "-R", REPO]
    for k, v in fields.items(): args += ["-f", f"{k}={v}"]
    r = sh(args)
    if r.returncode: log("DISPATCH FAIL", wf, fields, r.stderr.strip()[:200])
    return r.returncode == 0

def find_run(wf, arm, tag):
    for _ in range(30):
        r = sh(["gh", "run", "list", "-R", REPO, "--workflow", f"{wf}.yml", "-L", "40", "--json", "databaseId,displayTitle,status,conclusion"])
        try: rows = json.loads(r.stdout)
        except Exception: rows = []
        for x in rows:
            t = x["displayTitle"].split()
            if tag in t and arm in t: return x["databaseId"]
        time.sleep(5)
    return None

def lane(L, sem):
    with sem:
        name, wf, model = L["name"], L["wf"], L["model"]
        st = state["lanes"][name] = {"model": model, "wf": wf, "guard_before": guard(), "runs": []}
        log("LANE START", name, st["guard_before"]); save()
        t0 = time.time()
        for i, task in enumerate(L["tasks"][:L["n"]]):
            wait = t0 + i * GAP - time.time()
            if wait > 0: time.sleep(wait)
            tag = f"c1101-r1-{name}-s{i+1}"
            arms = ["gateway", BASE[wf]]; random.Random(f"{name}-{i}").shuffle(arms)
            for arm in arms:
                f = dict(task, arm=arm, model=model, tag=tag)
                ok = dispatch(wf, f)
                st["runs"].append({"seq": i + 1, "arm": arm, "task": task, "tag": tag, "t": time.time(), "ok": ok})
            save()
        for r in st["runs"]:
            if r["ok"]:
                r["rid"] = find_run(wf, r["arm"], r["tag"])
        save()
        for r in st["runs"]:
            if not r.get("rid"): continue
            for _ in range(180):
                x = sh(["gh", "run", "view", str(r["rid"]), "-R", REPO, "--json", "status,conclusion"])
                try: j = json.loads(x.stdout)
                except Exception: j = {}
                if j.get("status") == "completed":
                    r["conclusion"] = j.get("conclusion"); break
                time.sleep(20)
            d = f"{OUT}/art/{r['rid']}"
            os.makedirs(d, exist_ok=True)
            sh(["gh", "run", "download", str(r["rid"]), "-R", REPO, "-D", d])
        st["guard_after"] = guard()
        log("LANE DONE", name, st["guard_after"]); save()

if __name__ == "__main__":
    only = sys.argv[1:]
    sem = threading.Semaphore(MAXLANES)
    state["guard_start"] = guard(); log("ROUND START", state["guard_start"])
    ths = [threading.Thread(target=lane, args=(L, sem)) for L in LANES if not only or L["name"] in only]
    for t in ths: t.start(); time.sleep(2)
    for t in ths: t.join()
    state["guard_end"] = guard(); save(); log("ROUND END", state["guard_end"])
