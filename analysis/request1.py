#!/usr/bin/env python3
"""Recompute request-1 size and request-1 cache behaviour, direct-ts arm vs gateway arm, from public Actions artifacts.

Usage: python3 -I analysis/request1.py ART_DIR [--all] [--json OUT]
ART_DIR/<run_id>/<artifact>/ as in analysis/cost-split.py. Runs: confirm-1101/r1/rows.jsonl and confirm-1101/run2/rows.jsonl,
success, not error, Sonnet 5.5. Request 1 = first main-agent request of a run. Size = input + cache write + cache read.
Cache reads and writes are the provider's counts as the client reports them. No regex.
"""
import collections, glob, json, os, statistics as st, sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLISHED = ("fix-ci", "fix-mention", "labels")  # the jobs the website shows; add --all for every job in the rows


def first_request(d):
    f = os.path.join(d, "lab-metrics.json")
    if os.path.exists(f):  # confirm-review: per_message_usage rows
        pm = [p for p in json.load(open(f)).get("per_message_usage") or [] if not p.get("sub")]
        if pm:
            p = pm[0]
            return p.get("in", 0) or 0, p.get("cw", 0) or 0, p.get("cr", 0) or 0
        return None
    raw = open(os.path.join(d, "claude-output.json")).read()
    try:
        ev = json.loads(raw); ev = ev if isinstance(ev, list) else [ev]
    except ValueError:
        ev = [json.loads(l) for l in raw.splitlines() if l.strip().startswith("{")]
    for e in ev:
        if e.get("type") == "assistant" and not e.get("parent_tool_use_id"):
            u = (e.get("message") or {}).get("usage") or {}
            return u.get("input_tokens", 0) or 0, u.get("cache_creation_input_tokens", 0) or 0, u.get("cache_read_input_tokens", 0) or 0
    return None


def main():
    art = sys.argv[1]
    runs = {}
    for f in ("confirm-1101/r1/rows.jsonl", "confirm-1101/run2/rows.jsonl"):
        for l in open(os.path.join(LAB, f)):
            r = json.loads(l)
            if (r.get("area") in PUBLISHED or "--all" in sys.argv) and r.get("conclusion") == "success" and not r.get("is_error") and r.get("model") == "claude-sonnet-5-5" and r.get("arm") in ("direct-ts", "gateway"):
                runs[r["run_id"]] = (r["area"], r["arm"])
    data = collections.defaultdict(list)
    for rid, (area, arm) in runs.items():
        ds = glob.glob(os.path.join(art, rid, "*"))
        if not ds:
            continue
        fr = first_request(ds[0])
        if fr:
            data[(area, arm)].append(fr)
    out = {}
    print("area | runs d/g | request 1 tokens direct -> gateway | smaller | gateway runs with 0 written on request 1 | request 1 read from cache, gateway | direct")
    for area in sorted({a for a, _ in data}):
        d, g = data[(area, "direct-ts")], data[(area, "gateway")]
        if not d or not g:
            continue
        sz = lambda L: st.mean(sum(x) for x in L)
        smaller = 100 * (1 - sz(g) / sz(d))
        zero = sum(1 for x in g if x[1] == 0)
        rd = 100 * sum(x[2] for x in g) / sum(sum(x) for x in g)
        rdd = 100 * sum(x[2] for x in d) / sum(sum(x) for x in d)
        out[area] = dict(direct_read_share_pct=round(rdd, 1), runs_direct=len(d), runs_gateway=len(g), req1_direct=round(sz(d)), req1_gateway=round(sz(g)), smaller_pct=round(smaller, 1),
                         gateway_zero_write_runs=zero, gateway_read_share_pct=round(rd, 1))
        print(f"{area} | {len(d)}/{len(g)} | {sz(d):,.0f} -> {sz(g):,.0f} | {smaller:.1f}% | {zero} of {len(g)} | {rd:.1f}% | {rdd:.1f}%")
    if "--json" in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)


main()
