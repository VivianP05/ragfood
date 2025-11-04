/**
 * Error Handling Utilities for Upstash Vector and Groq API
 * 
 * Provides comprehensive error handling, retry logic, and error categorization
 * for external API calls to Upstash Vector database and Groq AI service.
 * 
 * @module errorHandling
 */

// ============================================================================
// ERROR TYPES & CLASSIFICATIONS
// ============================================================================

/**
 * Custom error class for Upstash Vector operations
 */
export class UpstashVectorError extends Error {
  constructor(
    message: string,
    public readonly category: ErrorCategory,
    public readonly retryable: boolean,
    public readonly statusCode?: number,
    public readonly originalError?: unknown
  ) {
    super(message);
    this.name = 'UpstashVectorError';
  }
}

/**
 * Custom error class for Groq API operations
 */
export class GroqAPIError extends Error {
  constructor(
    message: string,
    public readonly category: ErrorCategory,
    public readonly retryable: boolean,
    public readonly statusCode?: number,
    public readonly originalError?: unknown
  ) {
    super(message);
    this.name = 'GroqAPIError';
  }
}

/**
 * Error categories for better error handling and user feedback
 */
export enum ErrorCategory {
  // Network-related errors
  NETWORK = 'NETWORK',
  TIMEOUT = 'TIMEOUT',
  
  // Authentication/Authorization errors
  AUTH = 'AUTH',
  PERMISSION = 'PERMISSION',
  
  // Rate limiting and quota errors
  RATE_LIMIT = 'RATE_LIMIT',
  QUOTA_EXCEEDED = 'QUOTA_EXCEEDED',
  
  // Input validation errors
  INVALID_INPUT = 'INVALID_INPUT',
  INVALID_QUERY = 'INVALID_QUERY',
  
  // Database/Service errors
  DATABASE_ERROR = 'DATABASE_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  
  // Response errors
  EMPTY_RESPONSE = 'EMPTY_RESPONSE',
  INVALID_RESPONSE = 'INVALID_RESPONSE',
  
  // Unknown/Unexpected errors
  UNKNOWN = 'UNKNOWN',
}

/**
 * Error information for user-friendly messages
 */
interface ErrorInfo {
  category: ErrorCategory;
  retryable: boolean;
  userMessage: string;
  suggestedAction: string;
}

// ============================================================================
// ERROR CLASSIFICATION
// ============================================================================

/**
 * Classify error based on error message and type
 * @param error - The error to classify
 * @returns Classified error information
 */
export function classifyError(error: unknown): ErrorInfo {
  if (!error) {
    return {
      category: ErrorCategory.UNKNOWN,
      retryable: false,
      userMessage: 'An unknown error occurred',
      suggestedAction: 'Please try again later',
    };
  }

  const errorMessage = error instanceof Error ? error.message.toLowerCase() : String(error).toLowerCase();
  const errorString = String(error).toLowerCase();

  // Network errors
  if (
    errorMessage.includes('network') ||
    errorMessage.includes('fetch failed') ||
    errorMessage.includes('econnrefused') ||
    errorMessage.includes('enotfound') ||
    errorString.includes('networkerror')
  ) {
    return {
      category: ErrorCategory.NETWORK,
      retryable: true,
      userMessage: 'Network connection error',
      suggestedAction: 'Please check your internet connection and try again',
    };
  }

  // Timeout errors
  if (
    errorMessage.includes('timeout') ||
    errorMessage.includes('timed out') ||
    errorMessage.includes('etimedout')
  ) {
    return {
      category: ErrorCategory.TIMEOUT,
      retryable: true,
      userMessage: 'Request timed out',
      suggestedAction: 'The service is taking longer than expected. Please try again',
    };
  }

  // Authentication errors
  if (
    errorMessage.includes('unauthorized') ||
    errorMessage.includes('authentication') ||
    errorMessage.includes('invalid token') ||
    errorMessage.includes('invalid api key') ||
    errorMessage.includes('401')
  ) {
    return {
      category: ErrorCategory.AUTH,
      retryable: false,
      userMessage: 'Authentication failed',
      suggestedAction: 'Please contact support - API credentials may be invalid',
    };
  }

  // Rate limiting
  if (
    errorMessage.includes('rate limit') ||
    errorMessage.includes('too many requests') ||
    errorMessage.includes('429')
  ) {
    return {
      category: ErrorCategory.RATE_LIMIT,
      retryable: true,
      userMessage: 'Rate limit exceeded',
      suggestedAction: 'Too many requests. Please wait a moment and try again',
    };
  }

  // Quota exceeded
  if (
    errorMessage.includes('quota') ||
    errorMessage.includes('limit exceeded') ||
    errorMessage.includes('usage limit')
  ) {
    return {
      category: ErrorCategory.QUOTA_EXCEEDED,
      retryable: false,
      userMessage: 'Service quota exceeded',
      suggestedAction: 'Daily or monthly quota reached. Please try again later',
    };
  }

  // Service unavailable
  if (
    errorMessage.includes('service unavailable') ||
    errorMessage.includes('503') ||
    errorMessage.includes('502') ||
    errorMessage.includes('500')
  ) {
    return {
      category: ErrorCategory.SERVICE_UNAVAILABLE,
      retryable: true,
      userMessage: 'Service temporarily unavailable',
      suggestedAction: 'The service is experiencing issues. Please try again in a few minutes',
    };
  }

  // Empty/Invalid response
  if (
    errorMessage.includes('no results') ||
    errorMessage.includes('empty response') ||
    errorMessage.includes('no data')
  ) {
    return {
      category: ErrorCategory.EMPTY_RESPONSE,
      retryable: false,
      userMessage: 'No results found',
      suggestedAction: 'Try rephrasing your question or using different search terms',
    };
  }

  // Invalid input
  if (
    errorMessage.includes('invalid') ||
    errorMessage.includes('validation') ||
    errorMessage.includes('bad request') ||
    errorMessage.includes('400')
  ) {
    return {
      category: ErrorCategory.INVALID_INPUT,
      retryable: false,
      userMessage: 'Invalid request',
      suggestedAction: 'Please check your input and try again',
    };
  }

  // Default: Unknown error
  return {
    category: ErrorCategory.UNKNOWN,
    retryable: true,
    userMessage: error instanceof Error ? error.message : 'An unexpected error occurred',
    suggestedAction: 'Please try again. If the problem persists, contact support',
  };
}

