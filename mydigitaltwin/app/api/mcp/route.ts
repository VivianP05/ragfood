import { NextRequest, NextResponse } from 'next/server';
import { queryFoodRAG, searchByCategory, getCacheStats } from '@/src/actions/foodRagActions';
import { 
  queryDigitalTwin, 
  getSkillInformation, 
  getWorkExperience, 
  getEducation, 
  getCertifications,
  getProjects 
} from '@/src/actions/digitalTwinActions';

/**
 * MCP Server Endpoint for Food RAG System + Digital Twin Profile
 * 
 * Provides tools for Claude Desktop to query:
 * - Food database (200+ food items)
 * - Vivian's professional profile (27 profile vectors)
 */

// Define MCP tools available to Claude
const MCP_TOOLS = [
  // === DIGITAL TWIN PROFILE TOOLS ===
  {
    name: "query_professional_profile",
    description: "Query Vivian Pham's professional profile, including skills, experience, education, certifications, and achievements. This is the primary tool for getting information about Vivian's background for job interviews, assessments, or professional inquiries.",
    inputSchema: {
      type: "object",
      properties: {
        question: {
          type: "string",
          description: "Question about Vivian's professional background (e.g., 'What are my Excel skills?', 'Tell me about my work experience', 'What certifications do I have?')"
        }
      },
      required: ["question"]
    }
  },
  {
    name: "get_skill_details",
    description: "Get detailed information about a specific skill (Excel, Power BI, Python, SQL, etc.) including proficiency level, achievements, and relevant experience.",
    inputSchema: {
      type: "object",
      properties: {
        skill: {
          type: "string",
          description: "Skill name (e.g., 'Excel', 'Power BI', 'Python', 'SQL', 'Data Analysis')"
        }
      },
      required: ["skill"]
    }
  },
  {
    name: "get_work_experience",
    description: "Get Vivian's work experience, employment history, roles, and responsibilities. Can filter by specific company if provided.",
    inputSchema: {
      type: "object",
      properties: {
        company: {
          type: "string",
          description: "Optional: specific company name to query (e.g., 'Ausbiz Consulting')"
        }
      }
    }
  },
  {
    name: "get_education",
    description: "Get Vivian's educational background, degrees, and academic qualifications.",
    inputSchema: {
      type: "object",
      properties: {}
    }
  },
  {
    name: "get_certifications",
    description: "Get all of Vivian's professional certifications and credentials.",
    inputSchema: {
      type: "object",
      properties: {}
    }
  },
  {
    name: "get_projects",
    description: "Get information about Vivian's key projects and achievements. Can filter by project type if provided.",
    inputSchema: {
      type: "object",
      properties: {
        projectType: {
          type: "string",
          description: "Optional: type of project (e.g., 'data visualization', 'automation', 'analysis')"
        }
      }
    }
  },

  // === FOOD RAG TOOLS ===
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
      case 'notifications/initialized':
        // Acknowledge initialization notification (no response needed)
        return NextResponse.json({
          jsonrpc: "2.0"
        });

      case 'tools/list':
        // Return list of available tools in proper JSON-RPC format
        return NextResponse.json({
          jsonrpc: "2.0",
          id: body.id,
          result: {
            tools: MCP_TOOLS
          }
        });

      case 'tools/call':
        // Execute tool based on name
        const { name, arguments: args } = params;

        // === DIGITAL TWIN PROFILE TOOLS ===
        if (name === 'query_professional_profile') {
          const { question } = args;
          const result = await queryDigitalTwin(question);
          
          const responseText = result.success 
            ? `${result.answer}\n\n📚 Sources: ${result.profile_vectors_found} profile vectors found\n${result.sources?.map((s, i) => `${i + 1}. ${s.name} (${s.section}) - Relevance: ${s.relevance}`).join('\n')}`
            : `Error: ${result.error}`;

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: responseText
                }
              ]
            }
          });
        }

        if (name === 'get_skill_details') {
          const { skill } = args;
          const result = await getSkillInformation(skill);
          
          const responseText = result.success 
            ? `${result.answer}\n\n📚 Sources: ${result.profile_vectors_found} profile vectors found`
            : `Error: ${result.error}`;

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: responseText
                }
              ]
            }
          });
        }

        if (name === 'get_work_experience') {
          const { company } = args;
          const result = await getWorkExperience(company);
          
          const responseText = result.success 
            ? `${result.answer}\n\n📚 Sources: ${result.profile_vectors_found} profile vectors found`
            : `Error: ${result.error}`;

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: responseText
                }
              ]
            }
          });
        }

        if (name === 'get_education') {
          const result = await getEducation();
          
          const responseText = result.success 
            ? `${result.answer}\n\n📚 Sources: ${result.profile_vectors_found} profile vectors found`
            : `Error: ${result.error}`;

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: responseText
                }
              ]
            }
          });
        }

        if (name === 'get_certifications') {
          const result = await getCertifications();
          
          const responseText = result.success 
            ? `${result.answer}\n\n📚 Sources: ${result.profile_vectors_found} profile vectors found`
            : `Error: ${result.error}`;

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: responseText
                }
              ]
            }
          });
        }

        if (name === 'get_projects') {
          const { projectType } = args;
          const result = await getProjects(projectType);
          
          const responseText = result.success 
            ? `${result.answer}\n\n📚 Sources: ${result.profile_vectors_found} profile vectors found`
            : `Error: ${result.error}`;

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: responseText
                }
              ]
            }
          });
        }

        // === FOOD RAG TOOLS ===
        if (name === 'query_food_database') {
          const { question } = args;
          const result = await queryFoodRAG(question);
          
          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: result.success ? result.answer : `Error: ${result.error}`
                }
              ]
            }
          });
        }

        if (name === 'search_by_category') {
          const { category, limit = 5 } = args;
          const result = await searchByCategory(category, limit);
          
          if (!result.success || !result.results) {
            return NextResponse.json({
              jsonrpc: "2.0",
              id: body.id,
              result: {
                content: [
                  {
                    type: "text",
                    text: `Error: ${result.error || 'No results found'}`
                  }
                ]
              }
            });
          }

          const formattedResults = result.results
            .map((item: any, index: number) => 
              `${index + 1}. **${item.name || 'Unknown'}**\n   ${item.description || item.text || 'No description'}\n   Category: ${item.category || item.type || 'N/A'}\n   Origin: ${item.origin || item.region || 'N/A'}`
            )
            .join('\n\n');

          return NextResponse.json({
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: `Found ${result.results.length} items in category "${category}":\n\n${formattedResults}`
                }
              ]
            }
          });
        }

        if (name === 'get_cache_statistics') {
          const stats = await getCacheStats();
          
          if (!stats.success || !stats.stats) {
            return NextResponse.json({
              jsonrpc: "2.0",
              id: body.id,
              result: {
                content: [
                  {
                    type: "text",
                    text: `Error: ${stats.error || 'Cache statistics unavailable'}`
                  }
                ]
              }
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
            jsonrpc: "2.0",
            id: body.id,
            result: {
              content: [
                {
                  type: "text",
                  text: statsText
                }
              ]
            }
          });
        }

        return NextResponse.json({
          jsonrpc: "2.0",
          id: body.id,
          error: {
            code: -32601,
            message: `Unknown tool: ${name}`
          }
        }, { status: 404 });

      case 'initialize':
        // Return server capabilities in proper JSON-RPC format
        return NextResponse.json({
          jsonrpc: "2.0",
          id: body.id,
          result: {
            protocolVersion: "2024-11-05",
            capabilities: {
              tools: {}
            },
            serverInfo: {
              name: "vivian-digital-twin-mcp",
              version: "3.0.0"
            }
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
    message: "Vivian's Digital Twin MCP Server is running",
    version: "3.0.0",
    capabilities: {
      digitalTwin: true,
      foodRAG: true
    },
    tools: MCP_TOOLS.length,
    toolCategories: {
      digitalTwin: 6,
      foodRAG: 3
    }
  });
}
