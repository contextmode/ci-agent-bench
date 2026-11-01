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