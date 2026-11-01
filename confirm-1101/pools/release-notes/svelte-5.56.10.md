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
