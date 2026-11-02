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

# Review of PR 163282: share `GitInfo` via a build service (backport to 9.5 of #162435)

I found no blocking problems. This is a clean backport of a build-logic change. I read the diff only and did not run the build or the new func tests.

## What it does
- It adds `GitInfoService`, a per-build `BuildService` that holds a memoized `GitInfoValueSource` provider.
- `GitInfoPlugin` now gets its git root from `project.getLayout().getSettingsDirectory()` instead of walking the Gradle build hierarchy.
- `LicensingPlugin` and `PublishPlugin` apply the plugin to their own project, not `getRootProject()`. That removes the cross-project access that isolated projects forbid.
- It adds `GitInfoPluginFuncTest`.

## Observations

1. **Existing bug in `GitInfoPlugin.apply`, not fixed here.**
   - The line `info.getRevision() == null ? info.getRevision() : "main"` is inverted. It returns `null` when the revision is missing and `"main"` when it is present.
   - The intent was almost certainly "fall back to `main` when null".
   - `LicensingPlugin` uses this provider for snapshot license URLs, so snapshot builds likely link to `main` instead of the commit.
   - It is out of scope for a faithful backport. I'd fix it in a separate PR against `main`, with a func test that asserts the license commit.

2. **`findGitRootDir` behaves differently from the old lookup.**
   - Before, a missing `.git` fell back to `Util.locateElasticsearchWorkspace`. Now it checks only the settings dir, then its direct parent (looking for `build-tools-internal/version.properties`), and otherwise returns `settingsDir`.
   - This covers `build-conventions`, `build-tools` and `build-tools-internal`, and the func test covers the submodule case.
   - If a build is ever included from a deeper directory, git info would silently resolve against the wrong directory.
   - It would be safer to log or fail when neither check matches. Alternatively, walk up the parent directories until `.git` is found.

3. **`GitInfoService` reads its parameter eagerly.** The constructor calls `getParameters().getGitRootDir().get()`. That is fine because `registerIfAbsent` always sets it, but `registerIfAbsent` keeps the first registration. If a different settings dir ever reaches it first, later projects silently reuse that first value. The old code created a separate provider per applying project. Gradle shared services are per-build, so this should be fine today. A short comment would help.

4. **Tests.**
   - The func test is good. It covers isolated projects, the configuration-cache hit and miss cases, and included builds, and it fakes git without needing a binary.
   - Gaps: nothing tests the missing-git fallback in point 2, and nothing tests `PublishPlugin`'s POM generation with the new per-project application.
   - The Windows ignore refers to issue #129100, which is consistent with other func tests.

5. **Style.** Javadoc is present and explains the "why", as AGENTS.md asks. There are no wildcard imports. The license header looks correct for the file's location. `GitInfoService.NAME = "gitInfo"` is a generic name that could collide with another service. A more specific name would be safer.

## Verdict
LGTM for the backport. I'd follow up on the inverted revision fallback in point 1 and on error handling in `findGitRootDir`.

# REVIEW B

## Review: #163282, backport of #162435 to 9.5 ("Share GitInfo via build service for Isolated Projects")

I read the diff but not the whole thing. The tool output was truncated, so I did not see the full `GitInfoService` source or the first half of the new Spock spec. The comments below cover the parts I did see.

### Summary
`GitInfoPlugin` no longer reads from `project.getRootProject()` or `Util.locateElasticsearchWorkspace(gradle)`, which isolated projects forbid. Instead it registers a shared build service, `GitInfoService`, and each project applies the plugin to itself. `LicensingPlugin` and `PublishPlugin` now apply the plugin to `project` instead of the root project. A new Spock spec runs the plugin against fake git repos, including nested included builds, with isolated projects enabled.

### What looks good
- The approach fits isolated projects. `registerIfAbsent` with a settings-directory-based parameter avoids cross-project access, and the git lookup is still done once per build.
- `findGitRootDir` is a small static helper, so it can be tested on its own. Its Javadoc explains why it avoids `Util#locateElasticsearchWorkspace`.
- The test uses a hand-built `.git` directory with HEAD, a branch ref and an origin remote. That covers the case of a submodule with its own `.git` and the case of `build-tools` without one, so it is fast and hermetic. The comment on Gradle 8 build-path semantics is useful.
- The changes to `LicensingPlugin` and `PublishPlugin` are minimal.

### Issues and suggestions

1. **Inverted null check (carried over, not new).**
   - `revision = getGitInfo().map(info -> info.getRevision() == null ? info.getRevision() : "main");` returns the revision only when it is null, and `"main"` otherwise. It almost certainly should be `!= null ? info.getRevision() : "main"`.
   - This provider feeds `LicensingPlugin`'s license commit for snapshot versions. Because the plugin is now applied per project, the bug is more visible.
   - The same bug is on `main`. Fix it there first and backport the fix, rather than diverging on 9.5. The new spec only checks the `printGitInfo` task, so it would not catch this.

2. **Root-detection heuristic is fragile.**
   - `findGitRootDir` falls back to `settingsDir.getParentFile()` when `build-tools-internal/version.properties` exists there. This ties git discovery to one marker file. If the layout changes, it silently returns `settingsDir`, and `GitInfo` may then report no revision or origin.
   - The final fallback is also silent. Consider logging at debug level, or walking up to the nearest `.git` (file or directory) with a bounded depth. A `.git` *file* is how worktrees and submodules are laid out, and `.exists()` handles that today, but the walk-up is more general.

3. **Service registered with `registerIfAbsent` from many projects.** The parameters come from whichever project registers first. The settings directory is the same for all projects in one build, so this is fine. Included builds each have their own `Gradle` instance, so each gets its own service. That matches the test, but add a short comment so nobody later assumes one global instance.

4. **Test coverage.**
   - The spec covers the main layouts. A unit test for `findGitRootDir` itself would be cheap: `.git` present, parent marker present, and neither.
   - Add a test for the "no git" case (no `.git` anywhere), since the plugin should degrade gracefully, for example in source-tarball builds.
   - Add a regression test for the revision/`main` fallback described in item 1.

5. **Backport hygiene.** The PR is already merged with `auto-merge-without-approval`. Check that the 9.5 Gradle wrapper version supports `getLayout().getSettingsDirectory()` (Gradle 8.8 or later) and `ISOLATED_PROJECTS` in the test runner. If the build had passed on 9.5 CI, this is moot.

### Security / performance
- No security concerns. The service only reads local `.git` files.
- Performance should improve or stay neutral. The git lookup is shared, and the `ValueSource` is replaced by a build service whose output is memoized as a provider.

### Verdict
Looks good as a clean backport. Fix the inverted null check as a follow-up on `main`, then backport it, and consider adding the small tests from item 4.