// ============================================================================
// RETRY LOGIC
// ============================================================================

/** Maximum number of retry attempts */
const MAX_RETRIES = 3;

/** Base delay for exponential backoff (ms) */
const RETRY_DELAY_BASE = 1000;

/** Maximum delay between retries (ms) */
const MAX_RETRY_DELAY = 10000;

/**
 * Sleep for specified duration
 * @param ms - Milliseconds to sleep
 */
const sleep = (ms: number): Promise<void> =>
  new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Calculate exponential backoff delay with jitter
 * @param attempt - Current attempt number (0-indexed)
 * @returns Delay in milliseconds
 */
function calculateBackoff(attempt: number): number {
  const exponentialDelay = RETRY_DELAY_BASE * Math.pow(2, attempt);
  const jitter = Math.random() * 1000; // Random jitter to prevent thundering herd
  const delay = Math.min(exponentialDelay + jitter, MAX_RETRY_DELAY);
  return delay;
}

/**
 * Retry configuration options
 */
interface RetryOptions {
  maxRetries?: number;
  baseDelay?: number;
  shouldRetry?: (error: unknown) => boolean;
  onRetry?: (attempt: number, error: unknown) => void;
}

/**
 * Execute function with retry logic and exponential backoff
 * 
 * @param fn - Async function to execute
 * @param operation - Description of operation for logging
 * @param options - Retry configuration options
 * @returns Result of successful execution
 * @throws Last error if all retries fail
 * 
 * @example
 * ```typescript
 * const result = await withRetry(
 *   () => index.query({ data: "test", topK: 3 }),
 *   'Vector search',
 *   { maxRetries: 3 }
 * );
 * ```
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  operation: string,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = MAX_RETRIES,
    shouldRetry = (error: unknown) => {
      const info = classifyError(error);
      return info.retryable;
    },
    onRetry,
  } = options;

  let lastError: unknown;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      // Attempt the operation
      return await fn();
    } catch (error) {
      lastError = error;
      const errorInfo = classifyError(error);

      // Don't retry if error is not retryable
      if (!shouldRetry(error)) {
        console.error(
          `❌ ${operation} failed with non-retryable error [${errorInfo.category}]:`,
          error instanceof Error ? error.message : String(error)
        );
        throw error;
      }

      // Don't retry on last attempt
      if (attempt >= maxRetries - 1) {
        break;
      }

      const delay = calculateBackoff(attempt);
      
      console.warn(
        `⚠️  ${operation} failed (attempt ${attempt + 1}/${maxRetries}) [${errorInfo.category}]: ${
          error instanceof Error ? error.message : String(error)
        }. Retrying in ${Math.round(delay)}ms...`
      );

      // Call retry callback if provided
      if (onRetry) {
        onRetry(attempt, error);
      }

      await sleep(delay);
    }
  }

  // All retries failed
  const errorInfo = classifyError(lastError);
  const finalError = new Error(
    `${operation} failed after ${maxRetries} attempts [${errorInfo.category}]: ${errorInfo.userMessage}`
  );
  
  console.error('❌ All retry attempts exhausted:', finalError.message);
  throw finalError;
}

// ============================================================================
// UPSTASH VECTOR SPECIFIC ERROR HANDLING
// ============================================================================

/**
 * Wrap Upstash Vector query with comprehensive error handling
 * 
 * @param queryFn - Function that performs the vector query
 * @param queryDescription - Description of the query for logging
 * @returns Query results with error handling
 * 
 * @example
 * ```typescript
 * const results = await safeVectorQuery(
 *   () => index.query({ data: question, topK: 3, includeMetadata: true }),
 *   'Food search query'
 * );
 * ```
 */
