## Flint on Linux and Windows

[Flint](https://ollama.com/library/flint) now runs on Linux and Windows as well as macOS.

## Other improvements

- Streaming OpenAI Responses and Anthropic Messages requests now report generation failures instead of ending silently after partial output.
- `ollama launch` now passes cloud models' context lengths and capabilities to coding tools, fixing incorrect context and compaction settings.
- Anthropic-compatible web search now uses the model's supported thinking setting in follow-up requests, preventing avoidable failures.

**Full Changelog**: https://github.com/ollama/ollama/compare/v0.40.8...v0.40.9