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
