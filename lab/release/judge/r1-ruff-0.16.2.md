# Judge file r1-ruff-0.16.2

## PUBLISHED RELEASE NOTES (written by the maintainers)

## Release Notes

Released on 2026-08-06.

### Bug fixes

- \[`flake8-pyi`\] Avoid false positives on `singledispatch` functions (`PYI041`) ([#27335](https://github.com/astral-sh/ruff/pull/27335))

### Server

- Register formatting capabilities dynamically to exclude TOML files ([#27332](https://github.com/astral-sh/ruff/pull/27332))

### Contributors

- [@MeGaGiGaGon](https://github.com/MeGaGiGaGon)
- [@charliermarsh](https://github.com/charliermarsh)
- [@epage](https://github.com/epage)
- [@sharkdp](https://github.com/sharkdp)
- [@ntBre](https://github.com/ntBre)

## Install ruff 0.16.2

### Install prebuilt binaries via shell script

```sh
curl --proto '=https' --tlsv1.2 -LsSf https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-installer.sh | sh
```

### Install prebuilt binaries via powershell script

```sh
powershell -ExecutionPolicy Bypass -c "irm https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-installer.ps1 | iex"
```

## Download ruff 0.16.2

|  File  | Platform | Checksum |
|--------|----------|----------|
| [ruff-aarch64-apple-darwin.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-apple-darwin.tar.gz) | Apple Silicon macOS | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-apple-darwin.tar.gz.sha256) |
| [ruff-x86_64-apple-darwin.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-apple-darwin.tar.gz) | Intel macOS | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-apple-darwin.tar.gz.sha256) |
| [ruff-aarch64-pc-windows-msvc.zip](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-pc-windows-msvc.zip) | ARM64 Windows | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-pc-windows-msvc.zip.sha256) |
| [ruff-i686-pc-windows-msvc.zip](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-i686-pc-windows-msvc.zip) | x86 Windows | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-i686-pc-windows-msvc.zip.sha256) |
| [ruff-x86_64-pc-windows-msvc.zip](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-pc-windows-msvc.zip) | x64 Windows | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-pc-windows-msvc.zip.sha256) |
| [ruff-aarch64-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-unknown-linux-gnu.tar.gz) | ARM64 Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-i686-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-i686-unknown-linux-gnu.tar.gz) | x86 Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-i686-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-powerpc64-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-powerpc64-unknown-linux-gnu.tar.gz) | PPC64 Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-powerpc64-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-powerpc64le-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-powerpc64le-unknown-linux-gnu.tar.gz) | PPC64LE Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-powerpc64le-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-riscv64gc-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-riscv64gc-unknown-linux-gnu.tar.gz) | RISCV Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-riscv64gc-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-s390x-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-s390x-unknown-linux-gnu.tar.gz) | S390x Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-s390x-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-x86_64-unknown-linux-gnu.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-unknown-linux-gnu.tar.gz) | x64 Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-unknown-linux-gnu.tar.gz.sha256) |
| [ruff-armv7-unknown-linux-gnueabihf.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-armv7-unknown-linux-gnueabihf.tar.gz) | ARMv7 Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-armv7-unknown-linux-gnueabihf.tar.gz.sha256) |
| [ruff-aarch64-unknown-linux-musl.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-unknown-linux-musl.tar.gz) | ARM64 MUSL Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-aarch64-unknown-linux-musl.tar.gz.sha256) |
| [ruff-i686-unknown-linux-musl.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-i686-unknown-linux-musl.tar.gz) | x86 MUSL Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-i686-unknown-linux-musl.tar.gz.sha256) |
| [ruff-x86_64-unknown-linux-musl.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-unknown-linux-musl.tar.gz) | x64 MUSL Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-x86_64-unknown-linux-musl.tar.gz.sha256) |
| [ruff-arm-unknown-linux-musleabihf.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-arm-unknown-linux-musleabihf.tar.gz) | ARMv6 MUSL Linux (Hardfloat) | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-arm-unknown-linux-musleabihf.tar.gz.sha256) |
| [ruff-armv7-unknown-linux-musleabihf.tar.gz](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-armv7-unknown-linux-musleabihf.tar.gz) | ARMv7 MUSL Linux | [checksum](https://releases.astral.sh/github/ruff/releases/download/0.16.2/ruff-armv7-unknown-linux-musleabihf.tar.gz.sha256) |

## Verifying GitHub Artifact Attestations

The artifacts in this release have attestations generated with GitHub Artifact Attestations. These can be verified by using the [GitHub CLI](https://cli.github.com/manual/gh_attestation_verify):
```sh
gh attestation verify <file-path of downloaded artifact> --repo astral-sh/ruff
```

You can also download the attestation from [GitHub](https://github.com/astral-sh/ruff/attestations) and verify against that directly:
```sh
gh attestation verify <file-path of downloaded artifact> --bundle <file-path of downloaded attestation>
```




## COMMIT SUBJECTS between the previous tag and the release

[ty] Precalculate supports in constraint sets (#27306)
[ty] Do not top-materialize (user) `TypeIs` return types (#26864)
[ty] Migrate legacy TypeVar diagnostics to inline snapshots (#27343)
[ty] Reuse static-class accessor for tuple checks (#27364)
[ty] Remove unused frozen-collection APIs (#27347)
[ty] Remove unused generic-context display settings (#27351)
[ty] Share symmetric narrowing-constraint branches (#27358)
[ty] Remove unused string-literal display settings (#27352)
[ty] Remove unused file-scoped place identifiers (#27354)
[ty] Simplify static class specialization dispatch (#27359)
[ty] Unify symmetric bounded TypeVar comparisons (#27357)
[ty] Consolidate functional enum mixin conversion (#27342)
[ty] Derive the corpus workspace root without spawning Cargo (#27345)
[ty] Unify break and continue flow handling (#27360)
[ty] Deduplicate module-resolver test-builder transitions (#27353)
[ty] Remove unused nonlocal symbol lookup (#27363)
[ty] Share dynamic class header-range reconstruction (#27356)
[ty] Remove bespoke inference VecMap iterator (#27362)
[ty] Merge duplicated VecSet implementation blocks (#27365)
[ty] Remove empty corpus known-failure machinery (#27344)
[ty] Reuse tuple length accessors for size hints (#27366)
[ty] Remove single-use current-assignment conversions (#27361)
[ty] Restore frozen-collection APIs (#27367)
[ty] Diagnose dataclass fields after inherited defaults (#27327)
[ty] Use legacy ParamSpec syntax in legacy wrapper test (#27348)
[ty] Index with-statement targets as symbols (#27256)
Register formatting capabilities dynamically to exclude TOML files (#27332)
[`flake8-pyi`] Avoid false positives on `singledispatch` functions (`PYI041`) (#27335)
[ty] Reject specializing non-generic subclasses (#27377)
[ty] Preserve TypeVarTuple context during Generic recovery (#27381)
[ty] Reject `ClassVar` and `Final` qualifiers in `NamedTuple` fields (#27380)
Narrow internal visibility with Hawk (#27339)
Remove unused APIs from ruff_ranged_value (#27391)
[ty] Remove unused APIs from ty_site_packages (#27399)
[ty] Remove unused APIs from ty_python_core (#27396)
Remove unused APIs from ruff_workspace (#27393)
Remove unused APIs from ruff_diagnostics (#27383)
Remove unused APIs from ruff_linter (#27385)
Remove unused APIs from ruff_python_stdlib (#27390)
[ty] Remove unused APIs from ty_server (#27398)
Remove unused APIs from ruff_db (#27382)
[ty] Remove unused APIs from ty_module_resolver (#27394)
[ty] Remove unused APIs from ty_project (#27395)
[ty] Sync vendored typeshed stubs (#27401)
[`ruff_python_ast`] Fix double visit / missing elif visit (#27404)
Restore symmetric public APIs (#27405)
Remove unused APIs from ruff_notebook (#27386)
Move formatter line terminators into test module (#27384)
Remove unused APIs from ruff_source_file (#27392)
Remove unused ClassMemberBoundness predicates (#27389)
[ty] Remove unused TypeVarVariance bounds (#27408)
[ty] Detect `__aenter__` and `__aexit__` that do not return awaitables (#27414)
[ty] Improve error context for incompatible callable signatures (#27422)
[ty] Prioritize readable mdtest organization in AGENTS.md (#27424)
[ty] Trigger signature help after completing callable with parentheses (#27084)
[ty] Revert "Remove bespoke inference VecMap iterator" (#27428)
Use `LinterSettings` builder methods in tests (#27418)
[ty] Make parsed modules Python-version aware (#26856)
[ty] Document inference behavior of unannotated parameters with default values (#24943)
[ty] Recognize Pydantic on extra search paths (#27429)
[ty] Move Unknown into ty_extensions._internal (#27430)
[ty] Reject out-of-scope ParamSpec components (#27378)
[ty] Hide stub-only helpers from implicit builtin lookup (#27423)
Add pywin32 to Ruff ecosystem checks (#27437)
[ty] Check property compatibility when matching class objects to protocols (#27402)
[ty] Make module resolution environment-aware (#27128)
[ty] Support different type inference settings in a single Salsa DB (#27152)
[ty] Move Python version source out of `Program` (#27434)
[ty] Preserve return constraints for object-variadic callables (#27431)
[ty] Preserve return constraints for top callables (#27446)
[ty] Bump ecosystem-analyzer to fix attrs and Bokeh (#27457)
[ty] Top-materialize `is_dataclass` type guard (#27455)
[ty] Reject unsupported `dataclass_transform` parameters (#27458)
[ty] Fix unused hints for OR-pattern captures (#27438)
[ty] Preserve generic class type variables in constructor inference (#27340)
[ty] Retain typing-only symbols in explicit completions (#27435)
[ty] Remove deprecated `src.root` setting in favor of `environment.root` (#27456)
[ty] Fix specialization cycle with deferred TypeVar defaults (#27453)
[ty] Extract constraint-set-related benchmarks into separate file (#27459)
[ty] Infer generic TypedDicts through synthesized constructor signatures (#27436)
[ty] Rename the Markdown code-span predicate used in docstring parsing (#27463)
[ty] Preserve class type parameters through generic decorators (#27442)
[ty] Recover generic constructor types from failing overloads (#27460)
[ty] Index match-pattern bindings as symbols (#27260)
[ty] Preserve called types in intersection diagnostics (#27475)
[ty] Validate constructor calls on unbounded type variables (#27449)
[ty] Fix constructor calls on narrowed type-variable intersections (#27493)
Update Rust crate camino to v1.2.5 (#27481)
Update Rust crate thin-vec to v0.2.19 (#27484)
Update taiki-e/install-action action to v2.85.3 (#27490)
Update CodSpeedHQ/action action to v4.19.1 (#27487)
Update Rust crate toml to v1.1.4 (#27485)
Update Rust crate toml_parser to v1.1.3 (#27486)
Update Rust crate jiff to v0.2.35 (#27482)
Update dependency astral-sh/uv to v0.12.1 (#27477)
Update dependency unidiff to v1 (#27491)
Update Rust crate schemars to v1.2.2 (#27483)
Update cargo-bins/cargo-binstall action to v1.21.1 (#27476)
Update prek dependencies (#27480)
Update dependency ruff to v0.16.1 (#27479)
Update dependency prek to v0.4.11 (#27478)
Update NPM Development dependencies (#27489)
Update docker/login-action action to v4.5.2 (#27488)
[ty] [playground] Make run panel scrollable and wrapping (#27474)
[ty] Update Salsa to 0.28.2 (#27496)
[ty] Select benchmark projects in memory reports (#27499)
[ty] Infer generic TypedDicts from unpacked TypedDicts (#27439)
[ty] Avoid exponential slowdown copying narrowed TypedDict unions (#27492)
[ty] Reject Self with incompatible explicit receiver annotations (#27454)
[ty] Install primer dependencies for memory reports (#27500)
[ty] Suppress `unimported-reveal` diagnostics in stub files and `if TYPE_CHECKING` blocks (#27508)
[ty] Clarify ecosystem summary diagnostic placement (#27511)
[ty] Normalize unpacked callable signatures for assignability (#27450)
test(annotate): Verify cell_index behavior
fix(annotate): Fix the suggestion anonymous logic
refactor(annotate): Pull out origin formatting
fix(annotate): Render cells for patches
refactor(annotate): Allow optional paths in Origin
fix(annotate): Show origin when cell changed from last suggestion
fix(annotate): Always show cell index
fix(annotate): Hide the path when just the cell changes
fix(annotate): Use ruff's patch origin marker
test(annotate): Capture confusing suggestion
perf(annotate): Remove redundant location lookup
fix(annotate): Remove panic in suggestions
[ty]Tokenize reStructuredText prefix roles (#27464)
refactor(db): Delegate Diff::fmt to an inherent method
refactor(db): Extract applicability note
refactor(db): Decouple applicability note from Diff Part 1
refactor(db): Decouple applicability note from Diff Part 2
refactor(db): Pull out common applicability code
refactor(db): Pull out applicability note call
refactor(db): Render Applicability through annotate-snippets
release: use self-repo syntax (#27514)
[ty] Target the mdtest binary when running individual mdtests (#27521)
[ty] Reject unhashable objects for Hashable protocols (#27441)
[ty] Restore bottom callable subtyping for gradual prefixes (#27519)
[ty] Shrink callable types in property tests (#27504)
[ty] Add subdiagnostic hint when an open `TypedDict` is not assignable to a certain `Mapping` type, but it would be if it were closed (#27512)
[ty] Preserve property getter call errors (#27509)
refactor(db): Better focus comments
refactor(db): Extract cell calculation function
refactor(db): Prefer early return
refactor(db): Clarify we are working with a cell index
refactor(db): Pull out range calculations
refactor(db): Adjust cell index type
refactor(db): Decouple edit filters from diff render
[ty] Simplify numeric tower displays (e.g., `float` over `int | float`) (#27406)
[ty] Avoid double inference of Unpack operands in Union (#27525)
Disable local ThinLTO for optimized development workflows (#27526)
[ty] Fix panic from mismatched OR-pattern bindings (#27533)
[ty] Gradual `isinstance` narrowing for generic classes (#27308)
[ty] Temporarily remove myself from the reviewer pool (#27541)
[ty] Require ClassVar declarations for protocol members (#27530)
[ty] Infer variance through type[T] (#27534)
[ty] Bump ecosystem-analyzer for strict project settings (#27542)
[ty] Expose strict analysis options in the playground (#27543)
[ty] Diagnose invalid descriptor `__get__` calls (#27400)
[ty] Enable (but downrank) auto-import completion suggestions from stub-only modules (#27433)
[ty] Diagnose invalid __getattr__ calls (#27502)
[ty] Normalize type labels in structured docstrings (#26923)
[ty] Reuse primer commands in memory reports (#27553)
[ty] Add helper extension methods for half-range and equality constraints (#27564)
Update Swatinem/rust-cache action to v2.9.2 (#27568)
Bump 0.16.2 (#27555)

# CANDIDATE A

## Release Notes

Released on 2026-08-06.

### Bug fixes

- \[`flake8-pyi`\] Avoid false positives on `singledispatch` functions, where rewriting the union would change which implementation is dispatched to (`PYI041`) ([#27335](https://github.com/astral-sh/ruff/pull/27335))
- Fix some rules reporting duplicate diagnostics when the condition of an `elif` clause contained a violation ([#27404](https://github.com/astral-sh/ruff/pull/27404))

### Server

- Register formatting capabilities dynamically so editors no longer offer Ruff as a formatter for TOML files ([#27332](https://github.com/astral-sh/ruff/pull/27332))

### Other changes

- Internal cleanups: remove unused APIs across crates and narrow internal visibility ([#27339](https://github.com/astral-sh/ruff/pull/27339))
- Add `pywin32` to the ecosystem checks ([#27437](https://github.com/astral-sh/ruff/pull/27437))
- Disable local ThinLTO for optimized development builds ([#27526](https://github.com/astral-sh/ruff/pull/27526))
- Improve internal diagnostic rendering of suggestions in notebooks and fix a panic in the suggestion renderer
- Update dependencies and CI actions
- Many changes to ty, which is released separately; see the ty release notes for details

### Contributors


# CANDIDATE B

## Release Notes

Released on 2026-11-01.

### Bug fixes

- \[`flake8-pyi`\] Avoid false positives on `singledispatch` functions (`PYI041`) ([#27335](https://github.com/astral-sh/ruff/pull/27335))
- Fix the AST visitor so `elif` conditions are no longer visited twice, which could produce duplicate diagnostics ([#27404](https://github.com/astral-sh/ruff/pull/27404))

### Server

- Register formatting capabilities dynamically so Ruff is not offered as a formatter for TOML files ([#27332](https://github.com/astral-sh/ruff/pull/27332))

### Other changes

- Fix diagnostic rendering of suggested changes in notebooks and remove a panic in suggestion rendering
- Remove unused internal APIs and narrow internal visibility ([#27339](https://github.com/astral-sh/ruff/pull/27339))
- Add pywin32 to the Ruff ecosystem checks ([#27437](https://github.com/astral-sh/ruff/pull/27437))
- Disable local ThinLTO for optimized development workflows ([#27526](https://github.com/astral-sh/ruff/pull/27526))
- Update dependencies and GitHub Actions

## Contributors


