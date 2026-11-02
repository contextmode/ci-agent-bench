# Judge file r1-svelte-5.56.10

## PUBLISHED RELEASE NOTES (written by the maintainers)

### Patch Changes

-   fix: preserve CSS escape sequences when printing selectors ([#18667](https://github.com/sveltejs/svelte/pull/18667))

-   fix: parse `:nth-child(2n of.foo)` where `of` is not followed by whitespace ([#18611](https://github.com/sveltejs/svelte/pull/18611))

-   fix: transform expressions inside labeled statements during server compilation ([#18617](https://github.com/sveltejs/svelte/pull/18617))

-   docs: clarify that context lookup includes the current component and all ancestors ([#18581](https://github.com/sveltejs/svelte/pull/18581))

-   fix: apply CSS custom properties with falsy values on components ([#18634](https://github.com/sveltejs/svelte/pull/18634))

-   fix: correctly print `{#await ... catch x}` et al ([#18645](https://github.com/sveltejs/svelte/pull/18645))

-   fix: ignore comments of Program node during migration script ([#18656](https://github.com/sveltejs/svelte/pull/18656))

-   fix: reliably resolve append_style to its correct root ([#18614](https://github.com/sveltejs/svelte/pull/18614))

-   fix: clean up removed capture event handlers from spread attributes ([#18618](https://github.com/sveltejs/svelte/pull/18618))

-   fix: don't corrupt renderer type during SSR's legacy `bind:` retry loop ([#18616](https://github.com/sveltejs/svelte/pull/18616))

-   fix: treat concise arrow function bodies as implicit returns when calculating blockers ([#18613](https://github.com/sveltejs/svelte/pull/18613))

-   fix: give effect teardowns the value from before the first write in a flush ([#18620](https://github.com/sveltejs/svelte/pull/18620))

-   fix: avoid double-calling a derived reference when destructuring `$derived` of another `$derived` during server-side rendering ([#18668](https://github.com/sveltejs/svelte/pull/18668))

-   fix: preserve namespaces in CSS type selectors ([#18678](https://github.com/sveltejs/svelte/pull/18678))

-   fix: increment private state fields through a non-`this` receiver ([#18622](https://github.com/sveltejs/svelte/pull/18622))

-   chore: deduplicate client and server context helpers ([#18580](https://github.com/sveltejs/svelte/pull/18580))

-   fix: release `last_propagated_event` after event propagation settles so it no longer retains the last event's target subtree ([#18569](https://github.com/sveltejs/svelte/pull/18569))

-   fix: allow custom elements to receive async values as props ([#18661](https://github.com/sveltejs/svelte/pull/18661))

-   fix: strip comments from inline `style` values in linear time ([#18553](https://github.com/sveltejs/svelte/pull/18553))

-   fix: prevent declaration comments from breaking server derived references ([#18641](https://github.com/sveltejs/svelte/pull/18641))

-   perf: make async blocker analysis scale linearly with the number of top-level references ([#18549](https://github.com/sveltejs/svelte/pull/18549))

-   fix: preserve short-circuiting for logical assignments to private state fields ([#18594](https://github.com/sveltejs/svelte/pull/18594))


## COMMIT SUBJECTS between the previous tag and the release

fix: increment private state fields through a non-`this` receiver (#18622)
fix: apply CSS custom properties with falsy values on components (#18634)
fix: preserve comment placement for server derived reads (#18641)
fix: give effect teardowns the value from before the first write in a flush (#18620)
 fix: remove stale capture listeners from spread attributes (#18618)
fix: transform expressions inside labeled statements during server compilation (#18617)
fix: prevent crash on async custom element attributes (#18661)
fix: skip Program comment nodes in migration to prevent crash (#18656)
fix: preserve logical assignments to private state fields (#18594)
fix: avoid double-calling a derived reference when destructuring (#18668)
fix: preserve CSS escape sequences when printing selectors (#18667)
fix: print `{#await ... catch}` et al correctly (#18645)
fix: preserve namespaces in CSS type selectors (#18678)
fix: preserve renderer type in copy() during SSR (#18616)
fix: append_styles resolving to `document.head` in WC (#18614)
fix: treat concise arrow function bodies as implicit returns when calculating blockers (#18613)
fix: parse nth-child `of` syntax without whitespace after `of` (#18611)
docs: note that transitions bypass CSS prefers-reduced-motion (#18597)
chore: deduplicate client/server context helpers (#18580)
docs: clarify that context lookup includes the current component and all ancestors (#18581)
chore: switch to @changesets/changelog-github (#18570)
fix: release last_propagated_event after event propagation settles (#18569)
fix: strip comments from inline style values in linear time (#18553)
perf: make async blocker analysis linear (#18549)
docs: note comments within tags possibility (#18482)
Version Packages (#18640)

# CANDIDATE A

## svelte@5.56.10

### Patch Changes

#### Compiler fixes

- Preserve CSS escape sequences when printing selectors ([#18667](https://github.com/sveltejs/svelte/pull/18667))
- Preserve namespaces in CSS type selectors ([#18678](https://github.com/sveltejs/svelte/pull/18678))
- Parse `:nth-child(2n of.foo)` when `of` isn't followed by whitespace ([#18611](https://github.com/sveltejs/svelte/pull/18611))
- Print `{#await ... catch x}` and similar blocks correctly ([#18645](https://github.com/sveltejs/svelte/pull/18645))
- Fix a migration script crash caused by comments on the Program node ([#18656](https://github.com/sveltejs/svelte/pull/18656))
- Treat concise arrow function bodies as implicit returns when calculating async blockers ([#18613](https://github.com/sveltejs/svelte/pull/18613))
- Preserve short-circuiting for logical assignments to private state fields ([#18594](https://github.com/sveltejs/svelte/pull/18594))
- Allow incrementing private state fields through a receiver other than `this` ([#18622](https://github.com/sveltejs/svelte/pull/18622))
- Strip comments from inline `style` values in linear time ([#18553](https://github.com/sveltejs/svelte/pull/18553))
- Speed up async blocker analysis so it scales linearly with the number of top-level references ([#18549](https://github.com/sveltejs/svelte/pull/18549))

#### Server-side rendering fixes

- Transform expressions inside labeled statements during server compilation ([#18617](https://github.com/sveltejs/svelte/pull/18617))
- Avoid calling a derived twice when destructuring a `$derived` of another `$derived` ([#18668](https://github.com/sveltejs/svelte/pull/18668))
- Stop comments in declarations from breaking derived references ([#18641](https://github.com/sveltejs/svelte/pull/18641))
- Avoid corrupting the renderer type during the legacy `bind:` retry loop ([#18616](https://github.com/sveltejs/svelte/pull/18616))

#### Runtime fixes

- Apply CSS custom properties with falsy values on components ([#18634](https://github.com/sveltejs/svelte/pull/18634))
- Resolve `append_styles` to the correct root in web components ([#18614](https://github.com/sveltejs/svelte/pull/18614))
- Remove stale capture event handlers from spread attributes ([#18618](https://github.com/sveltejs/svelte/pull/18618))
- Give effect teardowns the value from before the first write in a flush ([#18620](https://github.com/sveltejs/svelte/pull/18620))
- Allow custom elements to receive async values as props ([#18661](https://github.com/sveltejs/svelte/pull/18661))
- Release the last propagated event after propagation settles, so it no longer retains the target's subtree in memory ([#18569](https://github.com/sveltejs/svelte/pull/18569))

### Other

- Clarify that context lookup includes the current component and all ancestors ([#18581](https://github.com/sveltejs/svelte/pull/18581))
- Note that transitions bypass CSS `prefers-reduced-motion` ([#18597](https://github.com/sveltejs/svelte/pull/18597))
- Note that comments are allowed within tags ([#18482](https://github.com/sveltejs/svelte/pull/18482))
- Deduplicate client and server context helpers ([#18580](https://github.com/sveltejs/svelte/pull/18580))
- Switch to `@changesets/changelog-github` ([#18570](https://github.com/sveltejs/svelte/pull/18570))


# CANDIDATE B

## svelte@5.56.10

### Patch Changes

#### Compiler

- Fix server compilation not transforming expressions inside labeled statements ([#18617](https://github.com/sveltejs/svelte/pull/18617))
- Fix a derived reference being called twice when destructuring a `$derived` of another `$derived` during server-side rendering ([#18668](https://github.com/sveltejs/svelte/pull/18668))
- Fix declaration comments breaking server derived references ([#18641](https://github.com/sveltejs/svelte/pull/18641))
- Fix the renderer type being corrupted during SSR's legacy `bind:` retry loop ([#18616](https://github.com/sveltejs/svelte/pull/18616))
- Treat concise arrow function bodies as implicit returns when calculating async blockers ([#18613](https://github.com/sveltejs/svelte/pull/18613))
- Fix incrementing private state fields through a non-`this` receiver ([#18622](https://github.com/sveltejs/svelte/pull/18622))
- Preserve short-circuiting for logical assignments to private state fields ([#18594](https://github.com/sveltejs/svelte/pull/18594))
- Fix parsing `:nth-child(2n of.foo)` when `of` isn't followed by whitespace ([#18611](https://github.com/sveltejs/svelte/pull/18611))
- Preserve namespaces in CSS type selectors ([#18678](https://github.com/sveltejs/svelte/pull/18678))
- Strip comments from inline `style` values in linear time ([#18553](https://github.com/sveltejs/svelte/pull/18553))
- Make async blocker analysis scale linearly with the number of top-level references ([#18549](https://github.com/sveltejs/svelte/pull/18549))

#### Printing and migration

- Preserve CSS escape sequences when printing selectors ([#18667](https://github.com/sveltejs/svelte/pull/18667))
- Print `{#await ... catch x}` and similar blocks correctly ([#18645](https://github.com/sveltejs/svelte/pull/18645))
- Ignore comments of the Program node in the migration script ([#18656](https://github.com/sveltejs/svelte/pull/18656))

#### Runtime

- Apply CSS custom properties with falsy values on components ([#18634](https://github.com/sveltejs/svelte/pull/18634))
- Resolve `append_style` to its correct root reliably ([#18614](https://github.com/sveltejs/svelte/pull/18614))
- Clean up removed capture event handlers from spread attributes ([#18618](https://github.com/sveltejs/svelte/pull/18618))
- Give effect teardowns the value from before the first write in a flush ([#18620](https://github.com/sveltejs/svelte/pull/18620))
- Allow custom elements to receive async values as props ([#18661](https://github.com/sveltejs/svelte/pull/18661))
- Release `last_propagated_event` after event propagation settles, so it no longer retains the last event's target subtree ([#18569](https://github.com/sveltejs/svelte/pull/18569))

#### Other

- Docs: clarify that context lookup includes the current component and all ancestors ([#18581](https://github.com/sveltejs/svelte/pull/18581))
- Docs: note that comments within tags are possible ([#18482](https://github.com/sveltejs/svelte/pull/18482))
- Deduplicate client and server context helpers ([#18580](https://github.com/sveltejs/svelte/pull/18580))

