# Paired cost analysis for the reproduce flow. Same method as the published table (lab/ci-night/stats.py):
#   saving   = -(exp(mean log(gateway cost / direct cost)) - 1), positive = gateway cheaper
#   95% CI   = bootstrap that resamples tasks (10,000 draws, seed 1)
#   cheaper  = pairs where the gateway run cost less
#   net      = mean direct cost - mean gateway cost - $0.0009 x API requests of the gateway run
# Usage: python3 reproduce/analyze.py STATE_JSON ARTIFACT_DIR [--json OUT] [--md OUT]
# STATE_JSON: {"lanes": {name: {"model":..., "runs": [{"seq", "arm", "task", "rid"}]}}}; ARTIFACT_DIR/<rid>/... holds
# each run's downloaded artifact (lab-metrics.json and claude-output.json or claude-stream.jsonl).
# Cost is total_cost_usd as Claude Code reports it for each run. No key is read or printed.
import collections, glob, json, math, random, sys

FEE = 0.0009
BASE_ARM, GW_ARM = "direct-ts", "gateway"


def first(pattern_list):
    for p in pattern_list:
        g = glob.glob(p)
        if g:
            return g[0]
    return None


def load_metrics(art, rid):
    f = first([f"{art}/{rid}/*/lab-metrics.json", f"{art}/{rid}/lab-metrics.json"])
    return json.load(open(f)) if f else None


def api_requests(art, rid, m):
    f = None
    for fn in ("claude-output.json", "claude-stream.jsonl"):
        f = first([f"{art}/{rid}/*/{fn}", f"{art}/{rid}/{fn}"])
        if f:
            break
    ids = set()
    if f:
        raw = open(f).read()
        try:
            x = json.loads(raw)
            x = x if isinstance(x, list) else [x]
        except ValueError:
            x = []
            for line in raw.splitlines():
                if line.strip().startswith("{"):
                    try:
                        x.append(json.loads(line))
                    except ValueError:
                        pass
        for e in x:
            if isinstance(e, dict) and e.get("type") == "assistant":
                ids.add((e.get("message") or {}).get("id"))
    return len(ids) or m.get("api_requests") or m.get("num_turns") or 0


def boot(pairs, draws=10000):
    by = collections.defaultdict(list)
    for t, d in pairs:
        by[t].append(d)
    tasks = list(by)
    if len(tasks) < 2:
        return None, None
    rng = random.Random(1)
    out = []
    for _ in range(draws):
        s = [x for t in (rng.choice(tasks) for _ in tasks) for x in by[t]]
        out.append(sum(s) / len(s))
    out.sort()
    return out[int(0.025 * draws)], out[int(0.975 * draws)]


def pct(x):
    return None if x is None else round((math.exp(x) - 1) * 100, 1)


def summarize(ps):
    if not ps:
        return None
    lr = [(b["_task"], math.log(g["total_cost_usd"] / b["total_cost_usd"])) for _, b, g in ps]
    mean = sum(x for _, x in lr) / len(lr)
    lo, hi = boot(lr)
    mb = sum(b["total_cost_usd"] for _, b, _g in ps) / len(ps)
    mg = sum(g["total_cost_usd"] for _, _b, g in ps) / len(ps)
    api = sum(g["_api"] for _, _b, g in ps) / len(ps)
    return dict(n=len(ps), saving_pct=-pct(mean), ci_pct=(None if lo is None else [-pct(hi), -pct(lo)]),
                cheaper=sum(1 for _, x in lr if x < 0), base_cost=round(mb, 4), gw_cost=round(mg, 4),
                net=round(mb - mg - FEE * api, 4),
                pairs=[dict(seq=s, task=json.loads(b["_task"]), direct=b["total_cost_usd"], gateway=g["total_cost_usd"],
                            direct_run=b["_rid"], gateway_run=g["_rid"]) for s, b, g in ps])


def analyze(state, art):
    res = {}
    for name, lane in state["lanes"].items():
        rows = collections.defaultdict(dict)
        for r in lane["runs"]:
            if not r.get("rid"):
                continue
            m = load_metrics(art, r["rid"])
            if m is None:
                continue
            m["_rid"] = r["rid"]
            m["_task"] = json.dumps(r["task"], sort_keys=True)
            m["_api"] = api_requests(art, r["rid"], m)
            rows[r["seq"]][r["arm"]] = m
        pairs = []
        for s, d in sorted(rows.items()):
            g, b = d.get(GW_ARM), d.get(BASE_ARM)
            if any((not x) or x.get("is_error") or not x.get("total_cost_usd") for x in (g, b)):
                continue
            pairs.append((s, b, g))
        res[name] = dict(model=lane.get("model"), cold=summarize([p for p in pairs if p[0] == 1]),
                         warm=summarize([p for p in pairs if p[0] > 1]), all=summarize(pairs),
                         runs={f"s{r['seq']}-{r['arm']}": r.get("rid") for r in lane["runs"]})
    return res


def fmt_ci(ci):
    return "n/a" if not ci else f"{ci[0]}% to {ci[1]}%"


def markdown(res, repo=None):
    out = ["## Paired CI cost: direct-ts vs gateway", "",
           "Saving = -(exp(mean log-ratio) - 1); positive = gateway cheaper. 95% CI = bootstrap over tasks (10,000, seed 1). "
           "Net = mean direct - mean gateway - $0.0009 x gateway API requests. Run 1 of each lane is cold; runs 2.. are warm.", "",
           "| area | model | pairs (warm/all) | warm saving | warm 95% CI | cheaper (warm) | direct $/run | gateway $/run | net $/run | all-runs saving |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in res.items():
        w, a = r["warm"], r["all"]
        if not a:
            out.append(f"| {name} | {r['model']} | 0 | no valid pair | | | | | | |")
            continue
        src = w or a
        out.append(f"| {name} | {r['model']} | {w['n'] if w else 0}/{a['n']} | {src['saving_pct']}% | {fmt_ci(src['ci_pct'])} | "
                   f"{src['cheaper']}/{src['n']} | ${src['base_cost']} | ${src['gw_cost']} | ${src['net']} | {a['saving_pct']}% |")
    out += ["", "Runs (direct, gateway) per pair:", ""]
    for name, r in res.items():
        for p in (r["all"] or {}).get("pairs", []):
            link = (lambda rid: f"[{rid}](https://github.com/{repo}/actions/runs/{rid})" if repo else str(rid))
            out.append(f"- {name} s{p['seq']}: direct {link(p['direct_run'])} ${p['direct']:.4f}, gateway {link(p['gateway_run'])} ${p['gateway']:.4f}")
    if any(not (r["warm"] and r["warm"]["n"] >= 2) for r in res.values()):
        out += ["", "A lane with fewer than 2 warm pairs falls back to all pairs, and a CI needs 2 or more tasks."]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    state, art = json.load(open(args[0])), args[1]
    opts = dict(zip(args[2::2], args[3::2]))
    res = analyze(state, art)
    if "--json" in opts:
        json.dump(res, open(opts["--json"], "w"), indent=1)
    md = markdown(res, opts.get("--repo"))
    if "--md" in opts:
        open(opts["--md"], "a").write(md)
    print(md)
