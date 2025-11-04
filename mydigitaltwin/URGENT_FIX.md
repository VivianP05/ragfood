# 🚨 QUICK FIX - RUN THIS NOW!

## The problem is that the server needs to stay running. Here's the exact fix:

### **COPY AND PASTE THIS INTO YOUR TERMINAL:**

```bash
cd /Users/DELL/ragfood/mydigitaltwin && npm run dev
```

### **IMPORTANT:**
1. ✅ Open a NEW terminal window (don't use this one!)
2. ✅ Paste the command above
3. ✅ Press Enter
4. ✅ Wait until you see: `✓ Ready in XXXms`
5. ⚠️ **LEAVE THAT TERMINAL OPEN** - Don't close it!

---

## **Then test it works:**

Open ANOTHER terminal window and run:

```bash
curl http://localhost:3000/api/mcp
```

You should see:
```json
{"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}
```

---

## **Then in Claude Desktop:**

Wait 10-20 seconds, then type:

```
Using food-rag-system tools, tell me about Biryani.
```

---

## ⚠️ **WHY THIS KEEPS HAPPENING:**

The automated terminal keeps changing directories back to `/Users/DELL/ragfood` instead of staying in `/Users/DELL/ragfood/mydigitaltwin`.

**SOLUTION**: You need to manually open a terminal and run the command yourself.

---

## 📝 **STEP-BY-STEP (DO THIS NOW):**

### 1. Open Terminal (the real one, not VS Code terminal)
- Press `Cmd + Space`
- Type "Terminal"
- Press Enter

### 2. Copy and paste this EXACT command:
```bash
cd /Users/DELL/ragfood/mydigitaltwin && npm run dev
```

### 3. You'll see this output:
```
> mydigitaltwin@0.1.0 dev
> next dev

   ▲ Next.js 16.0.1 (Turbopack)
   - Local:        http://localhost:3000

 ✓ Starting...
 ✓ Ready in 800ms
```

### 4. STOP! Don't do anything else in this terminal
- This is your MCP server
- It MUST stay running
- Minimize the window (don't close it!)

### 5. To test, open a NEW terminal and run:
```bash
curl http://localhost:3000/api/mcp
```

### 6. Go to Claude Desktop and wait 20 seconds
- The 🔌 icon should appear
- Try: "Using food-rag-system, tell me about Biryani"

---

## 🎯 **THE KEY RULE:**

**One terminal running `npm run dev` = Claude can connect**

**No terminal running = Claude disconnects**

---

## ✅ **Checklist:**

- [ ] Opened real Terminal app (not VS Code)
- [ ] Ran: `cd /Users/DELL/ragfood/mydigitaltwin && npm run dev`
- [ ] Saw: `✓ Ready in XXXms`
- [ ] Left terminal open (minimized is fine)
- [ ] Tested: `curl http://localhost:3000/api/mcp` (in a different terminal)
- [ ] Got response: `{"status":"ok",...}`
- [ ] Waited 20 seconds
- [ ] Tried in Claude: "Using food-rag-system..."

---

**DO THIS NOW and it will work!** The issue is just that you need to manually keep a terminal running with the server. 🚀
