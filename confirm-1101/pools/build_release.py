"""Build pools/release.json (30 candidates) and pools/release-notes/<id>.md.

Run: python3 build_release.py            (re-run reads pools/cache/, same output)
     python3 build_release.py --refresh  (fetch everything again from GitHub)

Rules (pre-registered; nothing else is used to pick or drop a candidate):
  R1  Repos: the REPOS table below, fixed before any release note was read. Each
      repo has one product, one tag prefix and one tag suffix (a monorepo gives
      only its main product line). A repo is used only if it has >= 20000 stars
      and is not archived.
  R2  Tag shape: tag = prefix + version + suffix, version = 2 or more dot-separated
      integers (no "-rc", "-pre" and so on). Other tags are ignored.
  R3  The new release is published (not draft, not prerelease) with published_at
      in 2026-08-01T00:00:00Z .. 2026-10-31T23:59:59Z.
  R4  Notes written for users: body length >= 400 characters, and the body with
      every line that contains "Full Changelog" removed is still >= 400
      characters (so a body that is only the auto "Full Changelog" link fails).
      notes_len = len(body).
  R5  Release line = (prefix, suffix, major version). prev = among the stable
      published releases in the same line with a lower version and published
      before the new one, the one with the HIGHEST version. On a single branch
      this is the release published right before it. With parallel patch lines
      (e.g. PowerShell 7.5.x and 7.6.x, redis 8.8.x and 8.10.x) it picks the
      previous patch of the same minor line (7.6.9 -> 7.6.8), not a backport to
      an older minor that happened to be published in between.
      (Changed before the pool was used: the first draft took the one published
      last, and gave cross-branch pairs such as v7.6.9 -> v7.5.13.)
  R6  REST compare prev...tag: status must be "ahead" (prev is an ancestor of
      tag), and commits = ahead_by must be 5 to 200.
  R7  Exclusions: every release tag named by an earlier task (common.Exclusions).
  R8  Per repo, releases that pass R2-R4 and R7 are put in draw order
      (common.draw_key on the tag); R5-R6 are checked in that order and the
      first 3 that pass are kept. common.round_robin then takes 30 over all
      repos. Output is sorted by (repo, tag).
  R9  pools/release-notes/<id>.md holds the published body, byte for byte as the
      API returns it. id = "<short-repo>-<version><suffix>".
"""
import json
import os
from urllib.parse import quote

from common import (Exclusions, POOLS, draw_key, gh, repo_meta, round_robin, short_repo,
                    write_pool, MIN_STARS, PER_REPO)

