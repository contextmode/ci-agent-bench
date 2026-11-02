# PR diff (the real change)

```diff
diff --git a/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/JarUrlClassLoader.java b/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/JarUrlClassLoader.java
index 0aad597470b6..a58d38b90624 100644
--- a/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/JarUrlClassLoader.java
+++ b/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/JarUrlClassLoader.java
@@ -68,9 +68,6 @@ public JarUrlClassLoader(URL[] urls, ClassLoader parent) {
 
 	@Override
 	public URL findResource(String name) {
-		if (!LoadableNames.isValidResourceName(name)) {
-			return null;
-		}
 		if (this.nestedOnlyOptimizedLoader != null) {
 			return this.nestedOnlyOptimizedLoader.findResource(name);
 		}
@@ -88,9 +85,6 @@ public URL findResource(String name) {
 
 	@Override
 	public Enumeration<URL> findResources(String name) throws IOException {
-		if (!LoadableNames.isValidResourceName(name)) {
-			return Collections.emptyEnumeration();
-		}
 		if (this.nestedOnlyOptimizedLoader != null) {
 			return this.nestedOnlyOptimizedLoader.findResources(name);
 		}
diff --git a/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/LoadableNames.java b/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/LoadableNames.java
index e529ce801241..854a2f8f5332 100644
--- a/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/LoadableNames.java
+++ b/loader/spring-boot-loader/src/main/java/org/springframework/boot/loader/net/protocol/jar/LoadableNames.java
@@ -8,31 +8,73 @@
  * Utility used to check names are valid before performing expensive loading operations.
  *
  * @author Phillip Webb
+ * @author Jan Mohr
  */
 final class LoadableNames {
 
+	private static final char ESCAPE = '\\';
+
 	private LoadableNames() {
 	}
 
+	/**
+	 * Return true of the class name is valid according to <a href=
+	 * "https://docs.oracle.com/javase/specs/jvms/se14/html/jvms-4.html#jvms-4.2">Section
+	 * 4.2 of the Java Virtual Machine Specification</a>.
+	 * @param name the name to test
+	 * @return if the name is valid
+	 */
 	static boolean isValidClassName(String name) {
 		if (name == null || name.isEmpty()) {
 			return false;
 		}
-		boolean identifierStart = true;
+		boolean escape = false;
+		boolean validPackagePart = true;
 		for (int i = 0; i < name.length(); i++) {
 			char ch = name.charAt(i);
-			boolean dotOrSlash = (ch == '.' || ch == '/');
-			if ((identifierStart && !Character.isJavaIdentifierStart(ch))
-					|| !identifierStart && !Character.isJavaIdentifierPart(ch) && !dotOrSlash) {
+			if (isRestrictedNameCharacter(ch)) {
 				return false;
 			}
-			identifierStart = dotOrSlash;
+			if (isPartSeparator(ch)) {
+				if (!validPackagePart || escape || i == 0 || i == name.length() - 1
+						|| isPartSeparator(name.charAt(i + 1))) {
+					return false;
+				}
+				validPackagePart = true;
+				continue;
+			}
+			validPackagePart = validPackagePart && !isInRestrictedPackageCharacterRange(ch);
+			if (escape) {
+				validPackagePart = validPackagePart && (ch == ESCAPE || isPackageCharacterThatShouldBeEscaped(ch));
+				escape = false;
+				continue;
+			}
+			if (ch == ESCAPE) {
+				escape = true;
+				continue;
+			}
+			validPackagePart = validPackagePart && !isPackageCharacterThatShouldBeEscaped(ch);
 		}
 		return true;
 	}
 
-	static boolean isValidResourceName(String name) {
-		return (name != null && !name.isEmpty() && name.indexOf(':') == -1);
+	private static boolean isRestrictedNameCharacter(char ch) {
+		// JVMS 4.2.1. Binary Class and Interface Names
+		return ch == ';' || ch == '[' || ch == '<' || ch == '>';
+	}
+
+	private static boolean isInRestrictedPackageCharacterRange(char ch) {
+		// JVMS 4.2.3. Module and Package Names
+		return ch >= 0 && ch <= 0x1F;
+	}
+
+	private static boolean isPackageCharacterThatShouldBeEscaped(char ch) {
+		// JVMS 4.2.3. Module and Package Names
+		return ch == ':' || ch == '@';
+	}
+
+	private static boolean isPartSeparator(char ch) {
+		return ch == '.' || ch == '/';
 	}
 
 }
diff --git a/loader/spring-boot-loader/src/test/java/org/springframework/boot/loader/net/protocol/jar/LoadableNamesTests.java b/loader/spring-boot-loader/src/test/java/org/springframework/boot/loader/net/protocol/jar/LoadableNamesTests.java
index a19eb34a209d..4b93bae897d3 100644
--- a/loader/spring-boot-loader/src/test/java/org/springframework/boot/loader/net/protocol/jar/LoadableNamesTests.java
+++ b/loader/spring-boot-loader/src/test/java/org/springframework/boot/loader/net/protocol/jar/LoadableNamesTests.java
@@ -17,7 +17,7 @@
 class LoadableNamesTests {
 
 	@Test
-	void isValidClassNameWhenValid() {
+	void isValidClassNameWhenValidReturnsTrue() {
 		assertThatIsValidClassName("$").isTrue();
 		assertThatIsValidClassName("MyClass").isTrue();
 		assertThatIsValidClassName("com.example.MyClass").isTrue();
@@ -29,36 +29,73 @@ void isValidClassNameWhenValid() {
 	}
 
 	@Test
-	void isValidClassNameWhenInvalid() {
+	void isValidClassNameWhenNotJavaIdentifierReturnsTrue() {
+		assertThatIsValidClassName("com.example.package-info").isTrue();
+		assertThatIsValidClassName("com.example.-MyClass").isTrue();
+		assertThatIsValidClassName("com.example.MyClass$my-function$1").isTrue();
+		assertThatIsValidClassName("com.example.my-package.MyClass").isTrue();
+		assertThatIsValidClassName("1Bad").isTrue();
+		assertThatIsValidClassName("com.1Bad").isTrue();
+		assertThatIsValidClassName("My Class").isTrue();
+		assertThatIsValidClassName("my!class").isTrue();
+		assertThatIsValidClassName("my:class").isTrue();
+	}
+
+	@Test
+	void isValidClassNameWhenInvalidReturnsFalse() {
 		assertThatIsValidClassName("").isFalse();
 		assertThatIsValidClassName(".").isFalse();
-		assertThatIsValidClassName("1Bad").isFalse();
-		assertThatIsValidClassName("com.1Bad").isFalse();
+		assertThatIsValidClassName("..").isFalse();
+		assertThatIsValidClassName("./").isFalse();
+		assertThatIsValidClassName("//").isFalse();
+		assertThatIsValidClassName("/.").isFalse();
+		assertThatIsValidClassName("com.").isFalse();
+		assertThatIsValidClassName(".com").isFalse();
+		assertThatIsValidClassName("com.").isFalse();
 		assertThatIsValidClassName("com..MyClass").isFalse();
-		assertThatIsValidClassName("My Class").isFalse();
-		assertThatIsValidClassName("my!class").isFalse();
-		assertThatIsValidClassName("my:class").isFalse();
+		assertThatIsValidClassName("com//MyClass").isFalse();
+		assertThatIsValidClassName("com./MyClass").isFalse();
+		assertThatIsValidClassName("com/.MyClass").isFalse();
+		assertThatIsValidClassName("com.example.My;Class").isFalse();
+		assertThatIsValidClassName("[Lcom.example.MyClass;").isFalse();
+		assertThatIsValidClassName("com.example.MyClass[]").isFalse();
+		assertThatIsValidClassName("com.example.MyClass<").isFalse();
+		assertThatIsValidClassName("com.example.MyClass>").isFalse();
 	}
 
 	@Test
-	void isValidResourceNameWhenValid() {
-		assertThatIsValidResourceName("resource.txt").isTrue();
-		assertThatIsValidResourceName("/some/resource.txt").isTrue();
-		assertThatIsValidResourceName("some/resource.txt").isTrue();
+	void isValidWhenPackageNameWithEscapesReturnsTrue() {
+		assertThatIsValidClassName("com.example\\\\.MyClass").isTrue();
+		assertThatIsValidClassName("com.example\\@.MyClass").isTrue();
+		assertThatIsValidClassName("com.example\\:.MyClass").isTrue();
+		assertThatIsValidClassName("com/example\\:/MyClass").isTrue();
+		assertThatIsValidClassName("com.example\u0020.MyClass").isTrue();
 	}
 
 	@Test
-	void isValidResourceNameWhenInvalid() {
-		assertThatIsValidResourceName("").isFalse();
-		assertThatIsValidResourceName("test:test").isFalse();
+	void isValidWhenPackageNameInBadCharRangeReturnsFalse() {
+		assertThatIsValidClassName("com.example\u0000.MyClass").isFalse();
+		assertThatIsValidClassName("com.example\u001F.MyClass").isFalse();
 	}
 
-	private AbstractBooleanAssert<?> assertThatIsValidClassName(String n) {
-		return assertThat(LoadableNames.isValidClassName(n));
+	@Test
+	void isValidWhenPackageNameWithoutEscapesReturnsFalse() {
+		assertThatIsValidClassName("com.example\\.MyClass").isFalse();
+		assertThatIsValidClassName("com.example@.MyClass").isFalse();
+		assertThatIsValidClassName("com.example:.MyClass").isFalse();
+		assertThatIsValidClassName("com/example:/MyClass").isFalse();
+		assertThatIsValidClassName("com.ex@mple.another.MyClass").isFalse();
 	}
 
-	private AbstractBooleanAssert<?> assertThatIsValidResourceName(String n) {
-		return assertThat(LoadableNames.isValidResourceName(n));
+	@Test
+	void isValidWhenSimpleClassNameDoesNotEnforcePackageRules() {
+		assertThatIsValidClassName("My@Class").isTrue();
+		assertThatIsValidClassName("My:Class").isTrue();
+		assertThatIsValidClassName("com.ex@mple").isTrue();
+	}
+
+	private AbstractBooleanAssert<?> assertThatIsValidClassName(String n) {
+		return assertThat(LoadableNames.isValidClassName(n));
 	}
 
 }

```

