# cm-ci-lab

Public lab for one question: how much does a headless CI agent (Claude Code `claude -p`,
`anthropics/claude-code-action`) cost when it sends its model traffic through the Context Mode gateway,
compared with a direct run of the same job?

**Reproduce it yourself in one click:** see [reproduce/README.md](reproduce/README.md).

- Workflows: `.github/workflows/<area>.yml` (one per CI use-case), all `workflow_dispatch` only, so fork code never sees a secret.
- Task specs: `reproduce/tasks/<area>.json` (repos, issue or PR numbers, pinned commits).
- Results: `docs/ci-night-1101-r2.md`, raw table `lab/ci-night/results-r2.json`.

The base code is python-slugify (MIT, Val Neekman, upstream commit 35aca63f, see LICENSE), used by the early lab runs.
