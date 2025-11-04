# 🔧 MCP Connection Troubleshooting Guide

## Issue: "food-rag-system disconnected" in Claude Desktop

This guide will help you fix the disconnection issue and keep your MCP server running properly.

---

## 🎯 Quick Fix (Do This First!)

### Step 1: Start the Server Properly

**Option A: Use the startup script (RECOMMENDED)**

```bash
cd /Users/DELL/ragfood/mydigitaltwin
./start-mcp-server.sh
```

**Option B: Manual start**

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

### Step 2: Keep the Terminal Open!

⚠️ **CRITICAL**: Do NOT close the terminal window!
- The server MUST stay running for Claude to connect
- You'll see: `✓ Ready in XXXms`
- Keep this window in the background

### Step 3: Verify Server is Running

Open a **new terminal** and test:

```bash
curl http://localhost:3000/api/mcp
```

**Expected response**:
```json
{"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}
```

If you get this response, your server is working! ✅

### Step 4: Reconnect Claude Desktop

Claude Desktop needs to detect the server:

1. **Don't close Claude** - just wait 10-20 seconds
2. Or try typing a new message
3. The 🔌 icon should reappear
4. If not, quit and relaunch Claude (Cmd+Q)

---

## 🔍 Common Issues & Solutions

### Issue 1: "Connection refused" or "Failed to connect"

**Cause**: Server is not running

**Solution**:
```bash
# Check if server is running
lsof -ti:3000

# If nothing appears, start server:
cd /Users/DELL/ragfood/mydigitaltwin
./start-mcp-server.sh
```

### Issue 2: "404 Not Found" when testing endpoint

**Cause**: Server is running but MCP route not loaded

**Solution**:
```bash
# Kill old server process
kill -9 $(lsof -ti:3000)

# Start fresh
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

### Issue 3: Server starts but disconnects after a few minutes

**Cause**: Server crashed or terminal was closed

**Solution**:
1. Check the terminal where server is running
2. Look for error messages
3. Common errors:
   - Missing environment variables → Check `.env.local`
   - Port already in use → Kill old process
   - Out of memory → Restart computer

### Issue 4: Claude says "Tool not found"

**Cause**: MCP configuration issue or server not responding

**Solution**:
```bash
# 1. Verify config file
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Should show "food-rag-system" entry

# 3. Restart everything:
# - Quit Claude Desktop (Cmd+Q)
# - Kill server: kill -9 $(lsof -ti:3000)
# - Start server: cd /Users/DELL/ragfood/mydigitaltwin && npm run dev
# - Relaunch Claude Desktop
```

---

## 📋 Proper Workflow

Follow this workflow every time you want to use the Food RAG System:

### Morning Routine:

```bash
# 1. Open Terminal
cd /Users/DELL/ragfood/mydigitaltwin

# 2. Start server
./start-mcp-server.sh

# 3. Minimize terminal (don't close!)

# 4. Open Claude Desktop

# 5. Wait 10-20 seconds for connection

# 6. Test with: "Using food-rag-system, tell me about Biryani"
```

### Evening Shutdown:

```bash
# 1. Go to terminal running server

# 2. Press Ctrl+C to stop

# 3. Close terminal

# 4. Quit Claude Desktop (Cmd+Q)
```

---

## 🧪 Testing Checklist

Run through this checklist to verify everything works:

### Server Health Check:

- [ ] Terminal shows `✓ Ready in XXXms`
- [ ] No error messages in terminal
- [ ] Port 3000 is being used: `lsof -ti:3000` returns a process ID

### Endpoint Test:

```bash
# Test 1: Health check
curl http://localhost:3000/api/mcp

# Expected: {"status":"ok",...}

# Test 2: Main page
curl http://localhost:3000

# Expected: HTML content (the chat interface)

# Test 3: MCP tools list
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/list"}'

# Expected: {"tools":[...]} with 3 tools
```

### Claude Desktop Check:

- [ ] Claude Desktop is running
- [ ] 🔌 icon visible (or tools indicator)
- [ ] "food-rag-system" appears in tools
- [ ] Test query works

---

## 🚨 Emergency Reset

If nothing works, do a complete reset:

### 1. Kill Everything

```bash
# Kill all node processes
killall node

