#!/bin/bash

# Build the Docker image
docker build -t claude-code-sandbox .devcontainer/

# Run the container with same configuration as devcontainer
docker run -it --rm \
  --privileged \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  -v "$(pwd):/workspace" \
  -v "$HOME/.claude:/home/node/.claude" \
  -v "claude-code-bashhistory:/commandhistory" \
  -v /Users/egorkolds/.docker/run/docker.sock:/var/run/docker.sock \
  -e "CLAUDE_CONFIG_DIR=/home/node/.claude" \
  -w /workspace \
  --user root \
  claude-code-sandbox \
  /bin/bash -c "
    # Fix Docker socket permissions for node user
    chmod 666 /var/run/docker.sock
    
    # Initialize firewall as root
    /usr/local/bin/init-firewall.sh
    
    # Switch to node user
    su node -c 'cd /workspace && ./scripts/langtools/uv-sync.sh && exec zsh'
  "