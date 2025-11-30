# 2. Architecture & Project Structure

## 2.1 Vertical Slice Architecture — MANDATORY

The project MUST follow a vertical-slice layout, with code and tests co-located by feature:

```text
src/project/
  __init__.py
  main.py

  core/
    __init__.py
    db/
      __init__.py
      connection.py
      models.py
      tests/
        test_connection.py
        test_models.py
    auth/
      __init__.py
      authentication.py
      authorization.py
      tests/
        test_authentication.py
        test_authorization.py

  features/
    user_management/
      __init__.py
      handlers.py
      validators.py
      services.py
      tests/
        test_handlers.py
        test_validators.py
        test_services.py

    payment_processing/
      __init__.py
      processor.py
      gateway.py
      tests/
        test_processor.py
        test_gateway.py

  shared/
    __init__.py
    consts.py
    types.py
    utils/
      __init__.py
      string_utils.py
      date_utils.py
      tests/
        test_string_utils.py
        test_date_utils.py
```

## 2.2 File, Function, and Class Limits

* Files MUST NOT exceed **500 lines**.
* Functions MUST NOT exceed **50 lines**.
* Classes MUST NOT exceed **100 lines**.
* Maximum line length MUST be **100 characters**.

When nearing these limits, code MUST be split into smaller modules, functions, or classes.

## 2.3 Import Rules (No Relative Imports)

* Relative imports (`from ..module import X`) MUST NOT be used.
* All imports MUST be absolute, from the top-level package.

```python
# ❌ Forbidden
from ..shared.utils import string_utils

# ✅ Required
from project.shared.utils import string_utils
```

## 2.4 Constants and “Magic” Values

* Magic strings/numbers MUST NOT be hard-coded in multiple places.
* Shared constants MUST live in `project/shared/consts.py`.

```python
# project/shared/consts.py
DEFAULT_PAGE_SIZE = 50
SYSTEM_USER_NAME = "system"
EVENT_USER_CREATED = "user_created"
```

```python
# ❌ Forbidden: inline magic string
audit.log("user_created", user_id=user.id)

# ✅ Required
from project.shared.consts import EVENT_USER_CREATED

audit.log(EVENT_USER_CREATED, user_id=user.id)
```

## 2.5 Dependency Injection for Complex Components

* Complex components (DB connections, repositories, external API clients, service classes) MUST be provided via dependency injection, not constructed deep inside business logic.

```python
# ❌ Forbidden: hard-coding dependency
def process_user(user_id: UUID) -> None:
    repo = UserRepository(create_db_connection())
    repo.process(user_id)


# ✅ Required: inject dependency
def process_user(user_id: UUID, repo: UserRepositoryProtocol) -> None:
    repo.process(user_id)
```
