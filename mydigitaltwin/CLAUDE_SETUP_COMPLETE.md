# ✅ Claude Desktop MCP Setup - COMPLETE!

## What I Just Did For You

I've successfully configured your Claude Desktop to connect to your Food RAG System! Here's what was done:

---

## 1. ✅ Configuration Updated

**File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Added**:
```json
"food-rag-system": {
  "command": "npx",
  "args": [
    "-y",
    "mcp-remote",
    "http://localhost:3000/api/mcp"
  ]
}
```

**Backup created**: `claude_desktop_config.json.backup`

Your configuration now has **4 MCP servers**:
1. ✅ bootcamp-rag
2. ✅ tech-bootcamp-consultations
3. ✅ rolldice
4. ✅ **food-rag-system** (NEW!)

---

## 2. 🚀 Next Steps (Follow These!)

### Step 1: Start Your Server (IMPORTANT!)

Every time you want to use the Food RAG System with Claude, you need to have the server running:

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

**Keep this terminal open!** The server needs to be running for Claude to connect.

You should see:
```
✓ Ready in 800ms
- Local: http://localhost:3000
```

### Step 2: Restart Claude Desktop

This is **CRITICAL** - Claude needs to reload the configuration:

1. **Quit Claude Desktop completely**
   - Press `Cmd + Q` (don't just close the window!)
   - Make sure it's fully quit (check the Dock)

2. **Relaunch Claude Desktop**
   - Open it fresh from Applications

3. **Look for the 🔌 icon**
   - You should see a tools/plugins indicator
   - Or "Connected tools" somewhere in the interface

### Step 3: Test Your MCP Connection

In Claude Desktop, try one of these prompts:

**Test 1: Simple Query**
```
Using the food-rag-system tools, tell me about Biryani.
```

**Test 2: Category Search**
```
Using food-rag-system, search for Main Course items and show me 5 results.
```

**Test 3: Cache Statistics**
```
Using food-rag-system, show me the current cache statistics.
```

---

## 3. 🔧 Available Tools in Claude

Once connected, you'll have access to **3 powerful tools**:

### Tool 1: query_food_database
**What it does**: Ask any question about food, cuisines, recipes, dietary info

**Example prompts**:
- "Using food-rag-system, what are popular Indian desserts?"
- "Tell me about vegetarian dishes using the food database"
- "What ingredients are in Biryani?"

### Tool 2: search_by_category
**What it does**: Find food items by category

**Available categories**:
- Main Course
- Dessert
- Beverage
- Appetizer
- Snack
- Fruit
- Vegetable
- Spice
- Condiment

**Example prompts**:
- "Using food-rag-system, search for Dessert items"
- "Show me 10 Main Course dishes from the database"
- "Find all Spice items"

### Tool 3: get_cache_statistics
**What it does**: Show performance metrics and cache statistics

**Example prompts**:
- "Using food-rag-system, show cache statistics"
- "What are the top cached queries?"
- "How efficient is the cache?"

---

## 4. 🎯 Complete Workflow

Here's the complete process every time you want to use it:

```bash
# 1. Open Terminal
cd /Users/DELL/ragfood/mydigitaltwin

# 2. Start server
npm run dev

# 3. Leave terminal open (server must keep running)

# 4. In Claude Desktop, use prompts like:
#    "Using food-rag-system, tell me about Sushi"
```

---

## 5. 🔍 Troubleshooting

### Problem: "Tool not found" or tools don't appear

**Solution**:
1. Make sure server is running (`npm run dev`)
2. Quit Claude Desktop completely (Cmd+Q)
3. Relaunch Claude Desktop
4. Wait 10-20 seconds for connection

### Problem: Server won't start

**Solution**:
```bash
# Make sure you're in the right directory
cd /Users/DELL/ragfood/mydigitaltwin

# Check if something is using port 3000
lsof -ti:3000

# If yes, kill it
kill -9 $(lsof -ti:3000)

# Try starting again
npm run dev
```

### Problem: "Connection refused" error

**Solution**:
1. Verify server is running: `curl http://localhost:3000/api/mcp`
2. Should return: `{"status":"ok","message":"Food RAG MCP Server is running",...}`
3. If not, restart server

### Problem: Tools work but responses are slow

**Solution**:
- First query always takes ~1500-2000ms (normal - fetching from APIs)
- Cached queries should be <50ms
- Check your internet connection
- Verify Upstash and Groq API keys in `.env.local`

---

## 6. ✨ Pro Tips

### Tip 1: Keep Server Running
For best experience, keep the dev server running in a dedicated terminal window while working with Claude.

### Tip 2: Use Specific Prompts
Be explicit when using tools:
- ✅ "Using food-rag-system, tell me about..."
- ❌ "Tell me about..." (might not use the tool)

### Tip 3: Chain Queries
You can ask Claude to use multiple tools:
```
Using food-rag-system:
1. Search for Dessert items
2. For the first 3 results, get detailed information
3. Create a dessert menu with descriptions
```

### Tip 4: Check Cache Stats
Periodically check cache statistics to see which queries are popular and how efficient your system is.

---

## 7. 📊 Verify Installation

Run this checklist to make sure everything works:

- [ ] Server starts without errors
- [ ] `curl http://localhost:3000/api/mcp` returns OK status
- [ ] Claude Desktop shows 🔌 tools icon
- [ ] `food-rag-system` appears in tools list
- [ ] Test query returns food information
- [ ] Cache statistics work
- [ ] Category search works

---

## 8. 🎬 Example Session

Here's a complete example of using the Food RAG System with Claude:

**You**: "Using food-rag-system, tell me about Biryani"

**Claude**: *Uses query_food_database tool* → Returns detailed Biryani information

**You**: "Now search for other Main Course items"

**Claude**: *Uses search_by_category tool* → Returns list of main courses

**You**: "Show me the cache statistics"

**Claude**: *Uses get_cache_statistics tool* → Shows cache performance

---

## 9. 🚀 When You're Done

To stop the server:
1. Go to the terminal running `npm run dev`
2. Press `Ctrl + C`
3. Server will stop

To use again later:
1. Start server: `npm run dev`
2. Use Claude Desktop (no need to reconfigure!)

---

## 10. 📝 Your Configuration Files

For reference, these files were modified:

**Main config**:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Backup** (in case you need to restore):
```
~/Library/Application Support/Claude/claude_desktop_config.json.backup
```

**Server endpoint**:
```
http://localhost:3000/api/mcp
```

---

## 🎉 You're All Set!

Your Food RAG System is now integrated with Claude Desktop!

**Remember**:
1. ✅ Start server: `npm run dev`
2. ✅ Keep terminal open
3. ✅ Use in Claude: "Using food-rag-system, ..."

**Need help?**
- See `MCP_SETUP_GUIDE.md` for detailed troubleshooting
- See `COMPLETE_SETUP_SUMMARY.md` for full features overview

---

**Setup completed**: October 31, 2025  
**Server**: http://localhost:3000/api/mcp  
**Status**: ✅ Ready to use!
