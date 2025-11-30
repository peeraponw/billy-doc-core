# 3. Tooling, Packaging, and Environment

## 3.1 Build System — Hatchling (Required)

`pyproject.toml` MUST use `hatchling`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 3.2 Environment and Dependency Management — uv (Required)

* uv MUST be used for environments and dependencies.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

uv venv
uv sync

uv add fastapi pydantic
uv add --dev pytest ruff pyright
uv remove some-package
```

* Dependencies MUST NOT be edited manually in `pyproject.toml`; use `uv add` / `uv remove`.

## 3.3 Code Quality Tools

The following tools are mandatory:

* Formatting: `ruff format`
* Linting: `ruff check`
* Type checking: `pyright`
* Testing: `pytest`
* Coverage: `pytest --cov=src --cov-report=html`

Example commands:

```bash
uv run ruff format .
uv run ruff check .
uv run pyright src/
uv run pytest
uv run pytest --cov=src --cov-report=html
```
