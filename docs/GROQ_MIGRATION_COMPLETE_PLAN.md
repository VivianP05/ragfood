# Complete Migration Plan: Ollama (Local) → Groq Cloud API

**Date:** October 16, 2025  
**Project:** RAG-Food System  
**Current Branch:** `cloud-migration`

---

## 📋 Table of Contents

1. [Migration Overview](#migration-overview)
2. [Pre-Migration Checklist](#pre-migration-checklist)
3. [Detailed Migration Steps](#detailed-migration-steps)
4. [Code Changes Required](#code-changes-required)
5. [Error Handling & Resilience](#error-handling--resilience)
6. [Rate Limiting Strategy](#rate-limiting-strategy)
7. [Cost Implications & Monitoring](#cost-implications--monitoring)
8. [Fallback Strategies](#fallback-strategies)
9. [Testing Approach](#testing-approach)
10. [Performance Comparison](#performance-comparison)
11. [Rollback Plan](#rollback-plan)

---

## 🎯 Migration Overview

### Current State (Ollama Local)
```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ChromaDB       │◄──────┐
│  (Local)        │       │
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  Ollama API     │───────┘
│  localhost:11434│  Embeddings
│  llama3.2       │  + Generation
└─────────────────┘
```

**Characteristics:**
- ✅ No API costs
- ✅ No rate limits
- ✅ Full data privacy
- ❌ Requires local GPU/CPU
- ❌ Slower inference (5-10s)
- ❌ Model size limitations

### Target State (Groq Cloud)
```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ChromaDB       │◄──────┐
│  (Local)        │       │
└────────┬────────┘       │
         │                │ Ollama Embeddings
         ▼                │ (Keep Local)
┌─────────────────┐       │
│  Groq Cloud API │───────┘
│  llama-3.1-8b   │  Generation Only
│  Instant        │
└─────────────────┘
```

**Characteristics:**
- ✅ Fast inference (0.5-2s)
- ✅ No local resources needed
- ✅ Better model quality
- ❌ API costs (~$0.05-0.10 per 1K tokens)
- ❌ Rate limits (30 RPM free tier)
- ❌ Data sent to cloud

### Hybrid Approach (Recommended)
- **Embeddings:** Keep Ollama local (mxbai-embed-large)
- **Generation:** Migrate to Groq (llama-3.1-8b-instant)
- **Reasoning:** Embeddings are fast locally; generation benefits from cloud speed

---

## ✅ Pre-Migration Checklist

### 1. Environment Setup
- [x] Groq API key added to `.env` file
- [ ] `.env` file included in `.gitignore`
- [ ] Groq Python SDK installed: `pip install groq`
- [ ] `python-dotenv` installed: `pip install python-dotenv`
- [ ] Test API key validity

### 2. Backup Current System
```bash
# Backup current implementation
cp src/rag_run.py src/rag_run_ollama_backup.py

# Backup ChromaDB
cp -r chroma_db chroma_db_backup_$(date +%Y%m%d)

# Create git branch for migration
git checkout -b groq-migration
git add .
git commit -m "Backup before Groq migration"
```

### 3. Dependencies
```bash
# Install required packages
pip install groq python-dotenv requests

# Update requirements.txt
cat >> requirements.txt << EOF
groq>=0.4.0
python-dotenv>=1.0.0
requests>=2.31.0
chromadb>=0.4.0
EOF
```

### 4. API Key Validation
```bash
# Test .env file exists
ls -la .env

# Verify GROQ_API_KEY is set (don't print the actual key!)
grep -q "GROQ_API_KEY" .env && echo "✅ Key found" || echo "❌ Key missing"
```

---

## 🔧 Detailed Migration Steps

### Step 1: Create Migration Branch (5 minutes)
```bash
cd /Users/DELL/ragfood
git checkout -b groq-cloud-migration
git status
```

### Step 2: Install Dependencies (5 minutes)
```bash
# Activate virtual environment if using one
# source venv/bin/activate

# Install Groq SDK
pip install groq python-dotenv

# Verify installation
python -c "from groq import Groq; print('✅ Groq SDK installed')"
```

### Step 3: Validate Environment (5 minutes)
Create a test script to validate setup:

```python
# test_groq_setup.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def test_groq():
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env")
        return False
    
    print("✅ API key found (length: {})".format(len(api_key)))
    
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        print("✅ Groq API connection successful")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

if __name__ == "__main__":
    test_groq()
```

Run test:
```bash
python test_groq_setup.py
```

### Step 4: Modify rag_run.py (30 minutes)

**Key Changes Required:**

#### 4.1 Add Imports
```python
# Add at top of file
from groq import Groq
from dotenv import load_dotenv
import time
from typing import Optional

# Load environment variables
load_dotenv()
```

#### 4.2 Add Constants
```python
# After existing constants
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_MAX_TOKENS = 1024
GROQ_TEMPERATURE = 0.7
GROQ_TIMEOUT = 30
RATE_LIMIT_RPM = 30  # Requests per minute for free tier
```

#### 4.3 Create Rate Limiter Class
```python
class GroqRateLimiter:
    """Simple rate limiter for Groq API calls"""
    def __init__(self, requests_per_minute=30):
        self.requests_per_minute = requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        """Implement token bucket rate limiting"""
        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < 60]
        
        if len(self.requests) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                print(f"⏳ Rate limit: waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
        
        self.requests.append(now)

# Global rate limiter instance
rate_limiter = GroqRateLimiter(requests_per_minute=RATE_LIMIT_RPM)
```

#### 4.4 Initialize Groq Client
```python
def initialize_groq_client() -> Optional[Groq]:
    """Initialize Groq client with error handling"""
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return None

# Initialize client globally
groq_client = initialize_groq_client()
```

#### 4.5 Replace LLM Generation Function
**OLD (Ollama):**
```python
# Step 6: Generate answer with Ollama
response = requests.post("http://localhost:11434/api/generate", json={
    "model": LLM_MODEL,
    "prompt": prompt,
    "stream": False
})

return response.json()["response"].strip()
```

**NEW (Groq):**
```python
def generate_with_groq(prompt: str, client: Groq) -> str:
    """Generate response using Groq API with error handling"""
    if not client:
        return "❌ Groq client not initialized. Check API key."
    
    try:
        # Apply rate limiting
        rate_limiter.wait_if_needed()
        
        # Make API call
        print("🌊 Generating response with Groq Cloud API...")
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful food expert assistant. Provide accurate, detailed answers based on the given context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
            top_p=1,
            stream=False,
            stop=None
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return f"❌ Failed to generate response: {str(e)}"

# In rag_query function, replace Step 6:
answer = generate_with_groq(prompt, groq_client)
return answer
```

#### 4.6 Keep Embeddings Local (Recommended)
```python
# Keep this function unchanged - Ollama embeddings are fast locally
def get_embedding(text):
    """Get embedding from local Ollama (unchanged)"""
    try:
        response = requests.post("http://localhost:11434/api/embeddings", json={
            "model": EMBED_MODEL,
            "prompt": text
        })
        if response.status_code != 200:
            raise Exception(f"Embedding failed: {response.status_code}")
        return response.json()["embedding"]
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        raise
```

### Step 5: Add Error Recovery (15 minutes)

```python
def generate_with_groq_retry(prompt: str, client: Groq, max_retries=3) -> str:
    """Generate with automatic retry on failure"""
    
    for attempt in range(max_retries):
        try:
            rate_limiter.wait_if_needed()
            
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful food expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
                timeout=GROQ_TIMEOUT
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"⏳ Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"❌ All retry attempts exhausted")
                return f"❌ Failed after {max_retries} attempts: {str(e)}"
```

### Step 6: Add Usage Tracking (15 minutes)

```python
class UsageTracker:
    """Track API usage and costs"""
    def __init__(self):
        self.total_requests = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.errors = 0
    
    def record_request(self, response):
        """Record successful request"""
        self.total_requests += 1
        if hasattr(response, 'usage'):
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens
    
    def record_error(self):
        """Record failed request"""
        self.errors += 1
    
    def get_estimated_cost(self):
        """Calculate estimated cost (Groq pricing as of Oct 2024)"""
        # Groq pricing: ~$0.05 per 1M input tokens, ~$0.10 per 1M output tokens
        input_cost = (self.total_input_tokens / 1_000_000) * 0.05
        output_cost = (self.total_output_tokens / 1_000_000) * 0.10
        return input_cost + output_cost
    
    def print_summary(self):
        """Print usage summary"""
        print("\n" + "="*60)
        print("📊 GROQ API USAGE SUMMARY")
        print("="*60)
        print(f"Total Requests: {self.total_requests}")
        print(f"Successful: {self.total_requests - self.errors}")
        print(f"Errors: {self.errors}")
        print(f"Input Tokens: {self.total_input_tokens:,}")
        print(f"Output Tokens: {self.total_output_tokens:,}")
        print(f"Estimated Cost: ${self.get_estimated_cost():.4f}")
        print("="*60)

# Global tracker
usage_tracker = UsageTracker()
```

### Step 7: Update Main Query Function (10 minutes)

```python
def rag_query(question):
    """RAG query with Groq Cloud API"""
    
    # Step 1: Embed question (keep local Ollama)
    print("🧠 Generating question embedding...")
    q_emb = get_embedding(question)

    # Step 2: Query vector DB
    print("🔍 Searching vector database...")
    results = collection.query(query_embeddings=[q_emb], n_results=3)

    # Step 3: Extract documents
    top_docs = results['documents'][0]
    top_ids = results['ids'][0]

    # Step 4: Display retrieved context
    print("\n📚 Found {} relevant food items:\n".format(len(top_docs)))
    for i, doc in enumerate(top_docs):
        print(f"🔹 Source {i + 1} (ID: {top_ids[i]}):")
        print(f"    \"{doc}\"\n")

    # Step 5: Build prompt
    context = "\n".join(top_docs)
    prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""

    # Step 6: Generate with Groq (with retry and tracking)
    try:
        answer = generate_with_groq_retry(prompt, groq_client)
        
        # Track usage if response object available
        # (Note: need to modify generate function to return full response)
        usage_tracker.total_requests += 1
        
        return answer
        
    except Exception as e:
        usage_tracker.record_error()
        return f"❌ Error: {str(e)}"
```

### Step 8: Add Graceful Shutdown (5 minutes)

```python
import atexit

def cleanup():
    """Print usage summary on exit"""
    usage_tracker.print_summary()

# Register cleanup function
atexit.register(cleanup)
```

---

## 🛡️ Error Handling & Resilience

### Error Categories & Solutions

#### 1. API Key Errors
```python
def handle_api_key_error():
    """Handle missing or invalid API key"""
    print("❌ API Key Error")
    print("\n📋 Resolution Steps:")
    print("1. Check .env file exists")
    print("2. Verify GROQ_API_KEY=your_key is set")
    print("3. Get key from: https://console.groq.com/keys")
    print("4. Restart application")
```

#### 2. Rate Limit Errors
```python
def handle_rate_limit(retry_after=60):
    """Handle rate limit exceeded"""
    print(f"⏳ Rate limit exceeded - waiting {retry_after}s")
    print("💡 Consider upgrading to Groq Pro for higher limits")
    time.sleep(retry_after)
```

#### 3. Network Errors
```python
def handle_network_error(error):
    """Handle connection failures"""
    print(f"🌐 Network error: {error}")
    print("💡 Check internet connection")
    print("💡 Verify Groq API status: https://status.groq.com")
    # Optional: fallback to local Ollama
```

#### 4. Timeout Errors
```python
def handle_timeout(timeout_duration=30):
    """Handle request timeout"""
    print(f"⏱️ Request timed out after {timeout_duration}s")
    print("💡 Try reducing max_tokens or simplifying query")
```

### Comprehensive Error Handler
```python
def safe_groq_generate(prompt: str, client: Groq) -> str:
    """Fully error-handled Groq generation"""
    
    try:
        rate_limiter.wait_if_needed()
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a food expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
            timeout=GROQ_TIMEOUT
        )
        
        usage_tracker.record_request(response)
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        error_type = type(e).__name__
        usage_tracker.record_error()
        
        if "API key" in str(e) or "authentication" in str(e).lower():
            handle_api_key_error()
            return "❌ API key error - check configuration"
            
        elif "rate limit" in str(e).lower():
            handle_rate_limit()
            return "❌ Rate limit exceeded - please wait"
            
        elif "timeout" in str(e).lower():
            handle_timeout()
            return "❌ Request timeout - try again"
            
        elif "connection" in str(e).lower():
            handle_network_error(e)
            return "❌ Network error - check connection"
            
        else:
            print(f"❌ Unexpected error ({error_type}): {e}")
            return f"❌ Error: {str(e)}"
```

---

## ⏱️ Rate Limiting Strategy

### Groq Free Tier Limits
- **RPM (Requests Per Minute):** 30
- **RPD (Requests Per Day):** 14,400
- **Tokens Per Minute:** 15,000
- **Concurrent Requests:** 5

### Implementation Strategy

#### 1. Token Bucket Algorithm
```python
class TokenBucketRateLimiter:
    """Advanced rate limiter with token bucket"""
    
    def __init__(self, rate=30, burst=5):
        self.rate = rate  # Requests per minute
        self.burst = burst  # Max burst size
        self.tokens = burst
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def acquire(self):
        """Acquire token, wait if necessary"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            
            # Refill tokens based on elapsed time
            self.tokens = min(
                self.burst,
                self.tokens + elapsed * (self.rate / 60)
            )
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                # Calculate wait time
                wait_time = (1 - self.tokens) / (self.rate / 60)
                time.sleep(wait_time)
                self.tokens = 0
                return True
```

#### 2. Request Queue
```python
from queue import Queue
import threading

class RequestQueue:
    """Queue-based request handler"""
    
    def __init__(self, max_concurrent=3):
        self.queue = Queue()
        self.max_concurrent = max_concurrent
        self.active_requests = 0
        self.lock = threading.Lock()
    
    def process_request(self, func, *args, **kwargs):
        """Process request with concurrency control"""
        with self.lock:
            while self.active_requests >= self.max_concurrent:
                time.sleep(0.1)
            self.active_requests += 1
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            with self.lock:
                self.active_requests -= 1
```

#### 3. Adaptive Rate Limiting
```python
class AdaptiveRateLimiter:
    """Adjust rate based on errors"""
    
    def __init__(self, initial_rpm=30):
        self.rpm = initial_rpm
        self.errors = 0
        self.success = 0
    
    def on_success(self):
        """Increase rate on success"""
        self.success += 1
        if self.success > 10 and self.errors == 0:
            self.rpm = min(self.rpm * 1.1, 30)  # Max 30 RPM
            self.success = 0
    
    def on_error(self):
        """Decrease rate on error"""
        self.errors += 1
        if self.errors > 2:
            self.rpm = max(self.rpm * 0.5, 5)  # Min 5 RPM
            self.errors = 0
```

---

## 💰 Cost Implications & Monitoring

### Groq Pricing (As of Oct 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| llama-3.1-8b-instant | $0.05 | $0.10 |
| llama-3.1-70b-versatile | $0.59 | $0.79 |

### Cost Estimation

#### Typical RAG Query Breakdown
- **Average Prompt:** 300 tokens (context + question)
- **Average Response:** 150 tokens
- **Cost per query:** ~$0.000030 ($0.03 per 1,000 queries)

#### Monthly Cost Estimates

| Usage Level | Queries/Day | Queries/Month | Est. Cost/Month |
|-------------|-------------|---------------|-----------------|
| Light | 10 | 300 | $0.01 |
| Moderate | 100 | 3,000 | $0.09 |
| Heavy | 1,000 | 30,000 | $0.90 |
| Production | 10,000 | 300,000 | $9.00 |

### Cost Monitoring Implementation

```python
import json
from datetime import datetime

class CostMonitor:
    """Monitor and track API costs"""
    
    def __init__(self, log_file="groq_usage.json"):
        self.log_file = log_file
        self.daily_usage = {}
        self.load_history()
    
    def load_history(self):
        """Load usage history from file"""
        try:
            with open(self.log_file, 'r') as f:
                self.daily_usage = json.load(f)
        except FileNotFoundError:
            self.daily_usage = {}
    
    def save_history(self):
        """Save usage history to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.daily_usage, f, indent=2)
    
    def record_usage(self, input_tokens, output_tokens):
        """Record token usage"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.daily_usage:
            self.daily_usage[today] = {
                "requests": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "cost": 0.0
            }
        
        self.daily_usage[today]["requests"] += 1
        self.daily_usage[today]["input_tokens"] += input_tokens
        self.daily_usage[today]["output_tokens"] += output_tokens
        
        # Calculate cost
        input_cost = (input_tokens / 1_000_000) * 0.05
        output_cost = (output_tokens / 1_000_000) * 0.10
        self.daily_usage[today]["cost"] += input_cost + output_cost
        
        self.save_history()
    
    def get_monthly_cost(self):
        """Calculate current month cost"""
        current_month = datetime.now().strftime("%Y-%m")
        total_cost = sum(
            day_data["cost"] 
            for day, day_data in self.daily_usage.items() 
            if day.startswith(current_month)
        )
        return total_cost
    
    def check_budget_alert(self, budget_limit=10.0):
        """Alert if approaching budget"""
        current_cost = self.get_monthly_cost()
        if current_cost > budget_limit * 0.8:
            print(f"⚠️ Budget Alert: ${current_cost:.2f} / ${budget_limit:.2f}")
            return True
        return False
```

### Budget Protection

```python
class BudgetProtection:
    """Prevent exceeding budget limits"""
    
    def __init__(self, daily_limit=1.0, monthly_limit=10.0):
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        self.cost_monitor = CostMonitor()
    
    def can_make_request(self):
        """Check if request is within budget"""
        monthly_cost = self.cost_monitor.get_monthly_cost()
        
        if monthly_cost >= self.monthly_limit:
            print(f"🚫 Monthly budget limit reached: ${monthly_cost:.2f}")
            return False
        
        # Check daily limit (similar logic)
        # ...
        
        return True
```

---

## 🔄 Fallback Strategies

### Strategy 1: Automatic Fallback to Ollama

```python
class HybridLLMProvider:
    """Automatically fallback to Ollama if Groq fails"""
    
    def __init__(self):
        self.groq_client = initialize_groq_client()
        self.groq_failures = 0
        self.max_failures_before_fallback = 3
    
    def generate(self, prompt):
        """Try Groq first, fallback to Ollama"""
        
        # Try Groq if available and not failing too much
        if self.groq_client and self.groq_failures < self.max_failures_before_fallback:
            try:
                result = self.generate_with_groq(prompt)
                self.groq_failures = 0  # Reset on success
                return result
            except Exception as e:
                print(f"⚠️ Groq failed: {e}")
                self.groq_failures += 1
                print(f"🔄 Falling back to local Ollama...")
        
        # Fallback to Ollama
        return self.generate_with_ollama(prompt)
    
    def generate_with_groq(self, prompt):
        """Groq generation"""
        response = self.groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    
    def generate_with_ollama(self, prompt):
        """Ollama fallback generation"""
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"].strip()
```

### Strategy 2: Cached Responses

```python
import hashlib
import pickle

class ResponseCache:
    """Cache responses to reduce API calls"""
    
    def __init__(self, cache_file="response_cache.pkl"):
        self.cache_file = cache_file
        self.cache = self.load_cache()
    
    def load_cache(self):
        """Load cache from disk"""
        try:
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def save_cache(self):
        """Save cache to disk"""
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def get_cache_key(self, prompt):
        """Generate cache key from prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def get(self, prompt):
        """Get cached response"""
        key = self.get_cache_key(prompt)
        return self.cache.get(key)
    
    def set(self, prompt, response):
        """Cache response"""
        key = self.get_cache_key(prompt)
        self.cache[key] = response
        self.save_cache()
```

### Strategy 3: Degraded Mode

```python
class DegradedModeHandler:
    """Provide limited service when API unavailable"""
    
    def __init__(self):
        self.mode = "normal"  # or "degraded"
    
    def handle_query(self, question, context):
        """Handle query based on mode"""
        
        if self.mode == "degraded":
            # Return context only, no generation
            return f"ℹ️ Service in degraded mode. Here's relevant context:\n\n{context}"
        
        # Normal mode - try full RAG
        try:
            return self.full_rag_query(question, context)
        except Exception:
            self.mode = "degraded"
            return self.handle_query(question, context)
```

---

## 🧪 Testing Approach

### Test Suite Structure

```
tests/
├── test_groq_migration.py         # Main migration tests
├── test_groq_integration.py       # API integration tests
├── test_rate_limiting.py          # Rate limit tests
├── test_error_handling.py         # Error scenarios
├── test_cost_tracking.py          # Cost monitoring tests
└── test_performance_comparison.py # Ollama vs Groq comparison
```

### Test 1: Basic Connectivity
```python
# tests/test_groq_integration.py
import pytest
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def test_groq_api_key_exists():
    """Test API key is configured"""
    api_key = os.getenv('GROQ_API_KEY')
    assert api_key is not None, "GROQ_API_KEY not found in environment"
    assert len(api_key) > 20, "API key seems invalid"

def test_groq_client_initialization():
    """Test Groq client can be created"""
    client = Groq()
    assert client is not None

def test_groq_simple_completion():
    """Test basic API call"""
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say 'test passed'"}],
        max_tokens=10
    )
    assert response.choices[0].message.content is not None
    print(f"✅ Response: {response.choices[0].message.content}")
```

### Test 2: RAG Functionality
```python
# tests/test_groq_migration.py
def test_rag_query_with_groq():
    """Test complete RAG query with Groq"""
    from src.rag_run import query_rag
    
    question = "Tell me about spicy food"
    answer = query_rag(question)
    
    assert answer is not None
    assert len(answer) > 10
    assert not answer.startswith("❌")
    print(f"✅ RAG answer: {answer[:100]}...")

def test_multiple_queries():
    """Test multiple queries for rate limiting"""
    from src.rag_run import query_rag
    
    questions = [
        "What are healthy foods?",
        "Tell me about Asian cuisine",
        "What foods are high in protein?"
    ]
    
    for q in questions:
        answer = query_rag(q)
        assert answer is not None
        print(f"✅ Query successful: {q}")
```

### Test 3: Error Handling
```python
# tests/test_error_handling.py
def test_invalid_api_key():
    """Test behavior with invalid API key"""
    os.environ['GROQ_API_KEY'] = "invalid_key"
    
    from src.rag_run import initialize_groq_client
    client = initialize_groq_client()
    
    # Should handle gracefully
    assert client is not None  # or check error handling

def test_network_timeout():
    """Test timeout handling"""
    # Mock network delay
    # Verify timeout is handled properly
    pass

def test_rate_limit_handling():
    """Test rate limit is enforced"""
    # Make 35 requests rapidly
    # Verify rate limiting kicks in
    pass
```

### Test 4: Performance Comparison
```python
# tests/test_performance_comparison.py
import time

def test_response_time_comparison():
    """Compare Ollama vs Groq response times"""
    
    question = "What are healthy Mediterranean foods?"
    
    # Test Ollama
    start = time.time()
    # ollama_answer = query_with_ollama(question)
    ollama_time = time.time() - start
    
    # Test Groq
    start = time.time()
    # groq_answer = query_with_groq(question)
    groq_time = time.time() - start
    
    print(f"Ollama time: {ollama_time:.2f}s")
    print(f"Groq time: {groq_time:.2f}s")
    print(f"Speedup: {ollama_time/groq_time:.2f}x")
    
    # Groq should be faster
    assert groq_time < ollama_time
```

### Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_groq_integration.py -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

---

## 📊 Performance Comparison

### Expected Metrics

| Metric | Ollama (Local) | Groq (Cloud) | Improvement |
|--------|----------------|--------------|-------------|
| **Average Response Time** | 5-10s | 0.5-2s | **3-10x faster** |
| **Cold Start** | 2-5s (first query) | 0.3-0.5s | **5-10x faster** |
| **Throughput** | 6-12 queries/min | 30 queries/min | **2.5-5x higher** |
| **Memory Usage** | 4-8GB (model loaded) | <100MB | **40-80x less** |
| **CPU Usage** | 60-100% (during gen) | <5% | **12-20x less** |
| **Response Quality** | Good | Better | Slight improvement |

### Benchmark Script

```python
# benchmark_migration.py
import time
import statistics
from typing import List, Dict

def benchmark_implementation(query_func, queries: List[str], name: str) -> Dict:
    """Benchmark an implementation"""
    
    print(f"\n🔬 Benchmarking {name}...")
    results = {
        "name": name,
        "queries": len(queries),
        "response_times": [],
        "errors": 0
    }
    
    for i, query in enumerate(queries, 1):
        try:
            start = time.time()
            answer = query_func(query)
            elapsed = time.time() - start
            
            results["response_times"].append(elapsed)
            print(f"  Query {i}/{len(queries)}: {elapsed:.2f}s ✅")
            
        except Exception as e:
            results["errors"] += 1
            print(f"  Query {i}/{len(queries)}: ERROR ❌")
    
    # Calculate statistics
    if results["response_times"]:
        results["avg_time"] = statistics.mean(results["response_times"])
        results["median_time"] = statistics.median(results["response_times"])
        results["min_time"] = min(results["response_times"])
        results["max_time"] = max(results["response_times"])
        results["std_dev"] = statistics.stdev(results["response_times"]) if len(results["response_times"]) > 1 else 0
    
    return results

def print_comparison(ollama_results, groq_results):
    """Print comparison table"""
    
    print("\n" + "="*70)
    print("📊 PERFORMANCE COMPARISON: Ollama vs Groq")
    print("="*70)
    
    print(f"\n{'Metric':<30} {'Ollama':<15} {'Groq':<15} {'Improvement':<15}")
    print("-"*70)
    
    metrics = [
        ("Average Response Time", "avg_time", "s", True),
        ("Median Response Time", "median_time", "s", True),
        ("Min Response Time", "min_time", "s", True),
        ("Max Response Time", "max_time", "s", True),
        ("Std Deviation", "std_dev", "s", True),
        ("Error Count", "errors", "", False)
    ]
    
    for label, key, unit, lower_is_better in metrics:
        ollama_val = ollama_results.get(key, 0)
        groq_val = groq_results.get(key, 0)
        
        if lower_is_better and groq_val > 0:
            improvement = f"{ollama_val/groq_val:.2f}x faster"
        else:
            improvement = "-"
        
        print(f"{label:<30} {ollama_val:.2f}{unit:<14} {groq_val:.2f}{unit:<14} {improvement:<15}")

# Test queries
test_queries = [
    "What are healthy breakfast options?",
    "Tell me about spicy Asian food",
    "What foods are high in protein?",
    "Mediterranean diet recommendations",
    "Quick dinner ideas"
]

# Run benchmarks
# ollama_results = benchmark_implementation(query_with_ollama, test_queries, "Ollama")
# groq_results = benchmark_implementation(query_with_groq, test_queries, "Groq")

# print_comparison(ollama_results, groq_results)
```

---

## 🔙 Rollback Plan

### If Migration Fails

#### Step 1: Immediate Rollback (5 minutes)
```bash
# Switch back to working version
git checkout main  # or previous working branch

# Restore backup
cp src/rag_run_ollama_backup.py src/rag_run.py

# Verify Ollama is running
ollama serve &
ollama list

# Test
python src/rag_run.py
```

#### Step 2: Preserve Migration Work
```bash
# Save migration attempt
git checkout groq-migration
git add .
git commit -m "WIP: Groq migration - rollback for issues"
git push origin groq-migration

# Return to stable
git checkout main
```

#### Step 3: Document Issues
Create issue log:
```markdown
## Migration Rollback - [DATE]

### Reason for Rollback:
- [ ] API key issues
- [ ] Rate limiting problems
- [ ] Performance worse than expected
- [ ] Errors in production
- [ ] Cost concerns
- [ ] Other: ___________

### Issues Encountered:
1. ...
2. ...

### Next Steps:
- [ ] Review error logs
- [ ] Contact Groq support
- [ ] Adjust implementation
- [ ] Re-attempt migration
```

---

## 📝 Migration Checklist

### Pre-Migration
- [ ] ✅ Groq API key added to `.env`
- [ ] Backup current `rag_run.py`
- [ ] Install dependencies (`groq`, `python-dotenv`)
- [ ] Test Groq API connectivity
- [ ] Create migration git branch

### During Migration
- [ ] Add imports and constants
- [ ] Implement rate limiter
- [ ] Initialize Groq client
- [ ] Replace LLM generation function
- [ ] Add error handling
- [ ] Add usage tracking
- [ ] Test basic query
- [ ] Test multiple queries
- [ ] Test error scenarios

### Post-Migration
- [ ] Run full test suite
- [ ] Compare performance benchmarks
- [ ] Monitor costs for 24 hours
- [ ] Verify rate limiting works
- [ ] Check error handling
- [ ] Update documentation
- [ ] Merge to main branch
- [ ] Deploy to production

### Monitoring (First Week)
- [ ] Daily cost checks
- [ ] Error rate monitoring
- [ ] Performance metrics
- [ ] User feedback
- [ ] Rate limit incidents

---

## 🎯 Success Criteria

### Migration is Successful If:
1. ✅ **Functional:** All queries work correctly
2. ✅ **Fast:** Response time < 3s average
3. ✅ **Reliable:** Error rate < 5%
4. ✅ **Affordable:** Cost < $10/month for expected usage
5. ✅ **Stable:** No rate limit issues with normal usage
6. ✅ **Quality:** Answer quality equal or better than Ollama

### Migration Should Be Rolled Back If:
1. ❌ Error rate > 20%
2. ❌ Response time > 5s average
3. ❌ Cost > $50/month
4. ❌ Frequent rate limit issues
5. ❌ Answer quality significantly worse

---

## 📚 Additional Resources

### Documentation
- [Groq API Docs](https://console.groq.com/docs)
- [Groq Python SDK](https://github.com/groq/groq-python)
- [Rate Limiting Best Practices](https://console.groq.com/docs/rate-limits)

### Support
- Groq Discord: [discord.gg/groq](https://discord.gg/groq)
- Groq Status: [status.groq.com](https://status.groq.com)
- API Issues: support@groq.com

### Cost Calculator
- [Groq Pricing](https://console.groq.com/settings/billing)
- Token counter: [OpenAI Tokenizer](https://platform.openai.com/tokenizer)

---

## 🚀 Next Steps After Migration

1. **Optimize Prompts:** Fine-tune system prompts for better responses
2. **Implement Streaming:** Add streaming for real-time responses
3. **Add Analytics:** Track query patterns and popular topics
4. **Expand Models:** Test other Groq models (llama-3.1-70b)
5. **Production Hardening:** Add monitoring, alerting, logging
6. **User Feedback:** Collect feedback on response quality

---

**Migration Author:** AI Assistant  
**Last Updated:** October 16, 2025  
**Version:** 1.0  
**Status:** Ready for Implementation

