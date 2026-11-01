"""Build pools/review.json: 36 candidate merged PRs for the review benchmark.

Run: python3 build_review.py            (re-run reads pools/cache/, same output)
     python3 build_review.py --refresh  (fetch everything again from GitHub)

Rules (pre-registered; nothing else is used to pick or drop a candidate):
  R1  Repos: the REPOS list below (18 repos, 9 main languages), fixed before any
      PR was read. A repo is used only if it has >= 20000 stars and is not
      archived.
  R2  Merged PRs: search "repo:R is:pr is:merged merged:2026-10-01T00:00:00Z..
      2026-10-31T23:59:59Z"; mergedAt is checked again on each PR.
  R3  The PR author is a human (common.is_human: GitHub type "User", not a known
      bot login, login does not end in "bot"/"[bot]"/"robot").
  R4  additions + deletions is 60 to 600, and changedFiles is 1 to 30.
  R5  Not a dependency bump by title: the lower-case title does not start with
      "bump ", "chore(deps", "build(deps", "fix(deps", "deps:", "deps(", "[deps]",
      "update dependency", "update dependencies", "update rust crate",
      "update module", and does not contain "dependabot" or "renovate".
      Also a version bump: the title starts with "bump ", "upgrade " or "update "
      and its last word is a version (digits and dots, optional leading "v").
      (Added after the first run, before the pool was used: it let through
      "Upgrade Corepack to 0.34.7".)
  R6  Not docs-only: at least one changed file is not a docs file. A docs file
      has extension .md, .mdx, .rst or .adoc, or has a path segment "docs",
      "doc" or "documentation".
  R7  Not dependency/lockfile-only: at least one changed file is not a
      dependency file. A dependency file is a lockfile or manifest by base name
      (LOCK_NAMES, MANIFEST_NAMES below), or lives under a vendored-code folder
      (a path segment in VENDOR_DIRS).
  R8  Exclusions: every PR named by an earlier task (common.Exclusions).
  R9  Per repo, PRs that pass R2-R5 and R8 are put in draw order (common.draw_key
      on the PR number); R6-R7 (need the file list) are checked in that order and
      the first 3 that pass are kept. common.round_robin then takes 36 over all
      repos. Output is sorted by (repo, pr).
  head_sha = headRefOid of the PR (last commit of the PR branch).
"""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from common import (Exclusions, POOLS, draw_key, graphql, is_human, repo_meta, round_robin,
                    search_all, short_repo, write_pool, MIN_STARS, PER_REPO)

