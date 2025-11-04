"use server";

import { Index } from "@upstash/vector";
import Groq from "groq-sdk";
import {
  safeVectorQuery,
  safeGroqAPI,
  classifyError,
  logger,
} from "../lib/errorHandling";

/**
 * Food RAG Server Actions
 * 
 * Provides server-side actions for querying the Food RAG system.
 * Integrates Upstash Vector database for semantic search and Groq AI for response generation.
 * 
 * Features:
 * - Semantic search across 200+ food items
 * - AI-powered response generation with Groq
 * - Automatic retry logic with exponential backoff
 * - Response caching for improved performance
 * - Comprehensive error handling and classification
 * - Performance metrics tracking
 * - Structured logging for debugging
 * 
 * @module foodRagActions
 */

// ============================================================================
// CONSTANTS & CONFIGURATION
// ============================================================================

/** Performance monitoring thresholds (ms) */
const PERF_THRESHOLDS = {
  VECTOR_SEARCH_MS: 800,      // Warn if vector search takes longer
  AI_GENERATION_MS: 2000,     // Warn if AI generation takes longer
  TOTAL_MS: 2500,             // Warn if total query takes longer
  MIN_SCORE_THRESHOLD: 0.5,   // Minimum relevance score
} as const;

/** Cache configuration for optimal performance */
const CACHE_CONFIG = {
  MAX_SIZE: 200,              // Maximum cache entries
  TTL_MS: 10 * 60 * 1000,    // Time-to-live: 10 minutes
  CLEANUP_INTERVAL: 60000,    // Cleanup every 60 seconds
} as const;

/** Cache duration for responses (10 minutes for better hit rates) */
const CACHE_DURATION_MS = CACHE_CONFIG.TTL_MS;

/** Maximum cache size to prevent memory issues */
const MAX_CACHE_SIZE = CACHE_CONFIG.MAX_SIZE;

// ============================================================================
// INITIALIZATION & VALIDATION
// ============================================================================

/**
 * Validate required environment variables
 * Throws descriptive errors if configuration is missing
 */
