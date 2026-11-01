"""Build pools/labels.json: 36 candidate issues for the labels benchmark.

Run: python3 build_labels.py            (re-run reads pools/cache/, same output)
     python3 build_labels.py --refresh  (fetch everything again from GitHub)

Rules (pre-registered; nothing else is used to pick or drop a candidate):
  R1  Repos: the REPOS list below, fixed before any issue was read. A repo is
      used only if it has >= 20000 stars and is not archived.
  R2  Closed issues, not PRs: search "repo:R is:issue is:closed
      created:2026-10-01T00:00:00Z..2026-10-31T23:59:59Z closed:<=2026-10-31T23:59:59Z"
      and the same dates are checked again on each issue.
  R3  Body length (Python len of the body text) is 200 to 6000 characters.
  R4  The issue author is a human (common.is_human). This is the same filter as
      the earlier labels bench ("issue author is a user").
  R5  Truth labels = the labels on the issue now, minus every label that
      matches the DROP list of lab/labels/extract.py (copied exactly below).
  R6  At least 1 truth label, and at least one truth label was added by a
      timeline "labeled" event whose actor is a human (common.is_human) and is
      not the issue author. "labeler" = the actor of the earliest such event.
      (common.BOT_LOGINS got "robobun" after the first run, before the pool was
      used: it is oven-sh's bot with GitHub type "User".)
  R7  Exclusions: every issue named by an earlier task (common.Exclusions).
  R8  Per repo, eligible issues are put in draw order (common.draw_key on the
      issue number); the first 3 are kept. common.round_robin then takes 36
      over all repos. Output is sorted by (repo, number).
"""
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from common import (Exclusions, POOLS, draw_key, is_human, repo_meta, round_robin,
                    search_all, short_repo, write_pool, MIN_STARS, PER_REPO)

N = 36
START = datetime(2026, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
# R1: the 12 repos named in the task, then 4 more that label issues by hand.
REPOS = [
    "microsoft/vscode", "golang/go", "rust-lang/rust", "godotengine/godot",
    "zed-industries/zed", "tauri-apps/tauri", "oven-sh/bun", "denoland/deno",
    "flutter/flutter", "home-assistant/core", "astral-sh/uv", "pytorch/pytorch",
    "astral-sh/ruff", "neovim/neovim", "microsoft/TypeScript", "electron/electron",
]
# R5: copied exactly from lab/labels/extract.py.
DROP = ("stale", "triage", "needs", "wontfix", "duplicate", "invalid", "autoclose", "bot", "ai-", "status", "waiting", "close", "resolved",
        "fixed", "released", "regression-", "spam", "archived", "verif", "team", "contrib", "priority", "severity", "reach", "relnotes", "milestone")


def keep(l):
    return not any(x in l.lower() for x in DROP)


FRAGMENT = ("... on Issue{number title body createdAt closedAt url author{__typename login} "
            "labels(first:100){nodes{name}} "
            "timelineItems(itemTypes:[LABELED_EVENT],first:100){nodes{... on LabeledEvent"
            "{createdAt actor{__typename login} label{name}}}}}")


def build_repo(repo, ex):
    meta = repo_meta(repo)
    info = {"repo": repo, "stars": meta["stars"], "stars_fetched_at": meta["stars_fetched_at"]}
    if meta["stars"] < MIN_STARS or meta["archived"]:
        info["skipped"] = "stars < 20000 or archived"
        return info, []
    base = f"repo:{repo} is:issue is:closed closed:<={END.strftime('%Y-%m-%dT%H:%M:%SZ')}"
    nodes, fetched = search_all(base, "created", START, END, FRAGMENT)
    info["data_fetched_at"] = fetched
    stats = {"found": len(nodes), "dates": 0, "body": 0, "author": 0, "truth": 0, "human_label": 0, "excluded": 0}
    eligible = []
    for it in nodes:
        s, e = it["createdAt"], it.get("closedAt") or ""
        if not ("2026-10-01T00:00:00Z" <= s <= "2026-10-31T23:59:59Z" and e and e <= "2026-10-31T23:59:59Z"):
            continue
        stats["dates"] += 1
        body = it.get("body") or ""
        if not 200 <= len(body) <= 6000:
            continue
        stats["body"] += 1
        author = it.get("author")
        if not is_human(author):
            continue
        stats["author"] += 1
        truth = sorted({l["name"] for l in it["labels"]["nodes"] if keep(l["name"])})
        if not truth:
            continue
        stats["truth"] += 1
        events = sorted((ev for ev in it["timelineItems"]["nodes"] if ev and ev.get("label")),
                        key=lambda ev: ev["createdAt"])
        labeler = next((ev["actor"]["login"] for ev in events
                        if ev["label"]["name"] in truth and is_human(ev.get("actor"))
                        and ev["actor"]["login"].lower() != author["login"].lower()), None)
        if not labeler:
            continue
        stats["human_label"] += 1
        if ex.item(repo, it["number"]):
            stats["excluded"] += 1
            continue
        eligible.append({"repo": repo, "stars": meta["stars"], "number": it["number"],
                         "created": it["createdAt"], "title": it["title"], "body_len": len(body),
                         "truth": truth, "id": f"{short_repo(repo)}-{it['number']}",
                         "labeler": labeler, "url": it["url"]})
    eligible.sort(key=lambda c: draw_key(repo, c["number"]))
    info["counts"] = stats
    info["eligible"] = len(eligible)
    return info, eligible[:PER_REPO]


def main():
    ex = Exclusions()
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(lambda r: build_repo(r, ex), REPOS))
    per_repo = {info["repo"]: top for info, top in results if top}
    picked = round_robin(per_repo, N)
    picked.sort(key=lambda c: (c["repo"].lower(), c["number"]))
    used = {}
    for c in picked:
        used[c["repo"]] = used.get(c["repo"], 0) + 1
    repos = []
    for info, _ in results:
        info["picked"] = used.get(info["repo"], 0)
        repos.append(info)
    repos.sort(key=lambda r: r["repo"].lower())
    write_pool(os.path.join(POOLS, "labels.json"), "labels", __doc__, repos, picked)
    print(f"labels: {len(picked)} candidates from {len(used)} repos")
    for r in repos:
        print(" ", r["repo"], r["stars"], r.get("counts"), "eligible", r.get("eligible"), "picked", r["picked"])
    if len(picked) < N:
        raise SystemExit(f"only {len(picked)} of {N}")


if __name__ == "__main__":
    main()
