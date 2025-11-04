# 🚀 Start MCP Server - Simple Guide

## ❌ No "Start" Button? Use This Instead!

The VS Code Insiders MCP UI (Start button) is still in development. Here's how to start your MCP server **right now**:

---

## ✅ Method 1: Use Terminal in VS Code

### **Step 1: Open Integrated Terminal**
- Press `` Cmd+` `` (backtick key)
- Or: View → Terminal

### **Step 2: Run the MCP Server**
```bash
cd mydigitaltwin
node mcp-server.js
```

### **Step 3: Watch the Output**
You'll see:
```
✅ [SUCCESS] Environment variables validated
✅ [SUCCESS] Connected to Upstash Vector Database
✅ [SUCCESS] Connected to Groq AI (llama-3.1-8b-instant)
ℹ️  [INFO] Starting Food RAG MCP Server...
✅ [SUCCESS] ✨ Food RAG MCP Server is running!
📍 [INFO] Available tools: query_food_database, search_by_category, get_cache_statistics
🔗 [INFO] Database: Upstash Vector (200+ food items)
🤖 [INFO] AI Model: Groq llama-3.1-8b-instant
```

**Keep this terminal running!** The server needs to stay active.

---

## ✅ Method 2: Use VS Code Tasks (Recommended)

I'll create a VS Code task that you can run with one click.

### **Step 1: I'll create the task file**
(Creating now...)

### **Step 2: Run the task**
- Press `Cmd+Shift+P`
- Type: "Tasks: Run Task"
- Select: "Start Food RAG MCP Server"

This will start the server in a dedicated terminal panel.

---

## ✅ Method 3: Create a Launch Script

I'll create a simple start script you can double-click or run easily.

---

## 🔍 Why No Start Button?

The VS Code Insiders MCP UI is still experimental and requires:
1. Very recent VS Code Insiders build (Dec 2024+)
2. Specific MCP extensions enabled
3. GitHub Copilot Chat enabled with MCP support

**But you don't need it!** The methods above work perfectly.

---

## 📊 Monitoring Your Server

Once started, you'll see real-time logs like:

```
ℹ️  [INFO] Tool call: query_food_database
🔍 [DEBUG] Processing question: "What is Biryani?..."
🔍 [DEBUG] Searching Upstash Vector database...
🔍 [DEBUG] Vector search completed in 450ms (3 results)
✅ [SUCCESS] Query completed in 1650ms (vector: 450ms, AI: 1150ms)
🔧 [TOOL] query_food_database (1650ms)
```

---

Let me create the VS Code task and launch script for you now...
