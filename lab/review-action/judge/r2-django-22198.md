# PR diff (the real change)

```diff
diff --git a/.github/workflows/docs.yml b/.github/workflows/docs.yml
index 68df359a14b4..f29efdab6f8f 100644
--- a/.github/workflows/docs.yml
+++ b/.github/workflows/docs.yml
@@ -48,6 +48,8 @@ jobs:
         run: make black
       - name: Spelling
         run: SPHINXOPTS="-q -W" make spelling
+      - name: EPUBCheck
+        run: SPHINXOPTS="-q" make epubcheck
 
   sphinx-extension-tests:
     runs-on: ubuntu-24.04
diff --git a/docs/Makefile b/docs/Makefile
index 706bcaf0a261..926128aee5e7 100644
--- a/docs/Makefile
+++ b/docs/Makefile
@@ -26,7 +26,7 @@ ALLSPHINXOPTS   = -n -d $(BUILDDIR)/doctrees -D language=$(LANGUAGEOPT) --jobs $
 # the i18n builder cannot share the environment and doctrees with the others
 I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
 
-.PHONY: help clean html htmlview dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext
+.PHONY: help clean html htmlview dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext epubcheck
 
 help:
 	@echo "Please use \`make <target>' where <target> is one of"
@@ -52,6 +52,7 @@ help:
 	@echo "  spelling   to check for typos in documentation"
 	@echo "  black      to apply the black formatting to code blocks in documentation"
 	@echo "  lint       to check for linting errors in documentation"
+	@echo "  epubcheck  to validate the epub build with EPUBCheck"
 
 
 clean:
@@ -187,6 +188,9 @@ lint:
 	@echo
 	@echo "Documentation lint complete."
 
+epubcheck: epub
+	$(PYTHON) -m epubcheck $(BUILDDIR)/epub/Django.epub
+
 check:
 	@echo "=== Spelling check ==="; \
 	$(MAKE) --no-print-directory SPHINXOPTS="-q -W" spelling; SPELLING=$$?; \
diff --git a/docs/_static/console-tabs.css b/docs/_static/console-tabs.css
index f89d6dd96575..1cd3278d914e 100644
--- a/docs/_static/console-tabs.css
+++ b/docs/_static/console-tabs.css
@@ -107,6 +107,10 @@
     }
 
     > section {
+        box-sizing: border-box;
+        max-width: 100%;
+        overflow-x: auto;
+        /* Place the panel on its own row and hide it until active. */
         flex-basis: 100%;
         display: none;
     }
diff --git a/docs/conf.py b/docs/conf.py
index 74ad7a0e2b2b..7516760d89f5 100644
--- a/docs/conf.py
+++ b/docs/conf.py
@@ -238,6 +238,8 @@ def django_release():
 # Add any paths that contain custom static files (such as style sheets) here,
 # relative to this directory. They are copied after the builtin static files,
 # so a file named "default.css" will overwrite the builtin "default.css".
+# All files in html_static_path are bundled into epub as well. Use
+# epub_exclude_files for any that are not epub compatible.
 html_static_path = ["_static"]
 
 html_css_files = [
@@ -435,7 +437,12 @@ def django_release():
 # epub_post_files = []
 
 # A list of files that should not be packed into the epub file.
-# epub_exclude_files = []
+epub_exclude_files = ["_static/console-tabs.css"]
+
+# Empty, rather than defaulting to html_css_files, because its only entry is
+# the console-tabs.css excluded above. Any epub compatible addition to
+# html_css_files needs repeating here.
+epub_css_files = []
 
 # The depth of the table of contents in toc.ncx.
 # epub_tocdepth = 3
diff --git a/docs/internals/contributing/writing-documentation.txt b/docs/internals/contributing/writing-documentation.txt
index 5ad9a01fc171..eaa3a0912703 100644
--- a/docs/internals/contributing/writing-documentation.txt
+++ b/docs/internals/contributing/writing-documentation.txt
@@ -142,6 +142,8 @@ will be themed differently than the documentation at
 `docs.djangoproject.com <https://docs.djangoproject.com/>`_. This is OK! If
 your changes look good on your local machine, they'll look good on the website.
 
