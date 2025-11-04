#!/bin/bash

# Food RAG MCP Server Startup Script
# Keep this terminal window open while using Claude Desktop

echo "🚀 Starting Food RAG MCP Server..."
echo "📍 Directory: $(pwd)"
echo ""

# Change to correct directory
cd /Users/DELL/ragfood/mydigitaltwin

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "❌ Error: .env.local not found!"
    echo "   Please create .env.local with your API keys"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "✅ Starting Next.js server on http://localhost:3000"
echo ""
echo "⚠️  IMPORTANT: Keep this terminal window open!"
echo "   Closing this window will stop the MCP server."
echo ""
echo "🔌 Claude Desktop should now be able to connect to food-rag-system"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start Next.js dev server
npm run dev
