# Judge file r2-ollama-0.40.9

## PUBLISHED RELEASE NOTES (written by the maintainers)

## Flint on Linux and Windows

[Flint](https://ollama.com/library/flint) now runs on Linux and Windows as well as macOS.

## Other improvements

- Streaming OpenAI Responses and Anthropic Messages requests now report generation failures instead of ending silently after partial output.
- `ollama launch` now passes cloud models' context lengths and capabilities to coding tools, fixing incorrect context and compaction settings.
- Anthropic-compatible web search now uses the model's supported thinking setting in follow-up requests, preventing avoidable failures.

**Full Changelog**: https://github.com/ollama/ollama/compare/v0.40.8...v0.40.9

## COMMIT SUBJECTS between the previous tag and the release

ci: switch to released WoA CTK (#19185)
llama.cpp update (#19194)
anthropic: surface errors after streaming starts (#19188)
mlx: add d3 decision model support (#19196)
build: update Go toolchain and dependencies (#19200)
launch: use cloud model context in Claude Code (#19119)
build: update jsonparser to v1.1.2 (#19220)
mlxrunner: add Phonon text-to-speech support (#19166)
flint: fix replies with thinking disabled (#19216)
anthropic: reuse resolved thinking for web search (#19098)
openai: preserve failures in Responses streams (#19225)
Make sure all launchers know about cloud model metadata (#19223)
Support GA Gradium Phonon checkpoints (#19227)

# CANDIDATE A

## What's Changed

### New features
- Added text-to-speech support with Phonon models through the MLX runner, including an OpenAI-compatible speech endpoint and CLI playback. ([#19166](https://github.com/ollama/ollama/pull/19166))
- Phonon now imports Gradium's GA checkpoints, with default-voice import and speech conditioning; the earlier prerelease checkpoint format is no longer accepted and needs version 0.40.9 or newer. ([#19227](https://github.com/ollama/ollama/pull/19227))
- Added support for the d3 decision model on MLX. ([#19196](https://github.com/ollama/ollama/pull/19196))

### Fixes and improvements
- `ollama launch` now knows cloud model metadata (context length, thinking levels and capabilities) for all launchers. ([#19223](https://github.com/ollama/ollama/pull/19223))
- Claude Code launches now use the cloud model's context length. ([#19119](https://github.com/ollama/ollama/pull/19119))
- Flint now answers directly when thinking is disabled. ([#19216](https://github.com/ollama/ollama/pull/19216))
- The OpenAI-compatible Responses API now reports failures that happen mid-stream. ([#19225](https://github.com/ollama/ollama/pull/19225))
- The Anthropic-compatible API now reports errors that occur after streaming has started. ([#19188](https://github.com/ollama/ollama/pull/19188))
- Anthropic-compatible web search now reuses the already-resolved thinking setting. ([#19098](https://github.com/ollama/ollama/pull/19098))

### Other
- Updated llama.cpp. ([#19194](https://github.com/ollama/ollama/pull/19194))
- Updated the Go toolchain and dependencies, and jsonparser to v1.1.2. ([#19200](https://github.com/ollama/ollama/pull/19200), [#19220](https://github.com/ollama/ollama/pull/19220))
- CI now uses the released CUDA Toolkit for Windows on Arm. ([#19185](https://github.com/ollama/ollama/pull/19185))
- Added speech docs and bench reporting of loaded VRAM for decision models. ([#19166](https://github.com/ollama/ollama/pull/19166), [#19196](https://github.com/ollama/ollama/pull/19196))


# CANDIDATE B

## What's Changed

### New
- Added text-to-speech with the Phonon model: `ollama run phonon "Hello"` plays audio through your speakers, or writes a WAV file when the output is redirected. [#19166](https://github.com/ollama/ollama/pull/19166)
- Added an OpenAI-compatible speech endpoint so apps can stream generated audio from Ollama. [#19166](https://github.com/ollama/ollama/pull/19166)
- Added support for the d3 decision model on the MLX runner (requires Ollama 0.40.9 or later). [#19196](https://github.com/ollama/ollama/pull/19196)

### Improved
- Phonon now uses Gradium's GA checkpoints, including the default voice, and older prerelease Phonon checkpoints are rejected. [#19227](https://github.com/ollama/ollama/pull/19227)
- `ollama launch` now knows each cloud model's context length, thinking levels and capabilities, for Codex, pi, OpenCode, Deepseek harness and others. [#19223](https://github.com/ollama/ollama/pull/19223)
- Claude Code now launches with the selected cloud model's context length instead of an unknown-model warning and a 200k fallback. [#19119](https://github.com/ollama/ollama/pull/19119)
- Updated llama.cpp. [#19194](https://github.com/ollama/ollama/pull/19194)

### Fixed
- Fixed `/v1/responses` streams that failed after starting ending silently; clients now get a `response.failed` event with partial output kept. [#19225](https://github.com/ollama/ollama/pull/19225)
- Fixed `/v1/messages` streams that failed after starting hiding the error; clients now receive an error event. [#19188](https://github.com/ollama/ollama/pull/19188)
- Fixed Anthropic-compatible web search failing on follow-up requests when thinking settings were unsupported by the model. [#19098](https://github.com/ollama/ollama/pull/19098)
- Fixed Flint answering with thinking when thinking is turned off. [#19216](https://github.com/ollama/ollama/pull/19216)

### Other
- Updated the Go toolchain and dependencies, including jsonparser to v1.1.2. [#19200](https://github.com/ollama/ollama/pull/19200), [#19220](https://github.com/ollama/ollama/pull/19220)
- Switched Windows on Arm CI to the released CUDA toolkit. [#19185](https://github.com/ollama/ollama/pull/19185)
- Added speech documentation and tests for the new features.

**Full Changelog**: https://github.com/ollama/ollama/compare/v0.40.8...v0.40.9