+.. _documentation-autobuild:
+
 Automating documentation rebuilds
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
@@ -217,7 +219,8 @@ changes can be merged. They can also be run locally with a single command:
      $ make check
 
 This command runs all current checks and will include any new checks added in
-the future.
+the future, with the exception of :ref:`EPUBCheck <documentation-epub-check>`,
+which requires a Java runtime.
 
 .. _documentation-spelling-check:
 
@@ -289,6 +292,40 @@ The command prints any violations to the terminal in the form
   links into named references. The custom line length check should already skip
   common false positives such as headings, tables and long links.
 
+.. _documentation-epub-check:
+
+EPUBCheck
+---------
+
+Django's documentation is also available in EPUB format. EPUB is based on the
+HTML build but has several limitations that don't apply to content meant for
+web browsers. Verifying EPUB compatibility is particularly important when
+changing CSS files, images, or other assets that are included in the HTML
+documentation, or when altering any Sphinx ``toctree``.
+
+To ensure that the EPUB is valid, build it and check it with the `EPUBCheck`_
+tool from the ``docs`` directory:
+
+.. console::
+
+     $ make epubcheck
+
+Some ``NAV-011`` warnings are expected: they come from index pages with their
+own sections following a ``toctree``, which makes the table of contents link
+back to a document earlier in the EPUB reading order. Any errors, however,
+indicate a problem that should be fixed.
+
+The ``EPUBCheck`` tool requires Java, so it is not included in the standard
+set of :ref:`quality checks <documentation-checks>` run by ``make check``.
+
+Running ``sphinx-autobuild`` to :ref:`automatically rebuild
+<documentation-autobuild>` changes in HTML can interfere with EPUB builds.
+Sphinx warnings about ``.buildinfo.bak`` indicate overlapping builds that will
+lead to ``EPUBCheck`` errors. Stop ``sphinx-autobuild`` and run ``make clean``
+if this occurs.
+
+.. _EPUBCheck: https://www.w3.org/publishing/epubcheck/
+
 .. _documentation-link-check:
 
 Link check
diff --git a/docs/make.bat b/docs/make.bat
index 3dba849896a9..58d16bf81e2d 100644
--- a/docs/make.bat
+++ b/docs/make.bat
@@ -37,6 +37,7 @@ if "%1" == "help" (
 	echo.  spelling   to check for typos in documentation
 	echo.  black      to apply the black formatting to code blocks in documentation
 	echo.  lint       to check for linting errors in documentation
+	echo.  epubcheck  to validate the epub build with EPUBCheck
 	goto end
 )
 
@@ -116,10 +117,8 @@ if "%1" == "devhelp" (
 )
 
 if "%1" == "epub" (
-	%SPHINXBUILD% -b epub %ALLSPHINXOPTS% %BUILDDIR%/epub
+	call :run_epub
 	if errorlevel 1 exit /b 1
-	echo.
-	echo.Build finished. The epub file is in %BUILDDIR%/epub.
 	goto end
 )
 
@@ -189,6 +188,16 @@ results in %BUILDDIR%/doctest/output.txt.
 	goto end
 )
 
