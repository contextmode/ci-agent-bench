# Recorded jobs for the contextmode.ai/try page

These are the exact request bodies the page sends (one JSON file per task). Each was recorded from a real `claude -p` run. The page loads them from this repo at a pinned commit and checks the sha256 below.

Model: claude-sonnet-5-5. Claude Code: 2.1.316, installed with the native installer: `curl -fsSL https://claude.ai/install.sh | bash`.

Each task is one run. Task A pays the cold prefix; B and C read what A wrote. Only input tokens are billed: the page sets `max_tokens` to 1.

| file | upstream | prompt | requests | bytes | sha256 |
|---|---|---|---|---|---|
| [ci-fix--express.json](jobs/ci-fix--express.json) | [expressjs/express#7459](https://github.com/expressjs/express/pull/7459) | CI failed. Run `npm test`, find the root cause, fix it with the smallest change. | 6 | 336101 | `c35f431d24c9b4ab037b44d652c6abe6fdf4136f7c4d7f351d9bad197406f069` |
| [ci-fix--koa.json](jobs/ci-fix--koa.json) | [koajs/koa#2025](https://github.com/koajs/koa/pull/2025) | CI failed. Run `npm test`, find the root cause, fix it with the smallest change. | 6 | 331529 | `de2efb0c491ddaf2b83000596cc4a6cd6e9477acb2907271a1f9dca325a75a2b` |
| [ci-fix--requests.json](jobs/ci-fix--requests.json) | [psf/requests#7205](https://github.com/psf/requests/pull/7205) | CI failed. Run `python -m pytest tests -v -p no:cacheprovider`, find the root cause, fix it with the smallest  | 4 | 225711 | `ecbeaf231de677efe09849a424709b08132f0ebf050e1b41c351f5f78a90390b` |
| [mention-fix--fd.json](jobs/mention-fix--fd.json) | [sharkdp/fd#2192](https://github.com/sharkdp/fd/issues/2192) | You are Claude, an AI assistant designed to help with GitHub issues and pull requests. Think carefully as you  | 8 | 544954 | `a16bcf48b20a5f316b02538fe744b2ab161b16b98b0de3ccf3d33a7a01a533b4` |
| [mention-fix--gin.json](jobs/mention-fix--gin.json) | [gin-gonic/gin#4851](https://github.com/gin-gonic/gin/issues/4851) | You are Claude, an AI assistant designed to help with GitHub issues and pull requests. Think carefully as you  | 9 | 532897 | `425013252b82bf03e9982db275829241dfb8163064a1e410e3ac885d7095c628` |
| [mention-fix--loguru.json](jobs/mention-fix--loguru.json) | [Delgan/loguru#1501](https://github.com/Delgan/loguru/issues/1501) | You are Claude, an AI assistant designed to help with GitHub issues and pull requests. Think carefully as you  | 5 | 315767 | `45e24a92092cfeee5650f03da149f5d2f3974f162a3a895f33501bd9d85cd365` |
| [triage--godot-124950.json](jobs/triage--godot-124950.json) | [godotengine/godot#124950](https://github.com/godotengine/godot/issues/124950) | You're an issue triage assistant. Analyze the issue and manage labels. IMPORTANT: Don't post any comments or m | 2 | 98677 | `a6d5446eee4990b574924e3038c4a15025db52dc855f52875a476d81117852f2` |
| [triage--tauri-16340.json](jobs/triage--tauri-16340.json) | [tauri-apps/tauri#16340](https://github.com/tauri-apps/tauri/issues/16340) | You're an issue triage assistant. Analyze the issue and manage labels. IMPORTANT: Don't post any comments or m | 2 | 103140 | `094381c6f2c5b298524e23707f21dc23557d33d0014432770f949a25047388e1` |
| [triage--zed-66189.json](jobs/triage--zed-66189.json) | [zed-industries/zed#66189](https://github.com/zed-industries/zed/issues/66189) | You're an issue triage assistant. Analyze the issue and manage labels. IMPORTANT: Don't post any comments or m | 2 | 110146 | `47e2776c1b73fbb69e116d13f901d1803c3a7e799e3f0d32bbe1b55b1768bf26` |
