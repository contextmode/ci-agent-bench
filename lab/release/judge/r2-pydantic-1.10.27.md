# Judge file r2-pydantic-1.10.27

## PUBLISHED RELEASE NOTES (written by the maintainers)

## v1.10.27 (2026-10-29)

This is the last V1 Pydantic release. V1 support (including the `pydantic.v1` namespace in Pydantic V2) fully ends after this release.

This release contains three security fixes, that were also included in the `pydantic.v1` namespace of the [v2.14.2](https://github.com/pydantic/pydantic/releases/tag/v2.14.2) release.

* Check `unique_items` in linear time for builtin scalar types by @Viicos in https://github.com/pydantic/pydantic/pull/14101. Addresses https://github.com/pydantic/pydantic/security/advisories/GHSA-49g6-96jj-f7r9.
* Ignore internal `__pydantic` attributes when setting extra values on dataclasses by @Viicos in https://github.com/pydantic/pydantic/pull/14103. Addresses https://github.com/pydantic/pydantic/security/advisories/GHSA-r49w-vh47-r4hf.
* Only accept `.` as the decimal separator in ISO 8601 durations by @Viicos in https://github.com/pydantic/pydantic/pull/14096. Addresses https://github.com/pydantic/pydantic/security/advisories/GHSA-jfv7-ghgv-gx4x.

* Fix compatibility with Cython 3.3 by @Viicos in https://github.com/pydantic/pydantic/pull/14102


**Full Changelog**: https://github.com/pydantic/pydantic/compare/v1.10.26...v1.10.27

## COMMIT SUBJECTS between the previous tag and the release

Fix compatibility with Cython 3.3 (#14102)
Only accept `.` as the decimal separator in ISO 8601 durations (#14096)
Ignore internal `__pydantic` attributes when setting extra values on dataclasses (#14103)
Check `unique_items` in linear time for builtin scalar types (#14101)
Prepare release 1.10.27 (#14106)

# CANDIDATE A

## What's Changed

### Fixes

* Only accept `.` as the decimal separator in ISO 8601 durations, instead of any character. [#14096](https://github.com/pydantic/pydantic/pull/14096)
* Ignore internal `__pydantic*` attributes passed as extra values to dataclasses with `Extra.allow`. [#14103](https://github.com/pydantic/pydantic/pull/14103)

### Performance

* Check `unique_items` in linear time for lists of builtin scalar types (`int`, `float`, `str`, `bytes`, `bool`, `None`). [#14101](https://github.com/pydantic/pydantic/pull/14101)

### Other

* Fix compatibility with Cython 3.3. [#14102](https://github.com/pydantic/pydantic/pull/14102)
* Add `pytest-timeout` to the test requirements and add a benchmark data file.
* Prepare release 1.10.27. [#14106](https://github.com/pydantic/pydantic/pull/14106)

**Full Changelog**: https://github.com/pydantic/pydantic/compare/v1.10.26...v1.10.27


# CANDIDATE B

## What's Changed

### Fixes

* Only accept `.` as the decimal separator in ISO 8601 durations, so strings with other characters in that position are now rejected. [#14096](https://github.com/pydantic/pydantic/pull/14096)
* Ignore internal `__pydantic` attributes when setting extra values on dataclasses with `Extra.allow`. [#14103](https://github.com/pydantic/pydantic/pull/14103)
* Fix compatibility with Cython 3.3 when compiling Pydantic. [#14102](https://github.com/pydantic/pydantic/pull/14102)

### Performance

* Check `unique_items` in linear time for lists of builtin scalar types (`int`, `float`, `str`, `bytes`, `bool`, `None`). [#14101](https://github.com/pydantic/pydantic/pull/14101)

### Other

* Add a benchmark data file and `pytest-timeout` to the test requirements.
* Prepare release 1.10.27. [#14106](https://github.com/pydantic/pydantic/pull/14106)

**Full Changelog**: https://github.com/pydantic/pydantic/compare/v1.10.26...v1.10.27

