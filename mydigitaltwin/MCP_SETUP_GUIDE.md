# 🔌 MCP Server Setup Guide - Food RAG System

## Overview

This guide walks you through setting up your Food RAG System as a Model Context Protocol (MCP) server that Claude Desktop can connect to.

---

## Step 1: Claude Desktop Configuration (2 minutes)

### 1.1 Locate Claude Desktop Config

The configuration file location depends on your OS:

**macOS**:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux**:
```
~/.config/Claude/claude_desktop_config.json
```

### 1.2 Open Configuration File

For macOS:
```bash
# Open in VS Code
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use nano
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 1.3 Add MCP Server Configuration

Add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "food-rag-system": {
      "type": "http",
      "url": "http://localhost:3000/api/mcp",
      "timeout": 30000,
      "description": "Food RAG System - AI-powered food and cuisine knowledge base"
    }
  }
}
```

**If you already have other MCP servers configured**, add the `food-rag-system` entry to your existing `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      "type": "stdio",
      "command": "node",
      "args": ["path/to/server.js"]
    },
    "food-rag-system": {
      "type": "http",
      "url": "http://localhost:3000/api/mcp",
      "timeout": 30000,
      "description": "Food RAG System - AI-powered food and cuisine knowledge base"
    }
  }
}
```

### 1.4 Save and Restart Claude Desktop

1. Save the configuration file
2. Completely quit Claude Desktop (Cmd+Q on macOS)
3. Relaunch Claude Desktop

---

## Step 2: Create MCP Server Endpoint (5 minutes)

### 2.1 Create MCP API Route

Create the MCP server endpoint:

```bash
cd /Users/DELL/ragfood/mydigitaltwin
```

Create file: `src/app/api/mcp/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { queryFoodRAG, searchByCategory, getCacheStats } from '@/src/actions/foodRagActions';

/**
 * MCP Server Endpoint for Food RAG System
 * 
 * Provides tools for Claude Desktop to query food database
 */

// Define MCP tools available to Claude
const MCP_TOOLS = [
  {
    name: "query_food_database",
    description: "Search the food database for information about cuisines, dishes, ingredients, recipes, and dietary information. Returns AI-generated responses with context from 200+ food items.",
    inputSchema: {
      type: "object",
      properties: {
        question: {
          type: "string",
          description: "Question about food, cuisine, recipes, or dietary information (e.g., 'What is Biryani?', 'What are vegetarian Indian dishes?')"
        }
      },
      required: ["question"]
    }
  },
  {
    name: "search_by_category",
    description: "Search for food items by category. Categories include: Main Course, Dessert, Beverage, Appetizer, Snack, Condiment, Spice, Fruit, Vegetable, etc.",
    inputSchema: {
      type: "object",
      properties: {
        category: {
          type: "string",
          description: "Food category to search for"
        },
        limit: {
          type: "number",
          description: "Maximum number of results (default: 5)",
          default: 5
        }
      },
      required: ["category"]
    }
  },
  {
    name: "get_cache_statistics",
    description: "Get performance statistics about the Food RAG System cache, including cache size, hit rates, and performance metrics.",
    inputSchema: {
      type: "object",
      properties: {}
    }
  }
];

/**
 * POST /api/mcp
 * Handle MCP protocol requests from Claude Desktop
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { method, params } = body;

    // Handle MCP protocol methods
    switch (method) {
      case 'tools/list':
        // Return list of available tools
        return NextResponse.json({
          tools: MCP_TOOLS
        });

      case 'tools/call':
        // Execute tool based on name
        const { name, arguments: args } = params;

        if (name === 'query_food_database') {
          const { question } = args;
          const result = await queryFoodRAG(question);
          
          return NextResponse.json({
            content: [
              {
                type: "text",
                text: result.success ? result.answer : `Error: ${result.error}`
              }
            ]
          });
        }

        if (name === 'search_by_category') {
          const { category, limit = 5 } = args;
          const result = await searchByCategory(category, limit);
          
          if (!result.success) {
            return NextResponse.json({
              content: [
                {
                  type: "text",
                  text: `Error: ${result.error}`
                }
              ]
            });
          }

          const formattedResults = result.results
            .map((item: any, index: number) => 
              `${index + 1}. **${item.name || 'Unknown'}**\n   ${item.description || item.text || 'No description'}\n   Category: ${item.category || item.type || 'N/A'}\n   Origin: ${item.origin || item.region || 'N/A'}`
            )
            .join('\n\n');

          return NextResponse.json({
            content: [
              {
                type: "text",
                text: `Found ${result.results.length} items in category "${category}":\n\n${formattedResults}`
              }
            ]
          });
        }

        if (name === 'get_cache_statistics') {
          const stats = await getCacheStats();
          
          if (!stats.success) {
            return NextResponse.json({
              content: [
                {
                  type: "text",
                  text: `Error: ${stats.error}`
                }
              ]
            });
          }

          const statsText = `