N = 36
START = datetime(2026, 10, 1, 0, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
# R1: repo -> main language (for the report only; not used to pick).
REPOS = {
    "microsoft/vscode": "TypeScript",
    "vercel/next.js": "TypeScript",
    "grafana/grafana": "TypeScript/Go",
    "astral-sh/ruff": "Rust",
    "astral-sh/uv": "Rust",
    "zed-industries/zed": "Rust",
    "django/django": "Python",
    "huggingface/transformers": "Python",
    "pandas-dev/pandas": "Python",
    "kubernetes/kubernetes": "Go",
    "prometheus/prometheus": "Go",
    "godotengine/godot": "C++",
    "ggml-org/llama.cpp": "C++",
    "neovim/neovim": "C/Lua",
    "flutter/flutter": "Dart",
    "elastic/elasticsearch": "Java",
    "apache/kafka": "Java/Scala",
    "spring-projects/spring-boot": "Java",
}
TITLE_PREFIX = ("bump ", "chore(deps", "build(deps", "fix(deps", "deps:", "deps(", "[deps]",
                "update dependency", "update dependencies", "update rust crate", "update module")
TITLE_ANY = ("dependabot", "renovate")
DOC_EXT = (".md", ".mdx", ".rst", ".adoc")
DOC_DIRS = {"docs", "doc", "documentation"}
LOCK_NAMES = {
    "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock",
    "bun.lockb", "cargo.lock", "go.sum", "poetry.lock", "uv.lock", "pipfile.lock",
    "gemfile.lock", "composer.lock", "pubspec.lock", "flake.lock", "gradle.lockfile",
    "package.resolved", "podfile.lock", "mix.lock",
}
MANIFEST_NAMES = {
    "package.json", "cargo.toml", "go.mod", "pyproject.toml", "pipfile", "gemfile",
    "composer.json", "pubspec.yaml", "pom.xml", "build.gradle", "build.gradle.kts",
    "libs.versions.toml", "requirements.txt", "constraints.txt", "deps", ".gitmodules",
}
VENDOR_DIRS = {"thirdparty", "third_party", "vendor", "vendored", "external", "node_modules"}

FRAGMENT = ("... on PullRequest{number title additions deletions changedFiles mergedAt "
            "headRefOid url author{__typename login}}")
FILES_Q = ("query($o:String!,$n:String!,$num:Int!){repository(owner:$o,name:$n)"
           "{pullRequest(number:$num){files(first:100){totalCount nodes{path}}}}}")


def is_version(word):
    w = word[1:] if word.startswith("v") else word
    parts = w.split(".")
    return len(parts) >= 2 and all(p.isdigit() for p in parts)


def dep_title(title):
    t = title.lower().strip()
    if t.startswith(TITLE_PREFIX) or any(x in t for x in TITLE_ANY):
        return True
    words = t.split()
    return t.startswith(("bump ", "upgrade ", "update ")) and bool(words) and is_version(words[-1])


def segments(path):
    return [s.lower() for s in path.split("/")]


def is_doc(path):
    segs = segments(path)
    return segs[-1].endswith(DOC_EXT) or any(s in DOC_DIRS for s in segs[:-1])


def is_dep(path):
    segs = segments(path)
    name = segs[-1]
    return (name in LOCK_NAMES or name in MANIFEST_NAMES
            or (name.startswith("requirements") and name.endswith(".txt"))
            or any(s in VENDOR_DIRS for s in segs[:-1]))


def files_of(repo, number):
    owner, name = repo.split("/")
    d, at = graphql(FILES_Q, o=owner, n=name, num=number)
    f = d["repository"]["pullRequest"]["files"]
    return [x["path"] for x in f["nodes"]], f["totalCount"], at


def build_repo(repo, ex):
    meta = repo_meta(repo)
    info = {"repo": repo, "language": REPOS[repo], "stars": meta["stars"],
            "stars_fetched_at": meta["stars_fetched_at"]}
    if meta["stars"] < MIN_STARS or meta["archived"]:
        info["skipped"] = "stars < 20000 or archived"
        return info, []
    nodes, fetched = search_all(f"repo:{repo} is:pr is:merged", "merged", START, END,
                                FRAGMENT, per_page=100)
    stats = {"found": len(nodes), "dates": 0, "author": 0, "size": 0, "title": 0,
             "excluded": 0, "checked": 0, "docs_only": 0, "deps_only": 0}
    pending = []
    for pr in nodes:
        m = pr.get("mergedAt") or ""
        if not "2026-10-01T00:00:00Z" <= m <= "2026-10-31T23:59:59Z":
            continue
        stats["dates"] += 1
        if not is_human(pr.get("author")):
            continue
        stats["author"] += 1
        if not (60 <= pr["additions"] + pr["deletions"] <= 600 and 1 <= pr["changedFiles"] <= 30):
            continue
        stats["size"] += 1
        if dep_title(pr["title"]):
            continue
        stats["title"] += 1
        if ex.item(repo, pr["number"]):
            stats["excluded"] += 1
            continue
        pending.append(pr)
    pending.sort(key=lambda pr: draw_key(repo, pr["number"]))
    kept = []
    for pr in pending:
        if len(kept) == PER_REPO:
            break
        stats["checked"] += 1
        paths, total, at = files_of(repo, pr["number"])
        fetched = max(fetched, at)
        if total > len(paths):
            raise RuntimeError(f"{repo}#{pr['number']}: file list cut at {len(paths)} of {total}")
        if all(is_doc(p) for p in paths):
            stats["docs_only"] += 1
            continue
        if all(is_dep(p) for p in paths):
            stats["deps_only"] += 1
            continue
        kept.append({
            "id": f"{short_repo(repo)}-{pr['number']}", "repo": repo, "stars": meta["stars"],
            "pr": pr["number"], "title": pr["title"], "additions": pr["additions"],
            "deletions": pr["deletions"], "changed_files": pr["changedFiles"],
            "merged_at": pr["mergedAt"], "head_sha": pr["headRefOid"], "url": pr["url"],
        })
    info["data_fetched_at"] = fetched
    info["counts"] = stats
    info["kept"] = len(kept)
    return info, kept


def main():
    ex = Exclusions()
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(lambda r: build_repo(r, ex), sorted(REPOS)))
    per_repo = {info["repo"]: kept for info, kept in results if kept}
    picked = round_robin(per_repo, N)
    picked.sort(key=lambda c: (c["repo"].lower(), c["pr"]))
    assert len({c["id"] for c in picked}) == len(picked)
    used = {}
    for c in picked:
        used[c["repo"]] = used.get(c["repo"], 0) + 1
    repos = []
    for info, _ in results:
        info["picked"] = used.get(info["repo"], 0)
        repos.append(info)
    repos.sort(key=lambda r: r["repo"].lower())
    write_pool(os.path.join(POOLS, "review.json"), "review", __doc__, repos, picked)
    print(f"review: {len(picked)} candidates from {len(used)} repos")
    for r in repos:
        print(" ", r["repo"], r["language"], r["stars"], r.get("counts"), "kept", r.get("kept"),
              "picked", r["picked"])
    if len(picked) < N:
        raise SystemExit(f"only {len(picked)} of {N}")


if __name__ == "__main__":
    main()
