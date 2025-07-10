# Language Learning Tools - Hobby Projects

A monorepo for various hobby experimentation projects related to language learning and AI.

## Quick Start

**Option 1: Automated Setup (Recommended)**
```bash
./setup_env.sh
# Edit .env file with your API keys
source venv/bin/activate
```

**Option 2: Manual Setup**
1. **Set up environment variables** (required for AI functionality):
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install packages**:
   ```bash
   pip install -e "./langtools-ai[dev]"
   pip install -e "./langtools-mcp[dev]"
   ```

## Current Packages

- **langtools-ai/** - AI functions for language learning using LangChain
- **langtools-mcp/** - MCP server exposing langtools-ai via Model Context Protocol

## Environment Setup

Copy `.env.example` to `.env` and configure with your API keys:
- `ANTHROPIC_API_KEY` - For Claude models (recommended)
- `OPENAI_API_KEY` - For GPT models

At least one API key is required for functionality.
