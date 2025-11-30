# Testing Strategy (TDD)

* Write test → watch fail → implement minimal code → refactor
* Minimum **80% coverage**
* Tests must be co-located in a `tests/` folder next to the code they test
* Mock external dependencies
* Never skip tests
* Use descriptive test names
* Use fixtures for setup

## Example Testing Best Practices

```python
# Always use pytest fixtures for setup
import pytest
from datetime import datetime

@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return User(
        id=123,
        name="Test User",
        email="test@example.com",
        created_at=datetime.now()
    )

# Use descriptive test names
def test_user_can_update_email_when_valid(sample_user):
    """Test that users can update their email with valid input."""
    new_email = "newemail@example.com"
    sample_user.update_email(new_email)
    assert sample_user.email == new_email

# Test edge cases and error conditions
def test_user_update_email_fails_with_invalid_format(sample_user):
    """Test that invalid email formats are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        sample_user.update_email("not-an-email")
    assert "Invalid email format" in str(exc_info.value)
```
