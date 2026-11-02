# PR diff (the real change)

```diff
diff --git a/django/db/models/sql/query.py b/django/db/models/sql/query.py
index d0acb43965b8..b5ba45a7dfdd 100644
--- a/django/db/models/sql/query.py
+++ b/django/db/models/sql/query.py
@@ -1621,47 +1621,47 @@ def build_filter(
         lookup_type = condition.lookup_name
         clause = WhereNode([condition], connector=AND)
 
-        require_outer = (
-            lookup_type == "isnull" and condition.rhs is True and not current_negated
-        )
-        if (
-            current_negated
-            and (lookup_type != "isnull" or condition.rhs is False)
-            and condition.rhs is not None
-        ):
+        require_outer = False
+        if lookup_type == "isnull":
+            # Both `NOT (field IS NOT NULL)` and `field IS NULL` require an
+            # OUTER JOIN to effectively include related `NULL` values.
+            # Otherwise an INNER JOIN can be used as it excludes them.
+            require_outer = (
+                condition.rhs is False if current_negated else condition.rhs is True
+            )
+        elif current_negated and condition.rhs is not None:
             require_outer = True
-            if lookup_type != "isnull":
-                # The condition added here will be SQL like this:
-                # NOT (col IS NOT NULL), where the first NOT is added in
-                # upper layers of code. The reason for addition is that if col
-                # is null, then col != someval will result in SQL "unknown"
-                # which isn't the same as in Python. The Python None handling
-                # is wanted, and it can be gotten by
-                # (col IS NULL OR col != someval)
-                #   <=>
-                # NOT (col IS NOT NULL AND col = someval).
+            # The condition added below will be SQL like this:
+            # `NOT (col IS NOT NULL)`, where the first NOT is added in
+            # upper layers of code. The reason for addition is that if col
+            # `IS NULL`, then `col != someval` will result in SQL "unknown"
+            # which isn't the same as in Python. The Python None handling
+            # is wanted, and it can be achieved by
+            # `(col != someval OR col IS NULL)` which is equivalent to
+            # `NOT (col = someval AND col IS NOT NULL)`. The second form is
+            # required here as the condition is negated per `current_negated`.
+            if (
+                self.is_nullable(targets[0])
+                or self.alias_map[join_list[-1]].join_type == LOUTER
+            ):
+                lookup_class = targets[0].get_lookup("isnull")
+                col = self._get_col(targets[0], join_info.targets[0], alias)
+                # Use OR + IS NULL when RHS `in` values include None.
                 if (
-                    self.is_nullable(targets[0])
-                    or self.alias_map[join_list[-1]].join_type == LOUTER
+                    lookup_type == "in"
+                    # Check containers (not strings or bytes).
+                    and isinstance(condition.rhs, Iterable)
+                    and not isinstance(condition.rhs, (str, bytes))
+                    and any(v is None for v in condition.rhs)
                 ):
-                    lookup_class = targets[0].get_lookup("isnull")
-                    col = self._get_col(targets[0], join_info.targets[0], alias)
-                    # Use OR + IS NULL when RHS `in` values include None.
-                    if (
-                        lookup_type == "in"
-                        # Check containers (not strings or bytes).
-                        and isinstance(condition.rhs, Iterable)
-                        and not isinstance(condition.rhs, (str, bytes))
-                        and any(v is None for v in condition.rhs)
-                    ):
-                        clause.add(lookup_class(col, True), OR)
-                    else:
-                        clause.add(lookup_class(col, False), AND)
-                # If someval is a nullable column, someval IS NOT NULL is
-                # added.
-                if isinstance(value, Col) and self.is_nullable(value.target):
-                    lookup_class = value.target.get_lookup("isnull")
-                    clause.add(lookup_class(value, False), AND)
+                    clause.add(lookup_class(col, True), OR)
+                else:
+                    clause.add(lookup_class(col, False), AND)
+            # If someval is a nullable column, someval IS NOT NULL is
+            # added.
+            if isinstance(value, Col) and self.is_nullable(value.target):
+                lookup_class = value.target.get_lookup("isnull")
+                clause.add(lookup_class(value, False), AND)
         return clause, used_joins if not require_outer else ()
 
     def add_filter(self, filter_lhs, filter_rhs):

```

# REVIEW A

## Review of PR #22041: Simplified NULL handling in `sql.Query.build_filter()`

This PR is already merged. I found no blocking issues. I couldn't load the repository's CLAUDE.md (none exists in the working tree), so I judged style against Django's usual conventions.

### Correctness
I checked the refactor against the old logic case by case, and the behaviour is equivalent.

| Case | Old `require_outer` | New `require_outer` |
|---|---|---|
| `isnull`, not negated | `rhs is True` | `rhs is True` |
| `isnull`, negated | `True` only if `rhs is False` (the `rhs is not None` check always passes for a bool) | `rhs is False` |
| Other lookup, negated, `rhs is not None` | `True`, and the `IS NOT NULL` clause is added | same |
| Other lookup, not negated | `False` | `False` |

