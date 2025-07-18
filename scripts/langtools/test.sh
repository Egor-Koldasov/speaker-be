#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if any test fails
FAILED=0

# Function to run tests for a package
run_tests() {
    local package=$1
    echo -e "${YELLOW}Running tests for $package...${NC}"
    
    if [ -d "$package" ]; then
        if (cd "$package" && uv run pytest -v); then
            echo -e "${GREEN}✓ $package tests passed${NC}"
        else
            echo -e "${RED}✗ $package tests failed${NC}"
            FAILED=1
        fi
    else
        echo -e "${RED}✗ $package directory not found${NC}"
        FAILED=1
    fi
    echo
}

# Run tests for all packages
echo -e "${YELLOW}Running tests for all langtools packages...${NC}"
echo

# Run tests in dependency order
run_tests "langtools-utils"
run_tests "langtools-ai"
run_tests "langtools-main"
run_tests "langtools-mcp"

# Summary
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}One or more test suites failed!${NC}"
    exit 1
fi