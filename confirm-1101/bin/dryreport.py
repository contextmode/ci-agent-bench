#!/usr/bin/env python3
# Summarises a dryfwd.py folder: per request, the header names the agent sent, the bytes it sent, the bytes the gateway
# would forward, the tenant, and whether the forwarded body differs from the sent body. Usage: dryreport.py DIR
import glob, json, sys
CI = ("x-cm-ci-repo", "x-cm-ci-run", "x-cm-ci-ref", "x-cm-device-key", "x-context-mode-banner", "x-cm-client")
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    r = json.load(open(f)); names = {k.lower() for k in r["headers"]}
    d = r.get("dry") or {}
    sent = json.dumps(r.get("body"), separators=(",", ":")) if "body" in r else None
    fb = r.get("forwarded_body")
    fwd = json.dumps(fb, separators=(",", ":")) if fb is not None else None
    print(json.dumps({"file": f.split("/")[-1], "path": r["path"], "ci_headers_sent": sorted(n for n in names if n in CI),
                      "gw_status": r.get("gw_status"), "gw_error": (r.get("gw_error") or "")[:200], "tenant": d.get("tenant"),
                      "sent_bytes": len(sent) if sent else r.get("sent_bytes"), "forwarded_bytes": len(fwd) if fwd else None,
                      "changed": (sent != fwd) if (sent and fwd) else None,
                      "upstream_url": d.get("url"),
                      "x_cm_headers_forwarded": [h for h in d.get("forwarded_header_names", []) if h.startswith("x-cm")]}))
