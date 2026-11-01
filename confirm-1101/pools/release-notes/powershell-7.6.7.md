## [7.6.7]

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

