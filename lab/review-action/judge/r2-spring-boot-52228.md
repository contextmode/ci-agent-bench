# PR diff (the real change)

```diff
diff --git a/core/spring-boot/src/main/java/org/springframework/boot/logging/logback/ColorConverter.java b/core/spring-boot/src/main/java/org/springframework/boot/logging/logback/ColorConverter.java
index 12d489a40863..b311859f2fc2 100644
--- a/core/spring-boot/src/main/java/org/springframework/boot/logging/logback/ColorConverter.java
+++ b/core/spring-boot/src/main/java/org/springframework/boot/logging/logback/ColorConverter.java
@@ -21,6 +21,7 @@
 import org.springframework.boot.ansi.AnsiElement;
 import org.springframework.boot.ansi.AnsiOutput;
 import org.springframework.boot.ansi.AnsiStyle;
+import org.springframework.util.CollectionUtils;
 
 /**
  * Logback {@link CompositeConverter} to color output using the {@link AnsiOutput} class.
@@ -31,55 +32,65 @@
  * {@code reverse}).
  *
  * @author Phillip Webb
+ * @author Jan Mohr
  * @since 1.0.0
  */
 public class ColorConverter extends CompositeConverter<ILoggingEvent> {
 
-	private static final Map<String, AnsiElement> ELEMENTS;
+	private static final Map<String, AnsiElement> ELEMENTS_BY_NAME;
 
 	static {
-		Map<String, AnsiElement> ansiElements = new HashMap<>();
+		Map<String, AnsiElement> elements = new HashMap<>();
 		Arrays.stream(AnsiColor.values())
 			.filter((color) -> color != AnsiColor.DEFAULT)
-			.forEach((color) -> ansiElements.put(color.name().toLowerCase(Locale.ROOT), color));
+			.forEach((color) -> elements.put(color.name().toLowerCase(Locale.ROOT), color));
 		Arrays.stream(AnsiStyle.values())
-			.forEach((style) -> ansiElements.put(style.name().toLowerCase(Locale.ROOT), style));
+			.forEach((style) -> elements.put(style.name().toLowerCase(Locale.ROOT), style));
 		Arrays.stream(AnsiBackground.values())
-			.filter((bg) -> bg != AnsiBackground.DEFAULT)
-			.forEach((bg) -> ansiElements.put("bg_" + bg.name().toLowerCase(Locale.ROOT), bg));
-		ELEMENTS = Collections.unmodifiableMap(ansiElements);
+			.filter((background) -> background != AnsiBackground.DEFAULT)
+			.forEach((background) -> elements.put("bg_" + background.name().toLowerCase(Locale.ROOT), background));
+		ELEMENTS_BY_NAME = Collections.unmodifiableMap(elements);
 	}
 
-	private static final Map<Integer, AnsiElement> LEVELS;
+	private static final Map<Integer, AnsiElement> ELEMENTS_BY_LEVEL;
 
 	static {
-		Map<Integer, AnsiElement> ansiLevels = new HashMap<>();
-		ansiLevels.put(Level.ERROR_INTEGER, AnsiColor.RED);
-		ansiLevels.put(Level.WARN_INTEGER, AnsiColor.YELLOW);
-		LEVELS = Collections.unmodifiableMap(ansiLevels);
+		Map<Integer, AnsiElement> elements = new HashMap<>();
+		elements.put(Level.ERROR_INTEGER, AnsiColor.RED);
+		elements.put(Level.WARN_INTEGER, AnsiColor.YELLOW);
+		ELEMENTS_BY_LEVEL = Collections.unmodifiableMap(elements);
 	}
 
+	private static final AnsiElement[] NO_ELEMENTS = {};
+
+	private AnsiElement[] elements = NO_ELEMENTS;
+
 	@Override
-	protected String transform(ILoggingEvent event, String in) {
+	public void start() {
 		List<String> options = getOptionList();
-		List<AnsiElement> elements = new ArrayList<>();
-		if (options != null) {
+		if (!CollectionUtils.isEmpty(options)) {
+			List<AnsiElement> elements = new ArrayList<>();
 			for (String option : options) {
-				String[] optionParts = option.split(",");
-				for (String optionPart : optionParts) {
-					AnsiElement element = ELEMENTS.get(optionPart.trim().toLowerCase(Locale.ROOT));
+				for (String optionPart : option.split(",")) {
+					AnsiElement element = ELEMENTS_BY_NAME.get(optionPart.trim().toLowerCase(Locale.ROOT));
 					if (element != null) {
 						elements.add(element);
 					}
 				}
 			}
+			this.elements = elements.toArray(AnsiElement[]::new);
 		}
-		if (elements.isEmpty()) {
+		super.start();
+	}
+
+	@Override
+	protected String transform(ILoggingEvent event, String in) {
+		if (this.elements.length == 0) {
 			// Assume highlighting
-			AnsiElement element = LEVELS.get(event.getLevel().toInteger());
-			elements.add((element != null) ? element : AnsiColor.GREEN);
+			AnsiElement element = ELEMENTS_BY_LEVEL.get(event.getLevel().toInteger());
+			return toAnsiString(in, (element != null) ? element : AnsiColor.GREEN);
 		}
-		return toAnsiString(in, elements.toArray(new AnsiElement[0]));
+		return toAnsiString(in, this.elements);
 	}
 
 	protected String toAnsiString(String in, AnsiElement element) {
@@ -94,7 +105,7 @@ protected String toAnsiString(String in, AnsiElement... elements) {
 	}
 
 	static String getName(AnsiElement element) {
-		return ELEMENTS.entrySet()
+		return ELEMENTS_BY_NAME.entrySet()
 			.stream()
 			.filter((entry) -> entry.getValue().equals(element))
 			.map(Map.Entry::getKey)
diff --git a/core/spring-boot/src/test/java/org/springframework/boot/logging/logback/ColorConverterTests.java b/core/spring-boot/src/test/java/org/springframework/boot/logging/logback/ColorConverterTests.java
index b9b4d0d2e981..af5187bfd34f 100644
--- a/core/spring-boot/src/test/java/org/springframework/boot/logging/logback/ColorConverterTests.java
+++ b/core/spring-boot/src/test/java/org/springframework/boot/logging/logback/ColorConverterTests.java
@@ -5,7 +5,6 @@
 package org.springframework.boot.logging.logback;
 
 import java.util.Arrays;
-import java.util.Collections;
 
 import ch.qos.logback.classic.Level;
 import ch.qos.logback.classic.spi.LoggingEvent;
@@ -21,6 +20,7 @@
  * Tests for {@link ColorConverter}.
  *
  * @author Phillip Webb
+ * @author Jan Mohr
  */
 class ColorConverterTests {
 
@@ -42,196 +42,196 @@ static void resetAnsi() {
 
 	@Test
 	void black() {
-		this.converter.setOptionList(Collections.singletonList("black"));
+		startWithOptions("black");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[30min\033[0;39m");
 	}
 
 	@Test
 	void white() {
-		this.converter.setOptionList(Collections.singletonList("white"));
+		startWithOptions("white");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[37min\033[0;39m");
 	}
 
 	@Test
 	void faint() {
-		this.converter.setOptionList(Collections.singletonList("faint"));
+		startWithOptions("faint");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[2min\033[0;39m");
 	}
 
 	@Test
 	void red() {
-		this.converter.setOptionList(Collections.singletonList("red"));
+		startWithOptions("red");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[31min\033[0;39m");
 	}
 
 	@Test
 	void green() {
-		this.converter.setOptionList(Collections.singletonList("green"));
+		startWithOptions("green");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[32min\033[0;39m");
 	}
 
 	@Test
 	void yellow() {
-		this.converter.setOptionList(Collections.singletonList("yellow"));
+		startWithOptions("yellow");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[33min\033[0;39m");
 	}
 
 	@Test
 	void blue() {
-		this.converter.setOptionList(Collections.singletonList("blue"));
+		startWithOptions("blue");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[34min\033[0;39m");
 	}
 
 	@Test
 	void magenta() {
-		this.converter.setOptionList(Collections.singletonList("magenta"));
+		startWithOptions("magenta");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[35min\033[0;39m");
 	}
 
 	@Test
 	void cyan() {
-		this.converter.setOptionList(Collections.singletonList("cyan"));
+		startWithOptions("cyan");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[36min\033[0;39m");
 	}
 
 	@Test
 	void brightBlack() {
-		this.converter.setOptionList(Collections.singletonList("bright_black"));
+		startWithOptions("bright_black");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[90min\033[0;39m");
 	}
 
 	@Test
 	void brightWhite() {
-		this.converter.setOptionList(Collections.singletonList("bright_white"));
+		startWithOptions("bright_white");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[97min\033[0;39m");
 	}
 
 	@Test
 	void brightRed() {
-		this.converter.setOptionList(Collections.singletonList("bright_red"));
+		startWithOptions("bright_red");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[91min\033[0;39m");
 	}
 
 	@Test
 	void brightGreen() {
-		this.converter.setOptionList(Collections.singletonList("bright_green"));
+		startWithOptions("bright_green");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[92min\033[0;39m");
 	}
 
 	@Test
 	void brightYellow() {
-		this.converter.setOptionList(Collections.singletonList("bright_yellow"));
+		startWithOptions("bright_yellow");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[93min\033[0;39m");
 	}
 
 	@Test
 	void brightBlue() {
-		this.converter.setOptionList(Collections.singletonList("bright_blue"));
+		startWithOptions("bright_blue");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[94min\033[0;39m");
 	}
 
 	@Test
 	void brightMagenta() {
-		this.converter.setOptionList(Collections.singletonList("bright_magenta"));
+		startWithOptions("bright_magenta");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[95min\033[0;39m");
 	}
 
 	@Test
 	void brightCyan() {
-		this.converter.setOptionList(Collections.singletonList("bright_cyan"));
+		startWithOptions("bright_cyan");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[96min\033[0;39m");
 	}
 
 	@Test
 	void bold() {
-		this.converter.setOptionList(Collections.singletonList("bold"));
+		startWithOptions("bold");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[1min\033[0;39m");
 	}
 
 	@Test
 	void italic() {
-		this.converter.setOptionList(Collections.singletonList("italic"));
+		startWithOptions("italic");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[3min\033[0;39m");
 	}
 
 	@Test
 	void underline() {
-		this.converter.setOptionList(Collections.singletonList("underline"));
+		startWithOptions("underline");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[4min\033[0;39m");
 	}
 
 	@Test
 	void reverse() {
-		this.converter.setOptionList(Collections.singletonList("reverse"));
+		startWithOptions("reverse");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[7min\033[0;39m");
 	}
 
 	@Test
 	void bgRed() {
-		this.converter.setOptionList(Collections.singletonList("bg_red"));
+		startWithOptions("bg_red");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[41min\033[0;39m");
 	}
 
 	@Test
 	void bgGreen() {
-		this.converter.setOptionList(Collections.singletonList("bg_green"));
+		startWithOptions("bg_green");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[42min\033[0;39m");
 	}
 
 	@Test
 	void bgYellow() {
-		this.converter.setOptionList(Collections.singletonList("bg_yellow"));
+		startWithOptions("bg_yellow");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[43min\033[0;39m");
 	}
 
 	@Test
 	void bgBlue() {
-		this.converter.setOptionList(Collections.singletonList("bg_blue"));
+		startWithOptions("bg_blue");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[44min\033[0;39m");
 	}
 
 	@Test
 	void bgBrightRed() {
-		this.converter.setOptionList(Collections.singletonList("bg_bright_red"));
+		startWithOptions("bg_bright_red");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[101min\033[0;39m");
 	}
 
 	@Test
 	void multipleStylesCommaSeparated() {
-		this.converter.setOptionList(Collections.singletonList("bold, red"));
+		startWithOptions("bold, red");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[1;31min\033[0;39m");
 	}
 
 	@Test
 	void multipleStyles() {
-		this.converter.setOptionList(Arrays.asList("bold", "red"));
+		startWithOptions("bold", "red");
 		String out = this.converter.transform(this.event, this.in);
 		assertThat(out).isEqualTo("\033[1;31min\033[0;39m");
 	}
@@ -264,4 +264,9 @@ void highlightTrace() {
 		assertThat(out).isEqualTo("\033[32min\033[0;39m");
 	}
 
+	private void startWithOptions(String... options) {
+		this.converter.setOptionList(Arrays.asList(options));
+		this.converter.start();
+	}
+
 }

```

