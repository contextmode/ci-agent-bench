# Round 1 stats. Usage: python3 -I stats.py /tmp/ci-agent-bench-r1/state.json /tmp/ci-agent-bench-r1/art
import glob, json, math, random, sys, collections
FEE = 0.0009
state = json.load(open(sys.argv[1])); art = sys.argv[2]

def load(rid):
    f = glob.glob(f"{art}/{rid}/*/lab-metrics.json") + glob.glob(f"{art}/{rid}/lab-metrics.json")
    return json.load(open(f[0])) if f else None

def boot(pairs, B=10000):
    by = collections.defaultdict(list)
    for t, d in pairs: by[t].append(d)
    tasks = list(by)
    if len(tasks) < 2: return None, None
    rng = random.Random(1); out = []
    for _ in range(B):
        s = [x for t in (rng.choice(tasks) for _ in tasks) for x in by[t]]
        out.append(sum(s) / len(s))
    out.sort(); return out[int(.025 * B)], out[int(.975 * B)]

def pct(x): return None if x is None else round((math.exp(x) - 1) * 100, 1)

def msgs(rid):
    d = None
    for fn in ("claude-output.json", "claude-stream.jsonl"):
        g = glob.glob(f"{art}/{rid}/*/{fn}") + glob.glob(f"{art}/{rid}/{fn}")
        if g: d = g[0]; break
    if not d: return []
    raw = open(d).read()
    try: x = json.loads(raw); x = x if isinstance(x, list) else [x]
    except Exception:
        x = []
        for l in raw.splitlines():
            if l.strip().startswith("{"):
                try: x.append(json.loads(l))
                except Exception: pass
    seen = {}; per = []
    for e in x:
        if isinstance(e, dict) and e.get("type") == "assistant":
            mm = e.get("message") or {}; mid = mm.get("id"); u = mm.get("usage") or {}
            tools = [c.get("name") for c in (mm.get("content") or []) if c.get("type") == "tool_use"]
            if mid in seen:
                per[seen[mid]]["u"] = u; per[seen[mid]]["tools"] += tools; continue
            seen[mid] = len(per); per.append({"u": u, "tools": tools})
    return per

def thinking(rid):
    g = glob.glob(f"{art}/{rid}/*/lab-metrics.json") + glob.glob(f"{art}/{rid}/lab-metrics.json")
    for fn in ("claude-output.json", "claude-stream.jsonl"):
        h = glob.glob(f"{art}/{rid}/*/{fn}") + glob.glob(f"{art}/{rid}/{fn}")
        if not h: continue
        raw = open(h[0]).read()
        try: x = json.loads(raw); x = x if isinstance(x, list) else [x]
        except Exception:
            x = [json.loads(l) for l in raw.splitlines() if l.strip().startswith("{")]
        for e in reversed(x):
            if isinstance(e, dict) and e.get("type") == "result" or (isinstance(e, dict) and "usage" in e and "total_cost_usd" in e):
                return ((e.get("usage") or {}).get("output_tokens_details") or {}).get("thinking_tokens", 0)
    return 0

def quality(m):
    if m.get("hit_top3") is not None: return "top3", m["hit_top3"]
    for k in ("passed", "f1", "top3", "top3_hit", "hit"):
        if m.get(k) is not None: return k, m[k]
    a = m.get("answer") or {}
    for k in ("f1", "top3", "top3_hit", "hit"):
        if a.get(k) is not None: return k, a[k]
    return None, None

def mix(ms):
    c = collections.Counter()
    for m in ms:
        for p in m.get("_msgs") or []:
            for t in p["tools"]:
                c[t] += 1
    return dict(c.most_common(8))

