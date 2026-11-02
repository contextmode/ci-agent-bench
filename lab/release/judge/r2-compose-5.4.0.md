# Judge file r2-compose-5.4.0

## PUBLISHED RELEASE NOTES (written by the maintainers)

## What's Changed

> ℹ️ This release introduces a new way to reconcile resources such as volumes and networks

### ✨ Improvements
* Feat(reconcile): model volume recreation in the plan by @ndeloof in https://github.com/docker/compose/pull/13962
* Feat(reconcile): model network lifecycle in the plan by @ndeloof in https://github.com/docker/compose/pull/13966

### 🐛 Fixes
* Fix(reconcile): preserve zero-replica services during hashing by @junhaoliao in https://github.com/docker/compose/pull/13931
* Fix(config): warn when service selection is silently ignored by @glours in https://github.com/docker/compose/pull/13950
* Fix(build): use platform image-manifest digest, not attested index by @glours in https://github.com/docker/compose/pull/13949
* Fix(oci): honor --insecure-registry when `up` re-loads the model by @ptrdom in https://github.com/docker/compose/pull/13894
* Fix(config): pin type:image volume sources and pre_start hook images by @glours in https://github.com/docker/compose/pull/13956
* Tolerate missing env file on more runtime commands by @maxproske in https://github.com/docker/compose/pull/13603
* Resolve `pre_start` hook images alongside service images by @ndeloof in https://github.com/docker/compose/pull/13937
* Fix(cp): return non-nil Content from dry-run CopyFromContainer by @glours in https://github.com/docker/compose/pull/13982
* Fix(config): apply config flags to `--services`/`--volumes`/`--networks`/`--models`/`--hash` by @glours in https://github.com/docker/compose/pull/13979
* Fix: tolerate missing env file on scale, watch and shell completion by @glours in https://github.com/docker/compose/pull/13973

### 🔧  Internal
* README: remove Go Report Card badge by @thaJeztah in https://github.com/docker/compose/pull/13926
* Docs: adopt `AGENTS.md` standard, symlink `CLAUDE.md` to it by @glours in https://github.com/docker/compose/pull/13871
* Dockerfile: update golang image to alpine `3.23` by @thaJeztah in https://github.com/docker/compose/pull/13921
* Docs: require dated `AI_AGENT_DISCLOSURE.md`, drop committed copy by @glours in https://github.com/docker/compose/pull/13976
* CI: publish images to Docker Hub using OIDC by @glours in https://github.com/docker/compose/pull/13994

### ⚙️ Dependencies
* Build(deps): bump github/codeql-action/upload-sarif from `4.36.2` to `4.37.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13942
* Build(deps): bump the docker-actions group across 1 directory with 4 updates by @dependabot[bot] in https://github.com/docker/compose/pull/13941
* Build(deps): bump actions/stale from `10.3.0` to `10.4.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13943
* Build(deps): bump github.com/mattn/go-shellwords from `1.0.13` to `1.0.14` by @dependabot[bot] in https://github.com/docker/compose/pull/13948
* Build(deps): bump golang.org/x/sync from `0.21.0` to `0.22.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13927
* Build(deps): bump golang.org/x/sys from `0.46.0` to `0.47.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13928
* Build(deps): bump docker/github-builder/.github/workflows/bake.yml from `1.13.0` to `1.14.0` in the docker-actions group by @dependabot[bot] in https://github.com/docker/compose/pull/13953
* Build(deps): bump google.golang.org/grpc from `1.81.1` to `1.82.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13922
* Build(deps): bump softprops/action-gh-release from `3.0.1` to `3.0.2` by @dependabot[bot] in https://github.com/docker/compose/pull/13955
* Build(deps): bump actions/setup-go from `6.5.0` to `7.0.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13960
* Build(deps): bump google.golang.org/grpc from `1.82.0` to `1.82.1` in the go_modules group across 1 directory by @dependabot[bot] in https://github.com/docker/compose/pull/13961
* Build(deps): bump github.com/docker/cli from `29.6.1+incompatible` to `29.6.2+incompatible` by @dependabot[bot] in https://github.com/docker/compose/pull/13968
* Build(deps): bump github/codeql-action/upload-sarif from `4.37.0` to `4.37.3` by @dependabot[bot] in https://github.com/docker/compose/pull/13981
* Build(deps): bump actions/checkout from `7.0.0` to `7.0.1` by @dependabot[bot] in https://github.com/docker/compose/pull/13970
* Build(deps): bump github.com/moby/buildkit from `0.31.1` to `0.31.2` by @dependabot[bot] in https://github.com/docker/compose/pull/13969
* Bump compose-go to version `v2.14.0` by @glours in https://github.com/docker/compose/pull/13983
* Bump go-archive to version `v0.3.0` by @glours in https://github.com/docker/compose/pull/13986
* Build(deps): bump docker/github-builder/.github/workflows/bake.yml from `1.14.0` to `1.15.0` in the docker-actions group by @dependabot[bot] in https://github.com/docker/compose/pull/13989
* Chore(deps): bump github.com/moby/go-archive `v0.3.2` by @thaJeztah in https://github.com/docker/compose/pull/13991
* Update to `go1.26.5` by @thaJeztah in https://github.com/docker/compose/pull/13920
* Build(deps): bump actions/stale from `10.4.0` to `11.0.0` by @dependabot[bot] in https://github.com/docker/compose/pull/13996
* Build(deps): bump docker/docker-agent-action/.github/workflows/review-pr.yml from `2.0.2` to `2.0.3` in the docker-actions group by @dependabot[bot] in https://github.com/docker/compose/pull/13995
* Build(deps): bump ossf/scorecard-action from `2.4.3` to `2.4.4` by @dependabot[bot] in https://github.com/docker/compose/pull/13984
* Chore(deps): github.com/docker/buildx `v0.36.0`, buildkit `v0.32.0` by @glours in https://github.com/docker/compose/pull/13975
* Bump buildkit `v0.32.1` by @glours in https://github.com/docker/compose/pull/13997

