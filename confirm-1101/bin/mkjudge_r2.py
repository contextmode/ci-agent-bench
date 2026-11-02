#!/usr/bin/env python3
"""Blind judge files for release and review pairs (PLAN-r2.md section 5). No regex. Never reads a key.

Usage (repo root): python3 confirm-1101/bin/mkjudge_r2.py ROUND ART_DIR RUNS_JSON KEY_OUT
  ROUND: r1 or r2 (prefix of the judge ids, so both rounds live side by side).
  Writes lab/release/judge/<ROUND>-<task>.md and lab/review-action/judge/<ROUND>-<task>.md.
  The A/B order key goes to KEY_OUT (keep it outside the repo until the verdicts are in).
A/B order per pair: random.Random("confirm-1101-r2-judge|ROUND|area|task").random() < 0.5 -> gateway is A.
Release file: the maintainers' published notes, the commit subjects prev..tag, CANDIDATE A, CANDIDATE B.
Review file: the real PR diff, REVIEW A, REVIEW B. No tool or arm names in any file."""
import glob, json, os, random, subprocess, sys

ROUND, ART, RUNS, KEY = sys.argv[1:5]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from taskdb import find  # noqa: E402


def gh(args):
    for _ in range(4):
        r = subprocess.run(["gh"] + args, capture_output=True, text=True)
        if r.returncode == 0: return r.stdout
    raise SystemExit("gh failed: " + " ".join(args[:3]))


def out_of(rid):
    d = glob.glob(os.path.join(ART, str(rid), "*"))
    if not d: return None
    d = d[0]
    if os.path.exists(os.path.join(d, "release-notes.md")): return open(os.path.join(d, "release-notes.md"), errors="replace").read()
    if os.path.exists(os.path.join(d, "lab-metrics.json")): return json.load(open(os.path.join(d, "lab-metrics.json"))).get("review") or None
    return None


pairs = {}
for x in json.load(open(RUNS)):
    if x.get("conclusion") != "success": continue
    t = x["displayTitle"].split()
    if t[0] == "cc" and t[1] == "release":
        area, task, arm = "release", t[2], t[3]
    elif t[0] == "review":
        repo, pr = t[2].split("#"); area, task, arm = "review", repo.split("/")[1] + "-" + pr, t[1]
    else:
        continue
    pairs.setdefault((area, task), {})[arm] = x["databaseId"]

key = {}
for (area, task), arms in sorted(pairs.items()):
    if "gateway" not in arms or "direct-ts" not in arms: continue
    g, d = out_of(arms["gateway"]), out_of(arms["direct-ts"])
    if not g or not d:
        key[f"{ROUND}-{task}"] = dict(area=area, task=task, skipped="empty output", runs=arms); continue
    flip = random.Random(f"confirm-1101-r2-judge|{ROUND}|{area}|{task}").random() < 0.5
    a, b = (g, d) if flip else (d, g)
    t = find(area, task); jid = f"{ROUND}-{task}"
    if area == "release":
        notes = json.loads(gh(["api", f"repos/{t['repo']}/releases/tags/{t['tag']}"])).get("body") or ""
        cmp = json.loads(gh(["api", f"repos/{t['repo']}/compare/{t['prev']}...{t['tag']}?per_page=250"]))
        subj = "\n".join((c["commit"]["message"] or "").split("\n")[0] for c in cmp.get("commits") or [])
        body = (f"# Judge file {jid}\n\n## PUBLISHED RELEASE NOTES (written by the maintainers)\n\n{notes}\n\n"
                f"## COMMIT SUBJECTS between the previous tag and the release\n\n{subj}\n\n# CANDIDATE A\n\n{a}\n\n# CANDIDATE B\n\n{b}\n")
        path = f"lab/release/judge/{jid}.md"
    else:
        diff = gh(["api", f"repos/{t['repo']}/pulls/{t['pr']}", "-H", "Accept: application/vnd.github.diff"])
        body = f"# PR diff (the real change)\n\n```diff\n{diff}\n```\n\n# REVIEW A\n\n{a}\n\n# REVIEW B\n\n{b}\n"
        path = f"lab/review-action/judge/{jid}.md"
    open(path, "w").write(body)
    key[jid] = dict(area=area, task=task, A="gateway" if flip else "direct-ts", B="direct-ts" if flip else "gateway",
                    gateway_run=arms["gateway"], direct_run=arms["direct-ts"], file=path)
json.dump(key, open(KEY, "w"), indent=1)
print(len([k for k in key.values() if "file" in k]), "judge files;", sum(1 for k in key.values() if "skipped" in k), "skipped")
