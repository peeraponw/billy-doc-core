# Imports, Constants, and Dependency Injection

## Import Rules

### Never use relative imports
Relative imports complicate refactoring and break under certain tooling.

```python
# ❌ Do not use
from ..module.sub import Thing

# ✅ Always use absolute imports
from project.module.sub import Thing
```

## Constants and Magic Strings

### Avoid magic strings and numbers
All constants must be declared in a dedicated module:

```
src/project/consts.py
```

Example:

```python
# consts.py
DEFAULT_TIMEOUT_SECONDS = 30
EVENT_CREATED = "event_created"
```

## Dependency Injection

Use dependency injection for any **complex component**, such as:

* database connections
* repositories
* external API clients
* background job runners
* configuration providers

This improves testability and decoupling.

Example:

```python
def process_user(user_id: int, repo: UserRepository) -> User:
    return repo.fetch(user_id)
```
