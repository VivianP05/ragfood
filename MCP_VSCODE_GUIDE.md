# VS Code Insiders MCP Integration Guide

## 🚀 Your MCP Server is Already Running!

**Status:** ✅ Server running on port 3000 (PIDs: 753, 93478)

## 📋 How to Use MCP in VS Code Insiders

### Method 1: Command Palette (Easiest)

1. **Open Command Palette**: `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows)

2. **Type**: `MCP` to see MCP-related commands

3. **Available Commands**:
   - `MCP: Restart Server` - Restart the MCP server
   - `MCP: Stop Server` - Stop the MCP server
   - `MCP: View Logs` - View server output
   - `MCP: List Tools` - See available MCP tools

### Method 2: Terminal Commands

Since your server is already running, you can manage it via terminal:

```bash
# Check server status
lsof -ti:3000

# Test MCP endpoint
curl http://localhost:3000/api/mcp

# Test a query
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "query_food_database",
      "arguments": {"question": "Tell me about Sushi"}
    }
  }' | jq -r '.result.content[0].text'
```

### Method 3: Output Panel Monitoring

1. **Open Output Panel**: `Cmd+Shift+U` or **View → Output**
2. **Select Dropdown**: Choose "MCP: food-rag-system" (if available)
3. **View Logs**: Real-time server activity

### Method 4: Integrated Terminal

1. **Open Terminal**: ``Ctrl+` `` or **Terminal → New Terminal**
2. **Navigate to project**:
   ```bash
   cd /Users/DELL/ragfood/mydigitaltwin
   ```
3. **Start server manually**:
   ```bash
   npm run dev
   ```

## 🔧 Current MCP Configuration

**File**: `.vscode/mcp.json`

```json
{
  "food-rag-system": {
    "command": "npm",
    "args": ["run", "dev"],
    "cwd": "${workspaceFolder}/mydigitaltwin",
    "env": {
      "NODE_ENV": "development"
    },
    "description": "Food RAG System MCP Server - Query food database with AI"
  }
}
```

## ✅ Available MCP Tools

Your server provides 3 tools:

1. **query_food_database**
   - Search for food information with AI
   - Example: "What is Biryani?"

2. **search_by_category**
   - Filter by category (Main Course, Dessert, etc.)
   - Example: category="Dessert"

3. **get_cache_statistics**
   - View performance metrics
   - No parameters needed

## 🧪 Quick Test Commands

```bash
# List all tools
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq

# Query about food
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"query_food_database",
      "arguments":{"question":"What are popular Indian desserts?"}
    }
  }' | jq -r '.result.content[0].text'

# Search by category
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":3,
    "method":"tools/call",
    "params":{
      "name":"search_by_category",
      "arguments":{"category":"Dessert"}
    }
  }' | jq

# Get cache stats
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":4,
    "method":"tools/call",
    "params":{"name":"get_cache_statistics","arguments":{}}
  }' | jq
```

## 🔗 Connect to Claude Desktop

If you want to use this MCP server with Claude Desktop:

1. **Configuration file**: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Your current config**:
```json
{
  "mcpServers": {
    "food-rag-system": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:3000/api/mcp"]
    }
  }
}
```

3. **Restart Claude Desktop** to load the MCP server

4. **Test in Claude**: "Using food-rag-system, tell me about Biryani"

## 🐛 Troubleshooting

### Server Not Responding?

```bash
# Check if server is running
lsof -ti:3000

# If not running, start it
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

### Port Already in Use?

```bash
# Kill existing process
lsof -ti:3000 | xargs kill -9

# Start fresh
npm run dev
```

### View Server Logs

```bash
# In the terminal where server is running
# You'll see real-time logs
```

## 📚 Additional Resources

- **MCP Protocol Docs**: https://modelcontextprotocol.io/
- **Project Documentation**: See `PROJECT_COMPLETE.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`

---

**Last Updated**: October 31, 2025
**Server Status**: Running on port 3000 ✅
**MCP Tools**: 3 available ✅
