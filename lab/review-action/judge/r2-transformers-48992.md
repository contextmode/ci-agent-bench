# PR diff (the real change)

```diff
diff --git a/src/transformers/__init__.py b/src/transformers/__init__.py
index 113f579c5729..e468751800d2 100755
--- a/src/transformers/__init__.py
+++ b/src/transformers/__init__.py
@@ -20,9 +20,8 @@
 
 __version__ = "5.18.0.dev0"
 
-import importlib
+import re
 import sys
-import types
 from pathlib import Path
 from typing import TYPE_CHECKING
 
@@ -54,7 +53,7 @@
 from .utils import is_torchvision_available as is_torchvision_available
 from .utils import is_vision_available as is_vision_available
 from .utils import logging as logging
-from .utils.import_utils import define_import_structure
+from .utils.import_utils import _LegacyModuleAliasFinder, define_import_structure
 
 
 logger = logging.get_logger(__name__)  # pylint: disable=invalid-name
@@ -808,7 +807,16 @@
     from .utils.quantization_config import VptqConfig as VptqConfig
     from .video_processing_utils import BaseVideoProcessor as BaseVideoProcessor
 else:
+    # Deprecated top-level module paths -> replacements. Declared here so the legacy names are also part of the lazy
+    # import structure, keeping `transformers.tokenization_utils_fast` attribute access working.
+    _LEGACY_MODULE_ALIASES = {
+        "tokenization_utils_fast": "tokenization_utils_tokenizers",
+        "tokenization_utils": "tokenization_utils_sentencepiece",
+        "image_processing_utils_fast": "image_processing_backends",
+    }
     _import_structure = {k: set(v) for k, v in _import_structure.items()}
+    for _alias in _LEGACY_MODULE_ALIASES:
+        _import_structure.setdefault(_alias, set())
 
     import_structure = define_import_structure(Path(__file__).parent / "models", prefix="models")
     import_structure[frozenset({})].update(_import_structure)
@@ -821,54 +829,22 @@
         extra_objects={"__version__": __version__},
     )
 
-    def _create_module_alias(alias: str, target: str) -> None:
-        """
-        Lazily redirect legacy module paths to their replacements without importing heavy deps.
-        """
-        module = types.ModuleType(alias)
-        module.__doc__ = f"Alias module for backward compatibility with `{target}`."
-        # Set __file__ explicitly so that inspect.py's hasattr(module, '__file__') check
-        # never falls through to __getattr__ and triggers a premature (possibly circular) import.
-        module.__file__ = None
-
-        def _get_target():
-            return importlib.import_module(target, __name__)
-
-        module.__getattr__ = lambda name: getattr(_get_target(), name)
-        module.__dir__ = lambda: dir(_get_target())
-
-        sys.modules[alias] = module
-        setattr(sys.modules[__name__], alias.rsplit(".", 1)[-1], module)
-
-    _create_module_alias(f"{__name__}.tokenization_utils_fast", ".tokenization_utils_tokenizers")
-    _create_module_alias(f"{__name__}.tokenization_utils", ".tokenization_utils_sentencepiece")
-    _create_module_alias(f"{__name__}.image_processing_utils_fast", ".image_processing_backends")
-
-    for _proc_file in sorted((Path(__file__).parent / "models").rglob("image_processing_*.py")):
-        _model = _proc_file.parent.name
-        _module = _proc_file.stem
-        _target = f".models.{_model}.{_module}"
-        _create_module_alias(f"{__name__}.models.{_model}.{_module}_fast", _target)
-
-        # Also map XImageProcessorFast -> XImageProcessor for backward compat with old class names.
-        def getattr_factory(target):
-            def _getattr(name):
-                if name.endswith("Fast"):
-                    new_name = name.removesuffix("Fast")
-                    logger.warning_once(
-                        "Accessing `%s` from `%s`. Returning `%s` instead. Behavior may be "
-                        "different and this alias will be removed in future versions.",
-                        name,
-                        target,
-                        new_name,
-                    )
-                    return getattr(importlib.import_module(target, __name__), new_name)
-                # Silently forward non-Fast names to target (transparent alias behavior)
-                return getattr(importlib.import_module(target, __name__), name)
-
-            return _getattr
-
-        sys.modules[f"{__name__}.models.{_model}.{_module}_fast"].__getattr__ = getattr_factory(_target)
+    # Deprecated module paths, served on demand by `_LegacyModuleAliasFinder`. `models/x/image_processing_x_fast.py`
+    # became `models/x/image_processing_x.py` when torchvision became the default backend (PIL: `image_processing_pil_x.py`).
+    _LEGACY_FAST_IMAGE_PROCESSOR_MODULE = re.compile(
+        rf"{re.escape(__name__)}\.models\.(\w+)\.image_processing_(?!pil_)(\w+)_fast"
+    )
+
+    def _resolve_legacy_module_alias(fullname: str) -> str | None:
+        if (match := _LEGACY_FAST_IMAGE_PROCESSOR_MODULE.fullmatch(fullname)) is not None:
+            return f"{__name__}.models.{match[1]}.image_processing_{match[2]}"
+        package, _, name = fullname.rpartition(".")
+        if package == __name__ and name in _LEGACY_MODULE_ALIASES:
+            return f"{__name__}.{_LEGACY_MODULE_ALIASES[name]}"
+        return None
+
+    if not any(isinstance(finder, _LegacyModuleAliasFinder) for finder in sys.meta_path):  # this init can run twice
+        sys.meta_path.append(_LegacyModuleAliasFinder(_resolve_legacy_module_alias))
 
 if not is_torch_available():
     logger.warning_advice(
diff --git a/src/transformers/utils/import_utils.py b/src/transformers/utils/import_utils.py
index 30bcc54f47ad..bd1bcc12591f 100644
--- a/src/transformers/utils/import_utils.py
+++ b/src/transformers/utils/import_utils.py
@@ -16,6 +16,7 @@
 """
 
 import functools
+import importlib.abc
 import importlib.machinery
 import importlib.metadata
 import importlib.util
@@ -2802,6 +2803,38 @@ class OptionalDependencyNotAvailable(BaseException):
     """Internally used error class for signalling an optional dependency was not found."""
 
 
+class _LegacyModuleAliasFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
+    """
+    Serves deprecated module paths as copies of their replacement, created only when actually imported. Nothing is
+    pre-registered in `sys.modules`, so tools that scan it and probe attributes (unittest's `assertWarns`, `pickle`,
+    `inspect`, ...) never trigger imports of optional heavy dependencies.
+    """
+
+    def __init__(self, resolve: Callable[[str], str | None]):
+        self.resolve = resolve  # legacy module name -> replacement module name, `None` if not an alias
+
+    def find_spec(self, fullname, path=None, target=None):
+        replacement = self.resolve(fullname)
+        if replacement is None or importlib.util.find_spec(replacement) is None:
+            return None
+        return importlib.machinery.ModuleSpec(fullname, self, loader_state=replacement)
+
+    def exec_module(self, module):
+        # Import the replacement first: a missing optional dependency fails right here, at the user's import statement.
+        replacement = importlib.import_module(module.__spec__.loader_state)
+        vars(module).update({k: v for k, v in vars(replacement).items() if k == "__all__" or not k.startswith("__")})
+
+        def __getattr__(name):  # `XImageProcessorFast` classes were renamed `XImageProcessor`
+            if name.endswith("ImageProcessorFast") and hasattr(replacement, name[:-4]):
+                logger.warning_once(
+                    f"`{name}` is deprecated, use `{name[:-4]}` from `{replacement.__name__}` instead."
+                )
+                return getattr(replacement, name[:-4])
+            raise AttributeError(f"module {module.__name__!r} has no attribute {name!r}")
+
+        module.__getattr__ = __getattr__
+
+
 def direct_transformers_import(path: str, file="__init__.py") -> ModuleType:
     """Imports transformers directly
 
diff --git a/tests/utils/test_import_utils.py b/tests/utils/test_import_utils.py
index 531ffab5a5c2..a6909fb51680 100644
--- a/tests/utils/test_import_utils.py
+++ b/tests/utils/test_import_utils.py
@@ -3,11 +3,18 @@
 from types import ModuleType
 from unittest.mock import DEFAULT, MagicMock, patch
 
+import pytest
 from packaging.version import parse as parse_version
 from parameterized import parameterized
 
 from transformers import logging
-from transformers.testing_utils import CaptureLogger, LoggingLevel, require_torch, run_test_using_subprocess
+from transformers.testing_utils import (
+    CaptureLogger,
+    LoggingLevel,
+    require_torch,
+    require_torchvision,
+    run_test_using_subprocess,
+)
 from transformers.utils.import_utils import (
     _candidate_distribution_names,
     _is_package_available,
@@ -419,3 +426,62 @@ def run(x):
         return x + 1 if helper(*args) else x - 1
 
     run(torch.zeros(3))  # a graph break inside the helper would raise here
+
+
+@run_test_using_subprocess
+def test_legacy_module_aliases_are_served_on_demand():
+    """
+    Deprecated module paths (`transformers.tokenization_utils_fast`, `transformers.models.x.image_processing_x_fast`,
+    ...) are served by a `sys.meta_path` finder and must not be pre-registered in `sys.modules`: tools that scan
+    `sys.modules` and probe attributes (unittest's `assertWarns`, `pickle`, `inspect`) would otherwise trigger imports
+    of optional heavy dependencies. Regression test for https://github.com/huggingface/transformers/issues/48966.
+    """
+    import unittest
+    import warnings
+
+    import transformers
+    from transformers.utils import import_utils
+
+    finders = [f for f in sys.meta_path if isinstance(f, import_utils._LegacyModuleAliasFinder)]
+    assert len(finders) == 1
+    finder = finders[0]
+    pre_registered = [name for name in sys.modules if finder.resolve(name) is not None]
+    assert pre_registered == [], f"legacy module paths pre-registered in sys.modules: {pre_registered}"
+    assert not any(name.startswith("image_processing_") for name in vars(transformers))
+
+    # Scanning `sys.modules` (what `assertWarns` does on entry) must not import anything.
+    modules_before = len(sys.modules)
+    with unittest.TestCase().assertWarns(UserWarning):
+        warnings.warn("probe", UserWarning)
+    assert len(sys.modules) == modules_before
+
+    # Legacy paths still work, as thin shims over the replacement module.
+    from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
+
+    assert PreTrainedTokenizerFast is transformers.PreTrainedTokenizerFast
+    shim = sys.modules["transformers.tokenization_utils_fast"]
+    assert shim is transformers.tokenization_utils_fast
+    assert shim.__spec__.loader is finder
+    assert "PreTrainedTokenizerFast" in vars(shim)
+    # Module metadata is the shim's own, so attribute probes behave like on any other module.
+    assert getattr(shim, "__warningregistry__", None) is None
+    assert getattr(shim, "does_not_exist", None) is None
+
+    with pytest.raises(ModuleNotFoundError):
+        import transformers.models.aria.image_processing_nope_fast  # noqa: F401
+
+
+@require_torchvision
+def test_legacy_fast_image_processor_module_alias():
+    """`models/x/image_processing_x_fast.py` became `models/x/image_processing_x.py`; the old path is an alias."""
+    import transformers.models.aria.image_processing_aria_fast as legacy_module
+    from transformers.models.aria.image_processing_aria import AriaImageProcessor
+    from transformers.models.aria.image_processing_aria_fast import AriaImageProcessorFast  # legacy class name
+
+    assert AriaImageProcessorFast is AriaImageProcessor
+    assert legacy_module.AriaImageProcessor is AriaImageProcessor
+    assert legacy_module.__all__ == ["AriaImageProcessor"]
+
+    # Only paths that actually existed are aliased.
+    with pytest.raises(ModuleNotFoundError):
+        import transformers.models.aria.image_processing_pil_aria_fast  # noqa: F401

```

