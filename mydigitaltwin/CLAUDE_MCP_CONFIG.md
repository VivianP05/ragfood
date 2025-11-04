# 🔌 Claude Desktop MCP Configuration

## Quick Setup (2 minutes)

### 1. Configure Claude Desktop

**Edit this file**:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Add this configuration**:
```json
{
  "mcpServers": {
    "food-rag-system": {
      "type": "http",
      "url": "http://localhost:3000/api/mcp",
      "timeout": 30000,
      "description": "Food RAG System - AI-powered food and cuisine knowledge base with 200+ items"
    }
  }
}
```

### 2. Start Your Server

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

### 3. Restart Claude Desktop

- Quit Claude (Cmd+Q)
- Relaunch Claude Desktop
- Look for 🔌 icon or "Connected tools"

### 4. Test It!

Try these prompts in Claude:

```
Using food-rag-system tools, tell me about Biryani.
```

```
Search the food database for Main Course dishes.
```

```
Show me the cache statistics from the food system.
```

---

## Available Tools

### 1. query_food_database
Ask questions about food, cuisines, recipes, dietary info

**Example**:
```
Using food-rag-system, what are popular Indian desserts?
```

### 2. search_by_category  
Find food items by category

**Categories**: Main Course, Dessert, Beverage, Appetizer, Snack, Fruit, Vegetable, Spice

**Example**:
```
Using food-rag-system, search for Dessert items and show me 5 results.
```

### 3. get_cache_statistics
View performance stats and top queries

**Example**:
```
Using food-rag-system, show me the current cache statistics.
```

---

## Troubleshooting

### Can't connect?

1. **Check server is running**:
   ```bash
   curl http://localhost:3000/api/mcp
   # Should return: {"status":"ok",...}
   ```

2. **Verify config syntax**:
   ```bash
   python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Restart everything**:
   - Stop Next.js (Ctrl+C)
   - Quit Claude Desktop (Cmd+Q)
   - Start Next.js: `npm run dev`
   - Launch Claude Desktop

### Tools not showing?

- Make sure server shows "Ready" in terminal
- Check for 🔌 icon in Claude
- Try closing and reopening chat
- Restart Claude Desktop

---

## Production Deployment

When deployed to Vercel, update config:

```json
{
  "mcpServers": {
    "food-rag-system": {
      "type": "http",
      "url": "https://your-app.vercel.app/api/mcp",
      "timeout": 30000
    }
  }
}
```

---

**For full setup guide, see**: `MCP_SETUP_GUIDE.md`

**Server status**: http://localhost:3000/api/mcp
