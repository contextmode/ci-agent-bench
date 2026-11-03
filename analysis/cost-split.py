#!/usr/bin/env python3
"""Recompute the cost split and the cache-write share of a direct CI agent run from public Actions artifacts.

Usage: python3 -I analysis/cost-split.py ART_DIR [--all] [--json OUT]\nDefault: the three jobs the website shows (fix-ci, fix-mention, labels). --all adds the other jobs in the rows.
ART_DIR/<run_id>/<artifact>/ holds one artifact per run (gh run download RUN_ID -R contextmode/ci-agent-bench -D ART_DIR/RUN_ID).
Run ids come from confirm-1101/r1/rows.jsonl and confirm-1101/run2/rows.jsonl (arm == direct-ts, success, not error).
Prices: confirm-1101/prices/anthropic-pricing-2026-11-01.md (Sonnet 5.5: in 2.00, 5m write 2.50, 1h write 4.00, read 0.10, out 10.00 per MTok).
No regex.
"""
import collections, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
PUBLISHED = ("fix-ci", "fix-mention", "labels")  # the jobs the website shows; add --all for every job in the rows
P = {"in": 2.0, "w5": 2.5, "w1": 4.0, "rd": 0.10, "out": 10.0}  # Sonnet 5.5, USD per MTok


def events(path):
    raw = open(path).read()
    try:
        d = json.loads(raw)
        return d if isinstance(d, list) else [d]
    except ValueError:
        return [json.loads(l) for l in raw.splitlines() if l.strip().startswith("{")]


def requests(ev):
    """One usage row per API request: last assistant event per message id, main agent only."""
    seen, order = {}, []
    for e in ev:
        if e.get("type") != "assistant" or e.get("parent_tool_use_id"):
            continue
        m = e.get("message") or {}
        if m.get("id") not in seen:
            order.append(m.get("id"))
        seen[m.get("id")] = m.get("usage") or {}
    return [seen[i] for i in order]


def tok(u):
    cc = u.get("cache_creation") or {}
    w5 = cc.get("ephemeral_5m_input_tokens", 0) or 0
    w1 = cc.get("ephemeral_1h_input_tokens", 0) or 0
    total = u.get("cache_creation_input_tokens", 0) or 0
    if w5 + w1 != total:
        w5 = total - w1
    return dict(i=u.get("input_tokens", 0) or 0, w5=w5, w1=w1, rd=u.get("cache_read_input_tokens", 0) or 0)


def usd(i=0, w5=0, w1=0, rd=0, out=0):
    return (i * P["in"] + w5 * P["w5"] + w1 * P["w1"] + rd * P["rd"] + out * P["out"]) / 1e6


def direct_ids():
    out = {}
    for f in ("confirm-1101/r1/rows.jsonl", "confirm-1101/run2/rows.jsonl"):
        for l in open(os.path.join(LAB, f)):
            r = json.loads(l)
            if (r.get("area") in PUBLISHED or "--all" in sys.argv) and r.get("arm") == "direct-ts" and r.get("conclusion") == "success" and not r.get("is_error") and r.get("model") == "claude-sonnet-5-5":
                out[r["run_id"]] = r["area"]
    return out


def main():
    art = sys.argv[1]
    ids = direct_ids()
    per_area = collections.defaultdict(lambda: collections.Counter())
    n = collections.Counter()
    wshare = collections.defaultdict(list)
    nreq = collections.defaultdict(list)
    for rid, area in sorted(ids.items()):
        fs = glob.glob(os.path.join(art, rid, "*", "claude-output.json"))
        if not fs:
            continue
        ev = events(fs[0])
        res = next((e for e in reversed(ev) if e.get("type") == "result"), None)
        rq = requests(ev)
        if not res or not rq:
            continue
        # Per-request output in the stream is a start-of-message value. Use the result totals for output and thinking.
        out = (res.get("usage") or {}).get("output_tokens", 0) or 0
        th = ((res.get("usage") or {}).get("output_tokens_details") or {}).get("thinking_tokens", 0) or 0
        th = min(th, out)
        t = [tok(u) for u in rq]
        # Fixed prefix = the request-1 write plus every cache read (reads re-read the prefix). Tool results and history =
        # all later writes and uncached input. Same grouping as lab/ci-night/stats.py.
        c = collections.Counter()
        c["prefix"] = usd(i=t[0]["i"], w5=t[0]["w5"], w1=t[0]["w1"]) + usd(rd=sum(x["rd"] for x in t))
        c["tool_results"] = sum(usd(i=x["i"], w5=x["w5"], w1=x["w1"]) for x in t[1:])
        c["thinking"] = usd(out=th)
        c["answer"] = usd(out=out - th)
        total = sum(c.values())
        writes = sum(usd(w5=x["w5"], w1=x["w1"]) for x in t)
        for k, v in c.items():
            per_area[area][k] += v
        per_area[area]["_total"] += total
        per_area[area]["_writes"] += writes
        n[area] += 1
        wshare[area].append(100 * writes / total)
        nreq[area].append(len(rq))
    rows = {}
    for area in sorted(per_area):
        a = per_area[area]
        rows[area] = {k: round(100 * a[k] / a["_total"], 1) for k in ("prefix", "tool_results", "thinking", "answer")}
        rows[area]["cache_write_share"] = round(100 * a["_writes"] / a["_total"], 1)
        rows[area]["runs"] = n[area]
        rows[area]["mean_requests"] = round(sum(nreq[area]) / len(nreq[area]), 1)
    mean = {k: round(sum(r[k] for r in rows.values()) / len(rows), 1) for k in ("prefix", "tool_results", "thinking", "answer")}
    print("area | runs | requests/run | prefix | tool results+history | thinking | answer | cache writes (share of bill)")
    for a, r in rows.items():
        print(f"{a} | {r['runs']} | {r['mean_requests']} | {r['prefix']} | {r['tool_results']} | {r['thinking']} | {r['answer']} | {r['cache_write_share']}")
    print("MEAN over areas:", mean)
    if "--json" in sys.argv:
        json.dump({"areas": rows, "mean": mean}, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)


main()
