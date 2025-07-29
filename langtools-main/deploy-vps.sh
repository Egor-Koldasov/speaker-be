#!/bin/bash
# Deployment script for vps1.egor-koldasov.dev

set -e

echo "🚀 Deploying to vps1.egor-koldasov.dev..."

# Load VPS environment
export $(grep -v '^#' .env.vps | xargs)

echo "📋 Environment loaded:"
echo "  HYDRA_PUBLIC_URL: $HYDRA_PUBLIC_URL"
echo "  LOGIN_UI_URL: $LOGIN_UI_URL"
echo "  ENVIRONMENT: $ENVIRONMENT"

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose down || true

# Pull latest images
echo "📦 Pulling latest images..."
docker compose pull

# Build API image
echo "🔨 Building API image..."
docker compose build api

# Start services
echo "🟢 Starting services..."
docker compose --env-file .env.vps up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker compose ps

# Test Hydra health
echo "🩺 Testing Hydra health..."
curl -f http://localhost:4444/health/ready || echo "⚠️ Hydra not ready yet"

# Test API health
echo "🩺 Testing API health..."
curl -f http://localhost:8000/docs || echo "⚠️ API not ready yet"

echo "✅ Deployment complete!"
echo ""
echo "🌐 Services available at:"
echo "  Hydra Public API: https://vps1.egor-koldasov.dev:4444"
echo "  Langtools API: https://vps1.egor-koldasov.dev:8000"
echo "  API Docs: https://vps1.egor-koldasov.dev:8000/docs"
echo ""
echo "📝 Next steps:"
echo "  1. Set up reverse proxy/SSL certificates"
echo "  2. Create login UI at port 3000"
echo "  3. Register OAuth2 clients"