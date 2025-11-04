# 🛡️ Error Handling Guide - Food RAG System

## Overview

The Food RAG system now includes **comprehensive error handling** for all Upstash Vector queries and Groq AI API calls. This guide explains the error handling architecture, features, and usage patterns.

---

## 📋 Table of Contents

1. [Features](#features)
2. [Error Categories](#error-categories)
3. [Retry Logic](#retry-logic)
4. [Caching System](#caching-system)
5. [Logging](#logging)
6. [Usage Examples](#usage-examples)
7. [Performance Metrics](#performance-metrics)
8. [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Comprehensive Error Handling
- ✅ **Automatic retry logic** with exponential backoff
- ✅ **Error classification** into 10+ categories
- ✅ **User-friendly error messages**
- ✅ **Detailed logging** for debugging
- ✅ **Performance metrics** tracking
- ✅ **Response caching** for improved performance

### Error Detection
- Network failures (ECONNREFUSED, ENOTFOUND, timeouts)
- Authentication errors (401, invalid API keys)
- Rate limiting (429, quota exceeded)
- Service unavailable (500, 502, 503)
- Empty/invalid responses
- Input validation errors

---

## 🏷️ Error Categories

The system classifies errors into the following categories:

### 1. **NETWORK** (Retryable)
- Network connection failures
- DNS resolution errors
- Connection refused

**User Message**: "Network connection error"  
**Suggested Action**: "Please check your internet connection and try again"

### 2. **TIMEOUT** (Retryable)
- Request timeouts
- Operation took too long
- ETIMEDOUT errors

**User Message**: "Request timed out"  
**Suggested Action**: "The service is taking longer than expected. Please try again"

### 3. **AUTH** (Non-retryable)
- Invalid API keys
- Authentication failures
- 401 Unauthorized

**User Message**: "Authentication failed"  
**Suggested Action**: "Please contact support - API credentials may be invalid"

### 4. **RATE_LIMIT** (Retryable)
- Too many requests
- 429 errors
- Rate limit exceeded

**User Message**: "Rate limit exceeded"  
**Suggested Action**: "Too many requests. Please wait a moment and try again"

### 5. **QUOTA_EXCEEDED** (Non-retryable)
- Daily/monthly quota reached
- Usage limit exceeded

**User Message**: "Service quota exceeded"  
**Suggested Action**: "Daily or monthly quota reached. Please try again later"

### 6. **SERVICE_UNAVAILABLE** (Retryable)
- 500, 502, 503 errors
- Backend service down
- Temporary outages

**User Message**: "Service temporarily unavailable"  
**Suggested Action**: "The service is experiencing issues. Please try again in a few minutes"

### 7. **EMPTY_RESPONSE** (Non-retryable)
- No results from vector search
- Empty AI responses
- No data returned

**User Message**: "No results found"  
**Suggested Action**: "Try rephrasing your question or using different search terms"

### 8. **INVALID_INPUT** (Non-retryable)
- Validation errors
- Bad request (400)
- Invalid parameters

**User Message**: "Invalid request"  
**Suggested Action**: "Please check your input and try again"

### 9. **DATABASE_ERROR** (Retryable)
- Database connection issues
- Query execution errors

### 10. **UNKNOWN** (Retryable)
- Unexpected errors
- Unclassified failures

**User Message**: Error message from exception  
**Suggested Action**: "Please try again. If the problem persists, contact support"

---

## 🔄 Retry Logic

### Exponential Backoff Strategy

The system uses **exponential backoff with jitter** to retry failed operations:

```typescript
Attempt 1: Wait 1s + random(0-1s) = 1-2s
Attempt 2: Wait 2s + random(0-1s) = 2-3s
Attempt 3: Wait 4s + random(0-1s) = 4-5s
Maximum: 10 seconds between retries
```

### Retry Configuration

```typescript
{
  maxRetries: 3,           // Maximum retry attempts
  baseDelay: 1000,         // 1 second base delay
  maxDelay: 10000,         // 10 second max delay
  shouldRetry: (error) =>  // Only retry if error is retryable
}
```

### Retryable vs Non-Retryable Errors

**Retryable** (will automatically retry):
- Network errors
- Timeouts
- Rate limits
- Service unavailable (5xx)
- Unknown errors

**Non-Retryable** (fail immediately):
- Authentication errors
- Quota exceeded
- Invalid input
- Empty responses

---

## 💾 Caching System

### Cache Configuration

```typescript
{
  duration: 5 minutes (300,000ms),
  maxSize: 100 entries,
  eviction: LRU (Least Recently Used)
}
```

### How It Works

1. **Cache Key**: Lowercase, trimmed question text
2. **Cache Hit**: Returns cached response immediately
3. **Cache Miss**: Performs full RAG query and caches result
4. **Cache Eviction**: When cache is full, oldest entry is removed

### Cache Metrics

Logged messages:
- `💾 Cache HIT for: "question..." (age: Xs)`
- `💾 Cache STORE for: "question..."`
- `🗑️ Cache evicted oldest entry (size limit: 100)`

---

## 📊 Logging

### Log Levels

#### **INFO** (`logger.info`)
- Query processing started
- Cache hits
- Successful completions

```typescript
logger.info('Processing food query', { 
  question: "What is Biryani?",
  length: 17 
});
```

#### **ERROR** (`logger.error`)
- Query failures
- API errors
- Exceptions

```typescript
logger.error('Query failed [NETWORK]', error);
```

#### **WARN** (`logger.warn`)
- Retry attempts
- Input validation warnings
- Cache evictions

```typescript
logger.warn('Question exceeds maximum length', { 
  length: 550 
});
```

#### **DEBUG** (`logger.debug`)
- Detailed operation info (development only)
- Search results
- Context building

```typescript
logger.debug('Search result 1', {
  score: 0.8523,
  hasName: true
});
```

#### **PERF** (`logger.perf`)
- Performance metrics
- Operation timings

```typescript
logger.perf('Vector search', 245, { 
  resultsCount: 3 
});
```

### Log Format

```
[2025-01-15T10:30:45.123Z] ℹ️  Processing food query { "question": "What is Biryani?", "length": 17 }
[2025-01-15T10:30:45.368Z] ⚡ Vector search completed in 245ms { "resultsCount": 3 }
[2025-01-15T10:30:46.122Z] ⚡ AI response generation completed in 754ms { "answerLength": 412, "tokensUsed": 156 }
[2025-01-15T10:30:46.125Z] ⚡ Complete food query completed in 1002ms { "vectorSearchTime": 245, "aiGenerationTime": 754, "cached": false }
```

---

## 💻 Usage Examples

### Example 1: Basic Query with Error Handling

```typescript
import { queryFoodRAG } from '@/src/actions/foodRagActions';

const result = await queryFoodRAG("What is Biryani?");

if (result.success) {
  console.log('Answer:', result.answer);
  console.log('Processing time:', result.metadata?.processingTime, 'ms');
  console.log('Was cached:', result.metadata?.cached);
} else {
  console.error('Error:', result.error);
  // Error message is user-friendly and actionable
}
```

### Example 2: Category Search

```typescript
import { searchByCategory } from '@/src/actions/foodRagActions';

const result = await searchByCategory("Dessert", 10);

if (result.success) {
  result.results?.forEach(food => {
    console.log(`${food.name} from ${food.region}: ${food.description}`);
  });
} else {
  console.error('Search failed:', result.error);
}
```

### Example 3: Personalized Recommendations

```typescript
import { getFoodRecommendations } from '@/src/actions/foodRagActions';

const result = await getFoodRecommendations("healthy vegetarian breakfast");

if (result.success) {
  console.log('Recommendations:', result.recommendations);
} else {
  console.error('Failed to generate recommendations:', result.error);
}
```

### Example 4: Direct Use of Safe Wrappers

```typescript
import { safeVectorQuery, safeGroqAPI } from '@/src/lib/errorHandling';
import { index } from '@/src/actions/foodRagActions';

// Safe vector query with automatic retry
const results = await safeVectorQuery(
  async () => {
    return await index.query({
      data: "spicy Indian food",
      topK: 5,
      includeMetadata: true,
    });
  },
  'Spicy food search'
);

// Safe Groq API call with automatic retry
const completion = await safeGroqAPI(
  async () => {
    return await groq.chat.completions.create({
      messages: [...],
      model: "llama-3.1-8b-instant",
    });
  },
  'Food description generation'
);
```

---

## ⚡ Performance Metrics

### Tracked Metrics

All operations track the following metrics:

```typescript
{
  processingTime: 1250,        // Total time (ms)
  vectorSearchTime: 245,       // Vector search only (ms)
  aiGenerationTime: 754,       // AI generation only (ms)
  searchResults: 3,            // Number of results
  cached: false,               // Whether from cache
  model: "llama-3.1-8b-instant"
}
```

### Performance Benchmarks

**Average Response Times** (uncached):
- Vector search: 200-400ms
- AI generation: 500-1500ms
- Total: 700-1900ms

**Cached Response Times**:
- Total: 5-15ms (99% faster!)

### Optimization Tips

1. **Use Caching**: Identical questions return instantly
2. **Batch Queries**: Group related searches
3. **Limit Results**: Use appropriate `topK` values (3-5 recommended)
4. **Monitor Logs**: Check `logger.perf` for slow operations

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: "Authentication failed"

**Cause**: Invalid or missing API credentials

**Solution**:
```bash
# Check .env.local file
cat mydigitaltwin/.env.local

# Verify environment variables are set
UPSTASH_VECTOR_REST_URL="https://..."
UPSTASH_VECTOR_REST_TOKEN="..."
GROQ_API_KEY="gsk_..."
```

#### Issue 2: "Rate limit exceeded"

**Cause**: Too many requests to Upstash or Groq

**Solution**:
- Wait 1-2 minutes before retrying
- Implement client-side rate limiting
- Upgrade to higher tier plan if needed

#### Issue 3: "No results found"

**Cause**: Vector search returned no matches

**Solution**:
- Try different search terms
- Make questions more specific
- Check if database has relevant content

#### Issue 4: "Request timed out"

**Cause**: Network latency or service overload

**Solution**:
- System automatically retries (3 attempts)
- Check internet connection
- Wait and try again
- Increase timeout if issue persists

#### Issue 5: "Service temporarily unavailable"

**Cause**: Upstash or Groq backend issues

**Solution**:
- System automatically retries
- Check status pages:
  - Upstash: https://status.upstash.com
  - Groq: https://status.groq.com
- Wait a few minutes and retry

### Debugging Tips

1. **Enable Debug Logging**:
```typescript
// In development, all debug logs are visible
process.env.NODE_ENV = 'development';
```

2. **Check Terminal Output**:
```bash
# Look for error patterns
[timestamp] ❌ Query failed [NETWORK]: ...
[timestamp] ⚠️  Vector search failed (attempt 1/3): ...
```

3. **Inspect Metadata**:
```typescript
const result = await queryFoodRAG("test");
console.log(result.metadata);
// Shows: processingTime, cached, searchResults, etc.
```

4. **Test Individual Components**:
```typescript
// Test vector search only
import { safeVectorQuery } from '@/src/lib/errorHandling';
const results = await safeVectorQuery(...);

// Test AI generation only
import { safeGroqAPI } from '@/src/lib/errorHandling';
const completion = await safeGroqAPI(...);
```

---

## 🧪 Testing Error Handling

### Manual Tests

```typescript
// Test empty input
await queryFoodRAG("");  // Should return validation error

// Test very long input
await queryFoodRAG("x".repeat(600));  // Should return validation error

// Test with invalid category
await searchByCategory("");  // Should return validation error

// Test with invalid limit
await searchByCategory("Dessert", -5);  // Should return validation error
```

### Error Simulation

For testing retry logic, you can temporarily modify the code:

```typescript
// In errorHandling.ts, reduce retries for testing
const MAX_RETRIES = 1;  // Fail faster for testing

// Simulate network error
throw new Error('network error');

// Simulate timeout
throw new Error('ETIMEDOUT');

// Simulate rate limit
throw new Error('rate limit exceeded');
```

---

## 📚 Additional Resources

### Related Files

- **Error Handling Module**: `src/lib/errorHandling.ts`
- **Server Actions**: `src/actions/foodRagActions.ts`
- **MCP Server**: `src/mcp-server/index.ts`
- **API Route**: `app/api/query/route.ts`

### Documentation

- [Upstash Vector Docs](https://upstash.com/docs/vector)
- [Groq API Docs](https://console.groq.com/docs)
- [MCP Specification](https://modelcontextprotocol.io/)

### Status Pages

- [Upstash Status](https://status.upstash.com)
- [Groq Status](https://status.groq.com)

---

## 🎯 Best Practices

1. ✅ **Always check `result.success`** before using data
2. ✅ **Display user-friendly error messages** from `result.error`
3. ✅ **Log errors for debugging** but show clean UI to users
4. ✅ **Use caching** for frequently asked questions
5. ✅ **Monitor performance metrics** to identify slow queries
6. ✅ **Implement graceful degradation** in UI on errors
7. ✅ **Test error scenarios** during development

---

**Last Updated**: October 30, 2025  
**Version**: 2.0.0  
**Maintained By**: VivianP05
