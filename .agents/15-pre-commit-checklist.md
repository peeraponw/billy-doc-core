# 15. Pre-Commit Checklist

Before committing, ALL of the following MUST be true:

* [ ] `uv sync` has been run and `pyproject.toml` / lockfile are up to date
* [ ] `uv run ruff format .` has been run (and/or `ruff format --check` passes)
* [ ] `uv run ruff check .` passes with no errors
* [ ] `uv run pyright src/` passes with no errors
* [ ] `uv run pytest` passes
* [ ] Coverage is ≥80% and new code is covered
* [ ] No `print` statements in production code
* [ ] No relative imports
* [ ] No magic strings where constants exist
* [ ] No secrets added to the repository
* [ ] New public functions/classes have docstrings
* [ ] New external data flows use validation (Pydantic or equivalent)

---

This checklist is mandatory for every change.
