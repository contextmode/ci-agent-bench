# Judge file r1-valkey-9.0.7

## PUBLISHED RELEASE NOTES (written by the maintainers)

Valkey 9.0.7  -  Released Mon 26 October 2026
---------------------------------------------

Upgrade urgency SECURITY: This release includes security fixes we recommend you apply as soon as possible.

### Security Fixes
* GHSA-f4q9-j22m-xqq9: Fix a heap buffer overflow in cluster Pub/Sub message construction that could allow an authenticated client to potentially execute arbitrary code by publishing an oversized message by @roshkhatri (#5030)

### Bug Fixes
* Fix stream commands that mutate consumer-group or PEL state (`XGROUP`, `XSETID`, `XREADGROUP`, `XACK`, `XCLAIM`, `XAUTOCLAIM`) not triggering `WATCH` and client-side tracking invalidation by @Tarte12 (#3459)
* Reject module write commands while the server is paused for writes, preventing a crash from module timer callbacks during `CLIENT PAUSE WRITE` or `CLUSTER FAILOVER` by @smkher (#3645)
* Fix a server abort on a RESTORE payload declaring a string length that overflows the allocation size; such payloads are now rejected as bad data by @enjoy-binbin (#4733)
* Fix ZINTER/ZINTERSTORE returning input-order-dependent scores when a weighted term is 0*inf; a NaN weighted score now counts as 0, matching ZUNION by @leomurillo (#4997)
* Correct `ValkeyModule_FreeModuleUser`, `ValkeyModule_ACLAddLogEntry` and `ValkeyModule_ACLAddLogEntryByUserName` declarations to return int as implemented, fixing undefined behavior on targets with strict call signature checks by @rainsupreme (#4676)
* valkey-check-aof now recognizes RDB base files with the `VALKEY` signature instead of misreporting a valid multipart AOF as invalid by @sarthakaggarwal97 (#4739)
* Fix a huge memory allocation when a command such as COMMAND GETKEYS EVAL declares a far larger key count than the arguments provided by @murphyjacob4 (#3598)
* Reject relative expire times in `SET`/`GETEX`, `RESTORE`, and `ValkeyModule_SetExpire` that overflow when added to the current time, preventing server aborts from negative expires by @madolson (#4880)
* `HDEL`, `HGETDEL`, `HPERSIST`, and `HEXPIRE` no longer propagate fields they treat as expired, preventing replica and AOF-reload divergence by @xdk-amz (#4772)
* Fix a server crash when loading an ACL file containing a selector with an unmatched parenthesis by @magic-peach (#4214)
* `COPY` of a hash now includes expired-but-unreaped fields so their deletion is propagated and replicas stay in sync by @pirate329 (#4939)
* Sorted set range commands with a negative `LIMIT` offset now return an empty result instead of a spurious element on btree-encoded keys by @xiaocj (#4637)
* Fix atomic slot migration not replicating evictions on the import target, which let replicas grow far past `maxmemory` by @shanezx-sc (#4920)
* Redact error text in server logs when `hide-user-data-from-log` is enabled, so command arguments no longer leak into logs by @zackcam (#4815)
* Fix `HSETEX` and `HGETEX` failing to parse their arguments when the key is named `fields` by @sebxt (#4945)
* Fix cluster config saving to avoid publishing truncated `nodes.conf` files, losing the startup lock after the first save, and failing every save on SMB filesystems such as Azure Files; the lock now lives on a separate `nodes.conf.lock` file by @KewangZhili (#4489)
* Fix atomic slot migration with `cluster-databases` > 1 applying writes made during the snapshot to the wrong database on the target by @pirate329 (#4952)
* Fix `LSET` on 64-bit builds silently modifying the wrong element for out-of-range indexes instead of returning an index out of range error by @charsyam (#4823)

**Full Changelog**: https://github.com/valkey-io/valkey/compare/9.0.6...9.0.7


## COMMIT SUBJECTS between the previous tag and the release

Fix missing signalModifiedKey calls for stream commands (#3459)
Move build-debian-old CI job to Debian Bookworm (#4613)
Fix return types of three module API declarations to match definitions (#4676)
Persist OPENSSL_PREFIX across builds (#4738)
Fix valkey-check-aof detection of Valkey RDB base files (#4739)
Repair backport validation failure
Fix valkey-benchmark spin on would-block writes (#4567)
fix: Reject module writes during client pause to prevent crash (#3645)
Repair backport validation failure
fix: validate key count before allocating result in keyspec (#3598)
Reject relative expires that overflow when the base time is added (#4880)
Fix flaky multi-part AOF manifest tests (#4491)
Fix wait for slot migration completion before checking DBSIZE (#4366)
Avoid propagating expired hash fields from HDEL, HGETDEL, HPERSIST, and HEXPIRE (#4772)
Repair backport validation failure
fix(acl): prevent NULL pointer dereference on malformed selector in ACL file (#4214)
Fix test_reclaimFilePageCache to avoid tmpfs (#4362)
Fix sds overflow assert on RESTORE payload with an overflowing string length (#4733)
Copy expired-but-unreaped fields in hashTypeDup (#4939)
Return empty result for a negative LIMIT offset in zset range commands (#4637)
Fix eviction replication and replica DB selection during atomic slot migration (#4920)
CI: avoid installing LTTng kernel modules in UST job (#4967)
Redacting when hide_user_data_from_log is set for after error reply (#4815)
Fix HSETEX and HGETEX when the key is named "fields" (#4945)
CI: update FreeBSD daily test image (#4922)
Hold no descriptor on nodes.conf when rename() publishes it (#4489)
Fix runtest-moduleapi module linking on macOS
Fix ZINTER/ZINTERSTORE score when a weighted term is 0*inf (#4997)
Send SELECT at the end of the slot migration snapshot (#4952)
CI: allow SELECTs in spellcheck
Fix CI failures on clang-format due to OS changes on the runner Image (#5029)
[correctness] Fix LSET modifying elements for out-of-range 64-bit indexes (#4823)
CI: stabilize release jobs on Ubuntu 24.04
CI: support ubuntu-latest runner updates
CI: run clang-format check on ubuntu-latest
Fix cluster Pub/Sub length truncation (#5030)
Add release notes entry for Valkey 9.0.7 (#5051)

# CANDIDATE A

# Valkey 9.0.7

Upgrade urgency: **SECURITY**. This release fixes a cluster Pub/Sub message-size problem and several crashes on malformed or extreme input, so we recommend upgrading.

## Security fixes

* Reject cluster `PUBLISH` and `SPUBLISH` messages too large for the cluster bus, instead of silently truncating the length field. [#5030](https://github.com/valkey-io/valkey/pull/5030)

## Behavior changes

* In cluster mode, `PUBLISH` and `SPUBLISH` now return the error `Publish message is too large for the cluster bus` when the channel plus message exceed the cluster bus limit (about 4 GB). [#5030](https://github.com/valkey-io/valkey/pull/5030)
* The cluster config file is now locked through a separate `<cluster-config-file>.lock` file (for example `nodes-6379.conf.lock`) in the same directory. [#4489](https://github.com/valkey-io/valkey/pull/4489)
  * The lock file must stay creatable and must not be deleted while the node runs. Container mounts and cleanup jobs that only handle `nodes.conf` need to allow for it.
  * Pointing two nodes at one config file through a symlink or hard link is not supported.

## Bug fixes

### Crashes and invalid input
* Fix a crash when module timer callbacks or thread-safe contexts write while the server is paused for writes; those writes are now rejected with an error. [#3645](https://github.com/valkey-io/valkey/pull/3645)
* Fix a server abort when a corrupt `RESTORE` payload declares a string length that overflows; it is now rejected as bad data. [#4733](https://github.com/valkey-io/valkey/pull/4733)
* Fix relative expire times in `SET`/`GETEX`, `RESTORE`, and `ValkeyModule_SetExpire` overflowing when added to the current time, which could crash the server. [#4880](https://github.com/valkey-io/valkey/pull/4880)
* Fix a crash when loading an ACL file with a selector that has unmatched parentheses. [#4214](https://github.com/valkey-io/valkey/pull/4214)
* Fix a huge memory allocation in `COMMAND GETKEYS` when a command such as `EVAL` declares an excessive key count. [#3598](https://github.com/valkey-io/valkey/pull/3645)

### Commands and data correctness
* Fix `LSET` on 64-bit builds changing the wrong element instead of returning an out-of-range error for indexes beyond 32 bits. [#4823](https://github.com/valkey-io/valkey/pull/4823)
* Fix `ZINTER`/`ZINTERSTORE` returning order-dependent scores when a weighted score is 0*inf; it now counts as 0, matching `ZUNION`. [#4997](https://github.com/valkey-io/valkey/pull/4997)
* Fix sorted-set range commands returning a wrong element on large sorted sets when `LIMIT` has a negative offset; they now return an empty result. [#4637](https://github.com/valkey-io/valkey/pull/4637)
* Fix `HSETEX` and `HGETEX` failing to parse arguments when the key is named `fields`. [#4945](https://github.com/valkey-io/valkey/pull/4945)
* Fix stream commands (`XGROUP`, `XSETID`, `XREADGROUP`, `XACK`, `XCLAIM`, `XAUTOCLAIM`) not triggering `WATCH` and client-side tracking invalidation. [#3459](https://github.com/valkey-io/valkey/pull/3459)

### Replication and hash fields
* Fix `HDEL`, `HGETDEL`, `HPERSIST`, and `HEXPIRE` propagating already-expired hash fields, which could make replicas and AOF-reloaded data differ from the primary. [#4772](https://github.com/valkey-io/valkey/pull/4772)
* Fix `COPY` of a hash dropping expired-but-not-yet-deleted fields, which left stale fields on replicas. [#4939](https://github.com/valkey-io/valkey/pull/4939)

### Cluster and slot migration
* Fix evictions on an atomic slot migration target not being replicated, which could let replicas grow far past `maxmemory`. [#4920](https://github.com/valkey-io/valkey/pull/4920)
* Fix writes made during an atomic slot migration snapshot being applied to the wrong database on the target when `cluster-databases` is greater than 1. [#4952](https://github.com/valkey-io/valkey/pull/4952)
* Fix cluster config saving: a failed write can no longer replace a good `nodes.conf` with a truncated one, the startup lock is no longer lost after the first save, and saves no longer fail on SMB filesystems such as Azure Files. [#4489](https://github.com/valkey-io/valkey/pull/4489)

### Logging
* Redact error reply text in server logs when `hide-user-data-from-log` is enabled, so keys and values no longer leak into the log. [#4815](https://github.com/valkey-io/valkey/pull/4815)

### Tools and modules
* Fix `valkey-check-aof` not recognizing RDB base files with the `VALKEY` signature, which made healthy multipart AOFs look invalid. [#4739](https://github.com/valkey-io/valkey/pull/4739)
* Fix `valkey-benchmark` spinning on would-block writes, which could starve reply processing and the `--duration` timer. [#4567](https://github.com/valkey-io/valkey/pull/4567)
* Fix the declared return types of `ValkeyModule_FreeModuleUser`, `ValkeyModule_ACLAddLogEntry`, and `ValkeyModule_ACLAddLogEntryByUserName` to match their implementations. [#4676](https://github.com/valkey-io/valkey/pull/4676)

## Build

* Remember `OPENSSL_PREFIX` between builds, so it no longer has to be passed again. [#4738](https://github.com/valkey-io/valkey/pull/4738)
* Fix linking of module API test modules on macOS.
* `utils/create-cluster clean` now also removes `nodes-*.conf.lock` files. [#4489](https://github.com/valkey-io/valkey/pull/4489)

## Other

* CI: update the FreeBSD daily image, move the old-Debian job to Bookworm, avoid installing LTTng kernel modules in the UST job, and adapt workflows and clang-format checks to the `ubuntu-latest` runner change. [#4922](https://github.com/valkey-io/valkey/pull/4922), [#4613](https://github.com/valkey-io/valkey/pull/4613), [#4967](https://github.com/valkey-io/valkey/pull/4967), [#5029](https://github.com/valkey-io/valkey/pull/5029)
* Tests: fix flaky multipart AOF manifest and slot migration tests, avoid tmpfs in the page-cache reclaim test, and allow `SELECTs` in the spellcheck config. [#4491](https://github.com/valkey-io/valkey/pull/4491), [#4366](https://github.com/valkey-io/valkey/pull/4366), [#4362](https://github.com/valkey-io/valkey/pull/4362)
* Add a `DEBUG CLUSTER-PUBLISH-MESSAGE-LIMIT` subcommand used for testing. [#5030](https://github.com/valkey-io/valkey/pull/5030)
* Version bump and release notes for 9.0.7. [#5051](https://github.com/valkey-io/valkey/pull/5051)


# CANDIDATE B

# Valkey 9.0.7

Upgrade urgency: **SECURITY** for cluster deployments. This release fixes a heap buffer overflow in cluster Pub/Sub. It also fixes several crashes and data-consistency bugs.

## Security fixes

* Fix a heap buffer overflow in cluster `PUBLISH` and `SPUBLISH` when the channel and message are very large. Oversized requests are now rejected before anything is published. ([#5030](https://github.com/valkey-io/valkey/pull/5030))

## Bug fixes

### Commands and data types

* Fix `LSET` changing the wrong element when given a very large index, such as `4294967296`. It now returns `ERR index out of range`. ([#4823](https://github.com/valkey-io/valkey/pull/4823))
* Fix `ZINTER` and `ZINTERSTORE` returning wrong scores when a weighted score on a later input is `0*inf`. ([#4997](https://github.com/valkey-io/valkey/pull/4997))
* Return an empty result for a negative `LIMIT` offset in sorted-set range commands, instead of one stray element on some encodings. ([#4637](https://github.com/valkey-io/valkey/pull/4637))
* Fix `HSETEX` and `HGETEX` failing when the key is named `fields`. ([#4945](https://github.com/valkey-io/valkey/pull/4945))
* Stop `HDEL`, `HGETDEL`, `HPERSIST` and `HEXPIRE` from propagating already-expired hash fields, which made replicas and AOF replay differ from the primary. ([#4772](https://github.com/valkey-io/valkey/pull/4772))
* Fix duplicating a hash that has expired fields that haven't been removed yet. ([#4939](https://github.com/valkey-io/valkey/pull/4939))
* Add the missing key-modified notifications for some stream commands, so `WATCH` and client-side caching see the change. ([#3459](https://github.com/valkey-io/valkey/pull/3459))
* Reject relative expire times that overflow once added to the current time, which could crash the server or break AOF restart. ([#4880](https://github.com/valkey-io/valkey/pull/4880))

### Crashes and robustness

* Fix a crash when `RESTORE` receives a payload with an overflowing string length. ([#4733](https://github.com/valkey-io/valkey/pull/4733))
* Fix a crash when an ACL file contains a malformed selector. ([#4214](https://github.com/valkey-io/valkey/pull/4214))
* Validate the key count before allocating memory when computing key specs. ([#3598](https://github.com/valkey-io/valkey/pull/3598))
* Reject module writes while clients are paused, which previously could crash the server. ([#3645](https://github.com/valkey-io/valkey/pull/3645))

### Cluster and replication

* Send `SELECT` at the end of the atomic slot migration snapshot so the target uses the right database. ([#4952](https://github.com/valkey-io/valkey/pull/4952))
* Fix eviction replication and replica database selection during atomic slot migration. ([#4920](https://github.com/valkey-io/valkey/pull/4920))
* Keep a separate `nodes.conf.lock` file for the startup lock, so saving `nodes.conf` no longer holds a descriptor on it during `rename()`. A failed write now aborts the save. ([#4489](https://github.com/valkey-io/valkey/pull/4489))

### Tools, logging and modules

* Hide user data in the log line written after an error reply when `hide-user-data-from-log` is set. ([#4815](https://github.com/valkey-io/valkey/pull/4815))
* Fix `valkey-benchmark` spinning on writes that would block. ([#4567](https://github.com/valkey-io/valkey/pull/4567))
* Fix `valkey-check-aof` not recognizing Valkey RDB base files. ([#4739](https://github.com/valkey-io/valkey/pull/4739))
* Fix the return types of three module API declarations in `valkeymodule.h` to match their definitions. ([#4676](https://github.com/valkey-io/valkey/pull/4676))

## Other

* Build: `OPENSSL_PREFIX` now persists across builds, and module API test linking is fixed on macOS. ([#4738](https://github.com/valkey-io/valkey/pull/4738))
* CI: move to Debian Bookworm and Ubuntu 24.04 runners, update the FreeBSD image, avoid LTTng kernel modules, and fix clang-format and spellcheck jobs. ([#4613](https://github.com/valkey-io/valkey/pull/4613), [#4922](https://github.com/valkey-io/valkey/pull/4922), [#4967](https://github.com/valkey-io/valkey/pull/4967), [#5029](https://github.com/valkey-io/valkey/pull/5029))
* Tests: fix flaky AOF manifest, slot migration and page cache tests, and add new tests for the fixes above. ([#4491](https://github.com/valkey-io/valkey/pull/4491), [#4366](https://github.com/valkey-io/valkey/pull/4366), [#4362](https://github.com/valkey-io/valkey/pull/4362))
* Bump the version to 9.0.7 and add the release notes entry. ([#5051](https://github.com/valkey-io/valkey/pull/5051))

