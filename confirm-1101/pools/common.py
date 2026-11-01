"""Shared helpers for the confirm-1101 candidate pools.

Rules that hold for every pool:
  * Data comes only from the GitHub API through the `gh` CLI. No LLM is called.
  * Every API response is saved under pools/cache/ the first time it is fetched,
    with its fetch time (UTC). A re-run reads the cache, so it gives the same
    output byte for byte. Pass --refresh to fetch everything again.
  * A repo is eligible only if it has >= 20000 stars (GraphQL stargazerCount).
    Stars and the UTC fetch time are recorded per repo in each pool file.
  * Candidates are drawn in a fixed pseudo-random order:
        sha256("confirm-1101|<repo>|<number or tag>")
    lowest hash first. This draw does not look at content, so no candidate is
    picked or dropped by a guess about how hard it is.
  * At most 3 candidates per repo. The output is sorted by (repo, number/tag).
  * Exclusions: every issue, PR or tag that an earlier task used. See
    load_exclusions() for the exact sources.
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

POOLS = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(POOLS, "..", ".."))  # /private/tmp/confirm1101/lab
CACHE = os.path.join(POOLS, "cache")
SEED = "confirm-1101"
MIN_STARS = 20000
PER_REPO = 3
REFRESH = "--refresh" in sys.argv


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def draw_key(repo, item):
    """Pre-registered random order: lowest sha256 first."""
    return hashlib.sha256(f"{SEED}|{repo.lower()}|{item}".encode()).hexdigest()


TRANSIENT = ("couldn't respond", "timeout", "timed out", "502", "503", "504", "secondary rate",
             "rate limit", "something went wrong", "eof", "connection reset", "tls handshake")


def gh(args, body=None, tries=6):
    """Run `gh api <args>` (body = JSON sent on stdin). Returns (data, fetched_at).

    Responses are cached on disk. Permanent errors (404, 422, ...) are cached as
    {"__error__": "..."} so a re-run sees the same answer."""
    key = hashlib.sha1(json.dumps([args, body], sort_keys=True).encode()).hexdigest()
    path = os.path.join(CACHE, key[:2], key + ".json")
    if not REFRESH and os.path.exists(path):
        c = json.load(open(path))
        return c["data"], c["fetched_at"]
    cmd = ["gh", "api"] + list(args) + (["--input", "-"] if body is not None else [])
    last = ""
    for attempt in range(tries):
        fetched_at = utcnow()
        p = subprocess.run(cmd, input=json.dumps(body) if body is not None else None,
                           capture_output=True, text=True)
        out = p.stdout.strip()
        data = None
        try:
            data = json.loads(out) if out else None
        except Exception:
            data = None
        errs = ""
        if isinstance(data, dict) and data.get("errors"):
            errs = json.dumps(data["errors"])[:400]
        if p.returncode == 0 and data is not None and not errs:
            break
        last = (p.stderr + " " + errs + " " + (out[:300] if data is None else "")).strip()
        if any(t in last.lower() for t in TRANSIENT) and attempt < tries - 1:
            time.sleep(min(60, 4 * 2 ** attempt))
            continue
        if isinstance(data, dict) and data.get("data") and errs:
            # GraphQL partial data with a permanent error: keep data, note the error.
            data["__error__"] = errs
            break
        data = {"__error__": last[:600]}
        break
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({"args": args, "body": body, "fetched_at": fetched_at, "data": data},
              open(path, "w"))
    return data, fetched_at


def graphql(query, **variables):
    data, at = gh(["graphql"], {"query": query, "variables": variables})
    if not isinstance(data, dict) or "data" not in data or data["data"] is None:
        raise RuntimeError(f"graphql failed: {str(data)[:400]}")
    return data["data"], at


def repo_meta(repo):
    """Stars and fetch time for one repo."""
    owner, name = repo.split("/")
    d, at = graphql("query($o:String!,$n:String!){repository(owner:$o,name:$n)"
                    "{nameWithOwner stargazerCount isArchived}}", o=owner, n=name)
    r = d["repository"]
    return {"stars": r["stargazerCount"], "stars_fetched_at": at, "archived": r["isArchived"]}


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def search_all(base_query, qualifier, start, end, fragment, per_page=50):
    """All search hits for `base_query <qualifier>:<start>..<end>`.

    GitHub search returns at most 1000 hits, so a range with more than 1000 hits
    is split in two halves (by day) until each part is below the cap."""
    count_q = "query($q:String!){search(query:$q,type:ISSUE,first:1){issueCount}}"
    page_q = ("query($q:String!,$after:String){rateLimit{remaining}"
              f"search(query:$q,type:ISSUE,first:{per_page},after:$after)"
              "{issueCount pageInfo{hasNextPage endCursor} nodes{" + fragment + "}}}")
    out, ranges, times = [], [(start, end)], []
    while ranges:
        a, b = ranges.pop(0)
        q = f"{base_query} {qualifier}:{iso(a)}..{iso(b)}"
        d, at = graphql(count_q, q=q)
        times.append(at)
        n = d["search"]["issueCount"]
        days = (b - a).days
        if n > 1000 and days >= 1:
            mid = a + timedelta(days=(days + 1) // 2)
            ranges[:0] = [(a, mid - timedelta(seconds=1)), (mid, b)]
            continue
        after = None
        while True:
            d, at = graphql(page_q, q=q, after=after)
            times.append(at)
            s = d["search"]
            out.extend(x for x in s["nodes"] if x)
            if not s["pageInfo"]["hasNextPage"]:
                break
            after = s["pageInfo"]["endCursor"]
    seen, uniq = set(), []
    for x in out:
        if x.get("number") is not None and x["number"] not in seen:
            seen.add(x["number"])
            uniq.append(x)
    # Second value: UTC time of the last fetch for this repo's search.
    return uniq, max(times)


# Accounts that are bots but have the GitHub type "User", so __typename alone misses them.
BOT_LOGINS = {
    "github-actions", "dependabot", "renovate", "copilot", "vs-code-engineering", "vscodenpa",
    "vscode-triage-bot", "rust-highfive", "rustbot", "rust-timer", "bors", "gopherbot",
    "facebook-github-bot", "pytorchmergebot", "pytorchbot", "pytorch-bot", "flutter-dashboard",
    "fluttergithubbot", "auto-submit", "home-assistant", "denobot", "k8s-ci-robot",
    "k8s-triage-robot", "electron-bot", "electron-roller", "nodejs-github-bot", "msftbot",
    "microsoft-github-policy-service", "copybara-service", "google-cla", "ghost",
    # Added after the first labels run: oven-sh's bot ("robobun", type User) labeled 3 bun issues.
    "robobun",
}


def is_human(actor):
    """A human = GitHub type "User", login not in BOT_LOGINS, login does not end in
    "bot", "[bot]" or "robot". A deleted account (null actor) does not count."""
    if not actor or actor.get("__typename") != "User":
        return False
    login = (actor.get("login") or "").lower()
    if login in BOT_LOGINS or login.endswith("bot") or login.endswith("[bot]") or login.endswith("robot"):
        return False
    return True


# ---------------------------------------------------------------- exclusions
REPO_NUM = re.compile(r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#(\d+)")
URL_NUM = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/(?:issues|pull)/(\d+)")
URL_TAG = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/releases/tag/([^\s)\"'`>\]<,]+)")
URL_CMP = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/compare/([^\s)\"'`>\]<,]+)")
SHORT_ID = re.compile(r"\b([a-z0-9_.]+)-(\d{2,})\b")
REL_SH = re.compile(r"REL_REPO=(\S+?);\s*REL_TAG=(\S+?);\s*REL_PREV=(\S+?);")
NUM_KEYS = ("number", "pr", "issue", "original", "run_pr")
TAG_KEYS = ("tag", "previous_tag", "prev")
REPO_KEYS = ("repo", "upstream", "REL_REPO")


def _lab_files():
    """Every file in lab/, reproduce/ and docs/ (this pools folder is not read)."""
    files = []
    for top in ("lab", "reproduce", "docs"):
        for p in glob.glob(os.path.join(LAB, top, "**", "*"), recursive=True):
            if os.path.isfile(p) and "/.git/" not in p and not p.startswith(POOLS):
                files.append(p)
    return sorted(files)


class Exclusions:
    """Exclusion sources (read in full, not sampled):
      1. lab/labels/tasks.json, lab/dedupe/tasks.json, reproduce/tasks/*.json,
         lab/review-action/results/runs.json, lab/pr-review*/** (every JSON file):
         any object with a repo key (repo/upstream) gives (repo, number) for the
         keys number/pr/issue/original/run_pr and (repo, tag) for tag/previous_tag/prev.
      2. lab/release/tasks.sh: REL_REPO / REL_TAG / REL_PREV triples.
      3. Text of every file in lab/, reproduce/, docs/: "owner/repo#N",
         github.com/owner/repo/(issues|pull)/N, .../releases/tag/T, .../compare/A...B,
         and task ids "<repo-name>-<N>" (for example "godot-124950").
      4. Release tags only: a tag is also excluded when it appears as a whole word
         in a file under docs/, lab/release/ or reproduce/tasks/release.json that
         also names the repo."""

    def __init__(self):
        self.items, self.tags, self.short = set(), set(), set()
        self.release_texts = []
        for p in _lab_files():
            try:
                text = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            if p.endswith(".json"):
                try:
                    self._walk(json.loads(text))
                except Exception:
                    pass
            for r, n in REPO_NUM.findall(text) + URL_NUM.findall(text):
                self.items.add((r.lower(), int(n)))
            for r, t in URL_TAG.findall(text):
                self.tags.add((r.lower(), t))
            for r, rng in URL_CMP.findall(text):
                for t in rng.split("..."):
                    if t:
                        self.tags.add((r.lower(), t))
            for r, t, pv in REL_SH.findall(text):
                self.tags.add((r.lower(), t))
                self.tags.add((r.lower(), pv))
            for name, n in SHORT_ID.findall(text.lower()):
                self.short.add((name, int(n)))
            rel = os.path.relpath(p, LAB)
            if rel.startswith("docs/") or rel.startswith("lab/release/") or rel == "reproduce/tasks/release.json":
                self.release_texts.append(text)

    def _walk(self, o):
        if isinstance(o, dict):
            repo = next((o[k] for k in REPO_KEYS if isinstance(o.get(k), str) and "/" in o[k]), None)
            if repo:
                for k in NUM_KEYS:
                    v = o.get(k)
                    if isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
                        self.items.add((repo.lower(), int(v)))
                for k in TAG_KEYS:
                    v = o.get(k)
                    if isinstance(v, str) and v:
                        self.tags.add((repo.lower(), v))
            for v in o.values():
                self._walk(v)
        elif isinstance(o, list):
            for v in o:
                self._walk(v)

    def item(self, repo, n):
        name = repo.split("/")[1].lower()
        return (repo.lower(), int(n)) in self.items or (name, int(n)) in self.short

    def tag(self, repo, tag):
        if (repo.lower(), tag) in self.tags:
            return True
        word = re.compile(r"(?<![\w.])" + re.escape(tag) + r"(?![\w.])")
        for t in self.release_texts:
            if repo.lower() in t.lower() and word.search(t):
                return True
        return False


SHORT = {"home-assistant/core": "home-assistant"}


def short_repo(repo):
    """Short name for ids: the repo name, except a generic name gets the owner."""
    return SHORT.get(repo, repo.split("/")[1]).lower()


def round_robin(per_repo, n):
    """Pick n candidates from per_repo = {repo: [up to 3 eligible, in draw order]}.

    Round 1 takes the first candidate of every repo, round 2 the second, round 3
    the third. Inside a round, repos go in the order of draw_key(repo, "repo").
    Stop at n. This spreads the pool over as many repos as possible and looks at
    nothing but the pre-registered draw."""
    order = sorted(per_repo, key=lambda r: draw_key(r, "repo"))
    picked = []
    for rnd in range(PER_REPO):
        for r in order:
            if len(picked) == n:
                return picked
            if len(per_repo[r]) > rnd:
                picked.append(per_repo[r][rnd])
    return picked


def write_pool(path, pool, rules, repos, candidates, extra=None):
    # No build time stamp: a re-run from the cache gives the same bytes.
    # Each repo carries the UTC time its data was fetched.
    out = {"pool": pool, "seed": SEED, "rules": rules.strip(),
           "repos": repos, "count": len(candidates), "candidates": candidates}
    if extra:
        out.update(extra)
    with open(path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
