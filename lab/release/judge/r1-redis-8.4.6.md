# Judge file r1-redis-8.4.6

## PUBLISHED RELEASE NOTES (written by the maintainers)

Update urgency: `SECURITY`: There are security fixes in the release.

### Security fixes

- (CVE-2026-62356) Miscalculated buffer size in `CMSketch` RDB loading may lead to heap OOB write
- Out-of-bounds access in TopK heap cleanup path (MOD-15410)
- Use-after-free in the TLS pending-data list when a command closes another pending connection
- #15478 ACL key permission bypass in `SORT`, `GEORADIUS`/`GEORADIUSBYMEMBER` and `XREAD`/`XREADGROUP`: the keys validated by ACL could differ from the keys the command actually accesses
- #14847 Out-of-bounds `argv` access during key extraction when checking ACL permissions of a KEYNUM keyspec command (e.g. `EVAL`) with wrong arity
- A malicious RDB payload with an out-of-range `SLOT_INFO` slot id causes memory corruption during RDB loading, which may lead to Remote Code Execution
- Vector Sets: missing node level validation when loading a vector set from RDB may lead to out-of-bounds access
- Vector Sets: use-after-free when `VREM` mutates the HNSW graph while background `VSIM` threads are still running
- Vector Sets: a negative `hnsw_search()` return was treated as a huge unsigned count, reading past the end of the result arrays
- #15594 Use-after-free in the blocked-client list when reprocessing a command evicts another client blocked on the same key

## COMMIT SUBJECTS between the previous tag and the release

Update RedisBloom module version to v8.4.9 (#15655)
Fix use-after-free in tlsProcessPendingData() pending-list iteration (#1391)
Fix ACL key checks for SORT, GEORADIUS/GEORADIUSBYMEMBER, and XREAD/XREADGROUP (#15478)
Fix ACL OOB for wrong-arity KEYNUM commands (#14847)
Check slotinfo range when loading RDB (#1541)
VDP-4971 Vector Sets RDB load — missing `level` cap in `hnsw_insert_serialized` (illegal `max-level` / resource risk) (#1464)
MOD-16035: Fix VSIM/VREM race in Vector Sets
Vector Sets: harden VSIM_execute against negative hnsw_search return
Fix use-after-free in handleClientsBlockedOnKey (#15594)
Redis 8.4.6

# CANDIDATE A

# Redis 8.4.6

Redis 8.4.6 is a security and stability release. It contains no new features, deprecations, removals or breaking changes. Upgrading is recommended for all users.

## Security fixes

- Fix a memory corruption bug when loading an RDB file with an out-of-range slot ID in its slot metadata. This could be abused for remote code execution through a malicious RDB.
- Fix ACL bypasses where `GEORADIUS`/`GEORADIUSBYMEMBER` with repeated `STORE`/`STOREDIST`, `SORT` with repeated `STORE`, and `XREAD`/`XREADGROUP` with confusing option or name values could access keys the user was not permitted to use. [#15478](https://github.com/redis/redis/pull/15478)
- Fix an out-of-bounds read that could crash the server when ACL checks ran on commands with the wrong number of arguments (for example, `EVAL`), from Lua scripts or modules. [#14847](https://github.com/redis/redis/pull/14847)
- Vector Sets: validate node levels when loading from RDB, and fix a level calculation that could read out of bounds.

## Bug fixes

- Fix a use-after-free crash when client eviction removed other clients blocked on the same key. [#15594](https://github.com/redis/redis/pull/15594)
- Fix a use-after-free crash when processing pending TLS connections.
- Vector Sets: fix a crash when `VREM` ran at the same time as a background `VSIM`.
- Vector Sets: stop `VSIM` from reading past its result buffers if a search returns an error.

## Other

- Update the bundled RedisBloom module to v8.4.9. [#15655](https://github.com/redis/redis/pull/15655)
- Add tests for the ACL, scripting, module API, client eviction and Vector Sets fixes.


# CANDIDATE B

# Redis 8.4.6

This is a security and stability release. Upgrading is recommended for everyone, especially deployments that use ACLs, TLS, cluster mode or Vector Sets.

## Security fixes

- Fix ACL key checks that could be bypassed with `GEORADIUS`/`GEORADIUSBYMEMBER` when `STORE` or `STOREDIST` is given more than once ([#15478](https://github.com/redis/redis/pull/15478)).
- Fix ACL key checks for `SORT` when an earlier `STORE` value looks like an option keyword ([#15478](https://github.com/redis/redis/pull/15478)).
- Fix ACL key checks for `XREAD`/`XREADGROUP` when a group or consumer is named `STREAMS`, or when options come before `STREAMS` ([#15478](https://github.com/redis/redis/pull/15478)).
- `XREAD`/`XREADGROUP` key parsing now also handles the `CLAIM` option correctly ([#15478](https://github.com/redis/redis/pull/15478)).
- Fix an out-of-bounds read when checking ACLs for commands called with the wrong number of arguments ([#14847](https://github.com/redis/redis/pull/14847)).
- Reject RDB files that contain an out-of-range cluster slot ID, instead of risking an out-of-bounds access ([#1541](https://github.com/redis/redis/pull/1541)).
- Reject Vector Sets RDB data with an illegal node level, which could cause excessive memory use.

## Bug fixes

- Fix a use-after-free when clients blocked on the same key are served and one of them is evicted ([#15594](https://github.com/redis/redis/pull/15594)).
- Fix a use-after-free when processing pending TLS data ([#1391](https://github.com/redis/redis/pull/1391)).
- Fix a race between `VSIM` and `VREM` in Vector Sets that could crash the server.
- Make `VSIM` handle a negative search result safely.
- Fix Vector Sets random node level generation so it never reaches the maximum level.

## Behavior changes

- `redis.acl_check_cmd()` in Lua now returns the error "Wrong number of args for redis.acl_check_cmd()" when the argument count is wrong ([#14847](https://github.com/redis/redis/pull/14847)).
- `RedisModule_ACLCheckCommandPermissions()` now fails with `errno` set to `EINVAL` when the argument count is wrong ([#14847](https://github.com/redis/redis/pull/14847)).

## Modules

- Update RedisBloom to v8.4.9 ([#15655](https://github.com/redis/redis/pull/15655)).

## Other

- Added regression tests for ACL, client eviction, scripting, module ACL checks and concurrent `VSIM`/`VREM`.
- Bumped the version to 8.4.6.

