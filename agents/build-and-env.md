# Build & Environment

## Build & Packaging Standards

### Use Hatchling (Required)
This project uses **hatchling** for builds.

`pyproject.toml` example:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Development Environment

### UV Package Management (Required)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
uv sync

uv add requests
uv add --dev pytest ruff pyright
uv remove requests

uv run python script.py
uv run pytest
uv run ruff check .
uv python install 3.13
```

### Development Commands (TDD Workflow)

```bash
uv run pytest
uv run pytest tests/test_module.py -v
uv run pytest --cov=src --cov-report=html

uv run ruff format .
uv run ruff check .
uv run ruff check --fix .

uv run pyright src/
uv run pre-commit run --all-files
```
