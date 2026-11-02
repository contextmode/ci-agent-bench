# PR diff (the real change)

```diff
diff --git a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/GitInfoPlugin.java b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/GitInfoPlugin.java
index 6f64edfc8c0dc..645d036f5cea7 100644
--- a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/GitInfoPlugin.java
+++ b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/GitInfoPlugin.java
@@ -10,41 +10,54 @@
 package org.elasticsearch.gradle.internal.conventions;
 
 import org.elasticsearch.gradle.internal.conventions.info.GitInfo;
-import org.elasticsearch.gradle.internal.conventions.info.GitInfoValueSource;
-import org.elasticsearch.gradle.internal.conventions.util.Util;
+import org.elasticsearch.gradle.internal.conventions.info.GitInfoService;
 import org.gradle.api.Plugin;
 import org.gradle.api.Project;
 import org.gradle.api.provider.Property;
 import org.gradle.api.provider.Provider;
-import org.gradle.api.provider.ProviderFactory;
 
 import java.io.File;
 
-import javax.inject.Inject;
-
+/**
+ * Exposes the {@link GitInfo} of the repository containing the current build.
+ *
+ * <p>This plugin can be applied to any project. The git lookup itself is shared across all projects of a
+ * build via {@link GitInfoService}, so consumers should apply it to the project they configure instead
+ * of reaching into the root project, which is not allowed with Gradle's isolated projects.
+ */
 public abstract class GitInfoPlugin implements Plugin<Project> {
 
-    private ProviderFactory factory;
     private Provider<String> revision;
 
-    @Inject
-    public GitInfoPlugin(ProviderFactory factory) {
-        this.factory = factory;
-    }
-
     @Override
     public void apply(Project project) {
-        File rootDir = getGitRootDir(project);
-        getGitInfo().convention(factory.of(GitInfoValueSource.class, spec -> { spec.getParameters().getPath().set(rootDir); }));
+        File settingsDir = project.getLayout().getSettingsDirectory().getAsFile();
+        Provider<GitInfoService> service = project.getGradle()
+            .getSharedServices()
+            .registerIfAbsent(
+                GitInfoService.NAME,
+                GitInfoService.class,
+                spec -> spec.getParameters().getGitRootDir().set(findGitRootDir(settingsDir))
+            );
+        getGitInfo().convention(service.flatMap(GitInfoService::getGitInfo));
         revision = getGitInfo().map(info -> info.getRevision() == null ? info.getRevision() : "main");
     }
 
-    private static File getGitRootDir(Project project) {
-        File rootDir = project.getRootDir();
-        if (new File(rootDir, ".git").exists()) {
-            return rootDir;
+    /**
+     * Resolves the git working tree root for the build rooted at {@code settingsDir}. For the {@code build-conventions}
+     * and {@code build-tools*} included builds, which live directly inside the elasticsearch workspace, this is the
+     * workspace directory. Unlike {@code Util#locateElasticsearchWorkspace} this does not navigate the Gradle build
+     * hierarchy, which is not allowed with isolated projects.
+     */
+    static File findGitRootDir(File settingsDir) {
+        if (new File(settingsDir, ".git").exists()) {
+            return settingsDir;
+        }
+        File parent = settingsDir.getParentFile();
+        if (parent != null && new File(parent, "build-tools-internal/version.properties").exists()) {
+            return parent;
         }
-        return Util.locateElasticsearchWorkspace(project.getGradle());
+        return settingsDir;
     }
 
     public abstract Property<GitInfo> getGitInfo();
diff --git a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/LicensingPlugin.java b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/LicensingPlugin.java
index 63514ae671bf3..0c11f516acb68 100644
--- a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/LicensingPlugin.java
+++ b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/LicensingPlugin.java
@@ -33,7 +33,7 @@ public LicensingPlugin(ProviderFactory providerFactory) {
 
     @Override
     public void apply(Project project) {
-        Provider<String> revision = project.getRootProject().getPlugins().apply(GitInfoPlugin.class).getRevision();
+        Provider<String> revision = project.getPlugins().apply(GitInfoPlugin.class).getRevision();
         Provider<String> licenseCommitProvider = providerFactory.provider(
             () -> isSnapshotVersion(project) ? revision.get() : "v" + project.getVersion()
         );
diff --git a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/PublishPlugin.java b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/PublishPlugin.java
index cf245ab3aedb2..86e009c161f3f 100644
--- a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/PublishPlugin.java
+++ b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/PublishPlugin.java
@@ -129,7 +129,7 @@ private static String getArchivesBaseName(ExtensionContainer extensions) {
      * Configuration generation of maven poms.
      */
     private void configurePomGeneration(Project project) {
-        var gitInfo = project.getRootProject().getPlugins().apply(GitInfoPlugin.class).getGitInfo();
+        var gitInfo = project.getPlugins().apply(GitInfoPlugin.class).getGitInfo();
         var generatePomTask = project.getTasks().register("generatePom");
         project.getTasks().named(LifecycleBasePlugin.ASSEMBLE_TASK_NAME).configure(assemble -> assemble.dependsOn(generatePomTask));
         var extensions = project.getExtensions();
diff --git a/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/info/GitInfoService.java b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/info/GitInfoService.java
new file mode 100644
index 0000000000000..ab0d346262ba1
--- /dev/null
+++ b/build-conventions/src/main/java/org/elasticsearch/gradle/internal/conventions/info/GitInfoService.java
@@ -0,0 +1,52 @@
+/*
+ * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
+ * or more contributor license agreements. Licensed under the "Elastic License
+ * 2.0", the "GNU Affero General Public License v3.0 only", and the "Server Side
+ * Public License v 1"; you may not use this file except in compliance with, at
+ * your election, the "Elastic License 2.0", the "GNU Affero General Public
+ * License v3.0 only", or the "Server Side Public License, v 1".
+ */
+
+package org.elasticsearch.gradle.internal.conventions.info;
+
+import org.gradle.api.provider.Property;
+import org.gradle.api.provider.Provider;
+import org.gradle.api.provider.ProviderFactory;
+import org.gradle.api.services.BuildService;
+import org.gradle.api.services.BuildServiceParameters;
+
+import java.io.File;
+
+import javax.inject.Inject;
+
+/**
+ * Build-scoped holder for the {@link GitInfo} of the git repository that contains the current build.
+ *
+ * <p>Every project that needs git information shares a single instance of this service, so the git
+ * metadata is resolved at most once per build. This replaces applying {@code GitInfoPlugin} to the
+ * root project from other projects, which is not compatible with Gradle's isolated projects.
+ *
+ * <p>The value is still backed by {@link GitInfoValueSource} so that the configuration cache tracks
+ * it as a build input whenever it is read at configuration time.
+ */
+public abstract class GitInfoService implements BuildService<GitInfoService.Params> {
+
+    public static final String NAME = "gitInfo";
+
+    private final Provider<GitInfo> gitInfo;
+
+    @Inject
+    public GitInfoService(ProviderFactory providerFactory) {
+        File gitRootDir = getParameters().getGitRootDir().get();
+        // a value source provider memoizes its value, so sharing this instance means a single lookup per build
+        this.gitInfo = providerFactory.of(GitInfoValueSource.class, spec -> spec.getParameters().getPath().set(gitRootDir));
+    }
+
+    public Provider<GitInfo> getGitInfo() {
+        return gitInfo;
+    }
+
+    public interface Params extends BuildServiceParameters {
+        Property<File> getGitRootDir();
+    }
+}
diff --git a/build-tools-internal/src/integTest/groovy/org/elasticsearch/gradle/internal/GitInfoPluginFuncTest.groovy b/build-tools-internal/src/integTest/groovy/org/elasticsearch/gradle/internal/GitInfoPluginFuncTest.groovy
new file mode 100644
index 0000000000000..362e07df92a48
--- /dev/null
+++ b/build-tools-internal/src/integTest/groovy/org/elasticsearch/gradle/internal/GitInfoPluginFuncTest.groovy
@@ -0,0 +1,213 @@
+/*
+ * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
+ * or more contributor license agreements. Licensed under the "Elastic License
+ * 2.0", the "GNU Affero General Public License v3.0 only", and the "Server Side
+ * Public License v 1"; you may not use this file except in compliance with, at
+ * your election, the "Elastic License 2.0", the "GNU Affero General Public
+ * License v3.0 only", or the "Server Side Public License, v 1".
+ */
+
+package org.elasticsearch.gradle.internal
+
+import spock.lang.IgnoreIf
+
+import org.elasticsearch.gradle.fixtures.AbstractGradleFuncTest
+
+/**
+ * Covers how {@code GitInfoPlugin} resolves and shares git metadata via the per-build {@code GitInfoService}:
+ * <ul>
+ *     <li>plugins consuming git info ({@code elasticsearch.licensing} here) are applied to subprojects only and must not
+ *     reach into the root project, so the build has to pass with isolated projects enabled</li>
+ *     <li>git metadata stays a configuration cache input, both when read at execution time and at configuration time</li>
+ *     <li>included builds resolve the git root the same way as before: their own {@code .git} first (e.g. the
+ *     elasticsearch submodule inside elasticsearch-serverless), otherwise the enclosing elasticsearch workspace
+ *     (e.g. {@code build-tools})</li>
+ * </ul>
+ * Git repositories are faked with the minimal set of files {@code GitInfo} reads, so no git binary is required.
+ */
+// Ignoring this test on windows due to what appears to be a bug in the gradle testkit runner.
+// https://github.com/elastic/elasticsearch/issues/129100
+@IgnoreIf({ os.isWindows() })
+class GitInfoPluginFuncTest extends AbstractGradleFuncTest {
+
+    private static final String ISOLATED_PROJECTS = "-Dorg.gradle.unsafe.isolated-projects=true"
+
+    private static final String REVISION_1 = "1111111111111111111111111111111111111111"
+    private static final String REVISION_2 = "2222222222222222222222222222222222222222"
+    private static final String SUBMODULE_REVISION = "3333333333333333333333333333333333333333"
+
+    private static final String ORIGIN = "https://github.com/acme/outer.git"
+    private static final String SUBMODULE_ORIGIN = "https://github.com/acme/inner.git"
+
+    def "subprojects share git info without accessing the root project"() {
+        given:
+        fakeGitRepository(new File(projectDir, ".git"), REVISION_1, ORIGIN)
+        gitInfoProbe(subProject(":lib-a"))
+        gitInfoProbe(subProject(":lib-b"))
+
+        when:
+        def result = gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+
+        then:
+        result.output.contains("GITINFO :lib-a revision=${REVISION_1} origin=${ORIGIN}")
+        result.output.contains("GITINFO :lib-b revision=${REVISION_1} origin=${ORIGIN}")
+    }
+
+    def "configuration cache is reused and git changes are picked up when read at execution time"() {
+        given:
+        def gitDir = new File(projectDir, ".git")
+        fakeGitRepository(gitDir, REVISION_1, ORIGIN)
+        gitInfoProbe(subProject(":lib-a"))
+
+        when:
+        gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+        def reused = gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+
+        then:
+        reused.output.contains("Reusing configuration cache.")
+        reused.output.contains("GITINFO :lib-a revision=${REVISION_1} origin=${ORIGIN}")
+
+        when:
+        new File(gitDir, "refs/heads/main").text = REVISION_2 + "\n"
+        def afterCommit = gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+
+        then:
+        // git info is only read at execution time here, so switching commits or branches must not invalidate the cache
+        afterCommit.output.contains("Reusing configuration cache.")
+        afterCommit.output.contains("GITINFO :lib-a revision=${REVISION_2} origin=${ORIGIN}")
+    }
+
+    def "configuration cache is invalidated when git info read at configuration time changes"() {
+        given:
+        def gitDir = new File(projectDir, ".git")
+        fakeGitRepository(gitDir, REVISION_1, ORIGIN)
+        gitInfoProbe(subProject(":lib-a")) << """
+            println "CONFIGURED revision=\${gitInfo.get().revision}"
+        """
+
+        when:
+        gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+        def reused = gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+
+        then:
+        reused.output.contains("Reusing configuration cache.")
+        reused.output.contains("CONFIGURED") == false
+
+        when:
+        new File(gitDir, "refs/heads/main").text = REVISION_2 + "\n"
+        def afterCommit = gradleRunner("printGitInfo", ISOLATED_PROJECTS).build()
+
+        then:
+        afterCommit.output.contains("Reusing configuration cache.") == false
+        afterCommit.output.contains("CONFIGURED revision=${REVISION_2}")
+        afterCommit.output.contains("GITINFO :lib-a revision=${REVISION_2} origin=${ORIGIN}")
+    }
+
+    def "included builds resolve their own git root or the enclosing elasticsearch workspace"() {
+        given:
+        // outer repository, e.g. elasticsearch-serverless
+        fakeGitRepository(new File(projectDir, ".git"), REVISION_1, ORIGIN)
+        gitInfoProbe(subProject(":lib-a"))
+
+        // an included build checked out as git submodule, e.g. the elasticsearch submodule in serverless
+        def submoduleGitDir = new File(projectDir, ".git/modules/elasticsearch")
+        fakeGitRepository(submoduleGitDir, SUBMODULE_REVISION, SUBMODULE_ORIGIN)
+        def submodule = new File(projectDir, "elasticsearch")
+        file(submodule, ".git").text = "gitdir: ../.git/modules/elasticsearch\n"
+        file(submodule, "build-tools-internal/version.properties").text = versionPropertiesFile.text
+        includedBuild(submodule)
+
+        // an included build without its own .git living inside the elasticsearch workspace, e.g. build-tools
+        includedBuild(new File(submodule, "build-tools"))
+
+        settingsFile << """
+            includeBuild 'elasticsearch'
+            includeBuild 'elasticsearch/build-tools'
+        """
+
+        when:
+        // Since Gradle 8.0 the build path follows the directory hierarchy of included builds, so the build at
+        // 'elasticsearch/build-tools' is addressed as ':elasticsearch:build-tools' although both are included from the root
+        // settings. See https://docs.gradle.org/current/userguide/upgrading_version_7.html ("Changes to paths of included builds")
+        def result = gradleRunner(
+            ":lib-a:printGitInfo",
+            ":elasticsearch:lib:printGitInfo",
+            ":elasticsearch:build-tools:lib:printGitInfo",
+            ISOLATED_PROJECTS
+        ).build()
+
+        then:
+        result.output.contains("GITINFO :lib-a revision=${REVISION_1} origin=${ORIGIN}")
+        result.output.contains("GITINFO :elasticsearch:lib revision=${SUBMODULE_REVISION} origin=${SUBMODULE_ORIGIN}")
+        result.output.contains("GITINFO :elasticsearch:build-tools:lib revision=${SUBMODULE_REVISION} origin=${SUBMODULE_ORIGIN}")
+    }
+
+    /**
+     * Creates the subset of a git directory that {@code GitInfo} reads: HEAD, the referenced branch and the origin remote.
+     */
+    private static void fakeGitRepository(File gitDir, String revision, String origin) {
+        gitDir.mkdirs()
+        new File(gitDir, "HEAD").text = "ref: refs/heads/main\n"
+        def ref = new File(gitDir, "refs/heads/main")
+        ref.parentFile.mkdirs()
+        ref.text = revision + "\n"
+        new File(gitDir, "config").text = """\
+            [core]
+            \trepositoryformatversion = 0
+            [remote "origin"]
+            \turl = ${origin}
+            \tfetch = +refs/heads/*:refs/remotes/origin/*
+        """.stripIndent()
+    }
+
+    /**
+     * Creates a standalone build with a single {@code :lib} project applying the git info probe.
+     */
+    private void includedBuild(File buildDir) {
+        file(buildDir, "settings.gradle").text = """
+            rootProject.name = '${buildDir.name}'
+            include 'lib'
+        """
+        file(buildDir, "build.gradle").text = ""
+        gitInfoProbe(file(buildDir, "lib/build.gradle"))
+    }
+
+    /**
+     * Applies {@code elasticsearch.licensing}, which applies {@code GitInfoPlugin} to the same project, and registers a
+     * {@code printGitInfo} task that resolves git info at execution time. Exposes {@code gitInfo} for further use in the
+     * build script.
+     */
+    private static File gitInfoProbe(File buildFile) {
+        buildFile << """
+            plugins {
+                id 'elasticsearch.licensing'
+            }
+
+            abstract class PrintGitInfo extends DefaultTask {
+                @Input
+                abstract Property<String> getProjectPath()
+
+                @Input
+                abstract Property<String> getRevision()
+
+                @Input
+                abstract Property<String> getOrigin()
+
+                @TaskAction
+                void print() {
+                    println "GITINFO \${projectPath.get()} revision=\${revision.get()} origin=\${origin.get()}"
+                }
+            }
+
+            def gitInfo = plugins.getPlugin(org.elasticsearch.gradle.internal.conventions.GitInfoPlugin).gitInfo
+            // build tree path includes the included build's path, e.g. ':elasticsearch:lib'
+            def projectBuildTreePath = buildTreePath
+            tasks.register('printGitInfo', PrintGitInfo) {
+                projectPath = projectBuildTreePath
+                revision = gitInfo.map { it.revision }
+                origin = gitInfo.map { it.origin }
+            }
+        """
+        buildFile
+    }
+}

```

