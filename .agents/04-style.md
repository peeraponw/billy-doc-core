# 4. Python Style and Conventions

## 4.1 PEP 8 with Project-Specific Rules

* Code MUST follow PEP 8.
* Line length MUST be 100 characters.
* Strings MUST use double quotes by default.
* Trailing commas MUST be used in multiline collections and argument lists.
* Type hints MUST be present on all public functions and methods.

```python
def create_user(
    email: str,
    name: str,
    is_admin: bool = False,
) -> User:
    ...
```

## 4.2 Type Hints and `TYPE_CHECKING`

* All public function arguments and return values MUST have type hints.
* Class attributes MUST be annotated.
* `from typing import TYPE_CHECKING` MUST NOT be used. Type issues MUST be solved at their root (correct imports, stubs, or architecture), not hidden behind type-check-only imports.

```python
# ❌ Forbidden
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project.core.models import User


# ✅ Required
from project.core.models import User
```
