## v1.10.27 (2026-10-29)

This is the last V1 Pydantic release. V1 support (including the `pydantic.v1` namespace in Pydantic V2) fully ends after this release.

This release contains three security fixes, that were also included in the `pydantic.v1` namespace of the [v2.14.2](https://github.com/pydantic/pydantic/releases/tag/v2.14.2) release.

* Check `unique_items` in linear time for builtin scalar types by @Viicos in https://github.com/pydantic/pydantic/pull/14101. Addresses https://github.com/pydantic/pydantic/security/advisories/GHSA-49g6-96jj-f7r9.
* Ignore internal `__pydantic` attributes when setting extra values on dataclasses by @Viicos in https://github.com/pydantic/pydantic/pull/14103. Addresses https://github.com/pydantic/pydantic/security/advisories/GHSA-r49w-vh47-r4hf.
* Only accept `.` as the decimal separator in ISO 8601 durations by @Viicos in https://github.com/pydantic/pydantic/pull/14096. Addresses https://github.com/pydantic/pydantic/security/advisories/GHSA-jfv7-ghgv-gx4x.

* Fix compatibility with Cython 3.3 by @Viicos in https://github.com/pydantic/pydantic/pull/14102


**Full Changelog**: https://github.com/pydantic/pydantic/compare/v1.10.26...v1.10.27