# REVIEW A

# Review of #163282: share GitInfo via a build service (9.5 backport of #162435)

This is a clean backport. I found no blocking issues. The PR is already merged, so these notes are for the record or follow-up.

## What it does
- `GitInfoService` is a new build-scoped `BuildService`. It wraps a memoized `GitInfoValueSource` provider, so the git lookup happens once per build.
- `GitInfoPlugin` now registers the service with `registerIfAbsent` on `project.getGradle()`. It resolves the git root from the settings directory instead of calling `Util.locateElasticsearchWorkspace`.
- `LicensingPlugin` and `PublishPlugin` apply the plugin to their own project instead of `project.getRootProject()`. This removes the cross-project access that isolated projects forbid.
- `GitInfoPluginFuncTest` covers four cases: isolated projects, configuration cache reuse, cache invalidation when git info is read at configuration time, and included builds.

## Code quality
- **Good:**
  - The Javadoc explains why the code is shaped this way.
  - Keeping `GitInfoValueSource` underneath preserves configuration-cache input tracking.
  - The tests fake the `.git` directory, so no git binary is needed.
  - The test is `@IgnoreIf` on Windows with the issue link.
- **`GitInfoPlugin.findGitRootDir`:** it silently falls back to `settingsDir` when neither `.git` nor the parent workspace marker is found. The old code threw from `locateElasticsearchWorkspace` in a similar situation. The fallback is probably fine, for example for source tarballs without `.git`, but I'd confirm `GitInfoValueSource` handles a missing `.git` gracefully. A short comment or a func test for that case would help.
- **Marker file:** the check relies on `build-tools-internal/version.properties` in the parent directory. That is reasonable, but it is a hidden coupling. A comment pointing at why that file was chosen would help future maintainers.
- **Pre-existing bug, untouched here:** the line `revision = getGitInfo().map(info -> info.getRevision() == null ? info.getRevision() : "main")` has an inverted condition. It returns `null` (an empty provider) when the revision is null and `"main"` otherwise, so the real revision is never used. It is probably meant to be `!= null ? info.getRevision() : "main"`. Fixing it would change license URLs, so it belongs in a separate follow-up. It is worth tracking, because the new test covers `gitInfo` but not `getRevision()` as consumed by `LicensingPlugin`.
- **Eager `.get()`:** `GitInfoService`'s constructor calls `getGitRootDir().get()` eagerly. That is safe because the parameter is always set, but you could pass the provider into the value source spec lazily.

