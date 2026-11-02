# Judge file r1-node-26.7.0

## PUBLISHED RELEASE NOTES (written by the maintainers)




### Notable Changes

* \[[`58717685a1`](https://github.com/nodejs/node/commit/58717685a1)] - **(SEMVER-MINOR)** **crypto**: support loading private keys through STORE loaders (Filip Skokan) [#63949](https://github.com/nodejs/node/pull/63949)
* \[[`44b940ee8c`](https://github.com/nodejs/node/commit/44b940ee8c)] - **crypto**: update root certificates to NSS 3.125 (Node.js GitHub Bot) [#64746](https://github.com/nodejs/node/pull/64746)
* \[[`c1e4f7365e`](https://github.com/nodejs/node/commit/c1e4f7365e)] - **(SEMVER-MINOR)** **lib**: add perfetto support (Chengzhong Wu) [#64565](https://github.com/nodejs/node/pull/64565)
* \[[`11c2f9c642`](https://github.com/nodejs/node/commit/11c2f9c642)] - **(SEMVER-MINOR)** **module**: implement `Symbol.dispose` in `ModuleHooks` (Remco Haszing) [#63928](https://github.com/nodejs/node/pull/63928)
* \[[`a646319f61`](https://github.com/nodejs/node/commit/a646319f61)] - **(SEMVER-MINOR)** **test\_runner**: add support for `--test-coverage-include-all` (avivkeller) [#64830](https://github.com/nodejs/node/pull/64830)

### Commits

* \[[`a2d3f891d3`](https://github.com/nodejs/node/commit/a2d3f891d3)] - **async\_hooks**: use validateBoolean for trackPromises (Soul Lee) [#64731](https://github.com/nodejs/node/pull/64731)
* \[[`d7266cdd99`](https://github.com/nodejs/node/commit/d7266cdd99)] - **benchmark**: fix calibrate-n option handling (Luan Muniz) [#64146](https://github.com/nodejs/node/pull/64146)
* \[[`2e64293e3f`](https://github.com/nodejs/node/commit/2e64293e3f)] - **buffer**: use Clamp conversion in Blob slice (Donghoon Kang) [#64739](https://github.com/nodejs/node/pull/64739)
* \[[`5fda0958bd`](https://github.com/nodejs/node/commit/5fda0958bd)] - **buffer**: validate copyArrayBuffer offsets against buffer length (Ilia Alshanetsky) [#63904](https://github.com/nodejs/node/pull/63904)
* \[[`5298db40f9`](https://github.com/nodejs/node/commit/5298db40f9)] - **build**: run perfetto build and test on GHA (Chengzhong Wu) [#64721](https://github.com/nodejs/node/pull/64721)
* \[[`e3eac7cef9`](https://github.com/nodejs/node/commit/e3eac7cef9)] - **build**: fix v8\_use\_perfetto source scraping (Chengzhong Wu) [#64721](https://github.com/nodejs/node/pull/64721)
* \[[`ab5f076d7f`](https://github.com/nodejs/node/commit/ab5f076d7f)] - **build**: bump rustc requirement to >=1.86 (Renegade334) [#64543](https://github.com/nodejs/node/pull/64543)
* \[[`df608e061f`](https://github.com/nodejs/node/commit/df608e061f)] - **(SEMVER-MINOR)** **build**: perfetto-sdk (Chengzhong Wu) [#64565](https://github.com/nodejs/node/pull/64565)
* \[[`74928adc46`](https://github.com/nodejs/node/commit/74928adc46)] - **build,tools**: fix shared library cross-compile (Kirill Saied) [#63963](https://github.com/nodejs/node/pull/63963)
* \[[`58717685a1`](https://github.com/nodejs/node/commit/58717685a1)] - **(SEMVER-MINOR)** **crypto**: support loading private keys through STORE loaders (Filip Skokan) [#63949](https://github.com/nodejs/node/pull/63949)
* \[[`58d13b6f3d`](https://github.com/nodejs/node/commit/58d13b6f3d)] - **crypto**: preserve OpenSSL errors from KDF failures (Filip Skokan) [#64776](https://github.com/nodejs/node/pull/64776)
* \[[`478a719cb5`](https://github.com/nodejs/node/commit/478a719cb5)] - **crypto**: fix Argon2 bypassing FIPS mode (Filip Skokan) [#64776](https://github.com/nodejs/node/pull/64776)
* \[[`44b940ee8c`](https://github.com/nodejs/node/commit/44b940ee8c)] - **crypto**: update root certificates to NSS 3.125 (Node.js GitHub Bot) [#64746](https://github.com/nodejs/node/pull/64746)
* \[[`fde85237c7`](https://github.com/nodejs/node/commit/fde85237c7)] - **crypto**: clarify missing cipher error (Filip Skokan) [#64852](https://github.com/nodejs/node/pull/64852)
* \[[`c604d8846d`](https://github.com/nodejs/node/commit/c604d8846d)] - **crypto**: reuse X509 issuer result (Filip Skokan) [#64852](https://github.com/nodejs/node/pull/64852)
* \[[`c68c7d0112`](https://github.com/nodejs/node/commit/c68c7d0112)] - **crypto**: validate key generation options (Filip Skokan) [#64852](https://github.com/nodejs/node/pull/64852)
* \[[`c36bb1d017`](https://github.com/nodejs/node/commit/c36bb1d017)] - **crypto**: fix Argon2 validation errors (Filip Skokan) [#64852](https://github.com/nodejs/node/pull/64852)
* \[[`f61408bb27`](https://github.com/nodejs/node/commit/f61408bb27)] - **crypto**: handle XOF output allocation failure (Filip Skokan) [#64851](https://github.com/nodejs/node/pull/64851)
* \[[`2b4053d046`](https://github.com/nodejs/node/commit/2b4053d046)] - **crypto**: initialize KeyObjectData mutex eagerly (Filip Skokan) [#64851](https://github.com/nodejs/node/pull/64851)
* \[[`4b7b2adf44`](https://github.com/nodejs/node/commit/4b7b2adf44)] - **crypto**: handle DH operation failures (Filip Skokan) [#64851](https://github.com/nodejs/node/pull/64851)
* \[[`12170c3753`](https://github.com/nodejs/node/commit/12170c3753)] - **crypto**: use user-facing error for output encoding changes (Archkon) [#64692](https://github.com/nodejs/node/pull/64692)
* \[[`474f06d550`](https://github.com/nodejs/node/commit/474f06d550)] - **debugger**: preserve overlapping CDP request state (Trivikram Kamat) [#64467](https://github.com/nodejs/node/pull/64467)
* \[[`718cbe9497`](https://github.com/nodejs/node/commit/718cbe9497)] - **deps**: upgrade npm to 11.19.0 (npm team) [#64883](https://github.com/nodejs/node/pull/64883)
* \[[`657c6154b3`](https://github.com/nodejs/node/commit/657c6154b3)] - **deps**: update ngtcp2 to 1.25.0 (Node.js GitHub Bot) [#64944](https://github.com/nodejs/node/pull/64944)
* \[[`75a1fbeff9`](https://github.com/nodejs/node/commit/75a1fbeff9)] - **deps**: update nghttp3 to 1.18.0 (Node.js GitHub Bot) [#64943](https://github.com/nodejs/node/pull/64943)
* \[[`07d7cb7cd8`](https://github.com/nodejs/node/commit/07d7cb7cd8)] - **deps**: update minimatch to 10.2.6 (Node.js GitHub Bot) [#64945](https://github.com/nodejs/node/pull/64945)
* \[[`f7d56359f1`](https://github.com/nodejs/node/commit/f7d56359f1)] - **deps**: update simdjson to 4.6.6 (Node.js GitHub Bot) [#64942](https://github.com/nodejs/node/pull/64942)
* \[[`8b06457cfb`](https://github.com/nodejs/node/commit/8b06457cfb)] - **deps**: update acorn to 8.18.0 (Node.js GitHub Bot) [#64941](https://github.com/nodejs/node/pull/64941)
* \[[`5919d01525`](https://github.com/nodejs/node/commit/5919d01525)] - **deps**: update googletest to 1b6f64d659944658a4c685b7bd9f04c1c3b8a39b (Node.js GitHub Bot) [#64940](https://github.com/nodejs/node/pull/64940)
* \[[`4a87ad6cff`](https://github.com/nodejs/node/commit/4a87ad6cff)] - **deps**: update nghttp2 to 1.70.0 (Node.js GitHub Bot) [#64939](https://github.com/nodejs/node/pull/64939)
* \[[`c96d76a7c8`](https://github.com/nodejs/node/commit/c96d76a7c8)] - **deps**: update zlib to 1.3.2.1-motley-42c2f19 (Node.js GitHub Bot) [#64744](https://github.com/nodejs/node/pull/64744)
* \[[`2b59984c0f`](https://github.com/nodejs/node/commit/2b59984c0f)] - **deps**: V8: backport 5177b10891e6 (avivkeller) [#64631](https://github.com/nodejs/node/pull/64631)
* \[[`b839af91da`](https://github.com/nodejs/node/commit/b839af91da)] - **deps**: update ada to 4.0.0 (Node.js GitHub Bot) [#64790](https://github.com/nodejs/node/pull/64790)
* \[[`70dedef942`](https://github.com/nodejs/node/commit/70dedef942)] - **deps**: update sqlite to 3.53.4 (Node.js GitHub Bot) [#64745](https://github.com/nodejs/node/pull/64745)
* \[[`7bc4c171f5`](https://github.com/nodejs/node/commit/7bc4c171f5)] - **deps**: update Rust crates for V8 14.6.202.34-node.26 (Renegade334) [#64543](https://github.com/nodejs/node/pull/64543)
* \[[`308c6b2ac3`](https://github.com/nodejs/node/commit/308c6b2ac3)] - **deps**: V8: backport 7d9b7e03141d (Manish Goregaokar) [#64543](https://github.com/nodejs/node/pull/64543)
* \[[`8eeae28e88`](https://github.com/nodejs/node/commit/8eeae28e88)] - **deps**: V8: backport c4d06ba586f3 (liujiahui) [#63731](https://github.com/nodejs/node/pull/63731)
* \[[`bbd6fc58c4`](https://github.com/nodejs/node/commit/bbd6fc58c4)] - **diagnostics\_channel**: grow native channel storage (Stephen Belanger) [#64497](https://github.com/nodejs/node/pull/64497)
* \[[`ce8b292955`](https://github.com/nodejs/node/commit/ce8b292955)] - **doc**: fix grammar and punctuation in dgram documentation (Kamal Rawal) [#64957](https://github.com/nodejs/node/pull/64957)
* \[[`1a413a60cf`](https://github.com/nodejs/node/commit/1a413a60cf)] - **doc**: fix grammar and editorial issues in addons documentation (Kamal Rawal) [#64952](https://github.com/nodejs/node/pull/64952)
* \[[`63fbd59e64`](https://github.com/nodejs/node/commit/63fbd59e64)] - **doc**: formalize fn/name as part of TestOptions API (Christopher Hiller) [#64946](https://github.com/nodejs/node/pull/64946)
* \[[`b263b0bca1`](https://github.com/nodejs/node/commit/b263b0bca1)] - **doc**: remove references to `ca`/`crl` as per-context QuicSession options (René) [#64769](https://github.com/nodejs/node/pull/64769)
* \[[`f37de14b27`](https://github.com/nodejs/node/commit/f37de14b27)] - **doc**: fix typo in maintaining-dependencies.md (greenhead) [#64896](https://github.com/nodejs/node/pull/64896)
* \[[`16cb77cdc8`](https://github.com/nodejs/node/commit/16cb77cdc8)] - **doc**: add RafaelGSS as last security release stewards (Rafael Gonzaga) [#64843](https://github.com/nodejs/node/pull/64843)
* \[[`335c28cd17`](https://github.com/nodejs/node/commit/335c28cd17)] - **doc**: fix typos in documentation (greenhead) [#64900](https://github.com/nodejs/node/pull/64900)
* \[[`d4bed8ca39`](https://github.com/nodejs/node/commit/d4bed8ca39)] - **doc**: fix missing references in doc type map (Tim Perry) [#64872](https://github.com/nodejs/node/pull/64872)
* \[[`e71d09d5f1`](https://github.com/nodejs/node/commit/e71d09d5f1)] - **doc**: improve TestContext hook descriptions (Kamal Rawal) [#64899](https://github.com/nodejs/node/pull/64899)
* \[[`7089bd9ae4`](https://github.com/nodejs/node/commit/7089bd9ae4)] - **doc**: add missing float32/float64 FFI type names (Soul Lee) [#64874](https://github.com/nodejs/node/pull/64874)
* \[[`8d3ae0830e`](https://github.com/nodejs/node/commit/8d3ae0830e)] - **doc**: document stream.isDestroyed() (YspritanHyzygy) [#64789](https://github.com/nodejs/node/pull/64789)
* \[[`a757e62af7`](https://github.com/nodejs/node/commit/a757e62af7)] - **doc**: add contributing detail for git Signed-off-by trailer (Mike McCready) [#64862](https://github.com/nodejs/node/pull/64862)
* \[[`3e840f43ed`](https://github.com/nodejs/node/commit/3e840f43ed)] - **doc**: mark config-file as release candidate (Marco Ippolito) [#64516](https://github.com/nodejs/node/pull/64516)
* \[[`70cd5df810`](https://github.com/nodejs/node/commit/70cd5df810)] - **doc**: fix duplicated word in test snapshot docs (Kamal Rawal) [#64837](https://github.com/nodejs/node/pull/64837)
* \[[`d5f36c7adc`](https://github.com/nodejs/node/commit/d5f36c7adc)] - **doc**: remove obsolete cctest node.gyp instructions (Soul Lee) [#64814](https://github.com/nodejs/node/pull/64814)
* \[[`a0bf29ea09`](https://github.com/nodejs/node/commit/a0bf29ea09)] - **doc**: report proper return type on url.format (Brian Muenzenmeyer) [#64806](https://github.com/nodejs/node/pull/64806)
* \[[`e655e42085`](https://github.com/nodejs/node/commit/e655e42085)] - **doc**: use ffi.suffix for library paths in examples (Junsoo Ha) [#64805](https://github.com/nodejs/node/pull/64805)
* \[[`e0f0830dbc`](https://github.com/nodejs/node/commit/e0f0830dbc)] - **doc**: document --permission-audit audit mode behavior (Adrián Estrada) [#64791](https://github.com/nodejs/node/pull/64791)
* \[[`efbede6de0`](https://github.com/nodejs/node/commit/efbede6de0)] - **doc**: clarify tlsSocket.authorized on resumption (soreavis) [#64584](https://github.com/nodejs/node/pull/64584)
* \[[`db95655c4a`](https://github.com/nodejs/node/commit/db95655c4a)] - **doc**: stabilize --disable-warning (Jean Michelet) [#64742](https://github.com/nodejs/node/pull/64742)
* \[[`a8367200be`](https://github.com/nodejs/node/commit/a8367200be)] - **doc**: add MDN links for explicit resource management in fs (lluisemper) [#59557](https://github.com/nodejs/node/pull/59557)
* \[[`1c09165c2e`](https://github.com/nodejs/node/commit/1c09165c2e)] - **doc**: mention constructor check in deepStrictEqual (Sumit Kumar Das) [#62010](https://github.com/nodejs/node/pull/62010)
* \[[`29709324e0`](https://github.com/nodejs/node/commit/29709324e0)] - **doc**: update technical priorities (Jacob Smith) [#64505](https://github.com/nodejs/node/pull/64505)
* \[[`522a28e648`](https://github.com/nodejs/node/commit/522a28e648)] - **doc**: deprecation add more codemod (Augustin Mauroy) [#63175](https://github.com/nodejs/node/pull/63175)
* \[[`c40aaa6539`](https://github.com/nodejs/node/commit/c40aaa6539)] - **doc**: run license-builder (Node.js GitHub Bot) [#63918](https://github.com/nodejs/node/pull/63918)
* \[[`428e9bc50f`](https://github.com/nodejs/node/commit/428e9bc50f)] - **ffi**: fix crash in refCallback and unrefCallback (Trivikram Kamat) [#64881](https://github.com/nodejs/node/pull/64881)
* \[[`33912103e7`](https://github.com/nodejs/node/commit/33912103e7)] - **ffi**: reject fast calls after library close (Trivikram Kamat) [#64860](https://github.com/nodejs/node/pull/64860)
* \[[`b348ed7f92`](https://github.com/nodejs/node/commit/b348ed7f92)] - **ffi**: validate fast 32-bit integer argument ranges (Trivikram Kamat) [#64691](https://github.com/nodejs/node/pull/64691)
* \[[`48f4cfb480`](https://github.com/nodejs/node/commit/48f4cfb480)] - **ffi**: fix optimized buffer conversions (Trivikram Kamat) [#64639](https://github.com/nodejs/node/pull/64639)
* \[[`109ffcd4f3`](https://github.com/nodejs/node/commit/109ffcd4f3)] - **ffi**: preserve link register in ppc64 trampoline (Trivikram Kamat) [#64792](https://github.com/nodejs/node/pull/64792)
* \[[`aa3f168b31`](https://github.com/nodejs/node/commit/aa3f168b31)] - **ffi**: preserve strings during reentrant calls (Trivikram Kamat) [#64551](https://github.com/nodejs/node/pull/64551)
* \[[`ca60942f38`](https://github.com/nodejs/node/commit/ca60942f38)] - **ffi**: preserve uint8 semantics for bool fast calls (Trivikram Kamat) [#64527](https://github.com/nodejs/node/pull/64527)
* \[[`0fb1d2bd65`](https://github.com/nodejs/node/commit/0fb1d2bd65)] - **ffi**: validate fast integer argument ranges (Trivikram Kamat) [#64614](https://github.com/nodejs/node/pull/64614)
* \[[`b250b40b30`](https://github.com/nodejs/node/commit/b250b40b30)] - **fs**: key glob matcher cache by platform (Archkon) [#64571](https://github.com/nodejs/node/pull/64571)
* \[[`e26891ec6a`](https://github.com/nodejs/node/commit/e26891ec6a)] - **http**: fix writableFinished and 'finish' after write errors (Tim Perry) [#64847](https://github.com/nodejs/node/pull/64847)
* \[[`dfc192fdfb`](https://github.com/nodejs/node/commit/dfc192fdfb)] - **http**: avoid aborting IncomingMessage signal on normal close (Archkon) [#64392](https://github.com/nodejs/node/pull/64392)
* \[[`6794441c85`](https://github.com/nodejs/node/commit/6794441c85)] - **http**: guard invalid timeout values in checkConnections (Efe Karasakal) [#64506](https://github.com/nodejs/node/pull/64506)
* \[[`6879aa4aa8`](https://github.com/nodejs/node/commit/6879aa4aa8)] - **http**: propagate highWaterMark to ClientRequest OutgoingMessage (trivenay) [#64653](https://github.com/nodejs/node/pull/64653)
* \[[`72448a82f4`](https://github.com/nodejs/node/commit/72448a82f4)] - **http2**: avoid copying the options in respond() (Matteo Collina) [#64265](https://github.com/nodejs/node/pull/64265)
* \[[`f6692da576`](https://github.com/nodejs/node/commit/f6692da576)] - **http2**: avoid per-write closures in kWriteGeneric (Matteo Collina) [#64265](https://github.com/nodejs/node/pull/64265)
* \[[`3ed37153f8`](https://github.com/nodejs/node/commit/3ed37153f8)] - **http2**: reduce per-request allocations (Matteo Collina) [#64265](https://github.com/nodejs/node/pull/64265)
* \[[`bce92debba`](https://github.com/nodejs/node/commit/bce92debba)] - _**Revert**_ "**http2**: avoid per-write closures in kWriteGeneric" (Antoine du Hamel) [#64663](https://github.com/nodejs/node/pull/64663)
* \[[`b5d5dd74a1`](https://github.com/nodejs/node/commit/b5d5dd74a1)] - _**Revert**_ "**http2**: avoid copying the options in respond()" (Antoine du Hamel) [#64663](https://github.com/nodejs/node/pull/64663)
* \[[`19b9c14d60`](https://github.com/nodejs/node/commit/19b9c14d60)] - **lib**: fix AbortSignal.any() observed-composite leak (Paul Bouchon) [#64481](https://github.com/nodejs/node/pull/64481)
* \[[`d3cada57c2`](https://github.com/nodejs/node/commit/d3cada57c2)] - **lib**: fix typo in comment in \_http\_client.js (agape1225) [#64729](https://github.com/nodejs/node/pull/64729)
* \[[`c1e4f7365e`](https://github.com/nodejs/node/commit/c1e4f7365e)] - **(SEMVER-MINOR)** **lib**: add perfetto support (Chengzhong Wu) [#64565](https://github.com/nodejs/node/pull/64565)
* \[[`6c2157522d`](https://github.com/nodejs/node/commit/6c2157522d)] - **loader**: enforce path normalization before lookup (Maël Nison) [#63917](https://github.com/nodejs/node/pull/63917)
* \[[`31522c41a7`](https://github.com/nodejs/node/commit/31522c41a7)] - **meta**: bump actions/stale from 10.3.0 to 11.0.0 (dependabot\[bot]) [#64935](https://github.com/nodejs/node/pull/64935)
* \[[`88c8b8ef54`](https://github.com/nodejs/node/commit/88c8b8ef54)] - **meta**: bump github/codeql-action/analyze from 4.36.2 to 4.37.3 (dependabot\[bot]) [#64934](https://github.com/nodejs/node/pull/64934)
* \[[`9dcd759a84`](https://github.com/nodejs/node/commit/9dcd759a84)] - **meta**: bump github/codeql-action/autobuild from 4.36.2 to 4.37.3 (dependabot\[bot]) [#64933](https://github.com/nodejs/node/pull/64933)
* \[[`82ca02db3c`](https://github.com/nodejs/node/commit/82ca02db3c)] - **meta**: bump actions/setup-python from 6.3.0 to 7.0.0 (dependabot\[bot]) [#64932](https://github.com/nodejs/node/pull/64932)
* \[[`848e2287f2`](https://github.com/nodejs/node/commit/848e2287f2)] - **meta**: bump github/codeql-action/init from 4.36.2 to 4.37.3 (dependabot\[bot]) [#64931](https://github.com/nodejs/node/pull/64931)
* \[[`ae8ad3b17b`](https://github.com/nodejs/node/commit/ae8ad3b17b)] - **meta**: bump Mozilla-Actions/sccache-action from 0.0.10 to 0.0.11 (dependabot\[bot]) [#64930](https://github.com/nodejs/node/pull/64930)
* \[[`0b359cfa4c`](https://github.com/nodejs/node/commit/0b359cfa4c)] - **meta**: bump cachix/install-nix-action from 31.10.6 to 31.11.0 (dependabot\[bot]) [#64929](https://github.com/nodejs/node/pull/64929)
* \[[`3b4f980f4c`](https://github.com/nodejs/node/commit/3b4f980f4c)] - **meta**: bump github/codeql-action/upload-sarif from 4.36.2 to 4.37.3 (dependabot\[bot]) [#64927](https://github.com/nodejs/node/pull/64927)
* \[[`d7ee9e9ea7`](https://github.com/nodejs/node/commit/d7ee9e9ea7)] - **meta**: bump step-security/harden-runner from 2.19.4 to 2.20.0 (dependabot\[bot]) [#64926](https://github.com/nodejs/node/pull/64926)
* \[[`7e80bbaaa9`](https://github.com/nodejs/node/commit/7e80bbaaa9)] - **meta**: bump ossf/scorecard-action from 2.4.3 to 2.4.4 (dependabot\[bot]) [#64925](https://github.com/nodejs/node/pull/64925)
* \[[`915cabbfcf`](https://github.com/nodejs/node/commit/915cabbfcf)] - **meta**: remove node\_crates .gitignore (René) [#64779](https://github.com/nodejs/node/pull/64779)
* \[[`8e03c54347`](https://github.com/nodejs/node/commit/8e03c54347)] - **meta**: add @nodejs/url as codeowner for node\_url\_pattern.\* (Efe Karasakal) [#64737](https://github.com/nodejs/node/pull/64737)
* \[[`11c2f9c642`](https://github.com/nodejs/node/commit/11c2f9c642)] - **(SEMVER-MINOR)** **module**: implement Symbol.dispose in ModuleHooks (Remco Haszing) [#63928](https://github.com/nodejs/node/pull/63928)
* \[[`fffd8a76d0`](https://github.com/nodejs/node/commit/fffd8a76d0)] - **net**: support TCP handle transfer on Windows (Matteo Collina) [#64460](https://github.com/nodejs/node/pull/64460)
* \[[`fe9e0dbdc2`](https://github.com/nodejs/node/commit/fe9e0dbdc2)] - **net**: support AF\_UNIX paths in net.BoundSocket (Guy Bedford) [#64399](https://github.com/nodejs/node/pull/64399)
* \[[`eb61b7ee1e`](https://github.com/nodejs/node/commit/eb61b7ee1e)] - **permission**: add unique warning codes (David Evans) [#64414](https://github.com/nodejs/node/pull/64414)
* \[[`999a928822`](https://github.com/nodejs/node/commit/999a928822)] - **permission**: support v8.setHeapSnapshotNearHeapLimit (Ilyas Shabi) [#64808](https://github.com/nodejs/node/pull/64808)
* \[[`7de3d095b6`](https://github.com/nodejs/node/commit/7de3d095b6)] - **quic**: fix stop sending behaviour & callback (Tim Perry) [#64710](https://github.com/nodejs/node/pull/64710)
* \[[`6289398bb2`](https://github.com/nodejs/node/commit/6289398bb2)] - **quic**: fix coverage comment typo (Jungwon Sohn) [#64486](https://github.com/nodejs/node/pull/64486)
* \[[`01510dc759`](https://github.com/nodejs/node/commit/01510dc759)] - **quic**: fix segfault after fragmented client hello (Tim Perry) [#64720](https://github.com/nodejs/node/pull/64720)
* \[[`dcc348af97`](https://github.com/nodejs/node/commit/dcc348af97)] - **quic**: serialize stream reset code as string (한만욱) [#64577](https://github.com/nodejs/node/pull/64577)
* \[[`c25b8e3331`](https://github.com/nodejs/node/commit/c25b8e3331)] - **readline**: reduce createInterface overhead (Matteo Collina) [#64585](https://github.com/nodejs/node/pull/64585)
* \[[`14e802d1cd`](https://github.com/nodejs/node/commit/14e802d1cd)] - **sqlite**: invalidate sessions when closing database (Trivikram Kamat) [#64783](https://github.com/nodejs/node/pull/64783)
* \[[`279547b7da`](https://github.com/nodejs/node/commit/279547b7da)] - **sqlite**: check database state before calling SQLite (Trivikram Kamat) [#64812](https://github.com/nodejs/node/pull/64812)
* \[[`bb86521a42`](https://github.com/nodejs/node/commit/bb86521a42)] - **sqlite**: fix crash when a session outlives its database (Mohamed Sayed) [#63797](https://github.com/nodejs/node/pull/63797)
* \[[`870f4997e7`](https://github.com/nodejs/node/commit/870f4997e7)] - **sqlite**: fix use-after-free in Exec() and ApplyChangeset() (Matteo Collina) [#64535](https://github.com/nodejs/node/pull/64535)
* \[[`a8ec5a9df7`](https://github.com/nodejs/node/commit/a8ec5a9df7)] - **src**: fix perfetto build on GetTraceFilePath (Chengzhong Wu) [#64721](https://github.com/nodejs/node/pull/64721)
* \[[`6cd643acaa`](https://github.com/nodejs/node/commit/6cd643acaa)] - **src**: implement MemoryRetainer protocol for ByteSource (Filip Skokan) [#64660](https://github.com/nodejs/node/pull/64660)
* \[[`8725e56928`](https://github.com/nodejs/node/commit/8725e56928)] - **src**: fix crash when writing odd-length hex string via Writev (RajeshKumar11) [#63658](https://github.com/nodejs/node/pull/63658)
* \[[`e018f9a4a1`](https://github.com/nodejs/node/commit/e018f9a4a1)] - **(SEMVER-MINOR)** **src**: add perfetto trace agent (Chengzhong Wu) [#64565](https://github.com/nodejs/node/pull/64565)
* \[[`0611d443ab`](https://github.com/nodejs/node/commit/0611d443ab)] - **(SEMVER-MINOR)** **src**: rename legacy trace event headers (Chengzhong Wu) [#64565](https://github.com/nodejs/node/pull/64565)
* \[[`2897cc1d93`](https://github.com/nodejs/node/commit/2897cc1d93)] - **(SEMVER-MINOR)** **src**: fix trace macro compatibility (Chengzhong Wu) [#64565](https://github.com/nodejs/node/pull/64565)
* \[[`d4d7172e10`](https://github.com/nodejs/node/commit/d4d7172e10)] - **src**: avoid using ToLocalChecked in crypto\_hash (James M Snell) [#64668](https://github.com/nodejs/node/pull/64668)
* \[[`53b7d48b47`](https://github.com/nodejs/node/commit/53b7d48b47)] - **src**: fix libuv assertion on windows (liuxingbaoyu) [#61999](https://github.com/nodejs/node/pull/61999)
* \[[`69d10ed021`](https://github.com/nodejs/node/commit/69d10ed021)] - **src,test**: disable trace events tests when perfetto is enabled (Chengzhong Wu) [#64721](https://github.com/nodejs/node/pull/64721)
* \[[`1b0597b4ef`](https://github.com/nodejs/node/commit/1b0597b4ef)] - **stream**: cut per-chunk allocations in pipeTo (Matteo Collina) [#64890](https://github.com/nodejs/node/pull/64890)
* \[[`2632d606bb`](https://github.com/nodejs/node/commit/2632d606bb)] - **stream**: preserve push signal abort reason (Trivikram Kamat) [#64798](https://github.com/nodejs/node/pull/64798)
* \[[`d5358a75bc`](https://github.com/nodejs/node/commit/d5358a75bc)] - **stream**: skip zero-byte broadcast writes (Trivikram Kamat) [#64772](https://github.com/nodejs/node/pull/64772)
* \[[`796c896fb4`](https://github.com/nodejs/node/commit/796c896fb4)] - **stream**: honor AbortSignal in Writer.end() (Trivikram Kamat) [#64727](https://github.com/nodejs/node/pull/64727)
* \[[`ff12b8e22e`](https://github.com/nodejs/node/commit/ff12b8e22e)] - **stream**: use validateString for consumer encoding (Jungwon Sohn) [#64754](https://github.com/nodejs/node/pull/64754)
* \[[`cfad2efb06`](https://github.com/nodejs/node/commit/cfad2efb06)] - **stream**: use the ring buffer for pending BYOB pull-into descriptors (Matteo Collina) [#64818](https://github.com/nodejs/node/pull/64818)
* \[[`fe06bf56dc`](https://github.com/nodejs/node/commit/fe06bf56dc)] - **stream**: fix uncatchable error closing half-open Duplex.toWeb() writable (Mohamed Sayed) [#64161](https://github.com/nodejs/node/pull/64161)
* \[[`f2919dbb83`](https://github.com/nodejs/node/commit/f2919dbb83)] - **test**: unflake debugger and REPL tests (Matteo Collina) [#64718](https://github.com/nodejs/node/pull/64718)
* \[[`a1c29174e8`](https://github.com/nodejs/node/commit/a1c29174e8)] - **test**: ensure assertions are reached on all tests (Antoine du Hamel) [#64716](https://github.com/nodejs/node/pull/64716)
* \[[`b9e596f8e5`](https://github.com/nodejs/node/commit/b9e596f8e5)] - **test**: reuse ffi.suffix instead of reimplementing it (Seongeun Lee) [#64840](https://github.com/nodejs/node/pull/64840)
* \[[`c816918e14`](https://github.com/nodejs/node/commit/c816918e14)] - **test**: remove test-repl-user-error-handler from flaky (avivkeller) [#64631](https://github.com/nodejs/node/pull/64631)
* \[[`9d2f10ec54`](https://github.com/nodejs/node/commit/9d2f10ec54)] - **test**: update WPT for url to 4832db4761 (Node.js GitHub Bot) [#64829](https://github.com/nodejs/node/pull/64829)
* \[[`75b80d0b7b`](https://github.com/nodejs/node/commit/75b80d0b7b)] - **test**: update WPT for url to b63305b743 (Node.js GitHub Bot) [#64790](https://github.com/nodejs/node/pull/64790)
* \[[`9a139b3c86`](https://github.com/nodejs/node/commit/9a139b3c86)] - **test**: cover worker throwing primitive values (varshitha) [#64365](https://github.com/nodejs/node/pull/64365)
* \[[`796acc8920`](https://github.com/nodejs/node/commit/796acc8920)] - **test**: mark test-repl-user-error-handler as flaky (Aviv Keller) [#64612](https://github.com/nodejs/node/pull/64612)
* \[[`a646319f61`](https://github.com/nodejs/node/commit/a646319f61)] - **(SEMVER-MINOR)** **test\_runner**: add support for --test-coverage-include-all (avivkeller) [#64830](https://github.com/nodejs/node/pull/64830)
* \[[`4368303e01`](https://github.com/nodejs/node/commit/4368303e01)] - **test\_runner**: wait for filtered suite build (semimikoh) [#64208](https://github.com/nodejs/node/pull/64208)
* \[[`70d11241a3`](https://github.com/nodejs/node/commit/70d11241a3)] - **test\_runner**: convert to uint during deserialization (Aviv Keller) [#64706](https://github.com/nodejs/node/pull/64706)
* \[[`cafe7bffcc`](https://github.com/nodejs/node/commit/cafe7bffcc)] - **tls**: fix SNICallback certificate selection (Matteo Collina) [#64700](https://github.com/nodejs/node/pull/64700)
* \[[`9ee05ec40f`](https://github.com/nodejs/node/commit/9ee05ec40f)] - **tools**: bump the eslint group in /tools/eslint with 4 updates (dependabot\[bot]) [#64928](https://github.com/nodejs/node/pull/64928)
* \[[`5f4b859932`](https://github.com/nodejs/node/commit/5f4b859932)] - **tools**: bump brace-expansion from 5.0.7 to 5.0.9 in /tools/eslint (dependabot\[bot]) [#64904](https://github.com/nodejs/node/pull/64904)
* \[[`b5ced907b3`](https://github.com/nodejs/node/commit/b5ced907b3)] - **tools**: use 'readonly' for EventSource global (Honey Tyagi) [#64787](https://github.com/nodejs/node/pull/64787)
* \[[`fd4460e34e`](https://github.com/nodejs/node/commit/fd4460e34e)] - **typings**: add heap\_utils internalBinding types (Donghoon Kang) [#64816](https://github.com/nodejs/node/pull/64816)
* \[[`3bc0ee0492`](https://github.com/nodejs/node/commit/3bc0ee0492)] - **typings**: remove isDataView from types binding (Archkon) [#64738](https://github.com/nodejs/node/pull/64738)
* \[[`236d7ca965`](https://github.com/nodejs/node/commit/236d7ca965)] - **url**: create URLPattern result properties in WebIDL order (Archkon) [#64733](https://github.com/nodejs/node/pull/64733)
* \[[`3def577ab4`](https://github.com/nodejs/node/commit/3def577ab4)] - **v8**: report minor mark-sweep in GCProfiler (Archkon) [#64688](https://github.com/nodejs/node/pull/64688)
* \[[`5293abff73`](https://github.com/nodejs/node/commit/5293abff73)] - **vfs**: speed up recursive readdir test setup (Trivikram Kamat) [#64813](https://github.com/nodejs/node/pull/64813)
* \[[`4345185496`](https://github.com/nodejs/node/commit/4345185496)] - **vfs**: make lchown update symlink metadata (Trivikram Kamat) [#64573](https://github.com/nodejs/node/pull/64573)
* \[[`b6ab546de5`](https://github.com/nodejs/node/commit/b6ab546de5)] - **wasm**: register missing SetURL function (Archkon) [#64679](https://github.com/nodejs/node/pull/64679)
* \[[`f322870bd1`](https://github.com/nodejs/node/commit/f322870bd1)] - **zlib**: validate pledgedSrcSize as a safe integer (Archkon) [#64604](https://github.com/nodejs/node/pull/64604)
* \[[`44042c20d4`](https://github.com/nodejs/node/commit/44042c20d4)] - **zlib**: accept ArrayBuffer dictionary in Zstd (Ryuhei Shima) [#64599](https://github.com/nodejs/node/pull/64599)



## COMMIT SUBJECTS between the previous tag and the release

Working on v26.6.1
Revert "http2: avoid copying the options in respond()"
Revert "http2: avoid per-write closures in kWriteGeneric"
http2: reduce per-request allocations
http2: avoid per-write closures in kWriteGeneric
http2: avoid copying the options in respond()
zlib: accept ArrayBuffer dictionary in Zstd
diagnostics_channel: grow native channel storage
ffi: validate fast integer argument ranges
ffi: preserve uint8 semantics for bool fast calls
sqlite: fix use-after-free in Exec() and ApplyChangeset()
ffi: preserve strings during reentrant calls
http: propagate highWaterMark to ClientRequest OutgoingMessage
zlib: validate pledgedSrcSize as a safe integer
doc: run license-builder
src: fix libuv assertion on windows
src: avoid using ToLocalChecked in crypto_hash
deps: V8: backport c4d06ba586f3
build: perfetto-sdk
lib: add perfetto support
src: fix trace macro compatibility
src: rename legacy trace event headers
src: add perfetto trace agent
readline: reduce createInterface overhead
net: support AF_UNIX paths in net.BoundSocket
net: support TCP handle transfer on Windows
debugger: preserve overlapping CDP request state
doc: deprecation add more codemod
doc: update technical priorities
v8: report minor mark-sweep in GCProfiler
src: fix crash when writing odd-length hex string via Writev
crypto: use user-facing error for output encoding changes
buffer: validate copyArrayBuffer offsets against buffer length
loader: enforce path normalization before lookup
module: implement Symbol.dispose in ModuleHooks
sqlite: fix crash when a session outlives its database
stream: fix uncatchable error closing half-open Duplex.toWeb() writable
test: mark test-repl-user-error-handler as flaky
test_runner: convert to uint during deserialization
doc: mention constructor check in deepStrictEqual
quic: serialize stream reset code as string
deps: V8: backport 7d9b7e03141d
deps: update Rust crates for V8 14.6.202.34-node.26
build: bump rustc requirement to >=1.86
meta: add @nodejs/url as codeowner for node_url_pattern.*
typings: remove isDataView from types binding
vfs: make lchown update symlink metadata
url: create URLPattern result properties in WebIDL order
deps: update sqlite to 3.53.4
doc: add MDN links for explicit resource management in fs
doc: stabilize --disable-warning
buffer: use Clamp conversion in Blob slice
benchmark: fix calibrate-n option handling
test_runner: wait for filtered suite build
lib: fix typo in comment in _http_client.js
test: cover worker throwing primitive values
lib: fix AbortSignal.any() observed-composite leak
async_hooks: use validateBoolean for trackPromises
tools: use 'readonly' for EventSource global
meta: remove node_crates .gitignore
src: implement MemoryRetainer protocol for ByteSource
deps: update ada to 4.0.0
test: update WPT for url to b63305b743
doc: clarify tlsSocket.authorized on resumption
doc: document --permission-audit audit mode behavior
ffi: preserve link register in ppc64 trampoline
http: guard invalid timeout values in checkConnections
doc: use ffi.suffix for library paths in examples
doc: report proper return type on url.format
permission: support v8.setHeapSnapshotNearHeapLimit
fs: key glob matcher cache by platform
wasm: register missing SetURL function
ffi: fix optimized buffer conversions
ffi: validate fast 32-bit integer argument ranges
sqlite: check database state before calling SQLite
vfs: speed up recursive readdir test setup
doc: remove obsolete cctest node.gyp instructions
quic: fix segfault after fragmented client hello
test: update WPT for url to 4832db4761
stream: use the ring buffer for pending BYOB pull-into descriptors
test_runner: add support for --test-coverage-include-all
deps: V8: backport 5177b10891e6
test: remove test-repl-user-error-handler from flaky
stream: use validateString for consumer encoding
typings: add heap_utils internalBinding types
quic: fix coverage comment typo
doc: fix duplicated word in test snapshot docs
test: reuse ffi.suffix instead of reimplementing it
crypto: handle DH operation failures
crypto: initialize KeyObjectData mutex eagerly
crypto: handle XOF output allocation failure
crypto: fix Argon2 validation errors
crypto: validate key generation options
crypto: reuse X509 issuer result
crypto: clarify missing cipher error
stream: honor AbortSignal in Writer.end()
doc: mark config-file as release candidate
doc: add contributing detail for git Signed-off-by trailer
crypto: update root certificates to NSS 3.125
doc: document stream.isDestroyed()
permission: add unique warning codes
src: fix perfetto build on GetTraceFilePath
src,test: disable trace events tests when perfetto is enabled
build: fix v8_use_perfetto source scraping
build: run perfetto build and test on GHA
doc: add missing float32/float64 FFI type names
ffi: reject fast calls after library close
deps: update zlib to 1.3.2.1-motley-42c2f19
ffi: fix crash in refCallback and unrefCallback
stream: skip zero-byte broadcast writes
doc: improve TestContext hook descriptions
build,tools: fix shared library cross-compile
tools: bump brace-expansion from 5.0.7 to 5.0.9 in /tools/eslint
crypto: fix Argon2 bypassing FIPS mode
crypto: preserve OpenSSL errors from KDF failures
doc: fix missing references in doc type map
doc: fix typos in documentation
tls: fix SNICallback certificate selection
doc: add RafaelGSS as last security release stewards
doc: fix typo in maintaining-dependencies.md
test: ensure assertions are reached on all tests
http: avoid aborting IncomingMessage signal on normal close
crypto: support loading private keys through STORE loaders
test: unflake debugger and REPL tests
meta: bump ossf/scorecard-action from 2.4.3 to 2.4.4
meta: bump step-security/harden-runner from 2.19.4 to 2.20.0
meta: bump github/codeql-action/upload-sarif from 4.36.2 to 4.37.3
tools: bump the eslint group in /tools/eslint with 4 updates
meta: bump cachix/install-nix-action from 31.10.6 to 31.11.0
meta: bump Mozilla-Actions/sccache-action from 0.0.10 to 0.0.11
meta: bump github/codeql-action/init from 4.36.2 to 4.37.3
meta: bump actions/setup-python from 6.3.0 to 7.0.0
meta: bump github/codeql-action/autobuild from 4.36.2 to 4.37.3
meta: bump github/codeql-action/analyze from 4.36.2 to 4.37.3
meta: bump actions/stale from 10.3.0 to 11.0.0
sqlite: invalidate sessions when closing database
doc: remove references to `ca`/`crl` as per-context QuicSession options
deps: update nghttp2 to 1.70.0
deps: update googletest to 1b6f64d659944658a4c685b7bd9f04c1c3b8a39b
deps: update acorn to 8.18.0
deps: update simdjson to 4.6.6
deps: update minimatch to 10.2.6
doc: formalize fn/name as part of TestOptions API
stream: preserve push signal abort reason
quic: fix stop sending behaviour & callback
http: fix writableFinished and 'finish' after write errors
doc: fix grammar and editorial issues in addons documentation
deps: update nghttp3 to 1.18.0
deps: update ngtcp2 to 1.25.0
deps: upgrade npm to 11.19.0
stream: cut per-chunk allocations in pipeTo
doc: fix grammar and punctuation in dgram documentation
2026-08-05, Version 26.7.0 (Current)

# CANDIDATE A

# Node.js v26.7.0 (Current)

## Notable changes

- **crypto:** Private keys can now be loaded through OpenSSL STORE loaders by passing a URL as the key. A new `properties` option is available. ([#63949](https://github.com/nodejs/node/pull/63949))
  - Under the permission model this is blocked unless you pass the new `--allow-openssl-store` flag.
- **crypto:** Root certificates are updated to NSS 3.125. ([#64746](https://github.com/nodejs/node/pull/64746))
- **Perfetto tracing:** Node.js can now be built with Perfetto support (`--with-perfetto`). It writes `.pftrace` trace files that you can open in ui.perfetto.dev. ([#64565](https://github.com/nodejs/node/pull/64565))
  - When Perfetto is enabled, inspector trace support is disabled.
- **module:** Hooks returned by `module.registerHooks()` now implement `Symbol.dispose`, which works like `deregister()`. ([#63928](https://github.com/nodejs/node/pull/63928))
- **test_runner:** The new experimental `--test-coverage-include-all` flag reports source files that no test loaded as having zero coverage. ([#64830](https://github.com/nodejs/node/pull/64830))

## Other features and changes

- **cli:** `--disable-warning` is now stable. ([#64742](https://github.com/nodejs/node/pull/64742))
- **config:** The configuration file feature is now marked as a release candidate. ([#64516](https://github.com/nodejs/node/pull/64516))
- **net:** `net.BoundSocket` now supports Unix domain socket and named pipe paths through a new `path` option. ([#64399](https://github.com/nodejs/node/pull/64399))
  - `boundSocket.isPipe` is new, and `address()` returns the path for pipe binds.
- **net:** TCP handles can now be transferred to workers on Windows. ([#64460](https://github.com/nodejs/node/pull/64460))
- **permission:** Permission-related security warnings now have unique `PERM` codes so they can be silenced individually. ([#64414](https://github.com/nodejs/node/pull/64414))
- **permission:** `v8.setHeapSnapshotNearHeapLimit()` is now supported under the permission model. ([#64808](https://github.com/nodejs/node/pull/64808))
- **zlib:** The Zstd `dictionary` option now accepts an `ArrayBuffer`, `DataView` or other typed array. ([#64599](https://github.com/nodejs/node/pull/64599))
- **v8:** `GCProfiler` now reports minor mark-sweep collections. ([#64688](https://github.com/nodejs/node/pull/64688))
- **http:** The `highWaterMark` option of `http.request()` is now also applied to the outgoing message before a socket is connected. ([#64653](https://github.com/nodejs/node/pull/64653))
- **url:** `URLPattern` result properties are now created in WebIDL order. ([#64733](https://github.com/nodejs/node/pull/64733))
- **vfs:** `lchown` now updates symlink metadata. ([#64573](https://github.com/nodejs/node/pull/64573))

## Bug fixes

- **crypto:** Argon2 no longer bypasses FIPS mode. ([#64776](https://github.com/nodejs/node/pull/64776))
- **crypto:** OpenSSL errors from KDF failures are now preserved. ([#64776](https://github.com/nodejs/node/pull/64776))
- **crypto:** Argon2 validation errors, key generation option validation and the missing-cipher error message are fixed or clearer. ([#64852](https://github.com/nodejs/node/pull/64852))
- **crypto:** Failures in Diffie-Hellman operations and XOF output allocation are now handled instead of crashing. ([#64851](https://github.com/nodejs/node/pull/64851))
- **crypto:** Changing the output encoding now throws a user-facing error. ([#64692](https://github.com/nodejs/node/pull/64692))
- **tls:** Fix certificate selection when using `SNICallback`. ([#64700](https://github.com/nodejs/node/pull/64700))
- **http:** `IncomingMessage.signal` is no longer aborted when the message completes normally. ([#64392](https://github.com/nodejs/node/pull/64392))
- **http:** Fix `writableFinished` and the `'finish'` event after write errors. ([#64847](https://github.com/nodejs/node/pull/64847))
- **http:** Invalid timeout values no longer break `checkConnections`. ([#64506](https://github.com/nodejs/node/pull/64506))
- **stream:** Preserve the abort reason of `push` signals. ([#64798](https://github.com/nodejs/node/pull/64798))
- **stream:** `Writer.end()` now honors an `AbortSignal`. ([#64727](https://github.com/nodejs/node/pull/64727))
- **stream:** Fix an uncatchable error when closing the writable side of a half-open `Duplex.toWeb()`. ([#64161](https://github.com/nodejs/node/pull/64161))
- **stream:** Zero-byte broadcast writes are now skipped. ([#64772](https://github.com/nodejs/node/pull/64772))
- **stream:** Consumer encoding is now validated as a string. ([#64754](https://github.com/nodejs/node/pull/64754))
- **quic:** Fix stop-sending behavior and its callback. ([#64710](https://github.com/nodejs/node/pull/64710))
- **quic:** Fix a segfault after a fragmented client hello. ([#64720](https://github.com/nodejs/node/pull/64720))
- **quic:** Stream reset codes are now serialized as strings. ([#64577](https://github.com/nodejs/node/pull/64577))
- **sqlite:** Fix crashes and use-after-free bugs when sessions outlive their database, in `exec()` and in `applyChangeset()`. ([#63797](https://github.com/nodejs/node/pull/63797), [#64535](https://github.com/nodejs/node/pull/64535))
- **sqlite:** Sessions are now invalidated when the database closes, and the database state is checked before calling SQLite. ([#64783](https://github.com/nodejs/node/pull/64783), [#64812](https://github.com/nodejs/node/pull/64812))
- **ffi:** Fix crashes in `refCallback` and `unrefCallback`. ([#64881](https://github.com/nodejs/node/pull/64881))
- **ffi:** Fast calls are now rejected after the library is closed. ([#64860](https://github.com/nodejs/node/pull/64860))
- **ffi:** Fast-call integer arguments are now range-checked, and `bool` keeps `uint8` semantics. ([#64614](https://github.com/nodejs/node/pull/64614), [#64691](https://github.com/nodejs/node/pull/64691), [#64527](https://github.com/nodejs/node/pull/64527))
- **ffi:** Fix optimized buffer conversions, strings during reentrant calls, and the ppc64 trampoline. ([#64639](https://github.com/nodejs/node/pull/64639), [#64551](https://github.com/nodejs/node/pull/64551), [#64792](https://github.com/nodejs/node/pull/64792))
- **buffer:** Validate `copyArrayBuffer` offsets against the buffer length. ([#63904](https://github.com/nodejs/node/pull/63904))
- **buffer:** `Blob.slice()` now clamps its arguments. ([#64739](https://github.com/nodejs/node/pull/64739))
- **src:** Fix a crash when writing an odd-length hex string through `writev`. ([#63658](https://github.com/nodejs/node/pull/63658))
- **src:** Fix a libuv assertion failure on Windows. ([#61999](https://github.com/nodejs/node/pull/61999))
- **module:** Path normalization is now enforced before package map lookups. ([#63917](https://github.com/nodejs/node/pull/63917))
- **lib:** Fix a memory leak with `AbortSignal.any()` composite signals. ([#64481](https://github.com/nodejs/node/pull/64481))
- **async_hooks:** `trackPromises` is now validated as a boolean. ([#64731](https://github.com/nodejs/node/pull/64731))
- **zlib:** `pledgedSrcSize` is now validated as a safe integer. ([#64604](https://github.com/nodejs/node/pull/64604))
- **fs:** The glob matcher cache is now keyed by platform. ([#64571](https://github.com/nodejs/node/pull/64571))
- **wasm:** Register the missing `SetURL` function. ([#64679](https://github.com/nodejs/node/pull/64679))
- **debugger:** Preserve overlapping CDP request state. ([#64467](https://github.com/nodejs/node/pull/64467))
- **test_runner:** Wait for filtered suites to be built, and convert to uint during deserialization. ([#64208](https://github.com/nodejs/node/pull/64208), [#64706](https://github.com/nodejs/node/pull/64706))
- **diagnostics_channel:** Native channel storage now grows as needed. ([#64497](https://github.com/nodejs/node/pull/64497))

## Performance

- **stream:** Fewer per-chunk allocations in `pipeTo`, and BYOB pull-into descriptors use a ring buffer. ([#64890](https://github.com/nodejs/node/pull/64890), [#64818](https://github.com/nodejs/node/pull/64818))
- **readline:** Lower overhead when calling `createInterface`. ([#64585](https://github.com/nodejs/node/pull/64585))

## Dependencies

- npm 11.19.0 ([#64883](https://github.com/nodejs/node/pull/64883))
- ada 4.0.0 ([#64790](https://github.com/nodejs/node/pull/64790))
- ngtcp2 1.25.0, nghttp3 1.18.0, nghttp2 1.70.0 ([#64944](https://github.com/nodejs/node/pull/64944), [#64943](https://github.com/nodejs/node/pull/64943), [#64939](https://github.com/nodejs/node/pull/64939))
- SQLite 3.53.4 ([#64745](https://github.com/nodejs/node/pull/64745))
- zlib 1.3.2.1-motley-42c2f19 ([#64744](https://github.com/nodejs/node/pull/64744))
- acorn 8.18.0, minimatch 10.2.6, simdjson 4.6.6 ([#64941](https://github.com/nodejs/node/pull/64941), [#64945](https://github.com/nodejs/node/pull/64945), [#64942](https://github.com/nodejs/node/pull/64942))
- V8 backports and updated Rust crates ([#64543](https://github.com/nodejs/node/pull/64543), [#64631](https://github.com/nodejs/node/pull/64631), [#63731](https://github.com/nodejs/node/pull/63731))

## Other

- **build:** The minimum supported Rust version is now 1.86. ([#64543](https://github.com/nodejs/node/pull/64543))
- **build:** Fix shared library cross-compilation and Perfetto builds, and run Perfetto builds in CI. ([#63963](https://github.com/nodejs/node/pull/63963), [#64721](https://github.com/nodejs/node/pull/64721))
- **doc:** Many documentation fixes and improvements, including FFI type names, `stream.isDestroyed()`, permission audit mode, and codemod links for deprecations.
- **test:** Test fixes, unflaking, and WPT updates for `url`.
- **meta, tools:** GitHub Actions and ESLint dependency bumps, and codeowner updates.
- **typings, src:** Internal typings and `MemoryRetainer` improvements.


# CANDIDATE B

# Node.js v26.7.0 (Current)

## Notable changes

- **Private keys from OpenSSL STORE loaders.** `crypto.createPrivateKey()` and other APIs that take private keys can now load keys from a `URL` through OpenSSL STORE loaders ([#63949](https://github.com/nodejs/node/pull/63949)).
- **New `--allow-openssl-store` permission flag.** When the Permission Model is on, STORE loaders are blocked unless you pass this flag.
- **Coverage for unloaded files.** The new `--test-coverage-include-all` test runner option reports source files the tests never loaded as having zero coverage ([#64830](https://github.com/nodejs/node/pull/64830)).
- **Perfetto tracing (opt-in at build time).** Node.js can be built with `--with-perfetto` to write Perfetto `.pftrace` traces ([#64565](https://github.com/nodejs/node/pull/64565)). Inspector trace support is disabled in those builds.
- **Unix socket paths in `net.BoundSocket`.** `net.BoundSocket` accepts a `path` option to bind a Unix domain socket or Windows pipe synchronously ([#64399](https://github.com/nodejs/node/pull/64399)).
- **Unique warning codes for permission warnings.** Permission `SecurityWarning`s now have codes like `PERM0002`, so you can silence them one at a time with `--disable-warning` ([#64414](https://github.com/nodejs/node/pull/64414)).
- **Stability changes.** `--disable-warning` is now Stable ([#64742](https://github.com/nodejs/node/pull/64742)), and the config file feature is now a release candidate ([#64516](https://github.com/nodejs/node/pull/64516)).

## Features

- **crypto:** Load private keys through OpenSSL STORE loaders ([#63949](https://github.com/nodejs/node/pull/63949)).
- **test_runner:** Add `--test-coverage-include-all` ([#64830](https://github.com/nodejs/node/pull/64830)).
- **net:** Support Unix socket paths in `net.BoundSocket` ([#64399](https://github.com/nodejs/node/pull/64399)).
- **net:** Support TCP handle transfer on Windows ([#64460](https://github.com/nodejs/node/pull/64460)).
- **permission:** Add unique warning codes ([#64414](https://github.com/nodejs/node/pull/64414)).
- **permission:** Check permissions in `v8.setHeapSnapshotNearHeapLimit()` ([#64808](https://github.com/nodejs/node/pull/64808)).
- **module:** `ModuleHooks` now implements `Symbol.dispose` ([#63928](https://github.com/nodejs/node/pull/63928)).
- **zlib:** Zstd accepts an `ArrayBuffer` as a dictionary ([#64599](https://github.com/nodejs/node/pull/64599)).
- **v8:** `GCProfiler` reports minor mark-sweep collections ([#64688](https://github.com/nodejs/node/pull/64688)).
- **http:** `ClientRequest` passes `highWaterMark` on to its output buffer ([#64653](https://github.com/nodejs/node/pull/64653)).
- **build:** Add the `--with-perfetto` build option and Perfetto trace support ([#64565](https://github.com/nodejs/node/pull/64565)).

## Fixes

- **crypto:** Argon2 no longer works when FIPS mode should block it ([#64776](https://github.com/nodejs/node/pull/64776)).
- **crypto:** Argon2, HKDF, PBKDF2 and scrypt failures keep their OpenSSL error `code` and error stack ([#64776](https://github.com/nodejs/node/pull/64776)).
- **crypto:** Fix Argon2 validation errors, key generation option validation, and some error messages ([#64852](https://github.com/nodejs/node/pull/64852)).
- **crypto:** Handle failures in DH operations and XOF output allocation instead of crashing ([#64851](https://github.com/nodejs/node/pull/64851)).
- **crypto:** Use a user-facing error when output encoding is changed ([#64692](https://github.com/nodejs/node/pull/64692)).
- **tls:** Fix certificate selection in `SNICallback` ([#64700](https://github.com/nodejs/node/pull/64700)).
- **http:** `writableFinished` and `'finish'` are now correct after write errors ([#64847](https://github.com/nodejs/node/pull/64847)).
- **http:** `IncomingMessage`'s signal is no longer aborted on a normal close ([#64392](https://github.com/nodejs/node/pull/64392)).
- **http:** Invalid timeout values no longer break `checkConnections` ([#64506](https://github.com/nodejs/node/pull/64506)).
- **quic:** Fix stop-sending behavior and its callback ([#64710](https://github.com/nodejs/node/pull/64710)).
- **quic:** Fix a segfault after a fragmented client hello ([#64720](https://github.com/nodejs/node/pull/64720)).
- **quic:** Stream reset codes are now serialized as strings ([#64577](https://github.com/nodejs/node/pull/64577)).
- **sqlite:** Fix crashes and use-after-free bugs involving sessions, `exec()` and `applyChangeset()` ([#63797](https://github.com/nodejs/node/pull/63797), [#64535](https://github.com/nodejs/node/pull/64535), [#64783](https://github.com/nodejs/node/pull/64783)).
- **sqlite:** Check database state before calling SQLite ([#64812](https://github.com/nodejs/node/pull/64812)).
- **ffi:** Fix crashes in `refCallback` and `unrefCallback`, and reject fast calls after a library is closed ([#64881](https://github.com/nodejs/node/pull/64881), [#64860](https://github.com/nodejs/node/pull/64860)).
- **ffi:** Fix integer argument range checks, `bool` handling, buffer conversions, and strings during reentrant calls on fast calls ([#64614](https://github.com/nodejs/node/pull/64614), [#64691](https://github.com/nodejs/node/pull/64691), [#64527](https://github.com/nodejs/node/pull/64527), [#64639](https://github.com/nodejs/node/pull/64639), [#64551](https://github.com/nodejs/node/pull/64551)).
- **ffi:** Preserve the link register in the ppc64 trampoline ([#64792](https://github.com/nodejs/node/pull/64792)).
- **stream:** Fix an uncatchable error when closing a half-open `Duplex.toWeb()` writable ([#64161](https://github.com/nodejs/node/pull/64161)).
- **stream:** Keep the abort reason from `push` signals, honor `AbortSignal` in `Writer.end()`, and skip zero-byte broadcast writes ([#64798](https://github.com/nodejs/node/pull/64798), [#64727](https://github.com/nodejs/node/pull/64727), [#64772](https://github.com/nodejs/node/pull/64772)).
- **stream:** Validate the consumer encoding with `validateString` ([#64754](https://github.com/nodejs/node/pull/64754)).
- **lib:** Fix a memory leak in `AbortSignal.any()` ([#64481](https://github.com/nodejs/node/pull/64481)).
- **module:** Normalize paths before lookup so `createRequire()` works with package maps ([#63917](https://github.com/nodejs/node/pull/63917)).
- **buffer:** Validate `copyArrayBuffer` offsets and clamp `Blob.slice()` arguments ([#63904](https://github.com/nodejs/node/pull/63904), [#64739](https://github.com/nodejs/node/pull/64739)).
- **src:** Fix a crash when writing an odd-length hex string through `writev` ([#63658](https://github.com/nodejs/node/pull/63658)).
- **zlib:** Validate `pledgedSrcSize` as a safe integer ([#64604](https://github.com/nodejs/node/pull/64604)).
- **fs:** Cache glob matchers per platform ([#64571](https://github.com/nodejs/node/pull/64571)).
- **url:** Create `URLPattern` result properties in WebIDL order ([#64733](https://github.com/nodejs/node/pull/64733)).
- **async_hooks:** Validate the `trackPromises` option as a boolean ([#64731](https://github.com/nodejs/node/pull/64731)).
- **test_runner:** Wait for filtered suites to build, and fix uint conversion when deserializing ([#64208](https://github.com/nodejs/node/pull/64208), [#64706](https://github.com/nodejs/node/pull/64706)).
- **debugger:** Keep state for overlapping CDP requests ([#64467](https://github.com/nodejs/node/pull/64467)).
- **wasm:** Register the missing `SetURL` function ([#64679](https://github.com/nodejs/node/pull/64679)).
- **diagnostics_channel:** Grow native channel storage as needed ([#64497](https://github.com/nodejs/node/pull/64497)).
- **vfs:** `lchown` now updates symlink metadata ([#64573](https://github.com/nodejs/node/pull/64573)).
- **src:** Fix a libuv assertion on Windows ([#61999](https://github.com/nodejs/node/pull/61999)).

## Performance

- **stream:** `pipeTo` allocates less per chunk ([#64890](https://github.com/nodejs/node/pull/64890)).
- **stream:** Pending BYOB pull-into descriptors use a ring buffer ([#64818](https://github.com/nodejs/node/pull/64818)).
- **http2:** Fewer allocations per request ([#64265](https://github.com/nodejs/node/pull/64265)).
- **readline:** Lower `createInterface` overhead ([#64585](https://github.com/nodejs/node/pull/64585)).

## Dependencies

- ada 4.0.0 ([#64790](https://github.com/nodejs/node/pull/64790)).
- npm 11.19.0 ([#64883](https://github.com/nodejs/node/pull/64883)).
- ngtcp2 1.25.0 and nghttp3 1.18.0 ([#64944](https://github.com/nodejs/node/pull/64944), [#64943](https://github.com/nodejs/node/pull/64943)).
- nghttp2 1.70.0 ([#64939](https://github.com/nodejs/node/pull/64939)).
- SQLite 3.53.4 ([#64745](https://github.com/nodejs/node/pull/64745)).
- zlib 1.3.2.1-motley-42c2f19 ([#64744](https://github.com/nodejs/node/pull/64744)).
- acorn 8.18.0, minimatch 10.2.6, simdjson 4.6.6 ([#64941](https://github.com/nodejs/node/pull/64941), [#64945](https://github.com/nodejs/node/pull/64945), [#64942](https://github.com/nodejs/node/pull/64942)).
- Root certificates updated to NSS 3.125 ([#64746](https://github.com/nodejs/node/pull/64746)).
- V8 patches backported ([#63731](https://github.com/nodejs/node/pull/63731), [#64543](https://github.com/nodejs/node/pull/64543), [#64631](https://github.com/nodejs/node/pull/64631)).

## Other

- **Build:** Building now needs Rust 1.86 or later ([#64541](https://github.com/nodejs/node/pull/64541)). Shared-library cross-compiling is fixed ([#63963](https://github.com/nodejs/node/pull/63963)), and Perfetto builds run in CI.
- **Docs:** Documentation fixes and additions, including `--permission-audit` behavior, `stream.isDestroyed()`, FFI type names, and `TestOptions`.
- **Tests, CI and tooling:** Flaky test fixes, WPT updates, GitHub Actions and ESLint dependency bumps, and typings updates.
- **Internal:** `ByteSource` implements the MemoryRetainer protocol ([#64660](https://github.com/nodejs/node/pull/64660)), and `ToLocalChecked` is no longer used in `crypto_hash` ([#64668](https://github.com/nodejs/node/pull/64668)).