## New Contributors
* @junhaoliao made their first contribution in https://github.com/docker/compose/pull/13931

**Full Changelog**: https://github.com/docker/compose/compare/v5.3.1...v5.4.0

## COMMIT SUBJECTS between the previous tag and the release

README: remove Go Report Card badge
fix(reconcile): preserve zero-replica services during hashing
build(deps): bump github/codeql-action/upload-sarif
build(deps): bump the docker-actions group across 1 directory with 4 updates
build(deps): bump actions/stale from 10.3.0 to 10.4.0
fix(config): warn when service selection is silently ignored
build(deps): bump github.com/mattn/go-shellwords from 1.0.13 to 1.0.14
build(deps): bump golang.org/x/sync from 0.21.0 to 0.22.0
build(deps): bump golang.org/x/sys from 0.46.0 to 0.47.0
build(deps): bump docker/github-builder/.github/workflows/bake.yml
build(deps): bump google.golang.org/grpc from 1.81.1 to 1.82.0
fix(build): use platform image-manifest digest, not attested index
build(deps): bump softprops/action-gh-release from 3.0.1 to 3.0.2
fix(oci): honor --insecure-registry when up re-loads the model
docs: adopt AGENTS.md standard, symlink CLAUDE.md to it
build(deps): bump actions/setup-go from 6.5.0 to 7.0.0
build(deps): bump google.golang.org/grpc
Dockerfile: update golang image to alpine 3.23
feat(reconcile): model volume recreation in the plan
fix(reconcile): remove volumes_from consumers before volume recreation
fix(reconcile): preserve backward compatibility for legacy volumes
fix(reconcile): migrate containers to the renamed volume within the same up
fix(config): pin type:image volume sources and pre_start hook images
Tolerate missing env file on runtime commands
feat(reconcile): model network lifecycle in the plan
feat(reconcile): migrate containers on network rename
fix(reconcile): retry network create on conflict, keep owned config-hash
feat(reconcile): best-effort old-network removal on rename
refactor(reconcile): aggregate observed resources, resolve conflicts in reconcile
docs: require dated AI_AGENT_DISCLOSURE.md, drop committed copy
build(deps): bump github.com/docker/cli
build(deps): bump github/codeql-action/upload-sarif
Resolve pre_start hook images alongside service images
Dedup pre_start hook images against service and each other
Force-pull pre_start hook images under pull_policy: always
fix(cp): return non-nil Content from dry-run CopyFromContainer
fix(config): apply config flags to --services/--volumes/--networks/--models/--hash
fix: tolerate missing env file on scale, watch and shell completion
build(deps): bump actions/checkout from 7.0.0 to 7.0.1
build(deps): bump github.com/moby/buildkit from 0.31.1 to 0.31.2
bump compose-go to version v2.14.0
bump go-archive to version v0.3.0
build(deps): bump docker/github-builder/.github/workflows/bake.yml
chore(deps): bump github.com/moby/go-archive v0.3.2
ci: publish images to Docker Hub using OIDC
update to go1.26.5
build(deps): bump actions/stale from 10.4.0 to 11.0.0
build(deps): bump docker/docker-agent-action/.github/workflows/review-pr.yml
build(deps): bump ossf/scorecard-action from 2.4.3 to 2.4.4
chore(deps): github.com/docker/buildx v0.36.0-rc2, buildkit v0.32.0-rc2
fix(oci): fetch artifact layers from blobs endpoint, not via Resolve
bump buildx v0.36.0 and buildkit v0.32.0
bump buildkit v0.32.1

