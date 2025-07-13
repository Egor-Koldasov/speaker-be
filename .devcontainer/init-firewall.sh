#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, and pipeline failures
IFS=$'\n\t'       # Stricter word splitting

echo "Configuring firewall with unrestricted access..."

# Flush existing rules and delete existing ipsets
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
ipset destroy allowed-domains 2>/dev/null || true

# Set default policies to ACCEPT (unrestricted)
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Allow all established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow localhost
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

echo "Firewall configuration complete - unrestricted access enabled"

# Verify unrestricted access
echo "Verifying internet access..."
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    echo "✓ Internet access verified - able to reach https://example.com"
else
    echo "⚠ Warning: Unable to reach https://example.com - check network connectivity"
fi

# Verify GitHub API access
if curl --connect-timeout 5 https://api.github.com/zen >/dev/null 2>&1; then
    echo "✓ GitHub API access verified"
else
    echo "⚠ Warning: Unable to reach GitHub API - check network connectivity"
fi
