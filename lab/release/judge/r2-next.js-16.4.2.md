# Judge file r2-next.js-16.4.2

## PUBLISHED RELEASE NOTES (written by the maintainers)

## What's Changed
* [lts-active] turbo-tasks snapshot consistency fixes (#99644, #99732, #99649) by @lukesandberg in https://github.com/vercel/next.js/pull/100002
* [lts-active] Turbopack: backport Pages Router dev module graph chaining (#98823, #99910, #100091) by @sokra in https://github.com/vercel/next.js/pull/100008
* [lts-active] fix(next-code-frame): snap visible window to char boundaries by @lukesandberg in https://github.com/vercel/next.js/pull/100212
* [lts-active] [turbopack] Fix two GC paths that leave half-torn-down dependency edges by @lukesandberg in https://github.com/vercel/next.js/pull/100209
* [lts-active] Turbopack: Ignore realpath errors during module resolution, matching node's behavior by @lukesandberg in https://github.com/vercel/next.js/pull/100217
* [lts-active] Backport docs fixes since v16.4.0 by @icyJoseph in https://github.com/vercel/next.js/pull/100246
* [lts-active] Fix Turbopack lazy dynamic-import chunk-list collisions by @lukesandberg in https://github.com/vercel/next.js/pull/100211
* [lts-active] Backport additional documentation fixes since v16.4.0 by @aurorascharff in https://github.com/vercel/next.js/pull/100262


**Full Changelog**: https://github.com/vercel/next.js/compare/v16.4.1...v16.4.2

## COMMIT SUBJECTS between the previous tag and the release

[lts-active] turbo-tasks snapshot consistency fixes (#99644, #99732, #99649) (#100002)
[lts-active] Turbopack: backport Pages Router dev module graph chaining (#98823, #99910, #100091) (#100008)
[lts-active] fix(next-code-frame): snap visible window to char boundaries (#100212)
[lts-active] [turbopack] Fix two GC paths that leave half-torn-down dependency edges (#100209)
[lts-active] Turbopack: Ignore realpath errors during module resolution, matching node's behavior (#100217)
[lts-active] Keep requests through middleware in a single OpenTelemetry trace (#100226)
[lts-active] Backport docs fixes since v16.4.0 (#100246)
[lts-active] Fix Turbopack lazy dynamic-import chunk-list collisions (#100211)
[lts-active] Backport additional documentation fixes since v16.4.0 (#100262)
Revert "[lts-active] Keep requests through middleware in a single OpenTelemetry trace" (#100269)
v16.4.2

# CANDIDATE A

## Core Changes

- Fix Turbopack dev errors where lazy `dynamic()` imports could collide on chunk lists: [#100211](https://github.com/vercel/next.js/pull/100211)
- Fix Pages Router in Turbopack dev so code from `_app` is reliably available to pages: [#100008](https://github.com/vercel/next.js/pull/100008)
- Fix 404 errors when preloading `next/dynamic` imports from `_app` in the Pages Router, and preload them in production too: [#100008](https://github.com/vercel/next.js/pull/100008)
- Turbopack now ignores `realpath` errors during module resolution, matching Node.js: [#100217](https://github.com/vercel/next.js/pull/100217)
- Fix a Turbopack persistent cache bug that could save inconsistent state when a change happened during a background snapshot, which could crash `next dev` with a `parent_count underflow` error: [#100002](https://github.com/vercel/next.js/pull/100002)
- Fix two Turbopack garbage-collection paths that could leave broken dependency edges: [#100209](https://github.com/vercel/next.js/pull/100209)
- Fix code frames in error output showing a window that could cut through a character: [#100212](https://github.com/vercel/next.js/pull/100212)
- Agent feedback instructions now run with `npx --no-install next` and use clearer wording: [#100262](https://github.com/vercel/next.js/pull/100262)
- The TypeScript plugin now links to the real docs for the `prefetch` and `ensureStatic` route segment options: [#100262](https://github.com/vercel/next.js/pull/100262)

## Other

- Documentation fixes and updates across the App Router guides and API reference: [#100246](https://github.com/vercel/next.js/pull/100246), [#100262](https://github.com/vercel/next.js/pull/100262)
- Updated the `cache-handler-redis` and `cache-handler-redis-turbo` examples, and fixed the `error.tsx` files in the `with-stripe-typescript` example: [#100246](https://github.com/vercel/next.js/pull/100246), [#100262](https://github.com/vercel/next.js/pull/100262)
- Added tests for the changes above.


# CANDIDATE B

## Core Changes

- Turbopack: Fixed a crash in `next dev` (`parent_count underflow`) caused by inconsistent task state saved to the persistent cache. [#100002](https://github.com/vercel/next.js/pull/100002)
- Turbopack: Fixed more cases where cache cleanup could leave the dependency graph in a broken state. [#100209](https://github.com/vercel/next.js/pull/100209)
- Turbopack: Fixed lazy `next/dynamic` imports colliding in chunk lists. [#100211](https://github.com/vercel/next.js/pull/100211)
- Turbopack: Fixed `_app` availability and `next/dynamic` imports in `_app` returning 404s in Pages Router dev. [#100008](https://github.com/vercel/next.js/pull/100008)
- Turbopack: Module resolution now ignores `realpath` errors, matching Node.js. [#100217](https://github.com/vercel/next.js/pull/100217)
- Fixed error code frames cutting through multi-byte characters when trimming long lines. [#100212](https://github.com/vercel/next.js/pull/100212)
- TypeScript plugin hints for `prefetch` and `ensureStatic` now link to the API reference. [#100262](https://github.com/vercel/next.js/pull/100262)
- Updated the agent-feedback instructions in generated agent files to use `npx --no-install next` and clearer wording. [#100262](https://github.com/vercel/next.js/pull/100262)

## Other

- Documentation fixes and additions, including `next analyze` docs, Cache Components and cache handler guidance, Pages Router upgrade guides for 15 and 16, updated demo links, and a new Redis cache handler example. [#100246](https://github.com/vercel/next.js/pull/100246), [#100262](https://github.com/vercel/next.js/pull/100262)
- Added Pages Router and Turbopack regression tests. [#100008](https://github.com/vercel/next.js/pull/100008), [#100211](https://github.com/vercel/next.js/pull/100211)