export async function safeVectorQuery<T>(
  queryFn: () => Promise<T>,
  queryDescription: string
): Promise<T> {
  try {
    const result = await withRetry(
      queryFn,
      `Upstash Vector query: ${queryDescription}`,
      {
        maxRetries: 3,
        onRetry: (attempt) => {
          console.warn(`Retry attempt ${attempt + 1} for: ${queryDescription}`);
        },
      }
    );

    // Validate result
    if (!result) {
      throw new UpstashVectorError(
        'Vector query returned null or undefined',
        ErrorCategory.EMPTY_RESPONSE,
        false
      );
    }

    return result;
  } catch (error) {
    const errorInfo = classifyError(error);
    
    throw new UpstashVectorError(
      `Vector query failed: ${errorInfo.userMessage}`,
      errorInfo.category,
      errorInfo.retryable,
      undefined,
      error
    );
  }
}

// ============================================================================
// GROQ API SPECIFIC ERROR HANDLING
// ============================================================================

/**
 * Wrap Groq API calls with comprehensive error handling
 * 
 * @param apiFn - Function that calls Groq API
 * @param apiDescription - Description of the API call for logging
 * @returns API response with error handling
 * 
 * @example
 * ```typescript
 * const completion = await safeGroqAPI(
 *   () => groq.chat.completions.create({ messages, model, ... }),
 *   'Food query completion'
 * );
 * ```
 */
export async function safeGroqAPI<T>(
  apiFn: () => Promise<T>,
  apiDescription: string
): Promise<T> {
  try {
    const result = await withRetry(
      apiFn,
      `Groq API call: ${apiDescription}`,
      {
        maxRetries: 3,
        onRetry: (attempt) => {
          console.warn(`Retry attempt ${attempt + 1} for: ${apiDescription}`);
        },
      }
    );

    // Validate result
    if (!result) {
      throw new GroqAPIError(
        'Groq API returned null or undefined',
        ErrorCategory.EMPTY_RESPONSE,
        false
      );
    }

    return result;
  } catch (error) {
    const errorInfo = classifyError(error);
    
    throw new GroqAPIError(
      `Groq API call failed: ${errorInfo.userMessage}`,
      errorInfo.category,
      errorInfo.retryable,
      undefined,
      error
    );
  }
}

// ============================================================================
// LOGGING UTILITIES
// ============================================================================

/**
 * Structured logger with different log levels
 */
export const logger = {
  /**
   * Log informational messages
   */
  info: (message: string, data?: Record<string, unknown>) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ℹ️  ${message}`, data ? JSON.stringify(data, null, 2) : '');
  },

  /**
   * Log error messages
   */
  error: (message: string, error?: unknown) => {
    const timestamp = new Date().toISOString();
    const errorMsg = error instanceof Error ? error.message : String(error);
    const stack = error instanceof Error ? error.stack : undefined;
    console.error(`[${timestamp}] ❌ ${message}`, errorMsg);
    if (stack && process.env.NODE_ENV === 'development') {
      console.error('Stack trace:', stack);
    }
  },

  /**
   * Log warning messages
   */
  warn: (message: string, data?: Record<string, unknown>) => {
    const timestamp = new Date().toISOString();
    console.warn(`[${timestamp}] ⚠️  ${message}`, data ? JSON.stringify(data, null, 2) : '');
  },

  /**
   * Log debug messages (only in development)
   */
  debug: (message: string, data?: Record<string, unknown>) => {
    if (process.env.NODE_ENV === 'development') {
      const timestamp = new Date().toISOString();
      console.debug(`[${timestamp}] 🔍 ${message}`, data ? JSON.stringify(data, null, 2) : '');
    }
  },

  /**
   * Log performance metrics
   */
  perf: (operation: string, durationMs: number, data?: Record<string, unknown>) => {
    const timestamp = new Date().toISOString();
    console.log(
      `[${timestamp}] ⚡ ${operation} completed in ${durationMs}ms`,
      data ? JSON.stringify(data, null, 2) : ''
    );
  },
};