N = 30
START, END = "2026-08-01T00:00:00Z", "2026-10-31T23:59:59Z"
OLDEST_PAGE = "2025-08-01T00:00:00Z"  # stop paging once a page reaches back this far
MAX_PAGES = 20
# repo: (product name, tag prefix, tag suffix)
REPOS = {
    "astral-sh/uv": ("uv", "", ""),
    "astral-sh/ruff": ("Ruff", "", ""),
    "denoland/deno": ("Deno", "v", ""),
    "oven-sh/bun": ("Bun", "bun-v", ""),
    "tauri-apps/tauri": ("Tauri", "tauri-v", ""),
    "zed-industries/zed": ("Zed", "v", ""),
    "rust-lang/rust": ("Rust", "", ""),
    "nodejs/node": ("Node.js", "v", ""),
    "electron/electron": ("Electron", "v", ""),
    "neovim/neovim": ("Neovim", "v", ""),
    "vercel/next.js": ("Next.js", "v", ""),
    "eslint/eslint": ("ESLint", "v", ""),
    "biomejs/biome": ("Biome", "@biomejs/biome@", ""),
    "pnpm/pnpm": ("pnpm", "v", ""),
    "junegunn/fzf": ("fzf", "v", ""),
    "ollama/ollama": ("Ollama", "v", ""),
    "cli/cli": ("GitHub CLI", "v", ""),
    "hashicorp/terraform": ("Terraform", "v", ""),
    "traefik/traefik": ("Traefik", "v", ""),
    "caddyserver/caddy": ("Caddy", "v", ""),
    "gohugoio/hugo": ("Hugo", "v", ""),
    "nushell/nushell": ("Nushell", "", ""),
    "prometheus/prometheus": ("Prometheus", "v", ""),
    "immich-app/immich": ("Immich", "v", ""),
    "jdx/mise": ("mise", "v", ""),
    "pydantic/pydantic": ("Pydantic", "v", ""),
    "fastapi/fastapi": ("FastAPI", "", ""),
    "withastro/astro": ("Astro", "astro@", ""),
    "google-gemini/gemini-cli": ("Gemini CLI", "v", ""),
    "PowerShell/PowerShell": ("PowerShell", "v", ""),
    "docker/compose": ("Docker Compose", "v", ""),
    "jesseduffield/lazygit": ("lazygit", "v", ""),
    "pola-rs/polars": ("Polars", "py-", ""),
    "huggingface/transformers": ("Transformers", "v", ""),
    "vllm-project/vllm": ("vLLM", "v", ""),
    "microsoft/playwright": ("Playwright", "v", ""),
    "nestjs/nest": ("NestJS", "v", ""),
    "valkey-io/valkey": ("Valkey", "", ""),
    "duckdb/duckdb": ("DuckDB", "v", ""),
    "go-gitea/gitea": ("Gitea", "v", ""),
    "mastodon/mastodon": ("Mastodon", "v", ""),
    "grafana/grafana": ("Grafana", "v", ""),
    "syncthing/syncthing": ("Syncthing", "v", ""),
    "home-assistant/core": ("Home Assistant", "", ""),
    "langchain-ai/langchain": ("LangChain", "langchain==", ""),
    "sveltejs/svelte": ("Svelte", "svelte@", ""),
    "vitejs/vite": ("Vite", "v", ""),
    "redis/redis": ("Redis", "", ""),
    "n8n-io/n8n": ("n8n", "n8n@", ""),
    "godotengine/godot": ("Godot", "", "-stable"),
}
JQ = "[.[] | {tag_name, name, draft, prerelease, published_at, body, html_url}]"


def version(tag, prefix, suffix):
    """R2: tuple of ints, or None if the tag does not have the line's shape."""
    if not tag.startswith(prefix) or not tag.endswith(suffix):
        return None
    core = tag[len(prefix):len(tag) - len(suffix)]
    parts = core.split(".")
    if len(parts) < 2 or not all(p.isdigit() for p in parts):
        return None
    return tuple(int(p) for p in parts)


def user_notes(body):
    """R4."""
    rest = "\n".join(l for l in body.splitlines() if "full changelog" not in l.lower()).strip()
    return len(body) >= 400 and len(rest) >= 400


def releases(repo):
    out, times = [], []
    for page in range(1, MAX_PAGES + 1):
        data, at = gh([f"repos/{repo}/releases?per_page=100&page={page}", "--jq", JQ])
        times.append(at)
        if not isinstance(data, list):
            raise RuntimeError(f"{repo} releases page {page}: {str(data)[:300]}")
        out.extend(data)
        pubs = [r["published_at"] for r in data if r.get("published_at")]
        if len(data) < 100 or (pubs and min(pubs) < OLDEST_PAGE):
            break
    return out, max(times)


