# Judge file r2-eslint-10.13.0

## PUBLISHED RELEASE NOTES (written by the maintainers)

## Features
* [`48d5cc4`](https://github.com/eslint/eslint/commit/48d5cc47e43478670ccf95a74f7a73e8408152b5) feat: report references inside IIFEs in `no-use-before-define` (#21238) (Irfan fandi)
* [`a39d9fb`](https://github.com/eslint/eslint/commit/a39d9fb1fdb5db546f6407580cac531ba3370450) feat: add `globalThis` to `no-obj-calls` (#21382) (synthex-byte)
* [`66ac583`](https://github.com/eslint/eslint/commit/66ac58383e076940c11a5d7213ad079028d1140e) feat: check `yield*` expressions in `no-unsafe-optional-chaining` (#21399) (xbinaryx)

## Bug Fixes
* [`87bd2ce`](https://github.com/eslint/eslint/commit/87bd2cef7b2309739c29598fb2be335f4bed71a3) fix: avoid redeclared `let` when `no-var` and `one-var` fix together (#21389) (Daniel Pinto)

## Documentation
* [`4783a68`](https://github.com/eslint/eslint/commit/4783a6806fb73ea4843ac46c6ae3d8285f56c288) docs: Update README (GitHub Actions Bot)
* [`43f0ac9`](https://github.com/eslint/eslint/commit/43f0ac90e7858a834a0e68309e6397fb4cfa72dd) docs: clarify parameter description in `getText` (#21287) (lumir)

## Chores
* [`b59d889`](https://github.com/eslint/eslint/commit/b59d889c7c18d8c73144e6ba46e9e7f3e7da0196) chore: update github/codeql-action action to v4.38.3 (#21412) (renovate[bot])
* [`95e51a0`](https://github.com/eslint/eslint/commit/95e51a0518b15015304eca9844b3f64c1fc167ca) ci: re-enable `@typescript-eslint/typescript-eslint` in ecosystem tests (#21410) (Francesco Trotta)
* [`317fcb3`](https://github.com/eslint/eslint/commit/317fcb365f19e912a60d171a9d5a8d1f16fe4660) chore: update ecosystem plugins (#21409) (ESLint Bot)
* [`b92decf`](https://github.com/eslint/eslint/commit/b92decf8ead7cc4082a18a4a0ab28f3c7c589887) perf: skip no-redeclare scan for single-declaration variables (#21365) (James Ross)
* [`47b7063`](https://github.com/eslint/eslint/commit/47b7063b3f3f7bc7a5bcb87c082577e4e8b96e24) chore: update dependency @eslint/json to ^2.1.1 (#21398) (renovate[bot])
* [`e5aea41`](https://github.com/eslint/eslint/commit/e5aea414cc00555ecd43f6e608bf80e0f9a6d4d6) chore: update ecosystem plugins (#21390) (ESLint Bot)

## COMMIT SUBJECTS between the previous tag and the release

chore: update ecosystem plugins (#21390)
chore: update dependency @eslint/json to ^2.1.1 (#21398)
fix: avoid redeclared `let` when `no-var` and `one-var` fix together (#21389)
feat: check `yield*` expressions in `no-unsafe-optional-chaining` (#21399)
perf: skip no-redeclare scan for single-declaration variables (#21365)
feat: add `globalThis` to `no-obj-calls` (#21382)
docs: clarify parameter description in `getText` (#21287)
feat: report references inside IIFEs in `no-use-before-define` (#21238)
chore: update ecosystem plugins (#21409)
ci: re-enable `@typescript-eslint/typescript-eslint` in ecosystem tests (#21410)
chore: update github/codeql-action action to v4.38.3 (#21412)
docs: Update README
Build: changelog update for 10.13.0
10.13.0

# CANDIDATE A

## Features

- `no-use-before-define` now reports references inside immediately invoked functions (IIFEs) that run before the declaration ([#21238](https://github.com/eslint/eslint/pull/21238)).
- `no-obj-calls` now reports calls to `globalThis`, such as `globalThis()` ([#21382](https://github.com/eslint/eslint/pull/21382)).
- `no-unsafe-optional-chaining` now checks `yield*` expressions ([#21399](https://github.com/eslint/eslint/pull/21399)).

## Bug Fixes

- `no-var` no longer produces invalid code when its fix is applied together with `one-var`'s fix, for example when a `var` redeclares a parameter ([#21389](https://github.com/eslint/eslint/pull/21389)).

## Performance

- `no-redeclare` is faster because it skips variables that are declared only once ([#21365](https://github.com/eslint/eslint/pull/21365)).

## Documentation

- Clarified the `text` parameter description for `getText` in the custom rules docs ([#21287](https://github.com/eslint/eslint/pull/21287)).

## Other

- Updated `@eslint/json` to `^2.1.1` ([#21398](https://github.com/eslint/eslint/pull/21398)).
- Updated ecosystem test plugins and re-enabled `@typescript-eslint/typescript-eslint` in ecosystem tests ([#21390](https://github.com/eslint/eslint/pull/21390), [#21409](https://github.com/eslint/eslint/pull/21409), [#21410](https://github.com/eslint/eslint/pull/21410)).
- Updated `github/codeql-action` to v4.38.3 ([#21412](https://github.com/eslint/eslint/pull/21412)).
- Updated the README.


# CANDIDATE B

## Features

- Report references inside immediately invoked functions in `no-use-before-define` ([#21238](https://github.com/eslint/eslint/pull/21238)).
- Add `globalThis` to the non-callable globals checked by `no-obj-calls` ([#21382](https://github.com/eslint/eslint/pull/21382)).
- Check `yield*` expressions in `no-unsafe-optional-chaining` ([#21399](https://github.com/eslint/eslint/pull/21399)).

## Bug Fixes

- Avoid producing a redeclared `let` when the `no-var` and `one-var` fixes apply together ([#21389](https://github.com/eslint/eslint/pull/21389)).

## Performance Improvements

- Speed up `no-redeclare` by skipping variables with a single declaration ([#21365](https://github.com/eslint/eslint/pull/21365)).

## Documentation

- Clarify the `node` parameter description of `SourceCode#getText` ([#21287](https://github.com/eslint/eslint/pull/21287)).

## Other

- Update dependencies, ecosystem test plugins and the CodeQL action, and re-enable `typescript-eslint` in ecosystem tests ([#21412](https://github.com/eslint/eslint/pull/21412), [#21410](https://github.com/eslint/eslint/pull/21410), [#21409](https://github.com/eslint/eslint/pull/21409), [#21398](https://github.com/eslint/eslint/pull/21398), [#21390](https://github.com/eslint/eslint/pull/21390)).
- Update the README.