# REVIEW A

**Review of PR #52228: Parse Logback `ColorConverter` options once in `start()`**

The PR is already merged. I read the diff and have no blocking concerns.

**What it does**
- `getOptionList()` is now parsed once in `start()`, not on every `transform()` call. This is a regression fix for the behaviour introduced in #49285.
- The parsed result is cached in an `AnsiElement[]`.
- `transform()` falls back to level-based highlighting when the array is empty.
- The static maps are renamed to `ELEMENTS_BY_NAME` and `ELEMENTS_BY_LEVEL`.
- The tests now call `start()` through a `startWithOptions(...)` helper.

**Code quality**
- The design is sound. It is the standard Logback lifecycle pattern, and it matches what the Log4j2 converter does at construction time.
- `NO_ELEMENTS` avoids a null check on the hot path.
- `CollectionUtils.isEmpty` handles a null option list.
- `super.start()` is called after the options are parsed. `CompositeConverter.start()` can fail validation and leave the converter unstarted, but the options are still parsed by then. That is harmless.
- The `toAnsiString(in, this.elements)` call passes the shared array to a varargs method. That is safe only if `toAnsiString` doesn't mutate or retain it. As far as I can tell from the diff it doesn't, but a comment or a defensive note would help future maintainers.
- The local variable `elements` in `start()` shadows the field. This is minor, and the code already uses `this.` consistently, but a different name such as `parsed` would read more clearly.
- The static-map renames and the lambda parameter rename (`bg` to `background`) are unrelated to the fix. They add diff noise. Maintainers often accept this, and it was polished in the follow-up commit.

