# Workflow & Operations

## Important Notes

* Never assume or guess — verify first
* Keep file paths and module names accurate
* Keep AGENTS.md updated when patterns change
* Tests are mandatory for all features
* Avoid subjective or opinion-based statements in documentation
  (This file must remain factual and enforceable.)

## Search Command Requirements

**Always use `rg` (ripgrep).**  
Do not use `grep` or `find` directly.

```bash
# ❌ Do not use
grep -r "pattern" .
find . -name "*.py"

# ✅ Use ripgrep
rg "pattern"
rg --files | rg "\.py$"
rg --files -g "*.py"
```

## Git Workflow

### Branch Naming

* `main` — production
* `dev` — integration branch
* `feat/*` — new features
* `fix/*` — bug fixes
* `docs/*` — documentation
* `refactor/*` — refactoring
* `test/*` — tests only

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Container Build Rules

### Never include tests in the production container

You must maintain both:

* `.dockerignore`
* `.containerignore`

Contents must exclude:

```
**/tests/
**/test_*.py
__pycache__/
.pytest_cache/
.coverage
htmlcov/
*.log
*.tmp
```

## TYPE_CHECKING Restriction

Do **not** use:

```python
from typing import TYPE_CHECKING
```

This masks type-resolution problems instead of addressing root causes.

## Database Naming Standards

* Primary keys: `{entity}_id`
* Foreign keys: `{referenced_entity}_id`
* Timestamps: `{action}_at`
* Booleans: `is_{state}`
* Counts: `{entity}_count`
* Durations: `{property}_{unit}`

Repositories must auto-derive table and column names.

## Useful Resources

* UV: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
* Ruff: [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff)
* Pytest: [https://docs.pytest.org/](https://docs.pytest.org/)
* Pydantic: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
* FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
* PEP 8: [https://pep8.org/](https://pep8.org/)
* PEP 484: [https://www.python.org/dev/peps/pep-0484/](https://www.python.org/dev/peps/pep-0484/)
* Hitchhiker’s Guide: [https://docs.python-guide.org/](https://docs.python-guide.org/)

## Workflow Summary (GitHub Flow)

```
main (protected) ←── PR ←── feat/your-feature
        ↑                      ↓
      deploy                development
```

Daily workflow:

1. `git checkout main && git pull origin main`
2. `git checkout -b feat/new-feature`
3. Implement code + tests
4. `git push origin feat/new-feature`
5. Open PR → Review → Merge