# REVIEW A

**Review of PR #48992: Serve legacy module aliases through a `sys.meta_path` finder**

The PR is already merged, with approval from ArthurZucker. The description still says "Draft/agent PR, don't review yet". I read the diff for `__init__.py` and `import_utils.py` and the tail of the tests. The middle of the diff was truncated, so I didn't see all of the test changes. I did not run the code or the tests.

**Summary**

The PR replaces eager registration of fake alias modules in `sys.modules` with a lazy `MetaPathFinder`/`Loader`. The finder resolves three fixed top-level aliases and a regex pattern for `image_processing_*_fast`. This fixes the class of bug where scanning `sys.modules` (`assertWarns`, `pickle`, `inspect`) probed attributes on placeholder modules and triggered imports of heavy optional dependencies. It also removes a filesystem `rglob` at import time. The design is sound and the code is much smaller.

**Strengths**
- Nothing is pre-registered in `sys.modules`, so the import-time cost and the side effects are gone.
- `exec_module` imports the replacement first, so a missing optional dependency fails at the user's `import` line.
- The `any(isinstance(...))` guard prevents duplicate finders when `__init__` runs twice.
- The tests cover the main behaviours: no imports triggered by scanning `sys.modules`, identity of the shim, `ModuleNotFoundError` for paths that never existed, and `AriaImageProcessorFast is AriaImageProcessor`.

