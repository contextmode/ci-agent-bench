#!/usr/bin/env python3
"""Build RESULTS-r2.md from the round-2 analysis (PLAN-r2.md sections 4-9). No regex. Never reads a key.

Usage (repo root): python3 confirm-1101/bin/results_r2.py VERDICTS.json OUT.md
Inputs: run2/analysis.json, run2/agents.json (round 2); r2/an.json, r2/agents.json (round 1, all 150 runs);
run2/dispatch.jsonl, run2/dispatch-review-rerun.jsonl; VERDICTS.json (blind Opus judge, A/B key applied).
Writes run2/final.json (rows with judge quality, pooled rows, gaps, human-check list) and OUT.md."""
import collections, datetime, hashlib, json, math, os, statistics, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import analyze as A  # noqa: E402

VER, OUT = sys.argv[1], sys.argv[2]
J = lambda p: json.load(open(os.path.join(HERE, p)))
an2, ag2, an1, ag1 = J("run2/analysis.json"), J("run2/agents.json"), J("r2/an.json"), J("r2/agents.json")
V = json.load(open(VER))


def judge(area, rnd, pair_tasks):
    w = collections.Counter()
    for v in V.values():
        if v["area"] == area and v["round"] == rnd and v["task"] in pair_tasks: w[v["winner_arm"]] += 1
    p = round(A.mcnemar(w["direct-ts"], w["gateway"]), 3)
    ok = (w["gateway"] >= w["direct-ts"] or p >= 0.05) if sum(w.values()) else None
    txt = f"judge (Opus 5.5, blind) gateway {w['gateway']} / direct {w['direct-ts']} / tie {w['tie']}, sign p={p}" if sum(w.values()) else "not judged"
    return ok, txt, dict(w)


def norm(r, rnd):
    r = dict(r); r["round"] = rnd
    if r["area"] in ("release", "review"):
        ok, txt, w = judge(r["area"], rnd, {p["task"] for p in r.get("pairs") or []})
        r["quality_ok"], r["quality_text"], r["judge"] = ok, txt, w
        ci = r["ci_pct"]
        r["passed_bar"] = bool(ci and ci[0] > 0 and ok and r.get("tool_mix_ratio") and r["tool_mix_ratio"] >= 0.7)
    if "quality_text" not in r: r["quality_text"] = r.get("quality")
    return r


rows2 = [norm(r, "r1" if False else "r2") for r in an2["rows"]] + [norm(r, "r2") for r in ag2["rows"]]
rows1 = [norm(r, "r1") for r in an1["rows"]] + [norm(r, "r1") for r in ag1["rows"]]


def pooled(key):
    by = {}; dc = []; gc = []; td = tg = 0; npair = collections.Counter()
    for rnd, rows in (("r1", rows1), ("r2", rows2)):
        for r in rows:
            if (r["area"], r["agent"], r["model"]) != key: continue
            for p in r.get("pairs") or []:
                by[rnd + "|" + p["task"]] = [math.log(p["gateway_usd"] / p["direct_usd"])]
                dc.append(p["direct_usd"]); gc.append(p["gateway_usd"]); npair[rnd] += 1
                if p.get("tools"): td += p["tools"][0]; tg += p["tools"][1]
    n = len(by)
    if n < 2: return None
    m = sum(v[0] for v in by.values()) / n; ci = A.boot(by)
    return dict(area=key[0], agent=key[1], model=key[2], n=n, n_r1=npair["r1"], n_r2=npair["r2"], saving_pct=A.pct(m),
                ci_pct=[A.pct(ci[1]), A.pct(ci[0])], cheaper=f"{sum(1 for v in by.values() if v[0] < 0)}/{n}",
                direct_usd=round(sum(dc) / n, 4), gateway_usd=round(sum(gc) / n, 4), tool_mix_ratio=round(tg / td, 3) if td else None)


keys = sorted({(r["area"], r["agent"], r["model"]) for r in rows1 + rows2})
pool = [p for p in (pooled(k) for k in keys) if p]

# spacing: gaps between dispatches of the same lane and arm
D = [json.loads(l) for l in open(os.path.join(HERE, "run2/dispatch.jsonl"))]
D += [dict(x, lane="action-sonnet-review-rerun") for x in (json.loads(l) for l in open(os.path.join(HERE, "run2/dispatch-review-rerun.jsonl")))]
seq = collections.defaultdict(list)
for x in D:
    if x.get("wf") and x.get("rc") == 0: seq[(x["lane"], x["arm"])].append(datetime.datetime.strptime(x["t"], "%Y-%m-%dT%H:%M:%SZ"))
