# Architecture & Modularity

## Code Structure & Modularity

### File, Class, and Function Limits
* Files ≤ **500 lines**
* Functions ≤ **50 lines**
* Classes ≤ **100 lines**
* Max line length: **100 characters**
* Organize modules by feature (vertical slices)

## Project Architecture — Vertical Slice Pattern

Use vertical slices where each feature has its own handlers, validators, and tests.

```
src/project/
    __init__.py
    main.py
    tests/
        test_main.py
    conftest.py

    # Core modules
    database/
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

    # Feature slices
    features/
        user_management/
            __init__.py
            handlers.py
            validators.py
            tests/
                test_handlers.py
                test_validators.py

        document_generation/
            __init__.py
            handlers.py
            validators.py
            tests/
                test_handlers.py
                test_validators.py
```