**Issues and suggestions**

1. **Snapshot copy instead of a live alias (`import_utils.py`, `exec_module`).**
   - `vars(module).update(...)` copies the replacement's namespace once. The old code forwarded through `__getattr__` on every access.
   - Later changes to the replacement are not seen. Examples are monkeypatching `transformers.tokenization_utils_tokenizers.X` in tests, and attributes added after a lazy or circular import finishes.
   - Private names such as `_foo` are copied, but dunder names are dropped. `from legacy import *` is governed by `__all__`.
   - If the replacement is partially initialised (a circular import), the copy would be incomplete.
   - Consider a module-level `__getattr__` fallback to the replacement, or set `module.__dict__` lookups to delegate. At minimum, document the snapshot semantics.

2. **Deprecation warnings were dropped for legacy paths.** The `Fast`-suffix class warning is kept. Importing the deprecated module path itself still gives no warning, as before. Consider a `warnings.warn` or `logger.warning_once` in `exec_module` to steer users off the old paths.

3. **Cost of `find_spec` on every failed import (`find_spec`).**
   - The finder is appended to the end of `sys.meta_path`, so it only runs after the other finders fail. Normal imports are unaffected.
   - `importlib.util.find_spec(replacement)` imports the parent package (`transformers.models.x`). That is usually fine. The regex only matches names ending in `_fast`, so the cost stays limited.
   - `find_spec` and `resolve` are called for every unresolved import in the process, not just `transformers.*`. The regex `fullmatch` is cheap. A prefix check (`fullname.startswith("transformers.")`) first would be a trivial short-circuit.

