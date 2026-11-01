#!/usr/bin/env python3
"""confirm-1101 analysis (round 1, price-fixed). No regex.

Usage: analyze.py ART_DIR --runs runs.json [--ledger ledger.json] [--json OUT] [--md OUT] [--rows OUT.jsonl]

ART_DIR/<run_id>/<artifact>/ holds one GitHub artifact per run:
  claude-output.json (claude -p stream-json/json, or the action execution file) plus norm.json (confirm-claude)
  or lab-metrics.json (confirm-review).
runs.json: `gh run list --json databaseId,workflowName,status,conclusion,createdAt,displayTitle,headSha`.
ledger.json: gateway `/__ops-rows?tenant=t_ci_lab_1&kind=ledger` (gateway arm only).

Cost of a run = sum over every model in the result's modelUsage of
  input x base + 5m-write x w5 + 1h-write x w1h + cache-read x read + output x out   (list prices, per Mtok,
  docs.anthropic.com/en/docs/about-claude/pricing.md, saved in prices/). These are the provider's own usage counts
  as reported to the client; side calls (title, Haiku) are included because they are paid.
Gateway arm: when the ledger has rows for the run's session, the cost is the ledger usage (every upstream call the
gateway made, per call, at the same list prices). The client misses gateway-side upstream loops and reports the side
call under the main model, so the client-based number is kept as a cross-check, and a "max of both" variant is reported.
Cross-checks: client-based vs client total_cost_usd; client-based vs ledger billed_usd; ledger recomputed vs billed_usd.
"""
import collections, glob, json, math, os, random, sys

FEE = 0.0009
# model: (input, 5m write, 1h write, cache read, output) USD per Mtok. Global routing, no long-context tier for 5.5.
PRICES = {
    "claude-opus-5-5": (4.0, 5.0, 8.0, 0.20, 20.0),
    "claude-sonnet-5-5": (2.0, 2.5, 4.0, 0.10, 10.0),
    "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50),  # prompts up to 100k tokens
    "claude-haiku-4-5-20251001": (1.0, 1.25, 2.0, 0.10, 5.0),
}
OLD_PRICES = {"claude-sonnet-5-5": (3.0, 15.0), "claude-opus-5-5": (5.0, 25.0)}  # round-1 values, kept only to show the fix
HAIKU55_LONG = (0.50, 0.625, 1.0, 0.05, 2.50)


def price(model, prompt_tokens=0):
    if model == "claude-haiku-5-5" and prompt_tokens > 100000:
        return HAIKU55_LONG
    return PRICES[model]


def usd(model, inp, w5, w1, rd, out):
    p = price(model, inp + w5 + w1 + rd)
    return (inp * p[0] + w5 * p[1] + w1 * p[2] + rd * p[3] + out * p[4]) / 1e6


def events(path):
    raw = open(path).read()
    try:
        d = json.loads(raw)
        return d if isinstance(d, list) else [d]
    except ValueError:
        out = []
        for line in raw.splitlines():
            if line.strip().startswith("{"):
                try: out.append(json.loads(line))
                except ValueError: pass
        return out


def truthy(v):
    return v is True or v in ("true", "True", "1")


