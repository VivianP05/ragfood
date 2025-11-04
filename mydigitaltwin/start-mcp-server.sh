#!/bin/bash

# Food RAG System - Server Startup Script
# This script starts the Next.js development server properly

echo "🚀 Starting Food RAG MCP Server..."
echo ""

# Navigate to the correct directory
cd /Users/DELL/ragfood/mydigitaltwin

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "❌ Error: .env.local file not found!"
    echo "Please create .env.local with your API keys"
    exit 1
fi

# Check if node_modules exists
if [ ! -d node_modules ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "✅ Starting Next.js development server..."
echo "📍 Server will run at: http://localhost:3000"
echo "🔌 MCP endpoint: http://localhost:3000/api/mcp"
echo ""
echo "⚠️  IMPORTANT: Keep this terminal window open!"
echo "   The server must stay running for Claude Desktop to connect."
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

npm run dev
