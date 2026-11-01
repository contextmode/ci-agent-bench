#!/usr/bin/env python3
"""Prepare one fix task in $RUNNER_TEMP/repo. Usage: prep_fix.py <area> <task-id> [control]
area fix-ci: repo at the merge commit with the source fix reverted (tests kept). Fails again by design.
area fix-mention: repo at the parent of the merge commit; the PR's test files are held back in $RUNNER_TEMP/hidden,
  the fixed sources in $RUNNER_TEMP/fix. control: fix-ci keeps the fix; fix-mention is checked by the workflow.
Result is one commit with no history (the model cannot read the upstream fix). Writes TASK_* to $GITHUB_ENV. No regex."""
import json, os, shutil, subprocess, sys

area, tid = sys.argv[1], sys.argv[2]
control = len(sys.argv) > 3 and sys.argv[3] == "control"
tmp = os.environ["RUNNER_TEMP"]
from taskdb import find  # noqa: E402
t = find(area, tid)


def sh(*a, cwd=None, out=False):
    r = subprocess.run(a, cwd=cwd, check=True, capture_output=out, text=True)
    return r.stdout if out else None


d = os.path.join(tmp, "repo")
up = os.path.join(tmp, "up")
for p in (d, up, os.path.join(tmp, "hidden"), os.path.join(tmp, "fix")):
    shutil.rmtree(p, ignore_errors=True)
sh("git", "clone", "-q", "--filter=blob:none", "https://github.com/" + t["repo"], up)
sha = t["sha"]
if area == "fix-ci":
    sh("git", "checkout", "-q", sha, cwd=up)
    if not control:
        sh("git", "checkout", "-q", sha + "^", "--", *t["src"], cwd=up)
else:
    for kind, names in (("hidden", t["tests"]), ("fix", t["src"])):
        for p in names:
            dst = os.path.join(tmp, kind, p)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "w").write(sh("git", "show", sha + ":" + p, cwd=up, out=True))
    sh("git", "checkout", "-q", sha + "^", cwd=up)
shutil.copytree(up, d)
shutil.rmtree(up)
shutil.rmtree(os.path.join(d, ".git"))
sh("git", "init", "-q", cwd=d)
sh("git", "add", "-A", cwd=d)
sh("git", "-c", "user.name=lab", "-c", "user.email=lab@example.com", "commit", "-q", "-m", "snapshot", cwd=d)
snap = sh("git", "rev-parse", "HEAD", cwd=d, out=True).strip()
with open(os.environ["GITHUB_ENV"], "a") as f:
    for k, v in (("TASK_LANG", t["lang"]), ("TASK_TEST", t["test"]), ("TASK_INSTALL", t["install"]),
                 ("TASK_TESTFILES", " ".join(t["tests"])), ("TASK_SRC", " ".join(t["src"])), ("SNAP", snap),
                 ("TASK_REPO", t["repo"])):
        f.write(f"{k}={v}\n")
print("task", tid, t["repo"], sha[:8], t["test"])