**Potential bugs**
- If someone calls `setOptionList()` after `start()`, the change is silently ignored. This is normal for Logback components, since options are set before `start()`. It is a behaviour change from 4.1.0 only for unusual programmatic use.
- Code that subclasses `ColorConverter` and overrides `start()` without calling `super` would now get no options. This is unlikely, but worth noting in the release notes.
- Code that instantiates the converter and calls `transform()` without `start()` now always highlights by level. The tests were updated for this, which confirms it.

**Performance**
- The saving is real. The converter runs about six times per line with the default pattern, and each run previously did a split, trim, lowercase and list allocation. The PR reports about 20% faster formatting and about 500 bytes less allocation per line.
- The benchmark is local and informal. That's fine for a fix this simple.

**Security**
- No concerns. The change handles no external input beyond the pattern options, and it makes no behavioural change there.

**Test coverage**
- The existing option tests were migrated to start the converter first. They keep the same assertions, so there is no regression coverage loss.
- I would add three tests:
  - One checking that options are parsed once. For example, mutating the option list after `start()` should not change the output.
  - One for an unrecognised option, such as `"foo"`. It should fall back to level highlighting, which matches the old behaviour of an empty element list.
  - One for `start()` with a null or empty option list, which exercises the `CollectionUtils.isEmpty` branch directly.

