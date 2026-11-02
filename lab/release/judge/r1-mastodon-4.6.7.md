# Judge file r1-mastodon-4.6.7

## PUBLISHED RELEASE NOTES (written by the maintainers)

<h1><picture>
  <source media="(prefers-color-scheme: dark)" srcset="./lib/assets/wordmark.dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="./lib/assets/wordmark.light.png?raw=true">
  <img alt="Mastodon" src="./lib/assets/wordmark.light.png?raw=true" height="34">
</picture></h1>

## Upgrade overview

This release contains upgrade notes that deviate from the norm:

ℹ️ Requires assets recompilation

For more information, view the complete release notes and scroll down to the upgrade instructions section.

## Changelog

## Security

- Update dependencies
- Fix password authentication bypass in 2FA auth for LDAP/PAM/SSO accounts ([GHSA-vx32-x96w-qq65](https://github.com/mastodon/mastodon/security/advisories/GHSA-vx32-x96w-qq65))
- Fix Denial of Service when processing pathological JSON-LD activities ([GHSA-vgm8-frgh-rh2v](https://github.com/mastodon/mastodon/security/advisories/GHSA-vgm8-frgh-rh2v))
- Fix disabled staff accounts still having access to admin API ([GHSA-62j4-hvj7-px3f](https://github.com/mastodon/mastodon/security/advisories/GHSA-62j4-hvj7-px3f))

### Fixes

- Fix `config/` directory missing from Bootsnap precompilation options in Dockerfile (#40255 by @ClearlyClaire)
- Fix autosuggestions overstaying their welcome in languages that don't use spaces (#40217 by @Gargron)
- Fix error when processing remote actors with `null` public keys (#40194 by @ClearlyClaire)
- Fix various off-by-one errors in statistics time ranges (#40193 by @ClearlyClaire)

## Upgrade notes

To get the code for v4.6.7, use `git fetch && git checkout v4.6.7`.

> [!NOTE]
> As always, make sure you have backups of the database before performing any upgrades. If you are using docker-compose, this is how a backup command might look: `docker exec mastodon_db_1 pg_dump -Fc -U postgres postgres > name_of_the_backup.dump`

### Dependencies

External dependencies have not changed since v4.6.0.

- Ruby: 3.3 or newer
- PostgreSQL: 14 or newer
- Elasticsearch (recommended, for full-text search): 7.x (OpenSearch should also work)
- LibreTranslate (optional, for translations): 1.3.3 or newer
- Redis: 7.0 or newer
- Node: 22 or newer
- libvips: 8.13 or newer
- FFMpeg: 5.1 or newer

### Update steps

The following instructions are for updating from 4.6.6.

If you are upgrading directly from an earlier release, please carefully read the upgrade notes for the skipped releases as well, as they often require extra steps such as database migrations. In particular, it is very important to read the [4.6.0 release notes](https://github.com/mastodon/mastodon/releases/tag/v4.6.0).

### Non-Docker

> [!TIP]
> The `charlock_holmes` gem may fail to build on some systems with recent versions of gcc.
If you run into this issue, try `BUNDLE_BUILD__CHARLOCK_HOLMES="--with-cxxflags=-std=c++17" bundle install`.

1. Install dependencies with `bundle install`
2. Precompile the assets: `RAILS_ENV=production bundle exec rails assets:precompile`
3. Restart all Mastodon processes.

### When using Docker

1. Restart all Mastodon processes.

## COMMIT SUBJECTS between the previous tag and the release

Update security policy
Fix various off-by-one errors in statistics time ranges (#40193)
Fix error when processing remote actors with `null` public keys (#40194)
Switch APT repos to canonical ubuntu repos rather than Azure mirror (#40205)
Fix autosuggestions overstaying their welcome in languages that don't use spaces (#40217)
Add the `config/` directory to Bootsnap precompilation in Dockerfile (#40255)
Add some spec coverage (#40306)
Update `activestorage` dependency
Update `mail` dependency
Fix invited-without-approval-bypass not being asked for a textual reason (#40332)
Add another permission check to admin area (#39974)
Fix GHSA-vgm8-frgh-rh2v
Fixes GHSA-62j4-hvj7-px3f
Fix GHSA-vx32-x96w-qq65
Bump version to v4.6.7

# CANDIDATE A

## Security

- Fix admin pages and admin API endpoints being reachable by users without moderation or admin permissions (GHSA-62j4-hvj7-px3f). Disabled users are now treated as having no role.
- Fix a two-factor authentication prompt being shown to accounts with no local password, which allowed a login-flow bypass (GHSA-vx32-x96w-qq65).
- Limit the size and features of JSON-LD documents received from other servers, to prevent abuse with oversized documents (GHSA-vgm8-frgh-rh2v).
- Add another permission check to the admin area ([#39974](https://github.com/mastodon/mastodon/pull/39974)).
- Update the `activestorage` and `mail` dependencies for security fixes.

## Fixed

- Fix users with an invite that skips approval still being asked for a sign-up reason ([#40332](https://github.com/mastodon/mastodon/pull/40332)).
- Fix invites that don't skip approval wrongly hiding the reason field and showing the wrong button label ([#40332](https://github.com/mastodon/mastodon/pull/40332)).
- Fix user suggestions after `@` staying open and swallowing text when writing in languages that don't use spaces ([#40217](https://github.com/mastodon/mastodon/pull/40217)).
- Fix an error when processing remote accounts with a `null` public key ([#40194](https://github.com/mastodon/mastodon/pull/40194)).
- Fix off-by-one errors in the date ranges of admin statistics and dashboards ([#40193](https://github.com/mastodon/mastodon/pull/40193)).

## Other

- Add the `config/` directory to Bootsnap precompilation in the Dockerfile ([#40255](https://github.com/mastodon/mastodon/pull/40255)).
- Switch APT repositories to the canonical Ubuntu ones instead of the Azure mirror ([#40205](https://github.com/mastodon/mastodon/pull/40205)).
- Add test coverage ([#40306](https://github.com/mastodon/mastodon/pull/40306)).
- Update the security policy.


# CANDIDATE B

## Security

- Fixed an authentication issue in login with two-factor authentication: accounts without a local password (for example LDAP/PAM-backed ones) could be taken to the two-factor step without a valid password. [GHSA-vx32-x96w-qq65](https://github.com/mastodon/mastodon/security/advisories/GHSA-vx32-x96w-qq65)
- Fixed missing permission checks in the admin interface and admin API, and disabled users no longer keep their role's permissions. [GHSA-62j4-hvj7-px3f](https://github.com/mastodon/mastodon/security/advisories/GHSA-62j4-hvj7-px3f), [#39974](https://github.com/mastodon/mastodon/pull/39974)
- Added limits on the size and features of incoming JSON-LD documents, to stop abusive remote activities. [GHSA-vgm8-frgh-rh2v](https://github.com/mastodon/mastodon/security/advisories/GHSA-vgm8-frgh-rh2v)
- Updated the `activestorage` (Rails 8.1.3.1) and `mail` dependencies with security fixes.

## Fixed

- Fixed the sign-up form not asking for a reason when the invite used does not bypass approval. [#40332](https://github.com/mastodon/mastodon/pull/40332)
- Fixed user autosuggestions staying open while typing in languages that don't separate words with spaces. [#40217](https://github.com/mastodon/mastodon/pull/40217)
- Fixed an error when processing remote accounts with a `null` public key. [#40194](https://github.com/mastodon/mastodon/pull/40194)
- Fixed off-by-one errors in the time ranges of admin statistics and the dashboard. [#40193](https://github.com/mastodon/mastodon/pull/40193)

## Other

- Updated the security policy.
- Added `config/` to Bootsnap precompilation in the Dockerfile. [#40255](https://github.com/mastodon/mastodon/pull/40255)
- Switched APT repositories in builds to the canonical Ubuntu ones. [#40205](https://github.com/mastodon/mastodon/pull/40205)
- Added more test coverage. [#40306](https://github.com/mastodon/mastodon/pull/40306)

