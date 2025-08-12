FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy workspace configuration and dependencies
COPY pyproject.toml uv.lock /workspace-root/
COPY langtools-utils /workspace-root/langtools-utils/
COPY langtools-ai /workspace-root/langtools-ai/
COPY langtools-main /workspace-root/langtools-main/
COPY langtools-mcp /workspace-root/langtools-mcp/

# Set working directory to workspace root for installation
WORKDIR /workspace-root

# Unset VIRTUAL_ENV to prevent conflicts with uv
ENV VIRTUAL_ENV=""
ENV UV_PROJECT_ENVIRONMENT="/tmp/venv"

# Install dependencies
RUN uv sync --frozen

# Set working directory to langtools-mcp for runtime
WORKDIR /workspace-root/langtools-mcp

# Expose port
EXPOSE 8030

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD uv run python -c "import langtools.mcp.server; print('OK')" || exit 1

# Run the MCP server
CMD ["uv", "run", "python", "-m", "langtools.mcp.main"]