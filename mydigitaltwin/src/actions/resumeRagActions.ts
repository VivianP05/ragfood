"use server";

import { Index } from "@upstash/vector";
import Groq from "groq-sdk";

/**
 * Resume RAG Server Actions
 * 
 * Provides server-side actions for querying Vivian's professional resume and profile.
 * Integrates Upstash Vector database for semantic search and Groq AI for response generation.
 * 
 * Features:
 * - Semantic search across resume chunks (15) and professional profile (29 items)
 * - AI-powered resume Q&A with Groq
 * - Response caching for improved performance
 * - Comprehensive error handling
 * 
 * @module resumeRagActions
 */

// ============================================================================
// INITIALIZATION & VALIDATION
// ============================================================================

/**
 * Validate required environment variables
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

/** Initialize Upstash Vector Index */
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

/** Initialize Groq client */
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY!,
});

// ============================================================================
// CACHING LAYER
// ============================================================================

interface CacheEntry {
  data: string;
  timestamp: number;
}

const responseCache = new Map<string, CacheEntry>();
const CACHE_DURATION_MS = 10 * 60 * 1000; // 10 minutes

function getCached(key: string): string | undefined {
  const entry = responseCache.get(key);
  if (!entry) return undefined;

  const age = Date.now() - entry.timestamp;
  if (age > CACHE_DURATION_MS) {
    responseCache.delete(key);
    return undefined;
  }

  return entry.data;
}

function setCache(key: string, value: string): void {
  responseCache.set(key, {
    data: value,
    timestamp: Date.now(),
  });
}

// ============================================================================
// MAIN RAG QUERY FUNCTION
// ============================================================================

/**
 * Query Vivian's professional resume with RAG
 * 
 * @param question - User's question about resume, skills, experience, or career
 * @returns Promise resolving to response object with answer and metadata
 */
export async function queryResumeRAG(question: string): Promise<{
  success: boolean;
  answer?: string;
  error?: string;
  sources?: Array<{ title: string; relevance: number }>;
  metadata?: {
    searchResults: number;
    model: string;
    processingTime: number;
    cached: boolean;
  };
}> {
  const startTime = Date.now();

  try {
    // ========================================================================
    // STEP 1: INPUT VALIDATION
    // ========================================================================
    
    if (!question || typeof question !== 'string') {
      return {
        success: false,
        error: "Question must be a non-empty string",
      };
    }

    const trimmedQuestion = question.trim();
    
    if (trimmedQuestion.length === 0) {
      return {
        success: false,
        error: "Question cannot be empty",
      };
    }

    if (trimmedQuestion.length > 500) {
      return {
        success: false,
        error: "Question is too long (maximum 500 characters)",
      };
    }

    // ========================================================================
    // STEP 2: CACHE LOOKUP
    // ========================================================================
    
    const cacheKey = trimmedQuestion.toLowerCase().trim();
    const cachedAnswer = getCached(cacheKey);
    
    if (cachedAnswer) {
      const processingTime = Date.now() - startTime;
      return {
        success: true,
        answer: cachedAnswer,
        metadata: {
          searchResults: 0,
          model: "llama-3.1-8b-instant",
          processingTime,
          cached: true,
        },
      };
    }

    // ========================================================================
    // STEP 3: VECTOR SEARCH
    // ========================================================================
    
    const results = await index.query({
      data: trimmedQuestion,
      topK: 3,
      includeMetadata: true,
      includeData: true, // Critical: get the actual text content
    });

    if (!results || results.length === 0) {
      return {
        success: false,
        error: "No relevant information found. Please try rephrasing your question.",
      };
    }

    // ========================================================================
    // STEP 4: CONTEXT EXTRACTION
    // ========================================================================
    
    const contextItems: string[] = [];
    const sources: Array<{ title: string; relevance: number }> = [];
    
    results.forEach((result) => {
      const metadata = result.metadata as Record<string, string | undefined>;
      const textContent = result.data;
      
      // Build descriptive title from metadata
      let title: string;
      if (metadata.name) {
        if (metadata.company) {
          title = `${metadata.name} at ${metadata.company}`;
        } else if (metadata.skill) {
          const level = metadata.level || metadata.proficiency || 'N/A';
          title = `${metadata.skill} Skills (Level ${level})`;
        } else {
          title = metadata.name;
        }
      } else {
        title = result.id || "Information";
      }
      
      // Add to sources
      sources.push({
        title,
        relevance: result.score || 0,
      });
      
      // Add to context if we have text
      if (textContent) {
        contextItems.push(`${title}:\n${textContent}`);
      }
    });

    if (contextItems.length === 0) {
      return {
        success: false,
        error: "Found results but couldn't extract content. Please try again.",
      };
    }

    const context = contextItems.join("\n\n---\n\n");

    // ========================================================================
    // STEP 5: AI RESPONSE GENERATION
    // ========================================================================
    
    const completion = await groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content: `You are Vivian Pham's professional AI assistant. Answer questions about her professional background, skills, experience, projects, and career goals based on the provided context.

INSTRUCTIONS:
1. Be specific and use actual achievements and metrics from the context
2. Speak professionally and confidently
3. You can refer to Vivian in third person or use "I" to represent her (whichever feels more natural)
4. If the context doesn't fully answer the question, say what you know and acknowledge limitations
5. Highlight Jung Talents experience, dual BI platform expertise (Tableau + Power BI), and quantified achievements
6. Keep responses concise but comprehensive (2-3 paragraphs)

TONE: Professional, confident, achievement-focused`,
        },
        {
          role: "user",
          content: `RESUME CONTEXT:\n\n${context}\n\n---\n\nQUESTION: ${trimmedQuestion}\n\nProvide a helpful, accurate response based on the resume information:`,
        },
      ],
      model: "llama-3.1-8b-instant",
      temperature: 0.7,
      max_tokens: 500,
      top_p: 0.95,
    });

    const answer = completion.choices[0]?.message?.content;
    
    if (!answer) {
      throw new Error('AI generated empty response');
    }

    // ========================================================================
    // STEP 6: CACHE THE RESPONSE
    // ========================================================================
    
    setCache(cacheKey, answer);

    // ========================================================================
    // STEP 7: RETURN RESPONSE
    // ========================================================================
    
    const processingTime = Date.now() - startTime;

    return {
      success: true,
      answer,
      sources,
      metadata: {
        searchResults: results.length,
        model: "llama-3.1-8b-instant",
        processingTime,
        cached: false,
      },
    };

  } catch (error) {
    const processingTime = Date.now() - startTime;
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    
    console.error('Resume RAG query failed:', error);
    
    return {
      success: false,
      error: `Failed to process your question: ${errorMessage}`,
      metadata: {
        searchResults: 0,
        model: "llama-3.1-8b-instant",
        processingTime,
        cached: false,
      },
    };
  }
}
