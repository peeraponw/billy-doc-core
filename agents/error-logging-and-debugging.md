# Error Handling, Logging, and Debugging

## Error Handling

### Fail Fast
Raise early instead of silently recovering.

### Custom Exceptions
Define **domain-specific exception** classes.

### Context Managers for Resources
Use context managers for cleanup guarantees.

## Logging

* Use structured logging when available (`structlog`)
* Use the following logging format

```python
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s",
    level=logging.INFO
)
```

* Wrap processing functions with logging decorators when appropriate

## Monitoring & Observability

* Use structured logging
* Always include context in log entries

## Debugging Tools

Tools allowed:

* ipdb
* memory-profiler
* line-profiler
* rich traceback