+if "%1" == "epubcheck" (
+	call :run_epub
+	if errorlevel 1 exit /b 1
+	python -m epubcheck %BUILDDIR%/epub/Django.epub
+	if errorlevel 1 exit /b 1
+	echo.
+	echo.EPUBCheck complete.
+	goto end
+)
+
 if "%1" == "spelling" (
 	call :run_spelling
 	goto end
@@ -213,6 +222,13 @@ if "%1" == "check" (
 	goto end
 )
 
+:run_epub
+	%SPHINXBUILD% -b epub %ALLSPHINXOPTS% %BUILDDIR%/epub
+	if errorlevel 1 exit /b 1
+	echo.
+	echo.Build finished. The epub file is in %BUILDDIR%/epub.
+	exit /b
+
 :run_spelling
 	%SPHINXBUILD% -b spelling %ALLSPHINXOPTS% %BUILDDIR%/spelling
 	if errorlevel 1 exit /b 1
diff --git a/docs/requirements.txt b/docs/requirements.txt
index 8cf23220a7ab..6ac9446f0efc 100644
--- a/docs/requirements.txt
+++ b/docs/requirements.txt
@@ -3,3 +3,4 @@ Sphinx>=7.3.0
 sphinxcontrib-spelling
 blacken-docs
 sphinx-lint
+epubcheck

```

# REVIEW A

## Review of PR #22198: accessible console tabs fixes and EPUBCheck

I read the diff and PR description. The repo has no `CLAUDE.md`, so I judged style against Django's contributing conventions. I didn't build the docs or run the checks.

### Summary
The PR does three things:
1. It excludes `console-tabs.css` from the EPUB build with `epub_exclude_files` and `epub_css_files = []`.
2. It constrains console tab panels to the available width, with horizontal scrolling.
3. It adds an `epubcheck` target to the Makefile and `make.bat`, a CI step, a `docs/requirements.txt` entry and contributor documentation.

The change is small and well scoped. The comments in `conf.py` explain why the settings exist, which will help the next person who edits `html_css_files`.

### Code quality
- **CSS (`console-tabs.css`)**: `box-sizing: border-box; max-width: 100%; overflow-x: auto` is a reasonable fix for panels clipped on the left. The new comment ("Place the panel on its own row…") describes the existing `flex-basis: 100%` and `display: none` lines. It would be clearer next to the `flex-basis` line.
- **`epub_css_files = []`**: This is coupled to `html_css_files`. The comment calls that out, but it is easy to forget, because a future epub-compatible CSS file added to `html_css_files` will silently be missing from the EPUB. A computed value would remove the coupling. One option is to filter `html_css_files` for everything except `console-tabs.css`.
- **Sphinx version**: The description says the exclusion API arrived in Sphinx 9.1, but `docs/requirements.txt` still says `Sphinx>=7.3.0`. On older Sphinx, the exclusion may not take effect. The EPUB would then still ship the incompatible CSS, and the new EPUBCheck CI step would fail. Either raise the minimum version or note why it isn't needed. The same applies to the default docs build in CI, which probably installs the latest Sphinx.
- **`make.bat`**: Factoring out `:run_epub` matches the existing `:run_spelling` pattern and works. Check that the `:run_epub` label, placed after the final `if` blocks, cannot be reached by fall-through. The `exit /b` at its end covers that. Windows users also need `python` on the `PATH`, and the Makefile uses `$(PYTHON)`, so the two are slightly inconsistent.
- **Makefile**: `epubcheck: epub` plus `$(PYTHON) -m epubcheck $(BUILDDIR)/epub/Django.epub` is straightforward. The hard-coded `Django.epub` name will break if `epub_basename` ever changes.

### Potential issues
- **CI**: `SPHINXOPTS="-q"` has no `-W`, so Sphinx warnings during the EPUB build don't fail the job. The docs say `.buildinfo.bak` warnings lead to EPUBCheck errors, so those would still be caught by the validator itself. Confirm that is intended.
- **Java dependency**: The `epubcheck` PyPI package needs a Java runtime. GitHub's `ubuntu-24.04` runners include one, but the dependency is implicit. Adding it to `docs/requirements.txt` means anyone running `pip install -r docs/requirements.txt` gets a package that fails at run time without Java. The documentation notes the Java requirement, which is good.
- **Expected `NAV-011` warnings**: The docs describe them as expected. If the tool exits non-zero on warnings, CI would fail. Presumably this was verified, since the PR was approved and merged.
- **Pinning**: `epubcheck` is unpinned, so a new upstream EPUBCheck release with stricter rules could break CI unexpectedly. Consider a version bound.

### Performance
There is no runtime impact. CI gains a full EPUB build plus validation, which adds time to the docs job. This is acceptable for the compatibility coverage it gives.

### Security
No concerns. The new dependency comes from PyPI, it runs only in docs CI, and the workflow does not add untrusted input.

### Tests
There are no automated tests for the CSS behavior, which is normal for Django docs. The EPUBCheck step is itself a regression test for the EPUB problem. There is no visual verification that the panels no longer clip in non-Django themes. The PR template asks for light and dark screenshots for UI changes, and none were attached.

### Docs
- The new EPUBCheck section is clear and cross-references well, and the `documentation-autobuild` anchor is a useful addition.
- The `make check` paragraph correctly says EPUBCheck is excluded.
- Minor: the text should say the first run may download the EPUBCheck jar, if that is true of the PyPI package. I haven't verified this.

### Verdict
The PR is good and was reasonably merged. The main follow-ups I'd suggest are to reconcile the Sphinx 9.1 requirement with the `Sphinx>=7.3.0` floor, to derive `epub_css_files` from `html_css_files` instead of duplicating it, and to consider pinning `epubcheck`.

# REVIEW B

**Review of django/django#22198 — "Fixed problems in accessible console tabs"**

This PR is already merged and approved. I found no blocking issues. I only read the diff and did not build the docs or run EPUBCheck. The repo has no CLAUDE.md, so I judged style against Django's contributing conventions.

**Overall:** The change is small and focused, and it matches its description. It fixes the epub CSS incompatibility and the clipped wide console-tab panels, and it adds EPUBCheck to catch future regressions.

**Code quality**
- **`docs/_static/console-tabs.css`:** `box-sizing: border-box`, `max-width: 100%` and `overflow-x: auto` are a sensible way to keep wide panels inside the available width. The new comment about the row and the hidden state clarifies the `flex-basis` and `display: none` lines.
- **`docs/conf.py`:** The comments explain why `epub_css_files = []` is empty. The risk is that someone adds an epub-compatible entry to `html_css_files` and forgets to repeat it in `epub_css_files`. Sphinx 9.1 supports this exclusion API, but `docs/requirements.txt` still says `Sphinx>=7.3.0`. Older Sphinx versions will ignore or mishandle the setting, so the epub could still include the CSS there. That is probably acceptable for a docs-only build, but it's worth confirming.
- **`docs/make.bat`:** Moving the epub build into a `:run_epub` subroutine avoids duplication. Check that `exit /b` and the `call :run_epub` flow behave correctly in batch. The label sits after the `if` chain, so it must be unreachable by fall-through. The existing `:run_spelling` follows the same pattern, so this is probably fine.
- **`docs/Makefile`:** The `epubcheck` target depends on `epub` and `epubcheck` is in the `.PHONY` list. Both are correct. The `.bat` version also prints "EPUBCheck complete.", but the Makefile version does not, which is a small inconsistency.

**Potential issues**
- **Hard-coded `Django.epub`:** The Makefile and `.bat` both hard-code `$(BUILDDIR)/epub/Django.epub`. That breaks if `epub_basename` ever changes. A glob or a variable would be more robust.
- **Java dependency:** `epubcheck` on PyPI wraps the Java tool, so contributors need a JRE. The docs say this and exclude it from `make check`, which is good. CI on `ubuntu-24.04` has Java preinstalled, so it should work there.
- **Expected NAV-011 warnings:** The docs say these are expected, but the CI step only fails on errors. I could not tell from the diff whether `epubcheck` exits non-zero on warnings. If it does, CI would fail permanently. The PR description suggests the job was passing apart from the SVG issue (#37456), which was fixed separately.
- **Overlapping builds:** The note about `sphinx-autobuild` interfering with the `.buildinfo.bak` file is helpful.

**Performance:** There is no runtime impact. The CI job adds one epub build plus a Java startup, which is a modest cost.

**Security:** There are no concerns. The change touches only docs, CSS and CI, and `epubcheck` is an unpinned dev dependency used only in docs requirements. Pinning it would be slightly safer for reproducibility, but Django's other docs requirements are unpinned too.

**Tests:** Docs changes don't have unit tests. EPUBCheck in CI acts as the regression check for the epub fixes. The CSS overflow fix has no automated coverage. The PR's UI-screenshot checklist item is unchecked, so a before/after screenshot would have been nice for the CSS change.

**Docs:** The new EPUBCheck section is clear. The `documentation-autobuild` label was added so the section can cross-reference it. The `make check` paragraph correctly notes the exception. The PR's checklist items for tests, docs and release notes are unchecked even though docs were added. That is only a bookkeeping point.

**Verdict:** Good to merge, which it was. The suggestions above are optional follow-ups: the `Sphinx>=7.3.0` floor versus the 9.1 API, the hard-coded epub filename, and the Makefile versus `.bat` message mismatch.
