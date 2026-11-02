# Judge file r2-neovim-0.12.6

## PUBLISHED RELEASE NOTES (written by the maintainers)

```
NVIM v0.12.6
Build type: Release
LuaJIT 2.1.1774638290
```

## Release notes

- [Changelog](https://github.com/neovim/neovim/commit/779c36969e31080503be2dfccbcc3f999e289606) (fixes + features)
- [News](./runtime/doc/news.txt) (`:help news` in Nvim)

## Install

### Windows

#### Zip

1. Download **nvim-win64.zip** (or **nvim-win-arm64.zip** for ARM)
2. Extract the zip
3. Run `nvim.exe` in your terminal

#### MSI

1. Download **nvim-win64.msi** (or **nvim-win-arm64.msi** for ARM)
2. Run the MSI
3. Run `nvim.exe` in your terminal

Note: On Windows "Server" you may need to [install `vcruntime*.dll`](https://neovim.io/doc/install/#windows).

### macOS (x86_64)

1. Download **nvim-macos-x86_64.tar.gz**
2. Run `xattr -c ./nvim-macos-x86_64.tar.gz` (to avoid "unknown developer" warning)
3. Extract: `tar xzvf nvim-macos-x86_64.tar.gz`
4. Run `./nvim-macos-x86_64/bin/nvim`

### macOS (arm64)

1. Download **nvim-macos-arm64.tar.gz**
2. Run `xattr -c ./nvim-macos-arm64.tar.gz` (to avoid "unknown developer" warning)
3. Extract: `tar xzvf nvim-macos-arm64.tar.gz`
4. Run `./nvim-macos-arm64/bin/nvim`

### Linux (x86_64)

If your system does not have the required glibc version, try the (unsupported) [builds for older glibc](https://github.com/neovim/neovim-releases).

#### AppImage

1. Download **nvim-linux-x86_64.appimage**
2. Run `chmod u+x nvim-linux-x86_64.appimage && ./nvim-linux-x86_64.appimage`
   - If your system does not have FUSE you can [extract the appimage](https://github.com/AppImage/AppImageKit/wiki/FUSE#type-2-appimage):
     ```bash
     ./nvim-linux-x86_64.appimage --appimage-extract
     ./squashfs-root/usr/bin/nvim
     ```

#### Tarball

1. Download **nvim-linux-x86_64.tar.gz**
2. Extract: `tar xzvf nvim-linux-x86_64.tar.gz`
3. Run `./nvim-linux-x86_64/bin/nvim`

### Linux (arm64)

#### AppImage

1. Download **nvim-linux-arm64.appimage**
2. Run `chmod u+x nvim-linux-arm64.appimage && ./nvim-linux-arm64.appimage`
   - If your system does not have FUSE you can [extract the appimage](https://github.com/AppImage/AppImageKit/wiki/FUSE#type-2-appimage):
     ```bash
     ./nvim-linux-arm64.appimage --appimage-extract
     ./squashfs-root/usr/bin/nvim
     ```

#### Tarball

1. Download **nvim-linux-arm64.tar.gz**
2. Extract: `tar xzvf nvim-linux-arm64.tar.gz`
3. Run `./nvim-linux-arm64/bin/nvim`

### Other

- Install by [package manager](https://github.com/neovim/neovim/blob/master/INSTALL.md#install-from-package)


## COMMIT SUBJECTS between the previous tag and the release

build: version bump
fix(terminal): truecolor SGR with colour space id #41491
fix(snippet): cancel session on <Esc> in Select mode #39238
fix(snippet): cancel session on ESC in insert-mode #41555
Merge pull request #41562 from nathanzeng/backport-41555-to-release-0.12
backport: feat(pos): mutable vim.Pos, vim.Range fields (#41579)
fix(health): guard against nil result from vim.system:wait()
fix(health): restore pynvim version lookup #41619
fix(statuscolumn): heap buffer overflow with sign/number column (#41640)
Merge pull request #41650 from zeertzjq/backport
backport: fix(fuzzy): fuzmatch_str_free() frees the wrong element (#41695)
ci(macos): skip brew upgrade
ci(macos): untap untrusted aws/tap on macOS
ci(release): bump deprecated runner image to macos-15
fix(msgpack): out-of-bounds read on a truncated string #41683
fix(menu): menu_get() cannot tell :noremenu from :menu <script> #41686
fix(treesitter): #has-parent? errors on a node with no parent
fix(treesitter): conceal_lines is not applied to injected trees
fix(tui): don't treat ESC preceding repeat/release as ALT (#41770)
vim-patch:9.2.1040: matchfuzzypos() can be improved (#41786)
fix(scrollbind): window jumps back and forth with tall virt_lines block
revert(scrollbind): revert #41519 due to regressions
vim-patch:8.2.1353: crash when drawing double-wide character in terminal window (#41858)
backport: fix(filetype): empty 'filetype' skips :setfiletype #41985
fix(terminal): some keys like S-Del not working (#42080)
backport: fix(mpack): wrong encoding of integers beyond the int32 range (#42143)
ci(windows): fix missing package failure (#42126)
Merge pull request #42159 from zeertzjq/backport
vim-patch:9.2.1162: Wrong cursor position with 'linebreak' and large 'tabstop' (#42202)
vim-patch:9.2.0495: [security]: runtime(netrw): code injection via NetrwBookHistSave() #42275
NVIM v0.12.6

# CANDIDATE A

## Neovim v0.12.6

This is a bug-fix and security release. Upgrading is recommended.

### Security

- Fix code injection in netrw via `NetrwBookHistSave()`. [#42275](https://github.com/neovim/neovim/pull/42275)
- Fix a heap buffer overflow with the sign/number column in `'statuscolumn'`. [#41640](https://github.com/neovim/neovim/pull/41640)
- Fix an out-of-bounds read when unpacking a truncated msgpack string. [#41683](https://github.com/neovim/neovim/pull/41683)
- Fix a crash when drawing a double-wide character in a terminal window (vim-patch:8.2.1353). [#41858](https://github.com/neovim/neovim/pull/41858)

### Features

- `vim.Pos` and `vim.Range` fields (such as `row`, `col`, `start_row`) can now be assigned. [#41579](https://github.com/neovim/neovim/pull/41579)

### Fixes

- Terminal: keys like `S-Del` now work in Terminal mode. [#42080](https://github.com/neovim/neovim/pull/42080)
- Terminal: truecolor SGR sequences with a colour space id are now handled. [#41491](https://github.com/neovim/neovim/pull/41491)
- TUI: an ESC before a key repeat/release event is no longer treated as Alt. [#41770](https://github.com/neovim/neovim/pull/41770)
- Filetype: an empty `'filetype'` no longer prevents `:setfiletype` from working. [#41985](https://github.com/neovim/neovim/pull/41985)
- Msgpack: integers beyond the int32 range are now encoded correctly. [#42143](https://github.com/neovim/neovim/pull/42143)
- Snippets: the session is now cancelled on `<Esc>` in Insert and Select mode. [#41555](https://github.com/neovim/neovim/pull/41555), [#39238](https://github.com/neovim/neovim/pull/39238)
- Treesitter: `conceal_lines` now applies to injected trees.
- Treesitter: `#has-parent?` no longer errors on a node with no parent.
- Menus: `menu_get()` now distinguishes `:noremenu` from `:menu <script>`. [#41686](https://github.com/neovim/neovim/pull/41686)
- Fuzzy matching: fix freeing the wrong element in `matchfuzzy()` results. [#41695](https://github.com/neovim/neovim/pull/41695)
- `matchfuzzypos()` is improved (vim-patch:9.2.1040). [#41786](https://github.com/neovim/neovim/pull/41786)
- Health: `:checkhealth` no longer fails on a nil `vim.system():wait()` result and again finds the pynvim version. [#41619](https://github.com/neovim/neovim/pull/41619)
- Fix wrong cursor position with `'linebreak'` and a large `'tabstop'` (vim-patch:9.2.1162). [#42202](https://github.com/neovim/neovim/pull/42202)

### Other

- CI/build: update macOS runner image, avoid untrusted brew tap and upgrades, and fix a Windows package failure. [#42126](https://github.com/neovim/neovim/pull/42126)
- Docs: document the `nvim.snippet` augroup and the updated `:setfiletype`/`did_filetype()` behavior.
- Tests added for the fixes above.
- A scrollbind fix for tall virtual-lines blocks was added and then reverted within this release; there is no net change. [#41519](https://github.com/neovim/neovim/pull/41519)


# CANDIDATE B

## Neovim v0.12.6

This is a bug-fix and security release on the 0.12 series. There are no breaking changes, deprecations or removals.

### Security

- Fix code injection in netrw through `NetrwBookHistSave()`. #42275
- Fix an out-of-bounds read when msgpack data contains a truncated string. #41683
- Fix a heap buffer overflow when drawing `'statuscolumn'` with a sign or number column. #41640

### Features

- `vim.Pos` and `vim.Range` fields can now be changed after creation. #41579

### Fixes

#### Editor and options

- `:setfiletype` now works when `'filetype'` is empty, and `did_filetype()` follows the same rule. #41985
- Fix the cursor position with `'linebreak'` and a large `'tabstop'`. #42202
- `matchfuzzypos()` is faster. #41786
- Fix a crash when `matchfuzzy()` frees the wrong item. #41695
- `menu_get()` can now tell `:noremenu` from `:menu <script>`. #41686

#### Terminal and TUI

- Keys such as `S-Del` now work in Terminal mode. #42080
- Fix a crash when drawing a double-wide character in a terminal window. #41858
- Truecolor escape sequences that include a colour space id are now handled. #41491
- The TUI no longer treats an Escape key press before a key repeat or release as Alt. #41770

#### Lua and runtime

- Snippet sessions are now cancelled when you press `<Esc>` in Insert mode or Select mode. #41555, #39238
- Fix `#has-parent?` in treesitter queries raising an error on a node with no parent.
- `conceal_lines` now applies to injected treesitter trees.
- `:checkhealth` no longer fails when `vim.system():wait()` returns nothing, and it shows the pynvim version again. #41619

#### API and RPC

- Fix wrong encoding of integers beyond the 32-bit range in `vim.mpack`. #42143

### Other

- CI: fix a missing package failure on Windows. #42126
- CI: update the macOS runner image, untap an untrusted Homebrew tap and skip `brew upgrade`.
- Update version metadata for the release.

