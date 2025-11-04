# 🚀 VS Code Insiders MCP Integration - Complete Guide

## ✅ Setup Complete!

Your Food RAG MCP Server is now properly configured for VS Code Insiders with comprehensive monitoring.

---

## 📁 Configuration Files

### **Single JSON Configuration** (as requested)

**Location:** `.vscode/mcp.json`

```json
{
  "food-rag-system": {
    "command": "node",
    "args": ["${workspaceFolder}/mydigitaltwin/mcp-server.js"],
    "env": {
      "NODE_ENV": "development"
    }
  }
}
```

**What it does:**
- Tells VS Code Insiders to run `mcp-server.js` as a standalone MCP server
- Uses Node.js directly (not npm run dev)
- Provides clean monitoring output

---

## 🎯 How to Use in VS Code Insiders

### **Method 1: Using the VS Code UI (Recommended)**

1. **Open the MCP configuration file:**
   ```
   .vscode/mcp.json
   ```

2. **Look for the "Start" button:**
   - You should see a clickable link/button near line 2: `"food-rag-system"`
   - It might appear as: `▶ Start` or `Start Server`

3. **Click the "Start" button**
   - VS Code will launch the MCP server
   - The Output panel will automatically open

4. **Monitor in Output Panel:**
   - Bottom panel → "Output" tab
   - Dropdown: Select "MCP: food-rag-system"
   - You'll see real-time logs like:
     ```
     ✅ [SUCCESS] Environment variables validated
     ✅ [SUCCESS] Connected to Upstash Vector Database
     ✅ [SUCCESS] Connected to Groq AI
     ✅ [SUCCESS] ✨ Food RAG MCP Server is running!
     ```

---

### **Method 2: Manual Start (if no Start button)**

If you don't see the Start button, run manually:

```bash
cd /Users/DELL/ragfood/mydigitaltwin
node mcp-server.js
```

**Expected output:**
```
ℹ️  [INFO] MCP Server initialized
✅ [SUCCESS] Environment variables validated
✅ [SUCCESS] Connected to Upstash Vector Database
✅ [SUCCESS] Connected to Groq AI (llama-3.1-8b-instant)
ℹ️  [INFO] Starting Food RAG MCP Server...
✅ [SUCCESS] ✨ Food RAG MCP Server is running!
📍 [INFO] Available tools: query_food_database, search_by_category, get_cache_statistics
🔗 [INFO] Database: Upstash Vector (200+ food items)
🤖 [INFO] AI Model: Groq llama-3.1-8b-instant
📊 [INFO] Monitor this output in VS Code Output panel
---------------------------------------------------
```

---

## 🔍 Monitoring Features

The MCP server logs everything to the VS Code Output panel:

### **Log Types:**

| Icon | Level | Description |
|------|-------|-------------|
| ℹ️ | INFO | General information |
| ✅ | SUCCESS | Successful operations |
| ⚠️ | WARN | Warnings (non-critical) |
| ❌ | ERROR | Errors with details |
| 🔍 | DEBUG | Debug information |
| 🔧 | TOOL | Tool execution with timing |

### **Example Output:**

```
ℹ️  [INFO] Tool call: query_food_database
🔍 [DEBUG] Processing question: "What is Biryani?..."
🔍 [DEBUG] Searching Upstash Vector database...
🔍 [DEBUG] Vector search completed in 450ms (3 results)
🔍 [DEBUG] Context built from vector results
🔍 [DEBUG] Generating AI response with Groq...
✅ [SUCCESS] Query completed in 1650ms (vector: 450ms, AI: 1150ms)
🔧 [TOOL] query_food_database (1650ms)
```

---

## 🛠️ Available MCP Tools

### **1. query_food_database**
**Purpose:** AI-powered food queries with RAG

**Example usage:**
- "What is Biryani?"
- "Tell me about Japanese cuisine"
- "What are healthy breakfast options?"

**Logs you'll see:**
```
ℹ️  [INFO] Tool call: query_food_database
🔍 [DEBUG] Processing question: "What is Biryani?..."
🔍 [DEBUG] Searching Upstash Vector database...
🔍 [DEBUG] Vector search completed in 450ms (3 results)
✅ [SUCCESS] Query completed in 1650ms
🔧 [TOOL] query_food_database (1650ms)
```

---

### **2. search_by_category**
**Purpose:** Direct category-based search

**Example usage:**
- "Search for desserts"
- "Find main course dishes"
- "Show me Indian snacks"

**Logs you'll see:**
```
ℹ️  [INFO] Tool call: search_by_category
🔍 [DEBUG] Searching for category: "desserts" (limit: 5)
✅ [SUCCESS] Found 5 results in 380ms
🔧 [TOOL] search_by_category (380ms)
```

---

### **3. get_cache_statistics**
**Purpose:** Server status and information

