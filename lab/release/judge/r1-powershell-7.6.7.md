# Judge file r1-powershell-7.6.7

## PUBLISHED RELEASE NOTES (written by the maintainers)

﻿## [7.6.7]

### Engine Updates and Fixes

- Tolerate IO/JSON errors reading the per-user `powershell.config.json` (#28084)

### General Cmdlet Updates and Fixes

- Prevent localization of WPF key gesture strings (#28097)
- Allow user to force the default implicit formatting to use `AutoSize` (#28096)
- Handle MSIX installation specially when prepending to PATH (#28091)
- Add `GetImportModuleCommand` method and session restriction check in `Show-Command` (#28088)

### Tests

- Fix the PATH test for MSIX installed PowerShell (#28108)
- Fix `LocProject.json` tests and trigger CIs on changes to `LocProject.json` (#28104)
- Mark DSC Profile tests pending on MSIX test runs (#28092)

### Build and Packaging Improvements

<details>

<summary>

<p>Update to .NET SDK 10.0.402</p>

</summary>

<ul>
<li>Move to the latest <code>Microsoft.PowerShell.Native</code> package and add test (#28176)</li>
<li>Update <code>Microsoft.PowerShell.Native</code> package version (#28171)</li>
<li>Bump CodeQL init and analyze actions to 4.38.2 (#28156)</li>
<li>Add native Azure Linux 4 RPM packaging (#28154)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2725870 (#28105)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2734773 (#28102)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2724482 (#28101)</li>
<li>Simplify Microsoft Store listing metadata (#28103)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2716742 (#28100)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2730146 (#28099)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2726204 (#28098)</li>
<li>Add PDP.xml to the <code>LocProject.json</code> file (#28095)</li>
<li>Add Azure Linux 4 RPM support (#28039)</li>
<li>Revert &quot;Simplify Microsoft Store listing metadata&quot; (#28094)</li>
<li>Simplify Microsoft Store listing metadata (#28079)</li>
<li>Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2704971 (#28080)</li>
<li>Change Windows CI to stop using PowerShell 5.1 (#28081)</li>
<li>Support macOS signatures in nonofficial pipelines (#28076)</li>
<li>Bump github/codeql-action from 4.35.4 to 4.36.0 (#28083)</li>
<li>Bump actions/checkout from 6.0.2 to 7.0.1 (#28153)</li>
<li>Bump ossf/scorecard-action from 2.4.3 to 2.4.4 (#28157)</li>
<li>Bump actions/github-script from 8.0.0 to 9.0.0 (#28086)</li>
<li>Bump actions/upload-artifact from 7.0.0 to 7.0.1 (#28085)</li>
<li>Bump PowerShell/compliance/.github/workflows/ready-to-merge.yml from 1.0.0 to 1.0.1 (#28155)</li>
<li>Bump github/codeql-action/upload-sarif from 4.36.0 to 4.38.2 (#28158)</li>
<li>Bump actions/setup-dotnet from 5.2.0 to 6.0.0 (#28161)</li>
</ul>

</details>

[7.6.7]: https://github.com/PowerShell/PowerShell/compare/v7.6.6...v7.6.7


### SHA256 Hashes of the release artifacts

- hashes.sha256
  - 6C2D5F481CC20C83DF45D5C29E15F0D7E9E1DB82EB5B8F7F2FE33B107F308325
- powershell-7.6.7-1.azl4.aarch64.rpm
  - 2512824937A805EC83218BE2AE46DA45BAF780C279189B69259B7F8EDB1933A2
- powershell-7.6.7-1.azl4.x86_64.rpm
  - 47196B02BCD967EDD62F72BDADAEB922FDBF150A36E5AB722D4FBA488FB12E54
- powershell-7.6.7-1.cm.aarch64.rpm
  - 3204C62767010131797E95BC0220178CEC9B7E4B38A1ABD7CE3AB5B47D4EC154
- powershell-7.6.7-1.cm.x86_64.rpm
  - EF69FDE88F71DC37081553BF87CB96ED971A41C7DEFE266609F77BB64DDBE8F4
- powershell-7.6.7-1.rh.x86_64.rpm
  - 3C506D68EF70C47AC874BEA0985F4E3E9401B7591D0E2778501F4C5AA50A3518
- powershell-7.6.7-linux-arm32.tar.gz
  - 6C056A2104273C834DA2E383960FFA850520F3E760BADA5AF43F7CE8A64146D2
- powershell-7.6.7-linux-arm64.tar.gz
  - BA465EFDFB0984C1C5DC5ED9EB0B79A7E91A1B52C45F99377058C0659B84D3F1
- powershell-7.6.7-linux-musl-x64.tar.gz
  - D74A1B7E1D1FBF150AE6F29E083953CE07FC833FE9D66218D54940A8638249C6
- powershell-7.6.7-linux-x64-fxdependent.tar.gz
  - 0C87E8E10898FB42694E4DCEA1EE2B9420607836B6B8502C895D942E91CC34BD
- powershell-7.6.7-linux-x64-musl-noopt-fxdependent.tar.gz
  - 034931E34232DF4854C7769299BA60618ABBBEF1C6B5D1F6378F38160FFC22F7
- powershell-7.6.7-linux-x64.tar.gz
  - 6896F9E3A6B0A354BF470835A96DA76D2F801CD50DCF047AD7C4563BF93BF431
- powershell-7.6.7-osx-arm64.pkg
  - A627EF1649521449CAB796EC798DE3048CE89021C51F6F65B8B63D032165F1F5
- powershell-7.6.7-osx-arm64.tar.gz
  - 50DDE99BB066ADACBB9A748182D09EB9BEFF25119DC3B12E85C84B6B6B1C5DA9
- powershell-7.6.7-osx-x64.pkg
  - B5173081D521040ADD595D5C99FBDDA4135BA96BE82F49D340AA82B1227C319E
- powershell-7.6.7-osx-x64.tar.gz
  - C354CA845CB81F9239BC0C6FBFD14256056400E4B269BD7A6373D113AD94C1E3
- PowerShell-7.6.7-win-arm64.msi
  - DDB2F3613A0AD27817B90601A0827F7347E81DFA5BCE18D4BE8009B8CB0E0A31
- PowerShell-7.6.7-win-arm64.zip
  - 119BD9221254EF3637523CB1990797618F5FD68848B57DE40F12B561D743149E
- PowerShell-7.6.7-win-fxdependent.zip
  - 6B50AF1679D9A46D0C629B04BEC5508BC95B51AED253FD6DA576025CE0AFCF8C
- PowerShell-7.6.7-win-fxdependentWinDesktop.zip
  - 87EDAD652ADB342F3811C96815697F4FA0AA599DA436B5B731DCE3E8F8780821
- PowerShell-7.6.7-win-x64.msi
  - EC575CEF9EC56FCD905DE0D5EEAC9CB7F81A0A65ABB87BB5CD0E87FDFE2B8CC0
- PowerShell-7.6.7-win-x64.zip
  - D2F952EBDBF24386CB8923553AA58E41A846DB35A6155EA04C58142A4B16DBB7
- PowerShell-7.6.7-win-x86.msi
  - E0A5296FE368B2DC1B4FEF1217979A32CFED8A26F3586FB09FCEE9A72873691B
- PowerShell-7.6.7-win-x86.zip
  - 5D7594BE11DD0CE7177E5121D5DB643B7183170209A489FF4840B3284313CD73
- PowerShell-7.6.7.msixbundle
  - 4DDA8F77324028D2FC043A120CDDB9EA32465A96A31D48F6062DF2445FE12829
- powershell-lts-7.6.7-1.azl4.aarch64.rpm
  - 4790ADBFEA91AAE4D5EEBB26AFABB8C0CB7E45DDA40A7B62FFCDC9264D1A65EC
- powershell-lts-7.6.7-1.azl4.x86_64.rpm
  - 6E571ED4E05359FD3A1ABC029F2EDABF9F59E18D1D0496E13019A7F8FE3C7F4B
- powershell-lts-7.6.7-1.cm.aarch64.rpm
  - 11B0D3592BD824A888BA77265294597C75BB097835F6D96935942FEDCF5329D7
- powershell-lts-7.6.7-1.cm.x86_64.rpm
  - AF66FDD4EE0CA9FE2CF2CE3D4E5DBB97109CFA8457AD8EFD68266B2FEBEE12BD
- powershell-lts-7.6.7-1.rh.x86_64.rpm
  - 8636F860DA0C7D003E2BB8408FB0570E6AFEC032E989E0A1BA2BF8D8CE0E9EE1
- powershell-lts-7.6.7-osx-arm64.pkg
  - 64735FF201B9B1243BDF04C246C14FB4B5DC21D95FBA0D388E149A3633D186EE
- powershell-lts-7.6.7-osx-x64.pkg
  - AD40D1DA0B9B17688F4D37A23557D1838CA3C6BDC2E8C82202F9D712EFBC3310
- PowerShell-LTS-7.6.7.msixbundle
  - 7F2D6518B8EA93A6971A01D5912F388271FFB528836407748A17AA7988B5E538
- powershell-lts_7.6.7-1.deb_amd64.deb
  - A8E673EF7CC9A10B7AA5070C4C74B2DC5B868F6B3826690145B393CBF98834BB
- powershell-lts_7.6.7-1.deb_arm64.deb
  - 8E19050C8D8C4BBB4E1F43F26CEE9E5E5A72E829E1C77B95C5ED1A44ECAE8DAE
- powershell_7.6.7-1.deb_amd64.deb
  - 868C575F0822B2DEED054C1C3C464A9D4B841F67E153369147FB6ACE3545C8B2
- powershell_7.6.7-1.deb_arm64.deb
  - 120D3245F1985525A60A8225D80F65771D361A795D33E155A446AA8A6E30D3C4



## COMMIT SUBJECTS between the previous tag and the release

[release/v7.6.7] Support macOS signatures in nonofficial pipelines (#28076)
[release/v7.6.7] Change Windows CI to stop using PowerShell 5.1 (#28081)
[release/v7.6.7] Bump actions/setup-dotnet from 5.2.0 to 5.3.0 (#28082)
[release/v7.6.7] Bump github/codeql-action from 4.35.4 to 4.36.0 (#28083)
[release/v7.6.7] Tolerate IO/JSON errors reading the per-user `powershell.config.json` (#28084)
[release/v7.6.7] Bump actions/upload-artifact from 7.0.0 to 7.0.1 (#28085)
[release/v7.6.7] Add GetImportModuleCommand method and session restriction check in ShowCommand (#28088)
[release/v7.6.7] Bump actions/github-script from 8.0.0 to 9.0.0 (#28086)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2704971 (#28080)
[release/v7.6.7] Simplify Microsoft Store listing metadata (#28079)
[release/v7.6.7] Revert "[release/v7.6.7] Simplify Microsoft Store listing metadata" (#28094)
[release/v7.6.7] Add Azure Linux 4 RPM support (#28039)
[release/v7.6.7] Handle MSIX installation specially when prepend to PATH (#28091)
[release/v7.6.7] Allow user to force the default implicit formatting to use `AutoSize` (#28096)
[release/v7.6.7] Add PDP.xml to the `LocProject.json` file (#28095)
[release/v7.6.7] Prevent localization of WPF key gesture strings (#28097)
[release/v7.6.7] Mark DSC Profile tests pending on MSIX test runs (#28092)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2726204 (#28098)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2730146 (#28099)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2716742 (#28100)
[release/v7.6.7] Simplify Microsoft Store listing metadata (#28103)
[release/v7.6.7] Fix `LocProject.json` tests and trigger CIs on changes to `LocProject.json` (#28104)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2724482 (#28101)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2734773 (#28102)
[release/v7.6.7] Localized file check-in by OneLocBuild Task: Build definition ID 13420: Build ID 2725870 (#28105)
[release/v7.6.7] Fix the PATH test for MSIX installed PowerShell (#28108)
[release/v7.6.7] Bump actions/checkout from 6.0.2 to 7.0.1 (#28153)
[release/v7.6.7] Add native Azure Linux 4 RPM packaging (#28154)
[release/v7.6.7] Bump PowerShell/compliance/.github/workflows/ready-to-merge.yml from 1.0.0 to 1.0.1 (#28155)
[release/v7.6.7] Bump ossf/scorecard-action from 2.4.3 to 2.4.4 (#28157)
[release/v7.6.7] Bump github/codeql-action/upload-sarif from 4.36.0 to 4.38.2 (#28158)
[release/v7.6.7] Bump CodeQL init and analyze actions to 4.38.2 (#28156)
[release/v7.6.7] Bump actions/setup-dotnet from 5.3.0 to 6.0.0 (#28161)
[release/v7.6.7] Update Microsoft.PowerShell.Native package version (#28171)
[release/v7.6.7] Move to the latest `Microsoft.PowerShell.Native` package and add test (#28176)
Merged PR 41980: Fix the shadowing command bypass via alias for Import/Export-PSSession (#175)
Merged PR 41974: Add additional language mode checks to `PSSetMemberBinder` (#202)
Merged PR 41977: Throw in ForEach method if setting property in CLM (#170)
Merged PR 41968: Remove Wildcard GUID in HyperVSocketServer V2 Constructor (#165)
Merged PR 41965: Improve error handling for cab extraction and limit module name to 128 charac...
Merged PR 41971: Disable fetch delegate on $ref feature so external references are not allowed...
Merged PR 41991: [release/v7.6.7] Update branch for release
[release/v7.6.7] Update 7.6 changelog for v7.6.7 (#28178)
Merge commit 'ddf8a9b3b9b6b8a7485480e18aa2fcba2501e624'

# CANDIDATE A

# PowerShell v7.6.7 Release Notes

This release includes several security hardening changes, a new `Test-Json` parameter that changes how schema references work, and a few fixes and improvements for everyday use.

## Breaking Changes

- `Test-Json` no longer fetches external schema references (`$ref` to a URL or file) by default. Add the new `-FetchExternalReference` switch to turn this back on.
  - When a schema has a reference that can't be resolved, `Test-Json` now writes an `UnresolvedJsonSchemaRef` error that points you to the new switch.
  - Schemas with internal references keep working as before.

## New Features

- Add `$PSStyle.AutoSizeDefaultFormatting`, which makes the default implicit formatting use `AutoSize` for tables and wide lists when set to `$true` (#28096)
- Add `-FetchExternalReference` to `Test-Json` so you can opt in to retrieving external schema references.

## Security Hardening

- Constrained Language Mode now blocks setting properties on non-core types through instance members (including `PSObject` members) and through the `ForEach()` method.
- Fix `Import-PSSession` and `Export-PSSession` so a server-skipped or prefixed command can no longer shadow a local command through an alias.
- Make `Show-Command` refuse to run in restricted remote sessions, including when it imports modules.
- Bind the Hyper-V socket server used by PowerShell Direct (version 2) to a specific VM ID, instead of a wildcard ID.
- Harden `Update-Help` against bad help cabinet files:
  - Cabinet entries with empty paths or paths that resolve to the help folder itself are rejected.
  - File open and close failures during extraction are now reported instead of crashing or leaving a truncated file.
  - Multi-cabinet help content is rejected.
  - Module names longer than 128 characters are rejected with a `ModuleNameTooLong` error.

## Fixes

- PowerShell now starts when the per-user `powershell.config.json` can't be read or contains invalid JSON. It prints a warning and uses defaults instead of failing (#28084)
  - The system-wide config file is still strict and fails if it can't be read.
- Fix the `PATH` that PowerShell sets for child `pwsh` processes when installed from the Microsoft Store (MSIX). It now uses the stable app execution alias folder, which doesn't change on every update (#28091)
- Fix `AutoSize` not being applied to formats other than table and wide (#28096)
- Prevent the WPF key gesture strings used by `Show-Command` and `Out-GridView` from being localized (#28097)
- Update the `Microsoft.PowerShell.Native` package to 700.0.2 (#28171, #28176)

## Packaging

- Add Azure Linux 4 RPM packaging (#28039, #28154)

## Other

- CI and workflow updates:
  - Move Windows CI off Windows PowerShell 5.1 (#28081)
  - Bump GitHub Actions: `actions/checkout`, `actions/setup-dotnet`, `actions/upload-artifact`, `actions/github-script`, CodeQL, `ossf/scorecard-action` and the compliance workflow (#28082, #28083, #28085, #28086, #28153, #28155, #28156, #28157, #28158, #28161)
- Support macOS code signatures in non-official pipelines (#28076)
- Update Microsoft Store listing metadata and add localized store descriptions (#28079, #28094, #28095, #28103)
- Fix `LocProject.json` tests and trigger CI on `LocProject.json` changes (#28104)
- Check in localized files (#28080, #28098, #28099, #28100, #28101, #28102, #28105)
- Test updates: mark DSC profile tests pending on MSIX runs, fix the MSIX `PATH` test, and add tests for the changes above (#28092, #28108)
- Update the 7.6 changelog and release branch for v7.6.7 (#28178)


# CANDIDATE B

# PowerShell v7.6.7 Release Notes

## Breaking Changes

- `Test-Json` no longer fetches external `$ref` schema references by default. Use the new `-FetchExternalReference` switch to allow it. References inside the same schema still resolve without it. Blocked references now report the error ID `UnresolvedJsonSchemaRef`.
- `Import-PSSession` and `Export-PSSession` now check the command an alias resolves to, not just the alias name. Aliases that point to blocked or unsafe commands are no longer imported unless you pass `-Prefix`. If you rely on importing such aliases, you may now need `-AllowClobber`.

## Security Fixes

- Fixed a way to bypass the command skip list and shadowing checks in `Import-PSSession` and `Export-PSSession` by using an alias.
- Added more language mode checks when setting properties, so Constrained Language mode now blocks setting script properties and alias properties.
- The `ForEach()` method now throws when it is used to set a property in Constrained Language mode.
- `Show-Command` is now blocked in restricted remote sessions.
- Hardened updatable help CAB extraction against failures and malformed entries. It now rejects empty or root-resolving paths and multi-cabinet archives, and it handles close and open errors safely.
- Module names longer than 128 characters are now rejected by updatable help.
- The Hyper-V socket server for PowerShell Direct (V2 constructor) now listens on the correct partition ID instead of a wildcard GUID.

## New Features

- Added `$PSStyle.AutoSizeDefaultFormatting`. When it is `$true`, default output formatting uses `AutoSize` for table and wide views, like `Format-Table -AutoSize`. This gives more compact output in small terminals. List and complex views are still streamed. [#28096](https://github.com/PowerShell/PowerShell/pull/28096)
- Added Azure Linux 4 RPM packages. [#28039](https://github.com/PowerShell/PowerShell/pull/28039), [#28154](https://github.com/PowerShell/PowerShell/pull/28154)

## Bug Fixes

- PowerShell now starts with defaults and a warning if your per-user `powershell.config.json` can't be read or is invalid, instead of failing at startup. Machine-wide configuration still fails closed. [#28084](https://github.com/PowerShell/PowerShell/pull/28084)
- When PowerShell is installed from MSIX, it now puts a stable execution-alias path at the front of `PATH`. The versioned install folder changed on every update and broke tools such as CMake that cached the path. [#28091](https://github.com/PowerShell/PowerShell/pull/28091)
- Calling `pwsh` from inside `pwsh` now uses the running `pwsh` executable's folder, including when it was installed as a .NET tool. [#28091](https://github.com/PowerShell/PowerShell/pull/28091)
- WPF key gesture strings in `Show-Command` are no longer localized. [#28097](https://github.com/PowerShell/PowerShell/pull/28097)
- Updated to `Microsoft.PowerShell.Native` 700.0.2. [#28171](https://github.com/PowerShell/PowerShell/pull/28171), [#28176](https://github.com/PowerShell/PowerShell/pull/28176)

## Other

- Updated the .NET SDK to 10.0.402.
- Bumped GitHub Actions and security scanning actions: `actions/checkout`, `actions/setup-dotnet`, `actions/upload-artifact`, `actions/github-script`, CodeQL, `ossf/scorecard-action` and the compliance workflow. [#28153](https://github.com/PowerShell/PowerShell/pull/28153), [#28161](https://github.com/PowerShell/PowerShell/pull/28161), [#28085](https://github.com/PowerShell/PowerShell/pull/28085), [#28086](https://github.com/PowerShell/PowerShell/pull/28086), [#28156](https://github.com/PowerShell/PowerShell/pull/28156), [#28158](https://github.com/PowerShell/PowerShell/pull/28158), [#28083](https://github.com/PowerShell/PowerShell/pull/28083), [#28157](https://github.com/PowerShell/PowerShell/pull/28157), [#28155](https://github.com/PowerShell/PowerShell/pull/28155), [#28082](https://github.com/PowerShell/PowerShell/pull/28082)
- Updated the Microsoft Store listing metadata and added localized PDP files. [#28079](https://github.com/PowerShell/PowerShell/pull/28079), [#28103](https://github.com/PowerShell/PowerShell/pull/28103), [#28095](https://github.com/PowerShell/PowerShell/pull/28095)
- Updated localized resource files and fixed the `LocProject.json` tests. [#28104](https://github.com/PowerShell/PowerShell/pull/28104)
- Changed Windows CI to stop using Windows PowerShell 5.1. [#28081](https://github.com/PowerShell/PowerShell/pull/28081)
- Added macOS signature support in non-official pipelines. [#28076](https://github.com/PowerShell/PowerShell/pull/28076)
- Fixed the PATH test for MSIX installs and marked DSC profile tests pending on MSIX runs. [#28108](https://github.com/PowerShell/PowerShell/pull/28108), [#28092](https://github.com/PowerShell/PowerShell/pull/28092)
- Updated the 7.6 changelog. [#28178](https://github.com/PowerShell/PowerShell/pull/28178)

