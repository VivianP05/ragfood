# 🎯 VISUAL STEP-BY-STEP GUIDE

## The Problem
Claude says "food-rag-system disconnected" because the server isn't running continuously.

## The Solution (4 Simple Steps)

---

### ✅ STEP 1: Open a REAL Terminal

**macOS:**
1. Press `Cmd + Space` (opens Spotlight)
2. Type: `Terminal`
3. Press `Enter`

OR

- Click Launchpad
- Search for "Terminal"
- Click it

**You should see a new window that looks like:**
```
DELL@mac ~ %
```

---

### ✅ STEP 2: Copy & Paste This Command

In that terminal window, paste this EXACT command:

```bash
cd /Users/DELL/ragfood/mydigitaltwin && npm run dev
```

**How to paste in Terminal:**
- `Cmd + V` or right-click → Paste

Then press `Enter`

---

### ✅ STEP 3: Wait for Success Message

You should see output like this:

```
> mydigitaltwin@0.1.0 dev
> next dev

 ⚠ Warning: Next.js inferred your workspace root...
 
   ▲ Next.js 16.0.1 (Turbopack)
   - Local:        http://localhost:3000
   - Network:      http://192.168.87.21:3000
   - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 819ms    <---- LOOK FOR THIS!
```

**When you see `✓ Ready in XXXms`** → SUCCESS! ✅

---

### ✅ STEP 4: LEAVE THIS TERMINAL OPEN!

**⚠️ CRITICAL: DO NOT CLOSE THIS WINDOW!**

What you CAN do:
- ✅ Minimize it (`Cmd + M`)
- ✅ Move it to another desktop space
- ✅ Hide it (`Cmd + H`)

What you CANNOT do:
- ❌ Close the window (`Cmd + W`)
- ❌ Quit Terminal (`Cmd + Q`)
- ❌ Press `Ctrl + C` in that window

**This terminal MUST stay open as long as you want to use the Food RAG System with Claude!**

---

## 🧪 VERIFY IT'S WORKING

### Test 1: Check the Endpoint

Open a **NEW** terminal window (don't close the first one!) and run:

```bash
curl http://localhost:3000/api/mcp
```

**Expected output:**
```json
{"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}
```

✅ If you see this → Your server is working!
❌ If you see "Connection refused" → Go back to Step 1

---

### Test 2: Check in Claude Desktop

1. **Wait 20-30 seconds** (Claude needs time to detect the server)

2. Look for the 🔌 icon or "Connected tools" indicator

3. Type this in Claude:
   ```
   Using food-rag-system tools, tell me about Biryani.
   ```

4. Claude should respond with information about Biryani from your database

✅ If Claude responds → IT'S WORKING! 🎉
❌ If Claude says "disconnected" → Restart Claude Desktop (Cmd+Q, then reopen)

---

## 📊 Visual Diagram

```
┌─────────────────────────────────────────┐
│  Terminal Window #1                     │
│  (Keep this OPEN!)                      │
│                                         │
│  DELL@mac mydigitaltwin % npm run dev   │
│  ✓ Ready in 819ms                       │
│  Server running at localhost:3000       │
│                                         │
│  ⚠️ DO NOT CLOSE THIS WINDOW            │
└─────────────────────────────────────────┘
           │
           │ Server running
           ▼
┌─────────────────────────────────────────┐
│  Claude Desktop                         │
│                                         │
│  🔌 Connected to food-rag-system        │
│                                         │
│  > Using food-rag-system, tell me      │
│    about Biryani.                       │
│                                         │
│  ✓ Response received!                   │
└─────────────────────────────────────────┘
```

---

## ❓ TROUBLESHOOTING

### "Port 3000 is already in use"

Something else is using port 3000. Fix it:

```bash
# Find what's using port 3000
lsof -ti:3000

# Kill it (replace XXXX with the number from above)
kill -9 XXXX

# Try starting server again
cd /Users/DELL/ragfood/mydigitaltwin && npm run dev
```

---

### "Could not read package.json"

You're in the wrong directory. Make sure you run:

```bash
cd /Users/DELL/ragfood/mydigitaltwin && npm run dev
```

NOT just:
```bash
npm run dev
```

The `cd` part is critical!

---

### "Connection refused" when testing

Server isn't running. Go back to Step 1 and start it.

---

### Claude still says "disconnected"

1. Make sure server is running (check Terminal #1)
2. Test endpoint: `curl http://localhost:3000/api/mcp`
3. Quit Claude Desktop completely (`Cmd + Q`)
4. Wait 5 seconds
5. Reopen Claude Desktop
6. Wait 20 seconds
7. Try again

---

## 🎯 QUICK CHECKLIST

Before using Claude with food-rag-system:

- [ ] Terminal window is open with `npm run dev` running
- [ ] You see `✓ Ready in XXXms` in that terminal
- [ ] Terminal is still open (not closed)
- [ ] `curl http://localhost:3000/api/mcp` returns `{"status":"ok"...}`
- [ ] Claude Desktop is running
- [ ] Waited at least 20 seconds after starting server

If all checkboxes are ✅ → It should work!

---

## 💡 REMEMBER

**Think of it like this:**

The MCP server is like a bridge between Claude and your Food RAG database.

```
Claude Desktop  ←→  MCP Server  ←→  Food Database
                (must be running!)
```

If the server (bridge) isn't running, Claude can't connect to your database.

**That's why the terminal must stay open!**

---

## 🚀 YOU'RE READY!

1. Open Terminal
2. Run: `cd /Users/DELL/ragfood/mydigitaltwin && npm run dev`
3. See: `✓ Ready in XXXms`
4. Leave it open
5. Use Claude!

**IT'S THAT SIMPLE!** 🎉

---

**Need more help?** Check:
- `URGENT_FIX.md` - Quick fix guide
- `MCP_TROUBLESHOOTING.md` - Detailed troubleshooting
- `CLAUDE_SETUP_COMPLETE.md` - Full setup guide
