#!/usr/bin/env python3
"""Rows for OpenCode, Pi, Codex from norm.json (usageproxy provider usage). Usage: agents_rows.py ART_DIR OUT.json. No regex.
Anthropic: analyze.PRICES, writes priced as 5m. gpt-5-mini: 0.25 in, 0.025 cached read, 2.00 out per Mtok (OpenAI list price)."""
import collections, glob, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import analyze as A
def cost(r):
    if r["model"] == "gpt-5-mini": return (r["input"] * .25 + r["cache_read"] * .025 + r["output"] * 2.0) / 1e6
    return A.usd(r["model"], r["input"], r["cache_write"], 0, r["cache_read"], r["output"])
g = collections.defaultdict(lambda: collections.defaultdict(dict)); bad = []
for f in glob.glob(sys.argv[1] + "/*/*/norm.json"):
    n = json.load(open(f))
    if not str(n.get("area", "")).startswith("fix-ci-"): continue
    n["passed"] = A.truthy(n.get("passed"))
    if not n.get("requests"): bad.append({k: n.get(k) for k in ("agent", "task", "arm", "run_id", "passed", "failed_requests")}); continue
    g[(n["agent"], n["model"])][n["task"]][n["arm"]] = n
rows = []
for (ag, m), ts in sorted(g.items()):
    by = {}; dc = []; gc = []; td = tg = b = c = pd = pg = 0
    for t, a in sorted(ts.items()):
        if len(a) < 2: continue
        d, w = a["direct-ts"], a["gateway"]; cd, cw = cost(d), cost(w)
        by[t] = [math.log(cw / cd)]; dc.append(cd); gc.append(cw); td += sum(d["tools"].values()); tg += sum(w["tools"].values())
        pd += d["passed"]; pg += w["passed"]; b += d["passed"] and not w["passed"]; c += w["passed"] and not d["passed"]
    k = len(by)
    if not k:
        bad.append({'agent': ag, 'model': m, 'note': 'no complete direct/gateway pair'}); continue
    mm = sum(v[0] for v in by.values()) / k; ci = A.boot(by)
    mix = round(tg / td, 3) if td else None; p = round(A.mcnemar(b, c), 3)
    rows.append(dict(area="fix-ci", agent=ag, model=m, n=k, saving_pct=A.pct(mm), ci_pct=[A.pct(ci[1]), A.pct(ci[0])], cheaper=f"{sum(v[0] < 0 for v in by.values())}/{k}",
        direct_usd=round(sum(dc) / k, 4), gateway_usd=round(sum(gc) / k, 4), quality=f"pass {pd}/{k} -> {pg}/{k}, McNemar p={p}", tool_calls=[td, tg], tool_mix_ratio=mix,
        passed_bar=bool(ci[1] < 0 and (p >= .05 or pg >= pd) and mix and mix >= .7), total_usd=round(sum(dc) + sum(gc), 4)))
json.dump({"rows": rows, "unusable_runs": bad}, open(sys.argv[2], "w"), indent=1)
for r in rows: print(r)
print("unusable", bad)