**Logs you'll see:**
```
ℹ️  [INFO] Tool call: get_cache_statistics
🔍 [DEBUG] Fetching cache statistics...
✅ [SUCCESS] Cache statistics retrieved in 15ms
🔧 [TOOL] get_cache_statistics (15ms)
```

---

## 🔧 Troubleshooting

### **Issue: No "Start" button in .vscode/mcp.json**

**Solutions:**

1. **Update VS Code Insiders:**
   - Download latest: https://code.visualstudio.com/insiders/
   - MCP UI features require recent builds (Nov 2024+)

2. **Reload VS Code:**
   - Press `Cmd+Shift+P`
   - Type "Reload Window"
   - Press Enter

3. **Start manually:**
   ```bash
   cd /Users/DELL/ragfood/mydigitaltwin
   node mcp-server.js
   ```

---

### **Issue: Environment variable errors**

**Error message:**
```
❌ [ERROR] Missing required environment variables:
   - UPSTASH_VECTOR_REST_URL
   - UPSTASH_VECTOR_REST_TOKEN
   - GROQ_API_KEY
```

**Solution:**

1. Check `.env.local` exists:
   ```bash
   cat /Users/DELL/ragfood/mydigitaltwin/.env.local
   ```

2. Verify it contains:
   ```
   UPSTASH_VECTOR_REST_URL=https://free-loon-62438-us1-vector.upstash.io
   UPSTASH_VECTOR_REST_TOKEN=your-token-here
   GROQ_API_KEY=your-api-key-here
   ```

3. Restart the MCP server

---

### **Issue: Server won't start**

**Check Node.js version:**
```bash
node --version  # Should be v18+ (you have v22.20.0 ✅)
```

**Check dependencies:**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm list @modelcontextprotocol/sdk @upstash/vector groq-sdk dotenv
```

**Expected output:**
```
✅ @modelcontextprotocol/sdk@1.20.2
✅ @upstash/vector@1.2.2
✅ groq-sdk@0.34.0
✅ dotenv@17.2.3
```

---

## 🎯 Testing the Server

### **Test 1: Start the server manually**

```bash
cd /Users/DELL/ragfood/mydigitaltwin
node mcp-server.js
```

**Expected output:**
- ✅ Success messages for environment, database, and AI connection
- ✅ "Food RAG MCP Server is running!" message
- ✅ List of available tools

**Press `Ctrl+C` to stop**

---

### **Test 2: Use VS Code Insiders**

1. Open `.vscode/mcp.json`
2. Click the "Start" button (if available)
3. Check Output panel → "MCP: food-rag-system"
4. You should see the same success messages

---

### **Test 3: Use GitHub Copilot Chat (if available)**

In Copilot Chat, try:
```
Use the food-rag-system to tell me about Biryani
```

You'll see logs in Output panel:
```
ℹ️  [INFO] Tool call: query_food_database
🔍 [DEBUG] Processing question: "tell me about Biryani"
...
✅ [SUCCESS] Query completed in 1650ms
```

---

## 📊 Performance Monitoring

The server logs detailed performance metrics:

**Example:**
```
✅ [SUCCESS] Query completed in 1650ms (vector: 450ms, AI: 1150ms)
```

**What this means:**
- **Total time:** 1650ms
- **Vector search:** 450ms (searching Upstash database)
- **AI generation:** 1150ms (Groq generating response)

**Typical performance:**
- Vector search: 200-600ms
- AI generation: 800-1500ms
- Total: 1000-2000ms per query

---

## 📁 File Structure

```
/Users/DELL/ragfood/
├── .vscode/
│   ├── mcp.json              ← Single MCP configuration (ONLY FILE NEEDED)
│   └── settings.json         ← Empty (removed duplicate config)
│
└── mydigitaltwin/
    ├── mcp-server.js         ← Standalone MCP server
    ├── .env.local            ← Environment variables
    └── package.json          ← Dependencies
```

---

## ✅ Summary

**What we've built:**
1. ✅ **Standalone MCP server** (`mcp-server.js`) - 330 lines
2. ✅ **Single configuration file** (`.vscode/mcp.json`) - Clean setup
3. ✅ **Comprehensive monitoring** - All logs go to VS Code Output panel
4. ✅ **3 powerful tools** - Query, search, statistics
5. ✅ **Production-ready** - Error handling, validation, performance tracking

**What you can do now:**
1. ✅ Start server via VS Code UI "Start" button
2. ✅ Monitor in real-time in Output panel
3. ✅ Use with GitHub Copilot Chat
4. ✅ Query 200+ food items with AI
5. ✅ Track performance metrics

---

## 🚀 Next Steps

1. **Reload VS Code Insiders** (to see the Start button)
2. **Open `.vscode/mcp.json`**
3. **Click "Start"** or run `node mcp-server.js` manually
4. **Monitor Output panel** for logs
5. **Test with Copilot Chat** or use the tools directly

---

**Need help?** Check the troubleshooting section above or view the detailed logs in the Output panel!

🎉 **Your MCP server is ready to use!**
