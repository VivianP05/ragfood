# 🎯 How to Start Your Food RAG MCP Server

## ❌ No "Start" Button? Here's What to Do!

The VS Code Insiders MCP UI (Start button in JSON files) is still experimental. **Don't worry!** Here are 3 simple ways to start your MCP server with full monitoring.

---

## ✅ Method 1: VS Code Tasks (EASIEST - Recommended!)

### **Step-by-Step:**

1. **Open Command Palette**
   - Press: `Cmd+Shift+P` (macOS)

2. **Run the Task**
   - Type: `Tasks: Run Task`
   - Select: **"Start Food RAG MCP Server"**

3. **Watch the Output**
   - A terminal will open automatically
   - You'll see logs like:
     ```
     ✅ [SUCCESS] Environment variables validated
     ✅ [SUCCESS] Connected to Upstash Vector Database
     ✅ [SUCCESS] ✨ Food RAG MCP Server is running!
     ```

4. **Keep It Running**
   - Leave this terminal open
   - The server must stay active

### **To Stop the Server:**
   - Press `Ctrl+C` in the terminal
   - Or run task: "Stop Food RAG MCP Server"

---

## ✅ Method 2: Terminal Command (SIMPLE)

### **In VS Code Terminal:**

1. **Open Terminal**
   - Press: `` Cmd+` `` (backtick key)
   - Or: Menu → View → Terminal

2. **Run These Commands:**
   ```bash
   cd mydigitaltwin
   node mcp-server.js
   ```

3. **You'll See:**
   ```
   ℹ️  [INFO] MCP Server initialized
   ✅ [SUCCESS] Environment variables validated
   ✅ [SUCCESS] Connected to Upstash Vector Database
   ✅ [SUCCESS] Connected to Groq AI (llama-3.1-8b-instant)
   ✅ [SUCCESS] ✨ Food RAG MCP Server is running!
   📍 [INFO] Available tools: query_food_database, search_by_category, get_cache_statistics
   🔗 [INFO] Database: Upstash Vector (200+ food items)
   🤖 [INFO] AI Model: Groq llama-3.1-8b-instant
   📊 [INFO] Monitor this output in VS Code Output panel
   ---------------------------------------------------
   ```

4. **Keep Terminal Open!**

### **To Stop:**
   - Press `Ctrl+C`

---

## ✅ Method 3: Shell Script (ONE-CLICK)

### **From Terminal:**

```bash
cd /Users/DELL/ragfood/mydigitaltwin
./start-mcp-standalone.sh
```

### **What You'll See:**

```
🚀 Starting Food RAG MCP Server (Standalone)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Environment: OK
✅ Node.js version: v22.20.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MONITORING STARTED - Watch for logs below
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ℹ️  [INFO] MCP Server initialized
✅ [SUCCESS] Environment variables validated
✅ [SUCCESS] Connected to Upstash Vector Database
✅ [SUCCESS] Connected to Groq AI (llama-3.1-8b-instant)
✅ [SUCCESS] ✨ Food RAG MCP Server is running!
```

---

## 📊 What to Expect When Running

### **Initial Startup (1-2 seconds):**
```
ℹ️  [INFO] MCP Server initialized
✅ [SUCCESS] Environment variables validated
✅ [SUCCESS] Connected to Upstash Vector Database
✅ [SUCCESS] Connected to Groq AI (llama-3.1-8b-instant)
ℹ️  [INFO] Starting Food RAG MCP Server...
✅ [SUCCESS] ✨ Food RAG MCP Server is running!
```

### **When Someone Uses a Tool:**
```
ℹ️  [INFO] Tool call: query_food_database
🔍 [DEBUG] Arguments: {
  "question": "What is Biryani?"
}
🔍 [DEBUG] Processing question: "What is Biryani?..."
🔍 [DEBUG] Searching Upstash Vector database...
🔍 [DEBUG] Vector search completed in 450ms (3 results)
🔍 [DEBUG] Context built from vector results
🔍 [DEBUG] Generating AI response with Groq...
✅ [SUCCESS] Query completed in 1650ms (vector: 450ms, AI: 1150ms)
🔧 [TOOL] query_food_database (1650ms)
```

### **Performance Metrics:**
Every tool call shows:
- ⏱️ **Total time** (e.g., 1650ms)
- 🔍 **Vector search time** (e.g., 450ms)
- 🤖 **AI generation time** (e.g., 1150ms)
- 📊 **Results count** (e.g., 3 results)

---

## 🔧 Troubleshooting

### **Problem: "Missing environment variables"**

**Error:**
```
❌ [ERROR] Missing required environment variables:
   - UPSTASH_VECTOR_REST_URL
   - UPSTASH_VECTOR_REST_TOKEN
   - GROQ_API_KEY
