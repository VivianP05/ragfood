#!/usr/bin/env node

/**
 * Food RAG MCP Server
 * 
 * Model Context Protocol server for food queries using RAG
 * with Upstash Vector database and Groq AI
 * 
 * Usage:
 * - Standalone: node dist/mcp-server/index.js
 * - Claude Desktop: Configure in claude_desktop_config.json
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { Index } from "@upstash/vector";
import Groq from "groq-sdk";

// Environment variables validation
const UPSTASH_URL = process.env.UPSTASH_VECTOR_REST_URL;
const UPSTASH_TOKEN = process.env.UPSTASH_VECTOR_REST_TOKEN;
const GROQ_API_KEY = process.env.GROQ_API_KEY;

if (!UPSTASH_URL || !UPSTASH_TOKEN || !GROQ_API_KEY) {
  console.error("❌ Missing required environment variables:");
  if (!UPSTASH_URL) console.error("  - UPSTASH_VECTOR_REST_URL");
  if (!UPSTASH_TOKEN) console.error("  - UPSTASH_VECTOR_REST_TOKEN");
  if (!GROQ_API_KEY) console.error("  - GROQ_API_KEY");
  process.exit(1);
}

// Initialize Upstash Vector Index
const index = new Index({
  url: UPSTASH_URL,
  token: UPSTASH_TOKEN,
});

// Initialize Groq client
const groq = new Groq({
  apiKey: GROQ_API_KEY,
});

// Create MCP server
const server = new Server(
  {
    name: "food-rag-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
const TOOLS: Tool[] = [
  {
    name: "query_food_database",
    description:
      "Query the food database using RAG (Retrieval-Augmented Generation). Searches 200+ food items including cuisines, dishes, recipes, ingredients, and dietary information. Returns AI-generated responses with relevant food context.",
    inputSchema: {
      type: "object",
      properties: {
        question: {
          type: "string",
          description:
            "Question about food, cuisines, recipes, ingredients, or dietary information. Examples: 'What is Biryani?', 'Tell me about vegetarian dishes', 'What are tropical fruits?'",
        },
      },
      required: ["question"],
    },
  },
  {
    name: "search_by_category",
    description:
      "Search food items by category. Categories include: Main Course, Dessert, Fruit, Spice, Beverage, Snack, etc. Returns a list of food items in the specified category.",
    inputSchema: {
      type: "object",
      properties: {
        category: {
          type: "string",
          description: "Food category to search for (e.g., 'Main Course', 'Dessert', 'Fruit')",
        },
        limit: {
          type: "number",
          description: "Maximum number of results to return (default: 5)",
          default: 5,
        },
      },
      required: ["category"],
    },
  },
  {
    name: "get_food_recommendations",
    description:
      "Get personalized food recommendations based on preferences. Preferences can include dietary restrictions (vegetarian, vegan), flavor profiles (spicy, sweet), cuisine types (Indian, Italian), or meal types (quick, healthy).",
    inputSchema: {
      type: "object",
      properties: {
        preferences: {
          type: "string",
          description:
            "User preferences for food recommendations (e.g., 'vegetarian and spicy', 'healthy breakfast options', 'traditional Indian desserts')",
        },
      },
      required: ["preferences"],
    },
  },
  {
    name: "search_by_region",
    description:
      "Search for foods from a specific region or country. Explores regional cuisines and traditional dishes.",
    inputSchema: {
      type: "object",
      properties: {
        region: {
          type: "string",
          description: "Region or country name (e.g., 'India', 'Italy', 'Tropical', 'Mediterranean')",
        },
        limit: {
          type: "number",
          description: "Maximum number of results to return (default: 5)",
          default: 5,
        },
      },
      required: ["region"],
    },
  },
];

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: TOOLS,
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "query_food_database":
        return await handleQueryFoodDatabase(args);
      
      case "search_by_category":
        return await handleSearchByCategory(args);
      
      case "get_food_recommendations":
        return await handleGetRecommendations(args);
      
      case "search_by_region":
        return await handleSearchByRegion(args);
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "Unknown error";
    return {
      content: [
        {
          type: "text",
          text: `Error: ${errorMessage}`,
        },
      ],
      isError: true,
    };
  }
});

/**
 * Handle query_food_database tool
 */
