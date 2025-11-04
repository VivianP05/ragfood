import os
import json
import time
from upstash_vector import Index
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "../data/foods.json" if os.path.exists("../data/foods.json") else "data/foods.json"
LLM_MODEL = "llama-3.1-8b-instant"  # Groq model
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

def validate_upstash_setup():
    """Validate Upstash configuration"""
    try:
        if not os.getenv('UPSTASH_VECTOR_REST_URL'):
            raise ValueError("UPSTASH_VECTOR_REST_URL not set in environment")
        if not os.getenv('UPSTASH_VECTOR_REST_TOKEN'):
            raise ValueError("UPSTASH_VECTOR_REST_TOKEN not set in environment")
        print("✅ Upstash environment variables found")
        return True
    except Exception as e:
        print(f"❌ Upstash setup validation failed: {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Create Vector Index: https://console.upstash.com/")
        print("2. Choose model: mixedbread-ai/mxbai-embed-large-v1")
        print("3. Add to .env: UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN")
        return False

def validate_groq_setup():
    """Validate Groq API configuration"""
    try:
        if not os.getenv('GROQ_API_KEY'):
            raise ValueError("GROQ_API_KEY not set in environment")
        print("✅ Groq API key found")
        return True
    except Exception as e:
        print(f"❌ Groq setup validation failed: {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Get API key: https://console.groq.com/")
        print("2. Add to .env: GROQ_API_KEY=your-api-key-here")
        return False

def initialize_groq_client():
    """Initialize Groq client"""
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        print("✅ Groq client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return None

def initialize_upstash_index():
    """Initialize Upstash Vector index"""
    try:
        index = Index.from_env()
        print("✅ Upstash Vector client initialized successfully")
        return index
    except Exception as e:
        print(f"❌ Failed to initialize Upstash Vector: {e}")
        return None

# Load data
with open(JSON_FILE, "r", encoding="utf-8") as f:
    food_data = json.load(f)

print(f"✅ Loaded {len(food_data)} food items from {JSON_FILE}")

# Setup Upstash Vector
if not validate_upstash_setup():
    print("⚠️  Please configure Upstash Vector to continue")
    index = None
else:
    index = initialize_upstash_index()

# Setup Groq client
if not validate_groq_setup():
    print("⚠️  Please configure Groq API to continue")
    groq_client = None
else:
    groq_client = initialize_groq_client()
    
    # Prepare and upload all data (Upstash handles embeddings automatically)
    if index:
        print(f"🚀 Uploading {len(food_data)} documents to Upstash Vector...")
        vectors_to_upsert = []
        
        for item in food_data:
            # Enhance text with region/type context
            enriched_text = item["text"]
            if "region" in item:
                enriched_text += f" This food is popular in {item['region']}."
            if "type" in item:
                enriched_text += f" It is a type of {item['type']}."
            
            # Upstash auto-embeds the text - no manual embedding needed!
            vectors_to_upsert.append((
                item["id"],
                enriched_text,
                {
                    "original_text": item["text"],
                    "region": item.get("region", "Unknown"),
                    "type": item.get("type", "Unknown")
                }
            ))
        
        try:
            index.upsert(vectors=vectors_to_upsert)
            print("✅ All documents uploaded to Upstash Vector successfully!")
        except Exception as e:
            print(f"❌ Failed to upload data: {e}")

# RAG query
def rag_query(question):
    """Perform RAG query using Upstash Vector"""
    if not index:
        return "❌ Upstash Vector not initialized. Please check configuration."
    
    try:
        print(f"\n🔍 Processing query: '{question}'")
        
        # Step 1: Query Upstash Vector (automatic embedding + search)
        print("🧠 Searching Upstash Vector database...")
        results = index.query(
            data=question,  # Upstash auto-embeds the query
            top_k=3,
            include_metadata=True
        )
        
        if not results:
            return "❌ No relevant food information found."
        
        # Step 2: Extract and display retrieved documents
        print(f"\n📚 Found {len(results)} relevant food items:\n")
        
        top_docs = []
        for i, result in enumerate(results):
            print(f"🔹 Source {i + 1} (ID: {result.id}, Relevance: {result.score:.3f}):")
            print(f"    \"{result.metadata['original_text']}\"\n")
            top_docs.append(result.metadata['original_text'])
        
        print("📚 These are the most relevant pieces of information to answer your question.\n")
        
        # Step 3: Build prompt from context
        context = "\n".join(top_docs)
        
        system_message = "You are a helpful food expert assistant. Use the provided context to answer questions accurately and concisely."
        user_message = f"""Context:
{context}

Question: {question}

Please provide a helpful answer based on the context above."""
        
        # Step 4: Generate answer with Groq (with retry logic)
        if not groq_client:
            return "❌ Groq client not initialized. Please check your API key configuration."
        
        for attempt in range(MAX_RETRIES):
            try:
                print(f"🤖 Generating response with Groq ({LLM_MODEL})...")
                
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    model=LLM_MODEL,
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stream=False
                )
                
                answer = chat_completion.choices[0].message.content.strip()
                return answer
                
            except Exception as e:
                error_msg = str(e)
                
                # Check for rate limiting
                if "rate_limit" in error_msg.lower():
                    if attempt < MAX_RETRIES - 1:
                        wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                        print(f"⚠️  Rate limit hit. Retrying in {wait_time}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                        time.sleep(wait_time)
                        continue
                    else:
                        return f"❌ Rate limit exceeded. Please try again later."
                
                # Check for authentication errors
                elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                    return f"❌ Authentication failed. Please check your GROQ_API_KEY in .env file."
                
                # Other errors
                else:
                    if attempt < MAX_RETRIES - 1:
                        print(f"⚠️  Error occurred. Retrying... (attempt {attempt + 1}/{MAX_RETRIES})")
                        time.sleep(RETRY_DELAY)
                        continue
                    else:
                        return f"❌ Error generating response: {error_msg}"
        
        return "❌ Failed to generate response after multiple attempts."
            
    except Exception as e:
        return f"❌ Error during RAG query: {str(e)}"

# Standardized wrapper function
def query_rag(question):
    return rag_query(question)

# Interactive loop
if index and groq_client:
    print("\n🧠 RAG is ready with Upstash Vector + Groq Cloud. Ask a question (type 'exit' to quit):\n")
    print(f"   Vector DB: Upstash Vector (mixedbread-ai/mxbai-embed-large-v1)")
    print(f"   LLM: Groq Cloud ({LLM_MODEL})\n")
    
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        answer = rag_query(question)
        print("🤖:", answer)
else:
    print("\n⚠️  Cannot start interactive mode - Missing configuration:")
    if not index:
        print("   ❌ Upstash Vector not initialized")
    if not groq_client:
        print("   ❌ Groq client not initialized")
    print("\nPlease check your .env configuration and try again")
