# Judge file r2-nushell-0.116.0

## PUBLISHED RELEASE NOTES (written by the maintainers)

This is the 0.116.0 release of Nushell. You can learn more about this release here: https://www.nushell.sh/blog/2026-09-26-nushell_v0_116_0.html

For convenience, we are providing full builds for Windows, Linux, and macOS. Be sure you have the requirements to enable all capabilities: https://www.nushell.sh/book/installation.html#dependencies

This release was made possible by PR contributions from @app/dependabot, @aron-intframe, @ayax79, @bobisageek, @catlover-bot, @costajohnt, @cptpiepmatz, @cuishuang, @Developer1010x, @Dheebz, @dilr, @Dorumin, @fdncred, @fly1d, @hexbinoct, @hustcer, @i-api, @Jorge-Polanco-Roque, @KaiSforza, @kronberger-droid, @LouisDeconinck, @luangucun, @magnify035, @maxim-uvarov, @mikehasa, @mkatychev, @Mrfiregem, @mrhard9090, @neveroNiwe, @nos1dot618, @pheenty, @philocalyst, @pickx, @ronisbr, @rvhelden, @sebaschi, @sidsri14, @surma, @user93390, @windlandneko, @zozo123

## COMMIT SUBJECTS between the previous tag and the release

Bump patch version after release (#18885)
chore(reedline): bump reedline to 73b928a (#18890)
chore(reedline): bump reedline fc19b91 (#18892)
named parameters can pass null or omit parameter entirely for easier shadowing (#18796)
reduce ast dependency for ir calls - phase 1 (#18813)
perf - stop parse-time-loading modules and extra cwd walks while typing `use std/` (#18841)
fix `lines --skip-empty` for string and byte stream input (#18872)
fix unmatched `{` at end of `format pattern` and `parse` patterns (#18871)
Upgrade to polars 0.55.2 (#18866)
fix: infer string from `semver | into string`. (#18901)
Allow float value strings with commas in `into float` (#18882)
Allow raw `null`  as a value for `to yaml --non-roundtrip` (#18851)
roundup of 2 fixes for "did you mean?" (#18728)
Polars date range (#18887)
fix(format date): render locales whose format carries %E or %O (#18918)
build(deps): bump uuid from 1.24.0 to 1.25.0 (#18906)
build(deps): bump taiki-e/install-action from 2.85.11 to 2.86.6 (#18904)
fix(format date): resolve `%r` when the locale's am/pm fallback also carries `%O` (#18924)
docs(tutor): add reedline shortcuts tutorial and document $env (#18903)
docs(tutor): add custom commands and pipeline input tutorials (#18927)
docs(nuon): add a specification of the NUON format (#18925)
Remove most `fs` helpers from `nu-test-support` (#18910)
fix(tests): fix completions by resolving ".." in `WORKSPACE_ROOT` path (#18941)
fix(yaml): do not parse embedded float tokens (#18897)
update proc_macro_error to 3 and other dependencies (#18945)
update fff-searh to 0.10.6 (#18946)
Propagate `local-socket` feature into `nu-plugin-test-support` (#18947)
when config changes invalidate cache (#18950)
Update doc_config.nu
build(deps): bump crate-ci/typos from 1.48.0 to 1.50.0 (#18954)
build(deps): bump hustcer/milestone-action from 3.1 to 3.2 (#18955)
build(deps): bump ureq from 3.3.0 to 3.4.0 (#18957)
chore(ls): update default color mappings (#18937)
MCP: set default bind host to 127.0.0.1 (#18952)
fix parsing performance regression (#18948)
let more commands use row conditions (#18844)
Document behavior of `each` for more types of inputs. (#18893)
fix: strip ANSI from redirected CLI help (#18899)
fix `keybindings listen` - ignore KeyEventState when checking for Esc (#18867)
Add `completions.persistent_menus` config option (#18573)
fix(env): normalize PATH when refreshing ENV_CONVERSIONS (#18832)
Don't print a stray blank line when try with catch or finally collects an external (#18811)
fix improper cant convert error in path-relative-to (#18792)
each while: preserve errors instead of silently stopping (#18958)
bump reedline to a8e9364 (#18959)
Include UTC offset in `date list-timezone` output (#18922)
View source dependencies (#18801)
fix(parser): parse brace expressions in external calls (#18837)
ide: report file read failures from --ide-check (#18961)
bump rust toolchain to 1.96.1 (#18968)
docs(tutor): add conditional(if, match, where) tutorials (#18972)
update(style_computer.rs): fixed unessesary string allocations (#18975)
fix table truncating vs wrapping (#18979)
fix(nix): bump rust-overlay so the 1.96.1 toolchain resolves (#18985)
fix(nu-plugin): add socket feature flag to handle `--no-default-features` correctly (#18988)
chore: bump reedline 06bf606 (#18986)
build(deps): bump the uutils group with 8 updates (#18992)
Test Incredibuild self-hosted runner in CI (#18810)
feat(completions)!: unify completer inputs and output contracts (#18791)
build(deps): bump taiki-e/install-action from 2.86.6 to 2.87.7 (#18990)
build(deps): bump crate-ci/typos from 1.50.0 to 1.50.1 (#18991)
mkdir errors on already-created dir (#19006)
Replace `to yaml` `--compact-list-indent` with `--list-indent` (#19005)
fix: propagate error stream values in length, columns, and is-empty (#18976)
Revert "mkdir errors on already-created dir" (#19008)
Support escaped spaces inside double quotes (#19010)
Fix par-each deadlock when chaining same-size thread pools (#18999)
chore: bump reedline to 436f17b (#19013)
fix nested table after wrapping/truncating changes (#19007)
fix: use stack config for commandline completions (#19012)
fix(mkdir): don't report an existing directory as created in --verbose (#19017)
docs(mkdir): the --verbose example showed output that never occurs (#19023)
fix(view source): put a space after the colon on a rest parameter (#19024)
update rustls & friends (#19026)
feat(hash): add `sha512` subcommand (#19027)
build(deps): bump actions-rust-lang/setup-rust-toolchain from 1.17.0 to 2.0.0 (#19029)
build(deps): bump dirs from 6.0.0 to 7.0.0 (#19030)
build(deps): bump tabled from 0.21.0 to 0.22.0 (#19031)
Merge commit from fork
build(deps): bump taiki-e/install-action from 2.87.7 to 2.87.12 (#19028)
feat(mkdir): add --fail-if-exists flag to error on existing directory (#19021)
engine: IR-shaped const evaluation for run_const (AST migration phase 2) (#18967)
Add structured context support to std/log (#18971)
update some deps (#19034)
build(deps): bump tango-bench from 0.7.2 to 0.8.0 (#18907)
error make: Allow no text value (#19037)
scripts/nix: Update the flake lock (#19038)
bump uu_* crates to 0.12.0 (#19040)
fix(query web): parse headerless tables row by row (#19041)
chore(reedline): bump reedline to e0f1c0b (#19042)
fix(reedline): forward Menu::settings through SourcedMenu (#19043)
fix(ci): run `ready_for_review` CI on the PR head, not on `main` (#19047)
perf(startup): make $nu.startup-time accurate and speed up config loading, plugin registry, and gstat (#19049)
the tui family of commands (#19025)
fix(table): don't panic when the terminal is too narrow to draw (#19045)
perf(parser): reduce parse time by 30% - 50% (#19055)
feat(save): create parent directories with `--force` (#19039)
Don't go to tmp if --directory (#18996)
fix(engine): run every finally on the way out of nested try blocks, and unwind break/continue through them (#19052)
bump fff-search to 0.11.0 (#19057)
Merge commit from fork
fix(default): accept cell paths for column arguments (#19058)
fix(flatten): keep nested fields that collide with top-level columns (#19059)
feat(update cells): add --recursive flag to visit nested leaf values (#19060)
build(deps): bump aws-config from 1.10.0 to 1.12.0 (#18994)
fix(std/dt): correct `datetime-diff` day count when borrowing a month (#19064)
Add a `nu-dap` crate and `nu --dap`: a Debug Adapter Protocol server for Nushell (#18738)
fix(parser): reject unexpected semicolons in list literals and patterns (#19063)
build(deps): bump crate-ci/typos from 1.50.1 to 1.50.2 (#19069)
build(deps): bump rstest from 0.26.1 to 0.27.0 (#19070)
feat(reedline): bump to db34d84 (#19077)
fix(rm): skip `.` and `..` glob matches on Windows (#19065)
fix(table): keep markdown and restructured headers off the separator (#19066)
fix(rm): answer one `--interactive` prompt per key press on Windows (#19067)
build(deps): bump taiki-e/install-action from 2.87.12 to 2.87.17 (#19068)
build(deps): bump serde-saphyr from 1.2.0 to 1.3.0 (#19071)
fix(idx search): don't cap matches at 200 per file (#19078)
fix lsp hover tooltip markdown (#19080)
fixes for unified/completions in general (#19054)
Fix nushell command docs build error (#19084)
fix(config): keep XDG config when there is no home directory (#19083)
`char`: add forward slash/backslash. (#19082)
fix(completions): expand alias heads in `place.command`, keep completer warnings off the menu (#19085)
Bump minor version (#19090)

# CANDIDATE A

# Nushell 0.116.0

This release adds a debugger (`nu --dap`), a family of `tui` commands for building terminal UIs, and a reworked completion system. It also includes security fixes, many bug fixes and speedups.

## Breaking changes

### Custom completers use new named inputs ([#18791](https://github.com/nushell/nushell/pull/18791))

Parameter completers, `@complete` completers, external completers and menu `source` closures now all receive the same named inputs: `token`, `place` and `buffer`. Declare the ones you need as positional parameters, in any order.

| Old form | New form |
| :--- | :--- |
| `def comp [input pos] {...}` | `def comp [token: record] {...}` |
| `def comp [spans] {...}` | `def comp [buffer: string] {...}` |
| `{ \|spans\| ... }` (external completer) | `{ \|buffer: string\| ... }` |
| `{ \|buffer position\| ... }` (menu source) | `{ \|token: record\| ... }`, `{ \|place: record\| ... }` or `{ \|buffer: string\| ... }` |

- The new `@interactive` attribute marks completers that need the terminal, such as `fzf` or `input list`.
- The experimental `background-completions` option is removed. Use `@interactive` instead.
- The old `positional` input is deprecated.
- Unrecognized parameter names receive `null` and log a diagnostic.

### `to yaml --compact-list-indent` is replaced by `--list-indent` ([#19005](https://github.com/nushell/nushell/pull/19005))

`--list-indent` takes `compact` (the default) or `indented`. The same applies to `to yml`.

### Parser is stricter about semicolons ([#19063](https://github.com/nushell/nushell/pull/19063))

Unexpected semicolons in list literals and patterns are now parse errors.

### MCP server binds to `127.0.0.1` by default ([#18952](https://github.com/nushell/nushell/pull/18952))

The MCP server no longer listens on all interfaces unless you ask it to.

### `ls` default colors changed ([#18937](https://github.com/nushell/nushell/pull/18937))

The default color mappings used by `ls` were updated.

## Security

- Relative or otherwise invalid vendor autoload paths are now rejected, and rejected directories are logged. ([GHSA fix, merge commit 9364bd38d](https://github.com/nushell/nushell/commit/9364bd38d))
- Plugin local sockets are now isolated from other users. ([merge commit 8daac3a29](https://github.com/nushell/nushell/commit/8daac3a29))

## New features

### Debugger

- `nu --dap` starts a Debug Adapter Protocol server so editors like VS Code, Zed and Neovim can debug `.nu` scripts. It supports breakpoints, stepping and variable inspection. ([#18738](https://github.com/nushell/nushell/pull/18738))

### `tui` commands

- A new family of `tui` commands builds interactive terminal UIs and dialogs from composable widgets, such as `ls | tui table | tui run`. ([#19025](https://github.com/nushell/nushell/pull/19025))
- Widgets include `tui label`, `table`, `tree`, `textbox`, `select`, `menu`, `button`, `search`, `preview`, `progress`, `log`, `split`, `box` and `tab`. `tui bind` attaches key handlers, and `tui debug` inspects a UI.

### Commands and flags

- `hash sha512` computes SHA-512 hashes. ([#19027](https://github.com/nushell/nushell/pull/19027))
- `mkdir --fail-if-exists` errors when the directory already exists. ([#19021](https://github.com/nushell/nushell/pull/19021))
- `save --force` creates missing parent directories. ([#19039](https://github.com/nushell/nushell/pull/19039))
- `update cells --recursive` visits nested leaf values. ([#19060](https://github.com/nushell/nushell/pull/19060))
- `char` adds names for forward slash and backslash. ([#19082](https://github.com/nushell/nushell/pull/19082))
- `date list-timezone` now includes the UTC offset. ([#18922](https://github.com/nushell/nushell/pull/18922))
- `take until`, `take while`, `skip until`, `skip while` and `chunk-by` accept row conditions as well as closures. ([#18844](https://github.com/nushell/nushell/pull/18844))
- `error make` allows omitting the text value. ([#19037](https://github.com/nushell/nushell/pull/19037))
- `into float` accepts strings with commas. ([#18882](https://github.com/nushell/nushell/pull/18882))
- `to yaml --non-roundtrip` accepts raw `null`. ([#18851](https://github.com/nushell/nushell/pull/18851))
- `view source` now shows dependencies. ([#18801](https://github.com/nushell/nushell/pull/18801))
- Polars: a date range command was added and Polars was upgraded to 0.55.2. ([#18887](https://github.com/nushell/nushell/pull/18887), [#18866](https://github.com/nushell/nushell/pull/18866))
- `std/log` commands take `--context` to attach structured fields to log lines. ([#18971](https://github.com/nushell/nushell/pull/18971))
- `tutor` has new lessons on conditionals, custom commands, pipeline input, reedline shortcuts and `$env`. ([#18972](https://github.com/nushell/nushell/pull/18972), [#18927](https://github.com/nushell/nushell/pull/18927), [#18903](https://github.com/nushell/nushell/pull/18903))

### Language and shell

- A named flag passed `null` is now treated as omitted where the flag takes a value. This makes it easier to wrap built-ins like `cp --preserve`. ([#18796](https://github.com/nushell/nushell/pull/18796))
- Escaped spaces now work inside double-quoted strings. ([#19010](https://github.com/nushell/nushell/pull/19010))
- `$env.config.completions.persistent_menus` keeps completion and history menus open while you edit. It defaults to `false`. ([#18573](https://github.com/nushell/nushell/pull/18573))

## Fixes

### Language and engine

- Every `finally` block now runs when leaving nested `try` blocks, and `break`/`continue` unwind through them. ([#19052](https://github.com/nushell/nushell/pull/19052))
- `try` with `catch` or `finally` no longer prints a stray blank line when collecting an external command. ([#18811](https://github.com/nushell/nushell/pull/18811))
- Brace expressions in external command arguments now parse correctly. ([#18837](https://github.com/nushell/nushell/pull/18837))
- `par-each` no longer deadlocks when chained with the same thread-pool size. ([#18999](https://github.com/nushell/nushell/pull/18999))
- `PATH` is normalized when `ENV_CONVERSIONS` refreshes. ([#18832](https://github.com/nushell/nushell/pull/18832))
- A parsing performance regression is fixed. ([#18948](https://github.com/nushell/nushell/pull/18948))
- `semver | into string` is now inferred as a string. ([#18901](https://github.com/nushell/nushell/pull/18901))
- "Did you mean?" suggestions are more accurate. ([#18728](https://github.com/nushell/nushell/pull/18728))
- Unmatched `{` at the end of `format pattern` and `parse` patterns is handled. ([#18871](https://github.com/nushell/nushell/pull/18871))
- Config changes now correctly invalidate cached state. ([#18950](https://github.com/nushell/nushell/pull/18950))
- The XDG config directory is kept when there is no home directory. ([#19083](https://github.com/nushell/nushell/pull/19083))
- `nu --directory` no longer goes to the temp directory first. ([#18996](https://github.com/nushell/nushell/pull/18996))

### Commands

- `each while` keeps errors instead of silently stopping. ([#18958](https://github.com/nushell/nushell/pull/18958))
- `length`, `columns` and `is-empty` pass through errors from error streams. ([#18976](https://github.com/nushell/nushell/pull/18976))
- `default` accepts cell paths for column arguments. ([#19058](https://github.com/nushell/nushell/pull/19058))
- `flatten` keeps nested fields whose names match top-level columns. ([#19059](https://github.com/nushell/nushell/pull/19059))
- `lines --skip-empty` works for string and byte streams. ([#18872](https://github.com/nushell/nushell/pull/18872))
- `path relative-to` gives a proper error instead of a wrong conversion error. ([#18792](https://github.com/nushell/nushell/pull/18792))
- `mkdir --verbose` no longer reports an existing directory as created. ([#19017](https://github.com/nushell/nushell/pull/19017))
- `rm` skips `.` and `..` glob matches on Windows and handles one `--interactive` prompt per key press. ([#19065](https://github.com/nushell/nushell/pull/19065), [#19067](https://github.com/nushell/nushell/pull/19067))
- `query web` parses headerless tables row by row. ([#19041](https://github.com/nushell/nushell/pull/19041))
- `format date` handles locales whose formats include `%E`, `%O` or `%r`. ([#18918](https://github.com/nushell/nushell/pull/18918), [#18924](https://github.com/nushell/nushell/pull/18924))
- `view source` puts a space after the colon on rest parameters. ([#19024](https://github.com/nushell/nushell/pull/19024))
- `from yaml` no longer parses embedded float tokens as numbers. ([#18897](https://github.com/nushell/nushell/pull/18897))
- `std/dt` `datetime-diff` gives the right day count when borrowing a month. ([#19064](https://github.com/nushell/nushell/pull/19064))
- `idx search` no longer caps matches at 200 per file. ([#19078](https://github.com/nushell/nushell/pull/19078))
- Redirected CLI help no longer contains ANSI codes. ([#18899](https://github.com/nushell/nushell/pull/18899))

### Tables

- Tables no longer panic when the terminal is too narrow. ([#19045](https://github.com/nushell/nushell/pull/19045))
- Truncating versus wrapping and nested tables render correctly. ([#18979](https://github.com/nushell/nushell/pull/18979), [#19007](https://github.com/nushell/nushell/pull/19007))
- Markdown and restructured table headers stay off the separator line. ([#19066](https://github.com/nushell/nushell/pull/19066))

### Completions, editor and tooling

- Command-line completions use the stack config. ([#19012](https://github.com/nushell/nushell/pull/19012))
- Alias heads are expanded in `place.command`, and completer warnings stay out of the menu. ([#19085](https://github.com/nushell/nushell/pull/19085))
- Various general completion fixes. ([#19054](https://github.com/nushell/nushell/pull/19054))
- `keybindings listen` ignores key event state when checking for Esc. ([#18867](https://github.com/nushell/nushell/pull/18867))
- Menu settings are forwarded through sourced menus. ([#19043](https://github.com/nushell/nushell/pull/19043))
- LSP hover tooltips render markdown correctly. ([#19080](https://github.com/nushell/nushell/pull/19080))
- `--ide-check` reports file read failures. ([#18961](https://github.com/nushell/nushell/pull/18961))
- `nu-plugin` builds with `--no-default-features`. ([#18988](https://github.com/nushell/nushell/pull/18988), [#18947](https://github.com/nushell/nushell/pull/18947))

## Performance

- Parsing is 30–50% faster. ([#19055](https://github.com/nushell/nushell/pull/19055))
- `$nu.startup-time` is now accurate, and config loading, the plugin registry and `gstat` start faster. ([#19049](https://github.com/nushell/nushell/pull/19049))
- Typing `use std/` no longer loads modules at parse time or does extra directory walks. ([#18841](https://github.com/nushell/nushell/pull/18841))

## Other

- Documentation: `each` input types, the NUON specification, `mkdir` examples and the command docs build. ([#18893](https://github.com/nushell/nushell/pull/18893), [#18925](https://github.com/nushell/nushell/pull/18925), [#19023](https://github.com/nushell/nushell/pull/19023), [#19084](https://github.com/nushell/nushell/pull/19084))
- Internal engine work: IR-based const evaluation and fewer AST dependencies in calls. ([#18967](https://github.com/nushell/nushell/pull/18967), [#18813](https://github.com/nushell/nushell/pull/18813))
- Reedline was bumped several times, and the Rust toolchain moved to 1.96.1. ([#19077](https://github.com/nushell/nushell/pull/19077), [#18968](https://github.com/nushell/nushell/pull/18968))
- Dependency updates, including uutils 0.12.0, rustls, tabled, dirs, fff-search, serde-saphyr and rstest. ([#19040](https://github.com/nushell/nushell/pull/19040), [#19026](https://github.com/nushell/nushell/pull/19026), [#19031](https://github.com/nushell/nushell/pull/19031), [#19030](https://github.com/nushell/nushell/pull/19030), [#19057](https://github.com/nushell/nushell/pull/19057), [#19071](https://github.com/nushell/nushell/pull/19071), [#19070](https://github.com/nushell/nushell/pull/19070))
- CI, Nix flake and test-support cleanups, plus other routine maintenance. ([#19047](https://github.com/nushell/nushell/pull/19047), [#19038](https://github.com/nushell/nushell/pull/19038), [#18910](https://github.com/nushell/nushell/pull/18910), [#18810](https://github.com/nushell/nushell/pull/18810))
- Version bump to 0.116.0. ([#19090](https://github.com/nushell/nushell/pull/19090))


# CANDIDATE B

# Nushell 0.116.0

This release adds a debugger server, a new family of `tui` commands, a unified completer interface, and a long list of fixes. It also includes breaking changes to custom completers and `to yaml`.

## Breaking changes

- Custom completers now receive named inputs (`token`, `place`, `buffer`) instead of the old per-completer arguments. This covers parameter completers, `@complete` completers, external completers and menu `source` closures. ([#18791](https://github.com/nushell/nushell/pull/18791))
- Completers that need the terminal, such as fzf or `input list`, must now be marked with the new `@interactive` attribute. ([#18791](https://github.com/nushell/nushell/pull/18791))
- `to yaml --compact-list-indent` is replaced by `--list-indent`, which takes `compact` (the default) or `indented`. ([#19005](https://github.com/nushell/nushell/pull/19005))
- `ls` default colors have changed. ([#18937](https://github.com/nushell/nushell/pull/18937))
- The MCP server now binds to `127.0.0.1` by default. ([#18952](https://github.com/nushell/nushell/pull/18952))
- Relative entries in the XDG data and config directory lists are now ignored, and vendor autoload paths must be absolute. ([#19057](https://github.com/nushell/nushell/pull/19057) range of security fixes; see Security)
- A named parameter passed as `--flag=$null` in a custom command that forwards flags is now treated as if the flag were omitted. ([#18796](https://github.com/nushell/nushell/pull/18796))
- `date list-timezone` output now includes each zone's UTC offset. ([#18922](https://github.com/nushell/nushell/pull/18922))

## Security

- Relative vendor autoload directories and relative XDG directory entries are rejected instead of being resolved against the current directory. Resolved autoload paths are validated.
- Plugin local-socket communication has stronger validation.

## Highlights

### Debug Adapter Protocol server

`nu --dap` starts a Debug Adapter Protocol server, so editors such as VS Code, Zed and Neovim can debug `.nu` scripts. It supports breakpoints, conditional breakpoints, logpoints, stepping and variable inspection. It sits behind the new default-on `dap` feature. ([#18738](https://github.com/nushell/nushell/pull/18738))

### `tui` commands

A new `tui` command family lets you compose widgets and dialogs (`tui label`, `tui table`, `tui split`, `tui run` and more) into terminal UIs. ([#19025](https://github.com/nushell/nushell/pull/19025))

```nushell
ls | tui label --title "files" | tui table | tui run
```

### Completions

- All completers now share one input and output contract. ([#18791](https://github.com/nushell/nushell/pull/18791))
- New `completions.persistent_menus` option keeps a menu open when you erase the characters you typed to filter it. ([#18573](https://github.com/nushell/nushell/pull/18573))
- Completions use the current stack's config. ([#19012](https://github.com/nushell/nushell/pull/19012))
- Alias heads are expanded in `place.command`, and completer warnings no longer show up in the menu. ([#19085](https://github.com/nushell/nushell/pull/19085))
- Several general fixes to unified completions. ([#19054](https://github.com/nushell/nushell/pull/19054))
- "Did you mean?" suggestions got two fixes. ([#18728](https://github.com/nushell/nushell/pull/18728))

## New features and improvements

### Commands

- `view source --dependencies` also shows the custom commands and constants the item uses. ([#18801](https://github.com/nushell/nushell/pull/18801))
- `update cells --recursive` visits nested leaf values. ([#19060](https://github.com/nushell/nushell/pull/19060))
- `save --force` creates missing parent directories. ([#19039](https://github.com/nushell/nushell/pull/19039))
- `mkdir --fail-if-exists` errors when the directory already exists. ([#19021](https://github.com/nushell/nushell/pull/19021))
- `hash sha512` is new. ([#19027](https://github.com/nushell/nushell/pull/19027))
- `char` gains forward slash and backslash names. ([#19082](https://github.com/nushell/nushell/pull/19082))
- `take until`, `take while`, `skip until`, `skip while` and `chunk-by` accept row conditions. ([#18844](https://github.com/nushell/nushell/pull/18844))
- `default` accepts cell paths for column arguments. ([#19058](https://github.com/nushell/nushell/pull/19058))
- `error make` allows a missing `text` value. ([#19037](https://github.com/nushell/nushell/pull/19037))
- `into float` accepts strings with comma separators. ([#18882](https://github.com/nushell/nushell/pull/18882))
- `to yaml --non-roundtrip` accepts a raw `null`. ([#18851](https://github.com/nushell/nushell/pull/18851))
- `polars date-range` is new or improved. ([#18887](https://github.com/nushell/nushell/pull/18887))
- `std/log` supports structured context. ([#18971](https://github.com/nushell/nushell/pull/18971))
- `each` documentation now covers more input types. ([#18893](https://github.com/nushell/nushell/pull/18893))

### Language and parser

- Named parameters can be passed `null` or omitted, which makes shadowing builtins easier. ([#18796](https://github.com/nushell/nushell/pull/18796))
- Double-quoted strings accept `\ ` (an escaped space), as pasted by terminals when you drag in files. ([#19010](https://github.com/nushell/nushell/pull/19010))
- Brace expressions such as closures and records work in external command arguments. ([#18837](https://github.com/nushell/nushell/pull/18837))
- Unexpected semicolons in list literals and patterns are now parse errors. ([#19063](https://github.com/nushell/nushell/pull/19063))
- Parsing is 30–50% faster. ([#19055](https://github.com/nushell/nushell/pull/19055))
- A parsing performance regression was fixed. ([#18948](https://github.com/nushell/nushell/pull/18948))
- Typing `use std/` no longer loads modules at parse time. ([#18841](https://github.com/nushell/nushell/pull/18841))

### Shell and config

- `$nu.startup-time` is accurate, and config loading, the plugin registry and `gstat` start faster. ([#19049](https://github.com/nushell/nushell/pull/19049))
- Config changes invalidate the cache. ([#18950](https://github.com/nushell/nushell/pull/18950))
- `nu --ide-check` reports file read failures. ([#18961](https://github.com/nushell/nushell/pull/18961))
- The XDG config is kept when there is no home directory. ([#19083](https://github.com/nushell/nushell/pull/19083))
- Reedline was updated several times. ([#19077](https://github.com/nushell/nushell/pull/19077), [#19043](https://github.com/nushell/nushell/pull/19043))
- `nu` with `--directory` no longer goes to the temp directory. ([#18996](https://github.com/nushell/nushell/pull/18996))

## Bug fixes

- Nested `try` blocks run every `finally` on the way out, and `break` and `continue` unwind through them correctly. ([#19052](https://github.com/nushell/nushell/pull/19052))
- `par-each` no longer deadlocks when chained with the same thread-pool size. ([#18999](https://github.com/nushell/nushell/pull/18999))
- `each while` keeps errors instead of silently stopping. ([#18958](https://github.com/nushell/nushell/pull/18958))
- `length`, `columns` and `is-empty` pass on error values from streams. ([#18976](https://github.com/nushell/nushell/pull/18976))
- `try` with `catch` or `finally` no longer prints a stray blank line after an external command. ([#18811](https://github.com/nushell/nushell/pull/18811))
- `flatten` keeps nested fields that collide with top-level columns. ([#19059](https://github.com/nushell/nushell/pull/19059))
- `lines --skip-empty` works for string and byte stream input. ([#18872](https://github.com/nushell/nushell/pull/18872))
- `format pattern` and `parse` handle an unmatched `{` at the end of a pattern. ([#18871](https://github.com/nushell/nushell/pull/18871))
- `query web` parses headerless tables row by row. ([#19041](https://github.com/nushell/nushell/pull/19041))
- `mkdir --verbose` no longer reports an existing directory as created. ([#19017](https://github.com/nushell/nushell/pull/19017))
- `rm` skips `.` and `..` glob matches on Windows. ([#19065](https://github.com/nushell/nushell/pull/19065))
- `rm --interactive` answers one prompt per key press on Windows. ([#19067](https://github.com/nushell/nushell/pull/19067))
- `format date` works with locales whose formats use `%E` or `%O`, and with `%r`. ([#18918](https://github.com/nushell/nushell/pull/18918), [#18924](https://github.com/nushell/nushell/pull/18924))
- `std/dt datetime-diff` gives the right day count when borrowing a month. ([#19064](https://github.com/nushell/nushell/pull/19064))
- `path relative-to` gives a proper error. ([#18792](https://github.com/nushell/nushell/pull/18792))
- Updating `ENV_CONVERSIONS` normalizes `PATH`. ([#18832](https://github.com/nushell/nushell/pull/18832))
- `semver | into string` infers a string type. ([#18901](https://github.com/nushell/nushell/pull/18901))
- YAML parsing no longer treats embedded float tokens as floats. ([#18897](https://github.com/nushell/nushell/pull/18897))
- `keybindings listen` ignores key event state when checking for Esc. ([#18867](https://github.com/nushell/nushell/pull/18867))
- Redirected CLI help has no ANSI codes. ([#18899](https://github.com/nushell/nushell/pull/18899))
- `view source` puts a space after the colon on a rest parameter. ([#19024](https://github.com/nushell/nushell/pull/19024))
- Table fixes: no panic when the terminal is too narrow ([#19045](https://github.com/nushell/nushell/pull/19045)), markdown and restructured headers stay off the separator ([#19066](https://github.com/nushell/nushell/pull/19066)), nested tables render correctly after the wrapping changes ([#19007](https://github.com/nushell/nushell/pull/19007)), and truncating versus wrapping is fixed ([#18979](https://github.com/nushell/nushell/pull/18979)).
- The LSP hover tooltip renders markdown correctly. ([#19080](https://github.com/nushell/nushell/pull/19080))
- `idx search` no longer caps matches at 200 per file. ([#19078](https://github.com/nushell/nushell/pull/19078))
- `nu-plugin` builds with `--no-default-features`. ([#18988](https://github.com/nushell/nushell/pull/18988), [#18947](https://github.com/nushell/nushell/pull/18947))

## Other

- Dependency updates, including polars 0.55.2, rustls, the uutils crates 0.12.0, tabled, dirs, serde-saphyr, rstest, ureq, aws-config and fff-search. ([#18866](https://github.com/nushell/nushell/pull/18866), [#19040](https://github.com/nushell/nushell/pull/19040), [#19026](https://github.com/nushell/nushell/pull/19026))
- Rust toolchain moved to 1.96.1, with Nix flake updates. ([#18968](https://github.com/nushell/nushell/pull/18968), [#19038](https://github.com/nushell/nushell/pull/19038))
- Internal engine refactors moving calls and const evaluation off the AST. ([#18813](https://github.com/nushell/nushell/pull/18813), [#18967](https://github.com/nushell/nushell/pull/18967))
- New tutor lessons on conditionals, custom commands, pipeline input and reedline shortcuts. ([#18972](https://github.com/nushell/nushell/pull/18972), [#18927](https://github.com/nushell/nushell/pull/18927), [#18903](https://github.com/nushell/nushell/pull/18903))
- Added a NUON format specification and other docs fixes. ([#18925](https://github.com/nushell/nushell/pull/18925), [#19084](https://github.com/nushell/nushell/pull/19084), [#19023](https://github.com/nushell/nushell/pull/19023))
- CI, GitHub Actions and test-support cleanups. ([#18810](https://github.com/nushell/nushell/pull/18810), [#19047](https://github.com/nushell/nushell/pull/19047), [#18910](https://github.com/nushell/nushell/pull/18910), [#18941](https://github.com/nushell/nushell/pull/18941))
- Minor allocation cleanup in the style computer. ([#18975](https://github.com/nushell/nushell/pull/18975))

