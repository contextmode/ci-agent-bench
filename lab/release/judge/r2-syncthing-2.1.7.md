# Judge file r2-syncthing-2.1.7

## PUBLISHED RELEASE NOTES (written by the maintainers)

## What's Changed

Built with Go 1.27.3.

### Fixes
* fix: handle missing max-sequence file entries by @calmh in https://github.com/syncthing/syncthing/pull/10912
* fix(sqlite): avoid early garbage collection of deleted recv-enc files by @calmh in https://github.com/syncthing/syncthing/pull/10916
* fix(sqlite): do not generate unbounded prepared statements (ref #10913) by @calmh in https://github.com/syncthing/syncthing/pull/10915
* fix(discover): skip unnecessary identical global announce updates; obey retry-after by @calmh in https://github.com/syncthing/syncthing/pull/10918
* fix(protocol): convert panics on bad data to protocol errors by @calmh in https://github.com/syncthing/syncthing/pull/10923
* fix(model): verify local change before applying metadata shortcut (fixes #10924) by @calmh in https://github.com/syncthing/syncthing/pull/10925
* fix(model): ensure parent ownership is copied properly (fixes #8399) by @calmh in https://github.com/syncthing/syncthing/pull/10926
* fix(model): properly compare blocks when reconciling receive-only (fixes #10928) by @calmh in https://github.com/syncthing/syncthing/pull/10929
### Other
* build(deps): update dependencies by @calmh in https://github.com/syncthing/syncthing/pull/10917
* chore(protocol): add protovalidate validation of incoming messages, reasonable limits by @calmh in https://github.com/syncthing/syncthing/pull/10838

**Full Changelog**: https://github.com/syncthing/syncthing/compare/v2.1.6...v2.1.7

## COMMIT SUBJECTS between the previous tag and the release

build: skip defunct loki sending
fix: handle missing max-sequence file entries (#10912)
fix(sqlite): avoid early garbage collection of deleted recv-enc files (#10916)
fix(sqlite): do not generate unbounded prepared statements (ref #10913) (#10915)
build(deps): update dependencies (#10917)
fix(discover): skip unnecessary identical global announce updates; obey retry-after (#10918)
chore(gui, man, authors): update docs, translations, and contributors
fix(protocol): convert panics on bad data to protocol errors (#10923)
chore(protocol): add protovalidate validation of incoming messages, reasonable limits (#10838)
fix(model): verify local change before applying metadata shortcut (fixes #10924) (#10925)
fix(model): ensure parent ownership is copied properly (fixes #8399) (#10926)
fix: cap body sizes for incoming requests to public services
chore(gui, man, authors): update docs, translations, and contributors
fix(model): properly compare blocks when reconciling receive-only (fixes #10928) (#10929)

# CANDIDATE A

## Syncthing v2.1.7

### Bugfixes

- Receive-only folders now compare file blocks correctly when reconciling local changes. ([#10928](https://github.com/syncthing/syncthing/issues/10928), [#10929](https://github.com/syncthing/syncthing/pull/10929))
- Parent directories created along with a new directory now get the correct ownership. ([#8399](https://github.com/syncthing/syncthing/issues/8399), [#10926](https://github.com/syncthing/syncthing/pull/10926))
- A local change is now verified before a metadata-only update is applied. ([#10924](https://github.com/syncthing/syncthing/issues/10924), [#10925](https://github.com/syncthing/syncthing/pull/10925))
- Syncthing no longer fails on folders whose newest entries are deleted files after the tombstone cleanup time has passed. ([#10912](https://github.com/syncthing/syncthing/pull/10912))
- Deleted files in receive-encrypted folders are no longer cleaned up from the database too early. ([#10916](https://github.com/syncthing/syncthing/pull/10916))
- Global discovery skips announcements that haven't changed and respects the server's retry-after delay. ([#10918](https://github.com/syncthing/syncthing/pull/10918))

### Security and robustness

- Bad data from a remote device now causes a protocol error instead of crashing Syncthing. ([#10923](https://github.com/syncthing/syncthing/pull/10923))
- Incoming protocol messages are validated and unreasonable values are rejected early. ([#10838](https://github.com/syncthing/syncthing/pull/10838))
- Database API requests with unusual paging parameters can no longer cause unbounded memory use. ([#10913](https://github.com/syncthing/syncthing/issues/10913), [#10915](https://github.com/syncthing/syncthing/pull/10915))
- The discovery, relay pool and usage-reporting servers now limit the size of incoming request bodies.

### Other

- Updated dependencies. ([#10917](https://github.com/syncthing/syncthing/pull/10917))
- Updated translations, documentation, man pages and contributor list.
- Build: stopped sending logs to the defunct Loki service, and added protobuf validation tooling.


# CANDIDATE B

## Syncthing v2.1.7

### Bugfixes

- Receive-only folders now compare file blocks correctly when reconciling local changes ([#10929](https://github.com/syncthing/syncthing/pull/10929), fixes [#10928](https://github.com/syncthing/syncthing/issues/10928)).
- Local changes are now verified before the metadata-only shortcut is used ([#10925](https://github.com/syncthing/syncthing/pull/10925), fixes [#10924](https://github.com/syncthing/syncthing/issues/10924)).
- When several nested directories are created at once, ownership is now inherited through all parent directories ([#10926](https://github.com/syncthing/syncthing/pull/10926), fixes [#8399](https://github.com/syncthing/syncthing/issues/8399)).
- Folders whose newest entries are deleted files no longer hit an error after the default 180-day tombstone cleanup ([#10912](https://github.com/syncthing/syncthing/pull/10912)).
- Deleted files in receive-encrypted folders are no longer garbage collected too early ([#10916](https://github.com/syncthing/syncthing/pull/10916)).
- Fixed a memory leak caused by REST API requests with varying paging parameters ([#10915](https://github.com/syncthing/syncthing/pull/10915)).
- Global discovery now skips announcements that would be identical and respects the server's retry-after delay ([#10918](https://github.com/syncthing/syncthing/pull/10918)).

### Security and robustness

- Malformed data from a remote device now causes a protocol error instead of a crash ([#10923](https://github.com/syncthing/syncthing/pull/10923)).
- Incoming protocol messages are now validated early, with limits on sizes and offsets ([#10838](https://github.com/syncthing/syncthing/pull/10838)).
- Request body sizes are now capped on the public discovery and relay pool services ([7b7b0f7](https://github.com/syncthing/syncthing/commit/7b7b0f753)).

### Other

- Updated dependencies ([#10917](https://github.com/syncthing/syncthing/pull/10917)).
- Updated translations, man pages and contributor list.
- Build: stopped sending to the defunct Loki service.