def split(ms):
    # Per run: price p per base input token from total = p*(in + 1.25 cw + 0.1 cr + 5 out), using RESULT totals
    # (per-message output in the stream is partial). Request 1 = prefix write; later cache writes = new tool results.
    acc = collections.Counter(); tot = 0
    for m in ms:
        pm = m.get("_msgs") or []
        if not pm or not m.get("total_cost_usd"): continue
        U = lambda u, k: u.get(k, 0) or 0
        out = m.get("output_tokens") or 0
        th = m.get("_thinking") or 0
        cw_all = sum(U(r["u"], "cache_creation_input_tokens") for r in pm)
        cr_all = sum(U(r["u"], "cache_read_input_tokens") for r in pm)
        in_all = sum(U(r["u"], "input_tokens") for r in pm)
        units = in_all + 1.25 * cw_all + 0.1 * cr_all + 5 * out
        if not units: continue
        p = m["total_cost_usd"] / units
        cw1 = U(pm[0]["u"], "cache_creation_input_tokens") + U(pm[0]["u"], "input_tokens")
        acc["prefix writes"] += p * 1.25 * cw1
        acc["new tool results"] += p * (1.25 * (cw_all - U(pm[0]["u"], "cache_creation_input_tokens")) + (in_all - U(pm[0]["u"], "input_tokens")))
        acc["prefix reads"] += p * 0.1 * cr_all
        acc["thinking"] += p * 5 * min(th, out); acc["output"] += p * 5 * (out - min(th, out))
        tot += m["total_cost_usd"]
    return {k: round(100 * v / tot, 1) for k, v in acc.items()} if tot else {}

res = {}
for name, L in state["lanes"].items():
    rows = collections.defaultdict(dict)  # seq -> arm -> m
    for r in L["runs"]:
        if not r.get("rid"): continue
        m = load(r["rid"])
        if m is None: continue
        m["_rid"] = r["rid"]; m["_msgs"] = msgs(r["rid"]); m["_thinking"] = thinking(r["rid"]); m["_task"] = json.dumps(r["task"], sort_keys=True)
        rows[r["seq"]][r["arm"]] = m
    pairs = []
    for s, d in sorted(rows.items()):
        g = d.get("gateway"); b = d.get("direct-ts")
        bad = lambda x: (not x) or x.get("is_error") or not x.get("total_cost_usd")
        if bad(g) or bad(b): continue
        pairs.append((s, b, g))
    def summ(ps):
        if not ps: return None
        lr = [(b["_task"], math.log(g["total_cost_usd"] / b["total_cost_usd"])) for s, b, g in ps]
        mean = sum(x for _, x in lr) / len(lr); lo, hi = boot(lr)
        mb = sum(b["total_cost_usd"] for s, b, g in ps) / len(ps); mg = sum(g["total_cost_usd"] for s, b, g in ps) / len(ps)
        api = sum((len(g["_msgs"]) or g.get("api_requests") or g.get("num_turns") or 0) for s, b, g in ps) / len(ps)
        return dict(n=len(ps), saving_pct=-pct(mean), ci_pct=(None if lo is None else (-pct(hi), -pct(lo))),
                    cheaper=sum(1 for _, x in lr if x < 0), base_cost=round(mb, 4), gw_cost=round(mg, 4), net=round(mb - mg - FEE * api, 4))
    out = dict(model=L["model"], guard_before=L.get("guard_before"), guard_after=L.get("guard_after"),
               valid=bool(L.get("guard_after")) and L["guard_after"].get("used_paused") == L["guard_before"].get("used_paused"),
               cold=summ([p for p in pairs if p[0] == 1]), warm=summ([p for p in pairs if p[0] > 1]), all=summ(pairs),
               errors=sum(1 for r in L["runs"] if r.get("conclusion") not in (None, "success")))
    qb = [quality(b) for _, b, g in pairs]; qg = [quality(g) for _, b, g in pairs]
    out["quality"] = dict(key=qb[0][0] if qb else None, base=[q[1] for q in qb], gw=[q[1] for q in qg])
    out["mix_base"] = mix([b for _, b, g in pairs]); out["mix_gw"] = mix([g for _, b, g in pairs])
    out["gw_cost_split_pct"] = split([g for _, b, g in pairs])
    out["rids"] = {f"s{r['seq']}-{r['arm']}": r.get("rid") for r in L["runs"]}
    res[name] = out
json.dump(res, open(f"{sys.argv[2]}/../results.json", "w"), indent=1)
print(json.dumps(res, indent=1))
