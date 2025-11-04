import { NextRequest, NextResponse } from 'next/server';
import { queryFoodRAG, searchByCategory, getCacheStats } from '@/src/actions/foodRagActions';

/**
 * MCP Server Endpoint for Food RAG System
 * 
 * Provides tools for Claude Desktop to query food database via Model Context Protocol
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
          
          if (!result.success || !result.results) {
            return NextResponse.json({
              content: [
                {
                  type: "text",
                  text: `Error: ${result.error || 'No results found'}`
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
          
          if (!stats.success || !stats.stats) {
            return NextResponse.json({
              content: [
                {
                  type: "text",
                  text: `Error: ${stats.error || 'Cache statistics unavailable'}`
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
- Average Accesses per Entry: ${stats.stats.avgAccessCount.toFixed(2)}

⚡ Performance:
- Pending Requests: ${stats.stats.pendingRequests}
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