The `elif current_negated and condition.rhs is not None` branch now covers only non-`isnull` lookups. That makes the old `if lookup_type != "isnull":` guard redundant, so removing it and de-indenting the block is safe. The `Col`/`is_nullable(value.target)` clause and the `in`-with-`None` handling are unchanged. The only difference is the lower indentation.

### Code quality
- **Structure:** Branching on `lookup_type` first is easier to read than the old compound boolean. It also sets up the follow-up work for `__in=[None]` (#22040) and the `Expression`-flags idea (#16817).
- **`isnull` comment:** The new comment explains why an OUTER JOIN is needed. It is a clear improvement over having no explanation.
- **Negation comment:** The comment now says `NOT (col = someval AND col IS NOT NULL)` and gives the reason for the second form. That is more precise than before.
- **Nit:** The block comment says "The condition added below will be SQL like this: `NOT (col IS NOT NULL)`". The actual clause is `NOT (col IS NOT NULL AND col = someval)`, with the first `NOT` added by callers. The comment's second half does explain this, but the first line could be reworded.
- **Nit:** `require_outer = True` sits above a long comment that mostly describes the nullable-column clause below it. Moving the assignment next to the comment, or splitting the comment, would make the link clearer.
- **Nit:** The nested conditions (`is_nullable or LOUTER`, then the `in`/`None` check) are still deep. You could pull the `in`-contains-`None` test into a small local variable. That fits the planned follow-up and isn't needed here.

### Performance
There is no change. The same checks run, and the `any(...)` scan over `in` values is unchanged.

### Security
I see no concerns. The change only reorganises SQL generation and doesn't alter what gets parameterised.

### Test coverage
The PR adds no tests, which is appropriate for a behaviour-preserving refactor. The existing suites (`queries`, `lookup`, `null_queries`, `null_fk`, `or_lookups`) should exercise all four branches. I'd want to confirm those passed in CI, particularly negated `exclude()` across nullable FKs, `exclude(x__in=[None, ...])`, and `exclude(f=F("nullable"))`. #22040 should add explicit tests for `__in=[None]`.

**Verdict:** a clean, behaviour-preserving refactor, with only comment nits to consider.

# REVIEW B

# Review of django/django#22041: Simplified NULL handling in `sql.Query.build_filter()`

**Verdict: approve.** This is a behavior-preserving refactor. I found no bugs.

I did not run the test suite. I checked equivalence by reading the diff.

## Equivalence check

The old `require_outer` logic reduces to the following:

| Case | Old | New |
|---|---|---|
| `isnull`, not negated | `rhs is True` | `rhs is True` |
| `isnull`, negated | `rhs is False` (the old `rhs is not None` is implied) | `rhs is False` |
| other lookup, negated | `rhs is not None` | `rhs is not None` |
| other lookup, not negated | `False` | `False` |

The nested block that adds `col IS NOT NULL`, the `OR col IS NULL` for `__in` containing `None`, and the `value.target` nullable-column check was only reachable for non-`isnull` lookups in the old code. In the new code it sits in the `elif`, so it is reachable only for non-`isnull` lookups. The change also dedents that block by one level.

## Code quality

- The refactor removes the redundant `lookup_type != "isnull"` checks that were repeated at two levels. Branching on `isnull` first makes the intent clear.
- The new comment on the `isnull` branch is a good addition. The expression `condition.rhs is False if current_negated else condition.rhs is True` is compact and readable.
- Minor: in the rewritten comment, `NOT (col IS NOT NULL)` is described as the condition added below. The code actually adds `col IS NOT NULL` (or `col IS NULL` with `OR`), and the outer `NOT` is applied elsewhere. The comment says this, but the first sentence could be misread. Saying "`col IS NOT NULL` is added below, and the upper layers wrap the whole clause in `NOT`" would be clearer.
- Minor: the new `elif` branch sets `require_outer = True` before a long comment and nested conditionals. That's fine, but moving the comment above the `if` that uses it would keep the assignment next to its explanation.
- The remaining `condition.rhs is not None` check in the `elif` looks like it could be confusing next to the `isnull` branch. It's unchanged behavior, so it's out of scope here.

## Performance and security

- Performance: there is no meaningful change. The same checks run, in a slightly different order.
- Security: there is no impact. The generated SQL is unchanged.

## Tests

No tests were added or changed. That's appropriate for a pure refactor, since the existing `queries`, `lookup`, `null_queries` and `null_fk` suites exercise these paths. It would be worth confirming that the full `queries` and `lookup` suites ran in CI. They cover the negated `isnull`, `__in=[None]` and `F()` nullable-column cases that this code touches.

## Process notes

The PR follows the repository conventions: the ticket reference is in the title, the commit message is in past tense and ends with a period, and the AI disclosure is filled in. The stated motivation is to prepare for the `__in=[None]` fix in #22040 and the `Expression` flags work in #16817. That is a reasonable justification for splitting this out as its own commit.
