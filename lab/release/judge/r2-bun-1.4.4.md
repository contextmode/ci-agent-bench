# Judge file r2-bun-1.4.4

## PUBLISHED RELEASE NOTES (written by the maintainers)

To install Bun v1.4.4
```bash
curl -fsSL https://bun.com/install | bash
# or you can use npm
# npm install -g bun
```

Windows:
```bash
powershell -c "irm bun.com/install.ps1|iex"
```

To upgrade to Bun v1.4.4:
```bash
bun upgrade
```

### [Read Bun v1.4.4's release notes on Bun's blog](https://bun.com/blog/bun-v1.4.4)

### Thanks to 39 contributors!

- [@0xh3x](https://github.com/0xh3x)
- [@1cedsoda](https://github.com/1cedsoda)
- [@alex-mextner](https://github.com/alex-mextner)
- [@alii](https://github.com/alii)
- [@Artoria2e5](https://github.com/Artoria2e5)
- [@bompus](https://github.com/bompus)
- [@C0casio45](https://github.com/C0casio45)
- [@cirospaciari](https://github.com/cirospaciari)
- [@davidhevn](https://github.com/davidhevn)
- [@deepshekhardas](https://github.com/deepshekhardas)
- [@Dex4Sure](https://github.com/Dex4Sure)
- [@dylan-conway](https://github.com/dylan-conway)
- [@EffortlessSteven](https://github.com/EffortlessSteven)
- [@eriklangille](https://github.com/eriklangille)
- [@filipesarturi](https://github.com/filipesarturi)
- [@fredluz](https://github.com/fredluz)
- [@gerardp](https://github.com/gerardp)
- [@gohryt](https://github.com/gohryt)
- [@himself65](https://github.com/himself65)
- [@hughescr](https://github.com/hughescr)
- [@Jarred-Sumner](https://github.com/Jarred-Sumner)
- [@jdjkelly](https://github.com/jdjkelly)
- [@jecquas](https://github.com/jecquas)
- [@jobansd](https://github.com/jobansd)
- [@kernoeb](https://github.com/kernoeb)
- [@KilianB](https://github.com/KilianB)
- [@MarshallOfSound](https://github.com/MarshallOfSound)
- [@Neekoras](https://github.com/Neekoras)
- [@nikeee](https://github.com/nikeee)
- [@nikelborm](https://github.com/nikelborm)
- [@ousamabenyounes](https://github.com/ousamabenyounes)
- [@pjb3](https://github.com/pjb3)
- [@RajeshKumar11](https://github.com/RajeshKumar11)
- [@ralyodio](https://github.com/ralyodio)
- [@robobun](https://github.com/robobun)
- [@RubenPari](https://github.com/RubenPari)
- [@sosukesuzuki](https://github.com/sosukesuzuki)
- [@steipete](https://github.com/steipete)
- [@SyMind](https://github.com/SyMind)


## COMMIT SUBJECTS between the previous tag and the release

Bump
tls: consolidate the open TLS fixes (both engines, node:tls, node:https, WebSocket, SQL) (#44618)
`bun check`: three false errors, with immer's `Draft<this>`, with ts-pattern and with a union of intersections (#44955)
DOM constructors: read new.target.prototype before X::create() (#45008)
Add `bun lint` and `bun format` (#44805)
install: migrate Yarn Berry (v2+) yarn.lock to bun.lock (#40057)
`bun check`: `readonly`, `private` and `protected` on a property of an intersection or a union, a large `paths` map, and two more differences from `tsc` (#45001)
`bun check`: circles, loops and types in progress as `tsc` has them, and `then` on `Promise<T> | PromiseLike<T>` (#45066)
install: use the shared percent-encoding helpers in the yarn berry migration (#45051)
Fix startup SIGILL on Linux arm64 when SVE2 is reported without SVE (#45099)
test: replace verdaccio with an npm registry on Bun.serve (#44055)
`bun lint`, `bun fmt`: the first run, oxlint's order, Prettier's Tailwind plugin, native JavaScript plugins, a faster `Bun.Glob` (#45043)
node:http: build `req.headers` in one native call, validate a set header name once (#44912)
ci: use `bun lint` and `bun fmt`; docs: a Linter tab (#45119)
ci: fix the `Format` check; docs: give the formatter its own tab (#45121)
test: wait for all 100 requests in the next dev server test (#45109)
`bun check`: three differences from `tsc` in generic types, and `-b` with many small projects (#45097)
test: fix the race in the filesink pending-write test (#45103)
test: give the AbortSignal.any leak test a signal above the noise (#45107)
node:tls: keep the peer's answer when a pending write is rejected (#45124)
test: stop the lint config tests from calling the npm registry (#45110)
test: prune flaky-tests.txt, and read flaky-new wherever flaky is read (#45137)
test: fix two races in the h2 and h3 graceful stop test (#45105)
test: fix rule-docs.test.ts on Windows (#45135)
streams: pull a blob into a buffer the size of what it has left (#45120)
`bun lint`: load ESLint plugins from bunfig.toml; `bun fmt`: print errors like the rest of Bun (#45134)
tls: stop a node:https busy loop after a rejected send (#45139)
`bun fmt`: format Svelte components (#45146)
Bun.JSONL: fix `read` and repeated values when `,` `]` or `}` follows a value (#45190)
`bun lint`, `bun fmt`: `bunfig.toml` from a subdirectory, `svelte` in `[fmt]`, `oxlint-disable` without a config, and fixes (#45193)
`bun lint`: the rules that need types, compared with tsgolint function by function (#45133)
css: keep translate, rotate and scale apart from transform (#45210)
`bun lint`: redundant parentheses don't change what type-aware rules report (#45212)
Headers: iterate without a lookup and a string per name (#45157)
`bun check`: fix a hang in inference, errors missed in loops, and two false errors (#45217)
`bun lint`: report a problem once when a typed and an untyped rule both look for it (#45228)
`bun fmt`: every comment is attached to one node before printing, as in Prettier (#45205)
install: consolidate the open package manager pull requests (#44968)
sockets: a peer that keeps the receive buffer full no longer stops timers (#45278)
TextEncoder: fix `encode` of a substring whose parent string changed width (#45281)
`bun fmt` and `bun lint`: follow-ups to the comment model (#45268)
Bump WebKit: the limits of cgroup v2 are seen where a cgroup v1 hierarchy exists beside it (#45272)
worker_threads: array methods see indexed keys of a `SHARE_ENV` `process.env` prototype (#45283)
build: link the WebKit prebuilts with assertions and coverage of JSC on Linux x64 (#45280)
Round long hexadecimal, octal and binary literals to the nearest double (#45290)
util.inspect: don't take the iterator guards from the writable `node:util/types` (#45291)
Bun.ModuleGraph: `dispose()` closes the `Bun.Terminal` terminals the graph opened (#45294)
Bun.ModuleGraph: `dispose()` with a `node:http` server still listening no longer leaks the graph (#45293)
Windows: no debug panic in `bun check`, `lint`, `fmt` without a package.json (#45150)
`bun check`: no system call per link when listing a directory on Windows (#45147)
ci-images: check every download against a sha256, and pin what still floated (#45144)
`--disallow-code-generation-from-strings=strict` runs static code only, checked in one place in the engine (#45173)
Fix aborts from `channel._subscribers` and `Object.prototype.onEndCallbacks`, and handle `_subscribers` as Node does (#45289)
`bun lint`: categories skip frameworks the project doesn't use, and `"plugin/*" = "off"` turns a plugin off (#45297)
Upgrade WebKit to 23b0720b40 (#45303)
fetch over HTTP/2: reject on a TLS alert after the handshake, and stop using a connection that went silent after an abort (#45422)
One bindgen: replace bindgen v1 and v2, add classes, generate the Rust side (#45104)
install: fix regressions and older bugs found after the package manager consolidation (#45307)
`bun lint --type-aware`: ask for types on demand instead of checking every file first (#45451)
Compile cache: skip the bytecode optimizer when writing entries (#45446)
`bun lint`: warn when a tsconfig.json without `include` made it load many files to lint a few (#45302)
bake: options own their strings, in one set of types (#44496)
ci: bump mordant to 8ba3540 (#45463)
ci: bump mordant to 0d47474 (#45465)
install: terse messages, quieter output, and retries that start at 50 ms (#45460)
bake: drop React-specific behavior from core ("use server", --server-components, bun:app) (#45461)
ci: bump mordant to 564c8da (#45478)
remove JSPromise Strong::from_value, its last caller is gone (#45481)
Bun.indexOfLine with the bindgen, and .allowShared for a SharedArrayBuffer (#45454)
`bun lint`, `bun fmt`, `bun check`: fix the open issues (#45482)
Bump WebKit to 87ee10da087b (#45567)
Define eighteen Bun.* functions with the bindgen (#45450)
install: replace a file at a command's name behind a symlinked node_modules (#45477)
test: pack the rename-retry fixture with Bun.Archive, not the system tar (#45588)
bake: move the code into folders by job (no behavior change) (#45489)
bake: fix a plugin leak, ignoreDirs parsing, and a router crash (#45605)
YAML.parse: name a key that is a sequence or a mapping once the input has been read (#45593)
install: accept a migrated yarn.lock whose resolutions key has a range (#45616)
WebSocket: real closing handshake, one failure path, `ws` rewritten on native transports (consolidates the open WebSocket PRs) (#45223)
test: start the exit timer in worker-terminate-lifetime.test.ts once the fetches have responded (#45600)
test: reset with terminate() in the close() error tests of socket.test.ts (#45598)
test: drop the 5 second timeout of load-same-js-file-a-lot.test.ts (#45635)
test: compare the tarballs of the overrides test in run-autoinstall.test.ts without their order (#45640)
test: give the registry.npmjs.org stand-in of the migration tests its own cache (#45644)
test: keep hot() from being inlined in disallow-code-generation-from-strings.test.ts (#45639)
test: run harness-max-rss.test.ts and compile-rss.test.ts outside the parallel batch (#45636)
test(bake): remove the test that checks `Response.render` stays removed (#45641)
Add b.bytes and define thirty-five Bun.* functions with the bindgen (#45590)
`bun lint`: JSON and Markdown natively, programs in parallel. `bun check -b`: share work between projects. `bun fmt`: `package.json` and Svelte without Prettier (#45595)
sql: consolidate the open Bun.sql, bun:sqlite and node:sqlite pull requests (#45304)
`fs.realpath`: a backslash is part of the file name on POSIX, and each variant reads its path as Node does (#45423)
Define Bun.CryptoHasher, the static hashers and Bun.sha with the bindgen (#45687)
test: bind the blackhole listener to lo0 on macOS (#44413)
test: have the grandchild of the crashed worker test in parallel.test.ts block in wait (#45661)
test: ask the heap what keeps a graph alive in the 50 graphs test of module-graph.test.ts (#45674)
test: yield the next chunk once the client has the first in async-iterator-stream.test.ts (#45688)
test: wait for the close callback in the batch test of node-dgram.test.js (#45686)
test: spell PATH one way in bunEnv on Windows (#45692)
Remove dead code from bun_lint, bun_sema, BunProcess.cpp, and NodeDirent.cpp (#45764)
add bun bake: serve app/pages and app/server.ts (#45682)
test: rename the marker file into place in the macOS end-to-end test of cron.test.ts (#45809)
test: install the signal storm handler of setTimeout.test.js with SA_RESTART (#45811)
test: wait for the child in module-graph-workers.test.ts only once the worker's dispose() has returned (#45813)
test: do not wait for a build that is already done in module-graph-isolation.test.ts (#45821)
test: compile eight components on Windows in the chain of functions test of react-compiler.test.ts (#45808)
Check published types against the bindgen schemas, honor `memLevel` and `strategy` in `gzipSync` and `deflateSync`, and pass dictionaries to Rust by reference (#45794)
sql: fixes for problems found after the consolidation (#45304) (#45711)
Move 58 small natives of `node:*` and `Bun` to bindgen schemas (#45851)
WebSocket client: follow-up fixes to #45223 (#45720)
install: more fixes after the package manager consolidation (#45710)
bun bake: build plugins from bake.config.ts (#45828)
bun bake: start again when bake.config.ts changes (#45902)
bun bake: .tsx pages and frameworks in bake.config.ts (#45905)
install: fix regressions since 1.4.3 and resolve peer dependencies more like pnpm (#45898)
`bun check`: 1.4x to 7.8x faster on large projects. Fixes for `bun check`, `bun lint` and `bun fmt` (#45800)
bun bake: getServerSideProps, getStaticProps and getStaticPaths (#45911)
dev error overlay: scroll, show duplicate errors once, underline the whole css url() (#45921)
dev error overlay: the look of bun.com, and errors of one kind in one card (#45959)
Move `Crypto`, `TextDecoder`, `Bun.FileSystemRouter` and three more classes to bindgen schemas (#45888)
bun bake: the framework names the server-only exports of its pages (#45996)
test: fix 20 flaky tests (#45873)
test: fix bake.test.ts cleanup and the --check URL on Windows (#46135)
bun bake: require() of a built-in, and a route whose import threw (#46017)
Source positions: coverage, stack frames, call sites and source maps agree with the source (#45677)
crypto: update root certificates (#46159)
ci-images: update the system's trusted roots (#46227)
`bun check`: fix errors lost since #45800, and 9 to 37% faster (#46001)
Hardening: fix crashes across the runtime, bundler, dev server, shell and CLI (#46021)
Fix `TextEncoder.encodeInto` panic on a detached destination (#46274)
Fix `bun:sqlite` segfault in `Statement#run` before any `Database` has been opened (#46291)
Coverage: code that is skipped, or never reached after a yield or an await, reads as not run (#46183)
tls: reject chains containing blocked public keys, update root certificates to NSS 3.131.1 (#46300)
ci: update buildkite-agent to 4.7.0 (#46298)
bindgen: classes whose struct outlives the JS object, and move `Timeout`, `Immediate`, `NodeHTTPResponse` and 14 more to schemas (#46128)
Fix `FileSink` panic when `start({ path })` moves a writer from a TTY to a regular file (#46283)
bun test --coverage: list the line of finally (#46301)
build: --hardened=on compiles everything with the stack protector, _FORTIFY_SOURCE, stack clash protection and zeroed locals (#46317)
Hardening follow-up: fix regressions from #46021 and more crashes (#46270)
bun test --coverage: list the lines of an object literal's braces and of else (#46161)
Take a `Bun.build()` output as the Blob it holds in `Bun.hash`, `CryptoHasher`, the parsers and the client `WebSocket` (#45823)
bun test --coverage: list the lines of case and default (#46327)
tls: keep a stream TLS engine's context alive while its entry points run (#46335)
install: put the resolutions back after a layout hoist (#45783)
fetch: stop a `Connection: keep-alive` header from undoing `keepalive: false` on HTTP/1.1 (#46379)
bun build --react-compiler: catch has its own position in the source map (#46378)
structuredClone: reject malformed CryptoKey records instead of returning bogus or null keys (#46387)
js_parser: bind the body of a class with lowered class decorators to the decorated class (#45435)
Bump WebKit: the GC suspend signal handler works on an alternate signal stack (#45427)
sql(postgres): read the rows of a Bind written before its statement's RowDescription as text (#46408)
dev server: an `export *` after another statement of the same path loses exports of a barrel target (#46229)
Bun.write: stop reporting a caught direct stream failure as an unhandled rejection (#41721)
bun test --isolate: a macro call is `undefined` from the second test file on (#46405)
fetch, RedisClient: a TLS session that breaks after its handshake is a lost connection, not a failed handshake (#46409)
structuredClone: reject RSA CryptoKey records with no hash and ChaCha20-Poly1305 keys that are not 32 bytes (#46410)
install: re-parse a cached package.json in the call that replaces its text (#46394)
node:http: a request gets its body behind the FIN of socket.end() (#44419)
Fix regressions since 1.4.3 in bun install, bunx, node:fs and node:http2, and update brotli (#46392)
`bun check`: fix two regressions from #46001, the empty name in TS2883, and `this` of a constrained type parameter (#46417)
`bun lint`: a command in canary builds only (#46438)
install: apply overrides to the range that bun add and bun update write (#46230)
ws: keep the async context of the call beside each waiting send callback (#46390)
pack: read an ignore line or `files` entry that begins with `!(` as a negation again (#46240)
Fix quadratic `Bun.stringWidth` on non-ASCII multi-line text (#46389)
http3: lift lsquic's limits on header sizes, and honor the stream ID of a GOAWAY (#46436)
Fix 7 regressions since 1.4.3 in bun install, bunx, bun patch, bun pm pack and bun: imports (#46455)
usockets: fail the connection when send() reports too many bytes (#46452)
ci: fix the Windows sign step on the Build Tools image (#46462)
compile: revert the startup check of every module graph offset (#46461)
react-compiler: fix a throw on each render and stale values for a `let` that a memo block reassigns (#42482)
bunx: run the platform binary of a native dependency, not its stub (#46468)
install: fall back to copyfile only when the hard link itself fails (#46480)
node:http, node:http2: refuse the malformed requests that Node refuses (#46456)

# CANDIDATE A

## Highlights

- **`bun fmt`** is now a native formatter that reads Prettier and oxfmt configs. It formats `package.json` and Svelte files without Prettier. ([#44805](https://github.com/oven-sh/bun/pull/44805), [#45146](https://github.com/oven-sh/bun/pull/45146), [#45595](https://github.com/oven-sh/bun/pull/45595))
- **`bun lint`** is a native linter that reads ESLint and oxlint configs. It is only in canary builds for now, and release builds still run your own `lint` script. ([#44805](https://github.com/oven-sh/bun/pull/44805), [#46438](https://github.com/oven-sh/bun/pull/46438))
- **`bun bake`** serves the app in the current directory with the dev server: `app/pages/*.html` become routes, and an optional `app/server.ts` adds `routes`, `fetch` and `websocket`. ([#45682](https://github.com/oven-sh/bun/pull/45682))
- **WebSocket** client, `Bun.serve({ websocket })` and the built-in `ws` package were reworked to follow the spec and Node more closely (see Breaking changes). ([#45223](https://github.com/oven-sh/bun/pull/45223))
- **`bun install`** can migrate a Yarn Berry (v2+) `yarn.lock` to `bun.lock`. ([#40057](https://github.com/oven-sh/bun/pull/40057))

## Breaking changes and behavior changes

### WebSocket ([#45223](https://github.com/oven-sh/bun/pull/45223))
- `WebSocket.close()` now does a real closing handshake, and `close` fires when the connection actually closes.
- `close()` with no code sends an empty Close frame, and both sides see code 1005.
- Any client failure fires `error` and then `close` with code 1006. The details are in `ErrorEvent.message` and `ErrorEvent.error.code`.
- The 101 handshake response is validated strictly, including extension and `permessage-deflate` parameters.
- Header values are sent one byte per character, as `fetch` and Node do.
- `websocket.error` in `Bun.serve` now gets `(error, ws)`.
- `server.stop(true)` closes each WebSocket with code 1001 "Server closed".
- The `compress` sizes of `Bun.serve` websockets (`"dedicated"`, `"4KB"` to `"256KB"`) now use the window they name, which uses more memory.
- `server.upgrade()` is stricter about which headers it reads and accepts.

### Package manager
- Package manager commands now follow a consolidated, reviewed implementation with quieter output and terse messages. ([#44968](https://github.com/oven-sh/bun/pull/44968), [#45460](https://github.com/oven-sh/bun/pull/45460))
- Registry retries now back off, starting at 50 ms. `BUN_CONFIG_HTTP_RETRY_BACKOFF` sets the first wait. ([#44968](https://github.com/oven-sh/bun/pull/44968), [#45460](https://github.com/oven-sh/bun/pull/45460))
- `bun install` and `bun add` ignore about 180 flags from npm, Yarn and pnpm that Bun has no equivalent for, and a few are translated, such as `--node-linker`. Typos are still errors. ([#45898](https://github.com/oven-sh/bun/pull/45898))
- `bun ci` and `--frozen-lockfile` fail when `package.json` dependencies changed since `bun.lock` was saved. ([#44968](https://github.com/oven-sh/bun/pull/44968))
- `file:` folders are installed as hard-linked real files, not symlinks. ([#44968](https://github.com/oven-sh/bun/pull/44968))
- `bunx` stops with exit code 126 or 1 when the project's own bin file exists but can't run, instead of running the registry copy. ([#46455](https://github.com/oven-sh/bun/pull/46455))
- Overrides keyed by an `npm:` alias now read the `catalog:` or `workspace:` value under the alias name. ([#46455](https://github.com/oven-sh/bun/pull/46455))
- An import of an unknown `bun:name` stays `bun:name` and is no longer looked up as `name`. ([#46455](https://github.com/oven-sh/bun/pull/46455))
- `bun check`, `bun lint` and `bun fmt` fixes are listed under Other tooling.

### Other
- `node:http` and `node:http2` servers now refuse requests that Node refuses: control or high bytes in the request target, DEL in header values, and HTTP/2 DATA past the declared `content-length`. `Bun.serve` is unchanged. ([#46456](https://github.com/oven-sh/bun/pull/46456))
- `--disallow-code-generation-from-strings=strict` runs only static code. ([#45173](https://github.com/oven-sh/bun/pull/45173))
- `bun bake` no longer has built-in React behavior such as `"use server"`, `--server-components` and `bun:app`. ([#45461](https://github.com/oven-sh/bun/pull/45461))
- `Bun.sql`, `bun:sqlite` and `node:sqlite` were reworked, with many fixes and faster queries. ([#45304](https://github.com/oven-sh/bun/pull/45304), [#45711](https://github.com/oven-sh/bun/pull/45711))

## Features

- `bun test --coverage` and stack traces now agree with the source on positions. Skipped code, and code after a `yield` or `await` that is never reached, count as not run. ([#45677](https://github.com/oven-sh/bun/pull/45677), [#46183](https://github.com/oven-sh/bun/pull/46183))
- `bun test --coverage` lists the lines of `case`, `default`, `finally`, `else` and object literal braces. ([#46327](https://github.com/oven-sh/bun/pull/46327), [#46301](https://github.com/oven-sh/bun/pull/46301), [#46161](https://github.com/oven-sh/bun/pull/46161))
- `bun bake` supports `.tsx` pages, `getServerSideProps`, `getStaticProps` and `getStaticPaths`, plugins and frameworks from `bake.config.ts`, and restarts when that file changes. ([#45905](https://github.com/oven-sh/bun/pull/45905), [#45911](https://github.com/oven-sh/bun/pull/45911), [#45828](https://github.com/oven-sh/bun/pull/45828), [#45902](https://github.com/oven-sh/bun/pull/45902), [#45996](https://github.com/oven-sh/bun/pull/45996))
- The dev server error overlay has a new look, groups errors of one kind, and shows duplicates once. ([#45959](https://github.com/oven-sh/bun/pull/45959), [#45921](https://github.com/oven-sh/bun/pull/45921))
- `bun build` accepts `Bun.build()` outputs wherever a Blob is expected: `Bun.hash`, `CryptoHasher`, the parsers and the client `WebSocket`. ([#45823](https://github.com/oven-sh/bun/pull/45823))
- `gzipSync` and `deflateSync` honor `memLevel` and `strategy`. ([#45794](https://github.com/oven-sh/bun/pull/45794))
- `Bun.indexOfLine` accepts a `SharedArrayBuffer`. ([#45454](https://github.com/oven-sh/bun/pull/45454))
- CSS keeps `translate`, `rotate` and `scale` apart from `transform`. ([#45210](https://github.com/oven-sh/bun/pull/45210))
- Root certificates are updated to NSS 3.131.1, and TLS chains containing blocked public keys are rejected. ([#46300](https://github.com/oven-sh/bun/pull/46300), [#46159](https://github.com/oven-sh/bun/pull/46159))
- A hardened build option, `--hardened=on`, adds stack protection and fortified libc calls for Linux x64 builds. ([#46317](https://github.com/oven-sh/bun/pull/46317))
- HTTP/3 enforces header size limits and honors the stream ID of a GOAWAY. ([#46436](https://github.com/oven-sh/bun/pull/46436))
- WebKit was updated several times, including GC and cgroup v2 fixes. ([#45303](https://github.com/oven-sh/bun/pull/45303), [#45567](https://github.com/oven-sh/bun/pull/45567), [#45272](https://github.com/oven-sh/bun/pull/45272), [#45427](https://github.com/oven-sh/bun/pull/45427))

## Fixes

### bun install, bunx and bun pm
- `bun add` and `bun update` apply overrides to the range they write. ([#46230](https://github.com/oven-sh/bun/pull/46230))
- Peer dependencies resolve more like pnpm. ([#45898](https://github.com/oven-sh/bun/pull/45898))
- Hard links only fall back to a copy when the link itself fails. ([#46480](https://github.com/oven-sh/bun/pull/46480))
- `bunx` runs the platform binary of a native dependency, not its stub. ([#46468](https://github.com/oven-sh/bun/pull/46468))
- A workspace outside the project folder installs its dependencies and runs its scripts. ([#45898](https://github.com/oven-sh/bun/pull/45898))
- `bun pm pack` reads an ignore line or `files` entry starting with `!(` as a negation again. ([#46240](https://github.com/oven-sh/bun/pull/46240))
- Resolutions are kept after a layout hoist. ([#45783](https://github.com/oven-sh/bun/pull/45783))
- A cached `package.json` is re-parsed in the call that replaces its text. ([#46394](https://github.com/oven-sh/bun/pull/46394))
- A migrated `yarn.lock` whose `resolutions` key has a range is accepted. ([#45616](https://github.com/oven-sh/bun/pull/45616))
- A file at a command's name is replaced behind a symlinked `node_modules`. ([#45477](https://github.com/oven-sh/bun/pull/45477))
- `bun patch` keeps a checkout that `bun link` linked. ([#46455](https://github.com/oven-sh/bun/pull/46455))
- `npx` flags such as `--quiet`, `-q` and `--no` in package.json scripts no longer exit 1. ([#46392](https://github.com/oven-sh/bun/pull/46392))
- `bun update --interactive` no longer panics in some workspaces with a `catalog`. ([#46392](https://github.com/oven-sh/bun/pull/46392))
- `bun ci` accepts lockfiles that 1.4.3 wrote. ([#46392](https://github.com/oven-sh/bun/pull/46392))

### Networking, TLS, fetch and WebSocket
- `fetch` over HTTP/2 rejects on a TLS alert after the handshake, and stops reusing a connection that went silent after an abort. ([#45422](https://github.com/oven-sh/bun/pull/45422))
- A TLS session that breaks after its handshake is reported as a lost connection, not a failed handshake, in `fetch` and `RedisClient`. ([#46409](https://github.com/oven-sh/bun/pull/46409))
- `Connection: keep-alive` no longer undoes `keepalive: false` on HTTP/1.1. ([#46379](https://github.com/oven-sh/bun/pull/46379))
- A peer that keeps the receive buffer full no longer stops timers. ([#45278](https://github.com/oven-sh/bun/pull/45278))
- The connection fails when `send()` reports too many bytes. ([#46452](https://github.com/oven-sh/bun/pull/46452))
- A `node:https` busy loop after a rejected send is fixed. ([#45139](https://github.com/oven-sh/bun/pull/45139))
- `node:tls` keeps the peer's answer when a pending write is rejected. ([#45124](https://github.com/oven-sh/bun/pull/45124))
- The TLS engine's context stays alive while its entry points run. ([#46335](https://github.com/oven-sh/bun/pull/46335))
- A request gets its body behind the FIN of `socket.end()` in `node:http`. ([#44419](https://github.com/oven-sh/bun/pull/44419))
- The `ws` package keeps the async context of each waiting send callback. ([#46390](https://github.com/oven-sh/bun/pull/46390))
- `node:http` builds `req.headers` faster. ([#44912](https://github.com/oven-sh/bun/pull/44912))

### Runtime and APIs
- `structuredClone` rejects malformed `CryptoKey` records, RSA keys without a hash, and ChaCha20-Poly1305 keys that are not 32 bytes. ([#46387](https://github.com/oven-sh/bun/pull/46387), [#46410](https://github.com/oven-sh/bun/pull/46410))
- `Bun.stringWidth` is no longer quadratic on non-ASCII multi-line text. ([#46389](https://github.com/oven-sh/bun/pull/46389))
- `Bun.write` no longer reports a caught direct stream failure as an unhandled rejection. ([#41721](https://github.com/oven-sh/bun/pull/41721))
- `bun test --isolate` no longer makes a macro call `undefined` from the second test file on. ([#46405](https://github.com/oven-sh/bun/pull/46405))
- `bun:sqlite` no longer segfaults in `Statement#run` before any `Database` is opened. ([#46291](https://github.com/oven-sh/bun/pull/46291))
- `TextEncoder.encodeInto` no longer panics on a detached destination. ([#46274](https://github.com/oven-sh/bun/pull/46274))
- `TextEncoder.encode` handles a substring whose parent string changed width. ([#45281](https://github.com/oven-sh/bun/pull/45281))
- A `FileSink` panic when `start({ path })` moves from a TTY to a file is fixed. ([#46283](https://github.com/oven-sh/bun/pull/46283))
- Postgres rows of a Bind written before its statement's RowDescription are read as text. ([#46408](https://github.com/oven-sh/bun/pull/46408))
- `fs.realpath` treats a backslash as part of the name on POSIX, and `.` in a removed directory throws `ENOENT` as in Node. ([#45423](https://github.com/oven-sh/bun/pull/45423), [#46392](https://github.com/oven-sh/bun/pull/46392))
- `Bun.JSONL` `read` handles values followed by `,`, `]` or `}`. ([#45190](https://github.com/oven-sh/bun/pull/45190))
- `YAML.parse` names a key that is a sequence or mapping in its error. ([#45593](https://github.com/oven-sh/bun/pull/45593))
- Long hexadecimal, octal and binary literals round to the nearest double. ([#45290](https://github.com/oven-sh/bun/pull/45290))
- `util.inspect` no longer takes iterator guards from the writable `node:util/types`. ([#45291](https://github.com/oven-sh/bun/pull/45291))
- Aborts from `channel._subscribers` and `Object.prototype.onEndCallbacks` are fixed. ([#45289](https://github.com/oven-sh/bun/pull/45289))
- `process.env` with `SHARE_ENV` in workers works with array methods. ([#45283](https://github.com/oven-sh/bun/pull/45283))
- `Bun.ModuleGraph.dispose()` no longer leaks with a listening `node:http` server and closes `Bun.Terminal` terminals it opened. ([#45293](https://github.com/oven-sh/bun/pull/45293), [#45294](https://github.com/oven-sh/bun/pull/45294))
- Blobs are pulled into a buffer sized to what is left. ([#45120](https://github.com/oven-sh/bun/pull/45120))
- DOM constructors read `new.target.prototype` before creating the object. ([#45008](https://github.com/oven-sh/bun/pull/45008))
- Startup no longer crashes with SIGILL on Linux arm64 that reports SVE2 without SVE. ([#45099](https://github.com/oven-sh/bun/pull/45099))
- Many crashes across the runtime, bundler, dev server, shell and CLI were fixed. ([#46021](https://github.com/oven-sh/bun/pull/46021), [#46270](https://github.com/oven-sh/bun/pull/46270))
- `bun build --compile` no longer checks every module graph offset at startup. ([#46461](https://github.com/oven-sh/bun/pull/46461))
- The compile cache skips the bytecode optimizer when writing entries. ([#45446](https://github.com/oven-sh/bun/pull/45446))

### Bundler, transpiler and dev server
- Class decorators that are lowered bind the class body to the decorated class. ([#45435](https://github.com/oven-sh/bun/pull/45435))
- `--react-compiler` fixes a throw on each render, stale values for a `let` a memo block reassigns, and a missing `catch` source map position. ([#42482](https://github.com/oven-sh/bun/pull/42482), [#46378](https://github.com/oven-sh/bun/pull/46378))
- The dev server no longer loses barrel exports when an `export *` follows another statement of the same path. ([#46229](https://github.com/oven-sh/bun/pull/46229))
- Dev server `require()` of a built-in works, and a route whose import threw is handled. ([#46017](https://github.com/oven-sh/bun/pull/46017))
- Source maps, call sites and error previews agree with the source. ([#45677](https://github.com/oven-sh/bun/pull/45677))

### Tooling: bun check, bun fmt and bun lint
- `bun check` is much faster on large projects, with many fixes for differences from `tsc`. ([#45800](https://github.com/oven-sh/bun/pull/45800), [#46001](https://github.com/oven-sh/bun/pull/46001), [#46417](https://github.com/oven-sh/bun/pull/46417))
- `bun check`, `bun lint` and `bun fmt` no longer panic on Windows without a `package.json`. ([#45150](https://github.com/oven-sh/bun/pull/45150))
- `bun fmt` and `bun lint` read `bunfig.toml` from a subdirectory. ([#45193](https://github.com/oven-sh/bun/pull/45193))

## Other

- Dead code was removed, and several classes and functions were moved to bindgen schemas. ([#45104](https://github.com/oven-sh/bun/pull/45104), [#45851](https://github.com/oven-sh/bun/pull/45851), [#46128](https://github.com/oven-sh/bun/pull/46128))
- CI changes: the Windows sign step, buildkite-agent 4.7.0, and pinned and checksummed image downloads. ([#46462](https://github.com/oven-sh/bun/pull/46462), [#46298](https://github.com/oven-sh/bun/pull/46298), [#45144](https://github.com/oven-sh/bun/pull/45144))
- Many flaky tests were fixed, and the test npm registry now runs on `Bun.serve` instead of Verdaccio. ([#45873](https://github.com/oven-sh/bun/pull/45873), [#44055](https://github.com/oven-sh/bun/pull/44055))


# CANDIDATE B

## Bun v1.4.4

This is a large release. It adds a built-in formatter, a rewritten WebSocket client, a package manager overhaul, a Postgres, MySQL and SQLite rework, and a large round of crash fixes. Some of these change behavior you may rely on, so read **Breaking changes and behavior changes** first.

### Highlights

- `bun fmt` is a native formatter that reads Prettier and oxfmt configs.
- `WebSocket` now does a real closing handshake, and the built-in `ws` package is rewritten on native transports.
- `bun install` gets many fixes, Yarn Berry migration, new `bun pm` commands and `libc`-aware installs.
- `Bun.sql`, `bun:sqlite` and `node:sqlite` get many correctness fixes.
- Hundreds of crashes (segfaults, panics, aborts) now throw normal errors or work.

### Breaking changes and behavior changes

- `close()` on a `WebSocket` now sends a Close frame and fires `close` when the connection actually closes. Before, it fired right away. `close` reports the server's code and reason. [#45223](https://github.com/oven-sh/bun/pull/45223)
- A `WebSocket` that is closed without a code now reports code 1005, as in browsers and Node. [#45223](https://github.com/oven-sh/bun/pull/45223)
- Every `WebSocket` connection failure now fires `error`, then `close` with code 1006. The failure text is in `ErrorEvent.message`. [#45223](https://github.com/oven-sh/bun/pull/45223)
- A script that ends with `ws.close()` now exits one round trip later, and waits up to `BUN_CONFIG_WS_CLOSE_TIMEOUT` (30 s) if the server never answers. Use `terminate()` to exit right away. [#45223](https://github.com/oven-sh/bun/pull/45223)
- `WebSocket` now fails the connection if the server's 101 response picks an extension or a `permessage-deflate` parameter that was not offered. [#45223](https://github.com/oven-sh/bun/pull/45223)
- Header values in the `WebSocket` client and `fetch` are now sent one byte per code unit, as in Node. [#45223](https://github.com/oven-sh/bun/pull/45223)
- `Bun.serve({ websocket })` calls `websocket.error` as `(error, ws)`. Handlers that only take `error` still work. [#45223](https://github.com/oven-sh/bun/pull/45223)
- `server.stop(true)` now closes each WebSocket with 1001 "Server closed". [#45223](https://github.com/oven-sh/bun/pull/45223)
- `compress: "dedicated"` and `"4KB"` to `"256KB"` now use the window size they name, which uses more memory. [#45223](https://github.com/oven-sh/bun/pull/45223)
- `bun install`, `bun add`, `bun remove` and `bun update` still ignore the unknown flags of npm, Yarn and pnpm. A typo such as `--frozen-lockfil` is an error. [#45898](https://github.com/oven-sh/bun/pull/45898)
- `bun ci` and `--frozen-lockfile` now fail if a dependency of the root or a workspace was added, removed or changed in `package.json` since `bun.lock` was saved. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `file:` folders are now installed as hard-linked real files, and their scripts run once, not on every install. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `--provenance`, `--provenance-file`, `publishConfig.provenance` and the matching env var and `.npmrc` setting are now errors, instead of publishing without provenance. [#44968](https://github.com/oven-sh/bun/pull/44968)
- A negated `workspaces` entry such as `!dir/**` now also removes `dir`, as in npm. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun pm ls` lists what is on disk and exits 1 when there is no `node_modules`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- Failed registry requests now retry with a wait, so an unreachable registry takes about 9 s to fail. Set `BUN_CONFIG_HTTP_RETRY_BACKOFF=<ms>` to change the first wait. [#44968](https://github.com/oven-sh/bun/pull/44968), [#45460](https://github.com/oven-sh/bun/pull/45460)
- On glibc Linux, `bun install` no longer installs `-musl` variants of optional native packages. Use `--libc='*'` for both. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bunx` now stops, with exit code 126 or 1, when the project's own bin file cannot run, instead of running the registry copy. [#46455](https://github.com/oven-sh/bun/pull/46455)
- An override whose key is an alias, such as `"my-alias@npm:pkg@^1": "catalog:"`, now reads the catalog entry of the alias. [#46455](https://github.com/oven-sh/bun/pull/46455)
- An unknown `bun:name` import now stays `bun:name` instead of being looked up as `name`. [#46455](https://github.com/oven-sh/bun/pull/46455)
- In `Bun.sql`, integers from 2^51 to 2^53 - 1 are sent as `int8`/`BIGINT` instead of `float8`/`DOUBLE`. [#45304](https://github.com/oven-sh/bun/pull/45304)
- In `Bun.sql`, an array with an enumerable `raw` property is rejected as a template, to stop it from being run as SQL. [#45304](https://github.com/oven-sh/bun/pull/45304)
- In `Bun.sql`, `sql.array()` without a type no longer adds a `::JSON[]` cast. Pass the type if the server cannot infer it. [#45304](https://github.com/oven-sh/bun/pull/45304)
- `affectedRows` is now the number of rows written on PostgreSQL and SQLite, instead of `null`. [#45304](https://github.com/oven-sh/bun/pull/45304)
- `bun:sqlite` `changes` now counts only the statement's own rows, not rows written by triggers and cascades. [#45304](https://github.com/oven-sh/bun/pull/45304)
- 35 PostgreSQL array types, such as `uuid[]`, are now read as arrays instead of the text `"{...}"`. [#45304](https://github.com/oven-sh/bun/pull/45304)
- PostgreSQL columns named `01` and `1` no longer collapse into one key. [#45304](https://github.com/oven-sh/bun/pull/45304)
- A `Date` sent to a PostgreSQL `text` column is now ISO 8601, and a plain object is JSON. [#45304](https://github.com/oven-sh/bun/pull/45304)
- SQL sockets now turn on TCP keepalive (60 s idle). [#45304](https://github.com/oven-sh/bun/pull/45304)
- `bun:sqlite` `get()` now reads one row, and a column named like an index (`"2023"`) comes first in `Object.keys(row)`. [#45304](https://github.com/oven-sh/bun/pull/45304)
- A `db.transaction(fn)` callback that returns an already-rejected promise now rolls back. [#45304](https://github.com/oven-sh/bun/pull/45304)
- `--disallow-code-generation-from-strings=strict` now runs static code only. [#45173](https://github.com/oven-sh/bun/pull/45173)
- The `node:http` and `node:http2` servers now refuse requests that Node refuses. A request target with control characters or bytes from 0x7f to 0xff gets a `400`, and so does a header value with DEL. `Bun.serve` is unchanged. [#46456](https://github.com/oven-sh/bun/pull/46456)
- The `bun bake` React-specific features (`"use server"`, `--server-components`, `bun:app`) are removed from core. [#45461](https://github.com/oven-sh/bun/pull/45461)
- Long hexadecimal, octal and binary literals now round to the nearest double. [#45290](https://github.com/oven-sh/bun/pull/45290)
- `fs.realpath` now treats a backslash as part of the file name on POSIX. [#45423](https://github.com/oven-sh/bun/pull/45423)
- In `fetch` and `RedisClient`, a TLS session that breaks after its handshake is now reported as a lost connection, not a failed handshake. [#46409](https://github.com/oven-sh/bun/pull/46409)
- TLS now rejects certificate chains that contain blocked public keys. [#46300](https://github.com/oven-sh/bun/pull/46300)

### `bun fmt` (new)

- `bun fmt` is now a native formatter. It reads Prettier and oxfmt configs and needs no packages. A project `fmt` script still takes priority. [#44805](https://github.com/oven-sh/bun/pull/44805)
- It formats `.svelte` files and `package.json` itself, without the `prettier` package. [#45146](https://github.com/oven-sh/bun/pull/45146), [#45595](https://github.com/oven-sh/bun/pull/45595)
- It supports the Prettier Tailwind plugin and reads `bunfig.toml` from a subdirectory. [#45043](https://github.com/oven-sh/bun/pull/45043), [#45193](https://github.com/oven-sh/bun/pull/45193)
- It now attaches comments to nodes before printing, as Prettier does. [#45205](https://github.com/oven-sh/bun/pull/45205)
- `bun lint` is also in this release's source, but only in canary builds. It is not in the release build, and `bun lint` still runs your project's own `lint` script. [#46438](https://github.com/oven-sh/bun/pull/46438)

### `bun check`

- It is 1.4x to 7.8x faster on large projects, and `-b` shares work between the projects of a solution. [#45800](https://github.com/oven-sh/bun/pull/45800), [#45595](https://github.com/oven-sh/bun/pull/45595), [#46001](https://github.com/oven-sh/bun/pull/46001)
- It matches `tsc` in many more cases: generics, circular types, loops, `readonly`/`private`/`protected` on unions and intersections, and large `paths` maps. [#45097](https://github.com/oven-sh/bun/pull/45097), [#45066](https://github.com/oven-sh/bun/pull/45066), [#45001](https://github.com/oven-sh/bun/pull/45001), [#44955](https://github.com/oven-sh/bun/pull/44955), [#45217](https://github.com/oven-sh/bun/pull/45217)
- It now reports TS2563 where `tsc` does. [#45595](https://github.com/oven-sh/bun/pull/45595)
- It fixes a hang in inference, a TS2883 error with an empty name and `this` of a constrained type parameter. [#45217](https://github.com/oven-sh/bun/pull/45217), [#46417](https://github.com/oven-sh/bun/pull/46417)
- It no longer makes a system call per link when listing a directory on Windows, and no longer panics without a `package.json`. [#45147](https://github.com/oven-sh/bun/pull/45147), [#45150](https://github.com/oven-sh/bun/pull/45150)

### `bun bake` (experimental)

`bun bake` is on in canary builds. In release builds, set `BUN_FEATURE_FLAG_EXPERIMENTAL_BAKE=1`.

- `bun bake` serves `app/pages/*.html` as pages and an optional `app/server.ts` with `routes`, `fetch` and `websocket`. [#45682](https://github.com/oven-sh/bun/pull/45682)
- It reads `bake.config.ts` for plugins and frameworks, restarts when it changes, and supports `.tsx` pages. [#45828](https://github.com/oven-sh/bun/pull/45828), [#45902](https://github.com/oven-sh/bun/pull/45902), [#45905](https://github.com/oven-sh/bun/pull/45905)
- It supports `getServerSideProps`, `getStaticProps` and `getStaticPaths`, and server-only exports named by the framework. [#45911](https://github.com/oven-sh/bun/pull/45911), [#45996](https://github.com/oven-sh/bun/pull/45996)
- `require()` of a built-in works, and a route whose import threw is handled. [#46017](https://github.com/oven-sh/bun/pull/46017)
- The dev error overlay has a new look, shows duplicate errors once and scrolls. [#45959](https://github.com/oven-sh/bun/pull/45959), [#45921](https://github.com/oven-sh/bun/pull/45921)
- Fixed a plugin leak, `ignoreDirs` parsing and a router crash. [#45605](https://github.com/oven-sh/bun/pull/45605)
- Dev server: fixed an `export *` after another statement of the same path losing exports of a barrel target. [#46229](https://github.com/oven-sh/bun/pull/46229)

### WebSocket

- The `WebSocket` client now does a real closing handshake with one failure path. See the behavior changes above. [#45223](https://github.com/oven-sh/bun/pull/45223), [#45720](https://github.com/oven-sh/bun/pull/45720)
- The built-in `ws` package is rewritten in TypeScript on native transports, and behaves more like npm `ws`. [#45223](https://github.com/oven-sh/bun/pull/45223)
- `server.upgrade()` is stricter about handshake headers, and an HTTP/1.1 Upgrade or CONNECT request without `Host` gets a 400. [#45223](https://github.com/oven-sh/bun/pull/45223)
- Pings and pongs with no listener are dropped instead of queued, which stops a flood from growing memory. [#45223](https://github.com/oven-sh/bun/pull/45223)
- An endless stream of `100 Continue` responses no longer freezes the event loop. [#45223](https://github.com/oven-sh/bun/pull/45223)
- `ws` now keeps the async context of each waiting send callback. [#46390](https://github.com/oven-sh/bun/pull/46390)

### Package manager

New features:

- `bun install` migrates Yarn Berry (v2+) `yarn.lock` to `bun.lock`. [#40057](https://github.com/oven-sh/bun/pull/40057)
- `bun pm cache pack <file>` and `unpack <file>` move the cache entries a lockfile needs as one file. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun pm cache prune` drops old cache entries. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun pm fetch` downloads all dependencies into the cache. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun publish --recursive` and `--filter` publish workspaces, dependencies first. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun update --depth 0` updates direct dependencies only. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun prune --check` exits 1 if anything would be removed. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `packageExtensions` in the root `package.json` adds missing dependencies and peers to registry packages. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `link:./dir` links a directory, relative to the declaring `package.json`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- On Linux, only the glibc or musl variant of an optional native package is installed. `--libc` overrides this. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bunx --cwd`, `bunx --env-file` and `bunx --minimum-release-age` are supported. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `--env-file`, `--no-env-file` and `env = false` in `bunfig.toml` work for all package manager commands. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `minimumReleaseAge` accepts values such as `90m`, `12 hours` and `2 weeks`. `minimumReleaseAgeExcludes` accepts `name@version`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `npm-shrinkwrap.json` is migrated like `package-lock.json`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `--dry-run` works for `bun link`, `unlink`, `pm version`, `pm cache rm`, `pm trust`, `pm pkg` and `pm migrate`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- `bun publish` honors `publishConfig.registry`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- Auto-install reads registries and credentials from `.npmrc`. [#44968](https://github.com/oven-sh/bun/pull/44968)
- Peer dependency resolution now works more like pnpm's. [#45898](https://github.com/oven-sh/bun/pull/45898)

Output:

- About 170 warnings and errors are reworded to be short, and successful commands print much less. [#45460](https://github.com/oven-sh/bun/pull/45460)

Fixes:

- Fixed `bun install --frozen-lockfile` and `bun ci` refusing lockfiles that 1.4.3 wrote. [#46392](https://github.com/oven-sh/bun/pull/46392)
- Fixed `bun update --interactive` panicking after it rewrote `package.json`. [#46392](https://github.com/oven-sh/bun/pull/46392)
- Fixed `npx --quiet`, `-q` and `--no` in a `package.json` script exiting 1. [#46392](https://github.com/oven-sh/bun/pull/46392)
- Fixed a workspace outside the project (such as `../shared`) not getting its dependencies or scripts. [#45898](https://github.com/oven-sh/bun/pull/45898)
- Fixed 7 regressions since 1.4.3 in `bun install`, `bunx`, `bun patch`, `bun pm pack` and `bun:` imports. [#46455](https://github.com/oven-sh/bun/pull/46455)
- `bun add` and `bun update` now apply overrides to the range they write. [#46230](https://github.com/oven-sh/bun/pull/46230)
- `bun pm pack` reads an ignore line or `files` entry beginning with `!(` as a negation again. [#46240](https://github.com/oven-sh/bun/pull/46240)
- `bunx` runs the platform binary of a native dependency, not its stub. [#46468](https://github.com/oven-sh/bun/pull/46468)
- `bun install` falls back to a copy only when the hard link itself fails. [#46480](https://github.com/oven-sh/bun/pull/46480)
- Fixed a cached `package.json` not being re-parsed in the call that replaces its text. [#46394](https://github.com/oven-sh/bun/pull/46394)
- Fixed resolutions being lost after a layout hoist. [#45783](https://github.com/oven-sh/bun/pull/45783)
- Fixed a migrated `yarn.lock` whose `resolutions` key has a range. [#45616](https://github.com/oven-sh/bun/pull/45616)
- A command now replaces a file at its name behind a symlinked `node_modules`. [#45477](https://github.com/oven-sh/bun/pull/45477)
- Fixed more regressions after the package manager changes. [#45307](https://github.com/oven-sh/bun/pull/45307), [#45710](https://github.com/oven-sh/bun/pull/45710), [#46392](https://github.com/oven-sh/bun/pull/46392)

### SQL, `bun:sqlite` and `node:sqlite`

- The open `Bun.sql`, `bun:sqlite` and `node:sqlite` issues are fixed together, with faster Postgres queries (about 20% to 48% less client CPU in the PR's release measurements). [#45304](https://github.com/oven-sh/bun/pull/45304), [#45711](https://github.com/oven-sh/bun/pull/45711)
- `bun:sqlite` `Statement#run` no longer segfaults before any `Database` is opened. [#46291](https://github.com/oven-sh/bun/pull/46291)
- Postgres now reads rows of a `Bind` written before its statement's `RowDescription` as text. [#46408](https://github.com/oven-sh/bun/pull/46408)

### Node.js compatibility

- `node:http` gives a request its body behind the FIN of `socket.end()`. [#44419](https://github.com/oven-sh/bun/pull/44419)
- `node:http` builds `req.headers` in one native call, which is faster. [#44912](https://github.com/oven-sh/bun/pull/44912)
- Fixed regressions in `node:fs` and `node:http2`. [#46392](https://github.com/oven-sh/bun/pull/46392)
- `node:http2` drops DATA past a request's declared `content-length` and resets the stream. [#46456](https://github.com/oven-sh/bun/pull/46456)
- `node:tls` keeps the peer's answer when a pending write is rejected. [#45124](https://github.com/oven-sh/bun/pull/45124)
- `node:https` no longer busy-loops after a rejected send. [#45139](https://github.com/oven-sh/bun/pull/45139)
- Fixed aborts from `channel._subscribers` and `Object.prototype.onEndCallbacks`. `_subscribers` is now handled as in Node. [#45289](https://github.com/oven-sh/bun/pull/45289)
- `worker_threads`: array methods see indexed keys of a `SHARE_ENV` `process.env` prototype. [#45283](https://github.com/oven-sh/bun/pull/45283)
- `util.inspect` no longer takes its iterator guards from the writable `node:util/types`. [#45291](https://github.com/oven-sh/bun/pull/45291)
- `node:stream` web adapters and `node:http2` can no longer end the process with an uncatchable exception. [#46021](https://github.com/oven-sh/bun/pull/46021)

### Web APIs, `fetch` and TLS

- `fetch` no longer lets a `Connection: keep-alive` header undo `keepalive: false` on HTTP/1.1. [#46379](https://github.com/oven-sh/bun/pull/46379)
- `fetch` over HTTP/2 rejects on a TLS alert after the handshake, and stops using a connection that went silent after an abort. [#45422](https://github.com/oven-sh/bun/pull/45422)
- HTTP/3 enforces header size limits, answers `431` to an oversized request and honors the stream ID of a GOAWAY. [#46436](https://github.com/oven-sh/bun/pull/46436)
- TLS fixes across both engines, `node:tls`, `node:https`, WebSocket and SQL. [#44618](https://github.com/oven-sh/bun/pull/44618)
- `Bun.write` no longer reports a caught direct stream failure as an unhandled rejection. [#41721](https://github.com/oven-sh/bun/pull/41721)
- `structuredClone` rejects malformed `CryptoKey` records, RSA keys with no hash and ChaCha20-Poly1305 keys that are not 32 bytes. [#46387](https://github.com/oven-sh/bun/pull/46387), [#46410](https://github.com/oven-sh/bun/pull/46410)
- `Bun.hash`, `CryptoHasher`, the parsers and the client `WebSocket` accept a `Bun.build()` output as the Blob it holds. [#45823](https://github.com/oven-sh/bun/pull/45823)
- `Bun.stringWidth` is no longer quadratic on non-ASCII multi-line text. [#46389](https://github.com/oven-sh/bun/pull/46389)
- `Bun.JSONL`: fixed `read` and repeated values when `,`, `]` or `}` follows a value. [#45190](https://github.com/oven-sh/bun/pull/45190)
- `YAML.parse` names a key that is a sequence or a mapping once the input has been read. [#45593](https://github.com/oven-sh/bun/pull/45593)
- `Bun.indexOfLine` accepts a `SharedArrayBuffer`. [#45454](https://github.com/oven-sh/bun/pull/45454)
- `gzipSync` and `deflateSync` honor `memLevel` and `strategy`. [#45794](https://github.com/oven-sh/bun/pull/45794)
- `Headers` iterates faster. [#45157](https://github.com/oven-sh/bun/pull/45157)
- Fixed `TextEncoder.encode` of a substring whose parent string changed width, and a `TextEncoder.encodeInto` panic on a detached destination. [#45281](https://github.com/oven-sh/bun/pull/45281), [#46274](https://github.com/oven-sh/bun/pull/46274)
- Fixed a `FileSink` panic when `start({ path })` moves a writer from a TTY to a regular file. [#46283](https://github.com/oven-sh/bun/pull/46283)
- Fixed a stream blob being pulled into a buffer of the wrong size. [#45120](https://github.com/oven-sh/bun/pull/45120)
- A peer that keeps the receive buffer full no longer stops timers. [#45278](https://github.com/oven-sh/bun/pull/45278)
- A connection fails when `send()` reports too many bytes. [#46452](https://github.com/oven-sh/bun/pull/46452)
- A stream TLS engine's context stays alive while its entry points run. [#46335](https://github.com/oven-sh/bun/pull/46335)

### Bundler, transpiler and CSS

- A class body with lowered class decorators is now bound to the decorated class. [#45435](https://github.com/oven-sh/bun/pull/45435)
- CSS now keeps `translate`, `rotate` and `scale` apart from `transform`. [#45210](https://github.com/oven-sh/bun/pull/45210)
- `bun build --react-compiler`: `catch` has its own position in the source map, and a throw on each render and stale values for a `let` that a memo block reassigns are fixed. [#46378](https://github.com/oven-sh/bun/pull/46378), [#42482](https://github.com/oven-sh/bun/pull/42482)
- `bun build --compile`: reverted the startup check of every module graph offset. [#46461](https://github.com/oven-sh/bun/pull/46461)
- The compile cache skips the bytecode optimizer when writing entries. [#45446](https://github.com/oven-sh/bun/pull/45446)
- `Bun.ModuleGraph.dispose()` no longer leaks the graph when a `node:http` server is still listening, and closes the `Bun.Terminal` terminals the graph opened. [#45293](https://github.com/oven-sh/bun/pull/45293), [#45294](https://github.com/oven-sh/bun/pull/45294)

### Test runner

- Source positions for coverage, stack frames, call sites, source maps, JUnit, inline snapshots and build errors now agree with the source. This fixes several coverage issues. [#45677](https://github.com/oven-sh/bun/pull/45677)
- `bun test --coverage` now lists the lines of `finally`, `case` and `default`, `else`, and an object literal's braces. [#46301](https://github.com/oven-sh/bun/pull/46301), [#46327](https://github.com/oven-sh/bun/pull/46327), [#46161](https://github.com/oven-sh/bun/pull/46161)
- Code that is skipped, or never reached after a `yield` or `await`, now reads as not run in coverage. [#46183](https://github.com/oven-sh/bun/pull/46183)
- `bun test --isolate`: a macro call is no longer `undefined` from the second test file on. [#46405](https://github.com/oven-sh/bun/pull/46405)

### Crash fixes and hardening

- About 300 open crash fixes were merged, plus about 20 more, across the runtime, bundler, dev server, shell and CLI. [#46021](https://github.com/oven-sh/bun/pull/46021), [#46270](https://github.com/oven-sh/bun/pull/46270)
- Fixed random crashes in `bun build` with macros and a `.env` file. [#46021](https://github.com/oven-sh/bun/pull/46021)
- `bun run` and `bunx` no longer abort when a signal arrives while the child is spawning. [#46021](https://github.com/oven-sh/bun/pull/46021)
- A truncated or corrupted compiled executable now prints an error instead of dying with SIGBUS or a panic. [#46021](https://github.com/oven-sh/bun/pull/46021)
- Paths longer than the path buffer are now ordinary errors, or work. [#46021](https://github.com/oven-sh/bun/pull/46021)
- Native addons can use `uv_async_*`, `uv_timer_*`, `uv_idle_*`, `uv_prepare_*`, `uv_check_*`, `uv_queue_work` and `uv_cwd` on Linux and macOS. [#46021](https://github.com/oven-sh/bun/pull/46021)
- `--watch` and `--hot` print an error instead of panicking when out of inotify instances or file descriptors. [#46021](https://github.com/oven-sh/bun/pull/46021)
- Fixed a startup SIGILL on Linux arm64 when SVE2 is reported without SVE. [#45099](https://github.com/oven-sh/bun/pull/45099)
- The GC suspend signal handler now works on an alternate signal stack, and cgroup v2 limits are seen when a cgroup v1 hierarchy exists beside it. [#45427](https://github.com/oven-sh/bun/pull/45427), [#45272](https://github.com/oven-sh/bun/pull/45272)
- DOM constructors read `new.target.prototype` before creating the object. [#45008](https://github.com/oven-sh/bun/pull/45008)
- `--hardened=on` builds with the stack protector, `_FORTIFY_SOURCE`, stack clash protection and zeroed locals. [#46317](https://github.com/oven-sh/bun/pull/46317)
- TLS root certificates are updated to NSS 3.131.1. [#46300](https://github.com/oven-sh/bun/pull/46300), [#46159](https://github.com/oven-sh/bun/pull/46159)
- WebKit is updated. [#45303](https://github.com/oven-sh/bun/pull/45303), [#45567](https://github.com/oven-sh/bun/pull/45567)
- Brotli is updated. [#46392](https://github.com/oven-sh/bun/pull/46392)

### Other

- Internal: a single bindgen replaces the old two, and many natives moved to bindgen schemas. [#45104](https://github.com/oven-sh/bun/pull/45104), [#45450](https://github.com/oven-sh/bun/pull/45450), [#45590](https://github.com/oven-sh/bun/pull/45590), [#45687](https://github.com/oven-sh/bun/pull/45687), [#45851](https://github.com/oven-sh/bun/pull/45851), [#45888](https://github.com/oven-sh/bun/pull/45888), [#46128](https://github.com/oven-sh/bun/pull/46128)
- Internal: bake code moved into folders by job, and dead code removed. [#45489](https://github.com/oven-sh/bun/pull/45489), [#45764](https://github.com/oven-sh/bun/pull/45764)
- CI: build image downloads are checked against a sha256, `buildkite-agent` and mordant are updated, the Windows sign step is fixed, and the repo uses `bun fmt`. [#45144](https://github.com/oven-sh/bun/pull/45144), [#46298](https://github.com/oven-sh/bun/pull/46298), [#46462](https://github.com/oven-sh/bun/pull/46462), [#45119](https://github.com/oven-sh/bun/pull/45119)
- Tests: many flaky tests were fixed, and the registry test stand-in now runs on `Bun.serve` instead of Verdaccio. [#45873](https://github.com/oven-sh/bun/pull/45873), [#44055](https://github.com/oven-sh/bun/pull/44055)
- Docs: a formatter tab was added. [#45121](https://github.com/oven-sh/bun/pull/45121)

