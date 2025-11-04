#!/bin/bash

# ============================================================================
# Food RAG MCP Server - Standalone Server Start Script
# ============================================================================

echo ""
echo "🚀 Starting Food RAG MCP Server (Standalone)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Change to the correct directory
cd "$(dirname "$0")"

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "❌ Error: .env.local file not found!"
    echo ""
    echo "Please create .env.local with:"
    echo "  UPSTASH_VECTOR_REST_URL=your-url"
    echo "  UPSTASH_VECTOR_REST_TOKEN=your-token"
    echo "  GROQ_API_KEY=your-api-key"
    echo ""
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Environment: OK"
echo "✅ Node.js version: $(node --version)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 MONITORING STARTED - Watch for logs below"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the MCP server
node mcp-server.js

# If the server stops, show this message
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "👋 MCP Server stopped"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
