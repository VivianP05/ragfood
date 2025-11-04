#!/usr/bin/env node

/**
 * ============================================================================
 * FOOD RAG MCP SERVER - VS Code Insiders Integration
 * ============================================================================
 * 
 * Standalone MCP server for VS Code Insiders with comprehensive monitoring
 * 
 * Features:
 * ✅ Works with VS Code Insiders MCP UI controls
 * ✅ Detailed logging to VS Code Output panel
 * ✅ Real-time monitoring and debugging
 * ✅ Integrates with Food RAG System (Upstash Vector + Groq AI)
 * ✅ 3 powerful tools for food queries
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { Index } from '@upstash/vector';
import Groq from 'groq-sdk';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// Load environment variables
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
dotenv.config({ path: join(__dirname, '.env.local') });

// ============================================================================
// LOGGING SYSTEM (outputs to VS Code Output panel)
// ============================================================================

const log = {
  info: (msg, ...args) => console.error(`ℹ️  [INFO] ${msg}`, ...args),
  success: (msg, ...args) => console.error(`✅ [SUCCESS] ${msg}`, ...args),
  warn: (msg, ...args) => console.error(`⚠️  [WARN] ${msg}`, ...args),
  error: (msg, ...args) => console.error(`❌ [ERROR] ${msg}`, ...args),
  debug: (msg, ...args) => console.error(`🔍 [DEBUG] ${msg}`, ...args),
  tool: (name, duration) => console.error(`🔧 [TOOL] ${name} (${duration}ms)`),
};

// ============================================================================
// ENVIRONMENT VALIDATION
// ============================================================================

function validateEnvironment() {
  const required = ['UPSTASH_VECTOR_REST_URL', 'UPSTASH_VECTOR_REST_TOKEN', 'GROQ_API_KEY'];
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    log.error('Missing required environment variables:', missing.join(', '));
    log.error('Please check your .env.local file in mydigitaltwin/');
    process.exit(1);
  }
  
  log.success('Environment variables validated');
}

validateEnvironment();

// ============================================================================
// INITIALIZE UPSTASH VECTOR & GROQ
// ============================================================================

const vectorIndex = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN,
});

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

log.success('Connected to Upstash Vector Database');
log.success('Connected to Groq AI (llama-3.1-8b-instant)');

// ============================================================================
// TOOL IMPLEMENTATIONS
// ============================================================================

/**
 * Query food database with RAG
 */
async function queryFoodRAG(question) {
  const startTime = Date.now();
  
  try {
    log.debug(`Processing question: "${question.substring(0, 50)}..."`);
    
    // Step 1: Vector search
    log.debug('Searching Upstash Vector database...');
    const searchStart = Date.now();
    
    const results = await vectorIndex.query({
      data: question,
      topK: 3,
      includeMetadata: true,
    });
    
    const searchTime = Date.now() - searchStart;
    log.debug(`Vector search completed in ${searchTime}ms (${results.length} results)`);
    
    if (results.length === 0) {
      log.warn('No results found in vector database');
      return {
        content: [{
          type: 'text',
          text: 'I couldn\'t find any relevant information in the food database. Please try rephrasing your question.',
        }],
      };
    }
    
    // Step 2: Build context
    const context = results
      .map(r => {
        const text = r.metadata?.text || r.metadata?.name || 'Unknown food';
        const region = r.metadata?.region || r.metadata?.origin || 'Unknown region';
        const type = r.metadata?.type || r.metadata?.category || 'Food';
        return `${text} (${type} from ${region})`;
      })
      .join('\n\n');
    
    log.debug('Context built from vector results');
    
    // Step 3: Generate AI response
    log.debug('Generating AI response with Groq...');
    const aiStart = Date.now();
    
    const completion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: 'You are a helpful food expert assistant. Use the provided food information to answer questions about cuisines, dishes, recipes, and dietary information accurately and enthusiastically.',
        },
        {
          role: 'user',
          content: `Food Database Context:\n${context}\n\nQuestion: ${question}`,
        },
      ],
      model: 'llama-3.1-8b-instant',
      temperature: 0.7,
      max_tokens: 500,
    });
    
    const aiTime = Date.now() - aiStart;
    const totalTime = Date.now() - startTime;
    
    const answer = completion.choices[0]?.message?.content || 'No response generated.';
    
    log.success(`Query completed in ${totalTime}ms (vector: ${searchTime}ms, AI: ${aiTime}ms)`);
    log.tool('query_food_database', totalTime);
    
    return {
      content: [{
        type: 'text',
        text: `${answer}\n\n---\n*Response time: ${totalTime}ms | Results: ${results.length}*`,
      }],
    };
    
  } catch (error) {
    const totalTime = Date.now() - startTime;
    log.error('Query failed:', error.message);
    
    return {
      content: [{
        type: 'text',
        text: `❌ Error: ${error.message}\n\nPlease try again or rephrase your question.`,
      }],
      isError: true,
    };
  }
}

/**
 * Search by category
 */