**Food RAG System Cache Statistics**

📊 Cache Status:
- Size: ${stats.stats.size} / ${stats.stats.maxSize} entries
- Usage: ${((stats.stats.size / stats.stats.maxSize) * 100).toFixed(1)}%
- Total Accesses: ${stats.stats.totalAccesses}
- Average Accesses per Entry: ${stats.stats.averageAccessCount.toFixed(2)}

⚡ Performance:
- Cache Efficiency: ${(stats.stats.cacheEfficiency * 100).toFixed(1)}%
- Pending Requests: ${stats.stats.pendingRequests}

🔥 Top Cached Queries:
${stats.stats.topQueries.slice(0, 5).map((q: any, i: number) => 
  `${i + 1}. "${q.query}" (${q.accessCount} hits)`
).join('\n')}
          `.trim();

          return NextResponse.json({
            content: [
              {
                type: "text",
                text: statsText
              }
            ]
          });
        }

        return NextResponse.json({
          error: {
            code: "ToolNotFound",
            message: `Unknown tool: ${name}`
          }
        }, { status: 404 });

      case 'initialize':
        // Return server capabilities
        return NextResponse.json({
          protocolVersion: "2024-11-05",
          capabilities: {
            tools: {}
          },
          serverInfo: {
            name: "food-rag-system",
            version: "2.0.0"
          }
        });

      default:
        return NextResponse.json({
          error: {
            code: "MethodNotFound",
            message: `Unknown method: ${method}`
          }
        }, { status: 404 });
    }

  } catch (error) {
    console.error('MCP Server Error:', error);
    return NextResponse.json({
      error: {
        code: "InternalError",
        message: error instanceof Error ? error.message : "Unknown error"
      }
    }, { status: 500 });
  }
}

/**
 * GET /api/mcp
 * Health check endpoint
 */
export async function GET() {
  return NextResponse.json({
    status: "ok",
    message: "Food RAG MCP Server is running",
    version: "2.0.0",
    tools: MCP_TOOLS.length
  });
}
```

---

## Step 3: Start Your MCP Server (1 minute)

### 3.1 Start Development Server

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

Expected output:
```
> mydigitaltwin@0.1.0 dev
> next dev

  ▲ Next.js 16.0.1
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 2.1s
```

### 3.2 Verify MCP Endpoint

Test that the endpoint is working:

```bash
# Health check
curl http://localhost:3000/api/mcp

# Expected response:
# {"status":"ok","message":"Food RAG MCP Server is running","version":"2.0.0","tools":3}
```

---

## Step 4: Test in Claude Desktop (2 minutes)

### 4.1 Verify Connection

1. Open Claude Desktop
2. Look for the 🔌 icon or "Connected tools" indicator
3. You should see "food-rag-system" listed

### 4.2 Test Tool Usage

Try these prompts in Claude:

**Test 1: Query Food Database**
```
Using the food-rag-system tools, tell me about Biryani.
```

**Expected**: Detailed information about Biryani from your database

**Test 2: Search by Category**
```
Using the food-rag-system, show me Main Course dishes from the database.
```

**Expected**: List of main course items

**Test 3: Cache Statistics**
```
Using the food-rag-system, show me the current cache statistics.
```

**Expected**: Cache size, usage, efficiency, top queries

---

## Step 5: Advanced Usage (Optional)

### 5.1 Example Prompts

**Recipe Research**:
```
Using the food database, find vegetarian Indian dishes and suggest a 3-course meal.
```

**Dietary Information**:
```
Search the food database for vegan desserts and provide nutritional insights.
```

**Cuisine Exploration**:
```
Query the food database about South Indian cuisine and compare it with North Indian dishes.
```

