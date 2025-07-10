# Multi-stage build for optimal image size
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy langtools-ai dependency first  
COPY langtools-ai/ ./langtools-ai/

# Copy our package files
COPY langtools-mcp/pyproject.toml ./
COPY langtools-mcp/README.md ./
COPY langtools-mcp/src/ ./src/

# Install langtools-ai first, then our package
RUN cd langtools-ai && pip install --no-cache-dir -e . && cd ..
RUN pip install --no-cache-dir -e .

# Production stage - minimal runtime image
FROM python:3.10-slim as runtime

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r langtools && useradd -r -g langtools langtools

# Set work directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code for both packages
COPY --from=builder /app/src ./src
COPY --from=builder /app/langtools-ai/src ./langtools-ai-src

# Switch to non-root user for security
USER langtools

# Set Python path to find our packages
ENV PYTHONPATH=/app/src:/app/langtools-ai-src
ENV PYTHONUNBUFFERED=1

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import langtools.mcp.server; print('OK')" || exit 1

# Default command - run the MCP server
CMD ["python", "-m", "langtools.mcp.main"]

# Metadata
LABEL org.opencontainers.image.title="langtools-mcp"
LABEL org.opencontainers.image.description="MCP server for language learning tools"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.authors="langtools"