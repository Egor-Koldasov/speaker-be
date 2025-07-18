#!/bin/bash

# Build the Docker image
docker build -t claude-code-sandbox .devcontainer/

# Run the container with same configuration as devcontainer
docker run -it --rm \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v "$(pwd):/workspace" \
  -v "$HOME/.claude:/home/node/.claude" \
  -v "claude-code-bashhistory:/commandhistory" \
  -e "CLAUDE_CONFIG_DIR=/home/node/.claude" \
  -w /workspace \
  --user node \
  claude-code-sandbox \
  /bin/bash -c "sudo /usr/local/bin/init-firewall.sh && ./scripts/langtools/uv-sync.sh && exec zsh"