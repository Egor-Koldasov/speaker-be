# langtools-utils

Shared utility library for langtools packages.

## Overview

This package provides common utility functions and exception types that are shared across all langtools packages.

## Contents

- Common exception types for consistent error handling
- Utility functions for common operations
- Shared configuration and constants

## Development

This package uses the same development workflow as other langtools packages:

```bash
# Install dependencies
uv sync --extra dev

# Run quality checks
./scripts/lint.sh

# Run tests
./scripts/test.sh
```