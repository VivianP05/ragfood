# Food RAG MCP Server - Quick Reference

## 🚀 Quick Start Commands

```bash
# Web UI
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
# Visit: http://localhost:3000

# Build MCP Server
npm run build:mcp

# Run MCP Server (standalone)
npm run mcp
```

## 🔌 MCP Tools (Claude Desktop)

| Tool | Description | Example |
|------|-------------|---------|
| `query_food_database` | General food queries | "What is Biryani?" |
| `search_by_category` | Filter by category | "Show desserts" |
| `get_food_recommendations` | Personalized suggestions | "Vegetarian dishes" |
| `search_by_region` | Regional cuisines | "Foods from India" |

## 💻 Server Actions (TypeScript)

```typescript
import { queryFoodRAG, searchByCategory, getFoodRecommendations } from '@/src/actions/foodRagActions';

// General query
const result = await queryFoodRAG("What is Biryani?");
console.log(result.answer);

// Category search
const desserts = await searchByCategory("Dessert", 5);
console.log(desserts.results);

// Recommendations
const recs = await getFoodRecommendations("vegetarian and spicy");
console.log(recs.recommendations);
```

## 🔧 Claude Desktop Config

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "food-rag": {
      "command": "node",
      "args": ["/Users/DELL/ragfood/mydigitaltwin/dist/mcp-server/index.js"],
      "env": {
        "UPSTASH_VECTOR_REST_URL": "https://free-loon-62438-us1-vector.upstash.io",
        "UPSTASH_VECTOR_REST_TOKEN": "YOUR_TOKEN",
        "GROQ_API_KEY": "YOUR_KEY"
      }
    }
  }
}
```

Get credentials: `cat /Users/DELL/ragfood/.env`

## 📊 Your Database

- **Name:** free-loon-62438
- **Vectors:** 200 (110 food items)
- **Dimensions:** 1024
- **Model:** mxbai-embed-large-v1
- **AI:** llama-3.1-8b-instant

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/actions/foodRagActions.ts` | Server actions |
| `src/mcp-server/index.ts` | MCP server |
| `dist/mcp-server/index.js` | Compiled MCP |
| `app/api/query/route.ts` | API endpoint |
| `MCP_SERVER_SETUP.md` | Setup guide |
| `MCP_IMPLEMENTATION.md` | Full docs |

## 🐛 Troubleshooting

**Web UI not working?**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
rm -rf .next
npm run dev
```

**MCP server not building?**
```bash
rm -rf dist
npm run build:mcp
```

**Claude Desktop not seeing server?**
- Check config file path
- Validate JSON syntax
- Use absolute paths
- Restart Claude Desktop

## ✅ Test Checklist

- [ ] Web UI running at localhost:3000
- [ ] Can query "What is Biryani?"
- [ ] MCP server built successfully
- [ ] Claude Desktop configured
- [ ] Tested MCP tools in Claude
- [ ] Committed to git

## 🎯 Example Queries

```
"What is Biryani?"
"Recommend healthy breakfast"
"Show me tropical fruits"
"Tell me about Japanese cuisine"
"I want spicy vegetarian dishes"
"What desserts are available?"
```

---

**Built:** MCP Server + TypeScript Server Actions  
**Status:** ✅ Ready for testing  
**Next:** Test Web UI → Configure Claude Desktop → Enjoy! 🚀