4. **Regex edge cases (`__init__.py`).**
   - `(\w+)_fast` is greedy, and `(?!pil_)` only checks the prefix. The pattern is correct for the current tree. A model whose own name begins with `pil_` would be wrongly excluded, which is unlikely.
   - `find_spec` returning `None` for non-existent replacements is what makes `image_processing_pil_aria_fast` raise, and the test relies on that. The "only paths that existed" comment is slightly overstated, because any `x_fast` whose non-fast module exists now resolves. That includes ones that never existed under the old name. This is probably harmless.

5. **Lazy-structure hack (`__init__.py`).** `_import_structure.setdefault(_alias, set())` adds empty entries so that `transformers.tokenization_utils_fast` works as an attribute. This relies on the lazy module's behaviour for submodule names. It is worth a test that `transformers.tokenization_utils_fast` works with no prior import. The new tests appear to cover this through `shim is transformers.tokenization_utils_fast`.

6. **Minor.**
   - `__getattr__` in `exec_module` closes over `replacement`. It is fine, but it also won't forward arbitrary missing attributes, which relates to point 1.
   - `_LegacyModuleAliasFinder` has no `create_module`. The default behaviour works on Python 3.4+ for `Loader`, but returning `None` explicitly would be clearer.
   - `find_spec` has no type hints, unlike the `resolve` argument.
   - The PR description is empty beyond the draft note. For a refactor this size, a short description of behaviour changes (snapshot semantics, no pre-registration) would help.

**Security:** There are no new concerns. The finder only resolves a fixed set of names under `transformers.` to other `transformers` modules.

**Tests:** Coverage is good for the main paths. I would add tests for two cases:
- Monkeypatching on the replacement module, to pin down the snapshot behaviour in point 1.
- Importing a legacy alias twice or from multiple threads.

**Verdict:** Good direction and a net simplification. The main thing to look at afterwards is the snapshot-versus-live-alias semantics (point 1), since that is a quiet behaviour change from the old forwarding implementation.

# REVIEW B

**Review of #48992: serve legacy module aliases through a `sys.meta_path` finder**

The PR is already merged and approved. I read the diff only and did not run the tests. The approach is sound. Registering nothing in `sys.modules` fixes the `assertWarns`, `pickle` and `inspect` probing problem from #48966, and it removes the import-time loop over every `image_processing_*.py` file. I found a few things to fix or tighten.

**Potential bugs and behavior changes**

1. **The alias is a snapshot copy, not a live alias.** `exec_module` copies `vars(replacement)` into the shim once.
   - The shim and the replacement are different module objects.
   - `mock.patch("transformers.tokenization_utils_fast.X")` patches only the shim, not the real module.
   - Attributes defined after the copy, or set later by lazy loading, won't show up on the shim.
   - Copying `vars()` of a `_LazyModule` only captures what has already been resolved. Names still resolved lazily through the replacement's `__getattr__` would be missing from the shim, and the shim's `__getattr__` only handles the `ImageProcessorFast` case. This matters for the top-level aliases `tokenization_utils`, `tokenization_utils_fast` and `image_processing_utils_fast`, if their replacements are lazy.
   - The old code forwarded every unknown attribute to the target. A fallback like `return getattr(replacement, name)` before raising would keep that behavior. The tests only check `PreTrainedTokenizerFast`.
   - Whether `import transformers.tokenization_utils_fast as m; m.X` still works for every name that worked before is worth confirming.