```

**Solution:**
1. Check if `.env.local` exists:
   ```bash
   ls -la /Users/DELL/ragfood/mydigitaltwin/.env.local
   ```

2. It should contain:
   ```
   UPSTASH_VECTOR_REST_URL=https://free-loon-62438-us1-vector.upstash.io
   UPSTASH_VECTOR_REST_TOKEN=your-token-here
   GROQ_API_KEY=your-api-key-here
   ```

3. Get actual values from your main `.env` file:
   ```bash
   cat /Users/DELL/ragfood/.env
   ```

---

### **Problem: "Cannot find module"**

**Error:**
```
Error: Cannot find module '@modelcontextprotocol/sdk/server/index.js'
```

**Solution:**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm install
```

---

### **Problem: Server starts but no logs appear**

**Reason:** The server outputs to `stderr` (error stream), which is normal for logging.

**Solution:** Everything is working! The logs ARE appearing in your terminal.

---

## 📱 Using with GitHub Copilot Chat

Once your server is running, you can use it in Copilot Chat:

### **Example 1: Food Query**
```
@workspace Use the food-rag-system to tell me about Biryani
```

**You'll see in terminal:**
```
ℹ️  [INFO] Tool call: query_food_database
🔍 [DEBUG] Processing question: "tell me about Biryani"
✅ [SUCCESS] Query completed in 1650ms
```

---

### **Example 2: Search**
```
@workspace Search for desserts using food-rag-system
```

**Terminal output:**
```
ℹ️  [INFO] Tool call: search_by_category
🔍 [DEBUG] Searching for category: "desserts" (limit: 5)
✅ [SUCCESS] Found 5 results in 380ms
```

---

### **Example 3: Statistics**
```
@workspace Get status of food-rag-system
```

**Terminal output:**
```
ℹ️  [INFO] Tool call: get_cache_statistics
✅ [SUCCESS] Cache statistics retrieved in 15ms
```

---

## 🎯 Quick Reference Card

| **Action** | **Command** |
|------------|-------------|
| **Start (Task)** | `Cmd+Shift+P` → `Tasks: Run Task` → `Start Food RAG MCP Server` |
| **Start (Terminal)** | `cd mydigitaltwin && node mcp-server.js` |
| **Start (Script)** | `./start-mcp-standalone.sh` |
| **Stop** | Press `Ctrl+C` in terminal |
| **Check Status** | Look for `✅ [SUCCESS] ✨ Food RAG MCP Server is running!` |
| **View Logs** | Watch the terminal where server is running |

---

## 📁 Files Created

✅ **`.vscode/tasks.json`** - VS Code tasks for easy start/stop  
✅ **`.vscode/mcp.json`** - MCP configuration (for future VS Code features)  
✅ **`mydigitaltwin/mcp-server.js`** - Standalone MCP server (330 lines)  
✅ **`mydigitaltwin/start-mcp-standalone.sh`** - Shell script for easy startup  

---

## 🚀 Recommended Workflow

### **Best Way to Start:**

1. **Open VS Code Insiders**
2. **Press `Cmd+Shift+P`**
3. **Type: `Tasks: Run Task`**
4. **Select: "Start Food RAG MCP Server"**
5. **Watch logs in the terminal panel**
6. **Leave it running in background**

### **When You're Done:**
- Just press `Ctrl+C` in the terminal
- Or close VS Code (server will stop automatically)

---

## 💡 Why This Approach?

**The "Start" button in `.vscode/mcp.json` requires:**
- ✗ Specific VS Code Insiders version (Dec 2024+)
- ✗ Experimental MCP UI features enabled
- ✗ GitHub Copilot with MCP support

**Our approach works:**
- ✅ Right now with any VS Code version
- ✅ With full monitoring and logging
- ✅ Same functionality, simpler setup
- ✅ Better debugging experience

---

## 🎉 You're Ready!

Your MCP server is ready to use with **3 easy start methods**:

1. ⭐ **VS Code Tasks** (Easiest - recommended!)
2. 💻 **Terminal Command** (Simple and direct)
3. 📜 **Shell Script** (One-click startup)

**Choose whichever you prefer and start monitoring your Food RAG System!** 🍽️

---

**Need help?** All commands are in this guide. Just follow the steps above! 👆
