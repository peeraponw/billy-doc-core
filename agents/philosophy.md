# Philosophy

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)
Prefer the simplest working solution. Reduce cognitive overhead and complexity.

### YAGNI (You Aren’t Gonna Need It)
Implement functionality only when it is actually required.

## Design Principles
- **Dependency Inversion** — High-level modules depend on abstractions.
- **Open/Closed Principle** — Open for extension, closed for modification.
- **Single Responsibility** — One responsibility per function/class/module.
- **Fail Fast** — Detect errors as early as possible and raise immediately. Avoid fallback logic like:

```python
# ❌ Avoid silent defaulting
if is_valid(data):
    result = calculate(data)
else:
    result = 0  # Hidden fallback, masks real error
```

Instead, raise:

```python
# ✅ Fail fast
if not is_valid(data):
    raise ValueError("Invalid data")
```