2. **`__getattr__` check ordering.** In the shim's `__getattr__`, `hasattr(replacement, name[:-4])` runs before the deprecation warning. That order is fine. The warning text, though, no longer says the alias "will be removed in future versions." That is a small loss of information.

3. **Regex scope.** `(\w+)\.image_processing_(?!pil_)(\w+)_fast` with `fullmatch` is correct. `find_spec` returns `None` when the replacement doesn't exist, so bogus names raise `ModuleNotFoundError`. One edge case: a model whose real module is literally named `image_processing_foo_fast` would be shadowed. The normal import system runs earlier in `sys.meta_path` and finds the real module first, so it isn't actually shadowed.

4. **`find_spec` cost.** `importlib.util.find_spec(replacement)` for a dotted name imports the parent packages. That is fine here. A bad `models.<x>` segment raises `ModuleNotFoundError` from the parent import instead of returning `None`. The result is still a `ModuleNotFoundError` for the user, but with a less direct message.

5. **Finder placement and re-init.** The finder is appended to the end of `sys.meta_path`, which is correct, since the real modules win. The `any(isinstance(...))` guard against double init is good. If `transformers` is reloaded, the guard keeps the old finder, whose `resolve` closure points at the old module's globals. That is harmless but stale.

6. **`_import_structure.setdefault(_alias, set())`.** This makes `transformers.tokenization_utils_fast` resolve through `_LazyModule.__getattr__`, which presumably calls `importlib.import_module`, and the finder then serves it. Check that `from transformers import tokenization_utils_fast` works, because `_LazyModule` may treat the name as a submodule listed in `_import_structure`. The test covers `transformers.tokenization_utils_fast` by attribute access, so this is partly exercised.

**Code quality**

- `_LegacyModuleAliasFinder` implements both `MetaPathFinder` and `Loader`. The loader doesn't define `create_module`, so Python's default module creation is used. Defining it to return `None` explicitly would make that intent clear and avoids deprecation warnings on older Pythons.
- Copying only non-dunder names plus `__all__` is reasonable, since it keeps the shim's own `__name__`, `__spec__` and `__file__`.
- The comment on `_LEGACY_FAST_IMAGE_PROCESSOR_MODULE` is helpful. The `_LEGACY_MODULE_ALIASES` dict in `__init__` and the regex resolver are split across two places. Putting the resolver next to the dict would be easier to follow.
- `_proc_file` and `_module` loop variables are gone, so there is no module namespace pollution. The leftover `_alias` loop variable does leak into the `transformers` namespace. It is a minor point, and `del _alias` would fix it.
- The PR is labelled "Draft/agent PR right now, don't review yet!" in its description, but it is merged and approved. That note should be updated.

**Performance**

This is a clear win. Import time no longer includes a recursive glob of the models directory and the creation of hundreds of module objects. The per-import cost is a regex match on each failed import lookup that reaches the end of `sys.meta_path`. That cost is negligible.

**Security**

There are no concerns. The finder resolves only names that match a fixed regex or a fixed dictionary, and it imports only modules inside `transformers`.

**Tests**

Coverage is good:
- On-demand registration, using a subprocess for isolation.
- Absence of pre-registration.
- A `sys.modules` scan with `assertWarns`.
- The shim's own metadata.
- A negative case.
- Legacy class-name mapping and `__all__`.

Gaps:
- There is no test of the deprecation warning for `XImageProcessorFast`.
- There is no test for the `image_processing_utils_fast` and `tokenization_utils` aliases.
- There is no test of `pickle` or `inspect` on the shim, even though the docstring names them.
- There is no test of `mock.patch` or attribute-forwarding semantics (point 1).
- `test_legacy_fast_image_processor_module_alias` uses `require_torchvision`, so it won't run in CI environments without torchvision. The finder logic itself isn't torchvision-specific, so a test with a stub would run everywhere.

**Summary:** This is a good change. The main follow-up is the snapshot-copy semantics (point 1). I'd add an attribute fallback to the replacement module, or document that shims are static, and add tests for the other aliases and the warning.
