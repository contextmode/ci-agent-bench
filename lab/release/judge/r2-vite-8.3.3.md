# Judge file r2-vite-8.3.3

## PUBLISHED RELEASE NOTES (written by the maintainers)

### Bug Fixes

* **deps:** update launch-editor to v2.14.2 ([#23654](https://github.com/vitejs/vite/issues/23654)) ([22fd1d5](https://github.com/vitejs/vite/commit/22fd1d5238cce2ee9db0eb4122f9e8feb6b06097))
* **html:** filename passed to transformIndexHtml should not include queries ([#23653](https://github.com/vitejs/vite/issues/23653)) ([7dafd8e](https://github.com/vitejs/vite/commit/7dafd8e56f152403a3230608fa4005273c2e9e17))
* **server:** check `fs.serve` for `?vite-wasm-instance` ([#23655](https://github.com/vitejs/vite/issues/23655)) ([ba8b7ab](https://github.com/vitejs/vite/commit/ba8b7ab43b4afa5d0292ab4b6e3a7b5033cc9c73))
* **server:** store ids to `safeModulePaths` rather than URLs ([#23656](https://github.com/vitejs/vite/issues/23656)) ([c3e06f9](https://github.com/vitejs/vite/commit/c3e06f92e969952466b4e2f5801e85e1e00cd905))


## COMMIT SUBJECTS between the previous tag and the release

fix(html): filename passed to transformIndexHtml should not include queries (#23653)
fix(deps): update launch-editor to v2.14.2 (#23654)
fix(server): check `fs.serve` for `?vite-wasm-instance` (#23655)
fix(server): store ids to `safeModulePaths` rather than URLs (#23656)
release: v8.3.3 (#23657)

# CANDIDATE A

## Bug Fixes

- **security:** Fix `server.fs` checks being bypassed with `?vite-wasm-instance` imports in dev ([#23655](https://github.com/vitejs/vite/pull/23655))
- **security:** Fix `server.fs` checks by recording resolved module ids, not URLs, as safe modules ([#23656](https://github.com/vitejs/vite/pull/23656))
- **security:** Stop query strings from being included in the filename passed to `transformIndexHtml`, and avoid generating script tags with `//` URLs ([#23653](https://github.com/vitejs/vite/pull/23653))

## Dependencies

- Update `launch-editor` to v2.14.2 ([#23654](https://github.com/vitejs/vite/pull/23654))

## Other

- Release v8.3.3 ([#23657](https://github.com/vitejs/vite/pull/23657))
- Add playground tests covering the fixes above


# CANDIDATE B

## v8.3.3

This is a patch release with four fixes, most of them tightening dev server security. If you run the dev server, upgrading is recommended.

### Bug Fixes

- **server:** `server.fs` rules are now also checked for `?vite-wasm-instance` requests, like `?raw`, `?url` and `?inline` ([#23655](https://github.com/vitejs/vite/pull/23655)). Advisory: GHSA-vfpm-58rq-9qcg.
- **server:** The dev server now records resolved module ids, not request URLs, as safe module paths, and no longer records imports that fail to resolve ([#23656](https://github.com/vitejs/vite/pull/23656)). Advisory: GHSA-rq7h-c2jc-7f22.
- **html:** The filename passed to `transformIndexHtml` no longer includes the query string ([#23653](https://github.com/vitejs/vite/pull/23653)). Advisory: GHSA-9jrq-w75r-8gcw.
- **html:** Dev request URLs that start with `//` are now treated as starting with a single `/`, so Vite no longer generates `<script src="//…">` tags that point to another host ([#23653](https://github.com/vitejs/vite/pull/23653)).
- **deps:** Updated `launch-editor` to v2.14.2 ([#23654](https://github.com/vitejs/vite/pull/23654)). Advisories: GHSA-698v-4r3x-3vcv, GHSA-r825-w8mm-5pxw, GHSA-587h-7wmj-h5pm.

### Other

- Added tests for the changes above, including new `fs-serve` and `html` playground cases.
- Allowed the `launch-editor` v2.14.2 packages in the workspace release-age settings.
- Bumped the version to 8.3.3 ([#23657](https://github.com/vitejs/vite/pull/23657)).