def load_runs(art, runs_meta):
    meta = {str(x["databaseId"]): x for x in runs_meta}
    out = []
    for d in sorted(glob.glob(os.path.join(art, "*", "*"))):
        rid = os.path.basename(os.path.dirname(d)); fs = set(os.listdir(d)); m = meta.get(rid, {})
        title = (m.get("displayTitle") or "").split()
        r = {"run_id": rid, "workflow": m.get("workflowName"), "conclusion": m.get("conclusion"), "created": m.get("createdAt"),
             "head_sha": (m.get("headSha") or "")[:7], "agent": "claude-code"}
        if title[:1] == ["cc"]:
            r.update(area=title[1], task=title[2], arm=title[3], model=title[4])
        elif title[:1] == ["review"]:
            repo, pr = title[2].split("#")
            r.update(area="review", task=repo.split("/")[1] + "-" + pr, arm=title[1], model="claude-sonnet-5-5", agent="claude-code-action")
        if "claude-output.json" not in fs:
            r["error"] = "no claude output (" + str(m.get("conclusion")) + ")"; out.append(r); continue
        ev = events(os.path.join(d, "claude-output.json"))
        res = next((e for e in reversed(ev) if isinstance(e, dict) and e.get("type") == "result"), None)
        if not res:
            r["error"] = "no result event"; out.append(r); continue
        r.update(session=res.get("session_id"), client_cost=res.get("total_cost_usd"), is_error=res.get("is_error"),
                 geo=(res.get("usage") or {}).get("inference_geo"))
        mu = res.get("modelUsage") or {}
        per = {}
        for model, u in mu.items():
            w = u.get("cacheCreationInputTokens", 0) or 0
            w5 = u.get("cacheCreationEphemeral5mInputTokens", 0) or 0; w1 = u.get("cacheCreationEphemeral1hInputTokens", 0) or 0
            if w5 + w1 != w: w5 = w - w1  # unsplit writes priced as 5m (none seen in round 1)
            per[model] = dict(input=u.get("inputTokens", 0) or 0, w5=w5, w1=w1, read=u.get("cacheReadInputTokens", 0) or 0,
                              output=u.get("outputTokens", 0) or 0, client_usd=u.get("costUSD"))
            per[model]["usd"] = usd(model, per[model]["input"], w5, w1, per[model]["read"], per[model]["output"])
        r["models"] = per
        r["cost"] = sum(v["usd"] for v in per.values())
        old = OLD_PRICES.get(r.get("model"))  # round-1 analyze.py (wrong): main model only, base x1.25 write, x0.1 read
        u0 = per.get(r.get("model"))
        if old and u0:
            r["old_cost"] = (u0["input"] * old[0] + (u0["w5"] + u0["w1"]) * old[0] * 1.25 + u0["read"] * old[0] * 0.1 + u0["output"] * old[1]) / 1e6
        if "norm.json" in fs:
            n = json.load(open(os.path.join(d, "norm.json")))
            r["tools"] = n.get("tools") or {}; r["requests"] = n.get("requests")
            if "passed" in n: r["passed"] = truthy(n["passed"])
            if "f1" in n: r["f1"] = float(n["f1"])
        if "lab-metrics.json" in fs:
            lm = json.load(open(os.path.join(d, "lab-metrics.json")))
            tc = collections.Counter(t for p in lm.get("per_message_usage") or [] for t in p.get("tools") or [] if t)
            r["tools"] = dict(tc); r["requests"] = lm.get("api_requests")
        out.append(r)
    return out


def attach_ledger(runs, ledger_rows):
    by = collections.defaultdict(list)
    for x in ledger_rows:
        by[x["thread_key"].split(":")[0]].append(x)
    for r in runs:
        if r.get("arm") != "gateway" or not r.get("session"): continue
        rows = by.get(r["session"], [])
        r["ledger_rows"] = len(rows)
        r["ledger_usd"] = sum(x["billed_usd"] or 0 for x in rows)
        rec = 0.0; extra = 0.0; extra_models = collections.Counter()
        for x in rows:
            for lp in x.get("loops") or []:
                c = usd(x["model"], lp["input"], lp["cache_write_5m"] + lp["cache_write_unsplit"], lp["cache_write_1h"], lp["cache_read"], lp["output"])
                rec += c
                if x["model"] not in r["models"]:
                    extra += c; extra_models[x["model"]] += 1
        r["ledger_recomputed_usd"] = rec
        r["gw_only_side_usd"] = extra; r["gw_only_side_models"] = dict(extra_models)
        r["upstream_calls"] = sum(len(x.get("loops") or []) for x in rows)
        r["client_based_cost"] = r["cost"]
        if rows:  # the ledger lists every upstream call the gateway made for this session: that is the bill
            r["cost"] = rec


