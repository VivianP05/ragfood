# 🔧 Troubleshooting Guide - Food RAG MCP System

## 🎯 Your Current Setup

You have **TWO different MCP servers** available:

1. **HTTP-based MCP** (Next.js) - Currently Running ✅
   - URL: `http://localhost:3000/api/mcp`
   - File: `/Users/DELL/ragfood/mydigitaltwin/app/api/mcp/route.ts`
   - Port: 3000
   - Status: **Running** (PIDs: 753, 93478)

2. **Standalone MCP** (stdio) - Not Running
   - File: `/Users/DELL/ragfood/mydigitaltwin/mcp-server.js`
   - Protocol: stdin/stdout
   - Port: None
   - Status: **Not running**

---

## 🚀 Quick Tests

### Test 1: Check HTTP MCP Server (Currently Running)

```bash
# Test health check
curl http://localhost:3000/api/mcp

# Expected output:
# {"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}
```

### Test 2: List Available Tools

```bash
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq '.result.tools[].name'

# Expected output:
# "query_food_database"
# "search_by_category"
# "get_cache_statistics"
```

### Test 3: Test a Query

```bash
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"tools/call",
    "params":{
      "name":"query_food_database",
      "arguments":{"question":"What is Biryani?"}
    }
  }' | jq -r '.result.content[0].text'

# Expected: AI-generated response about Biryani
```

---

## ❌ Common Issues & Solutions

### **Issue 1: MCP Server Not Responding**

**Symptoms:**
- `curl http://localhost:3000/api/mcp` fails
- Connection refused errors
- 404 Not Found

**Diagnosis:**
```bash
# Check if server is running
lsof -ti:3000

# If no output, server is NOT running
```

**Solution:**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

**Expected output:**
```
✓ Starting...
✓ Ready in 2.3s
○ Local: http://localhost:3000
```

---

### **Issue 2: 500 Internal Server Error**

**Symptoms:**
- Server returns HTTP 500
- MCP endpoint accessible but tools fail

**Diagnosis:**
```bash
# Check server logs in the terminal where you ran `npm run dev`
# Look for error messages
```

**Common Causes:**

1. **Missing Environment Variables**
   ```bash
   # Check .env.local exists
   cat mydigitaltwin/.env.local
   
   # Should contain:
   # UPSTASH_VECTOR_REST_URL=https://free-loon-62438-us1-vector.upstash.io
   # UPSTASH_VECTOR_REST_TOKEN=your-token
   # GROQ_API_KEY=your-groq-key
   ```

2. **Upstash Connection Failed**
   ```bash
   # Test Upstash connection separately
   python3 check_upstash_database.py
   ```

3. **Groq API Issues**
   - Check your API key is valid
   - Verify you haven't exceeded rate limits
   - Check Groq dashboard: https://console.groq.com/

**Solution:**
```bash
# Restart server after fixing env vars
pkill -f "next dev"
npm run dev
```

---

### **Issue 3: VS Code Insiders MCP Not Connecting**

**Symptoms:**
- No "Start" button in `.vscode/mcp.json`
- Copilot doesn't recognize MCP tools
- MCP server not visible in VS Code

**Root Cause:**
VS Code Insiders MCP UI is still experimental and may not be available in your version.

**Solutions:**

**Option A: Use HTTP-based approach (Works Now)**
```bash
# Your server is already running at:
http://localhost:3000/api/mcp

# Test it directly:
curl http://localhost:3000/api/mcp
```

**Option B: Use Standalone MCP Server**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
node mcp-server.js

# This uses stdio (not HTTP) for MCP communication
```

**Option C: Update VS Code Insiders**
```bash
# Download latest version
open https://code.visualstudio.com/insiders/

# Check version after install
code-insiders --version
```

---

### **Issue 4: GitHub Copilot Not Using MCP**

**Symptoms:**
- Copilot doesn't see MCP tools
- `@workspace` commands don't use your server

**Diagnosis:**
```bash
# Check if MCP config exists
cat .vscode/mcp.json

# Check if settings.json has MCP enabled
cat .vscode/settings.json
```

**Current Status:**
- `.vscode/mcp.json` exists: ✅
- Points to standalone server (stdio)
- **But your HTTP server is what's running**

**Solution:**

Update `.vscode/mcp.json` to use HTTP approach:
```json
{
  "food-rag-system": {
    "command": "npm",
    "args": ["run", "dev"],
    "cwd": "${workspaceFolder}/mydigitaltwin"
  }
}
```

**Then:**
1. Reload VS Code: `Cmd+Shift+P` → "Reload Window"
2. Check for MCP status in status bar
3. Try: `@workspace What is Biryani?`

---

### **Issue 5: No Responses from Food Database**

**Symptoms:**
- MCP server responds but says "no results"
- Queries return empty answers

**Diagnosis:**
```bash
# Check if database has data
python3 check_upstash_database.py

