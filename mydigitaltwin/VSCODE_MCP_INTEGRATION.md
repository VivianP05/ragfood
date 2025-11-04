# 🚀 VS Code MCP Integration Guide

## ⚠️ Important: Current Setup Status

### Your Current Configuration:
- ✅ **MCP Server**: Running on http://localhost:3000/api/mcp
- ✅ **Claude Desktop Integration**: Configured
- ⚠️ **VS Code MCP Integration**: Newly created (requires VS Code Insiders)

---

## 📋 What's the Difference?

### Claude Desktop MCP (Currently Working)
**Config**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "food-rag-system": {
    "command": "npx",
    "args": ["-y", "mcp-remote", "http://localhost:3000/api/mcp"]
  }
}
```

**How to use**:
1. Start server: `npm run dev`
2. Launch Claude Desktop
3. Server connects automatically

---

### VS Code MCP Integration (Just Created)
**Config**: `.vscode/mcp.json`

```json
{
  "food-rag-system": {
    "command": "npm",
    "args": ["run", "dev"],
    "cwd": "${workspaceFolder}",
    "env": {
      "NODE_ENV": "development"
    },
    "description": "Food RAG System MCP Server"
  }
}
```

**Requirements**:
- VS Code Insiders (not regular VS Code)
- MCP extension installed

---

## 🔧 Step 3: Start MCP Server with VS Code Monitoring

### Prerequisites:
1. **Install VS Code Insiders**:
   - Download: https://code.visualstudio.com/insiders/
   - Or via Homebrew: `brew install --cask visual-studio-code-insiders`

2. **Install MCP Extension** (if available):
   - Open VS Code Insiders
   - Go to Extensions (Cmd+Shift+X)
   - Search for "MCP" or "Model Context Protocol"
   - Install the extension

---

### Method 1: VS Code Insiders MCP Controls (New)

**Step-by-Step**:

1. **Open Project in VS Code Insiders**:
   ```bash
   code-insiders /Users/DELL/ragfood/mydigitaltwin
   ```

2. **Open `.vscode/mcp.json`**:
   - File is located at: `/Users/DELL/ragfood/mydigitaltwin/.vscode/mcp.json`
   - You should see the MCP server configuration

3. **Start Server**:
   - Look for a "Start" button/link next to the server configuration
   - Click "Start" to launch the MCP server
   - VS Code will open the Output tab automatically

4. **Monitor Logs**:
   - Output tab will show server startup logs
   - Look for: `✓ Ready in XXXms`
   - MCP endpoint: http://localhost:3000/api/mcp

---

### Method 2: Manual Start with Terminal Monitoring (Currently Working)

**If VS Code Insiders isn't available, use this method**:

1. **Open Terminal in VS Code**:
   ```
   Terminal → New Terminal (Ctrl+`)
   ```

2. **Start Server**:
   ```bash
   npm run dev
   ```

3. **Watch Output**:
   ```
   ▲ Next.js 16.0.1 (Turbopack)
   - Local:        http://localhost:3000
   
   ✓ Starting...
   ✓ Ready in XXXms
   ```

4. **Test MCP Endpoint**:
   ```bash
   curl http://localhost:3000/api/mcp
   ```

   **Expected**:
   ```json
   {
     "status": "ok",
     "message": "Food RAG MCP Server is running",
     "version": "2.0.0",
     "tools": 3
   }
   ```

---

### Method 3: Background Monitoring (Advanced)

**Start server with detailed logging**:

```bash
cd /Users/DELL/ragfood/mydigitaltwin

# Start with verbose output
npm run dev 2>&1 | tee server.log
```

This will:
- Start the development server
- Display output in terminal
- Save logs to `server.log` file

---

## 🔍 Monitoring Your MCP Server

### Real-Time Health Checks

**1. MCP Endpoint**:
```bash
curl http://localhost:3000/api/mcp
```

**2. Main Application**:
```bash
curl http://localhost:3000
```

**3. Dashboard**:
```bash
open http://localhost:3000/dashboard
```

**4. Check Running Process**:
```bash
lsof -ti:3000
```

---

### Log Monitoring

**Watch server logs** (if using background mode):
```bash
tail -f /tmp/nextjs.log
```

**Check Claude Desktop MCP logs**:
```bash
tail -f ~/Library/Logs/Claude/mcp-server-food-rag-system.log
```

---

## 📊 Expected Output

### Successful Startup:
```
> mydigitaltwin@0.1.0 dev
> next dev

▲ Next.js 16.0.1 (Turbopack)
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000
- Environments: .env.local

✓ Starting...
✓ Ready in 605ms
```

### MCP Health Check Response:
```json
{
  "status": "ok",
  "message": "Food RAG MCP Server is running",
  "version": "2.0.0",
  "tools": 3
}
```

---

## ✅ Verification Checklist

After starting the server, verify:

- [ ] Server shows `✓ Ready in XXXms`
- [ ] Port 3000 is in use: `lsof -ti:3000`
- [ ] MCP endpoint responds: `curl http://localhost:3000/api/mcp`
- [ ] Main app loads: http://localhost:3000
- [ ] Dashboard accessible: http://localhost:3000/dashboard
- [ ] No errors in terminal output

---

## 🐛 Troubleshooting

### VS Code Insiders Not Showing MCP Controls

**Possible reasons**:
1. VS Code Insiders not installed
2. MCP extension not available yet
3. `.vscode/mcp.json` format incorrect

**Solution**: Use Method 2 (Manual Start) instead

---

### Port 3000 Already in Use

```bash
# Kill existing process
lsof -ti:3000 | xargs kill -9

# Restart
npm run dev
```

---

### Server Starts but MCP Endpoint 404

**Check route file exists**:
```bash
ls -la /Users/DELL/ragfood/mydigitaltwin/app/api/mcp/route.ts
```

**Should show**: 250-line TypeScript file

---

## 🎯 Current Status

### ✅ What's Working Now:
- Development server: **RUNNING** on port 3000
- MCP endpoint: **OPERATIONAL** at http://localhost:3000/api/mcp
- 3 MCP tools: **AVAILABLE**
- Claude Desktop config: **READY**

### 🆕 What's New:
- `.vscode/mcp.json` created for VS Code Insiders integration
- Ready for VS Code MCP controls when available

---

## 📚 Next Steps

### Option A: Use VS Code Insiders (Recommended if available)
1. Install VS Code Insiders
2. Open project in Insiders
3. Use built-in MCP controls
4. Monitor via Output tab

### Option B: Use Current Terminal Method (Working Now)
1. Keep using `npm run dev`
2. Monitor terminal output
3. Test with curl commands
4. Use Claude Desktop for MCP integration

### Option C: Use Both
1. Start server with VS Code Insiders MCP controls
2. Monitor logs in VS Code Output tab
3. Connect Claude Desktop to the running server
4. Best of both worlds!

---

## 🔗 Quick Reference

**Start Server**:
```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

**Test MCP**:
```bash
curl http://localhost:3000/api/mcp
```

**View Logs**:
```bash
# VS Code: View → Output → Select "Tasks" or server name
# Terminal: Watch the npm run dev output
# Claude Desktop: ~/Library/Logs/Claude/mcp-server-food-rag-system.log
```

---

**Created**: October 31, 2025  
**Status**: Ready for VS Code Insiders or Terminal monitoring  
**Server**: http://localhost:3000/api/mcp
