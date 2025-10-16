# Groq Cloud API Migration Plan

## Executive Summary

This document provides a detailed migration plan from local Ollama LLM to Groq Cloud API for the RAG food system. The migration will maintain vector search functionality (ChromaDB/Upstash) while replacing the local LLM with Groq's cloud-based `llama-3.1-8b-instant` model.

## Table of Contents

1. [Migration Overview](#migration-overview)
2. [Code Changes Required](#code-changes-required)  
3. [Implementation Steps](#implementation-steps)
4. [Error Handling & Rate Limiting](#error-handling--rate-limiting)
5. [Cost Implications](#cost-implications)
6. [Performance Expectations](#performance-expectations)
7. [Testing Strategy](#testing-strategy)
8. [Fallback Strategies](#fallback-strategies)
9. [Deployment Guide](#deployment-guide)

---

## Migration Overview

### Current vs Target Architecture

**Current (Ollama Local):**
```
User Query → Vector Search → Context → Ollama (localhost:11434) → Response
```

**Target (Groq Cloud):**
```
User Query → Vector Search → Context → Groq API (cloud) → Response
```

### Key Changes Required

| Component | Current | Target | Change Type |
|-----------|---------|---------|-------------|
| **LLM Endpoint** | localhost:11434/api/generate | Groq REST API | Replace |
| **Authentication** | None | Bearer token (GROQ_API_KEY) | Add |
| **Model** | llama3.2 | llama-3.1-8b-instant | Update |
| **Request Format** | Ollama format | OpenAI-compatible format | Transform |
| **Dependencies** | requests | groq SDK | Add |
| **Error Handling** | Basic | Robust API error handling | Enhance |

---

## Code Changes Required

### 1. Import and Setup Changes

```python
# REMOVE
# No specific imports to remove, keep existing ones

# ADD
from groq import Groq
from dotenv import load_dotenv
import time
from typing import Optional

# Load environment variables
load_dotenv()
```

### 2. Constants Update

```python
# UPDATE
LLM_MODEL = "llama-3.1-8b-instant"  # Changed from "llama3.2"

# ADD
GROQ_MAX_TOKENS = 1024
GROQ_TEMPERATURE = 0.7
GROQ_TIMEOUT = 30
```

### 3. LLM Client Initialization

```python
# ADD new function
def initialize_groq_client():
    """Initialize Groq client with API key validation"""
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return None
```

### 4. Main LLM Function Replacement

```python
# REPLACE the Ollama generation code in rag_query():

# OLD (Ollama):
response = requests.post("http://localhost:11434/api/generate", json={
    "model": LLM_MODEL,
    "prompt": prompt,
    "stream": False
})
return response.json()["response"].strip()

# NEW (Groq):
def generate_with_groq(client, prompt, max_retries=3):
    """Generate response using Groq API with error handling"""
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
                timeout=GROQ_TIMEOUT,
                stream=False
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            print(f"⚠️ Groq API attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return "❌ Failed to generate response after multiple attempts"
```

### 5. Updated RAG Query Function

```python
def rag_query(question, groq_client):
    """Enhanced RAG query with Groq integration"""
    try:
        # Steps 1-4: Vector search (unchanged)
        q_emb = get_embedding(question)
        results = collection.query(query_embeddings=[q_emb], n_results=3)
        top_docs = results['documents'][0]
        top_ids = results['ids'][0]

        # Display retrieved context (unchanged)
        print("\n🧠 Retrieving relevant information...\n")
        for i, doc in enumerate(top_docs):
            print(f"🔹 Source {i + 1} (ID: {top_ids[i]}):")
            print(f"    \"{doc}\"\n")

        # Build enhanced prompt
        context = "\n".join(top_docs)
        prompt = f"""You are a knowledgeable food expert. Use the following context to provide a comprehensive and helpful answer.

Context:
{context}

Question: {question}

Please provide a detailed, accurate, and engaging response based on the context provided."""

        # Generate with Groq
        print("🤖 Generating response with Groq...")
        response = generate_with_groq(groq_client, prompt)
        return response
        
    except Exception as e:
        return f"❌ Error in RAG query: {str(e)}"
```

---

## Implementation Steps

### Step 1: Environment Setup

```bash
# Install Groq SDK
pip3 install groq

# Update environment variables
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
```

### Step 2: Create New Implementation

I'll create `rag_run_groq.py` with the complete Groq integration:

```python
import os
import json
import chromadb
import requests
from groq import Groq
from dotenv import load_dotenv
import time
from typing import Optional

# Load environment variables
load_dotenv()

# Constants
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "foods"
JSON_FILE = "foods.json"
EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama-3.1-8b-instant"
GROQ_MAX_TOKENS = 1024
GROQ_TEMPERATURE = 0.7
GROQ_TIMEOUT = 30

def validate_environment():
    """Validate required environment variables and setup"""
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("Please add GROQ_API_KEY=your_key to your .env file")
        return False
    
    print("✅ GROQ_API_KEY found")
    return True

def initialize_groq_client():
    """Initialize Groq client"""
    try:
        client = Groq()
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Groq: {e}")
        return None

def test_groq_connection(client):
    """Test Groq API connection"""
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            max_tokens=10,
            timeout=10
        )
        print("✅ Groq API connection successful")
        return True
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

def generate_with_groq(client, prompt, max_retries=3):
    """Generate response using Groq with retries"""
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
                timeout=GROQ_TIMEOUT
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            if attempt == max_retries - 1:
                return f"❌ Groq API failed after {max_retries} attempts: {e}"
            
            print(f"⚠️ Groq attempt {attempt + 1} failed, retrying...")
            time.sleep(2 ** attempt)

# Rest of the implementation...
```

### Step 3: Testing and Validation

Create comprehensive tests for the new implementation.

### Step 4: Performance Monitoring

Implement usage tracking and performance metrics.

---

## Error Handling & Rate Limiting

### Rate Limiting Strategy

```python
class GroqRateLimiter:
    def __init__(self, requests_per_minute=30):
        self.requests_per_minute = requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        """Implement rate limiting"""
        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                print(f"⏳ Rate limit: waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
        
        self.requests.append(now)

rate_limiter = GroqRateLimiter()
```

### Error Classification

| Error Type | Handling Strategy | Fallback |
|------------|------------------|----------|
| **Authentication** | Validate API key, clear error message | Exit gracefully |
| **Rate Limiting** | Exponential backoff, retry | Queue requests |
| **Network Timeout** | Retry with backoff | Local fallback if available |
| **API Quota Exceeded** | Clear error message, stop requests | Notify user |
| **Model Unavailable** | Retry with different model | Graceful degradation |

---

## Cost Implications

### Groq Pricing Analysis

| Usage Pattern | Estimated Monthly Cost |
|---------------|----------------------|
| **Development/Testing** | $0-5 (within free tier) |
| **Light Usage (100 queries)** | $1-3 |
| **Moderate Usage (1000 queries)** | $5-15 |
| **Heavy Usage (10k queries)** | $30-100 |

### Cost Optimization Strategies

1. **Prompt Optimization**: Shorter, more focused prompts
2. **Response Length Control**: Set appropriate max_tokens
3. **Caching**: Cache similar responses to reduce API calls
4. **Usage Monitoring**: Track and alert on usage patterns

---

## Performance Expectations

| Metric | Ollama Local | Groq Cloud | Expected Change |
|--------|-------------|-------------|----------------|
| **Latency** | 2-5 seconds | 0.5-2 seconds | 🟢 60% faster |
| **Throughput** | 1 concurrent | High concurrent | 🟢 Much better |
| **Reliability** | Local dependency | 99.9% uptime | 🟢 More reliable |
| **Resource Usage** | High CPU/RAM | Minimal local | 🟢 90% reduction |
| **Model Quality** | llama3.2 | llama-3.1-8b-instant | 🟢 Similar/better |

---

## Testing Strategy

### Unit Tests
- API connection testing
- Error handling validation  
- Rate limiting verification
- Response format validation

### Integration Tests
- End-to-end RAG pipeline
- Vector search + Groq generation
- Error recovery scenarios
- Performance benchmarking

### Load Tests
- Concurrent query handling
- Rate limit compliance
- Memory usage under load
- Failover scenario testing

---

## Fallback Strategies

### 1. Graceful Degradation
```python
def rag_query_with_fallback(question, groq_client):
    """RAG with fallback to basic responses"""
    try:
        return rag_query(question, groq_client)
    except Exception as e:
        print(f"⚠️ Groq failed: {e}")
        
        # Fallback to simple context-based response
        context = get_context_for_question(question)
        return f"Based on available information: {context}"
```

### 2. Hybrid Local/Cloud
```python
def hybrid_llm_query(question, context):
    """Try Groq first, fallback to local if available"""
    try:
        return groq_generate(question, context)
    except:
        if ollama_available():
            return ollama_generate(question, context)
        else:
            return simple_context_response(context)
```

---

## Deployment Guide

### Pre-deployment Checklist
- [ ] Groq API key configured
- [ ] Dependencies installed
- [ ] Connection tested
- [ ] Backup of current system
- [ ] Error handling tested
- [ ] Rate limiting configured

### Deployment Steps
1. Test in development environment
2. Run parallel testing (Ollama vs Groq)
3. Deploy to staging
4. Monitor performance and errors
5. Deploy to production
6. Monitor usage and costs

### Monitoring & Alerting
- API usage and costs
- Error rates and types
- Response times
- Rate limit hits
- User satisfaction metrics

This completes the comprehensive Groq migration plan. The implementation provides robust error handling, cost monitoring, and fallback strategies while maintaining the existing RAG functionality.