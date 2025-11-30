# 1. Core Development Philosophy

## 1.1 KISS and YAGNI

- Code MUST use the simplest correct solution that satisfies requirements.
- Abstractions MUST be introduced only when they remove real duplication or complexity.
- Speculative features, unused extension points, or “maybe future” parameters MUST NOT be added.

```python
# ❌ Forbidden: speculative abstraction
def process_items(items, strategy: Callable | None = None) -> None:
    ...

# ✅ Required: implement only what is needed now
def process_items(items: Sequence[Item]) -> None:
    ...
```

## 1.2 Fail Fast

* Code MUST detect invalid state early and raise explicit exceptions.
* Silent fallbacks and dummy defaults MUST NOT be used unless explicitly documented for a specific use case.

```python
# ❌ Forbidden: hides real error behind magic fallback
def parse_count(raw: str) -> int:
    try:
        return int(raw)
    except ValueError:
        return 0  # silently wrong


# ✅ Required: fail fast with explicit error
def parse_count(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"Invalid count {raw!r}") from exc
```

## 1.3 No Guessing

* Code MUST NOT guess at types, formats, or paths.
* All external input MUST be validated.
* AI-assisted code MUST NOT invent paths or modules that do not exist.
