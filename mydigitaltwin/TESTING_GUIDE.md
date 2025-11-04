# 🧪 Testing Guide - Food RAG System

## Testing Your Error Handling Implementation

This guide provides step-by-step instructions to verify that the new error handling, retry logic, logging, and caching are working correctly.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Test Scenarios](#test-scenarios)
3. [Testing Checklist](#testing-checklist)
4. [Expected Outputs](#expected-outputs)
5. [Performance Testing](#performance-testing)
6. [Integration Testing](#integration-testing)

---

## 🚀 Quick Start

### Start the Development Server

```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm run dev
```

Server should start on: `http://localhost:3000`

### Watch the Console

Open your terminal to see real-time logs:
- ℹ️ Info messages (query processing)
- ⚡ Performance metrics
- ❌ Error messages
- ⚠️ Warnings and retries
- 🐛 Debug output (development mode)

---

## 🎯 Test Scenarios

### Test 1: Valid Query (Happy Path)

**Goal**: Verify normal operation with successful response

**Action**:
```typescript
// In browser console or test file
const result = await fetch('/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: "What is Biryani?" })
}).then(r => r.json());

console.log(result);
```

**Expected Result**:
```json
{
  "success": true,
  "answer": "Biryani is a flavorful Indian rice dish...",
  "context": [
    "Biryani (Main Course from Hyderabad): A fragrant rice dish...",
    "..."
  ],
  "metadata": {
    "searchResults": 3,
    "model": "llama-3.1-8b-instant",
    "processingTime": 1250,
    "cached": false,
    "vectorSearchTime": 245,
    "aiGenerationTime": 754
  }
}
```

**Console Output**:
```
[2025-01-15T10:30:45.123Z] ℹ️  Processing food query { "question": "What is Biryani?", "length": 17 }
[2025-01-15T10:30:45.368Z] ⚡ Vector search completed in 245ms { "resultsCount": 3 }
[2025-01-15T10:30:46.122Z] ⚡ AI response generation completed in 754ms { "answerLength": 412, "tokensUsed": 156 }
[2025-01-15T10:30:46.125Z] ⚡ Complete food query completed in 1002ms { "vectorSearchTime": 245, "aiGenerationTime": 754, "cached": false }
```

**Validation**:
- ✅ `success: true`
- ✅ `answer` is a non-empty string
- ✅ `metadata` includes all timing metrics
- ✅ Console shows all performance logs

---

### Test 2: Cache Hit

**Goal**: Verify caching works and improves performance

**Action**: Send the **same question twice**

```typescript
// First query
const result1 = await fetch('/api/query', {
  method: 'POST',
  body: JSON.stringify({ question: "What is Biryani?" })
}).then(r => r.json());

console.log('First query time:', result1.metadata.processingTime);

// Second query (same question)
const result2 = await fetch('/api/query', {
  method: 'POST',
  body: JSON.stringify({ question: "What is Biryani?" })
}).then(r => r.json());

console.log('Second query time:', result2.metadata.processingTime);
```

**Expected Result**:
- First query: ~1000-2000ms
- Second query: ~5-15ms (99% faster!)

**Console Output**:
```
[timestamp] ℹ️  Processing food query { "question": "What is Biryani?", "length": 17 }
[timestamp] ⚡ Vector search completed in 245ms
[timestamp] ⚡ AI response generation completed in 754ms
[timestamp] 💾 Cache STORE for: "what is biryani?"
[timestamp] ⚡ Complete food query completed in 1002ms { "cached": false }

[timestamp] ℹ️  Processing food query { "question": "What is Biryani?", "length": 17 }
[timestamp] 💾 Cache HIT for: "what is biryani?" (age: 2s)
[timestamp] ⚡ Complete food query completed in 8ms { "cached": true }
```

**Validation**:
- ✅ First query: `cached: false`
- ✅ Second query: `cached: true`
- ✅ Second query is dramatically faster
- ✅ Console shows "Cache HIT" message

---

### Test 3: Input Validation

**Goal**: Verify input validation prevents bad requests

**Test 3A: Empty Input**

```typescript
const result = await fetch('/api/query', {
  method: 'POST',
  body: JSON.stringify({ question: "" })
}).then(r => r.json());

console.log(result);
```

**Expected Result**:
```json
{
  "success": false,
  "error": "Question cannot be empty"
}
```

**Test 3B: Whitespace Only**

```typescript
const result = await fetch('/api/query', {
  method: 'POST',
  body: JSON.stringify({ question: "   " })
}).then(r => r.json());
```

**Expected Result**:
```json
{
  "success": false,
  "error": "Question cannot be empty"
}
```

**Test 3C: Too Long Input**

```typescript
const longQuestion = "x".repeat(600);  // 600 characters
const result = await fetch('/api/query', {
  method: 'POST',
  body: JSON.stringify({ question: longQuestion })
}).then(r => r.json());
```

**Expected Result**:
```json
{
  "success": false,
  "error": "Question too long (maximum 500 characters)"
}
```

**Validation**:
- ✅ All return `success: false`
- ✅ Error messages are user-friendly
- ✅ No API calls are made (fast failure)

---

### Test 4: Category Search

**Goal**: Test category-based search with validation

**Test 4A: Valid Category**

```typescript
import { searchByCategory } from '@/src/actions/foodRagActions';

const result = await searchByCategory("Dessert", 10);
console.log(result);
```

**Expected Result**:
```json
{
  "success": true,
  "results": [
    {
      "name": "Gulab Jamun",
      "category": "Dessert",
      "region": "India",
      "description": "Sweet fried balls soaked in sugar syrup",
      "score": 0.8523
    },
    // ... more desserts
  ],
  "metadata": {
    "searchResults": 10,
    "processingTime": 235
  }
}
```

**Test 4B: Invalid Category**

```typescript
const result = await searchByCategory("", 10);
```

**Expected Result**:
```json
{
  "success": false,
  "error": "Category is required"
}
```

**Test 4C: Invalid Limit**

```typescript
const result = await searchByCategory("Dessert", 150);  // Exceeds max 100
```

**Expected Result**:
```json
{
  "success": false,
  "error": "Limit must be between 1 and 100"
}
```

**Validation**:
- ✅ Valid inputs work correctly
- ✅ Invalid inputs fail with clear messages
- ✅ Results match category filter

---

### Test 5: Recommendations

**Goal**: Test personalized recommendations

**Action**:
```typescript
import { getFoodRecommendations } from '@/src/actions/foodRagActions';

const result = await getFoodRecommendations("healthy vegetarian breakfast");
console.log(result);
```

**Expected Result**:
```json
{
  "success": true,
  "recommendations": "Based on your preference for healthy vegetarian breakfast, I recommend:\n\n1. Idli - Steamed rice cakes...\n2. Upma - Semolina breakfast dish...\n3. Poha - Flattened rice...",
  "metadata": {
    "searchResults": 5,
    "processingTime": 1450,
    "vectorSearchTime": 280,
    "aiGenerationTime": 920
  }
}
```

**Console Output**:
```
[timestamp] ℹ️  Generating food recommendations { "preferences": "healthy vegetarian breakfast" }
[timestamp] ⚡ Vector search completed in 280ms { "resultsCount": 5 }
[timestamp] ⚡ AI response generation completed in 920ms
[timestamp] ⚡ Food recommendations completed in 1450ms
```

**Validation**:
- ✅ Returns AI-generated recommendations
- ✅ Matches user preferences
- ✅ Performance metrics logged

---

### Test 6: Error Scenarios (Simulated)

**Goal**: Verify error handling works for various error types

**Note**: These tests require temporarily modifying environment variables or code

**Test 6A: Invalid API Key**

1. Temporarily change `.env.local`:
```bash
GROQ_API_KEY="invalid-key-test"
```

2. Restart server: `npm run dev`

3. Make a query:
```typescript
const result = await fetch('/api/query', {
  method: 'POST',
  body: JSON.stringify({ question: "What is Biryani?" })
}).then(r => r.json());
```

**Expected Result**:
```json
{
  "success": false,
  "error": "Authentication failed"
}
```

**Console Output**:
```
[timestamp] ❌ Query failed [AUTH]: Invalid API key
```

4. **Restore correct API key** and restart

**Test 6B: Network Error Simulation**

Modify `src/lib/errorHandling.ts` temporarily:

```typescript
// In safeVectorQuery, add before the actual query:
throw new Error('ECONNREFUSED');  // Simulate network error
```

Make a query and observe:

**Expected Behavior**:
- 3 retry attempts
- Increasing delays between attempts
- Final error message: "Network connection error"

**Console Output**:
```
[timestamp] ⚠️  Vector search failed (attempt 1/3): ECONNREFUSED - retrying in 1000ms
[timestamp] ⚠️  Vector search failed (attempt 2/3): ECONNREFUSED - retrying in 2000ms
[timestamp] ⚠️  Vector search failed (attempt 3/3): ECONNREFUSED - retrying in 4000ms
[timestamp] ❌ Query failed [NETWORK]: ECONNREFUSED
```

**Remove the test code** after verification

---

## ✅ Testing Checklist

Use this checklist to verify all features:

### Basic Functionality
- [ ] Normal query returns valid response
- [ ] Response includes answer, context, and metadata
- [ ] Processing time is logged
- [ ] Vector search and AI generation times are tracked

### Caching
- [ ] First query is slow (~1-2 seconds)
- [ ] Second identical query is fast (<20ms)
- [ ] Cache hit is logged with age
- [ ] Different questions don't share cache

### Input Validation
- [ ] Empty question returns validation error
- [ ] Whitespace-only question returns validation error
- [ ] Too-long question (>500 chars) returns validation error
- [ ] Invalid category returns validation error
- [ ] Invalid limit (<1 or >100) returns validation error

### Error Handling
- [ ] Invalid API key shows authentication error
- [ ] Network errors trigger retry logic
- [ ] Retries use exponential backoff
- [ ] Non-retryable errors fail immediately
- [ ] All errors return user-friendly messages

### Logging
- [ ] Info logs show query processing
- [ ] Performance logs show timing metrics
- [ ] Error logs show failures with category
- [ ] Debug logs show detailed info (dev mode)
- [ ] All logs include timestamps

### Performance
- [ ] Cached queries < 20ms
- [ ] Uncached vector search: 200-400ms
- [ ] Uncached AI generation: 500-1500ms
- [ ] Total uncached: 700-1900ms
- [ ] No memory leaks over 100+ queries

---

## 📊 Expected Outputs

### Successful Query Output

```json
{
  "success": true,
  "answer": "Detailed answer about the food item...",
  "context": [
    "Context item 1 with food description",
    "Context item 2 with origin and category",
    "Context item 3 with ingredients"
  ],
  "metadata": {
    "searchResults": 3,
    "model": "llama-3.1-8b-instant",
    "processingTime": 1250,
    "cached": false,
    "vectorSearchTime": 245,
    "aiGenerationTime": 754
  }
}
```

### Error Output

```json
{
  "success": false,
  "error": "User-friendly error message with actionable suggestion"
}
```

### Console Logs (Typical Flow)

```
[2025-01-15T10:30:45.123Z] ℹ️  Processing food query { "question": "What is Biryani?", "length": 17 }
[2025-01-15T10:30:45.368Z] 🐛 Search result 1 { "score": 0.8523, "hasName": true, "region": "Hyderabad" }
[2025-01-15T10:30:45.369Z] 🐛 Search result 2 { "score": 0.7891, "hasName": true, "region": "India" }
[2025-01-15T10:30:45.370Z] 🐛 Search result 3 { "score": 0.7234, "hasName": true, "region": "South Asia" }
[2025-01-15T10:30:45.371Z] ⚡ Vector search completed in 245ms { "resultsCount": 3 }
[2025-01-15T10:30:46.122Z] ⚡ AI response generation completed in 754ms { "answerLength": 412, "tokensUsed": 156 }
[2025-01-15T10:30:46.125Z] 💾 Cache STORE for: "what is biryani?"
[2025-01-15T10:30:46.126Z] ⚡ Complete food query completed in 1002ms { "vectorSearchTime": 245, "aiGenerationTime": 754, "cached": false }
```

---

## ⚡ Performance Testing

### Load Test (100 Queries)

```typescript
// Test script
async function loadTest() {
  const questions = [
    "What is Biryani?",
    "Tell me about Sushi",
    "What are Indian desserts?",
    // ... 97 more
  ];

  const startTime = Date.now();
  
  for (const question of questions) {
    const result = await fetch('/api/query', {
      method: 'POST',
      body: JSON.stringify({ question })
    }).then(r => r.json());
    
    console.log(`${question}: ${result.metadata?.processingTime}ms`);
  }
  
  const totalTime = Date.now() - startTime;
  console.log(`Total time: ${totalTime}ms`);
  console.log(`Average: ${totalTime / questions.length}ms per query`);
}

loadTest();
```

**Expected Results**:
- First 100 queries: Mix of cached and uncached
- Cache hits should be <20ms
- Cache misses should be 700-1900ms
- No memory leaks
- No rate limit errors (with reasonable timing)

---

## 🔗 Integration Testing

### Test MCP Server Integration

```bash
# Test MCP server directly
cd /Users/DELL/ragfood/mydigitaltwin
node dist/mcp-server/index.js
```

Send test messages via Claude Desktop or MCP client.

### Test API Route

```bash
# Using curl
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Biryani?"}'
```

**Expected**: JSON response with `success: true`

---

## 🐛 Troubleshooting Tests

### Issue: Tests Fail with "Cannot find module"

**Solution**:
```bash
npm install
npm run build:mcp
```

### Issue: API Returns 500 Error

**Check**:
1. Environment variables set correctly
2. Python script exists and is executable
3. Console shows detailed error logs

### Issue: No Console Logs Appearing

**Solution**:
```bash
# Ensure running in development mode
export NODE_ENV=development
npm run dev
```

### Issue: Cache Not Working

**Check**:
1. Questions are identical (case-insensitive)
2. Cache duration hasn't expired (5 minutes)
3. Console shows "Cache STORE" after first query

---

## 📝 Test Report Template

Use this template to document your testing:

```markdown
## Test Report - [Date]

### Environment
- Node version: [version]
- npm version: [version]
- OS: [macOS/Windows/Linux]

### Tests Performed
- [ ] Valid query (happy path)
- [ ] Cache hit
- [ ] Input validation (3 tests)
- [ ] Category search (3 tests)
- [ ] Recommendations
- [ ] Error scenarios

### Results
- Total tests: X
- Passed: Y
- Failed: Z

### Issues Found
1. [Issue description]
   - Severity: High/Medium/Low
   - Steps to reproduce
   - Expected vs Actual

### Performance Metrics
- Average uncached query: Xms
- Average cached query: Yms
- Cache hit rate: Z%

### Recommendations
- [Any improvements needed]
```

---

## ✅ Success Criteria

Your error handling implementation is working correctly if:

1. ✅ All normal queries return valid responses
2. ✅ Caching works and dramatically speeds up repeated queries
3. ✅ Input validation catches all invalid inputs
4. ✅ Errors return user-friendly messages
5. ✅ Retry logic attempts failed requests 3 times
6. ✅ Logs show all operations with timestamps
7. ✅ Performance metrics are tracked accurately
8. ✅ No TypeScript or linting errors
9. ✅ Build succeeds without warnings
10. ✅ Server runs without crashes

---

**Last Updated**: October 30, 2025  
**Version**: 1.0.0  
**Maintained By**: VivianP05
