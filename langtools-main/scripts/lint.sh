#!/bin/bash
set -e

echo "Running FSRS module quality gate checks..."

# Ensure dependencies are installed
echo "0. Installing dependencies..."
uv sync --extra dev

echo "1. Formatting code..."
uv run ruff format src/ tests/

echo "2. Linting and fixing..."
uv run ruff check src/ tests/ --fix

echo "3. Type checking..."
uv run mypy src/ --show-error-codes

echo "✅ All quality gate checks passed!"