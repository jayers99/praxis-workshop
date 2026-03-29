# List available recipes
[default]
list:
    @just --list

# Install/sync dependencies
sync:
    uv sync

# Run tests
test *args:
    uv run pytest {{args}}

# Lint code
lint:
    uv run ruff check .

# Format code
format:
    uv run ruff format .
    uv run ruff check --fix .

# Type check
typecheck:
    uv run mypy .

# Run all checks (lint, typecheck, test)
check: lint typecheck test

# Clean build artifacts
clean:
    rm -rf .pytest_cache .mypy_cache .ruff_cache
    rm -rf dist build *.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
