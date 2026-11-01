# Recorded jobs for the contextmode.ai/try page

These are the exact request bodies the page sends (one JSON file per task). Each was recorded from a real `claude -p` run. The page loads them from this repo at a pinned commit and checks the sha256 below.

Model: claude-sonnet-5-5. Claude Code: 2.1.316, installed with the native installer: `curl -fsSL https://claude.ai/install.sh | bash`.

Each task is one run. Task A pays the cold prefix; B and C read what A wrote. Only input tokens are billed: the page sets `max_tokens` to 1.

| file | upstream | prompt | requests | bytes | sha256 |
|---|---|---|---|---|---|
| [ci-fix--express.json](jobs/ci-fix--express.json) | [expressjs/express#7459](https://github.com/expressjs/express/pull/7459) | CI failed. Run `npm test`, find the root cause, fix it with the smallest change. | 6 | 336119 | `6eb91d0694f4c5c496c3ee88b2010115618bd12ff9efb301c544ec41ab4ad372` |
| [ci-fix--koa.json](jobs/ci-fix--koa.json) | [koajs/koa#2025](https://github.com/koajs/koa/pull/2025) | CI failed. Run `npm test`, find the root cause, fix it with the smallest change. | 6 | 331547 | `23ea1e6d034995d5709ef9fcb5dd34bbd2a41c5cb2fd4add8f831fb404c0e2f0` |
| [ci-fix--requests.json](jobs/ci-fix--requests.json) | [psf/requests#7205](https://github.com/psf/requests/pull/7205) | CI failed. Run `python -m pytest tests -v -p no:cacheprovider`, find the root cause, fix it with the smallest  | 4 | 225723 | `c9fe1d30f6ca9b6b64a15a375a0379d2ac58a4bd2d3ba6af775dd0139b70831c` |
| [mention-fix--fd.json](jobs/mention-fix--fd.json) | [sharkdp/fd#2192](https://github.com/sharkdp/fd/issues/2192) | You are Claude, an AI assistant designed to help with GitHub issues and pull requests. Think carefully as you  | 8 | 544981 | `5d6d3b3dfb134c2b45be51f6ca86898de417f2641747848b2c5ae74fd62ccba8` |
| [mention-fix--gin.json](jobs/mention-fix--gin.json) | [gin-gonic/gin#4851](https://github.com/gin-gonic/gin/issues/4851) | You are Claude, an AI assistant designed to help with GitHub issues and pull requests. Think carefully as you  | 9 | 532924 | `0dda6552fe95c6c50b5af795a8c928fa2eb78e758cea088ba86c96387ba51e97` |
| [mention-fix--loguru.json](jobs/mention-fix--loguru.json) | [Delgan/loguru#1501](https://github.com/Delgan/loguru/issues/1501) | You are Claude, an AI assistant designed to help with GitHub issues and pull requests. Think carefully as you  | 5 | 315785 | `03a63c6ff36b33d3de61642b190cd2fffe6bb099ca38e16af9987143f94c61b7` |
| [triage--godot-124950.json](jobs/triage--godot-124950.json) | [godotengine/godot#124950](https://github.com/godotengine/godot/issues/124950) | You're an issue triage assistant. Analyze the issue and manage labels. IMPORTANT: Don't post any comments or m | 2 | 98683 | `e165acc687b56ed6ebf4adc4265d25c250e92ffb6f7d81078a634412457c423d` |
| [triage--tauri-16340.json](jobs/triage--tauri-16340.json) | [tauri-apps/tauri#16340](https://github.com/tauri-apps/tauri/issues/16340) | You're an issue triage assistant. Analyze the issue and manage labels. IMPORTANT: Don't post any comments or m | 2 | 103146 | `395d148422bbccc709a0356892bd1bda2d0dc9218bc1a9c1c4e3b169626ceb60` |
| [triage--zed-66189.json](jobs/triage--zed-66189.json) | [zed-industries/zed#66189](https://github.com/zed-industries/zed/issues/66189) | You're an issue triage assistant. Analyze the issue and manage labels. IMPORTANT: Don't post any comments or m | 2 | 110152 | `9d586fa76fedbd558324159c7378d8f11940b41960960e4e6cffa79696e1eda1` |
