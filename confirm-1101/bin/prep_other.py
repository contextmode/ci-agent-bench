#!/usr/bin/env python3
"""Prepare labels / release tasks and the mention prompt from confirm-1101/tasks. Usage: prep_other.py <labels|release|mention-prompt> <task-id>
labels: $RUNNER_TEMP/work (scripts, prompt.txt, tasks.json list for extract.py); writes TASK_* to $GITHUB_ENV.
release: runs the lab prep.sh with REL_* taken from the task file. mention-prompt: prints the prompt. No regex."""
import json, os, subprocess, sys

kind, tid = sys.argv[1], sys.argv[2]
area = {"labels": "labels", "release": "release", "mention-prompt": "fix-mention"}[kind]
t = next(x for x in json.load(open(f"confirm-1101/tasks/{area}.json"))["tasks"] if x["id"] == tid)
tmp = os.environ.get("RUNNER_TEMP", "/tmp")
env = os.environ.get("GITHUB_ENV")
if kind == "labels":
    w = os.path.join(tmp, "work"); os.makedirs(os.path.join(w, "scripts"), exist_ok=True)
    for f in os.listdir("lab/labels/scripts"):
        open(os.path.join(w, "scripts", f), "w").write(open(os.path.join("lab/labels/scripts", f)).read())
        os.chmod(os.path.join(w, "scripts", f), 0o755)
    p = open("lab/labels/prompt.md").read().replace("__REPO__", t["repo"]).replace("__NUMBER__", str(t["number"]))
    open(os.path.join(w, "prompt.txt"), "w").write(p)
    json.dump([t], open(os.path.join(w, "tasks.json"), "w"))
    with open(env, "a") as f:
        f.write(f"TASK_REPO={t['repo']}\nTASK_NUMBER={t['number']}\nTASK_CREATED={t['created']}\n")
elif kind == "release":
    s = open("lab/release/prep.sh").read()
    a = s.index('. "$here/tasks.sh"')
    b = s.index("\n", a)
    s = s[:a] + 'REL_REPO="$P_REPO"; REL_TAG="$P_TAG"; REL_PREV="$P_PREV"; REL_NAME="$P_NAME"' + s[b:]
    open(os.path.join(tmp, "prep_rel.sh"), "w").write(s)
    e = dict(os.environ, P_REPO=t["repo"], P_TAG=t["tag"], P_PREV=t["prev"], P_NAME=t["name"])
    subprocess.run(["bash", os.path.join(tmp, "prep_rel.sh"), tid], check=True, env=e)
else:
    i = t["issue"]
    os.makedirs("lab/mention/issues", exist_ok=True)
    json.dump({"repo": t["repo"], "number": i["number"], "title": i["title"], "body": i["body"], "author": i["author"],
               "created": i["created"], "state": i["state"]}, open(f"lab/mention/issues/{tid}.json", "w"))
    sys.stdout.write(subprocess.run(["python3", "lab/mention/prompt.py", tid], check=True, capture_output=True, text=True).stdout)
