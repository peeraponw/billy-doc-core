# 9. Testing Strategy

## 9.1 Coverage and Requirements

* Minimum test coverage MUST be **80%**.
* New code MUST NOT be merged if it reduces coverage below 80%.

## 9.2 TDD Preference

* Tests SHOULD be written before implementation, especially for core business logic.
* At minimum, tests MUST be added with new features or bug fixes.

## 9.3 Test Layout

* Tests MUST be co-located with the code they test, inside `tests/` directories as shown in the architecture section.
* `conftest.py` MUST be used for shared fixtures.

```python
# src/project/features/user_management/tests/test_handlers.py
def test_user_can_update_email(user_factory) -> None:
    user = user_factory(email="old@example.com")
    update_user_email(user, "new@example.com")
    assert user.email == "new@example.com"
```

## 9.4 Test Rules

* `pytest` MUST be used.
* `unittest` style MUST NOT be introduced for new tests.
* Tests MUST NOT rely on external services; external dependencies MUST be mocked.