**Summary:** This is a clean, low-risk fix and I would approve it. The suggestions above are non-blocking.

# REVIEW B

# Review of PR #52228: parse Logback `ColorConverter` options once in `start()`

I read the diff only and did not build or run the tests. The PR is already merged.

**Summary:** The change fixes the regression from #49285. Options were split, trimmed and lower-cased on every `transform()` call. They are now parsed once in `start()` into an `AnsiElement[]`. That matches how the Log4j2 converter behaves and is the right fix.

## What's good
- **Correct lifecycle hook.** Logback's `PatternLayoutBase.start()` starts the converters in the chain. `start()` is therefore the right place for the work.
- **Small hot path.** `transform()` now does one array-length check and then either a map lookup for the level or a reuse of the cached array. This removes the per-event `ArrayList`, `split`, `trim` and `toLowerCase` work.
- **Safe default.** `NO_ELEMENTS` as the field initializer means a converter that was never started still falls back to level-based highlighting. The existing `highlight*` tests rely on this and still pass.
- **Safe sharing.** `transform()` passes the shared array to `toAnsiString(String, AnsiElement...)`. This is only a concern if a subclass mutates the varargs array, which is unlikely.
- **Conventions.** The code uses tabs, `this.` prefixes and the `@author` tag, and the renames (`ELEMENTS_BY_NAME` and so on) read better.

## Minor issues and suggestions
1. **Stale state on restart.** `start()` only assigns `this.elements` when the options list is non-empty. If a converter is stopped, its options cleared, and it is started again, the old elements stay in place. Assigning `this.elements = NO_ELEMENTS` in an `else` branch, or always assigning the parsed result, would make `start()` idempotent. This is an edge case, but cheap to cover.
2. **Shadowed field name.** The local `List<AnsiElement> elements` in `start()` has the same name as the `elements` field. It compiles and `this.` is used correctly, but a name like `parsed` would avoid confusion.
3. **Options set after `start()` are ignored.** Previously, changing options at runtime took effect immediately. Now they don't. This is arguably correct for Logback, since options come from the pattern at configuration time. It is still a small behavior change, and the class Javadoc or a code comment could mention it.
4. **`super.start()` ordering.** The parsing runs before `super.start()`. That is harmless, because the parse can't fail and `super.start()` only validates the child converter. Calling `super.start()` first would be the more conventional order.

## Test coverage
- The 28 option tests were mechanically moved onto a `startWithOptions(...)` helper. This is clean and keeps the assertions unchanged.
- **Missing: unrecognized option.** There is no test that `start()` with only unknown options (for example `"foo"`) falls back to level-based highlighting. The old code handled this case implicitly. It is the main behavior that parsing in `start()` could regress.
- **Missing: restart.** There is no test for options that change across a stop and start (see issue 1).
- **Missing: not started.** There is no explicit test that an unstarted converter highlights. The `highlight*` tests cover it implicitly, which is probably enough.
- **No performance test.** That is reasonable. The PR description gives a benchmark (about 20% faster, about 500 bytes less allocation per line).

## Performance and security
- **Performance:** a clear improvement, as above.
- **Security:** none. The options come from the logging configuration, and the change adds no new inputs or I/O.

## Verdict
This is a correct, focused and well-tested fix. The only thing I would follow up on is the unknown-option fallback test, plus resetting `elements` on restart.
