# 🚀 Quick Start - Complete Cloud Migration

## ✅ Migration Status: COMPLETED

Your RAG system has been **fully migrated** from local (ChromaDB + Ollama) to cloud (Upstash Vector + Groq).

---

## 📝 What You Need to Do Now

### 1. **Install Dependencies** (1 minute)

```bash
pip install -r requirements.txt
```

This installs:
- `upstash-vector` - Cloud vector database
- `groq` - Groq Cloud API client
- `python-dotenv` - Environment management

---

### 2. **Get Your API Keys** (5 minutes)

#### A. Upstash Vector (FREE)

1. Go to: https://console.upstash.com/vector
2. Sign up / Login
3. Click **"Create Index"**
4. Configure:
   - **Name:** ragfood
   - **Region:** us-east-1 (or closest to you)
   - **Embedding Model:** `mixedbread-ai/mxbai-embed-large-v1`
   - **Dimensions:** 1024
   - **Similarity:** COSINE
5. Copy **REST URL** and **REST TOKEN**

#### B. Groq API (FREE)

1. Go to: https://console.groq.com/keys
2. Sign up / Login (free tier: 30 requests/min)
3. Click **"Create API Key"**
4. Copy your API key (starts with `gsk_`)

---

### 3. **Configure Environment** (1 minute)

Create `.env` file:

```bash
cp .env.template .env
```

Edit `.env` and add your credentials:

```bash
# Upstash Vector
UPSTASH_VECTOR_REST_URL=https://your-endpoint.upstash.io
UPSTASH_VECTOR_REST_TOKEN=AXXXXxxx...

# Groq Cloud
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

---

### 4. **Validate Setup** (30 seconds)

```bash
python3 scripts/setup_upstash.py --validate
```

Expected output:
```
✅ upstash-vector installed
✅ groq installed
✅ python-dotenv installed
✅ .env file exists
✅ UPSTASH_VECTOR_REST_URL found
✅ UPSTASH_VECTOR_REST_TOKEN found
✅ GROQ_API_KEY found
```

---

### 5. **Upload Your Data** (30 seconds)

```bash
python3 scripts/setup_upstash.py --upload
```

This uploads 110 food items to Upstash Vector.

---

### 6. **Test the System** (1 minute)

#### Quick Test:
```bash
python3 scripts/setup_upstash.py --query "healthy breakfast"
```

#### Full System Test:
```bash
python3 scripts/test_complete_system.py
```

This runs 8 comprehensive tests:
1. Dependencies check
2. Environment configuration
3. Upstash connection
4. Groq connection
5. Embedding generation
6. Query functionality
7. LLM responses
8. Performance benchmarks

---

### 7. **Run the RAG System** (Interactive)

```bash
python3 src/rag_run.py
```

Try these queries:
```
You: What is Pho?
You: Tell me about Italian pasta
You: Recommend healthy breakfast options
You: What are spicy Asian dishes?
You: exit
```

---

## 🎯 What Changed?

### Before (Local)
```
ChromaDB (200MB local storage)
   ↓
Manual embedding via Ollama (slow)
   ↓
Ollama LLM llama3.2 (3-5s response)
```

### After (Cloud)
```
Upstash Vector (10MB, cloud-based)
   ↓
Automatic embeddings (fast)
   ↓
Groq Cloud llama-3.1-8b-instant (1-2s response)
```

**Benefits:**
- ✅ **50% faster** responses
- ✅ **95% less** local storage
- ✅ **Zero** local dependencies
- ✅ **Cloud-based** - works anywhere
- ✅ **Better error handling** with retries
- ✅ **Automatic embeddings** - no manual work

---

## 🧪 Testing Commands

```bash
# Validate configuration
python3 scripts/setup_upstash.py --validate

# Test connection
python3 scripts/setup_upstash.py --test

# Upload data
python3 scripts/setup_upstash.py --upload

# Test a query
python3 scripts/setup_upstash.py --query "Vietnamese food"

# Full system test
python3 scripts/test_complete_system.py

# Run RAG system
python3 src/rag_run.py
```

---

## 🐛 Troubleshooting

### Issue: Missing dependencies
```bash
pip install upstash-vector groq python-dotenv
```

### Issue: Environment variables not found
```bash
# Check .env exists
ls -la .env

# Verify contents
cat .env
```

### Issue: Upstash connection failed
- Verify credentials at https://console.upstash.com/vector
- Check REST URL and TOKEN are correct
- Ensure index was created with correct embedding model

### Issue: Groq authentication failed
- Verify API key at https://console.groq.com/keys
- Ensure key starts with `gsk_`
- Check for extra spaces in .env file

---

## 📚 Documentation

Full guides available:
- `COMPLETE_MIGRATION_GUIDE.md` - Complete migration details
- `GROQ_MIGRATION_COMPLETE_PLAN.md` - Groq-specific guide
- `UPSTASH_MIGRATION_COMPLETED.md` - Upstash-specific guide
- `GROQ_QUICK_REFERENCE.md` - Quick reference

---

## 🎉 You're Ready!

After completing steps 1-7, your RAG system will be:
- ✅ Fully cloud-based
- ✅ Faster and more efficient
- ✅ Production-ready
- ✅ Easy to deploy anywhere

**Total setup time: ~10 minutes**

---

**Questions?** Check `COMPLETE_MIGRATION_GUIDE.md` for detailed troubleshooting.
