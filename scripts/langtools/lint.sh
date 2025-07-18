#!/bin/bash

# Exit on error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if any linter fails
FAILED=0

# Function to run linter for a package
run_linter() {
    local package=$1
    echo -e "${YELLOW}Running linter for $package...${NC}"
    
    if [ -f "$package/scripts/lint.sh" ]; then
        if (cd "$package" && ./scripts/lint.sh); then
            echo -e "${GREEN}✓ $package lint passed${NC}"
        else
            echo -e "${RED}✗ $package lint failed${NC}"
            FAILED=1
        fi
    else
        echo -e "${RED}✗ $package/scripts/lint.sh not found${NC}"
        FAILED=1
    fi
    echo
}

# Run linters for all packages
echo -e "${YELLOW}Running linters for all langtools packages...${NC}"
echo

# Run linters in dependency order
run_linter "langtools-utils"
run_linter "langtools-ai"
run_linter "langtools-main"
run_linter "langtools-mcp"

# Summary
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All linters passed!${NC}"
    exit 0
else
    echo -e "${RED}One or more linters failed!${NC}"
    exit 1
fi