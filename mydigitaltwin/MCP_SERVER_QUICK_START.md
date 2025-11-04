# 🚀 Food RAG MCP Server - Quick Start

## Problem: "Couldn't connect to Claude"

This error happens when the MCP server (Next.js) isn't running properly. Here's how to fix it:

---

## ✅ Solution: Start Server in a Dedicated Terminal

### Step 1: Open a New Terminal Window

1. Press `Cmd + Space`
2. Type "Terminal"
3. Press Enter

### Step 2: Start the MCP Server

Run this command:

```bash
cd /Users/DELL/ragfood/mydigitaltwin
./start-mcp.sh
```

**Alternative** (if script doesn't work):
```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

### Step 3: Keep Terminal Open

⚠️ **CRITICAL**: Do NOT close this terminal window!

You should see:
```
✓ Ready in XXXms
```

---

## Step 4: Restart Claude Desktop

1. **Quit Claude** completely (`Cmd + Q`)
2. Wait 5-10 seconds
3. **Relaunch** Claude Desktop
4. Look for connection indicators

---

## Step 5: Test the Connection

In Claude Desktop, try:

```
Using food-rag-system, tell me about Biryani
```

You should see Claude use the tool and return food information!

---

## 🔍 Troubleshooting

### "Port 3000 is already in use"

Kill the old process:
```bash
lsof -ti:3000 | xargs kill -9
```

Then restart with `./start-mcp.sh`

### Still Can't Connect?

1. **Verify server is running**:
   ```bash
   curl http://localhost:3000/api/mcp
   ```
   
   Should return:
   ```json
   {"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}
   ```

2. **Check Claude config**:
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
   
   Should have:
   ```json
   "food-rag-system": {
     "command": "npx",
     "args": ["-y", "mcp-remote", "http://localhost:3000/api/mcp"]
   }
   ```

3. **Check terminal location**:
   Make sure you're in `/Users/DELL/ragfood/mydigitaltwin` (not parent directory)

---

## 📊 What's Happening Behind the Scenes

```
┌─────────────────────┐
│  Claude Desktop     │
│                     │
│  food-rag-system    │
└──────────┬──────────┘
           │
           │ mcp-remote connects to →
           ↓
┌─────────────────────┐
│  localhost:3000     │
│  /api/mcp           │
│                     │
│  Next.js Server     │ ← Must be running in terminal!
│  (Terminal window)  │
└─────────────────────┘
```

**Key Points**:
- ✅ Server MUST be running in a terminal
- ✅ Terminal MUST stay open
- ✅ Use `npm run dev` (not background process)
- ✅ Restart Claude Desktop after server starts

---

## 🎯 Expected Workflow

1. **Open dedicated terminal** → Run `./start-mcp.sh`
2. **Keep terminal open** → Server stays running
3. **Launch Claude Desktop** → Connects to server
4. **Use tools** → `food-rag-system` available
5. **When done** → Ctrl+C in terminal to stop server

---

## ⚡ Quick Commands

```bash
# Start server
cd /Users/DELL/ragfood/mydigitaltwin && npm run dev

# Test endpoint
curl http://localhost:3000/api/mcp

# Check running processes
lsof -ti:3000

# Kill server
pkill -f "next dev"

# View Claude config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

---

## 🆘 Still Having Issues?

Check these files:
- `MCP_TROUBLESHOOTING.md` - Comprehensive troubleshooting
- `VISUAL_GUIDE.md` - Step-by-step with diagrams
- `CLAUDE_SETUP_COMPLETE.md` - Full setup guide

---

**Last Updated**: October 31, 2025  
**Server**: http://localhost:3000/api/mcp  
**Tools**: query_food_database, search_by_category, get_cache_statistics