def boot(by, draws=10000):
    tasks = sorted(by)
    if len(tasks) < 2: return None
    rng = random.Random(1); out = []
    for _ in range(draws):
        s = [x for t in (rng.choice(tasks) for _ in tasks) for x in by[t]]
        out.append(sum(s) / len(s))
    out.sort(); return out[int(.025 * draws)], out[int(.975 * draws)]


def pct(x): return None if x is None else round(-(math.exp(x) - 1) * 100, 1)


def mcnemar(b, c):
    n = b + c
    if n == 0: return 1.0
    return min(1.0, sum(math.comb(n, i) for i in range(min(b, c) + 1)) / 2 ** n * 2)


def analyse(runs, cost_key):
    g = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in runs:
        if r.get("error"): continue
        g[(r["area"], r["agent"], r["model"])][r["task"]][r["arm"]] = r
    rows = []
    for (area, agent, model), tasks in sorted(g.items()):
        by = {}; dc = []; gc = []; req = []; b = c = 0; pd_n = pg_n = 0; fd = []; fg = []; td = tg = 0; gw_first = 0; pairs = []
        for t, arms in sorted(tasks.items()):
            if "direct-ts" not in arms or "gateway" not in arms: continue
            d, w = arms["direct-ts"], arms["gateway"]
            cd, cw = cost_key(d), cost_key(w)
            if not cd or not cw or cd <= 0 or cw <= 0: continue
            by[t] = [math.log(cw / cd)]; dc.append(cd); gc.append(cw); req.append(w.get("requests") or 0)
            td += sum((d.get("tools") or {}).values()); tg += sum((w.get("tools") or {}).values())
            gw_first += (w["created"] or "") < (d["created"] or "")
            if "passed" in d and "passed" in w:
                pd_n += d["passed"]; pg_n += w["passed"]; b += d["passed"] and not w["passed"]; c += w["passed"] and not d["passed"]
            if "f1" in d and "f1" in w: fd.append(d["f1"]); fg.append(w["f1"])
            pairs.append({"task": t, "direct_run": d["run_id"], "gateway_run": w["run_id"], "direct_usd": round(cd, 5), "gateway_usd": round(cw, 5),
                          "saving_pct": round((1 - cw / cd) * 100, 1), "passed": [d.get("passed"), w.get("passed")] if "passed" in d else None,
                          "f1": [d.get("f1"), w.get("f1")] if "f1" in d else None,
                          "tools": [sum((d.get("tools") or {}).values()), sum((w.get("tools") or {}).values())]})
        n = len(by)
        if not n: continue
        m = sum(v[0] for v in by.values()) / n; ci = boot(by)
        md, mg = sum(dc) / n, sum(gc) / n
        mix = round(tg / td, 3) if td else None
        if area.startswith("fix"):
            q = {"direct_pass": pd_n, "gateway_pass": pg_n, "n": n, "mcnemar_p": round(mcnemar(b, c), 3)}
            qok = q["mcnemar_p"] >= 0.05 or pg_n >= pd_n; qtxt = f"pass {pd_n}/{n} -> {pg_n}/{n}, McNemar p={q['mcnemar_p']}"
        elif area == "labels":
            q = {"f1_direct": round(sum(fd) / len(fd), 3), "f1_gateway": round(sum(fg) / len(fg), 3)}
            qok = q["f1_gateway"] >= q["f1_direct"] - 0.05; qtxt = f"F1 {q['f1_direct']} -> {q['f1_gateway']}"
        else:
            q = None; qok = None; qtxt = "not judged (judge not run)"
        passed = bool(ci and ci[1] < 0 and qok and mix is not None and mix >= 0.7)
        rows.append({"area": area, "agent": agent, "model": model, "n": n, "saving_pct": pct(m),
                     "ci_pct": None if ci is None else [pct(ci[1]), pct(ci[0])],
                     "cheaper": f"{sum(1 for v in by.values() if v[0] < 0)}/{n}", "direct_usd": round(md, 4), "gateway_usd": round(mg, 4),
                     "quality": q, "quality_text": qtxt, "quality_ok": qok, "tool_calls": [td, tg], "tool_mix_ratio": mix,
                     "tool_mix_ok": None if mix is None else mix >= 0.7,
                     "net_per_run": round(md - mg - FEE * (sum(req) / n), 4), "gateway_first": f"{gw_first}/{n}",
                     "passed_bar": passed, "pairs": pairs})
    return rows


