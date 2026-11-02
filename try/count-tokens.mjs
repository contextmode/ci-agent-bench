// Recount try/tokens.json. Needs ANTHROPIC_API_KEY in the environment. count_tokens is free and writes nothing to a cache.
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
const key = process.env.ANTHROPIC_API_KEY;
if (!key) throw new Error("set ANTHROPIC_API_KEY");
const dir = new URL("./jobs/", import.meta.url);
const clean = (r) => ({ model: r.model, system: r.system, tools: r.tools, messages: r.messages.map((m) => { const o = {}; for (const x in m) if (x !== "output_config") o[x] = m[x]; return o; }) });
async function count(body) {
  const res = await fetch("https://api.anthropic.com/v1/messages/count_tokens", { method: "POST", headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" }, body: JSON.stringify(body) });
  if (!res.ok) throw new Error(res.status + " " + await res.text());
  return (await res.json()).input_tokens;
}
const out = { model: "claude-sonnet-5-5", method: "POST /v1/messages/count_tokens on each recorded request body (output_config and stream removed, as the page sends it). tokens[i] = input tokens of request i. stable = tokens of the system and tools alone (the prefix every task shares).", tasks: {} };
for (const f of readdirSync(dir).sort()) {
  const j = JSON.parse(readFileSync(new URL(f, dir), "utf8"));
  const tokens = [];
  for (const r of j.requests) tokens.push(await count(clean(r)));
  const r0 = clean(j.requests[0]);
  const stable = await count({ model: r0.model, system: r0.system, tools: r0.tools, messages: [{ role: "user", content: "x" }] });
  out.tasks[f.replace(".json", "")] = { tokens, stable, out: j.out };
}
writeFileSync(new URL("./tokens.json", import.meta.url), JSON.stringify(out, null, 1) + "\n");
