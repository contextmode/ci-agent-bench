# Judge file r2-nest-12.1.0

## PUBLISHED RELEASE NOTES (written by the maintainers)

## v12.1.0 (2026-09-23)

#### Bug fixes
* `core`
  * [#17838](https://github.com/nestjs/nest/pull/17838) fix(core): inherit optional ctor params when the ctor is not redeclared ([@kamilmysliwiec](https://github.com/kamilmysliwiec))
  * [#17819](https://github.com/nestjs/nest/pull/17819) fix(core): name the module when metadata entries are invalid ([@thekhegay](https://github.com/thekhegay))
* `microservices`
  * [#17828](https://github.com/nestjs/nest/pull/17828) fix(microservices): let the redis client retry after a failed connect ([@hktitof](https://github.com/hktitof))
  * [#17810](https://github.com/nestjs/nest/pull/17810) fix(microservices): fail every pending request when a callback throws ([@hktitof](https://github.com/hktitof))

#### Enhancements
* `core`
  * [#17846](https://github.com/nestjs/nest/pull/17846) fix(core): do not skip subsequent middleware after a transient one ([@lehafari](https://github.com/lehafari))
  * [#17840](https://github.com/nestjs/nest/pull/17840) fix(core): preserve route handler names ([@Grmiade](https://github.com/Grmiade))
* `common`, `core`
  * [#17713](https://github.com/nestjs/nest/pull/17713) feat(core): add support for array of global prefixes ([@micalevisk](https://github.com/micalevisk))
  * [#17834](https://github.com/nestjs/nest/pull/17834) feat(common,core): add built-in, adapter-agnostic cookies ([@kamilmysliwiec](https://github.com/kamilmysliwiec))
* `platform-fastify`
  * [#17824](https://github.com/nestjs/nest/pull/17824) fix(fastify): honor Nest forceCloseConnections in initHttpServer ([@xia-chao](https://github.com/xia-chao))
* `common`
  * [#17827](https://github.com/nestjs/nest/pull/17827) fix(common): apply the ParseDatePipe default to every missing value ([@xia-chao](https://github.com/xia-chao))
* `platform-fastify`, `testing`
  * [#17835](https://github.com/nestjs/nest/pull/17835) feat(fastify): add file upload interceptors backed by @fastify/multipart ([@kamilmysliwiec](https://github.com/kamilmysliwiec))
* `common`, `core`, `platform-fastify`
  * [#17836](https://github.com/nestjs/nest/pull/17836) feat(common,core,fastify): built-in CSRF protection and security headers ([@kamilmysliwiec](https://github.com/kamilmysliwiec))


#### Committers: 9
- Abdellatif Anaflous ([@hktitof](https://github.com/hktitof))
- Alejandro ([@lehafari](https://github.com/lehafari))
- Chris Z ([@haimingZZ](https://github.com/haimingZZ))
- Johnny J. Huirilef Millán ([@johnnyhuirilef](https://github.com/johnnyhuirilef))
- Jérémy Fauvel ([@Grmiade](https://github.com/Grmiade))
- Kamil Mysliwiec ([@kamilmysliwiec](https://github.com/kamilmysliwiec))
- Micael Levi L. Cavalcante ([@micalevisk](https://github.com/micalevisk))
- Roman Khegay ([@thekhegay](https://github.com/thekhegay))
- Xia Chao ([@xia-chao](https://github.com/xia-chao))


## COMMIT SUBJECTS between the previous tag and the release

chore: update readme
fix: three typos (subcription x2, propery) (#17833)
feat(common,core,fastify): built-in CSRF protection and security headers (#17836)
feat(fastify): add file upload interceptors backed by @fastify/multipart (#17835)
feat(common,core): add built-in, adapter-agnostic cookies (#17834)
chore(deps): update dependency oxlint to v1.85.0 (#17832)
fix(deps): update dependency dotenv to v18.0.2 (#17831)
chore(deps): update dependency typescript-eslint to v8.70.1 (#17830)
chore(deps): update dependency eventsource to v5.1.2 (#17829)
fix(microservices): undo a request whose publish threw (#17822)
fix(common): apply the ParseDatePipe default to every missing value (#17827)
fix(fastify): honor Nest forceCloseConnections in initHttpServer (#17824)
fix(deps): update nest monorepo to v12.0.4 (#17825)
fix(core): stop the Observable producer when the client disconnects (#17826)
fix(microservices): fail every pending request when a callback throws (#17810)
fix(core): name the module when metadata entries are invalid (#17819)
fix(microservices): let the redis client retry after a failed connect (#17828)
fix(core): inherit optional ctor params when the ctor is not redeclared (#17838)
fix(core): preserve route handler names (#17840)
chore(deps): update dependency supertest to v7.3.0 (#17837)
feat(core): add support for array of global prefixes (#17713)
Revert "feat(core): add support for array of global prefixes (#17713)" (#17845)
fix(core): do not skip subsequent middleware after a transient one (#17846)
fix(deps): update dependency mongoose to v9.10.2 (#17844)
fix(deps): update dependency dotenv to v18.0.3 (#17843)
chore(deps): update dependency @nestjs/cli to v12.0.5 (#17842)
chore(deps): update dependency @fastify/multipart to v10.1.2 (#17841)
sample: rewrite the dynamic modules sample around an id generator
chore(release): publish v12.1.0 release

# CANDIDATE A

## What's new

### Features

- Add built-in, adapter-agnostic cookies: a `cookies` application option, `@Cookies()` and `@SignedCookies()` parameter decorators, and cookie helpers on the HTTP adapter that work the same on Express and Fastify without `cookie-parser` or `@fastify/cookie`. ([#17834](https://github.com/nestjs/nest/pull/17834))
- Add opt-in `app.useSecurityHeaders()` (Helmet-style headers) and `app.enableCsrfProtection()` (cross-origin request protection) that work on Express and Fastify without extra packages. ([#17836](https://github.com/nestjs/nest/pull/17836))
- Add file upload interceptors for Fastify, backed by `@fastify/multipart`, with the same API as the Multer-based ones (`FileInterceptor`, `FilesInterceptor`, `FileFieldsInterceptor`, `AnyFilesInterceptor`, `NoFilesInterceptor`, `MultipartModule`). ([#17835](https://github.com/nestjs/nest/pull/17835))

### Bug fixes

- Fix middleware being skipped after a request-scoped (transient) middleware in the list. ([#17846](https://github.com/nestjs/nest/pull/17846))
- Fix subclasses without their own constructor losing the parent's `@Optional()` parameters, which broke bootstrap. ([#17838](https://github.com/nestjs/nest/pull/17838))
- Keep route handler names (such as `UsersController.findAll`) visible to the HTTP adapter. ([#17840](https://github.com/nestjs/nest/pull/17840))
- Stop an Observable returned from a route handler when the client disconnects. ([#17826](https://github.com/nestjs/nest/pull/17826))
- Name the module in the error when a provider, controller or export entry is invalid. ([#17819](https://github.com/nestjs/nest/pull/17819))
- Make `ParseDatePipe` use its `default` for every missing value, not only when `optional` is set. ([#17827](https://github.com/nestjs/nest/pull/17827))
- Make the Fastify adapter honor `forceCloseConnections` so keep-alive connections no longer block shutdown. ([#17824](https://github.com/nestjs/nest/pull/17824))
- Let the Redis microservice client reconnect after its retries are exhausted or the connection ends. ([#17828](https://github.com/nestjs/nest/pull/17828))
- Remove a pending request when sending it fails in the TCP, Redis and MQTT clients. ([#17822](https://github.com/nestjs/nest/pull/17822))
- Fail all pending requests when closing the Kafka, MQTT, Redis or TCP client, even if one callback throws. ([#17810](https://github.com/nestjs/nest/pull/17810))
- Fix typos in names and messages. ([#17833](https://github.com/nestjs/nest/pull/17833))

## Other

- Update dependencies, including `dotenv`, `mongoose`, `@fastify/multipart`, `@nestjs/cli`, `supertest`, `eventsource`, `typescript-eslint` and `oxlint`.
- Add integration tests for the new features, rewrite the dynamic modules sample, and update the readme.
- Support for an array of global prefixes was added and reverted within this release, so it is not included. ([#17713](https://github.com/nestjs/nest/pull/17713), [#17845](https://github.com/nestjs/nest/pull/17845))


# CANDIDATE B

## Highlights

NestJS v12.1.0 adds built-in cookies, CSRF protection and security headers that work the same on Express and Fastify, plus file upload interceptors for Fastify. It also fixes several bugs in middleware, dependency injection, microservice clients and HTTP handling.

## Features

- Add built-in, adapter-agnostic cookie support: the `@Cookies()` and `@SignedCookies()` parameter decorators, `setCookie()`/`clearCookie()` on the HTTP adapter, and a `cookies: { secret }` application option that supports secret rotation. No extra package is needed. ([#17834](https://github.com/nestjs/nest/pull/17834))
- Add `app.useSecurityHeaders()` to set security headers (Helmet-style defaults, including a Content Security Policy) on Express and Fastify. ([#17836](https://github.com/nestjs/nest/pull/17836))
- Add `app.enableCsrfProtection()` to reject cross-origin state-changing requests with a `403`, with `trustedOrigins` and `exclude` options. ([#17836](https://github.com/nestjs/nest/pull/17836))
- Add file upload interceptors for Fastify in `@nestjs/platform-fastify/multipart`, backed by `@fastify/multipart`. They include `FileInterceptor`, `FilesInterceptor`, `FileFieldsInterceptor`, `AnyFilesInterceptor`, `NoFilesInterceptor`, `MultipartModule`, `memoryStorage()` and `diskStorage()`, and they mirror the Express (Multer) API. ([#17835](https://github.com/nestjs/nest/pull/17835))

## Bug fixes

- Fix a transient-scoped middleware causing every middleware listed after it in the same `apply()` call to be silently skipped. ([#17846](https://github.com/nestjs/nest/pull/17846))
- Fix a regression from 12.0.x where a subclass without its own constructor lost its parent's `@Optional()` flags. This broke patterns such as `class LocalAuthGuard extends AuthGuard('local')`. ([#17838](https://github.com/nestjs/nest/pull/17838))
- Keep route handler names such as `Controller.method` instead of `<anonymous>`, so tracing and profiling tools can identify them. ([#17840](https://github.com/nestjs/nest/pull/17840))
- Stop a route handler's Observable when the client disconnects, instead of letting it keep producing. ([#17826](https://github.com/nestjs/nest/pull/17826))
- Make Fastify honor `forceCloseConnections`, so keep-alive connections no longer block `app.close()`. ([#17824](https://github.com/nestjs/nest/pull/17824))
- Make `ParseDatePipe`'s `default` apply to any missing value, not only when `optional` is set. ([#17827](https://github.com/nestjs/nest/pull/17827))
- Report an error that names the module when a provider has no valid `useClass`, `useValue`, `useFactory` or `useExisting`, or when `controllers` or `exports` contain an undefined entry. ([#17819](https://github.com/nestjs/nest/pull/17819))
- Microservices: fail every pending request when closing a Kafka, MQTT, Redis or TCP client, even if one callback throws. ([#17810](https://github.com/nestjs/nest/pull/17810))
- Microservices: clean up the request when sending fails on the TCP, Redis and MQTT clients, so it is no longer left pending. ([#17822](https://github.com/nestjs/nest/pull/17822))
- Microservices: let the Redis client reconnect after its connection attempts have failed, instead of replaying the old error. ([#17828](https://github.com/nestjs/nest/pull/17828))
- Fix typos in the codebase. ([#17833](https://github.com/nestjs/nest/pull/17833))

## Breaking changes, deprecations and removals

- None. The new features are opt-in. Custom adapters that extend `AbstractHttpAdapter` and already define `setCookie`, `clearCookie` or `setCookieSigner` may conflict with the new base methods.

## Other

- Rewrite the dynamic modules sample around an ID generator module. ([`0dabf67`](https://github.com/nestjs/nest/commit/0dabf675f))
- Update dependencies, including `mongoose`, `dotenv`, `@fastify/multipart`, `@nestjs/cli`, `supertest`, `eventsource`, `typescript-eslint` and `oxlint`. ([#17841](https://github.com/nestjs/nest/pull/17841), [#17842](https://github.com/nestjs/nest/pull/17842), [#17843](https://github.com/nestjs/nest/pull/17843), [#17844](https://github.com/nestjs/nest/pull/17844), [#17837](https://github.com/nestjs/nest/pull/17837), [#17829](https://github.com/nestjs/nest/pull/17829), [#17830](https://github.com/nestjs/nest/pull/17830), [#17831](https://github.com/nestjs/nest/pull/17831), [#17832](https://github.com/nestjs/nest/pull/17832), [#17825](https://github.com/nestjs/nest/pull/17825))
- Update the readme and add tests, including integration tests for the new features.