def main():
    a = sys.argv; art = a[1]
    opt = {a[i]: a[i + 1] for i in range(2, len(a) - 1) if a[i].startswith("--")}
    runs = load_runs(art, json.load(open(opt["--runs"])))
    ledger = json.load(open(opt["--ledger"]))["rows"] if "--ledger" in opt else []
    attach_ledger(runs, ledger)
    ok = [r for r in runs if not r.get("error")]
    # cross-checks
    xc_client = [abs(r.get("client_based_cost", r["cost"]) - r["client_cost"]) / r["client_cost"] for r in ok if r.get("client_cost")]
    gw = [r for r in ok if r["arm"] == "gateway" and r.get("ledger_rows")]
    xc_ledger = [abs(r["client_based_cost"] - r["ledger_usd"]) / r["ledger_usd"] for r in gw if r["ledger_usd"]]
    gaps = [{"run_id": r["run_id"], "area": r["area"], "task": r["task"], "client_based_usd": round(r["client_based_cost"], 5),
             "ledger_usd": round(r["ledger_usd"], 5), "gap": round((r["client_based_cost"] - r["ledger_usd"]) / r["ledger_usd"], 3),
             "ledger_rows": r["ledger_rows"], "upstream_calls": r["upstream_calls"], "client_requests": r.get("requests"),
             "ledger_side_models": r["gw_only_side_models"]} for r in gw if r["ledger_usd"] and abs(r["client_based_cost"] - r["ledger_usd"]) / r["ledger_usd"] > 0.03]
    xc_ledger_rec = [abs(r["ledger_recomputed_usd"] - r["ledger_usd"]) / r["ledger_usd"] for r in gw if r["ledger_usd"]]
    def summ(x): return None if not x else {"n": len(x), "mean": round(sum(x) / len(x), 4), "max": round(max(x), 4), "over_3pct": sum(1 for v in x if v > 0.03)}
    out = {
        "runs_total": len(runs), "runs_ok": len(ok), "errors": [{k: r.get(k) for k in ("run_id", "area", "task", "arm", "model", "error")} for r in runs if r.get("error")],
        "total_cost_computed": round(sum(r["cost"] for r in ok), 4), "total_cost_client": round(sum(r["client_cost"] or 0 for r in ok), 4),
        "cross_check": {"computed_vs_client": summ(xc_client), "computed_vs_ledger_gateway": summ(xc_ledger),
                        "ledger_recomputed_vs_ledger_billed": summ(xc_ledger_rec),
                        "gw_only_side_usd_total": round(sum(r.get("gw_only_side_usd", 0) for r in ok), 5),
                        "gw_only_side_runs": sum(1 for r in ok if r.get("gw_only_side_usd")), "ledger_gaps_over_3pct": gaps},
        "rows": analyse(runs, lambda r: r["cost"]),
        "rows_client_cost": analyse(runs, lambda r: r.get("client_cost")),
        "rows_max_client_ledger": analyse(runs, lambda r: max(r["cost"], r.get("client_based_cost", r["cost"]))),
        "rows_old_prices_3_15": analyse(runs, lambda r: r.get("old_cost")),
    }
    if "--json" in opt: json.dump(out, open(opt["--json"], "w"), indent=1)
    if "--rows" in opt:
        with open(opt["--rows"], "w") as f:
            for r in runs:
                f.write(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()}, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in out.items() if not k.startswith("rows")}, indent=1))
    for r in out["rows"]:
        print(r["area"], r["model"], r["n"], r["saving_pct"], r["ci_pct"], r["cheaper"], r["quality_text"], r["tool_mix_ratio"], r["gateway_first"], r["passed_bar"])


if __name__ == "__main__":
    main()