## Potential bugs and risks
- `registerIfAbsent` keeps the parameters of the first registrant. The directory is derived from the settings directory, which is the same for all projects in a build, so this is consistent. If anyone later passes a different directory, it would be silently ignored.
- `Project.getLayout().getSettingsDirectory()` needs a recent Gradle version (8.x). The wrapper on 9.5 should satisfy this, but it is worth confirming the wrapper version on the backport branch matches `main`.

## Performance
- This is an improvement. The git lookup is shared and memoized per build, and the cross-project root plugin application is gone.

## Security
- No concerns. The service only reads local `.git` metadata and takes no external input.

## Test coverage
- Coverage is strong for the new behavior. It covers sharing across subprojects, cache reuse, and invalidation. It also covers resolving a submodule's own `.git` and the enclosing workspace for `build-tools`.
- **Gaps:**
  - No test for the "no `.git` anywhere" fallback.
  - No test asserting the `getRevision()` value consumed by `LicensingPlugin` (which would expose the inverted condition above).
  - `PublishPlugin`'s POM generation path is not exercised under isolated projects.

**Verdict:** LGTM as a backport. The inverted `revision` condition is the main follow-up.

# REVIEW B

# Review of PR 163282: share `GitInfo` via a build service for Isolated Projects

This is a backport of #162435 to 9.5, and it is already merged. The change looks correct and tightly scoped. I only read the diff and did not build or run the tests.

