"""Build pools/fix-ci.json and pools/fix-mention.json (pre-registered; no model is called; no regex).

Run: python3 build_fix.py            (re-run reads pools/cache/, same output)
Source: GitHub API through `gh` only (GraphQL search). Rules, fixed before any PR was read:
  F1  Repos: the REPOS table below. A repo is used only if it has >= 20000 stars and is not archived.
  F2  Merged PRs, merged 2026-01-01..2026-10-31, title contains "fix" (search `fix in:title`), author is human
      (common.is_human), merge commit exists and has exactly 1 parent (squash or rebase merge, so merge^ is the base).
  F3  Files: at most 12 changed files; every file is a code file of the repo language, a test file, or a docs file
      (.md .rst .txt). At least 1 test file and 1-3 source code files. Source change (additions+deletions) is 3 to 150 lines.
  F4  Exclusions: the merge commit (full or first 8 chars) or `owner/repo#N` or `/pull/N` of the repo appears in any text
      file under lab/, reproduce/, docs/ or confirm-1101/ (except this pools folder's output) = used before.
  F5  Pool "mention": the PR closes at least one issue (closingIssuesReferences) whose body is not empty. Pool "ci": all other
      PRs that pass F2-F4. (The two pools never share a PR.)
  F6  Order: per repo, draw order sha256("confirm-1101|<repo>|<number>") lowest first, at most 4 kept per repo;
      common.round_robin-style interleave over repos in draw order of the repo name.
Test command per task = the repo's template with the changed test files (or their Go package dirs).
Whether a task is valid (baseline fails, control passes) is decided later by the free validation runs, not here.
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (LAB, POOLS, draw_key, graphql, is_human, repo_meta, search_all, short_repo,
                    write_pool, MIN_STARS)
from datetime import datetime, timezone

START = datetime(2026, 1, 1, tzinfo=timezone.utc)
END = datetime(2026, 10, 31, 23, 59, 59, tzinfo=timezone.utc)
PER_REPO = 4
NODE_INSTALL = "npm install --no-audit --no-fund --loglevel=error"
REPOS = {
    "labstack/echo":      dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "gofiber/fiber":      dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "spf13/viper":        dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "urfave/cli":         dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "uber-go/zap":        dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "sirupsen/logrus":    dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "samber/lo":          dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "gorilla/websocket":  dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "tj/commander.js":    dict(lang="node", install=NODE_INSTALL, test="npx jest {files}"),
    "immerjs/immer":      dict(lang="node", install=NODE_INSTALL, test="npx jest {files}"),
    "mochajs/mocha":      dict(lang="node", install=NODE_INSTALL, test="npx mocha {files}"),
    "scrapy/scrapy":      dict(lang="python", install="pip install -q -e . pytest testfixtures pexpect sybil",
                               test="python -m pytest {files} -p no:cacheprovider -q"),
    "httpie/cli":         dict(lang="python", install="pip install -q -e '.[test]' pytest",
                               test="python -m pytest {files} -p no:cacheprovider -q"),
    "python-poetry/poetry": dict(lang="python", install="pip install -q -e . pytest pytest-mock httpretty deepdiff pytest-xdist",
                               test="python -m pytest {files} -p no:cacheprovider -q -n 0"),
    "pydantic/pydantic":  dict(lang="python", install="pip install -q -e . pytest pytest-mock dirty-equals pytest-benchmark pytest-examples faker",
                               test="python -m pytest {files} -p no:cacheprovider -q"),
}
EXT = {"go": (".go",), "python": (".py",), "node": (".js", ".ts", ".mjs", ".cjs", ".tsx", ".jsx")}
DOC_EXT = (".md", ".rst", ".txt")
TEST_SEGS = ("test", "tests", "__tests__", "testdata", "spec", "fixtures", "testing")
TEST_SUFFIX = ("_test.go", "_test.py", ".test.js", ".test.ts", ".spec.js", ".spec.ts", ".test.mjs", ".test.tsx")
FRAG = ("... on PullRequest{number title mergedAt url author{__typename login} "
        "mergeCommit{oid parents(first:3){totalCount}} "
        "closingIssuesReferences(first:3){nodes{number title body createdAt state author{login}}} "
        "files(first:30){totalCount nodes{path additions deletions}}}")


def is_test(path):
    segs = path.lower().split("/")
    name = segs[-1]
    return (any(s in TEST_SEGS for s in segs[:-1]) or name.startswith("test_") or name.endswith(TEST_SUFFIX)
            or name in ("conftest.py",) or name.startswith("test."))


def used_text():
    """Lower-case text of every file under lab/, reproduce/, docs/ and confirm-1101/ (not the pool outputs)."""
    parts = []
    for top in ("lab", "reproduce", "docs", "confirm-1101"):
        for root, _d, files in os.walk(os.path.join(LAB, top)):
            if "/cache" in root or "/.git" in root:
                continue
            for f in files:
                p = os.path.join(root, f)
                if p.startswith(POOLS) and f.startswith("fix-"):
                    continue
                try:
                    parts.append(open(p, encoding="utf-8", errors="ignore").read().lower())
                except OSError:
                    pass
    return "\n".join(parts)


def used(text, repo, number, sha):
    r = repo.lower()
    return (sha in text or sha[:8] in text or (r + "#" + str(number)) in text
            or (r + "/pull/" + str(number)) in text or (r + "/issues/" + str(number)) in text)


def build_repo(repo, text):
    cfg = REPOS[repo]
    meta = repo_meta(repo)
    info = {"repo": repo, "language": cfg["lang"], "stars": meta["stars"], "stars_fetched_at": meta["stars_fetched_at"]}
    if meta["stars"] < MIN_STARS or meta["archived"]:
        info["skipped"] = "stars < 20000 or archived"
        return info, []
    nodes, fetched = search_all(f"repo:{repo} is:pr is:merged fix in:title", "merged", START, END, FRAG, per_page=20)
    cnt = {"found": len(nodes), "human_1parent": 0, "files_ok": 0, "unused": 0}
    out = []
    for pr in nodes:
        mc = pr.get("mergeCommit") or {}
        if not mc.get("oid") or (mc.get("parents") or {}).get("totalCount") != 1:
            continue
        if not is_human(pr.get("author")) or "fix" not in pr["title"].lower():
            continue
        cnt["human_1parent"] += 1
        f = pr["files"]
        if f["totalCount"] > 12 or f["totalCount"] > len(f["nodes"]):
            continue
        tests, srcs, other, changed = [], [], [], 0
        for x in f["nodes"]:
            p = x["path"]
            if p.lower().endswith(DOC_EXT):
                continue
            if is_test(p):
                tests.append(p)
            elif p.lower().endswith(EXT[cfg["lang"]]):
                srcs.append(p)
                changed += x["additions"] + x["deletions"]
            else:
                other.append(p)
        if other or not tests or not 1 <= len(srcs) <= 3 or not 3 <= changed <= 150:
            continue
        cnt["files_ok"] += 1
        if used(text, repo, pr["number"], mc["oid"]):
            continue
        cnt["unused"] += 1
        tf = [t for t in tests if t.lower().endswith(EXT[cfg["lang"]])] or tests
        dirs = sorted({("./" + os.path.dirname(t)) if os.path.dirname(t) else "." for t in tf})
        issues = [i for i in (pr["closingIssuesReferences"]["nodes"] or []) if i and (i.get("body") or "").strip()]
        cand = {"id": f"{short_repo(repo)}-{pr['number']}", "repo": repo, "stars": meta["stars"], "pr": pr["number"],
                "title": pr["title"], "merged_at": pr["mergedAt"], "url": pr["url"], "sha": mc["oid"],
                "lang": cfg["lang"], "src": srcs, "tests": tests, "src_lines": changed,
                "install": cfg["install"], "test": cfg["test"].replace("{files}", " ".join(tf)).replace("{dirs}", " ".join(dirs))}
        if issues:
            i = issues[0]
            cand["issue"] = {"number": i["number"], "title": i["title"], "body": i["body"], "author": (i.get("author") or {}).get("login") or "ghost",
                             "created": i["createdAt"], "state": "OPEN"}
        out.append(cand)
    out.sort(key=lambda c: draw_key(repo, c["pr"]))
    info["data_fetched_at"] = fetched
    info["counts"] = cnt
    return info, out


def interleave(per_repo):
    order = sorted(per_repo, key=lambda r: draw_key(r, "repo"))
    res = []
    for rnd in range(PER_REPO):
        for r in order:
            if len(per_repo[r]) > rnd:
                res.append(per_repo[r][rnd])
    return res


def main():
    text = used_text()
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(lambda r: build_repo(r, text), sorted(REPOS)))
    pools = {"ci": {}, "mention": {}}
    for info, cands in results:
        for c in cands:
            kind = "mention" if "issue" in c else "ci"
            pools[kind].setdefault(info["repo"], [])
            if len(pools[kind][info["repo"]]) < PER_REPO:
                pools[kind][info["repo"]].append(c)
    repos = sorted((i for i, _ in results), key=lambda r: r["repo"].lower())
    for kind in pools:
        cands = interleave(pools[kind])
        write_pool(os.path.join(POOLS, f"fix-{kind}.json"), f"fix-{kind}", __doc__, repos, cands)
        print(kind, len(cands), "candidates;", {r: len(v) for r, v in pools[kind].items()})
    for i in repos:
        print(i["repo"], i["stars"], i.get("counts"), i.get("skipped", ""))


if __name__ == "__main__":
    main()
