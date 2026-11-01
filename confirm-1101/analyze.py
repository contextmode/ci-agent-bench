#!/usr/bin/env python3
"""confirm-1101 analysis. Usage: analyze.py ARTIFACT_DIR [--json OUT] [--md OUT]
ARTIFACT_DIR/<anything>/norm.json (one per run, from bin/norm.py), plus judge.json {pair_key: {"gw":score,"direct":score}} optional.
Pairs by (area, agent, model, task). Cost = tokens x PRICES (per Mtok). No regex."""
import collections, glob, json, math, random, sys

FEE = 0.0009
PRICES = {  # input, output per Mtok; cache write x1.25, cache read x0.1 (OpenAI: read x0.1, no write fee)
    "claude-sonnet-5-5": (3.0, 15.0), "claude-opus-5-5": (5.0, 25.0), "gpt-5-mini": (0.25, 2.0)}


def cost(r):
    i, o = PRICES[r["model"]]
    wr = 1.25 if r["model"].startswith("claude") else 1.0
    return (r["input"] * i + r["cache_write"] * i * wr + r["cache_read"] * i * 0.1 + r["output"] * o) / 1e6


def boot(by, draws=10000):
    tasks = list(by)
    if len(tasks) < 2:
        return None
    rng = random.Random(1); out = []
    for _ in range(draws):
        s = [x for t in (rng.choice(tasks) for _ in tasks) for x in by[t]]
        out.append(sum(s) / len(s))
    out.sort(); return out[int(.025 * draws)], out[int(.975 * draws)]


def pct(x): return None if x is None else round(-(math.exp(x) - 1) * 100, 1)


def mcnemar(b, c):  # exact two-sided
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(1.0, p)


def main():
    art = sys.argv[1]
    runs = []
    for f in glob.glob(art + "/*/norm.json") + glob.glob(art + "/*/*/norm.json"):
        r = json.load(open(f))
        if r.get("requests"): runs.append(r)
    judge = {}
    for f in glob.glob(art + "/judge.json"): judge = json.load(open(f))
    g = collections.defaultdict(dict)
    for r in runs:
        g[(r["area"], r.get("agent", "claude"), r["model"])].setdefault(r["task"], {}).setdefault(r["arm"], []).append(r)
    rows = []
    for (area, agent, model), tasks in sorted(g.items()):
        by = collections.defaultdict(list); dc = []; gc = []; req = []; disc_b = disc_c = 0; f1d = []; f1g = []
        td = tg = 0; xc = []
        for t, arms in tasks.items():
            if "direct-ts" not in arms or "gateway" not in arms: continue
            d = arms["direct-ts"][0]; w = arms["gateway"][0]
            cd, cw = cost(d), cost(w)
            if cd <= 0 or cw <= 0: continue
            by[t].append(math.log(cw / cd)); dc.append(cd); gc.append(cw); req.append(w["requests"])
            for r in (d, w):
                if r.get("client_cost"): xc.append(abs(cost(r) - r["client_cost"]) / r["client_cost"])
            td += sum(d["tools"].values()); tg += sum(w["tools"].values())
            if "passed" in d and "passed" in w:
                pd, pw = d["passed"] == "True" or d["passed"] is True or d["passed"] == "true", w["passed"] == "True" or w["passed"] is True or w["passed"] == "true"
                disc_b += (pd and not pw); disc_c += (pw and not pd); f1d.append(pd); f1g.append(pw)
            if "f1" in d and "f1" in w:
                f1d.append(float(d["f1"])); f1g.append(float(w["f1"]))
        n = len(by)
        if not n: continue
        m = sum(sum(v) / len(v) for v in by.values()) / n
        ci = boot(by)
        cheaper = sum(1 for v in by.values() if sum(v) / len(v) < 0)
        md, mg = sum(dc) / len(dc), sum(gc) / len(gc)
        net = md - mg - FEE * (sum(req) / len(req))
        qd = sum(f1d) / len(f1d) if f1d else None; qg = sum(f1g) / len(f1g) if f1g else None
        q = None
        if area.startswith("fix"):
            q = {"direct_pass": sum(f1d), "gateway_pass": sum(f1g), "n": len(f1d), "mcnemar_p": round(mcnemar(disc_b, disc_c), 3)}
        elif area == "labels":
            q = {"f1_direct": round(qd, 3), "f1_gateway": round(qg, 3)}
        elif judge:
            q = {"judge": judge.get(area)}
        mix = round(tg / td, 3) if td else None
        ci_pct = None if ci is None else [pct(ci[1]), pct(ci[0])]
        qual_ok = None
        if area.startswith("fix"): qual_ok = q["mcnemar_p"] >= 0.05 or q["gateway_pass"] >= q["direct_pass"]
        elif area == "labels": qual_ok = qg >= qd - 0.05
        elif q and q.get("judge"): qual_ok = q["judge"].get("gw", 0) >= q["judge"].get("direct", 0) - 0.5
        passed = bool(ci and ci[1] < 0 and qual_ok and mix is not None and mix >= 0.7)
        rows.append({"area": area, "agent": agent, "model": model, "n": n, "saving_pct": pct(m), "ci_pct": ci_pct, "cheaper": f"{cheaper}/{n}",
                     "direct_usd": round(md, 4), "gateway_usd": round(mg, 4), "quality": q, "quality_ok": qual_ok, "tool_mix_ratio": mix,
                     "tool_mix_ok": None if mix is None else mix >= 0.7, "net_per_run": round(net, 4),
                     "cost_vs_client_gap_mean": round(sum(xc) / len(xc), 4) if xc else None, "passed_bar": passed})
    out = {"rows": rows, "total_cost_computed": round(sum(cost(r) for r in runs), 2), "runs": len(runs)}
    for i, a in enumerate(sys.argv):
        if a == "--json": json.dump(out, open(sys.argv[i + 1], "w"), indent=1)
        if a == "--md":
            with open(sys.argv[i + 1], "w") as f:
                f.write("| area | agent | model | n | saving % | CI | direct $ | gateway $ | quality | tool mix | net/run | passed |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
                for r in rows:
                    f.write(f"| {r['area']} | {r['agent']} | {r['model']} | {r['n']} | {r['saving_pct']} | {r['ci_pct']} | {r['direct_usd']} | {r['gateway_usd']} | {r['quality']} | {r['tool_mix_ratio']} | {r['net_per_run']} | {r['passed_bar']} |\n")
    print(json.dumps(out, indent=1))


main()
