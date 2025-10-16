# 🚀 Upstash Vector Migration - SETUP GUIDE

## Quick Setup Instructions

### Step 1: Create Upstash Vector Index
1. Go to [Upstash Console](https://console.upstash.com/)
2. Click "Create Database" → "Vector"
3. **Important**: Choose embedding model: `mixedbread-ai/mxbai-embed-large-v1`
4. Choose a region (closest to you for best performance)
5. Create the index

### Step 2: Get Your Credentials
1. In your new Vector index dashboard
2. Click "Connect" or "REST API" tab
3. Copy your **REST URL** and **REST TOKEN**

### Step 3: Configure Environment
```bash
# Copy the template
cp .env.template .env

# Edit .env file and replace with your actual credentials:
UPSTASH_VECTOR_REST_URL=https://your-index-url.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_actual_token_here
```

### Step 4: Test Connection
```bash
python3 test_groq_connection.py
```

### Step 5: Run Migration
```bash
python3 rag_run_upstash.py
```

## Files Created:
- `rag_run_upstash.py` - New Upstash Vector implementation
- `test_groq_connection.py` - Connection test script
- `.env.template` - Environment template
- `rag_run_chromadb_backup.py` - Backup of original
- `chroma_db_backup/` - Backup of ChromaDB data

## What's Different:
✅ **No more Ollama embedding calls** - Upstash handles automatically  
✅ **No more ChromaDB management** - Cloud-hosted  
✅ **Faster queries** - Single API call instead of two  
✅ **Better scaling** - Serverless auto-scaling  
✅ **Zero maintenance** - Fully managed  

## Next Steps:
1. Set up your `.env` file with Upstash credentials
2. Run the test script to verify connection
3. Run the new RAG system and test with food questions!

Need help? The error messages will guide you through any missing setup steps.