# Food RAG MCP Server - Claude Desktop Configuration

## 🎯 Overview

This MCP server enables Claude Desktop to query your Food RAG system with 200+ food items using Upstash Vector database and Groq AI.

## 📋 Prerequisites

- ✅ Node.js 18+ installed
- ✅ Claude Desktop installed
- ✅ Environment variables configured in `.env.local`

## 🔧 Setup Instructions

### Step 1: Build the MCP Server

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run build:mcp
```

This compiles the TypeScript MCP server to JavaScript in the `dist/` folder.

### Step 2: Configure Claude Desktop

1. **Locate Claude Desktop config file:**

   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   
   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   
   **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Edit the config file** and add the Food RAG MCP server:

```json
{
  "mcpServers": {
    "food-rag": {
      "command": "node",
      "args": ["/Users/DELL/ragfood/mydigitaltwin/dist/mcp-server/index.js"],
      "env": {
        "UPSTASH_VECTOR_REST_URL": "https://free-loon-62438-us1-vector.upstash.io",
        "UPSTASH_VECTOR_REST_TOKEN": "your-upstash-token-here",
        "GROQ_API_KEY": "your-groq-api-key-here"
      }
    }
  }
}
```

3. **Replace the environment variables** with your actual credentials from `.env.local`

4. **Restart Claude Desktop** for changes to take effect

### Step 3: Verify Installation

1. Open Claude Desktop
2. Look for the 🔌 MCP icon in the interface
3. You should see "food-rag" listed as an available server
4. The server provides 4 tools:
   - `query_food_database` - Ask questions about food
   - `search_by_category` - Find foods by category
   - `get_food_recommendations` - Get personalized recommendations
   - `search_by_region` - Explore regional cuisines

## 🎮 Usage Examples

Once configured, you can ask Claude:

### General Food Queries
```
"Use the food database to tell me about Biryani"
"What are some popular Indian dishes?"
"Explain the ingredients in traditional Italian pasta"
```

### Category Search
```
"Search for desserts in the food database"
"Show me all the fruits available"
"List spices from the database"
```

### Recommendations
```
"Recommend some vegetarian dishes for me"
"I want spicy food suggestions"
"What are good healthy breakfast options?"
```

### Regional Exploration
```
"What foods are from India?"
"Show me tropical fruits"
"Tell me about Mediterranean cuisine"
```

## 🛠️ Available MCP Tools

### 1. query_food_database
**Purpose:** General RAG-powered food queries  
**Input:** Any question about food, cuisines, recipes, or dietary information  
**Output:** AI-generated response with relevant context from the database

### 2. search_by_category
**Purpose:** Filter foods by category  
**Input:** Category name (e.g., "Main Course", "Dessert", "Fruit")  
**Output:** List of food items in that category

### 3. get_food_recommendations
**Purpose:** Get personalized food suggestions  
**Input:** User preferences (dietary, flavor, cuisine type)  
**Output:** AI-generated recommendations matching preferences

### 4. search_by_region
**Purpose:** Explore foods from specific regions  
**Input:** Region/country name (e.g., "India", "Italy", "Tropical")  
**Output:** Foods from that region with descriptions

## 🔍 Technical Details

- **Database:** Upstash Vector `free-loon-62438`
- **Vectors:** 200 (110 food items + 90 other)
- **Dimensions:** 1024
- **Embedding Model:** mxbai-embed-large-v1
- **Similarity:** COSINE
- **AI Model:** Groq llama-3.1-8b-instant
- **Temperature:** 0.7 (for natural responses)
- **Max Tokens:** 500

## 📊 Database Schema

The food database contains items in two formats:

**Simple Format:**
```json
{
  "id": "1-90",
  "text": "Food description",
  "region": "Geographic origin",
  "type": "Category (Main Course, Fruit, etc.)"
}
```

**Detailed Format:**
```json
{
  "id": "91-110",
  "name": "Dish name",
  "category": "Food category",
  "origin": "Country/region",
  "description": "Detailed description",
  "ingredients": "List of ingredients",
  "cooking_method": "Preparation method",
  "dietary_tags": "Vegetarian, Vegan, etc."
}
```

## 🚀 Testing the MCP Server

### Test Standalone (Before Claude Desktop)

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run mcp
```

This starts the MCP server in stdio mode. It won't show a prompt, but it's running and ready for MCP client connections.

Press `Ctrl+C` to stop.

### Test via Claude Desktop

1. Open Claude Desktop
2. Start a new conversation
3. Try: "Use the food-rag tool to tell me about Biryani"
4. Claude will automatically use the MCP server

## 🐛 Troubleshooting

### Server not appearing in Claude Desktop

**Check:**
- Config file location is correct
- JSON syntax is valid (no trailing commas)
- File paths are absolute, not relative
- Claude Desktop was restarted after config changes

**Fix:**
```bash
# Verify config file exists
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Validate JSON
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Environment variable errors

**Error:** `Missing required environment variables`

**Fix:** Ensure all three variables are set in the config:
- `UPSTASH_VECTOR_REST_URL`
- `UPSTASH_VECTOR_REST_TOKEN`
- `GROQ_API_KEY`

Copy exact values from `/Users/DELL/ragfood/.env`

### Build errors

**Error:** TypeScript compilation fails

**Fix:**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
rm -rf dist
npm run build:mcp
```

### Connection timeout

**Error:** Server takes too long to respond

**Possible causes:**
- Upstash database is slow (rare)
- Groq API rate limit reached
- Network connectivity issues

**Fix:** Wait a moment and try again. Check Groq dashboard for rate limits.

## 📝 Server Logs

The MCP server logs to stderr (visible in Claude Desktop logs):

```
🚀 Starting Food RAG MCP Server...
📊 Database: free-loon-62438 (200 food vectors)
🤖 AI Model: llama-3.1-8b-instant (Groq)
🔧 Tools available: 4

✅ Server ready for connections
```

When processing requests:
```
🔍 Searching food database for: What is Biryani?
✅ Found 3 relevant food items
🤖 Generating AI response with Groq...
✨ Response generated successfully
```

## 🔐 Security Notes

- ✅ Never commit the Claude Desktop config with real API keys
- ✅ Environment variables are isolated to the MCP server process
- ✅ The server runs locally, not exposed to the internet
- ✅ Only Claude Desktop can communicate with the server

## 🔄 Updating the Server

After making changes to the MCP server code:

```bash
# 1. Rebuild the server
npm run build:mcp

# 2. Restart Claude Desktop
# (No need to change the config file)
```

## 📚 Additional Resources

- **MCP Documentation:** https://modelcontextprotocol.io/
- **Upstash Docs:** https://upstash.com/docs/vector
- **Groq API:** https://console.groq.com/docs
- **Project Documentation:** See `agents.md` in project root

## ✅ Next Steps

1. ✅ Build the MCP server: `npm run build:mcp`
2. ✅ Configure Claude Desktop with your credentials
3. ✅ Restart Claude Desktop
4. ✅ Test with: "Tell me about Biryani using the food database"
5. ✅ Explore all 4 MCP tools!

---

**Server Status:** Ready for Claude Desktop integration 🚀
