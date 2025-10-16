# Groq Migration Quick Reference

## 🚀 Quick Start (5 minutes)

### Step 1: Validate Setup
```bash
python3 scripts/migrate_to_groq.py --validate
```

### Step 2: Run Migration
```bash
python3 scripts/migrate_to_groq.py --migrate
```

### Step 3: Test
```bash
python3 scripts/migrate_to_groq.py --test
```

---

## 📋 Manual Migration (Key Changes)

### 1. Add Imports (Top of rag_run.py)
```python
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()
```

### 2. Initialize Groq Client
```python
def initialize_groq_client():
    try:
        client = Groq()
        print("✅ Groq client initialized")
        return client
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

groq_client = initialize_groq_client()
```

### 3. Replace Generation (Line ~86)

**OLD:**
```python
response = requests.post("http://localhost:11434/api/generate", json={
    "model": LLM_MODEL,
    "prompt": prompt,
    "stream": False
})
return response.json()["response"].strip()
```

**NEW:**
```python
response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a food expert."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=1024
)
return response.choices[0].message.content.strip()
```

### 4. Keep Embeddings Local (Unchanged)
```python
# This stays the same - Ollama embeddings are fast locally
def get_embedding(text):
    response = requests.post("http://localhost:11434/api/embeddings", json={
        "model": EMBED_MODEL,
        "prompt": text
    })
    return response.json()["embedding"]
```

---

## 🔥 Rate Limiting (Essential!)

```python
class GroqRateLimiter:
    def __init__(self, requests_per_minute=30):
        self.rpm = requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        now = time.time()
        self.requests = [t for t in self.requests if now - t < 60]
        
        if len(self.requests) >= self.rpm:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.requests.append(now)

rate_limiter = GroqRateLimiter()

# Use before API calls
rate_limiter.wait_if_needed()
response = groq_client.chat.completions.create(...)
```

---

## 💰 Cost Tracking

```python
class UsageTracker:
    def __init__(self):
        self.requests = 0
        self.input_tokens = 0
        self.output_tokens = 0
    
    def record(self, response):
        self.requests += 1
        self.input_tokens += response.usage.prompt_tokens
        self.output_tokens += response.usage.completion_tokens
    
    def get_cost(self):
        # $0.05 per 1M input, $0.10 per 1M output
        return (self.input_tokens / 1_000_000) * 0.05 + \
               (self.output_tokens / 1_000_000) * 0.10

tracker = UsageTracker()
```

---

## 🛡️ Error Handling

```python
def safe_generate(prompt, client, max_retries=3):
    for attempt in range(max_retries):
        try:
            rate_limiter.wait_if_needed()
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                timeout=30
            )
            
            tracker.record(response)
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"⏳ Retry in {wait}s...")
                time.sleep(wait)
            else:
                return f"❌ Error: {str(e)}"
```

---

## 🧪 Quick Test

```python
# test_groq.py
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hello"}],
    max_tokens=10
)

print("✅ Groq works!")
print(f"Response: {response.choices[0].message.content}")
```

Run:
```bash
python3 test_groq.py
```

---

## 📊 Performance Comparison

| Metric | Ollama | Groq | Winner |
|--------|--------|------|--------|
| Speed | 5-10s | 0.5-2s | 🏆 Groq |
| Cost | Free | ~$0.03/1K queries | Ollama |
| Quality | Good | Better | Groq |
| Local | Yes | No | Ollama |
| Limits | None | 30 RPM | Ollama |

---

## 🔄 Rollback

```bash
# If anything goes wrong
python3 scripts/migrate_to_groq.py --rollback

# Or manually
cp src/rag_run_ollama_backup.py src/rag_run.py
```

---

## 💡 Pro Tips

1. **Keep embeddings local** - They're fast with Ollama
2. **Use streaming** - Add `stream=True` for real-time responses
3. **Monitor costs** - Check https://console.groq.com daily
4. **Cache responses** - For repeated queries
5. **Fallback to Ollama** - If Groq fails, use local model

---

## 🆘 Troubleshooting

### "API key not found"
```bash
# Check .env file
cat .env | grep GROQ_API_KEY

# Should see: GROQ_API_KEY=gsk_...
```

### "Rate limit exceeded"
```python
# Increase wait time
rate_limiter = GroqRateLimiter(requests_per_minute=20)  # Lower RPM
```

### "Timeout"
```python
# Increase timeout
response = client.chat.completions.create(
    timeout=60  # Increase from 30
)
```

### "Connection error"
- Check internet connection
- Verify https://status.groq.com
- Try again in a few minutes

---

## 📚 Resources

- **Full Plan:** `docs/GROQ_MIGRATION_COMPLETE_PLAN.md`
- **Groq Docs:** https://console.groq.com/docs
- **Groq Console:** https://console.groq.com
- **API Keys:** https://console.groq.com/keys
- **Pricing:** https://console.groq.com/settings/billing

---

**Last Updated:** October 16, 2025  
**Quick Start Time:** ~5 minutes  
**Full Migration Time:** ~30 minutes