async function handleQueryFoodDatabase(args: any) {
  const question = args.question as string;

  if (!question || question.trim().length === 0) {
    throw new Error("Question cannot be empty");
  }

  console.error(`🔍 Searching food database for: ${question}`);

  // Search Upstash Vector
  const results = await index.query({
    data: question,
    topK: 3,
    includeMetadata: true,
  });

  console.error(`✅ Found ${results.length} relevant food items`);

  // Build context
  const contextItems: string[] = [];
  
  results.forEach((result, idx) => {
    const metadata = result.metadata as Record<string, any>;
    
    let foodInfo: string;
    
    if (metadata.name) {
      // Detailed format
      foodInfo = `${metadata.name}: ${metadata.description || ""}`;
      if (metadata.origin) foodInfo += ` (Origin: ${metadata.origin})`;
      if (metadata.category) foodInfo += ` [${metadata.category}]`;
      if (metadata.ingredients) foodInfo += `\nIngredients: ${metadata.ingredients}`;
      if (metadata.cooking_method) foodInfo += `\nPreparation: ${metadata.cooking_method}`;
      if (metadata.dietary_tags) foodInfo += `\nDietary: ${metadata.dietary_tags}`;
    } else {
      // Simple format
      foodInfo = metadata.text || "";
      if (metadata.region) foodInfo += ` (${metadata.region})`;
      if (metadata.type) foodInfo += ` [${metadata.type}]`;
    }
    
    contextItems.push(foodInfo);
  });

  const context = contextItems.join("\n\n");

  console.error("🤖 Generating AI response with Groq...");

  // Generate response with Groq
  const completion = await groq.chat.completions.create({
    messages: [
      {
        role: "system",
        content: `You are a helpful food expert assistant with deep knowledge of global cuisines, dishes, recipes, and dietary information. 

Use the provided food database context to answer questions accurately and enthusiastically. Include details about:
- Origins and cultural significance
- Key ingredients and flavors
- Preparation methods
- Dietary considerations
- Regional variations

Be conversational, informative, and encouraging.`,
      },
      {
        role: "user",
        content: `Food Database Context:\n${context}\n\nQuestion: ${question}`,
      },
    ],
    model: "llama-3.1-8b-instant",
    temperature: 0.7,
    max_tokens: 500,
  });

  const answer = completion.choices[0]?.message?.content || "No response generated.";

  console.error("✨ Response generated successfully");

  return {
    content: [
      {
        type: "text",
        text: answer,
      },
    ],
  };
}

/**
 * Handle search_by_category tool
 */
async function handleSearchByCategory(args: any) {
  const category = args.category as string;
  const limit = (args.limit as number) || 5;

  console.error(`🔍 Searching for ${category} items...`);

  const results = await index.query({
    data: `${category} food items`,
    topK: limit,
    includeMetadata: true,
  });

  const foodItems = results.map((result, idx) => {
    const metadata = result.metadata as Record<string, any>;
    const name = metadata.name || metadata.text || "Unknown";
    const description = metadata.description || metadata.text || "";
    const region = metadata.region || metadata.origin || "Unknown";
    const type = metadata.type || metadata.category || category;
    
    return `${idx + 1}. **${name}** (${region}) - ${type}\n   ${description.substring(0, 150)}${description.length > 150 ? "..." : ""}`;
  }).join("\n\n");

  return {
    content: [
      {
        type: "text",
        text: `Found ${results.length} ${category} items:\n\n${foodItems}`,
      },
    ],
  };
}

/**
 * Handle get_food_recommendations tool
 */
async function handleGetRecommendations(args: any) {
  const preferences = args.preferences as string;

  console.error(`🔍 Finding recommendations for: ${preferences}`);

  const results = await index.query({
    data: preferences,
    topK: 5,
    includeMetadata: true,
  });

  const foodList = results
    .map((r, idx) => {
      const metadata = r.metadata as Record<string, any>;
      const name = metadata.name || metadata.text;
      const desc = metadata.description || "";
      return `${idx + 1}. ${name}${desc ? `: ${desc}` : ""}`;
    })
    .join("\n");

  const completion = await groq.chat.completions.create({
    messages: [
      {
        role: "system",
        content:
          "You are a food recommendation expert. Provide personalized, enthusiastic recommendations based on user preferences.",
      },
      {
        role: "user",
        content: `User preferences: ${preferences}\n\nRelevant foods from our database:\n${foodList}\n\nProvide 3-5 personalized recommendations with brief explanations why they match the preferences.`,
      },
    ],
    model: "llama-3.1-8b-instant",
    temperature: 0.8,
    max_tokens: 400,
  });

  const recommendations = completion.choices[0]?.message?.content || "No recommendations generated.";

  return {
    content: [
      {
        type: "text",
        text: recommendations,
      },
    ],
  };
}

/**
 * Handle search_by_region tool
 */
async function handleSearchByRegion(args: any) {
  const region = args.region as string;
  const limit = (args.limit as number) || 5;

  console.error(`🔍 Searching for foods from ${region}...`);

  const results = await index.query({
    data: `${region} food cuisine dishes`,
    topK: limit,
    includeMetadata: true,
  });

  const foodItems = results.map((result, idx) => {
    const metadata = result.metadata as Record<string, any>;
    const name = metadata.name || metadata.text || "Unknown";
    const description = metadata.description || metadata.text || "";
    const origin = metadata.region || metadata.origin || region;
    
    return `${idx + 1}. **${name}** from ${origin}\n   ${description.substring(0, 150)}${description.length > 150 ? "..." : ""}`;
  }).join("\n\n");

  return {
    content: [
      {
        type: "text",
        text: `Foods from ${region}:\n\n${foodItems}`,
      },
    ],
  };
}

/**
 * Start the MCP server
 */
async function main() {
  console.error("🚀 Starting Food RAG MCP Server...");
  console.error("📊 Database: free-loon-62438 (200 food vectors)");
  console.error("🤖 AI Model: llama-3.1-8b-instant (Groq)");
  console.error("🔧 Tools available: 4");
  console.error("");
  console.error("✅ Server ready for connections");

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("❌ Fatal error:", error);
  process.exit(1);
});