# Expected: "Total vectors: 200" or similar
```

**Solutions:**

1. **Database is Empty:**
   ```bash
   # Upload food data
   python3 upload_foods_to_upstash.py
   ```

2. **Wrong Database:**
   ```bash
   # Verify UPSTASH_VECTOR_REST_URL in .env.local
   # Should be: https://free-loon-62438-us1-vector.upstash.io
   cat mydigitaltwin/.env.local | grep UPSTASH_VECTOR_REST_URL
   ```

3. **Query Too Specific:**
   ```bash
   # Try broader questions
   # ❌ "Tell me about XYZ obscure dish"
   # ✅ "What is Biryani?" (known to be in database)
   ```

---

### **Issue 6: Port 3000 Already in Use**

**Symptoms:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Diagnosis:**
```bash
# Find what's using port 3000
lsof -ti:3000
```

**Solution:**
```bash
# Kill the process
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 npm run dev
```

---

## 🔍 Debugging Commands

### **Check Server Status**
```bash
# Is Next.js running?
lsof -ti:3000

# What process is it?
ps aux | grep "next dev" | grep -v grep

# Test HTTP endpoint
curl http://localhost:3000/api/mcp
```

### **Check Environment**
```bash
# Are env vars loaded?
cd mydigitaltwin
node -e "require('dotenv').config({path:'.env.local'}); console.log(process.env.UPSTASH_VECTOR_REST_URL)"
```

### **Check Database**
```bash
# Python check
python3 check_upstash_database.py

# Direct API check
curl "https://free-loon-62438-us1-vector.upstash.io/info" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **Check Logs**
```bash
# Start server with verbose logging
cd mydigitaltwin
npm run dev

# Watch for errors in output
```

---

## 🎯 Health Check Checklist

Run through this checklist to verify everything:

```bash
# 1. Server running?
lsof -ti:3000
# ✅ Should show PID numbers

# 2. MCP endpoint accessible?
curl http://localhost:3000/api/mcp
# ✅ Should return {"status":"ok",...}

# 3. Tools available?
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq '.result.tools | length'
# ✅ Should return: 3

# 4. Database accessible?
python3 check_upstash_database.py
# ✅ Should show vector count

# 5. Test query works?
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"query_food_database","arguments":{"question":"What is Biryani?"}}}' | jq -r '.result.content[0].text | .[0:100]'
# ✅ Should return first 100 chars of answer
```

---

## 📊 Current Status

Based on your system right now:

| Component | Status | Details |
|-----------|--------|---------|
| **Next.js Server** | ✅ Running | Port 3000, PIDs: 753, 93478 |
| **HTTP MCP Endpoint** | ✅ Available | http://localhost:3000/api/mcp |
| **Standalone MCP** | ❌ Not Running | Would use stdio, not HTTP |
| **VS Code MCP Config** | ⚠️ Misconfigured | Points to standalone, but HTTP is running |
| **Database** | ✅ Ready | Upstash Vector (200 food items) |
| **Environment Vars** | ✅ Loaded | .env.local detected |

---

## 🚀 Recommended Actions

### **For Your Current Setup (HTTP-based MCP):**

1. **Keep using the running server:**
   ```bash
   # It's already running, test it:
   curl http://localhost:3000/api/mcp
   ```

2. **Test tools directly:**
   ```bash
   # List tools
   curl -X POST http://localhost:3000/api/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
   ```

3. **If you want VS Code MCP integration:**
   - Update `.vscode/mcp.json` to use `npm run dev`
   - Reload VS Code
   - Look for MCP status

### **For Standalone MCP:**

1. **Stop the Next.js server:**
   ```bash
   lsof -ti:3000 | xargs kill -9
   ```

2. **Start standalone MCP:**
   ```bash
   cd mydigitaltwin
   node mcp-server.js
   ```

3. **This uses stdio** (not HTTP), better for Claude Desktop

---

## 💡 Which Server Should You Use?

| Use Case | Server Type | How to Start |
|----------|-------------|--------------|
| **Web UI** | HTTP (Next.js) | `npm run dev` |
| **GitHub Copilot** | HTTP (Next.js) | `npm run dev` |
| **Claude Desktop** | Standalone (stdio) | `node mcp-server.js` |
| **Direct API calls** | HTTP (Next.js) | `npm run dev` |
| **VS Code MCP (future)** | Either | Both work |

---

## 📞 Still Having Issues?

1. **Check the logs** in the terminal where server is running
2. **Try the health check checklist** above
3. **Verify environment variables** are correct
4. **Test with simple curl commands** first
5. **Check this file** for solutions: `HOW_TO_START_MCP.md`

---

**Your HTTP MCP server is running right now! Test it:**

```bash
curl http://localhost:3000/api/mcp
```

Should return: `{"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}` ✅