## Summary
`GitInfoPlugin` used to be applied to the root project from other projects, through `project.getRootProject().getPlugins().apply(...)`. That is incompatible with Gradle Isolated Projects. The PR replaces it with a build-scoped `GitInfoService`, registered with `registerIfAbsent`. `LicensingPlugin` and `PublishPlugin` now apply the plugin to their own project instead of the root project. The git root is resolved from the settings directory, with no navigation of the build hierarchy.

## What looks good
- **Isolated Projects:** Applying the plugin per project and sharing state through a build service is the right pattern. Nothing reaches across project boundaries any more.
- **One git lookup per build:** `GitInfoValueSource` still backs the value, so the configuration cache still tracks it as an input. The comment explaining that the provider is memoized is useful.
- **`findGitRootDir`:** It keeps the old behavior. It uses the build's own `.git` first, which covers the serverless submodule case. Otherwise it uses the enclosing workspace, detected through `build-tools-internal/version.properties`. It is package-private and static, which makes it easy to test.
- **Tests:** `GitInfoPluginFuncTest` is thorough. It runs with isolated projects on and covers:
  - sharing across subprojects;
  - configuration cache reuse when git info is read at execution time;
  - configuration cache invalidation when it is read at configuration time;
  - included builds, both with their own `.git` and nested inside the workspace.

  The tests fake the git directory instead of shelling out to git, which keeps them hermetic. The Windows `@IgnoreIf` references the existing issue (#129100).
- **Javadoc:** The new classes and the plugin explain why they exist, as AGENTS.md asks.

## Issues and suggestions
1. **Pre-existing inverted null check (not introduced here, but worth fixing):** In `GitInfoPlugin.apply`, `revision = getGitInfo().map(info -> info.getRevision() == null ? info.getRevision() : "main");` has the ternary backwards. It returns `null` when the revision is null and `"main"` when a revision exists. The fallback should be `info.getRevision() == null ? "main" : info.getRevision()`. A `null` return from `map` yields an empty provider. `LicensingPlugin` calls `revision.get()` for snapshot versions, so it would fail in that case. When a revision does exist, the license URL points at `main` instead of the commit. The diff touches this exact line's neighbors and `LicensingPlugin` now consumes it per project, so a follow-up fix with a func test assertion on `getRevision()` would be cheap.
2. **`registerIfAbsent` ignores parameters on later calls:** The first registrant wins. Today every project in a build has the same `settingsDir`, so this is safe. A short comment saying so would help future maintainers.
3. **Fallback in `findGitRootDir`:** If neither `.git` nor the workspace marker is found, it silently returns `settingsDir`. `GitInfoValueSource` then presumably reports unknown values, which matches the old fallback. Consider a debug log or a comment that this is intentional, for example for source tarball builds.
4. **Test gaps (minor):**
   - There is no unit test for `findGitRootDir` on its own, such as a `.git` file for a submodule or a missing marker. The func test covers the main paths.
   - There is no test for `PublishPlugin`'s POM generation with the per-project plugin application.
5. **Backport hygiene:** The backport appears to be a clean cherry-pick. I assume the `-Dorg.gradle.unsafe.isolated-projects` flag and `getSettingsDirectory()` are supported by the Gradle version on 9.5. The func test passing in CI should confirm that.

## Security and performance
There are no security concerns. The change only reads local git metadata. Performance should improve slightly, because the git lookup is shared across projects.

## Verdict
Approve. The only follow-up I would suggest is the inverted `revision` ternary in item 1, which was already present before this PR.