function validateEnvironment(): void {
  const required = {
    UPSTASH_VECTOR_REST_URL: process.env.UPSTASH_VECTOR_REST_URL,
    UPSTASH_VECTOR_REST_TOKEN: process.env.UPSTASH_VECTOR_REST_TOKEN,
    GROQ_API_KEY: process.env.GROQ_API_KEY,
  };

  const missing = Object.entries(required)
    .filter(([, value]) => !value)
    .map(([key]) => key);

  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missing.join(", ")}. ` +
      `Please check your .env.local file.`
    );
  }
}

// Validate environment on module load
validateEnvironment();

/** Initialize Upstash Vector Index with validated credentials */
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

/** Initialize Groq client with validated API key */
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY!,
});

// ============================================================================
// ADVANCED CACHING LAYER WITH LRU EVICTION
// ============================================================================

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  accessCount: number;
  lastAccessed: number;
}

/**
 * LRU (Least Recently Used) Cache with TTL
 * Provides efficient caching with automatic expiration and smart eviction
 */
class LRUCache<T> {
  private cache = new Map<string, CacheEntry<T>>();
  private cleanupInterval: NodeJS.Timeout | null = null;

  constructor() {
    this.startCleanup();
  }

  /**
   * Get value from cache if valid
   * Updates access metadata for LRU tracking
   */
  get(key: string): T | undefined {
    const entry = this.cache.get(key);
    if (!entry) return undefined;

    const age = Date.now() - entry.timestamp;
    if (age > CACHE_CONFIG.TTL_MS) {
      this.cache.delete(key);
      logger.debug('Cache entry expired', { key: key.substring(0, 30), age });
      return undefined;
    }

    // Update LRU metadata
    entry.accessCount++;
    entry.lastAccessed = Date.now();
    
    logger.debug('Cache HIT', { 
      key: key.substring(0, 30), 
      age: Math.round(age / 1000),
      accessCount: entry.accessCount 
    });
    
    return entry.data;
  }

  /**
   * Store value in cache with LRU eviction if needed
   */
  set(key: string, value: T): void {
    // Evict least recently used entry if cache is full
    if (this.cache.size >= CACHE_CONFIG.MAX_SIZE && !this.cache.has(key)) {
      this.evictLRU();
    }

    this.cache.set(key, {
      data: value,
      timestamp: Date.now(),
      accessCount: 1,
      lastAccessed: Date.now(),
    });

    logger.debug('Cache STORE', { 
      key: key.substring(0, 30),
      cacheSize: this.cache.size 
    });
  }

  /**
   * Evict least recently used entry
   */
  private evictLRU(): void {
    let lruKey: string | null = null;
    let lruTime = Infinity;

    for (const [key, entry] of this.cache.entries()) {
      if (entry.lastAccessed < lruTime) {
        lruTime = entry.lastAccessed;
        lruKey = key;
      }
    }

    if (lruKey) {
      this.cache.delete(lruKey);
      logger.debug('Cache evicted LRU entry', { 
        key: lruKey.substring(0, 30),
        age: Math.round((Date.now() - lruTime) / 1000) 
      });
    }
  }

  /**
   * Get cache statistics
   */
  getStats() {
    const entries = Array.from(this.cache.values());
    return {
      size: this.cache.size,
      maxSize: CACHE_CONFIG.MAX_SIZE,
      totalAccesses: entries.reduce((sum, e) => sum + e.accessCount, 0),
      avgAccessCount: entries.length > 0 
        ? entries.reduce((sum, e) => sum + e.accessCount, 0) / entries.length 
        : 0,
    };
  }

  /**
   * Clear all cache entries
   */
  clear(): void {
    this.cache.clear();
    logger.info('Cache cleared', { previousSize: this.cache.size });
  }

  /**
   * Start automatic cleanup of expired entries
   */
  private startCleanup(): void {
    this.cleanupInterval = setInterval(() => {
      const now = Date.now();
      let expiredCount = 0;

      for (const [key, entry] of this.cache.entries()) {
        if (now - entry.timestamp > CACHE_CONFIG.TTL_MS) {
          this.cache.delete(key);
          expiredCount++;
        }
      }

      if (expiredCount > 0) {
        logger.debug('Cache cleanup completed', { 
          expiredCount, 
          remainingSize: this.cache.size 
        });
      }
    }, CACHE_CONFIG.CLEANUP_INTERVAL);
  }

  /**
   * Stop cleanup interval (for cleanup/testing)
   */
  destroy(): void {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
  }
}

/** Global response cache instance with LRU eviction */
const responseCache = new LRUCache<string>();

// ============================================================================
// REQUEST DEDUPLICATION
// ============================================================================

/**
 * Request Deduplication Manager
 * Prevents duplicate concurrent requests by sharing promises
 */
class RequestDeduplicator {
  private pending = new Map<string, Promise<any>>();

  /**
   * Execute a function with deduplication
   * If the same key is already pending, returns the existing promise
   */
  async execute<T>(key: string, executor: () => Promise<T>): Promise<T> {
    // Return existing pending promise if available
    if (this.pending.has(key)) {
      logger.debug('Request deduplication HIT', { key: key.substring(0, 30) });
      return this.pending.get(key) as Promise<T>;
    }

    // Create new promise and track it
    logger.debug('Request deduplication MISS', { key: key.substring(0, 30) });
    const promise = executor();
    this.pending.set(key, promise);

    // Clean up when complete
    promise.finally(() => {
      this.pending.delete(key);
    });

    return promise;
  }

  /** Get number of pending requests */
  getPendingCount(): number {
    return this.pending.size;
  }
}

/** Global request deduplicator instance */
const requestDeduplicator = new RequestDeduplicator();

// ============================================================================
// QUERY PREPROCESSING
// ============================================================================

/**
 * Normalize and preprocess queries for better cache hits and search
 */
function preprocessQuery(query: string): string {
  return query
    .toLowerCase()
    .trim()
    .replace(/\s+/g, ' ')              // Normalize whitespace
    .replace(/[^\w\s]/g, '')           // Remove special characters
    .replace(/\b(what|is|are|the|a|an)\b/g, '') // Remove common words
    .trim();
}

/**
 * Generate optimized cache key from question
 */
function generateCacheKey(question: string): string {
  return preprocessQuery(question);
}

// ============================================================================
// MAIN RAG QUERY FUNCTION
// ============================================================================

// ============================================================================
// MAIN RAG QUERY FUNCTION
// ============================================================================

/**
 * Query the Food RAG system with comprehensive error handling and performance optimization
 * 
 * This function performs the following steps:
 * 1. Input validation and sanitization
 * 2. Cache lookup for previously answered questions
 * 3. Semantic search in Upstash Vector database
 * 4. Context extraction and formatting
 * 5. AI response generation via Groq
 * 6. Response caching for future queries
 * 
 * @param question - User's question about food, cuisines, recipes, or dietary information
 * @returns Promise resolving to response object with answer, context, and metadata
 * 
 * @example
 * ```typescript
 * const result = await queryFoodRAG("What is Biryani?");
 * if (result.success) {
 *   console.log(result.answer);
 * }
 * ```
 */
export async function queryFoodRAG(question: string): Promise<{
  success: boolean;
  answer?: string;
  error?: string;
  context?: string[];
  metadata?: {
    searchResults: number;
    model: string;
    processingTime: number;
    cached: boolean;
    vectorSearchTime?: number;
    aiGenerationTime?: number;
  };
}> {
  const startTime = Date.now();
  let vectorSearchTime = 0;
  let aiGenerationTime = 0;

  try {
    // ========================================================================
    // STEP 1: INPUT VALIDATION
    // ========================================================================
    
    if (!question || typeof question !== 'string') {
      logger.warn('Invalid input: question must be a non-empty string', { question });
      return {
        success: false,
        error: "Question must be a non-empty string",
      };
    }

    const trimmedQuestion = question.trim();
    
    if (trimmedQuestion.length === 0) {
      logger.warn('Empty question provided after trimming');
      return {
        success: false,
        error: "Question cannot be empty",
      };
    }

    if (trimmedQuestion.length > 500) {
      logger.warn('Question exceeds maximum length', { length: trimmedQuestion.length });
      return {
        success: false,
        error: "Question is too long (maximum 500 characters)",
      };
    }

    logger.info('Processing food query', { 
      question: trimmedQuestion.substring(0, 100),
      length: trimmedQuestion.length 
    });

    // ========================================================================
    // STEP 2: OPTIMIZED CACHE LOOKUP WITH PREPROCESSING
    // ========================================================================
    
    const cacheKey = generateCacheKey(trimmedQuestion);
    const cachedAnswer = responseCache.get(cacheKey);
    
    if (cachedAnswer) {
      const processingTime = Date.now() - startTime;
      logger.info('Returning cached response', { 
        processingTime,
        cacheAge: processingTime 
      });
      
      return {
        success: true,
        answer: cachedAnswer,
        context: [],
        metadata: {
          searchResults: 0,
          model: "llama-3.1-8b-instant",
          processingTime,
          cached: true,
        },
      };
    }

    // ========================================================================
    // STEP 3: REQUEST DEDUPLICATION & VECTOR SEARCH
    // ========================================================================
    
    // Use deduplicator to prevent concurrent duplicate queries
    return await requestDeduplicator.execute(cacheKey, async () => {
      // Check cache again (might have been filled by another request)
      const recheck = responseCache.get(cacheKey);
      if (recheck) {
        const processingTime = Date.now() - startTime;
        logger.info('Cache filled by deduplicated request', { processingTime });
        return {
          success: true,
          answer: recheck,
          context: [],
          metadata: {
            searchResults: 0,
            model: "llama-3.1-8b-instant",
            processingTime,
            cached: true,
          },
        };
      }

      logger.debug('Querying Upstash Vector database', { topK: 3 });
      const vectorSearchStart = Date.now();
      
      const results = await safeVectorQuery(
        async () => {
          const searchResults = await index.query({
            data: trimmedQuestion,
            topK: 3,
            includeMetadata: true,
          });
          
          if (!searchResults || searchResults.length === 0) {
            throw new Error('No results returned from vector search');
          }
          
          return searchResults;
        },
        `Food search for: "${trimmedQuestion.substring(0, 50)}..."`
      );

      vectorSearchTime = Date.now() - vectorSearchStart;
      
      // Performance threshold warning
      if (vectorSearchTime > PERF_THRESHOLDS.VECTOR_SEARCH_MS) {
        logger.warn('Vector search exceeded threshold', {
          duration: vectorSearchTime,
          threshold: PERF_THRESHOLDS.VECTOR_SEARCH_MS
        });
      }
      
      logger.perf('Vector search', vectorSearchTime, { 
        resultsCount: results.length,
      });

    // ========================================================================
    // STEP 4: CONTEXT EXTRACTION & FORMATTING
    // ========================================================================
    
    const contextItems: string[] = [];
    const debugInfo: Array<{ score: number; preview: string }> = [];
    
    results.forEach((result, idx) => {
      const metadata = result.metadata as Record<string, string | undefined>;
      let foodInfo: string;
      
      // Handle detailed format (with structured fields)
      if (metadata.name) {
        const parts: string[] = [`${metadata.name}: ${metadata.description || ""}`];
        
        if (metadata.origin) parts.push(`Origin: ${metadata.origin}`);
        if (metadata.category) parts.push(`Category: ${metadata.category}`);
        if (metadata.ingredients) parts.push(`Ingredients: ${metadata.ingredients}`);
        if (metadata.cooking_method) parts.push(`Preparation: ${metadata.cooking_method}`);
        if (metadata.dietary_tags) parts.push(`Dietary: ${metadata.dietary_tags}`);
        
        foodInfo = parts.join('\n');
      } 
      // Handle simple format (text-based)
      else {
        const parts: string[] = [metadata.text || ""];
        if (metadata.region) parts.push(`Region: ${metadata.region}`);
        if (metadata.type) parts.push(`Type: ${metadata.type}`);
        
        foodInfo = parts.join('\n');
      }
      
      contextItems.push(foodInfo);
      debugInfo.push({
        score: result.score || 0,
        preview: foodInfo.substring(0, 80) + (foodInfo.length > 80 ? '...' : '')
      });
      
      logger.debug(`Search result ${idx + 1}`, {
        score: result.score?.toFixed(4),
        hasName: !!metadata.name,
        hasDescription: !!metadata.description
      });
    });

    const context = contextItems.join("\n\n---\n\n");
    logger.debug('Context built', { 
      contextLength: context.length,
      itemsCount: contextItems.length 
    });

    // ========================================================================
    // STEP 5: AI RESPONSE GENERATION WITH PERFORMANCE TRACKING
    // ========================================================================
    
    logger.debug('Generating AI response with Groq');
    const aiGenerationStart = Date.now();
    
    const completion = await safeGroqAPI(
      async () => {
        return await groq.chat.completions.create({
          messages: [
            {
              role: "system",
              content: `You are an expert food assistant with comprehensive knowledge of global cuisines, dishes, recipes, and dietary information.