**Performance Analysis**:
```
Check the cache statistics and analyze the most popular food queries.
```

### 5.2 MCP Tool Chaining

Claude can chain multiple tools together:

```
Using the food-rag-system:
1. Search for Dessert category items
2. For each dessert found, query detailed information
3. Create a dessert menu with descriptions
```

---

## Troubleshooting

### Issue: Claude Desktop Can't Connect

**Symptoms**:
- No tools showing in Claude
- "Connection failed" error

**Solutions**:

1. **Verify server is running**:
   ```bash
   curl http://localhost:3000/api/mcp
   ```

2. **Check config file syntax**:
   ```bash
   # Validate JSON
   python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Restart everything**:
   ```bash
   # Stop Next.js server (Ctrl+C)
   # Quit Claude Desktop (Cmd+Q)
   
   # Start Next.js
   npm run dev
   
   # Launch Claude Desktop
   ```

### Issue: Tools Not Appearing

**Symptoms**:
- Server connects but tools not available
- Empty tools list

**Solutions**:

1. **Check MCP endpoint**:
   ```bash
   curl -X POST http://localhost:3000/api/mcp \
     -H "Content-Type: application/json" \
     -d '{"method":"tools/list"}'
   ```

2. **Verify response includes tools array**

3. **Check Claude Desktop logs**:
   - macOS: `~/Library/Logs/Claude/`
   - Look for connection errors

### Issue: Tool Execution Fails

**Symptoms**:
- Tool shows but returns errors
- Timeout errors

**Solutions**:

1. **Check environment variables**:
   ```bash
   cat /Users/DELL/ragfood/mydigitaltwin/.env.local
   ```

2. **Test tool directly**:
   ```bash
   curl -X POST http://localhost:3000/api/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "method": "tools/call",
       "params": {
         "name": "query_food_database",
         "arguments": {"question": "What is Sushi?"}
       }
     }'
   ```

3. **Increase timeout in config**:
   ```json
   "timeout": 60000  // Increase to 60 seconds
   ```

---

## MCP Protocol Reference

### Request Format

```json
{
  "method": "tools/call",
  "params": {
    "name": "query_food_database",
    "arguments": {
      "question": "What is Biryani?"
    }
  }
}
```

### Response Format

```json
{
  "content": [
    {
      "type": "text",
      "text": "Biryani is a mixed rice dish..."
    }
  ]
}
```

### Available Methods

1. **initialize** - Initialize connection
2. **tools/list** - Get available tools
3. **tools/call** - Execute a tool

---

## Production Deployment

### Deploy MCP Server to Production

When deploying to Vercel, your MCP endpoint will be:

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

**Important**: Ensure your production URL is accessible and has proper CORS settings if needed.

---

## Security Considerations

### 1. Authentication (Optional)

Add API key authentication:

```typescript
// In /api/mcp/route.ts
const API_KEY = process.env.MCP_API_KEY;

export async function POST(request: NextRequest) {
  const authHeader = request.headers.get('Authorization');
  
  if (authHeader !== `Bearer ${API_KEY}`) {
    return NextResponse.json({
      error: { code: "Unauthorized", message: "Invalid API key" }
    }, { status: 401 });
  }
  
  // Continue with normal processing...
}
```

Update Claude config:

```json
{
  "mcpServers": {
    "food-rag-system": {
      "type": "http",
      "url": "http://localhost:3000/api/mcp",
      "headers": {
        "Authorization": "Bearer your-secret-key"
      }
    }
  }
}
```

### 2. Rate Limiting

Consider adding rate limiting for production:

```typescript
// Simple in-memory rate limiter
const requestCounts = new Map<string, number>();

function checkRateLimit(ip: string): boolean {
  const count = requestCounts.get(ip) || 0;
  if (count > 100) return false; // 100 requests per window
  
  requestCounts.set(ip, count + 1);
  return true;
}
```

---

## Next Steps

1. ✅ Configure Claude Desktop with MCP server
2. ✅ Create MCP API endpoint
3. ✅ Start development server
4. ✅ Test tools in Claude
5. 🚀 Deploy to production with Vercel
6. 📚 Share your MCP-enabled Food RAG System!

---

**Last Updated**: October 31, 2025  
**Version**: 2.0  
**Protocol**: MCP 2024-11-05