def build_repo(repo, ex):
    product, prefix, suffix = REPOS[repo]
    meta = repo_meta(repo)
    info = {"repo": repo, "name": product, "tag_prefix": prefix, "tag_suffix": suffix,
            "stars": meta["stars"], "stars_fetched_at": meta["stars_fetched_at"]}
    if meta["stars"] < MIN_STARS or meta["archived"]:
        info["skipped"] = "stars < 20000 or archived"
        return info, []
    rels, fetched = releases(repo)
    stable = []
    for r in rels:
        v = version(r["tag_name"], prefix, suffix)
        if v and not r["draft"] and not r["prerelease"] and r.get("published_at"):
            stable.append((v, r))
    stats = {"releases_read": len(rels), "stable_in_line_shape": len(stable), "in_window": 0,
             "user_notes": 0, "excluded": 0, "checked": 0, "no_prev": 0, "not_ahead": 0,
             "commits_out_of_range": 0}
    pending = []
    for v, r in stable:
        if not START <= r["published_at"] <= END:
            continue
        stats["in_window"] += 1
        body = r.get("body") or ""
        if not user_notes(body):
            continue
        stats["user_notes"] += 1
        if ex.tag(repo, r["tag_name"]):
            stats["excluded"] += 1
            continue
        pending.append((v, r))
    pending.sort(key=lambda vr: draw_key(repo, vr[1]["tag_name"]))
    kept = []
    for v, r in pending:
        if len(kept) == PER_REPO:
            break
        stats["checked"] += 1
        line = [(pv, p) for pv, p in stable
                if pv[0] == v[0] and pv < v and p["published_at"] < r["published_at"]]
        if not line:
            stats["no_prev"] += 1
            continue
        prev = max(line, key=lambda pp: pp[0])[1]
        cmp_path = f"repos/{repo}/compare/{quote(prev['tag_name'], safe='')}...{quote(r['tag_name'], safe='')}"
        cmp, at = gh([cmp_path, "--jq", "{status, ahead_by, behind_by, total_commits}"])
        fetched = max(fetched, at)
        if not isinstance(cmp, dict) or cmp.get("status") != "ahead":
            stats["not_ahead"] += 1
            continue
        commits = cmp["ahead_by"]
        if not 5 <= commits <= 200:
            stats["commits_out_of_range"] += 1
            continue
        tag = r["tag_name"]
        kept.append({
            "id": f"{short_repo(repo)}-{'.'.join(map(str, v))}{suffix}",
            "repo": repo, "stars": meta["stars"], "tag": tag, "prev": prev["tag_name"],
            "name": product, "published_at": r["published_at"], "commits": commits,
            "notes_len": len(r["body"]), "url": r["html_url"], "_body": r["body"],
        })
    info["data_fetched_at"] = fetched
    info["counts"] = stats
    info["kept"] = len(kept)
    return info, kept


def main():
    ex = Exclusions()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(lambda r: build_repo(r, ex), sorted(REPOS)))
    per_repo = {info["repo"]: kept for info, kept in results if kept}
    picked = round_robin(per_repo, N)
    picked.sort(key=lambda c: (c["repo"].lower(), c["tag"]))
    notes_dir = os.path.join(POOLS, "release-notes")
    os.makedirs(notes_dir, exist_ok=True)
    ids = set()
    for c in picked:
        body = c.pop("_body")
        assert c["id"] not in ids, c["id"]
        ids.add(c["id"])
        with open(os.path.join(notes_dir, c["id"] + ".md"), "w", encoding="utf-8", newline="") as f:
            f.write(body)
    for f in os.listdir(notes_dir):  # drop notes left from an older run
        if f.endswith(".md") and f[:-3] not in ids:
            os.remove(os.path.join(notes_dir, f))
    used = {}
    for c in picked:
        used[c["repo"]] = used.get(c["repo"], 0) + 1
    repos = []
    for info, _ in results:
        info["picked"] = used.get(info["repo"], 0)
        repos.append(info)
    repos.sort(key=lambda r: r["repo"].lower())
    write_pool(os.path.join(POOLS, "release.json"), "release", __doc__, repos, picked)
    print(f"release: {len(picked)} candidates from {len(used)} repos")
    for r in repos:
        print(" ", r["repo"], r["stars"], r.get("counts"), "kept", r.get("kept"), "picked", r["picked"])
    if len(picked) < N:
        raise SystemExit(f"only {len(picked)} of {N}")


if __name__ == "__main__":
    main()