INSTRUCTIONS:
1. Use the provided food database context to answer questions accurately
2. Be enthusiastic and conversational while remaining informative
3. Include specific details from the context when available
4. Mention origins, ingredients, preparation methods, and dietary considerations
5. If context is limited, supplement with general culinary knowledge but clearly distinguish between database info and general knowledge
6. Keep responses concise but comprehensive (aim for 3-4 paragraphs)

TONE: Friendly, knowledgeable, encouraging`,
            },
            {
              role: "user",
              content: `FOOD DATABASE CONTEXT:\n\n${context}\n\n---\n\nUSER QUESTION: ${trimmedQuestion}`,
            },
          ],
          model: "llama-3.1-8b-instant",
          temperature: 0.7,
          max_tokens: 500,
          top_p: 0.95,
        });
      },
      `AI generation for: "${trimmedQuestion.substring(0, 50)}..."`
    );

    aiGenerationTime = Date.now() - aiGenerationStart;
    
    // Performance threshold warning
    if (aiGenerationTime > PERF_THRESHOLDS.AI_GENERATION_MS) {
      logger.warn('AI generation exceeded threshold', {
        duration: aiGenerationTime,
        threshold: PERF_THRESHOLDS.AI_GENERATION_MS
      });
    }
    
    const answer = completion.choices[0]?.message?.content;
    
    if (!answer) {
      throw new Error('AI generated empty response');
    }

    logger.perf('AI response generation', aiGenerationTime, { 
      answerLength: answer.length,
      tokensUsed: completion.usage?.total_tokens 
    });

    // ========================================================================
    // STEP 6: CACHE THE RESPONSE
    // ========================================================================
    
    responseCache.set(cacheKey, answer);

    // ========================================================================
    // STEP 7: RETURN COMPREHENSIVE RESPONSE WITH METRICS
    // ========================================================================
    
    const processingTime = Date.now() - startTime;
    
    // Overall performance threshold warning
    if (processingTime > PERF_THRESHOLDS.TOTAL_MS) {
      logger.warn('Total query time exceeded threshold', {
        duration: processingTime,
        threshold: PERF_THRESHOLDS.TOTAL_MS
      });
    }
    
    logger.perf('Complete food query', processingTime, { 
      vectorSearchTime,
      aiGenerationTime,
      cached: false,
    });

    return {
      success: true,
      answer,
      context: contextItems,
      metadata: {
        searchResults: results.length,
        model: "llama-3.1-8b-instant",
        processingTime,
        cached: false,
        vectorSearchTime,
        aiGenerationTime,
      },
    };
    }); // End of requestDeduplicator.execute()

  } catch (error) {
    // ========================================================================
    // COMPREHENSIVE ERROR HANDLING WITH CLASSIFICATION
    // ========================================================================
    
    const processingTime = Date.now() - startTime;
    const errorInfo = classifyError(error);
    
    logger.error(`Query failed [${errorInfo.category}]`, error);
    logger.debug('Error details', {
      category: errorInfo.category,
      retryable: errorInfo.retryable,
      processingTime,
    });
    
    return {
      success: false,
      error: errorInfo.userMessage,
      metadata: {
        searchResults: 0,
        model: "llama-3.1-8b-instant",
        processingTime,
        cached: false,
      },
    };
  }
}

/**
 * Search food database by category with comprehensive error handling
 * 
 * @param category - Food category (e.g., "Main Course", "Dessert", "Fruit", "Spice")
 * @param limit - Maximum number of results to return (default: 5)
 * @returns Promise resolving to array of food items in the category
 * 
 * @example
 * ```typescript
 * const result = await searchByCategory("Dessert", 10);
 * if (result.success) {
 *   console.log(result.results);
 * }
 * ```
 */
export async function searchByCategory(
  category: string,
  limit: number = 5
): Promise<{
  success: boolean;
  results?: Array<{
    name: string;
    description: string;
    region?: string;
    type?: string;
  }>;
  error?: string;
}> {
  const startTime = Date.now();
  
  try {
    // Input validation
    if (!category || typeof category !== 'string' || category.trim().length === 0) {
      logger.warn('Invalid category input', { category });
      return {
        success: false,
        error: "Category must be a non-empty string",
      };
    }

    if (limit < 1 || limit > 100) {
      logger.warn('Invalid limit parameter', { limit });
      return {
        success: false,
        error: "Limit must be between 1 and 100",
      };
    }

    logger.info(`Searching category: ${category}`, { limit });
    
    // Search with category-focused query using safe wrapper
    const results = await safeVectorQuery(
      async () => {
        return await index.query({
          data: `${category} food items`,
          topK: limit,
          includeMetadata: true,
        });
      },
      `Category search: ${category}`
    );

    const foodItems = results.map((result) => {
      const metadata = result.metadata as Record<string, string | undefined>;
      return {
        name: metadata.name || metadata.text || "Unknown",
        description: metadata.description || metadata.text || "",
        region: metadata.region || metadata.origin,
        type: metadata.type || metadata.category,
      };
    });

    const processingTime = Date.now() - startTime;
    logger.perf(`Category search: ${category}`, processingTime, { 
      resultCount: foodItems.length 
    });

    return {
      success: true,
      results: foodItems,
    };
    
  } catch (error) {
    const errorInfo = classifyError(error);
    
    logger.error(`Category search failed [${errorInfo.category}]`, error);
    
    return {
      success: false,
      error: errorInfo.userMessage,
    };
  }
}

/**
 * Get personalized food recommendations based on user preferences
 * 
 * Uses semantic search and AI to provide tailored food suggestions based on
 * dietary restrictions, flavor preferences, cuisine types, or meal requirements.
 * 
 * @param preferences - User preferences (e.g., "vegetarian and spicy", "healthy breakfast", "traditional Indian desserts")
 * @returns Promise resolving to personalized recommendations
 * 
 * @example
 * ```typescript
 * const result = await getFoodRecommendations("healthy vegetarian lunch options");
 * if (result.success) {
 *   console.log(result.recommendations);
 * }
 * ```
 */
export async function getFoodRecommendations(
  preferences: string
): Promise<{
  success: boolean;
  recommendations?: string;
  error?: string;
}> {
  const startTime = Date.now();
  
  try {
    // Input validation
    if (!preferences || typeof preferences !== 'string' || preferences.trim().length === 0) {
      logger.warn('Invalid preferences input', { preferences });
      return {
        success: false,
        error: "Preferences must be a non-empty string",
      };
    }

    const trimmedPreferences = preferences.trim();
    logger.info(`Generating recommendations for: ${trimmedPreferences.substring(0, 100)}`);
    
    // Search for foods matching preferences using safe wrapper
    const results = await safeVectorQuery(
      async () => {
        return await index.query({
          data: trimmedPreferences,
          topK: 5,
          includeMetadata: true,
        });
      },
      `Recommendations search: ${trimmedPreferences.substring(0, 50)}`
    );

    // Build context from results
    const foodList = results
      .map((r, idx) => {
        const metadata = r.metadata as Record<string, string | undefined>;
        const name = metadata.name || metadata.text;
        const desc = metadata.description || "";
        return `${idx + 1}. ${name}${desc ? `: ${desc}` : ""}`;
      })
      .join("\n");

    // Generate personalized recommendations using safe Groq wrapper
    const completion = await safeGroqAPI(
      async () => {
        return await groq.chat.completions.create({
          messages: [
            {
              role: "system",
              content:
                "You are a food recommendation expert. Provide personalized, enthusiastic recommendations based on user preferences. Be specific and helpful.",
            },
            {
              role: "user",
              content: `User preferences: ${trimmedPreferences}\n\nRelevant foods from our database:\n${foodList}\n\nProvide 3-5 personalized recommendations with brief explanations why they match the preferences.`,
            },
          ],
          model: "llama-3.1-8b-instant",
          temperature: 0.8,
          max_tokens: 400,
        });
      },
      `Recommendations generation: ${trimmedPreferences.substring(0, 50)}`
    );

    const recommendations = completion.choices[0]?.message?.content;
    
    if (!recommendations) {
      throw new Error('No recommendations generated');
    }

    const processingTime = Date.now() - startTime;
    logger.perf('Food recommendations', processingTime, {
      preferencesLength: trimmedPreferences.length,
      recommendationsLength: recommendations.length,
    });

    return {
      success: true,
      recommendations,
    };
    
  } catch (error) {
    const errorInfo = classifyError(error);
    
    logger.error(`Recommendations failed [${errorInfo.category}]`, error);
    
    return {
      success: false,
      error: errorInfo.userMessage,
    };
  }
}

// ============================================================================
// ADMIN & MONITORING UTILITIES
// ============================================================================

/**
 * Clear the response cache
 * Useful for testing or when data is updated
 * 
 * @example
 * ```typescript
 * const result = await clearCache();
 * console.log(result.message); // "Cache cleared successfully. Removed X entries."
 * ```
 */
export async function clearCache(): Promise<{
  success: boolean;
  message: string;
}> {
  try {
    const stats = responseCache.getStats();
    responseCache.clear();
    
    logger.info('Cache manually cleared', { previousSize: stats.size });
    
    return {
      success: true,
      message: `Cache cleared successfully. Removed ${stats.size} entries.`,
    };
  } catch (error) {
    logger.error('Failed to clear cache', error);
    return {
      success: false,
      message: 'Failed to clear cache',
    };
  }
}

/**
 * Get cache statistics for monitoring
 * 
 * @example
 * ```typescript
 * const stats = await getCacheStats();
 * console.log(`Cache: ${stats.stats.size}/${stats.stats.maxSize} entries`);
 * ```
 */
export async function getCacheStats(): Promise<{
  success: boolean;
  stats?: {
    size: number;
    maxSize: number;
    totalAccesses: number;
    avgAccessCount: number;
    pendingRequests: number;
  };
  error?: string;
}> {
  try {
    const cacheStats = responseCache.getStats();
    const pendingRequests = requestDeduplicator.getPendingCount();
    
    logger.debug('Cache stats requested', cacheStats);
    
    return {
      success: true,
      stats: {
        ...cacheStats,
        pendingRequests,
      },
    };
  } catch (error) {
    logger.error('Failed to get cache stats', error);
    return {
      success: false,
      error: 'Failed to retrieve cache statistics',
    };
  }
}