gaps = {}
for (ln, arm), ts in sorted(seq.items()):
    g = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
    if g: gaps[f"{ln} {arm}"] = dict(n=len(ts), min_s=min(g), median_s=statistics.median(g))
guards = [x for x in D if "guard_before" in x or "guard_after" in x]
paused = sorted({json.loads(g.split(" ", 2)[2])["used_paused"] for x in guards for g in (x.get("guard_before"), x.get("guard_after")) if g and g.startswith("quota ")})

# human check: lowest five sha256 per area
human = {}
for area in ("release", "review"):
    c = [(hashlib.sha256(f"confirm-1101-r2-human|{area}|{v['task']}".encode()).hexdigest(), k) for k, v in V.items() if v["area"] == area and v["round"] == "r2"]
    human[area] = [dict(jid=k, task=V[k]["task"], verdict=V[k]["winner_arm"], file=("lab/release/judge/" if area == "release" else "lab/review-action/judge/") + k + ".md", status="pending")
                   for _, k in sorted(c)[:5]]

json.dump(dict(rows_r2=rows2, rows_r1=rows1, pooled=pool, gaps=gaps, used_paused_seen=paused, human_check=human,
               cross_check=an2["cross_check"], errors=an2["errors"], agents_unusable=ag2["unusable_runs"]),
          open(os.path.join(HERE, "run2/final.json"), "w"), indent=1)


def fmt(r, pooled_row=False):
    ci = r["ci_pct"]
    base = f"| {r['area']} | {r['agent']} | {r['model']} | {r['n']} | {r['saving_pct']} | [{ci[0]}, {ci[1]}] | {r['cheaper']} | {r['direct_usd']} | {r['gateway_usd']} |"
    if pooled_row: return base + f" {r['n_r1']} + {r['n_r2']} | {r['tool_mix_ratio']} |"
    return base + f" {r['quality_text']} | {r['tool_mix_ratio']} | {'PASS' if r['passed_bar'] else 'no'} |"


H = "| area | agent | model | n | saving % | 95% CI | cheaper | direct $/run | gateway $/run |"
o = ["# confirm-1101 round 2 results", "",
     "Plan: PLAN-r2.md (commit a4770f7, GitHub push 2026-11-01T23:39:27Z, before any paid run).", "",
     "Saving = 1 - exp(mean log(gateway/direct)) over tasks; CI = paired bootstrap, 10000 draws, seed 1. Positive = gateway cheaper.",
     "Cost = provider usage x list price; gateway arm from the gateway ledger when it has rows for the session.", "",
     "## Round-2 rows (primary)", "", H + " quality | tool mix gw/direct | bar |", "|" + "---|" * 13]
o += [fmt(r) for r in rows2]
o += ["", "## Round-1 rows, same analysis (for reference)", "", H + " quality | tool mix gw/direct | bar |", "|" + "---|" * 13]
o += [fmt(r) for r in rows1]
o += ["", "## Pooled rows, round 1 + round 2 (secondary)", "", H + " pairs r1 + r2 | tool mix |", "|" + "---|" * 11]
o += [fmt(r, True) for r in pool]
o += ["", "## Cross-check", "", "```", json.dumps(an2["cross_check"], indent=1), "```", "",
      "## Spacing (seconds between dispatches of the same lane and arm)", "", "```", json.dumps(gaps, indent=1), "```", "",
      f"Quota guard used_paused values seen before and after every phase and lane: {paused}.", "",
      "## Human check (pending owner review; does not change any pass/fail)", ""]
for area, L in human.items():
    for h in L: o.append(f"- {area} {h['jid']}: judge says {h['verdict']} wins; file {h['file']}; {h['status']}")
o += ["", "## Unusable runs", "", "```", json.dumps(an2["errors"] + ag2["unusable_runs"], indent=1), "```", ""]
open(OUT, "w").write("\n".join(o) + "\n")
for r in rows2: print("R2", r["area"], r["agent"], r["model"], r["n"], r["saving_pct"], r["ci_pct"], r["quality_text"], r["tool_mix_ratio"], r["passed_bar"])
for r in pool: print("POOL", r["area"], r["agent"], r["model"], r["n"], r["saving_pct"], r["ci_pct"])
print("gaps min", min(g["min_s"] for g in gaps.values()), "paused", paused)
