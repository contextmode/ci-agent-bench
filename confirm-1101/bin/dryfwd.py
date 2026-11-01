#!/usr/bin/env python3
# Dry-run recorder for the agent probes (no model call, nothing billed).
# Listens on 127.0.0.1:PORT. For each POST from the agent it saves the path, the header NAMES and values that are not
# secrets, and the body; then sends the same request to the gateway with `x-cm-dry-run: 1` added. The gateway answers
# with the body it WOULD forward upstream (base64 after "cm-dry-run:"), which is saved next to the original.
# The agent gets a 400 back, so it stops after request 1. Usage: dryfwd.py PORT OUTDIR GATEWAY_ROOT
# Prints no secret: values of authorization, x-api-key and x-cm-device-key are never written.
import base64, http.server, itertools, json, os, ssl, sys, urllib.request, urllib.error
PORT, OUT, GW = int(sys.argv[1]), sys.argv[2], sys.argv[3].rstrip("/")
SECRET = ("authorization", "x-api-key", "x-cm-device-key", "x-context-mode-key", "cookie")
os.makedirs(OUT, exist_ok=True)
n = itertools.count()
CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)

def decode(raw):
    txt = ""
    for ln in raw.splitlines():
        if not ln.startswith("data:"): continue
        try: e = json.loads(ln[5:].strip())
        except Exception: continue
        if e.get("type") == "cm_dry_run": txt += e.get("text", "")
        elif e.get("type") == "content_block_delta": txt += (e.get("delta") or {}).get("text", "")
        elif e.get("type") == "response.output_text.delta": txt += e.get("delta", "")   # Codex /v1/responses stream
    if not txt:
        try:
            j = json.loads(raw)
            for c in (j.get("content") or []): txt += c.get("text", "")
            for o in (j.get("output") or []):
                for c in (o.get("content") or []): txt += c.get("text", "")
        except Exception: pass
    if not txt.startswith("cm-dry-run:"): return None
    return json.loads(base64.b64decode(txt[len("cm-dry-run:"):]))

class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        b = self.rfile.read(int(self.headers.get("content-length", "0")))
        i = next(n)
        hdr = {k: (v if k.lower() not in SECRET else "<set>") for k, v in self.headers.items()}
        rec = {"path": self.path, "headers": hdr, "sent_bytes": len(b)}
        try: rec["body"] = json.loads(b or b"{}")
        except Exception: rec["body_raw_bytes"] = len(b)
        fwd = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "content-length", "accept-encoding", "connection")}
        fwd["x-cm-dry-run"] = "1"
        url = GW + self.path
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, data=b, headers=fwd, method="POST"), context=CTX, timeout=120)
            raw = r.read().decode(errors="replace"); rec["gw_status"] = r.status
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace"); rec["gw_status"] = e.code; rec["gw_error"] = raw[:600]
        p = decode(raw) if rec["gw_status"] == 200 else None
        if p is not None:
            body = p.get("body")
            rec["dry"] = {"tenant": p.get("tenant"), "url": p.get("url"),
                          "forwarded_header_names": sorted((p.get("headers") or {}).keys()),
                          "forwarded_bytes": len(json.dumps(body, separators=(",", ":"))) if body is not None else None}
            rec["forwarded_body"] = body
        json.dump(rec, open(f"{OUT}/{i:03d}.json", "w"), indent=1)
        e = json.dumps({"type": "error", "error": {"type": "invalid_request_error", "message": "dry probe stop"}}).encode()
        self.send_response(400); self.send_header("content-type", "application/json"); self.send_header("content-length", str(len(e)))
        self.end_headers(); self.wfile.write(e)
    def do_GET(self):
        self.send_response(404); self.end_headers()
    def log_message(self, *a): pass

http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