# Kill all Next.js servers
kill -9 $(lsof -ti:3000)

# Quit Claude Desktop
# (Cmd+Q)
```

### 2. Clean Restart

```bash
# Navigate to project
cd /Users/DELL/ragfood/mydigitaltwin

# Clean Next.js cache
rm -rf .next

# Reinstall dependencies (if needed)
rm -rf node_modules
npm install

# Start server
npm run dev
```

### 3. Wait & Verify

```bash
# Wait 5 seconds for server to start
sleep 5

# Test endpoint
curl http://localhost:3000/api/mcp

# Should return {"status":"ok",...}
```

### 4. Restart Claude

- Launch Claude Desktop
- Wait 20-30 seconds
- Look for 🔌 icon
- Test with prompt

---

## 💡 Pro Tips

### Tip 1: Keep Terminal Visible

Create a dedicated desktop space for your server terminal so you can always see if it's running.

### Tip 2: Check Server Before Using Claude

Before opening Claude Desktop, verify server is running:
```bash
curl http://localhost:3000/api/mcp
```

### Tip 3: Use the Startup Script

The `start-mcp-server.sh` script includes helpful checks and clear output.

### Tip 4: Monitor Server Logs

Watch the server terminal for errors. Common issues:
- `ENOENT: no such file` → Missing files
- `ECONNREFUSED` → API connection issues
- `Missing environment variables` → Check `.env.local`

### Tip 5: Dedicated Terminal Window

Use iTerm2 or a separate Terminal window just for the server. Label it "MCP Server" so you don't accidentally close it.

---

## 🔧 Advanced Debugging

### Check MCP Route File

```bash
# Verify file exists
ls -la /Users/DELL/ragfood/mydigitaltwin/src/app/api/mcp/route.ts

# View first 10 lines
head -10 /Users/DELL/ragfood/mydigitaltwin/src/app/api/mcp/route.ts
```

### Check Environment Variables

```bash
# Verify .env.local exists
ls -la /Users/DELL/ragfood/mydigitaltwin/.env.local

# Check variables are set (doesn't show values)
grep -o '^[A-Z_]*=' /Users/DELL/ragfood/mydigitaltwin/.env.local
```

### Check Claude Config

```bash
# View full config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# View just food-rag-system
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep -A 7 "food-rag-system"
```

### Check Network

```bash
# Test if port 3000 is accessible
nc -zv localhost 3000

# Check what's using port 3000
lsof -i:3000
```

---

## 📞 Still Having Issues?

### Collect Debug Info

Run these commands and share the output:

```bash
# 1. Server status
lsof -ti:3000

# 2. Endpoint test
curl -v http://localhost:3000/api/mcp 2>&1 | head -20

# 3. File check
ls -la /Users/DELL/ragfood/mydigitaltwin/src/app/api/mcp/

# 4. Config check
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep -A 10 "food-rag-system"

# 5. Environment check
grep -o '^[A-Z_]*=' /Users/DELL/ragfood/mydigitaltwin/.env.local
```

---

## ✅ Success Indicators

You know it's working when:

1. ✅ Terminal shows: `✓ Ready in XXXms` and no errors
2. ✅ `curl http://localhost:3000/api/mcp` returns JSON with `"status":"ok"`
3. ✅ Claude Desktop shows 🔌 icon or tools indicator
4. ✅ Typing "Using food-rag-system..." in Claude triggers the tool
5. ✅ Claude returns food-related information from your database

---

## 🎯 Quick Reference Commands

```bash
# Start server
cd /Users/DELL/ragfood/mydigitaltwin && ./start-mcp-server.sh

# Test server
curl http://localhost:3000/api/mcp

# Check if running
lsof -ti:3000

# Kill server
kill -9 $(lsof -ti:3000)

# View config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Clean restart
cd /Users/DELL/ragfood/mydigitaltwin && rm -rf .next && npm run dev
```

---

**Remember**: The #1 reason for disconnection is the server not running or being stopped. Always keep that terminal window open!

**Created**: October 31, 2025  
**For**: Food RAG MCP System v2.0
