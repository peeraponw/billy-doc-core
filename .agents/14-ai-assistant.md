# 14. AI Assistant Rules

The AI assistant MUST:

* Obey all rules in this document.
* Inspect existing modules and patterns before generating new code.
* Prefer extending existing functions, classes, and patterns over introducing parallel ones.
* Always add or update tests when adding or changing behavior.
* Avoid new dependencies if equivalent functionality exists in the project or standard library.

The AI assistant MUST NOT:

* Introduce relative imports.
* Use `from typing import TYPE_CHECKING`.
* Add magic strings instead of using constants.
* Add uncovered (untested) critical-path code.
* Reduce type or linting strictness.