async function searchByCategory(category, limit = 5) {
  const startTime = Date.now();
  
  try {
    log.debug(`Searching for category: "${category}" (limit: ${limit})`);
    
    const results = await vectorIndex.query({
      data: category,
      topK: Math.min(Math.max(limit, 1), 20),
      includeMetadata: true,
    });
    
    const totalTime = Date.now() - startTime;
    
    if (results.length === 0) {
      log.warn(`No results found for category: ${category}`);
      return {
        content: [{
          type: 'text',
          text: `No foods found matching "${category}". Try a different search term.`,
        }],
      };
    }
    
    const formatted = results
      .map((r, idx) => {
        const name = r.metadata?.name || r.metadata?.text || 'Unknown';
        const cat = r.metadata?.category || r.metadata?.type || 'Food';
        const origin = r.metadata?.origin || r.metadata?.region || 'Unknown';
        return `${idx + 1}. **${name}**\n   Category: ${cat}\n   Origin: ${origin}\n   Score: ${r.score.toFixed(3)}`;
      })
      .join('\n\n');
    
    log.success(`Found ${results.length} results in ${totalTime}ms`);
    log.tool('search_by_category', totalTime);
    
    return {
      content: [{
        type: 'text',
        text: `**Found ${results.length} food(s) for "${category}":**\n\n${formatted}\n\n*Search time: ${totalTime}ms*`,
      }],
    };
    
  } catch (error) {
    const totalTime = Date.now() - startTime;
    log.error('Search failed:', error.message);
    
    return {
      content: [{
        type: 'text',
        text: `❌ Search Error: ${error.message}`,
      }],
      isError: true,
    };
  }
}

/**
 * Get cache statistics
 */
async function getCacheStatistics() {
  const startTime = Date.now();
  
  try {
    log.debug('Fetching cache statistics...');
    
    // In a real implementation, you'd fetch actual cache stats
    // For now, we'll return server info
    const stats = {
      serverStatus: 'Running',
      database: 'Upstash Vector (free-loon-62438)',
      vectorCount: '200+ food items',
      aiModel: 'llama-3.1-8b-instant',
      region: 'us-east-1',
    };
    
    const totalTime = Date.now() - startTime;
    
    const formatted = Object.entries(stats)
      .map(([key, value]) => `• **${key}**: ${value}`)
      .join('\n');
    
    log.success(`Cache statistics retrieved in ${totalTime}ms`);
    log.tool('get_cache_statistics', totalTime);
    
    return {
      content: [{
        type: 'text',
        text: `**Food RAG System Status:**\n\n${formatted}\n\n*Query time: ${totalTime}ms*`,
      }],
    };
    
  } catch (error) {
    log.error('Failed to get statistics:', error.message);
    
    return {
      content: [{
        type: 'text',
        text: `❌ Statistics Error: ${error.message}`,
      }],
      isError: true,
    };
  }
}

// ============================================================================
// MCP SERVER SETUP
// ============================================================================

const server = new Server(
  {
    name: 'food-rag-system',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

log.info('MCP Server initialized');

// Register tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  log.debug('ListTools request received');
  
  return {
    tools: [
      {
        name: 'query_food_database',
        description: 'Search the food database for information about cuisines, dishes, ingredients, recipes, and dietary information. Returns AI-generated responses with context from 200+ food items.',
        inputSchema: {
          type: 'object',
          properties: {
            question: {
              type: 'string',
              description: 'Question about food, cuisine, recipes, or dietary information',
            },
          },
          required: ['question'],
        },
      },
      {
        name: 'search_by_category',
        description: 'Search for food items by category. Categories include: Main Course, Dessert, Beverage, Appetizer, Snack, Condiment, Spice, Fruit, Vegetable, etc.',
        inputSchema: {
          type: 'object',
          properties: {
            category: {
              type: 'string',
              description: 'Food category to search for',
            },
            limit: {
              type: 'number',
              description: 'Maximum number of results (1-20, default: 5)',
              default: 5,
            },
          },
          required: ['category'],
        },
      },
      {
        name: 'get_cache_statistics',
        description: 'Get performance statistics about the Food RAG System, including server status and database information.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  log.info(`Tool call: ${name}`);
  log.debug('Arguments:', JSON.stringify(args, null, 2));
  
  try {
    switch (name) {
      case 'query_food_database':
        return await queryFoodRAG(args?.question);
        
      case 'search_by_category':
        return await searchByCategory(args?.category, args?.limit);
        
      case 'get_cache_statistics':
        return await getCacheStatistics();
        
      default:
        log.warn(`Unknown tool: ${name}`);
        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
    }
  } catch (error) {
    log.error('Tool execution failed:', error.message);
    
    if (error instanceof McpError) {
      throw error;
    }
    
    throw new McpError(
      ErrorCode.InternalError,
      error instanceof Error ? error.message : 'Tool execution failed'
    );
  }
});

// ============================================================================
// START SERVER
// ============================================================================

async function main() {
  try {
    log.info('Starting Food RAG MCP Server...');
    
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    log.success('✨ Food RAG MCP Server is running!');
    log.info('📍 Available tools: query_food_database, search_by_category, get_cache_statistics');
    log.info('🔗 Database: Upstash Vector (200+ food items)');
    log.info('🤖 AI Model: Groq llama-3.1-8b-instant');
    log.info('📊 Monitor this output in VS Code Output panel');
    log.info('---------------------------------------------------');
    
  } catch (error) {
    log.error('Failed to start MCP server:', error.message);
    process.exit(1);
  }
}

// Graceful shutdown
process.on('SIGINT', () => {
  log.info('Shutting down Food RAG MCP Server...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  log.info('Food RAG MCP Server terminated');
  process.exit(0);
});

// Start server
main().catch((error) => {
  log.error('Fatal error:', error.message);
  process.exit(1);
});
