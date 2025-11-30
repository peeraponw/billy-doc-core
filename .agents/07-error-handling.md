# 7. Error Handling

## 7.1 Custom Exceptions

* Domain-specific exceptions MUST be defined instead of using bare `Exception`.

```python
class ProjectError(Exception):
    """Base exception for project-level errors."""


class UserNotFoundError(ProjectError):
    """Raised when a user cannot be found."""


class PaymentError(ProjectError):
    """Raised when a payment fails."""
```

## 7.2 No Blanket `except Exception` Without Re-raise

* Blanket `except Exception` MUST NOT swallow errors.
* When catching, code MUST log and either:

  * transform to a domain error, or
  * re-raise.

```python
# ❌ Forbidden: swallow and hide error
try:
    process_payment(data)
except Exception:
    return {"status": "ok"}  # hides real problem


# ✅ Required: log and expose controlled status
try:
    process_payment(data)
except PaymentError as exc:
    logger.warning("Payment failed", extra={"error": str(exc)})
    return {"status": "payment_failed", "error": str(exc)}
```

## 7.3 Fail Fast Logic

* Branches that silently substitute dummy defaults in error conditions MUST NOT be used unless explicitly documented as “graceful degradation” behavior.