# CANDIDATE A

## What's changed in Docker Compose v5.4.0

### Behavior changes

- Renaming a network now moves the running containers onto the new network and removes the old one on the next `up`. Previously containers stayed on the old network until they were recreated for another reason. ([#13966](https://github.com/docker/compose/pull/13966))

### Improvements

- `pre_start` hook images are now resolved like service images. `config --images` lists them, `pull` fetches them, and `up` pulls them when they are missing instead of failing with "No such image". ([#13937](https://github.com/docker/compose/pull/13937))
- Hook images follow the service's `pull_policy`, including re-pulling with `always`. Images shared with the service or with other hooks are pulled only once. ([#13937](https://github.com/docker/compose/pull/13937))
- `config --resolve-image-digests` and `--lock-image-digests` now cover `type: image` volume sources and `pre_start` hook images. ([#13956](https://github.com/docker/compose/pull/13956))
- `config --lock-image-digests` warns that `pre_start` hook images are not pinned in its override output. ([#13956](https://github.com/docker/compose/pull/13956))
- `compose publish` now fails early if a dependent image cannot be resolved. ([#13956](https://github.com/docker/compose/pull/13956))
- `config --no-interpolate` and `config --variables` now warn when service names are passed, because those names are ignored. ([#13950](https://github.com/docker/compose/pull/13950))
- `scale`, `watch` and shell completion no longer fail when an unrelated service has a missing `env_file`. ([#13973](https://github.com/docker/compose/pull/13973), [#13603](https://github.com/docker/compose/pull/13603))
- Volumes and networks that have changed are now recreated as part of Compose's planned `up` steps. Containers using a recreated volume are replaced, and a volume rename moves them to the new volume in the same `up`. ([#13962](https://github.com/docker/compose/pull/13962), [#13966](https://github.com/docker/compose/pull/13966))
- Updated to buildx v0.36.0 and BuildKit v0.32. ([#13975](https://github.com/docker/compose/pull/13975))

### Bug fixes

- Fixed `config --services`, `--volumes`, `--networks`, `--models` and `--hash` ignoring flags such as `--profile`, `--no-consistency` and `--no-interpolate`. ([#13979](https://github.com/docker/compose/pull/13979))
- Fixed `up --build` recreating containers on every run with the containerd image store and provenance attestations. ([#13949](https://github.com/docker/compose/pull/13949))
- Fixed `up` ignoring `--insecure-registry` when it reloads an `oci://` project. ([#13894](https://github.com/docker/compose/pull/13894))
- Fixed pulling `oci://` Compose artifacts failing against registries that return an error for blob digests on the manifests endpoint. ([#13975](https://github.com/docker/compose/pull/13975))
- Fixed `cp --dry-run` from a container crashing with a nil pointer error. ([#13982](https://github.com/docker/compose/pull/13982))
- Fixed services scaled to zero replicas being dropped when computing configuration hashes. ([#13931](https://github.com/docker/compose/pull/13931))
- Fixed volume and network recreation with legacy volumes, with `volumes_from` consumers, and when a network already exists. ([#13962](https://github.com/docker/compose/pull/13962), [#13966](https://github.com/docker/compose/pull/13966))

### Other

- Updated compose-go to v2.14.0 and go-archive to v0.3.2. ([#13983](https://github.com/docker/compose/pull/13983), [#13986](https://github.com/docker/compose/pull/13986), [#13991](https://github.com/docker/compose/pull/13991))
- Built with Go 1.26.5, which includes security fixes. ([#13920](https://github.com/docker/compose/pull/13920))
- CI now publishes images to Docker Hub with short-lived OIDC credentials. ([#13994](https://github.com/docker/compose/pull/13994))
- Repository guidance moved to `AGENTS.md`, and the AI disclosure file is now dated. ([#13871](https://github.com/docker/compose/pull/13871), [#13976](https://github.com/docker/compose/pull/13976))
- Updated dependencies and GitHub Actions, and added or updated tests.


# CANDIDATE B

## What's changed in Docker Compose v5.4.0

### Fixes

- `config` flags such as `--no-consistency`, `--no-interpolate`, `--no-normalize`, `--no-path-resolution` and `--profile` now also apply to `--services`, `--volumes`, `--networks`, `--models` and `--hash`. This restores earlier behavior. [#13979](https://github.com/docker/compose/pull/13979)
- A missing `env_file` on a service you aren't targeting no longer makes `scale`, `watch` or shell completion fail. Targeted services still have their `env_file` checked. [#13973](https://github.com/docker/compose/pull/13973), [#13603](https://github.com/docker/compose/pull/13603)
- `docker compose cp --dry-run` no longer crashes when copying from a container. [#13982](https://github.com/docker/compose/pull/13982)
- `up --build` no longer recreates containers on every run when images are built with provenance attestations on the containerd image store. [#13949](https://github.com/docker/compose/pull/13949)
- `up` now honors `--insecure-registry` when it reloads a model from an `oci://` source. [#13894](https://github.com/docker/compose/pull/13894)
- Pulling `oci://` resources and publishing Compose artifacts works again with registries that reject manifest lookups for layer blobs. Layers are now fetched directly from the blobs endpoint. [#13975](https://github.com/docker/compose/pull/13975)
- Services with `deploy.replicas: 0` no longer have their config hash computed incorrectly. [#13931](https://github.com/docker/compose/pull/13931)
- `up` now recreates a volume and the containers using it in one run, including containers that share it through `volumes_from`. Volumes created by older versions keep working. [#13962](https://github.com/docker/compose/pull/13962)
- Renaming a network now moves containers to the new network, and the old network is removed when possible. Network creation retries if it conflicts. [#13966](https://github.com/docker/compose/pull/13966)

### Improvements

- `pre_start` hook images are now included in `config --images`, fetched by `pull` and `up`, and no longer fail with "No such image". [#13937](https://github.com/docker/compose/pull/13937)
- Hook images that match the service image or each other are listed and pulled only once.
- Hook images are re-pulled under `pull_policy: always`. With `pull_policy: build`, `pull` still fetches hook images.
- `config --resolve-image-digests` now also pins `type: image` volume sources and `pre_start` hook images, and `publish` fails early if one can't be resolved. [#13956](https://github.com/docker/compose/pull/13956)
- `config --lock-image-digests` keeps `type: image` volumes in its output. It warns that `pre_start` hook images aren't pinned there.
- `config --no-interpolate` and `config --variables` now warn when you pass service names, because services aren't filtered on those paths. [#13950](https://github.com/docker/compose/pull/13950)

### Other

- Updated to Go 1.26.5, which includes security fixes. [#13920](https://github.com/docker/compose/pull/13920)
- Updated dependencies: buildx v0.36.0, BuildKit v0.32.1, compose-go v2.14.0, go-archive v0.3.2, docker/cli v29.6.2, gRPC, and others. [#13975](https://github.com/docker/compose/pull/13975), [#13983](https://github.com/docker/compose/pull/13983)
- The Go minimum version is now 1.26.3.
- Docker Hub images are now published from CI using OIDC instead of a long-lived token. [#13994](https://github.com/docker/compose/pull/13994)
- Updated several GitHub Actions and the Dockerfile's Go image base (Alpine 3.23).
- Adopted the `AGENTS.md` standard for contributor instructions and updated the AI agent disclosure guidelines. [#13871](https://github.com/docker/compose/pull/13871), [#13976](https://github.com/docker/compose/pull/13976)
- Removed the Go Report Card badge from the README. [#13926](https://github.com/docker/compose/pull/13926)
- Added unit and e2e tests for the changes above.

