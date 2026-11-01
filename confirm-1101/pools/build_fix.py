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
  F7  Setup revision S1 (2026-11-01, after the first free validation, before any new paid run): round 1 showed setup
      errors, not task faults (poetry: no 'responses'; pydantic: 'thread_unsafe' marker from pytest-run-parallel,
      no pytz/jsonschema; scrapy: no pytest-twisted/pyftpdlib; commander.js and immer: jest is not their runner).
      Only the install and test templates changed. `python3 build_fix.py --retemplate` writes them into the existing
      pools; the candidates and their draw order are not touched (a new search would now exclude every drawn PR by F4,
      because tasks/ names them).
"""
import json
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
PY_TEST = "python -m pytest {files} -p no:cacheprovider -q"
REPOS = {
    "labstack/echo":      dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "gofiber/fiber":      dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "spf13/viper":        dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "urfave/cli":         dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "uber-go/zap":        dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "sirupsen/logrus":    dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "samber/lo":          dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    "gorilla/websocket":  dict(lang="go", install="go mod download", test="go test -count=1 {dirs}"),
    # Setup revision S1 (see F7): each runner below is the repo's own test runner (package.json "test" script).
    "tj/commander.js":    dict(lang="node", install=NODE_INSTALL, test="node --test {files}"),
    "immerjs/immer":      dict(lang="node", install=NODE_INSTALL, test="npx vitest run {files}"),
    "mochajs/mocha":      dict(lang="node", install=NODE_INSTALL, test="npx mocha {files}"),
    # Python test deps = the repo's own test requirements (scrapy tox.ini [test-requirements], poetry
    # [tool.poetry.group.test], pydantic [dependency-groups] dev; pip >= 25.1 reads dependency groups).
    "scrapy/scrapy":      dict(lang="python", install="pip install -q -e . pytest pytest-twisted pytest-xdist pytest-timeout "
                                                     "pytest-rerunfailures testfixtures pexpect sybil pyftpdlib attrs pygments "
                                                     "psutil httpx",
                               test=PY_TEST),
    "httpie/cli":         dict(lang="python", install="pip install -q -e '.[test]' pytest",
                               test=PY_TEST),
    "python-poetry/poetry": dict(lang="python", install="pip install -q -e . pytest pytest-mock pytest-xdist httpretty deepdiff "
                                                       "responses jaraco-classes",
                               test=PY_TEST + " -n 0"),
    "pydantic/pydantic":  dict(lang="python", install="python -m pip install -q -U 'pip>=25.1' && pip install -q -e . --group dev",
                               test=PY_TEST),
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


def commands(repo, tests):
    """Install and test command of one task, from the repo template and the PR's changed test files."""
    cfg = REPOS[repo]
    tf = [t for t in tests if t.lower().endswith(EXT[cfg["lang"]])] or tests
    dirs = sorted({("./" + os.path.dirname(t)) if os.path.dirname(t) else "." for t in tf})
    return {"install": cfg["install"], "test": cfg["test"].replace("{files}", " ".join(tf)).replace("{dirs}", " ".join(dirs))}


def retemplate():
    """F7: write the current install/test templates into the existing pools. Candidates and order are unchanged."""
    for kind in ("ci", "mention"):
        path = os.path.join(POOLS, f"fix-{kind}.json")
        d = json.load(open(path))
        for c in d["candidates"]:
            c.update(commands(c["repo"], c["tests"]))
        d["rules"] = __doc__.strip()
        d["setup_revision"] = "S1"
        with open(path, "w") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(path, len(d["candidates"]), "candidates retemplated")


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
        issues = [i for i in (pr["closingIssuesReferences"]["nodes"] or []) if i and (i.get("body") or "").strip()]
        cand = {"id": f"{short_repo(repo)}-{pr['number']}", "repo": repo, "stars": meta["stars"], "pr": pr["number"],
                "title": pr["title"], "merged_at": pr["mergedAt"], "url": pr["url"], "sha": mc["oid"],
                "lang": cfg["lang"], "src": srcs, "tests": tests, "src_lines": changed,
                **commands(repo, tests)}
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
    if sys.argv[1:] == ["--retemplate"]:
        retemplate()
    else:
        main()
