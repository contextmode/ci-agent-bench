# Judge file r1-fastapi-0.160.0

## PUBLISHED RELEASE NOTES (written by the maintainers)

Query, header, cookie, and form parameter models now apply their `extra` configuration to all submitted fields in the same parameter location, consistent with Pydantic behavior. This includes fields declared in other models, individual parameters, or dependencies, which were previously excluded.

With `extra="forbid"`, fields outside the model are rejected even if another parameter declares them. With `extra="allow"`, those fields are included as model extras. With the default `extra="ignore"`, they are ignored.

### Breaking Changes

* 🐛 Apply each parameter model's `extra` configuration to sibling fields. PR [#16594](https://github.com/fastapi/fastapi/pull/16594) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump certifi from 2026.1.4 to 2026.10.19. PR [#16571](https://github.com/fastapi/fastapi/pull/16571) by [@dependabot[bot]](https://github.com/apps/dependabot).


## COMMIT SUBJECTS between the previous tag and the release

⬆ Bump certifi from 2026.1.4 to 2026.10.19 (#16571)
📝 Update release notes
🐛 Apply each parameter model's `extra` configuration to sibling fields (#16594)
📝 Update release notes
🔖 Release version 0.160.0 (#16595)

# CANDIDATE A

## Fixes

* 🐛 Apply each parameter model's `extra` configuration to sibling fields. PR [#16594](https://github.com/fastapi/fastapi/pull/16594).
  * With several Query, Header, Cookie or Form parameter models (or models plus plain parameters) on one endpoint, each model now applies its own `extra` setting to every input it didn't claim, including values declared by sibling parameters or dependencies.
  * For example, a model with `extra="forbid"` now rejects a value that belongs to another parameter, and `extra="allow"` now collects it.
  * This reverses the earlier behavior that skipped names declared elsewhere, so check endpoints that combine several parameter models.

## Other

* ⬆ Bump certifi from 2026.1.4 to 2026.10.19 in the project's lock file. PR [#16571](https://github.com/fastapi/fastapi/pull/16571).
* ✅ Update tests for parameter models with different `extra` settings. PR [#16594](https://github.com/fastapi/fastapi/pull/16594).
* 🔖 Release version 0.160.0. PR [#16595](https://github.com/fastapi/fastapi/pull/16595).


# CANDIDATE B

## Breaking Changes

* 🐛 Apply each parameter model's `extra` configuration to all parameters in the request, including sibling ones. PR [#16594](https://github.com/fastapi/fastapi/pull/16594).
    * With `extra="forbid"`, query, header, cookie and form parameters declared in other models, parameters or dependencies are now rejected by that model, where 0.159.1 allowed them.
    * With `extra="allow"`, those parameters are now included in the model's extras.
    * If you combine several parameter models with `forbid`, check that your requests still validate, or use `extra="ignore"`.

## Other

* 📝 Update docs for parameter and form models to describe the `extra` behavior. PR [#16594](https://github.com/fastapi/fastapi/pull/16594).
* ✅ Update tests for multiple parameter and form models. PR [#16594](https://github.com/fastapi/fastapi/pull/16594).
* ⬆ Bump certifi from 2026.1.4 to 2026.10.19. PR [#16571](https://github.com/fastapi/fastapi/pull/16571).
* 🔖 Release version 0.160.0. PR [#16595](https://github.com/fastapi/fastapi/pull/16595).

