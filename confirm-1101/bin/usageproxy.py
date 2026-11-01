#!/usr/bin/env python3
"""Recording pass-through proxy for the non-Claude agents (OpenCode, Pi, Codex). Both arms use it, so both are measured
the same way: the provider's own usage, read from the response stream. Usage: usageproxy.py PORT UPSTREAM OUT.jsonl
Forwards every request unchanged (headers and body) to UPSTREAM + path. Per response it writes one JSON line:
input, cache_write, cache_read, output tokens, tool-call names. Never writes a header value. No regex."""
import http.client, http.server, json, ssl, sys, threading, urllib.parse
PORT, UP, OUT = int(sys.argv[1]), sys.argv[2].rstrip("/"), sys.argv[3]
U = urllib.parse.urlparse(UP)
LOCK = threading.Lock()


def note(rec):
    with LOCK:
        open(OUT, "a").write(json.dumps(rec) + "\n")


def scan(ev, acc):
    t = ev.get("type")
    if t == "message_start":
        m = ev.get("message") or {}; u = m.get("usage") or {}
        acc["id"] = m.get("id")
        for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"):
            acc[k] = u.get(k, 0) or 0
    elif t == "message_delta":
        u = ev.get("usage") or {}
        for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"):
            if u.get(k) is not None:
                acc[k] = u[k]
    elif t == "content_block_start":
        b = ev.get("content_block") or {}
        if b.get("type") in ("tool_use", "server_tool_use"):
            acc["tools"].append(b.get("name"))
    elif t == "response.output_item.added":
        it = ev.get("item") or {}
        if it.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
            acc["tools"].append(it.get("name") or it.get("type"))
    elif t in ("response.completed", "response.incomplete"):
        r = ev.get("response") or {}; u = r.get("usage") or {}
        acc["id"] = r.get("id")
        cached = (u.get("input_tokens_details") or {}).get("cached_tokens", 0) or 0
        acc["input_tokens"] = (u.get("input_tokens", 0) or 0) - cached
        acc["cache_read_input_tokens"] = cached
        acc["output_tokens"] = u.get("output_tokens", 0) or 0
        acc["reasoning_tokens"] = (u.get("output_tokens_details") or {}).get("reasoning_tokens", 0) or 0


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_POST(self):
        n = int(self.headers.get("content-length", "0")); body = self.rfile.read(n)
        hdr = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "content-length", "accept-encoding", "connection")}
        hdr["Accept-Encoding"] = "identity"
        cls = http.client.HTTPSConnection if U.scheme == "https" else http.client.HTTPConnection
        conn = cls(U.netloc, timeout=600, **({"context": ssl.create_default_context()} if U.scheme == "https" else {}))
        conn.request("POST", (U.path.rstrip("/") + self.path), body=body, headers=hdr)
        r = conn.getresponse()
        self.send_response(r.status)
        for k, v in r.getheaders():
            if k.lower() not in ("transfer-encoding", "connection", "content-length", "content-encoding"):
                self.send_header(k, v)
        self.send_header("Connection", "close"); self.end_headers()
        acc = {"path": self.path, "status": r.status, "tools": [], "req_bytes": n}
        buf = b""; whole = b""
        while True:
            c = r.read1(65536) if hasattr(r, "read1") else r.read(65536)
            if not c:
                break
            self.wfile.write(c); self.wfile.flush()
            whole += c if len(whole) < 4_000_000 else b""
            buf += c
            while b"\n" in buf:
                ln, buf = buf.split(b"\n", 1)
                ln = ln.strip()
                if ln.startswith(b"data:"):
                    try: scan(json.loads(ln[5:].strip()), acc)
                    except ValueError: pass
        if r.status == 200 and "id" not in acc:  # non-stream JSON answer
            try:
                j = json.loads(whole); u = j.get("usage") or {}
                acc["id"] = j.get("id")
                for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"):
                    acc[k] = u.get(k, 0) or 0
                for b in j.get("content") or []:
                    if b.get("type") == "tool_use": acc["tools"].append(b.get("name"))
            except ValueError: pass
        if r.status != 200:
            acc["error"] = whole[:300].decode(errors="replace")
        note(acc); self.close_connection = True

    def log_message(self, *a): pass


http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
