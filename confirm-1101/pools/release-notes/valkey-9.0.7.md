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
