#!/usr/bin/env python3
"""Normalise one run into out/norm.json. Usage: norm.py KIND SRC OUT [extra k=v ...]
KIND claude: SRC is claude -p --output-format stream-json/json, or the action execution_file (a JSON list).
KIND proxy:  SRC is the usageproxy.py jsonl. Tokens are the provider's own usage, one record per API request.
Writes requests, tokens (input, cache_write, cache_read, output), tools {name: n}, client_cost (Claude: total_cost_usd). No regex."""
import collections, json, sys
kind, src, dst = sys.argv[1:4]
extra = dict(a.split("=", 1) for a in sys.argv[4:])
out = {"kind": kind, **extra}
tools = collections.Counter()
if kind == "claude":
    raw = open(src).read()
    try:
        d = json.loads(raw); d = d if isinstance(d, list) else [d]
    except ValueError:
        d = []
        for l in raw.splitlines():
            if l.strip().startswith("{"):
                try: d.append(json.loads(l))
                except ValueError: pass
    seen = {}; per = []
    for e in d:
        if isinstance(e, dict) and e.get("type") == "assistant":
            m = e.get("message") or {}; mid = m.get("id")
            names = [c.get("name") for c in (m.get("content") or []) if c.get("type") == "tool_use"]
            if mid in seen:
                per[seen[mid]]["tools"] += names; per[seen[mid]]["u"] = m.get("usage") or {}; continue
            seen[mid] = len(per); per.append({"u": m.get("usage") or {}, "tools": names})
    res = next((e for e in reversed(d) if isinstance(e, dict) and e.get("type") == "result"), {})
    u = res.get("usage") or {}
    for p in per:
        tools.update(p["tools"])
    out.update(requests=len(per), input=u.get("input_tokens", 0) or 0, cache_write=u.get("cache_creation_input_tokens", 0) or 0,
               cache_read=u.get("cache_read_input_tokens", 0) or 0, output=u.get("output_tokens", 0) or 0,
               client_cost=res.get("total_cost_usd"), is_error=res.get("is_error"), turns=res.get("num_turns"),
               result=(res.get("result") or ""))
else:
    rows = [json.loads(l) for l in open(src) if l.strip()] if __import__("os").path.exists(src) else []
    ok = [r for r in rows if r.get("status") == 200 and r.get("id")]
    for r in ok:
        tools.update(t for t in r["tools"] if t)
    out.update(requests=len(ok), failed_requests=len(rows) - len(ok),
               input=sum(r.get("input_tokens", 0) for r in ok), cache_write=sum(r.get("cache_creation_input_tokens", 0) for r in ok),
               cache_read=sum(r.get("cache_read_input_tokens", 0) for r in ok), output=sum(r.get("output_tokens", 0) for r in ok),
               client_cost=None)
out["tools"] = dict(tools)
json.dump(out, open(dst, "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "result"}))
