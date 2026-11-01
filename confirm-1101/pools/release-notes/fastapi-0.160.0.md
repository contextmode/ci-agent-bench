Query, header, cookie, and form parameter models now apply their `extra` configuration to all submitted fields in the same parameter location, consistent with Pydantic behavior. This includes fields declared in other models, individual parameters, or dependencies, which were previously excluded.

With `extra="forbid"`, fields outside the model are rejected even if another parameter declares them. With `extra="allow"`, those fields are included as model extras. With the default `extra="ignore"`, they are ignored.

### Breaking Changes

* 🐛 Apply each parameter model's `extra` configuration to sibling fields. PR [#16594](https://github.com/fastapi/fastapi/pull/16594) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump certifi from 2026.1.4 to 2026.10.19. PR [#16571](https://github.com/fastapi/fastapi/pull/16571) by [@dependabot[bot]](https://github.com/apps/dependabot).
