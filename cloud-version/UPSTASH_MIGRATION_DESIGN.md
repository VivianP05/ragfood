# Upstash Vector Database Migration Design Document

## Executive Summary

This document provides a comprehensive design for migrating the existing ChromaDB-based RAG (Retrieval-Augmented Generation) system to Upstash Vector Database. The migration will leverage Upstash's built-in embedding capabilities, serverless architecture, and REST API to create a more scalable and maintainable solution.

## Table of Contents

1. [Architecture Comparison](#architecture-comparison)
2. [Current Implementation Analysis](#current-implementation-analysis)
3. [Upstash Integration Strategy](#upstash-integration-strategy)
4. [Code Structure Changes](#code-structure-changes)
5. [Implementation Plan](#implementation-plan)
6. [Performance and Cost Analysis](#performance-and-cost-analysis)
7. [Error Handling Strategies](#error-handling-strategies)
8. [Security Considerations](#security-considerations)
9. [Testing Strategy](#testing-strategy)
10. [Migration Checklist](#migration-checklist)

---

## Architecture Comparison

### Current Architecture (ChromaDB + Ollama)

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   User Query        │────│    RAG System      │────│   Ollama LLM        │
└─────────────────────┘    │                     │    └─────────────────────┘
                           │  1. Embed Query     │
                           │  2. Vector Search   │
                           │  3. Context Retrieval│
                           │  4. LLM Generation  │
                           └─────────────────────┘
                                      │
                           ┌─────────────────────┐    ┌─────────────────────┐
                           │   Ollama Embedding  │    │    ChromaDB         │
                           │   (mxbai-embed)     │────│  (Local Storage)    │
                           │   localhost:11434   │    │   Persistent Client │
                           └─────────────────────┘    └─────────────────────┘
```

**Current Flow:**
1. Text data → Ollama embedding API → Vector embeddings
2. Embeddings + metadata → ChromaDB local storage
3. Query → Ollama embedding → ChromaDB similarity search → Context retrieval
4. Context + Query → Ollama LLM → Generated response

### Target Architecture (Upstash Vector)

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   User Query        │────│    RAG System      │────│   Ollama LLM        │
└─────────────────────┘    │                     │    └─────────────────────┘
                           │  1. Direct Query    │
                           │  2. Vector Search   │
                           │  3. Context Retrieval│
                           │  4. LLM Generation  │
                           └─────────────────────┘
                                      │
                           ┌─────────────────────┐
                           │   Upstash Vector    │
                           │  Built-in Embedding │
                           │ (mxbai-embed-large) │
                           │  Cloud REST API     │
                           └─────────────────────┘
```

**Target Flow:**
1. Text data → Upstash Vector (auto-embedding) → Stored vectors
2. Query → Upstash Vector (auto-embedding + similarity search) → Context retrieval
3. Context + Query → Ollama LLM → Generated response

### Key Architectural Benefits

| Aspect | ChromaDB | Upstash Vector | Benefit |
|--------|----------|----------------|---------|
| **Embedding Generation** | External Ollama API | Built-in automatic | Simplified pipeline |
| **Storage** | Local filesystem | Cloud-hosted | No local storage management |
| **Scalability** | Single machine | Serverless auto-scale | Better performance |
| **API Calls** | 2 separate calls | 1 unified call | Reduced latency |
| **Maintenance** | Local DB management | Fully managed | Zero maintenance |
| **Deployment** | Requires Ollama + ChromaDB | Only needs API keys | Simpler deployment |

---

## Current Implementation Analysis

### Code Structure Overview

```python
# Current Dependencies
- chromadb: Local vector database
- requests: HTTP client for Ollama API
- json: Data handling
- os: Environment variables

# Key Components
1. ChromaDB persistent client initialization
2. Collection management (get_or_create)
3. Manual embedding generation via Ollama
4. Incremental data upsert with ID tracking
5. Query embedding + similarity search
6. Context formatting for LLM
```

### Data Flow Analysis

```python
# Current Data Pipeline
foods.json → Load JSON → 
  For each item:
    Enhanced text → Ollama embedding → ChromaDB upsert
    
# Current Query Pipeline  
User query → Ollama embedding → ChromaDB query → 
  Top results → Context assembly → LLM prompt → Response
```

### Current Pain Points

1. **Dual API dependency**: Both Ollama (embedding) and ChromaDB (storage)
2. **Local storage management**: ChromaDB persistence and file management
3. **Manual embedding pipeline**: Explicit embedding generation and error handling
4. **Incremental loading complexity**: ID tracking to avoid duplicates
5. **Development environment setup**: Requires Ollama installation and setup

---

## Upstash Integration Strategy

### Upstash Vector Features Alignment

| Feature | Current Need | Upstash Solution |
|---------|--------------|------------------|
| **Automatic Embeddings** | Manual Ollama calls | Built-in mxbai-embed-large-v1 |
| **Persistence** | ChromaDB local files | Cloud-hosted persistence |
| **Similarity Search** | ChromaDB query API | Native cosine similarity |
| **Metadata Storage** | Document + ID storage | Rich metadata support |
| **API Access** | Local network calls | REST API with authentication |

### Integration Architecture

```python
# New Upstash-based Components
1. Index client with environment-based auth
2. Direct text upsert (no manual embeddings)
3. Direct text query (auto-embedding)
4. Simplified error handling
5. Metadata-rich storage
```

### Authentication Strategy

```python
# Environment Variables Required
UPSTASH_VECTOR_REST_URL=your_upstash_url
UPSTASH_VECTOR_REST_TOKEN=your_upstash_token

# Client Initialization
from upstash_vector import Index
index = Index.from_env()  # Auto-loads from environment
```

### Why No Indexing Delays Are Needed

**Upstash Vector handles consistency automatically:**

1. **Built-in Consistency**: Upstash Vector is designed for immediate consistency - when an upsert returns successfully, the data is immediately available for queries
2. **Batch Operations**: Using single batch upserts instead of individual operations eliminates any potential timing issues
3. **Better Performance**: No artificial delays means faster data loading and better user experience
4. **Proper Error Handling**: Instead of delays, we use robust retry logic for actual failures

**Best Practices Without Delays:**
```python
# ✅ GOOD: Batch upsert (recommended)
all_vectors = [(id, text, metadata) for item in data]
index.upsert(vectors=all_vectors)

# ✅ GOOD: Large batches if needed
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)

# ❌ BAD: Individual upserts with delays
for item in data:
    index.upsert(vectors=[(id, text, metadata)])
    time.sleep(0.05)  # Unnecessary!
```

---

## Code Structure Changes

### Import Changes

```python
# REMOVE
import chromadb
import requests  # For Ollama embedding calls

# ADD  
from upstash_vector import Index
from dotenv import load_dotenv
import time  # For indexing delays
```

### Configuration Changes

```python
# REMOVE
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "foods" 
EMBED_MODEL = "mxbai-embed-large"

# ADD
load_dotenv()  # Load environment variables
# Upstash client handles embedding model automatically
```

### Client Initialization Changes

```python
# CURRENT
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# NEW
index = Index.from_env()
# Optional: Reset index for fresh start
# index.reset()
```

### Embedding Function Changes

```python
# REMOVE ENTIRELY
def get_embedding(text):
    response = requests.post("http://localhost:11434/api/embeddings", json={
        "model": EMBED_MODEL,
        "prompt": text
    })
    return response.json()["embedding"]

# NO REPLACEMENT NEEDED - Upstash handles automatically
```

### Data Upsert Changes

```python
# CURRENT
existing_ids = set(collection.get()['ids'])
new_items = [item for item in food_data if item['id'] not in existing_ids]

if new_items:
    for item in new_items:
        enriched_text = item["text"]
        if "region" in item:
            enriched_text += f" This food is popular in {item['region']}."
        if "type" in item:
            enriched_text += f" It is a type of {item['type']}."
        
        emb = get_embedding(enriched_text)
        collection.add(
            documents=[item["text"]],
            embeddings=[emb], 
            ids=[item["id"]]
        )

# NEW
# Simple approach: upsert all (Upstash handles duplicates efficiently)
for item in food_data:
    enriched_text = item["text"]
    if "region" in item:
        enriched_text += f" This food is popular in {item['region']}."
    if "type" in item:
        enriched_text += f" It is a type of {item['type']}."
    
    # Upsert with metadata
    index.upsert(
        vectors=[
            (
                item["id"],                    # ID
                enriched_text,                 # Text (auto-embedded)
                {                             # Metadata
                    "original_text": item["text"],
                    "region": item.get("region", "Unknown"),
                    "type": item.get("type", "Unknown"),
                    "enriched_text": enriched_text
                }
            )
        ]
    )

# Add small delay for indexing
time.sleep(0.1)
```

### Query Function Changes

```python
# CURRENT
def rag_query(question):
    # Step 1: Embed the user question
    q_emb = get_embedding(question)
    
    # Step 2: Query the vector DB
    results = collection.query(query_embeddings=[q_emb], n_results=3)
    
    # Step 3: Extract documents
    top_docs = results['documents'][0]
    top_ids = results['ids'][0]

# NEW
def rag_query(question):
    # Step 1: Direct query (auto-embedding)
    results = index.query(
        data=question,                    # Auto-embedded by Upstash
        top_k=3,
        include_metadata=True
    )
    
    # Step 2: Extract documents from results
    top_docs = []
    top_ids = []
    
    for result in results:
        top_ids.append(result.id)
        # Use original_text from metadata for context
        top_docs.append(result.metadata['original_text'])
```

### Complete New Implementation

```python
import os
import json
import time
from upstash_vector import Index
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "foods.json"
LLM_MODEL = "llama3.2"

# Initialize Upstash Vector Index
index = Index.from_env()

# Load data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    food_data = json.load(f)

# Upsert all documents to Upstash Vector
print(f"🚀 Upserting {len(food_data)} documents to Upstash Vector...")

for item in food_data:
    # Enhance text with region/type
    enriched_text = item["text"]
    if "region" in item:
        enriched_text += f" This food is popular in {item['region']}."
    if "type" in item:
        enriched_text += f" It is a type of {item['type']}."
    
    # Upsert to Upstash (automatic embedding)
    index.upsert(
        vectors=[
            (
                item["id"],
                enriched_text,  # This gets auto-embedded
                {
                    "original_text": item["text"],
                    "region": item.get("region", "Unknown"),
                    "type": item.get("type", "Unknown"),
                    "enriched_text": enriched_text
                }
            )
        ]
    )
    
    # Small delay to avoid rate limits
    time.sleep(0.05)

print("✅ All documents uploaded to Upstash Vector.")

# RAG query function
def rag_query(question):
    try:
        # Step 1: Query Upstash Vector (automatic embedding + search)
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        # Step 2: Extract documents and show retrieval info
        print("\n🧠 Retrieving relevant information from Upstash Vector...\n")
        
        top_docs = []
        for i, result in enumerate(results):
            print(f"🔹 Source {i + 1} (ID: {result.id}, Score: {result.score:.4f}):")
            print(f"    \"{result.metadata['original_text']}\"\n")
            top_docs.append(result.metadata['original_text'])
        
        print("📚 These seem to be the most relevant pieces of information.\n")
        
        # Step 3: Build context and generate response
        context = "\n".join(top_docs)
        prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""
        
        # Step 4: Generate answer with Ollama
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        })
        
        return response.json()["response"].strip()
        
    except Exception as e:
        return f"❌ Error during RAG query: {str(e)}"

# Interactive loop
print("\n🧠 RAG with Upstash Vector is ready! Ask a question (type 'exit' to quit):\n")
while True:
    question = input("You: ")
    if question.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break
    answer = rag_query(question)
    print("🤖:", answer)
```

---

## Implementation Plan

### Phase 1: Environment Setup (Day 1)

1. **Create Upstash Vector Index**
   ```bash
   # Navigate to Upstash Console
   # Create new Vector Index
   # Choose embedding model: mixedbread-ai/mxbai-embed-large-v1
   # Copy URL and TOKEN
   ```

2. **Environment Configuration**
   ```bash
   # Install dependencies
   pip install upstash-vector python-dotenv
   
   # Create .env file
   echo "UPSTASH_VECTOR_REST_URL=your_url_here" > .env
   echo "UPSTASH_VECTOR_REST_TOKEN=your_token_here" >> .env
   ```

3. **Backup Current System**
   ```bash
   # Backup current ChromaDB
   cp -r chroma_db chroma_db_backup
   cp rag_run.py rag_run_chromadb_backup.py
   ```

### Phase 2: Code Migration (Day 2)

1. **Create New Implementation**
   - Implement `rag_run_upstash.py` with new architecture
   - Test basic connectivity and authentication
   - Verify data upsert functionality

2. **Data Migration Testing**
   ```python
   # Test with small data subset first
   test_data = food_data[:5]
   # Verify upsert and query functionality
   ```

3. **Query Testing**
   ```python
   # Test queries and compare results with ChromaDB
   test_queries = [
       "What are some spicy foods?",
       "Tell me about Indian cuisine",
       "What fruits are mentioned?"
   ]
   ```

### Phase 3: Full Migration and Validation (Day 3)

1. **Full Data Migration**
   - Run complete data upsert to Upstash
   - Validate all documents are indexed
   - Test comprehensive query coverage

2. **Performance Testing**
   - Compare query response times
   - Test with concurrent queries
   - Validate result quality and relevance

3. **Integration Testing**
   - Test entire RAG pipeline end-to-end
   - Verify LLM integration still works
   - Test error scenarios and recovery

### Phase 4: Production Deployment (Day 4)

1. **Replace Main Implementation**
   ```bash
   mv rag_run.py rag_run_chromadb.py
   mv rag_run_upstash.py rag_run.py
   ```

2. **Clean Up Old Dependencies**
   ```bash
   # Optional: Remove ChromaDB if no longer needed
   pip uninstall chromadb
   rm -rf chroma_db/  # After confirming migration success
   ```

3. **Documentation Update**
   - Update README with new setup instructions
   - Document environment variable requirements
   - Add troubleshooting guide

---

## Performance and Cost Analysis

### Performance Comparison

| Metric | ChromaDB + Ollama | Upstash Vector | Expected Change |
|--------|-------------------|----------------|-----------------|
| **Initial Setup Time** | 2-3 minutes | 30 seconds | 🟢 85% faster |
| **Data Ingestion** | ~50ms/doc (embedding + store) | ~20ms/doc (store only) | 🟢 60% faster |
| **Query Latency** | ~100-200ms (embed + search) | ~50-100ms (search only) | 🟢 50% faster |
| **Concurrent Queries** | Limited by local resources | Auto-scaling | 🟢 Much better |
| **Memory Usage** | ~500MB (ChromaDB + embeddings) | ~50MB (client only) | 🟢 90% reduction |

### Cost Analysis

#### Current Costs (ChromaDB + Ollama)
- **Infrastructure**: Local compute resources
- **Storage**: Local disk space (~100MB for current dataset)
- **Compute**: CPU/RAM for embedding generation
- **Maintenance**: Developer time for updates and troubleshooting

#### Upstash Vector Costs
- **Base Plan**: Free tier includes 10K queries/month, 10K vectors
- **Pay-as-you-scale**: $0.40 per 100K queries beyond free tier
- **Storage**: Included in base pricing
- **No Infrastructure**: Zero maintenance overhead

#### Cost-Benefit Analysis
```
Current Dataset: ~100 documents
Expected Monthly Queries: ~1,000
Upstash Cost: $0 (within free tier)

Break-even Analysis:
- Local hosting cost (compute/time): ~$20/month equivalent
- Upstash becomes cost-effective immediately
- Additional benefits: reliability, scalability, zero maintenance
```

### Scalability Considerations

| Aspect | ChromaDB | Upstash Vector | Scaling Impact |
|--------|----------|----------------|----------------|
| **Data Volume** | Limited by local storage | Millions of vectors | 🟢 Highly scalable |
| **Query Volume** | Limited by single machine | Auto-scaling | 🟢 No limits |
| **Geographic Distribution** | Single location | Global CDN | 🟢 Global reach |
| **High Availability** | Single point of failure | Distributed system | 🟢 99.9% uptime |

---

## Error Handling Strategies

### Network and API Errors

```python
import time
from upstash_vector import Index
from upstash_vector.core.http import HttpError

def robust_upstash_query(question, max_retries=3, base_delay=1):
    """
    Robust query with exponential backoff and error handling
    """
    for attempt in range(max_retries):
        try:
            results = index.query(
                data=question,
                top_k=3,
                include_metadata=True
            )
            return results
            
        except HttpError as e:
            if e.status_code == 429:  # Rate limit
                delay = base_delay * (2 ** attempt)
                print(f"⚠️ Rate limit hit. Retrying in {delay}s...")
                time.sleep(delay)
                continue
            elif e.status_code >= 500:  # Server error
                delay = base_delay * (2 ** attempt)
                print(f"⚠️ Server error. Retrying in {delay}s...")
                time.sleep(delay)
                continue
            else:
                raise e  # Re-raise client errors (4xx)
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt)
            print(f"⚠️ Unexpected error: {e}. Retrying in {delay}s...")
            time.sleep(delay)
    
    raise Exception(f"Failed after {max_retries} attempts")

def robust_upstash_upsert(vectors, max_retries=3):
    """
    Robust upsert with batch processing and error recovery
    """
    batch_size = 10  # Process in smaller batches
    
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        
        for attempt in range(max_retries):
            try:
                index.upsert(vectors=batch)
                print(f"✅ Batch {i//batch_size + 1} uploaded successfully")
                break
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Failed to upload batch {i//batch_size + 1}: {e}")
                    # Log failed items for manual retry
                    with open("failed_upserts.json", "a") as f:
                        json.dump({"batch": i//batch_size + 1, "vectors": batch, "error": str(e)}, f)
                        f.write("\n")
                else:
                    delay = 2 ** attempt
                    print(f"⚠️ Batch {i//batch_size + 1} failed. Retrying in {delay}s...")
                    time.sleep(delay)
```

### Authentication and Configuration Errors

```python
def validate_upstash_setup():
    """
    Validate Upstash configuration and connectivity
    """
    try:
        # Check environment variables
        if not os.getenv('UPSTASH_VECTOR_REST_URL'):
            raise ValueError("UPSTASH_VECTOR_REST_URL not set in environment")
        if not os.getenv('UPSTASH_VECTOR_REST_TOKEN'):
            raise ValueError("UPSTASH_VECTOR_REST_TOKEN not set in environment")
        
        # Test connection
        index = Index.from_env()
        
        # Try a simple operation
        test_result = index.query(data="test", top_k=1)
        print("✅ Upstash Vector connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Upstash Vector setup validation failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Verify UPSTASH_VECTOR_REST_URL is correct")
        print("2. Verify UPSTASH_VECTOR_REST_TOKEN is correct")
        print("3. Check network connectivity")
        print("4. Verify index exists in Upstash Console")
        return False

# Usage
if not validate_upstash_setup():
    exit(1)
```

### Graceful Degradation

```python
def rag_query_with_fallback(question):
    """
    RAG query with fallback to direct LLM if vector search fails
    """
    try:
        # Primary: Upstash Vector RAG
        return upstash_rag_query(question)
        
    except Exception as e:
        print(f"⚠️ Vector search failed: {e}")
        print("🔄 Falling back to direct LLM response...")
        
        # Fallback: Direct LLM without context
        prompt = f"""Answer the following question about food based on your knowledge:

Question: {question}
Answer:"""
        
        try:
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False
            })
            return f"[Fallback Mode] {response.json()['response'].strip()}"
            
        except Exception as llm_error:
            return f"❌ Both vector search and LLM failed. Please try again later."
```

---

## Security Considerations

### API Key Security

1. **Environment Variables**
   ```bash
   # Never commit API keys to version control
   echo ".env" >> .gitignore
   
   # Use environment-specific configuration
   # Development: .env file
   # Production: System environment variables or secrets manager
   ```

2. **Key Rotation Strategy**
   ```python
   # Implement key rotation monitoring
   def check_api_key_validity():
       try:
           index = Index.from_env()
           index.query(data="test", top_k=1)
           return True
       except HttpError as e:
           if e.status_code == 401:
               print("🔑 API key expired or invalid. Please update.")
               return False
           return True
   ```

3. **Access Control**
   - Limit API key permissions to minimum required
   - Use separate keys for development/production
   - Monitor API key usage in Upstash Console

### Data Security

1. **Data Encryption**
   - Upstash Vector uses TLS encryption in transit
   - Data encrypted at rest by default
   - No sensitive data stored in metadata (if required)

2. **Data Privacy**
   ```python
   # Remove PII before upserting
   def sanitize_text(text):
       # Remove or mask sensitive information
       # Implement based on your privacy requirements
       return text
   
   # Example usage
   sanitized_text = sanitize_text(item["text"])
   index.upsert(vectors=[(item["id"], sanitized_text, metadata)])
   ```

### Network Security

1. **HTTPS Only**
   - Upstash Vector API uses HTTPS by default
   - Validate SSL certificates in production

2. **Rate Limiting**
   ```python
   # Implement client-side rate limiting
   import time
   from collections import deque
   
   class RateLimiter:
       def __init__(self, max_requests=100, time_window=60):
           self.max_requests = max_requests
           self.time_window = time_window
           self.requests = deque()
       
       def wait_if_needed(self):
           now = time.time()
           # Remove old requests outside time window
           while self.requests and self.requests[0] < now - self.time_window:
               self.requests.popleft()
           
           if len(self.requests) >= self.max_requests:
               sleep_time = self.time_window - (now - self.requests[0])
               if sleep_time > 0:
                   time.sleep(sleep_time)
           
           self.requests.append(now)
   
   rate_limiter = RateLimiter()
   
   def rate_limited_query(question):
       rate_limiter.wait_if_needed()
       return index.query(data=question, top_k=3, include_metadata=True)
   ```

---

## Testing Strategy

### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch
import json

class TestUpstashRAG:
    def setup_method(self):
        """Setup test environment"""
        self.test_data = [
            {"id": "test1", "text": "Apple is a red fruit", "region": "Global", "type": "Fruit"}
        ]
        
    @patch('upstash_vector.Index.from_env')
    def test_upsert_success(self, mock_index):
        """Test successful data upsert"""
        mock_index_instance = Mock()
        mock_index.return_value = mock_index_instance
        
        # Test upsert functionality
        result = upsert_food_data(self.test_data)
        
        assert result == True
        mock_index_instance.upsert.assert_called_once()
        
    @patch('upstash_vector.Index.from_env')
    def test_query_success(self, mock_index):
        """Test successful query"""
        mock_index_instance = Mock()
        mock_index.return_value = mock_index_instance
        
        # Mock query response
        mock_result = Mock()
        mock_result.id = "test1"
        mock_result.score = 0.9
        mock_result.metadata = {"original_text": "Apple is a red fruit"}
        mock_index_instance.query.return_value = [mock_result]
        
        result = rag_query("What is an apple?")
        
        assert "red fruit" in result.lower()
        mock_index_instance.query.assert_called_once()

    def test_error_handling(self):
        """Test error handling scenarios"""
        with patch('upstash_vector.Index.from_env') as mock_index:
            mock_index.side_effect = Exception("Connection failed")
            
            result = rag_query_with_fallback("What is an apple?")
            assert "[Fallback Mode]" in result

# Run tests
# pytest test_upstash_rag.py -v
```

### Integration Tests

```python
def test_end_to_end_rag():
    """Test complete RAG pipeline"""
    # Setup test index
    test_index = Index.from_env()
    
    # Upload test data
    test_data = [
        ("test1", "Pizza is an Italian dish", {"type": "Main Course"}),
        ("test2", "Sushi is Japanese raw fish", {"type": "Main Course"})
    ]
    
    test_index.upsert(vectors=test_data)
    
    # Test query - data should be immediately available
    results = test_index.query(data="What is Italian food?", top_k=1, include_metadata=True)
    
    assert len(results) > 0
    assert "pizza" in results[0].metadata.get("original_text", "").lower()
    
    # Cleanup
    test_index.reset()

def test_performance_benchmark():
    """Benchmark query performance"""
    import time
    
    queries = [
        "What are spicy foods?",
        "Tell me about fruits",
        "What is Indian cuisine?"
    ]
    
    start_time = time.time()
    
    for query in queries:
        result = rag_query(query)
        assert len(result) > 0
    
    end_time = time.time()
    avg_time = (end_time - start_time) / len(queries)
    
    print(f"Average query time: {avg_time:.3f} seconds")
    assert avg_time < 2.0  # Should complete within 2 seconds
```

### Load Testing

```python
import asyncio
import aiohttp
import time

async def load_test_upstash():
    """Test concurrent query performance"""
    
    async def single_query(session, query):
        # Simulate concurrent queries
        start = time.time()
        result = rag_query(f"Tell me about {query}")
        end = time.time()
        return end - start
    
    # Test with multiple concurrent queries
    queries = ["pizza", "sushi", "curry", "pasta", "salad"] * 10
    
    async with aiohttp.ClientSession() as session:
        tasks = [single_query(session, query) for query in queries]
        results = await asyncio.gather(*tasks)
    
    avg_time = sum(results) / len(results)
    max_time = max(results)
    
    print(f"Load test results:")
    print(f"- Queries: {len(queries)}")
    print(f"- Average time: {avg_time:.3f}s")
    print(f"- Max time: {max_time:.3f}s")
    
    assert avg_time < 1.0
    assert max_time < 3.0

# Run load test
# asyncio.run(load_test_upstash())
```

---

## Migration Checklist

### Pre-Migration

- [ ] Create Upstash Vector index with mixedbread-ai/mxbai-embed-large-v1 model
- [ ] Obtain UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN
- [ ] Install required dependencies: `pip install upstash-vector python-dotenv`
- [ ] Set up environment variables in `.env` file
- [ ] Test Upstash connectivity with simple query
- [ ] Backup current ChromaDB data: `cp -r chroma_db chroma_db_backup`
- [ ] Backup current implementation: `cp rag_run.py rag_run_chromadb.py`

### Migration Execution

- [ ] Implement new `rag_run_upstash.py` with Upstash integration
- [ ] Test upsert functionality with subset of data (5-10 records)
- [ ] Verify query functionality with test questions
- [ ] Compare results between ChromaDB and Upstash for same queries
- [ ] Run full data migration (all ~90 food items)
- [ ] Validate all documents are indexed correctly
- [ ] Test comprehensive query scenarios

### Post-Migration Validation

- [ ] Performance testing: measure query response times
- [ ] Load testing: test with concurrent queries
- [ ] Error handling testing: simulate network issues
- [ ] End-to-end RAG pipeline testing with LLM integration
- [ ] User acceptance testing with sample questions
- [ ] Documentation updates (README, setup instructions)
- [ ] Clean up old dependencies (optional): `pip uninstall chromadb`

### Production Deployment

- [ ] Replace main implementation: `mv rag_run_upstash.py rag_run.py`
- [ ] Update deployment scripts/containers with new dependencies
- [ ] Set up production environment variables
- [ ] Configure monitoring and logging
- [ ] Set up backup/recovery procedures for Upstash data
- [ ] Update team documentation and runbooks

### Rollback Plan (if needed)

- [ ] Keep ChromaDB backup accessible for 30 days
- [ ] Maintain `rag_run_chromadb.py` as rollback option
- [ ] Document rollback procedure: restore files and dependencies
- [ ] Test rollback procedure in development environment

---

## Conclusion

This migration from ChromaDB to Upstash Vector Database will significantly simplify the RAG system architecture while improving performance, scalability, and maintainability. The built-in embedding capabilities eliminate the need for manual embedding generation, the cloud-hosted nature removes local storage management complexity, and the REST API provides better integration flexibility.

The implementation plan provides a safe, phased approach with comprehensive testing and rollback capabilities. The expected benefits include:

- **50%+ faster query performance** due to unified embedding + search API
- **90% reduction in memory usage** by eliminating local vector storage
- **Zero maintenance overhead** with fully managed cloud infrastructure  
- **Better scalability** with auto-scaling serverless architecture
- **Simplified deployment** requiring only API credentials

The migration should be completed within 4 days with minimal risk and immediate benefits realized upon successful deployment.