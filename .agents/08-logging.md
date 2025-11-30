# 8. Logging and Observability

## 8.1 Logging

* Structured logging MUST be used (e.g. `structlog` or structured `logging`).
* Log MUST use the following: `format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s"`
* `print` MUST NOT be used for logging in production code.

```python
import logging

logger = logging.getLogger(__name__)


def process_user(user_id: str) -> None:
    logger.info("Processing user", extra={"user_id": user_id})
```

## 8.2 Error Logging

* All errors that reach top-level handlers (API endpoints, CLI commands, background workers) MUST be logged with error level and include relevant context (but no secrets).
