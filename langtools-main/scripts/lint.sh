#!/bin/bash
set -e

echo "Running FSRS module quality gate checks..."

# Ensure dependencies are installed
echo "0. Installing dependencies..."
uv sync --extra dev

echo "1. Formatting code..."
uv run ruff format .

echo "2. Linting and fixing..."
uv run ruff check . --fix

echo "3. Type checking..."
uv run mypy . --show-error-codes

echo "✅ All quality gate checks passed!"