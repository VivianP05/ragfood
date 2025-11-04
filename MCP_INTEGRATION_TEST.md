# MCP Integration Test

## ✅ Test MCP Connection in VS Code Insiders

### Step 1: Open GitHub Copilot Chat
- Press `Cmd+Shift+I` or click the Copilot icon in the sidebar
- The chat panel should open

### Step 2: Test MCP Tools

Try asking Copilot these questions:

**Test 1: List Available Tools**
```
What MCP tools are available in this workspace?
```

**Test 2: Use the Food RAG System**
```
Use the food-rag-system to tell me about Biryani
```

**Test 3: Search by Category**
```
Using the food-rag-system, search for desserts
```

**Test 4: Get Cache Statistics**
```
Show me the cache statistics from the food-rag-system
```

---

## 🔍 What to Look For

### In Copilot Chat:
- ✅ Copilot should recognize "food-rag-system" as an available tool
- ✅ It should be able to call the MCP server to query the food database
- ✅ You should get AI-generated responses about food

### In the Status Bar:
- Look for "MCP" or connection indicator
- GitHub Copilot should show as active

### If MCP is Working:
You'll see responses that come from your Food RAG database (200+ food items) with detailed information about cuisines, dishes, ingredients, and recipes.

---

## 🚨 Troubleshooting

### If Copilot doesn't recognize the tools:

1. **Check VS Code Insiders version:**
   - Go to: Code → About Visual Studio Code - Insiders
   - Make sure you have a recent build (October 2024 or later)

2. **Manually verify MCP endpoint:**
   ```bash
   curl -X POST http://localhost:3000/api/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
     | jq '.result.tools'
   ```

3. **Check Output panel:**
   - Press `Cmd+Shift+U`
   - Select "GitHub Copilot Chat" from dropdown
   - Look for any MCP-related errors

4. **Restart the MCP server:**
   ```bash
   # Kill existing processes
   lsof -ti:3000 | xargs kill -9
   
   # Restart server
   cd mydigitaltwin
   npm run dev
   ```

---

## 📝 Current Configuration

- ✅ **MCP Server**: http://localhost:3000/api/mcp
- ✅ **Tools Available**: 3 (query_food_database, search_by_category, get_cache_statistics)
- ✅ **VS Code Settings**: `.vscode/settings.json` configured
- ✅ **MCP Config**: `.vscode/mcp.json` ready
- ✅ **Server Status**: Running (PIDs: 753, 93478)

---

## 🎯 Next Steps

1. Open Copilot Chat in VS Code Insiders
2. Try the test queries above
3. Report back what you see!

If Copilot successfully uses the food-rag-system tools, you'll know MCP is fully integrated! 🎉
