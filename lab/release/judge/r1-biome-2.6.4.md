# Judge file r1-biome-2.6.4

## PUBLISHED RELEASE NOTES (written by the maintainers)

## 2.6.4

### Patch Changes

- [#12261](https://github.com/biomejs/biome/pull/12261) [`19fbfb2`](https://github.com/biomejs/biome/commit/19fbfb2311b5dc4bf1b6ee8dd5b258d9699436a5) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`noConsoleSpaces`](https://biomejs.dev/linter/rules/no-console-spaces/), which reports a leading or trailing space in a `console.log()`, `console.debug()`, `console.info()`, `console.warn()`, or `console.error()` argument that sits next to another argument. These methods already put a space between arguments, so such a space prints twice.
  
  ```js
  console.log("abc ", "def");
  ```

- [#12469](https://github.com/biomejs/biome/pull/12469) [`cd716d3`](https://github.com/biomejs/biome/commit/cd716d38575ce603d8cddbabec97b3d52463858b) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`noMagicArrayFlatDepth`](https://biomejs.dev/linter/rules/no-magic-array-flat-depth/), which reports number literals other than `1` passed as the depth of `Array.prototype.flat()` unless a comment inside the parentheses explains them.
  
  ```js
  const items = array.flat(2);
  ```

- [#12470](https://github.com/biomejs/biome/pull/12470) [`92c9e81`](https://github.com/biomejs/biome/commit/92c9e81bd7c767b4b3e583a312f75c0f364298dd) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noNull`](https://biomejs.dev/linter/rules/no-null/), which reports uses of the `null` literal and suggests `undefined` instead. Strict comparisons such as `foo === null` are allowed.
  
  ```js
  let foo = null;
  ```

- [#12483](https://github.com/biomejs/biome/pull/12483) [`9bd3527`](https://github.com/biomejs/biome/commit/9bd35277c99fffa6b252a594a2a74e553e977b3b) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noReturnArrayPush`](https://biomejs.dev/linter/rules/no-return-array-push/), which reports code that uses the return value of `push()` or `unshift()`. These methods return the new length of the array, not the added item or the array.
  
  ```js
  function add(item) {
    return items.push(item);
  }
  ```

- [#12477](https://github.com/biomejs/biome/pull/12477) [`a384892`](https://github.com/biomejs/biome/commit/a384892c6b9f882b9c1751bf725cb84d9c8738b6) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noUnreadableIife`](https://biomejs.dev/linter/rules/no-unreadable-iife/), which reports arrow functions that are called right where they are defined and whose body is wrapped in parentheses.
  
  ```js
  const foo = (bar => (bar ? bar.baz : baz))(getBar());
  ```

- [#12447](https://github.com/biomejs/biome/pull/12447) [`0a963e4`](https://github.com/biomejs/biome/commit/0a963e4a30cfb550e0994bd925d16391e725bf4f) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noUselessRecursion`](https://biomejs.dev/linter/rules/no-useless-recursion/), which reports functions that return a call to themselves when a loop can do the same work. Too many nested calls can crash the program with a stack overflow error.
  
  ```js
  function findRoot(node) {
      if (node.parent) {
          return findRoot(node.parent);
      }
      return node;
  }
  ```

- [#12554](https://github.com/biomejs/biome/pull/12554) [`2eddda9`](https://github.com/biomejs/biome/commit/2eddda9046fc36aa5ef455d8fd57b2900b7dc319) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noVueComputedPropertiesInData`](https://biomejs.dev/linter/rules/no-vue-computed-properties-in-data/), which reports computed properties used inside the `data` function of a Vue component. Vue runs `data` before it sets up computed properties, so the value read there is `undefined`.
  
  ```vue
  <script>
  export default {
    data() {
      return { total: this.doubled };
    },
    computed: {
      doubled() {
        return 2;
      },
    },
  };
  </script>
  ```

- [#12586](https://github.com/biomejs/biome/pull/12586) [`824df15`](https://github.com/biomejs/biome/commit/824df15e1e7c4bd433c3efaa999c4aa3e495c625) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noVueDeprecatedDeleteSet`](https://biomejs.dev/linter/rules/no-vue-deprecated-delete-set/), which reports calls to the `$set` and `$delete` functions, `Vue.set` and `Vue.delete`, and `set` and `del` imported from `vue`. Vue 3 removed these functions, so calling them throws an error.
  
  ```vue
  <script>
  export default {
    mounted() {
      this.$set(this.user, "name", "Alice");
    },
  };
  </script>
  ```

- [#12648](https://github.com/biomejs/biome/pull/12648) [`6fc1a51`](https://github.com/biomejs/biome/commit/6fc1a51e9e9493c6519892e10478d2e1fdf226db) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noVueDeprecatedRouterLinkTagProp`](https://biomejs.dev/linter/rules/no-vue-deprecated-router-link-tag-prop/), which disallows the `tag` prop on `RouterLink`. Vue Router 4 ignores this prop, so the link still renders as an `<a>` element.
  
  ```vue
  <template>
    <RouterLink tag="li" to="/">Home</RouterLink>
  </template>
  ```

- [#12631](https://github.com/biomejs/biome/pull/12631) [`de1188f`](https://github.com/biomejs/biome/commit/de1188fce7bd6205361225ae53c6dc32d16f3600) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`noVueDeprecatedScopeAttribute`](https://biomejs.dev/linter/rules/no-vue-deprecated-scope-attribute/), which reports the `scope` attribute on `<template>` elements in Vue files. Vue no longer supports this attribute, so use `v-slot` to receive slot props instead.
  
  ```vue
  <template>
    <ListComponent>
      <template scope="props">{{ props.title }}</template>
    </ListComponent>
  </template>
  ```

- [#12562](https://github.com/biomejs/biome/pull/12562) [`5d7553b`](https://github.com/biomejs/biome/commit/5d7553b94a472c8f4e9739b35efd15eb56eff7dd) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`noVueMultipleSlotArgs`](https://biomejs.dev/linter/rules/no-vue-multiple-slot-args/), which disallows passing more than one argument to a Vue slot from a render function. Slot content written in a template receives only the first argument.
  
  ```vue
  <script>
  export default {
    render() {
      return this.$slots.default(item, index); // reported
    },
  };
  </script>
  ```

- [#12513](https://github.com/biomejs/biome/pull/12513) [`2e520d8`](https://github.com/biomejs/biome/commit/2e520d81799678deedd2de0ef0f9be1c071415c3) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noVueMutatingProps`](https://biomejs.dev/linter/rules/no-vue-mutating-props/), which reports code that changes the props of a Vue component, in the script or in the template. Props belong to the parent component, so the child should emit an event or copy the value instead.
  
  ```vue
  <script setup>
  const props = defineProps({ items: Array });
  
  props.items.push("new item");
  </script>
  ```

- [#12567](https://github.com/biomejs/biome/pull/12567) [`144b786`](https://github.com/biomejs/biome/commit/144b7865bc9981258929e742785d75946b6bc077) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noVueSideEffectsInComputed`](https://biomejs.dev/linter/rules/no-vue-side-effects-in-computed/), which reports Vue computed properties that change state. Vue decides when to run a computed property, so changes made inside one happen at unpredictable times.
  
  ```vue
  <script setup>
  import { computed, ref } from "vue";
  
  const items = ref([]);
  // `reverse()` changes `items.value` in place.
  const reversedItems = computed(() => items.value.reverse());
  </script>
  ```

- [#12603](https://github.com/biomejs/biome/pull/12603) [`861b288`](https://github.com/biomejs/biome/commit/861b2888c4a8ab324f888cfc2d9b68a5cb41671c) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`noVueUnusedRefs`](https://biomejs.dev/linter/rules/no-vue-unused-refs/), which reports template refs in Vue components that nothing reads through `$refs`, `useTemplateRef()`, or a variable of the same name in `<script setup>`. The rule needs `html.experimentalFullSupportEnabled` to be `true`.
  
  ```vue
  <template>
    <input ref="input" />
  </template>
  ```

- [#12285](https://github.com/biomejs/biome/pull/12285) [`68770e0`](https://github.com/biomejs/biome/commit/68770e008365f0351d82c39cc6498293e4717110) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`noYamlBooleanKeys`](https://biomejs.dev/linter/rules/no-yaml-boolean-keys/), which disallows boolean values as keys in YAML. For example, the following key is a boolean instead of text, so it is reported:
  
  ```yaml
  true: enabled
  ```

- [#12338](https://github.com/biomejs/biome/pull/12338) [`f46411b`](https://github.com/biomejs/biome/commit/f46411b97772e24221dc1a8f406c8d07004f23e3) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useSvelteEventDispatcherTypes`](https://biomejs.dev/linter/rules/use-svelte-event-dispatcher-types/), which reports `createEventDispatcher()` calls that don't declare the types of their events in Svelte components written in TypeScript.
  
  The rule accepts a call that declares its events:
  
  ```svelte
  <script lang="ts">
    import { createEventDispatcher } from "svelte";
  
    const dispatch = createEventDispatcher<{ save: string }>();
  </script>
  ```

- [#12615](https://github.com/biomejs/biome/pull/12615) [`ade9845`](https://github.com/biomejs/biome/commit/ade9845477b4914fb07d47c64fe0cb1b29aec9d5) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueDefineOptions`](https://biomejs.dev/linter/rules/use-vue-define-options/), which reports the default export of a plain `<script>` block in Vue components that also use `<script setup>`, and suggests setting those options with `defineOptions()` instead.
  
  ```vue
  <script>
  export default { name: "MyComponent" }; // reported
  </script>
  
  <script setup>
  const props = defineProps(["title"]);
  </script>
  ```

- [#12514](https://github.com/biomejs/biome/pull/12514) [`e74b4dc`](https://github.com/biomejs/biome/commit/e74b4dc1cdf066076f67be9c9b437fa1ce0a1e07) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueDefinePropsDestructuring`](https://biomejs.dev/linter/rules/use-vue-define-props-destructuring/), which requires destructuring the props returned by `defineProps()` in Vue `<script setup>` blocks. It also reports `withDefaults()`, because destructured props can set their default values directly.
  
  ```vue
  <script setup lang="ts">
  const props = defineProps<{ foo?: string }>();
  </script>
  ```

- [#12559](https://github.com/biomejs/biome/pull/12559) [`94985ba`](https://github.com/biomejs/biome/commit/94985ba66b7cfbab5b8e66fe8b925ea7de074fd3) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueTemplateRef`](https://biomejs.dev/linter/rules/use-vue-template-ref/), which requires `useTemplateRef()` instead of `ref()` or `shallowRef()` to access elements of the template in `<script setup>`.
  
  ```vue
  <template>
    <input ref="input" />
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const input = ref(); // reported
  </script>
  ```

- [#12512](https://github.com/biomejs/biome/pull/12512) [`6be5078`](https://github.com/biomejs/biome/commit/6be5078e64484b64eae77510742dfd8cb2fe95ae) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueTypedProps`](https://biomejs.dev/linter/rules/use-vue-typed-props/), which reports Vue props declared without a type, in the `props` option, `defineProps()`, or `defineModel()`. Without a type, Vue accepts any value for the prop and can't warn when a component receives the wrong kind of value.
  
  ```vue
  <script setup>
  defineProps(["title"]);
  </script>
  ```

- [#12653](https://github.com/biomejs/biome/pull/12653) [`f307633`](https://github.com/biomejs/biome/commit/f30763352aff8b5a4f5269ffd3c1c026192da22e) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueVModel`](https://biomejs.dev/linter/rules/use-vue-v-model/), which reports a prop binding on a Vue component paired with an `update:` listener that only writes the new value back, and suggests `v-model` instead.
  
  ```vue
  <template>
    <MyComponent :title="title" @update:title="title = $event" />
  </template>
  ```

- [#12591](https://github.com/biomejs/biome/pull/12591) [`a810209`](https://github.com/biomejs/biome/commit/a810209d4f09e9c07b8ec73ef05480ad0e17c1eb) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueValidDefineEmits`](https://biomejs.dev/linter/rules/use-vue-valid-define-emits/), which enforces valid usage of Vue's `defineEmits` macro in `<script setup>`.
  
  For example, the following code is now reported, because `defineEmits` declares its events with both a type and an argument:
  
  ```vue
  <script setup lang="ts">
  const emit = defineEmits<(e: "notify") => void>(["submit"]);
  </script>
  ```

- [#12614](https://github.com/biomejs/biome/pull/12614) [`9308110`](https://github.com/biomejs/biome/commit/9308110c3c5c7c84675f1f4bf419c3dd65031254) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueValidDefineProps`](https://biomejs.dev/linter/rules/use-vue-valid-define-props/), which reports `defineProps()` calls that Vue can't compile or that declare props incorrectly. For example, it reports a component that calls `defineProps()` twice, or whose `defineProps()` argument uses a variable declared in `<script setup>`:
  
  ```vue
  <script setup>
  const definition = { msg: String };
  defineProps(definition);
  </script>
  ```

- [#12570](https://github.com/biomejs/biome/pull/12570) [`222a230`](https://github.com/biomejs/biome/commit/222a230c6026a9a741dddbe35a10dd1507d3e978) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueValidVIs`](https://biomejs.dev/linter/rules/use-vue-valid-v-is/), which reports `v-is` directives that have an argument or modifiers, have no value, or are used on a component instead of a native HTML element.
  
  For example, the following `v-is` directive has no value:
  
  ```vue
  <template>
    <tr v-is></tr>
  </template>
  ```

- [#12521](https://github.com/biomejs/biome/pull/12521) [`4010bb7`](https://github.com/biomejs/biome/commit/4010bb76235ef66297c1cc4ebc97df40653f5e89) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueValidVMemo`](https://biomejs.dev/linter/rules/use-vue-valid-v-memo/), which reports invalid `v-memo` directives in Vue templates. A `v-memo` directive must have an array value, can't have an argument or modifiers, and doesn't work inside an element with `v-for`.
  
  For example, the following value is an object instead of an array:
  
  ```vue
  <template>
    <div v-memo="{ id }"></div>
  </template>
  ```

- [#12597](https://github.com/biomejs/biome/pull/12597) [`aff42a7`](https://github.com/biomejs/biome/commit/aff42a73b0f03fc477d86208d44aff71df62acc4) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueValidVModel`](https://biomejs.dev/linter/rules/use-vue-valid-v-model/), which reports `v-model` directives that Vue can't use: on unsupported elements or file inputs, with an argument or unknown modifier on a native element, without a value, or with a value that can't be assigned to.
  
  For example, the following `v-model` directives are invalid:
  
  ```vue
  <template>
    <div v-model="foo"></div>
    <input v-model="foo + bar" />
  </template>
  ```

- [#12569](https://github.com/biomejs/biome/pull/12569) [`3058597`](https://github.com/biomejs/biome/commit/3058597e79e4e79438432ede4d729a1907dd945c) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`useVueValidVShow`](https://biomejs.dev/linter/rules/use-vue-valid-v-show/), which reports `v-show` directives that have an argument, a modifier, or no value, or that are placed on a `<template>` element.
  
  ```vue
  <template v-show="isVisible"><div></div></template>
  ```

- [#12525](https://github.com/biomejs/biome/pull/12525) [`e2e5a36`](https://github.com/biomejs/biome/commit/e2e5a36e1be8581419742a85268ad82f020da62e) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`useVueValidVSlot`](https://biomejs.dev/linter/rules/use-vue-valid-v-slot/), which reports misplaced, duplicated, or malformed `v-slot` directives in Vue templates.
  
  For example, the rule reports two `<template>` elements that fill the same slot:
  
  ```vue
  <MyComponent>
    <template #header>First title</template>
    <template #header>Second title</template>
  </MyComponent>
  ```

- [#12472](https://github.com/biomejs/biome/pull/12472) [`efd16bd`](https://github.com/biomejs/biome/commit/efd16bd44d84ad0580d59d27bba6843323761b42) Thanks [@dyc3](https://github.com/dyc3)! - Added the new nursery rule [`useWhileLoopCondition`](https://biomejs.dev/linter/rules/use-while-loop-condition/), which reports loops such as `while (true)` and `for (;;)` that start with an `if` statement containing only a `break`, and moves that condition into the `while` statement.
  
  ```js
  while (true) {
    if (!hasMore()) {
      break;
    } // reported
    processNext();
  }
  ```

- [#12640](https://github.com/biomejs/biome/pull/12640) [`167bb00`](https://github.com/biomejs/biome/commit/167bb00ed962640cb72bc1d896fd5f6e98e8ef4d) Thanks [@latin-1](https://github.com/latin-1)! - Updated [`useSortedProperties`](https://biomejs.dev/assist/actions/use-sorted-properties/) to follow `stylelint-config-recess-order` 7.9.0, adding sorting support for `scroll-behavior`, anchor positioning, multi-column layout, and other properties known to Biome.

- [#12719](https://github.com/biomejs/biome/pull/12719) [`40a82b0`](https://github.com/biomejs/biome/commit/40a82b0c5e11d825c3b3d42fc56950ca53d4b79a) Thanks [@dyc3](https://github.com/dyc3)! - Improved the performance of the linter. Biome now spends less time setting up the enabled rules for each file it analyzes.

- [#12722](https://github.com/biomejs/biome/pull/12722) [`f074730`](https://github.com/biomejs/biome/commit/f07473021c756cc1e3f2582b55959b91878a1d1a) Thanks [@dyc3](https://github.com/dyc3)! - Improved the performance of `biome lint` by about 1% to 3% on large projects, most noticeably with Biome's default rules and with rules that track variables or unreachable code.

- [#12501](https://github.com/biomejs/biome/pull/12501) [`90a4d74`](https://github.com/biomejs/biome/commit/90a4d74f206dd262f82bfdb2dda7420bde3770a3) Thanks [@ematipico](https://github.com/ematipico)! - Fixed [#12466](https://github.com/biomejs/biome/issues/12466): the Biome daemon used more memory with every `biome check --use-server` run. The daemon now reuses the data that it stores for each file and project, and it keeps syntax trees only for the files that it read most recently.

- [#12501](https://github.com/biomejs/biome/pull/12501) [`90a4d74`](https://github.com/biomejs/biome/commit/90a4d74f206dd262f82bfdb2dda7420bde3770a3) Thanks [@ematipico](https://github.com/ematipico)! - Fixed [biomejs/biome-vscode#923](https://github.com/biomejs/biome-vscode/issues/923): when a file open in the editor changed on disk, the language server replaced the editor's text with the text on disk. Biome now keeps the editor's text of open files until they are closed, so diagnostics, code actions and formatting stay at the right positions.

- [#12652](https://github.com/biomejs/biome/pull/12652) [`59ff42a`](https://github.com/biomejs/biome/commit/59ff42a79c795edd9bbdc64719bb43b7d4cf822c) Thanks [@kurovskyiii](https://github.com/kurovskyiii)! - Fixed [#12651](https://github.com/biomejs/biome/issues/12651): an imported name that the other module exports as both a type and a value now resolves to the type in type annotations, so [`noBaseToString`](https://biomejs.dev/linter/rules/no-base-to-string/) no longer reports `slug` below as an object.
  
  ```ts
  // rule-slug.ts
  export type RuleSlug = string;
  export const RuleSlug = { create: (text: string): RuleSlug => text } as const;
  
  // main.ts
  import { RuleSlug } from "./rule-slug";
  export const label = (slug: RuleSlug): string => `rule ${slug}`;
  ```

- [#12678](https://github.com/biomejs/biome/pull/12678) [`301402f`](https://github.com/biomejs/biome/commit/301402f9bcaec9087dc00fac2d2240880dc48921) Thanks [@nhedger](https://github.com/nhedger)! - Fixed [biomejs/biome-vscode#1113](https://github.com/biomejs/biome-vscode/issues/1113): the language server now shows a warning when the configuration file can't be parsed. Previously, Biome stopped processing files without telling the user why.

- [#12662](https://github.com/biomejs/biome/pull/12662) [`8c836eb`](https://github.com/biomejs/biome/commit/8c836eb1b7e80af3674dfd124887612c5f975faa) Thanks [@dyc3](https://github.com/dyc3)! - Fixed [#12645](https://github.com/biomejs/biome/issues/12645): the Markdown formatter no longer removes the blank line between a blockquote and the list that follows it, matching Prettier.
  
  ```md
  > A note.
  
  - one
  - two
  ```

- [#12662](https://github.com/biomejs/biome/pull/12662) [`8c836eb`](https://github.com/biomejs/biome/commit/8c836eb1b7e80af3674dfd124887612c5f975faa) Thanks [@dyc3](https://github.com/dyc3)! - Fixed [#12663](https://github.com/biomejs/biome/issues/12663): the Markdown formatter no longer removes the blank line between a table and the list that follows it, matching Prettier.
  
  ```md
  | Table |
  | ----- |
  | Value |
  
  - Hello
  ```

- [#12576](https://github.com/biomejs/biome/pull/12576) [`735d370`](https://github.com/biomejs/biome/commit/735d37073eb0c213dab5caf75db1e0bdbcb580cc) Thanks [@jfmcdowell](https://github.com/jfmcdowell)! - Fixed [#12541](https://github.com/biomejs/biome/issues/12541): Markdown list items whose markers are indented 4 or more spaces now nest at the correct level. Previously the formatter could move such an item under the item before it, or join it to that item's text.
  
  ```diff
   1. Step
      - a
        - x
  -       - y
  -         - b
  +     - y
  +   - b
  ```

- [#12575](https://github.com/biomejs/biome/pull/12575) [`0da9080`](https://github.com/biomejs/biome/commit/0da9080f34514c18cdc012e75b4c18d113c7ca01) Thanks [@jfmcdowell](https://github.com/jfmcdowell)! - Fixed formatting of Markdown block quotes inside deeply indented list items. With `proseWrap: "always"`, consecutive quote lines now wrap together within the same quote, while setext headings and fenced code blocks keep their structure.
  
  ```diff
   10. item
  -    > first line
  -    > second line
  +    > first line second line
  ```

- [#12607](https://github.com/biomejs/biome/pull/12607) [`896d53e`](https://github.com/biomejs/biome/commit/896d53eff2984a8e96d39f4419dd12ccdff15493) Thanks [@xucian](https://github.com/xucian)! - Fixed [#12542](https://github.com/biomejs/biome/issues/12542): the Markdown formatter is no longer idempotent when it formats tables.
  
  ```diff
  - | a        | b     |
  - | -------- | ----- |
  - | x        | `y` z |
  - | `p` z`q` | r     |
  + | a         | b     |
  + | --------- | ----- |
  + | x         | `y` z |
  + | `p` z `q` | r     |
  ```

- [#12692](https://github.com/biomejs/biome/pull/12692) [`8ff63f4`](https://github.com/biomejs/biome/commit/8ff63f42593e4fbc92679d6585320b950b20381d) Thanks [@NikitaCOEUR](https://github.com/NikitaCOEUR)! - Fixed the `linux-x64-musl` binary not using jemalloc, which it already ships: it fell back to musl's allocator, and `biome check` on several threads could take minutes instead of seconds, for example in Alpine-based CI images.

- [#12682](https://github.com/biomejs/biome/pull/12682) [`fa7cf4c`](https://github.com/biomejs/biome/commit/fa7cf4c0511ac2a07d6af42064c4108488aca0c6) Thanks [@dyc3](https://github.com/dyc3)! - Fixed [#12679](https://github.com/biomejs/biome/issues/12679): when `markdown.parser.frontmatter` and `markdown.formatter.formatEmbeds` are enabled, the Markdown formatter keeps the frontmatter of a fenced Markdown code block as written. Previously, it formatted the frontmatter as a thematic break and a paragraph, which removed the indentation of its YAML.
  
  ````md
  ```markdown
  ---
  verified:
    by: human
  ---
  # Policy
  ```
  ````

- [#12649](https://github.com/biomejs/biome/pull/12649) [`343c8ca`](https://github.com/biomejs/biome/commit/343c8ca9cc718d76717b334338cc7eff94b0d426) Thanks [@JamBalaya56562](https://github.com/JamBalaya56562)! - Fixed [#12643](https://github.com/biomejs/biome/issues/12643) and [#12669](https://github.com/biomejs/biome/issues/12669): Biome now migrates the Prettier option `bracketSpacing` to `formatter.bracketSpacing`, both at the top level and inside `overrides`. JSON and GraphQL files are now formatted with the same bracket spacing as JavaScript files.

- [#12640](https://github.com/biomejs/biome/pull/12640) [`167bb00`](https://github.com/biomejs/biome/commit/167bb00ed962640cb72bc1d896fd5f6e98e8ef4d) Thanks [@latin-1](https://github.com/latin-1)! - Fixed [`useSortedProperties`](https://biomejs.dev/assist/actions/use-sorted-properties/) to withhold sorting fixes that would change the effective values of overlapping declarations, physical/logical border or corner properties, or declarations followed by `all`.
  Updated [`noShorthandPropertyOverrides`](https://biomejs.dev/linter/rules/no-shorthand-property-overrides/) to recognize logical border, corner shape, `position-try`, `text-box`, and `transition-behavior` overrides.

- [#12723](https://github.com/biomejs/biome/pull/12723) [`b6cbec8`](https://github.com/biomejs/biome/commit/b6cbec881cd6e10381ee6194aa6e2437c47b6e28) Thanks [@dyc3](https://github.com/dyc3)! - Improved the performance of `biome lint`, `biome check`, and `biome ci` on files where rules report diagnostics with code fixes, by up to 12% with the default rules.

- [#12664](https://github.com/biomejs/biome/pull/12664) [`6021da0`](https://github.com/biomejs/biome/commit/6021da0fad40d556123ff227b9034cbed90b2ea2) Thanks [@MindTooth](https://github.com/MindTooth)! - Fixed Biome processing `pnpm-lock.yaml` files. These generated lockfiles are now protected from processing.

- [#12501](https://github.com/biomejs/biome/pull/12501) [`90a4d74`](https://github.com/biomejs/biome/commit/90a4d74f206dd262f82bfdb2dda7420bde3770a3) Thanks [@ematipico](https://github.com/ematipico)! - Fixed an issue where the CLI, when it ran with `--use-server` alongside an editor connected to the same daemon, checked the unsaved text of the files open in the editor instead of the files on disk, and could make the editor's text get lost. The CLI now checks the files on disk, and every editor and CLI run connected to the daemon keeps its own text of the files it opens.

- [#12519](https://github.com/biomejs/biome/pull/12519) [`9ae56ba`](https://github.com/biomejs/biome/commit/9ae56ba6e2cac09c4883fd0cf5fa21d3a94751a0) Thanks [@dyc3](https://github.com/dyc3)! - The rule [`noVueVIfWithVFor`](https://biomejs.dev/linter/rules/no-vue-v-if-with-v-for/) now also reports `v-else-if` and `v-else` on the same element as `v-for`.
  
  ```vue
  <div v-if="loading">Loading...</div>
  <TodoItem v-else v-for="todo in todos" :todo="todo" />
  ```

- [#12702](https://github.com/biomejs/biome/pull/12702) [`df0f7cc`](https://github.com/biomejs/biome/commit/df0f7ccad27358a61a6b60f8e4a2992097c3a29b) Thanks [@dyc3](https://github.com/dyc3)! - Fixed parsing of default values in Vue `v-for` bindings. Biome now parses the default value as JavaScript, so it is formatted and linted like other template expressions instead of being reported as a parse error.
  
  ```vue
  <div v-for="{ value = gt('v-for default') } in rows" />
  ```

- [#12656](https://github.com/biomejs/biome/pull/12656) [`25a00a2`](https://github.com/biomejs/biome/commit/25a00a2a4c61eb24923ff8c91f60672320c80833) Thanks [@dyc3](https://github.com/dyc3)! - Fixed non-JSON files inside the global settings directories of Zed, VS Code, and Cursor being parsed as JSON.

- [#12501](https://github.com/biomejs/biome/pull/12501) [`90a4d74`](https://github.com/biomejs/biome/commit/90a4d74f206dd262f82bfdb2dda7420bde3770a3) Thanks [@ematipico](https://github.com/ematipico)! - Fixed an issue where the language server kept using the previous parser options for open files after the configuration changed. Open files are now parsed again with the new options, for example `json.parser.allowComments`.

- [#12656](https://github.com/biomejs/biome/pull/12656) [`25a00a2`](https://github.com/biomejs/biome/commit/25a00a2a4c61eb24923ff8c91f60672320c80833) Thanks [@dyc3](https://github.com/dyc3)! - Improved the performance of Biome when it processes many files by up to 7%.

- [#12661](https://github.com/biomejs/biome/pull/12661) [`066a077`](https://github.com/biomejs/biome/commit/066a077c28ddd1d39bc10ca60afa592ad02cf2f5) Thanks [@dyc3](https://github.com/dyc3)! - Added the nursery rule [`noVueDeprecatedListeners`](https://biomejs.dev/linter/rules/no-vue-deprecated-listeners/). It reports references to `$listeners`, which Vue 3 removed, in Vue templates and component objects. For example, Biome now reports `<div v-on="$listeners" />` and `this.$listeners` inside a Vue component.



## What's Changed
* feat(lint): add useWhileLoopCondition by @dyc3 in https://github.com/biomejs/biome/pull/12472
* refactor(analyze): remove the rule-count limit on analyzer groups by @dyc3 in https://github.com/biomejs/biome/pull/12637
* fix(migrate): carry Prettier's bracketSpacing in overrides by @JamBalaya56562 in https://github.com/biomejs/biome/pull/12649
* fix(format/md): preserve newline between block quote and list by @dyc3 in https://github.com/biomejs/biome/pull/12662
* feat(lint): add noNull by @dyc3 in https://github.com/biomejs/biome/pull/12470
* fix(migrate): carry Prettier's bracketSpacing into the top-level by @JamBalaya56562 in https://github.com/biomejs/biome/pull/12670
* fix: mark pnpm-lock.yaml as protected file by @MindTooth in https://github.com/biomejs/biome/pull/12664
* fix(markdown_parser): attach whitespace before a table pipe to the pipe by @xucian in https://github.com/biomejs/biome/pull/12607
* feat(lint): add noYamlBooleanKeys by @dyc3 in https://github.com/biomejs/biome/pull/12285
* feat(lint): add noUnreadableIife by @dyc3 in https://github.com/biomejs/biome/pull/12477
* feat(lint): add useSvelteEventDispatcherTypes by @dyc3 in https://github.com/biomejs/biome/pull/12338
* feat(lint): add noMagicArrayFlatDepth by @dyc3 in https://github.com/biomejs/biome/pull/12469
* feat(lint): add noConsoleSpaces by @dyc3 in https://github.com/biomejs/biome/pull/12261
* perf(languages): resolve editor settings directories once, and check less often by @dyc3 in https://github.com/biomejs/biome/pull/12656
* feat(lint): add noUselessRecursion by @dyc3 in https://github.com/biomejs/biome/pull/12447
* fix(css): sync recess property order and preserve cascade when sorting by @latin-1 in https://github.com/biomejs/biome/pull/12640
* feat(lint): add noReturnArrayPush by @dyc3 in https://github.com/biomejs/biome/pull/12483
* fix(lsp): warn when the configuration file can't be loaded by @nhedger in https://github.com/biomejs/biome/pull/12678
* chore(deps): update rust crate notify to 8.2.1 by @renovate[bot] in https://github.com/biomejs/biome/pull/12689
* fix(module_graph): resolve an imported type merged with a value to the type in annotations by @kurovskyiii in https://github.com/biomejs/biome/pull/12652
* fix(markdown): keep frontmatter of fenced Markdown blocks when formatting embeds by @dyc3 in https://github.com/biomejs/biome/pull/12682
* chore(deps): update rust crate serde_json to 1.0.154 by @renovate[bot] in https://github.com/biomejs/biome/pull/12690
* chore(deps): update rust crate smallvec to 1.16.4 by @renovate[bot] in https://github.com/biomejs/biome/pull/12691
* fix(markdown_parser): continue block quotes inside deep list items by @jfmcdowell in https://github.com/biomejs/biome/pull/12575
* chore: update rule metadata by @dyc3 in https://github.com/biomejs/biome/pull/12699
* perf(lint): make noDuplicateCase, noDuplicateElseIf and noFallthroughSwitchClause linear by @dyc3 in https://github.com/biomejs/biome/pull/12457
* perf(lint): speed up useHookAtTopLevel, noUnusedImports and noUnusedPrivateClassMembers by @dyc3 in https://github.com/biomejs/biome/pull/12458
* feat(lint): add useVueTemplateRef by @dyc3 in https://github.com/biomejs/biome/pull/12559
* feat(lint): add useVueValidVShow by @dyc3 in https://github.com/biomejs/biome/pull/12569
* feat(lint): add useVueDefinePropsDestructuring by @dyc3 in https://github.com/biomejs/biome/pull/12514
* feat(lint): add useVueValidVIs by @dyc3 in https://github.com/biomejs/biome/pull/12570
* feat(noVueVIfWithVFor): report v-else and v-else-if with v-for by @dyc3 in https://github.com/biomejs/biome/pull/12519
* feat(lint): add noVueSideEffectsInComputed by @dyc3 in https://github.com/biomejs/biome/pull/12567
* feat(lint): add noVueDeprecatedListeners by @dyc3 in https://github.com/biomejs/biome/pull/12661
* feat(lint): add useVueValidVModel by @dyc3 in https://github.com/biomejs/biome/pull/12597
* feat(lint): add useVueValidVSlot by @dyc3 in https://github.com/biomejs/biome/pull/12525
* fix(markdown_parser): nest list items by enclosing content column by @jfmcdowell in https://github.com/biomejs/biome/pull/12576
* chore(deps): update rust:1.98.0-bullseye docker digest to 4730e38 by @renovate[bot] in https://github.com/biomejs/biome/pull/11645
* feat(lint): add useVueValidVMemo by @dyc3 in https://github.com/biomejs/biome/pull/12521
* feat(lint): add useVueValidDefineProps by @dyc3 in https://github.com/biomejs/biome/pull/12614
* feat(lint): add useVueTypedProps by @dyc3 in https://github.com/biomejs/biome/pull/12512
* feat(lint): add useVueVModel by @dyc3 in https://github.com/biomejs/biome/pull/12653
* feat(lint): add useVueValidDefineEmits by @dyc3 in https://github.com/biomejs/biome/pull/12591
* feat(lint): add noVueDeprecatedRouterLinkTagProp by @dyc3 in https://github.com/biomejs/biome/pull/12648
* chore: move myself to core by @Netail in https://github.com/biomejs/biome/pull/12713
* feat(lint): add useVueDefineOptions by @dyc3 in https://github.com/biomejs/biome/pull/12615
* feat(lint): add noVueMutatingProps by @dyc3 in https://github.com/biomejs/biome/pull/12513
* feat(lint): add noVueDeprecatedScopeAttribute by @dyc3 in https://github.com/biomejs/biome/pull/12631
* feat(lint): add noVueMultipleSlotArgs by @dyc3 in https://github.com/biomejs/biome/pull/12562
* fix(cli): use jemalloc on x86_64 musl by @NikitaCOEUR in https://github.com/biomejs/biome/pull/12692
* feat(lint): add noVueComputedPropertiesInData by @dyc3 in https://github.com/biomejs/biome/pull/12554
* refactor: source text as input by @ematipico in https://github.com/biomejs/biome/pull/12501
* refactor(core): scanner epoch and LRU eviction by @ematipico in https://github.com/biomejs/biome/pull/12694
* perf(rowan): read node text from the green tree by @dyc3 in https://github.com/biomejs/biome/pull/12723
* fix(parse/html/vue): parse `v-for` binding default values by @dyc3 in https://github.com/biomejs/biome/pull/12702
* chore: fix advisory by @dyc3 in https://github.com/biomejs/biome/pull/12730
* perf(rowan): iterate SyntaxKindSet by scanning set bits by @dyc3 in https://github.com/biomejs/biome/pull/12719
* perf(rowan): resolve syntax node pointers through the green tree and near a known node by @dyc3 in https://github.com/biomejs/biome/pull/12722
* feat(lint): add noVueUnusedRefs by @dyc3 in https://github.com/biomejs/biome/pull/12603
* feat(lint): add noVueDeprecatedDeleteSet by @dyc3 in https://github.com/biomejs/biome/pull/12586
* ci: release by @github-actions[bot] in https://github.com/biomejs/biome/pull/12647

## New Contributors
* @MindTooth made their first contribution in https://github.com/biomejs/biome/pull/12664
* @xucian made their first contribution in https://github.com/biomejs/biome/pull/12607
* @kurovskyiii made their first contribution in https://github.com/biomejs/biome/pull/12652
* @NikitaCOEUR made their first contribution in https://github.com/biomejs/biome/pull/12692

**Full Changelog**: https://github.com/biomejs/biome/compare/@biomejs/biome@2.6.3...@biomejs/biome@2.6.4

## COMMIT SUBJECTS between the previous tag and the release

feat(lint): add useWhileLoopCondition (#12472)
refactor(analyze): remove the rule-count limit on analyzer groups (#12637)
fix(migrate): carry Prettier's bracketSpacing in overrides (#12649)
fix(format/md): preserve newline between block quote and list (#12662)
feat(lint): add noNull (#12470)
fix(migrate): carry Prettier's bracketSpacing into the top-level (#12670)
fix: mark pnpm-lock.yaml as protected file (#12664)
fix(markdown_parser): attach whitespace before a table pipe to the pipe (#12607)
feat(lint): add noYamlBooleanKeys (#12285)
feat(lint): add noUnreadableIife (#12477)
feat(lint): add useSvelteEventDispatcherTypes (#12338)
feat(lint): add noMagicArrayFlatDepth (#12469)
feat(lint): add noConsoleSpaces (#12261)
perf(languages): resolve editor settings directories once, and check less often (#12656)
feat(lint): add noUselessRecursion (#12447)
fix(css): sync recess property order and preserve cascade when sorting (#12640)
feat(lint): add noReturnArrayPush (#12483)
fix(lsp): warn when the configuration file can't be loaded (#12678)
chore(deps): update rust crate notify to 8.2.1 (#12689)
fix(module_graph): resolve an imported type merged with a value to the type in annotations (#12652)
fix(markdown): keep frontmatter of fenced Markdown blocks when formatting embeds (#12682)
chore(deps): update rust crate serde_json to 1.0.154 (#12690)
chore(deps): update rust crate smallvec to 1.16.4 (#12691)
fix(markdown_parser): continue block quotes inside deep list items (#12575)
chore: update rule metadata (#12699)
perf(lint): make noDuplicateCase, noDuplicateElseIf and noFallthroughSwitchClause linear (#12457)
perf(lint): speed up useHookAtTopLevel, noUnusedImports and noUnusedPrivateClassMembers (#12458)
feat(lint): add useVueTemplateRef (#12559)
feat(lint): add useVueValidVShow (#12569)
feat(lint): add useVueDefinePropsDestructuring (#12514)
feat(lint): add useVueValidVIs (#12570)
feat(noVueVIfWithVFor): report v-else and v-else-if with v-for (#12519)
feat(lint): add noVueSideEffectsInComputed (#12567)
feat(lint): add noVueDeprecatedListeners (#12661)
feat(lint): add useVueValidVModel (#12597)
feat(lint): add useVueValidVSlot (#12525)
fix(markdown_parser): nest list items by enclosing content column (#12576)
chore(deps): update rust:1.98.0-bullseye docker digest to 4730e38 (#11645)
feat(lint): add useVueValidVMemo (#12521)
feat(lint): add useVueValidDefineProps (#12614)
feat(lint): add useVueTypedProps (#12512)
feat(lint): add useVueVModel (#12653)
feat(lint): add useVueValidDefineEmits (#12591)
feat(lint): add noVueDeprecatedRouterLinkTagProp (#12648)
chore: move myself to core (#12713)
feat(lint): add useVueDefineOptions (#12615)
feat(lint): add noVueMutatingProps (#12513)
feat(lint): add noVueDeprecatedScopeAttribute (#12631)
feat(lint): add noVueMultipleSlotArgs (#12562)
fix(cli): use jemalloc on x86_64 musl (#12692)
feat(lint): add noVueComputedPropertiesInData (#12554)
refactor: source text as input (#12501)
refactor(core): scanner epoch and LRU eviction (#12694)
perf(rowan): read node text from the green tree (#12723)
fix(parse/html/vue): parse `v-for` binding default values (#12702)
chore: fix advisory (#12730)
perf(rowan): iterate SyntaxKindSet by scanning set bits (#12719)
perf(rowan): resolve syntax node pointers through the green tree and near a known node (#12722)
feat(lint): add noVueUnusedRefs (#12603)
feat(lint): add noVueDeprecatedDeleteSet (#12586)
ci: release (#12647)

# CANDIDATE A

## @biomejs/biome@2.6.4

### New nursery rules

All rules below are in the `nursery` group and are not enabled by default.

JavaScript and TypeScript:

- Added [`noConsoleSpaces`](https://biomejs.dev/linter/rules/no-console-spaces/), which reports a leading or trailing space in a `console` method argument that sits next to another argument. [#12261](https://github.com/biomejs/biome/pull/12261)
- Added [`noMagicArrayFlatDepth`](https://biomejs.dev/linter/rules/no-magic-array-flat-depth/), which reports a depth other than `1` passed to `Array.prototype.flat()` unless a comment explains it. [#12469](https://github.com/biomejs/biome/pull/12469)
- Added [`noNull`](https://biomejs.dev/linter/rules/no-null/), which reports the `null` literal and suggests `undefined`. Strict comparisons such as `foo === null` are allowed. [#12470](https://github.com/biomejs/biome/pull/12470)
- Added [`noReturnArrayPush`](https://biomejs.dev/linter/rules/no-return-array-push/), which reports code that uses the return value of `push()` or `unshift()`. [#12483](https://github.com/biomejs/biome/pull/12483)
- Added [`noUnreadableIife`](https://biomejs.dev/linter/rules/no-unreadable-iife/), which reports immediately called arrow functions whose body is wrapped in parentheses. [#12477](https://github.com/biomejs/biome/pull/12477)
- Added [`noUselessRecursion`](https://biomejs.dev/linter/rules/no-useless-recursion/), which reports functions that return a call to themselves when a loop could do the same work. [#12447](https://github.com/biomejs/biome/pull/12447)
- Added [`useWhileLoopCondition`](https://biomejs.dev/linter/rules/use-while-loop-condition/). [#12472](https://github.com/biomejs/biome/pull/12472)

Svelte:

- Added [`useSvelteEventDispatcherTypes`](https://biomejs.dev/linter/rules/use-svelte-event-dispatcher-types/). [#12338](https://github.com/biomejs/biome/pull/12338)

YAML:

- Added [`noYamlBooleanKeys`](https://biomejs.dev/linter/rules/no-yaml-boolean-keys/). [#12285](https://github.com/biomejs/biome/pull/12285)

Vue:

- Added [`noVueComputedPropertiesInData`](https://biomejs.dev/linter/rules/no-vue-computed-properties-in-data/), which reports computed properties read inside the `data` function. [#12554](https://github.com/biomejs/biome/pull/12554)
- Added [`noVueDeprecatedDeleteSet`](https://biomejs.dev/linter/rules/no-vue-deprecated-delete-set/), which reports `$set`, `$delete`, `Vue.set` and `Vue.delete`, which Vue 3 removed. [#12586](https://github.com/biomejs/biome/pull/12586)
- Added [`noVueDeprecatedListeners`](https://biomejs.dev/linter/rules/no-vue-deprecated-listeners/), which reports `$listeners`, which Vue 3 removed. [#12661](https://github.com/biomejs/biome/pull/12661)
- Added [`noVueDeprecatedRouterLinkTagProp`](https://biomejs.dev/linter/rules/no-vue-deprecated-router-link-tag-prop/), which reports the `tag` prop on `RouterLink`. [#12648](https://github.com/biomejs/biome/pull/12648)
- Added [`noVueDeprecatedScopeAttribute`](https://biomejs.dev/linter/rules/no-vue-deprecated-scope-attribute/), which reports the `scope` attribute on `<template>` elements. [#12631](https://github.com/biomejs/biome/pull/12631)
- Added [`noVueMultipleSlotArgs`](https://biomejs.dev/linter/rules/no-vue-multiple-slot-args/), which reports more than one argument passed to a slot from a render function. [#12562](https://github.com/biomejs/biome/pull/12562)
- Added [`noVueMutatingProps`](https://biomejs.dev/linter/rules/no-vue-mutating-props/), which reports code that changes a component's props. [#12513](https://github.com/biomejs/biome/pull/12513)
- Added [`noVueSideEffectsInComputed`](https://biomejs.dev/linter/rules/no-vue-side-effects-in-computed/). [#12567](https://github.com/biomejs/biome/pull/12567)
- Added [`noVueUnusedRefs`](https://biomejs.dev/linter/rules/no-vue-unused-refs/). [#12603](https://github.com/biomejs/biome/pull/12603)
- Added [`useVueDefineOptions`](https://biomejs.dev/linter/rules/use-vue-define-options/). [#12615](https://github.com/biomejs/biome/pull/12615)
- Added [`useVueDefinePropsDestructuring`](https://biomejs.dev/linter/rules/use-vue-define-props-destructuring/). [#12514](https://github.com/biomejs/biome/pull/12514)
- Added [`useVueTemplateRef`](https://biomejs.dev/linter/rules/use-vue-template-ref/). [#12559](https://github.com/biomejs/biome/pull/12559)
- Added [`useVueTypedProps`](https://biomejs.dev/linter/rules/use-vue-typed-props/). [#12512](https://github.com/biomejs/biome/pull/12512)
- Added [`useVueVModel`](https://biomejs.dev/linter/rules/use-vue-v-model/). [#12653](https://github.com/biomejs/biome/pull/12653)
- Added [`useVueValidDefineEmits`](https://biomejs.dev/linter/rules/use-vue-valid-define-emits/). [#12591](https://github.com/biomejs/biome/pull/12591)
- Added [`useVueValidDefineProps`](https://biomejs.dev/linter/rules/use-vue-valid-define-props/). [#12614](https://github.com/biomejs/biome/pull/12614)
- Added [`useVueValidVIs`](https://biomejs.dev/linter/rules/use-vue-valid-v-is/). [#12570](https://github.com/biomejs/biome/pull/12570)
- Added [`useVueValidVMemo`](https://biomejs.dev/linter/rules/use-vue-valid-v-memo/). [#12521](https://github.com/biomejs/biome/pull/12521)
- Added [`useVueValidVModel`](https://biomejs.dev/linter/rules/use-vue-valid-v-model/). [#12597](https://github.com/biomejs/biome/pull/12597)
- Added [`useVueValidVShow`](https://biomejs.dev/linter/rules/use-vue-valid-v-show/). [#12569](https://github.com/biomejs/biome/pull/12569)
- Added [`useVueValidVSlot`](https://biomejs.dev/linter/rules/use-vue-valid-v-slot/). [#12525](https://github.com/biomejs/biome/pull/12525)

### Improvements to existing rules and actions

- [`noVueVIfWithVFor`](https://biomejs.dev/linter/rules/no-vue-v-if-with-v-for/) now also reports `v-else-if` and `v-else` on the same element as `v-for`. [#12519](https://github.com/biomejs/biome/pull/12519)
- [`useSortedProperties`](https://biomejs.dev/assist/actions/use-sorted-properties/) now follows `stylelint-config-recess-order` 7.9.0 and supports more properties. [#12640](https://github.com/biomejs/biome/pull/12640)
- [`noShorthandPropertyOverrides`](https://biomejs.dev/linter/rules/no-shorthand-property-overrides/) now recognizes logical border, corner shape, `position-try`, `text-box` and `transition-behavior` overrides. [#12640](https://github.com/biomejs/biome/pull/12640)

### Bug fixes

- Fixed [#12651](https://github.com/biomejs/biome/issues/12651): an imported name exported as both a type and a value now resolves to the type in type annotations, so `noBaseToString` no longer gives false positives. [#12652](https://github.com/biomejs/biome/pull/12652)
- Fixed `useSortedProperties` sorting fixes that changed the effective value of overlapping declarations, physical and logical border or corner properties, or declarations followed by `all`. [#12640](https://github.com/biomejs/biome/pull/12640)
- Fixed parsing of default values in Vue `v-for` bindings, which were reported as parse errors. [#12702](https://github.com/biomejs/biome/pull/12702)
- Fixed the Markdown formatter removing the blank line between a blockquote and the list after it. Fixes [#12645](https://github.com/biomejs/biome/issues/12645). [#12662](https://github.com/biomejs/biome/pull/12662)
- Fixed the Markdown formatter removing the blank line between a table and the list after it. Fixes [#12663](https://github.com/biomejs/biome/issues/12663).
- Fixed Markdown list items with markers indented 4 or more spaces nesting at the wrong level. Fixes [#12541](https://github.com/biomejs/biome/issues/12541). [#12576](https://github.com/biomejs/biome/pull/12576)
- Fixed formatting of Markdown block quotes inside deeply indented list items. [#12575](https://github.com/biomejs/biome/pull/12575)
- Fixed the Markdown formatter not being idempotent on tables. Fixes [#12542](https://github.com/biomejs/biome/issues/12542). [#12607](https://github.com/biomejs/biome/pull/12607)
- Fixed the Markdown formatter changing the frontmatter of fenced Markdown code blocks when `formatEmbeds` is enabled. Fixes [#12679](https://github.com/biomejs/biome/issues/12679). [#12682](https://github.com/biomejs/biome/pull/12682)
- Fixed `biome migrate prettier` ignoring `bracketSpacing`; it now migrates to `formatter.bracketSpacing` at the top level and in `overrides`. Fixes [#12643](https://github.com/biomejs/biome/issues/12643) and [#12669](https://github.com/biomejs/biome/issues/12669). [#12649](https://github.com/biomejs/biome/pull/12649), [#12670](https://github.com/biomejs/biome/pull/12670)
- Fixed the language server replacing the text of an open file with the text on disk when the file changed on disk. Fixes [biomejs/biome-vscode#923](https://github.com/biomejs/biome-vscode/issues/923).
- Fixed the CLI checking the unsaved editor text instead of the files on disk when run with `--use-server` next to an editor on the same daemon.
- Fixed the language server keeping old parser options for open files after a configuration change.
- Fixed the language server not warning when the configuration file can't be loaded. Fixes [biomejs/biome-vscode#1113](https://github.com/biomejs/biome-vscode/issues/1113). [#12678](https://github.com/biomejs/biome/pull/12678)
- Fixed the daemon using more memory with every `biome check --use-server` run. Fixes [#12466](https://github.com/biomejs/biome/issues/12466). [#12694](https://github.com/biomejs/biome/pull/12694)
- Fixed non-JSON files in the global settings directories of Zed, VS Code and Cursor being parsed as JSON. [#12656](https://github.com/biomejs/biome/pull/12656)
- Fixed the `linux-x64-musl` binary not using jemalloc, which made multi-threaded runs very slow, for example on Alpine. [#12692](https://github.com/biomejs/biome/pull/12692)
- Fixed Biome processing `pnpm-lock.yaml` files; they are now protected. [#12664](https://github.com/biomejs/biome/pull/12664)

### Performance

- Faster linting overall, including less time setting up enabled rules per file and faster runs on files with code fixes.
- Faster `useHookAtTopLevel`, `noUnusedImports`, `noUnusedPrivateClassMembers`, `noDuplicateCase`, `noDuplicateElseIf` and `noFallthroughSwitchClause`. [#12458](https://github.com/biomejs/biome/pull/12458), [#12457](https://github.com/biomejs/biome/pull/12457)
- Faster syntax tree operations: node text, syntax node lookups and kind sets. [#12723](https://github.com/biomejs/biome/pull/12723), [#12722](https://github.com/biomejs/biome/pull/12722), [#12719](https://github.com/biomejs/biome/pull/12719)

### Other

- Internal refactors: source text as analyzer input, scanner epochs and LRU eviction, and removal of the rule-count limit on analyzer groups. [#12501](https://github.com/biomejs/biome/pull/12501), [#12694](https://github.com/biomejs/biome/pull/12694), [#12637](https://github.com/biomejs/biome/pull/12637)
- Dependency updates (`smallvec`, `serde_json`, `notify`, Rust Docker image) and an advisory fix. [#12691](https://github.com/biomejs/biome/pull/12691), [#12690](https://github.com/biomejs/biome/pull/12690), [#12689](https://github.com/biomejs/biome/pull/12689), [#12645](https://github.com/biomejs/biome/pull/11645), [#12730](https://github.com/biomejs/biome/pull/12730)
- Updated rule metadata and team membership. [#12699](https://github.com/biomejs/biome/pull/12699), [#12713](https://github.com/biomejs/biome/pull/12713)


# CANDIDATE B

## @biomejs/biome@2.6.4

### New nursery rules

All new rules are in the `nursery` group and are not enabled by default.

JavaScript and general:
- Added [`noConsoleSpaces`](https://biomejs.dev/linter/rules/no-console-spaces/), which reports a leading or trailing space in `console` method arguments. ([#12261](https://github.com/biomejs/biome/pull/12261))
- Added [`noMagicArrayFlatDepth`](https://biomejs.dev/linter/rules/no-magic-array-flat-depth/), which reports `flat()` depths other than `1` unless a comment explains them. ([#12469](https://github.com/biomejs/biome/pull/12469))
- Added [`noNull`](https://biomejs.dev/linter/rules/no-null/), which reports the `null` literal and suggests `undefined`. ([#12470](https://github.com/biomejs/biome/pull/12470))
- Added [`noReturnArrayPush`](https://biomejs.dev/linter/rules/no-return-array-push/), which reports uses of the return value of `push()` or `unshift()`. ([#12483](https://github.com/biomejs/biome/pull/12483))
- Added [`noUnreadableIife`](https://biomejs.dev/linter/rules/no-unreadable-iife/), which reports immediately invoked arrow functions with a parenthesized body. ([#12477](https://github.com/biomejs/biome/pull/12477))
- Added [`noUselessRecursion`](https://biomejs.dev/linter/rules/no-useless-recursion/), which reports functions that return a call to themselves where a loop would do. ([#12447](https://github.com/biomejs/biome/pull/12447))
- Added [`useWhileLoopCondition`](https://biomejs.dev/linter/rules/use-while-loop-condition/), which moves a leading `if (...) break;` in `while (true)` and `for (;;)` loops into the loop condition. ([#12472](https://github.com/biomejs/biome/pull/12472))

YAML and Svelte:
- Added [`noYamlBooleanKeys`](https://biomejs.dev/linter/rules/no-yaml-boolean-keys/), which disallows boolean values as YAML keys. ([#12285](https://github.com/biomejs/biome/pull/12285))
- Added [`useSvelteEventDispatcherTypes`](https://biomejs.dev/linter/rules/use-svelte-event-dispatcher-types/), which reports `createEventDispatcher()` calls without event types in TypeScript Svelte components. ([#12338](https://github.com/biomejs/biome/pull/12338))

Vue:
- Added [`noVueComputedPropertiesInData`](https://biomejs.dev/linter/rules/no-vue-computed-properties-in-data/). ([#12554](https://github.com/biomejs/biome/pull/12554))
- Added [`noVueDeprecatedDeleteSet`](https://biomejs.dev/linter/rules/no-vue-deprecated-delete-set/). ([#12586](https://github.com/biomejs/biome/pull/12586))
- Added [`noVueDeprecatedListeners`](https://biomejs.dev/linter/rules/no-vue-deprecated-listeners/). ([#12661](https://github.com/biomejs/biome/pull/12661))
- Added [`noVueDeprecatedRouterLinkTagProp`](https://biomejs.dev/linter/rules/no-vue-deprecated-router-link-tag-prop/). ([#12648](https://github.com/biomejs/biome/pull/12648))
- Added [`noVueDeprecatedScopeAttribute`](https://biomejs.dev/linter/rules/no-vue-deprecated-scope-attribute/). ([#12631](https://github.com/biomejs/biome/pull/12631))
- Added [`noVueMultipleSlotArgs`](https://biomejs.dev/linter/rules/no-vue-multiple-slot-args/). ([#12562](https://github.com/biomejs/biome/pull/12562))
- Added [`noVueMutatingProps`](https://biomejs.dev/linter/rules/no-vue-mutating-props/). ([#12513](https://github.com/biomejs/biome/pull/12513))
- Added [`noVueSideEffectsInComputed`](https://biomejs.dev/linter/rules/no-vue-side-effects-in-computed/). ([#12567](https://github.com/biomejs/biome/pull/12567))
- Added [`noVueUnusedRefs`](https://biomejs.dev/linter/rules/no-vue-unused-refs/), which needs `html.experimentalFullSupportEnabled`. ([#12603](https://github.com/biomejs/biome/pull/12603))
- Added [`useVueDefineOptions`](https://biomejs.dev/linter/rules/use-vue-define-options/). ([#12615](https://github.com/biomejs/biome/pull/12615))
- Added [`useVueDefinePropsDestructuring`](https://biomejs.dev/linter/rules/use-vue-define-props-destructuring/). ([#12514](https://github.com/biomejs/biome/pull/12514))
- Added [`useVueTemplateRef`](https://biomejs.dev/linter/rules/use-vue-template-ref/). ([#12559](https://github.com/biomejs/biome/pull/12559))
- Added [`useVueTypedProps`](https://biomejs.dev/linter/rules/use-vue-typed-props/). ([#12512](https://github.com/biomejs/biome/pull/12512))
- Added [`useVueVModel`](https://biomejs.dev/linter/rules/use-vue-v-model/). ([#12653](https://github.com/biomejs/biome/pull/12653))
- Added [`useVueValidDefineEmits`](https://biomejs.dev/linter/rules/use-vue-valid-define-emits/). ([#12591](https://github.com/biomejs/biome/pull/12591))
- Added [`useVueValidDefineProps`](https://biomejs.dev/linter/rules/use-vue-valid-define-props/). ([#12614](https://github.com/biomejs/biome/pull/12614))
- Added [`useVueValidVIs`](https://biomejs.dev/linter/rules/use-vue-valid-v-is/). ([#12570](https://github.com/biomejs/biome/pull/12570))
- Added [`useVueValidVMemo`](https://biomejs.dev/linter/rules/use-vue-valid-v-memo/). ([#12521](https://github.com/biomejs/biome/pull/12521))
- Added [`useVueValidVModel`](https://biomejs.dev/linter/rules/use-vue-valid-v-model/). ([#12597](https://github.com/biomejs/biome/pull/12597))
- Added [`useVueValidVShow`](https://biomejs.dev/linter/rules/use-vue-valid-v-show/). ([#12569](https://github.com/biomejs/biome/pull/12569))
- Added [`useVueValidVSlot`](https://biomejs.dev/linter/rules/use-vue-valid-v-slot/). ([#12525](https://github.com/biomejs/biome/pull/12525))

### Improvements

- [`noVueVIfWithVFor`](https://biomejs.dev/linter/rules/no-vue-v-if-with-v-for/) now also reports `v-else-if` and `v-else` on the same element as `v-for`. ([#12519](https://github.com/biomejs/biome/pull/12519))
- [`useSortedProperties`](https://biomejs.dev/assist/actions/use-sorted-properties/) now follows `stylelint-config-recess-order` 7.9.0, adding `scroll-behavior`, anchor positioning, multi-column layout and other properties. ([#12640](https://github.com/biomejs/biome/pull/12640))
- [`noShorthandPropertyOverrides`](https://biomejs.dev/linter/rules/no-shorthand-property-overrides/) now recognizes logical border, corner shape, `position-try`, `text-box` and `transition-behavior` overrides. ([#12640](https://github.com/biomejs/biome/pull/12640))
- Linting is faster: less time is spent setting up rules per file, and `useHookAtTopLevel`, `noUnusedImports`, `noUnusedPrivateClassMembers`, `noDuplicateCase`, `noDuplicateElseIf` and `noFallthroughSwitchClause` run faster. ([#12458](https://github.com/biomejs/biome/pull/12458), [#12457](https://github.com/biomejs/biome/pull/12457), [#12637](https://github.com/biomejs/biome/pull/12637))
- `biome lint` is about 1% to 3% faster on large projects, and up to 12% faster with the default rules on files that have diagnostics with fixes. ([#12722](https://github.com/biomejs/biome/pull/12722), [#12719](https://github.com/biomejs/biome/pull/12719), [#12723](https://github.com/biomejs/biome/pull/12723))
- Processing many files is up to 7% faster. ([#12656](https://github.com/biomejs/biome/pull/12656))

### Bug fixes

Linter and analysis:
- Fixed [#12651](https://github.com/biomejs/biome/issues/12651): an imported name exported as both a type and a value now resolves to the type in annotations, so `noBaseToString` no longer reports it. ([#12652](https://github.com/biomejs/biome/pull/12652))
- Fixed `useSortedProperties` to withhold fixes that would change the effective values of overlapping declarations, physical/logical border or corner properties, or declarations followed by `all`. ([#12640](https://github.com/biomejs/biome/pull/12640))

Vue:
- Fixed parsing of default values in Vue `v-for` bindings, so they are formatted and linted instead of reported as parse errors. ([#12702](https://github.com/biomejs/biome/pull/12702))

Markdown:
- Fixed [#12645](https://github.com/biomejs/biome/issues/12645): the formatter no longer removes the blank line between a block quote and the following list. ([#12662](https://github.com/biomejs/biome/pull/12662))
- Fixed [#12663](https://github.com/biomejs/biome/issues/12663): the formatter no longer removes the blank line between a table and the following list.
- Fixed [#12541](https://github.com/biomejs/biome/issues/12541): list items indented 4 or more spaces now nest at the correct level. ([#12576](https://github.com/biomejs/biome/pull/12576))
- Fixed formatting of block quotes inside deeply indented list items. ([#12575](https://github.com/biomejs/biome/pull/12575))
- Fixed [#12542](https://github.com/biomejs/biome/issues/12542): table formatting is now idempotent. ([#12607](https://github.com/biomejs/biome/pull/12607))
- Fixed [#12679](https://github.com/biomejs/biome/issues/12679): the frontmatter of fenced Markdown code blocks is kept as written when formatting embeds. ([#12682](https://github.com/biomejs/biome/pull/12682))

CLI, migration and language server:
- Fixed [#12643](https://github.com/biomejs/biome/issues/12643) and [#12669](https://github.com/biomejs/biome/issues/12669): `biome migrate prettier` now migrates `bracketSpacing` at the top level and in `overrides`. ([#12649](https://github.com/biomejs/biome/pull/12649), [#12670](https://github.com/biomejs/biome/pull/12670))
- Fixed the `linux-x64-musl` binary not using jemalloc, which made multi-threaded runs very slow on Alpine-based images. ([#12692](https://github.com/biomejs/biome/pull/12692))
- Fixed Biome processing `pnpm-lock.yaml`; it is now a protected file. ([#12664](https://github.com/biomejs/biome/pull/12664))
- Fixed non-JSON files in the global settings directories of Zed, VS Code and Cursor being parsed as JSON.
- Fixed [#12466](https://github.com/biomejs/biome/issues/12466): the daemon used more memory with every `biome check --use-server` run. ([#12694](https://github.com/biomejs/biome/pull/12694))
- Fixed [biomejs/biome-vscode#923](https://github.com/biomejs/biome-vscode/issues/923): the language server no longer replaces an open editor's text with the text on disk. ([#12501](https://github.com/biomejs/biome/pull/12501))
- Fixed the CLI with `--use-server` checking an editor's unsaved text instead of the files on disk. ([#12501](https://github.com/biomejs/biome/pull/12501))
- Fixed the language server keeping old parser options for open files after a configuration change.
- Fixed [biomejs/biome-vscode#1113](https://github.com/biomejs/biome-vscode/issues/1113): the language server now warns when the configuration file can't be loaded. ([#12678](https://github.com/biomejs/biome/pull/12678))

### Other

- Internal refactors of the analyzer, scanner and source text handling. ([#12501](https://github.com/biomejs/biome/pull/12501), [#12637](https://github.com/biomejs/biome/pull/12637), [#12694](https://github.com/biomejs/biome/pull/12694))
- Dependency updates (`smallvec`, `serde_json`, `notify`, Rust Docker image) and an advisory fix. ([#12691](https://github.com/biomejs/biome/pull/12691), [#12690](https://github.com/biomejs/biome/pull/12690), [#12689](https://github.com/biomejs/biome/pull/12689), [#11645](https://github.com/biomejs/biome/pull/11645), [#12730](https://github.com/biomejs/biome/pull/12730))
- Updated rule metadata and contributor team listings. ([#12699](https://github.com/biomejs/biome/pull/12699), [#12713](https://github.com/biomejs/biome/pull/12713))