# REVIEW A

## Review of PR #52284: accept all valid JVM class names in `LoadableNames`

The PR is already merged. I read the diff only and did not build it or run the tests.

### Summary
The fix is correct for the reported regressions: `okio/internal/-ByteStringNonJs`, `package-info`, Kotlin names like `my-function`, and names that start with a digit. Moving from "Java identifier" rules to the JVMS rules is the right direction, and the new tests cover a lot of ground.

### Issues and concerns

1. **The implementation is stricter than the PR description says.**
   - The description says only an empty part, `;` or `[` are rejected. The code also rejects `<` and `>`, and it applies the JVMS 4.2.3 module/package-name rules (`\`, `:` and `@` escaping, and control characters 0x00–0x1F in package parts).
   - JVMS 4.2.2 forbids only `. ; [ /` in unqualified names. `<` and `>` are forbidden only for method names.
   - Section 4.2.3 governs `CONSTANT_Package_info` and `CONSTANT_Module_info`, not binary class names. A loader that mirrors it can reject names the JVM itself would accept. For example, a package part containing an unescaped `@` or `:`, or a bare `\`, is rejected.
   - The failure mode is the same as the regression this PR fixes: a spurious `ClassNotFoundException` or `NoClassDefFoundError` for a legal class.
   - This is rare in practice. Still, the point of the check is to skip expensive loads for names that are definitely invalid, so it should lean permissive. Consider dropping `<`/`>` and the escape logic unless there is a concrete reason for them. If they stay, the description and Javadoc should say why.

2. **Undocumented behavior change: `isValidResourceName` is removed.** The `findResource` and `findResources` guards that rejected empty names and names containing `:` are gone, along with their tests. This looks intentional, since it reverts the earlier "bypass unnecessary load operations" change. The PR description doesn't mention it, though, and it is a separate change from the class-name fix. Confirm that `Collections` is still used in `JarUrlClassLoader`, so there is no unused import for checkstyle to flag.

3. **The escape state machine is hard to follow.**
   - `validPackagePart` and `escape` interact in subtle ways. For example, `isInRestrictedPackageCharacterRange` runs before the escape branch, and a trailing `\` in the final part is silently accepted.
   - The simple class name (the last part) is never checked against the package rules. The tests show this is intended (`My@Class` is valid), but it is easy to misread.
   - Splitting into "split on separators", then "validate each package part", then "validate the simple name" would be clearer. It would also make the permissive rules easier to state.

4. **Nit: the Javadoc has a typo.** "Return true of the class name" should read "if the class name". The link also points to the `se14` spec, so consider linking a current one.

5. **Test nits.**
   - `assertThatIsValidClassName("com.")` appears twice in `isValidClassNameWhenInvalidReturnsFalse`.
   - The test names `isValidWhen...` don't match the `isValidClassNameWhen...` prefix used elsewhere.
   - There are no tests at the `JarUrlClassLoader` level. An integration-style test that loads a class such as `-Foo` or `package-info` from a nested jar would guard against this regression recurring.
   - Add cases for a name with a trailing `\`, a `$`-only inner name, and non-BMP or Unicode characters.

### Performance
The check is a single O(n) pass with no allocation, so there is no concern. Because the rules are now looser, the check rejects fewer names early. That is the intended trade-off.

### Security
None. The check is a pre-filter and not a security boundary. Rejecting `;` and `[` still stops array-descriptor-style names from reaching the load path.

### Verdict
The change is good because it fixes a real regression. The main follow-up is to align the validation with JVMS 4.2.2 for class names rather than the stricter 4.2.3 package rules. The PR description should also mention the removal of the resource-name checks.

# REVIEW B

# Review of PR #52284: accept all valid JVM class names in `LoadableNames`

The PR is already merged, and no `CLAUDE.md` exists in the checkout. I read the diff against the Spring Boot conventions I know, and I didn't build or run the tests.

## Summary
The fix is sound. #52271 limited class names to Java identifiers, but the JVM allows far more (JVMS 4.2). That broke `okio/internal/-ByteStringNonJs`, `package-info` and similar names. The PR now rejects only what the JVM can't accept:
- empty name parts
- `;`, `[`, `<` and `>`
- control characters in package parts
- unescaped `:`, `@` and `\` in package parts

The tests cover the regression cases well.

## Issues and suggestions

1. **The PR description doesn't match the code.** It says only an empty name part, `;` or `[` are rejected. The code also rejects `<`, `>`, control characters in package parts, and unescaped `:`, `@` and `\` in package parts. The code follows the spec more closely, so I'd update the description.

2. **Removing `isValidResourceName` is a separate behavior change.**
   - `findResource` and `findResources` no longer reject names containing `:` or empty names. The description doesn't mention this.
   - The old `:` check likely guarded against URL and protocol-style names such as `jar:` reaching the nested-jar lookup.
   - If dropping it is intentional, say so and add a test that `findResource("test:test")` and `findResource("")` return null or empty without exceptions. Otherwise, consider keeping a minimal check.
   - Check that the `Collections` import in `JarUrlClassLoader` is still used. Checkstyle fails the build on unused imports.

3. **The validation state machine is hard to follow.**
   - `validPackagePart` and `escape` interact subtly. The simple class name (the last part) is deliberately exempt from the package rules, as the `My@Class` tests show, but nothing in the code says so.
   - A short comment, or extracting a per-part helper, would make this easier to maintain.
   - The `escape && ch == ESCAPE` handling and `validPackagePart && …` chains could be flattened.
   - The check `escape` before a separator rejects `a\.b`. That's consistent with the tests, but the JVMS escaping rules are written for module names, so a comment citing the intent would help.

4. **Control characters are checked only in package parts.** The class part can contain `\u0000`. That's probably fine because the JVM would reject it later, but the early check is meant to be a cheap filter, so the asymmetry is worth a comment.

5. **Nits**
   - The Javadoc says "Return true of the class name" and should say "if".
   - `"com."` appears twice in the invalid tests.
   - The class Javadoc still says "check names are valid before performing expensive loading operations", but only class names remain.
   - `i == 0 || i == name.length() - 1` plus `name.charAt(i + 1)` is safe because of the length check, but the order of the conditions is easy to break in later edits.
   - `ch >= 0` is always true for a `char`, so the lower bound in `isInRestrictedPackageCharacterRange` is redundant. Static analysis may flag it.
   - The test names `isValidWhenPackageName…` omit "ClassName", unlike the others.

## Performance
The check is a single O(n) pass with no allocation, so it's fine as a pre-filter.

## Security
Rejecting `;`, `[`, `<` and `>` still blocks array and descriptor-style names. Loosening the rule is safe because the name only gates the lookup. The one thing to confirm is point 2, the dropped `:` filter on resources.

## Test coverage
Coverage is good for `LoadableNames`: escapes, control-character boundaries, separator edge cases and the regression names. Two gaps:
- There is no integration-level test in the loader that loads a class such as `-ByteStringNonJs` from a nested jar. That would guard against this regression recurring.
- There is no test for the resource-name path after the validation was removed.

**Verdict:** the change looks correct. I'd follow up on the resource-name behavior change and the description mismatch, and treat the rest as nits.
