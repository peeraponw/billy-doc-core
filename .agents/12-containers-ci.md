# 12. Containers and CI

## 12.1 `.dockerignore` and `.containerignore`

* Both `.dockerignore` and `.containerignore` MUST exist and MUST exclude tests and development artifacts from production images.

Example:

```text
**/tests/
**/test_*.py
__pycache__/
.pytest_cache/
.coverage
htmlcov/
*.log
*.tmp
.git
```

## 12.2 Container Build Rules

* Images MUST NOT `COPY . .` blindly.
* Only required code, configuration, and assets MUST be copied.

```dockerfile
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN uv sync --no-dev

CMD ["uv", "run", "python", "-m", "project.main"]
```

## 12.3 CI Pipeline

A CI job for Python MUST at least:

1. Install dependencies with `uv sync`.
2. Run `ruff format --check` (or equivalent).
3. Run `ruff check`.
4. Run `pyright`.
5. Run `pytest` with coverage and enforce ≥80%.
