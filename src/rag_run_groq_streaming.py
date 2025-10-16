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
CHROMA_DIR = "../chroma_db" if os.path.exists("../chroma_db") else "chroma_db"
COLLECTION_NAME = "foods"
JSON_FILE = "../data/foods.json" if os.path.exists("../data/foods.json") else "data/foods.json"
EMBED_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama-3.1-8b-instant"
GROQ_MAX_TOKENS = 1024
GROQ_TEMPERATURE = 0.7
GROQ_TIMEOUT = 30

class GroqRateLimiter:
    """Simple rate limiter for Groq API calls"""
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

# Global rate limiter
rate_limiter = GroqRateLimiter()

def validate_environment():
    """Validate required environment variables and setup"""
    print("🔍 Validating environment setup...")
    
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("📋 Setup Instructions:")
        print("1. Go to https://console.groq.com/keys")
        print("2. Create a new API key")
        print("3. Copy .env.template to .env")
        print("4. Add GROQ_API_KEY=your_actual_key to .env file")
        return False
    
    print("✅ GROQ_API_KEY found")
    
    # Check if ChromaDB directory exists
    if not os.path.exists(CHROMA_DIR):
        print("⚠️ ChromaDB directory not found - will be created on first run")
    
    # Check if foods.json exists
    if not os.path.exists(JSON_FILE):
        print(f"❌ {JSON_FILE} not found!")
        return False
    
    print("✅ All environment checks passed")
    return True

def initialize_groq_client():
    """Initialize Groq client with API key validation"""
    try:
        client = Groq()
        print("✅ Groq client initialized successfully")
        return client
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return None

def test_groq_connection(client):
    """Test Groq API connection with a simple query"""
    try:
        print("🧪 Testing Groq API connection...")
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": "Hello! Please respond with just 'Connection successful'"}],
            max_tokens=10,
            timeout=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Groq API connection successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        print("🔧 Troubleshooting:")
        print("1. Check your GROQ_API_KEY is correct")
        print("2. Verify you have API credits/quota available") 
        print("3. Check your internet connection")
        return False

def generate_with_groq_streaming(client, prompt, max_retries=3):
    """Generate response using Groq API with streaming support"""
    
    for attempt in range(max_retries):
        try:
            # Apply rate limiting
            rate_limiter.wait_if_needed()
            
            # Make streaming API call
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
                stream=True,
                stop=None
            )
            
            # Stream the response
            print("🤖 Groq AI: ", end="", flush=True)
            full_response = ""
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print()  # New line after streaming completes
            
            if not full_response.strip():
                raise ValueError("Empty response from Groq API")
                
            return full_response.strip()
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific error types
            if "rate limit" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5  # 5, 10, 20 seconds
                    print(f"\n⏳ Rate limited. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "❌ Rate limit exceeded. Please try again later."
            
            elif "quota" in error_msg or "credits" in error_msg:
                return "❌ API quota exceeded. Please check your Groq account credits."
            
            elif "timeout" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"\n⏳ Request timeout. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "❌ Request timed out after multiple attempts."
            
            elif "authentication" in error_msg or "401" in error_msg:
                return "❌ Authentication failed. Please check your GROQ_API_KEY."
            
            else:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"\n⚠️ Groq API attempt {attempt + 1}/{max_retries} failed: {e}")
                    print(f"⏳ Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
    
    return f"❌ Groq API failed after {max_retries} attempts. Please try again later."

def generate_with_groq_non_streaming(client, prompt, max_retries=3):
    """Generate response using Groq API without streaming (faster for simple responses)"""
    
    for attempt in range(max_retries):
        try:
            # Apply rate limiting
            rate_limiter.wait_if_needed()
            
            # Make non-streaming API call
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
            
            # Extract and return response
            response = completion.choices[0].message.content.strip()
            if not response:
                raise ValueError("Empty response from Groq API")
                
            return response
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Handle specific error types (same as streaming version)
            if "rate limit" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5
                    print(f"⏳ Rate limited. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "❌ Rate limit exceeded. Please try again later."
            
            elif "quota" in error_msg or "credits" in error_msg:
                return "❌ API quota exceeded. Please check your Groq account credits."
            
            elif "timeout" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"⏳ Request timeout. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return "❌ Request timed out after multiple attempts."
            
            elif "authentication" in error_msg or "401" in error_msg:
                return "❌ Authentication failed. Please check your GROQ_API_KEY."
            
            else:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"⚠️ Groq API attempt {attempt + 1}/{max_retries} failed: {e}")
                    print(f"⏳ Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
    
    return f"❌ Groq API failed after {max_retries} attempts. Please try again later."

# Ollama embedding function (unchanged)
def get_embedding(text):
    """Get embedding from local Ollama server"""
    try:
        response = requests.post("http://localhost:11434/api/embeddings", json={
            "model": EMBED_MODEL,
            "prompt": text
        })
        if response.status_code == 200:
            return response.json()["embedding"]
        else:
            raise Exception(f"Ollama embedding failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        raise e

def normalize_food_item(item):
    """Normalize food item to consistent format"""
    normalized = {
        'id': item['id']
    }
    
    # Handle text/description
    if 'text' in item:
        normalized['text'] = item['text']
    elif 'description' in item:
        # Create enhanced text from new format
        text_parts = []
        if 'name' in item:
            text_parts.append(f"{item['name']} is")
        text_parts.append(item['description'])
        normalized['text'] = ' '.join(text_parts)
    
    # Handle region/origin
    if 'region' in item:
        normalized['region'] = item['region']
    elif 'origin' in item:
        normalized['region'] = item['origin']
    else:
        normalized['region'] = 'Unknown'
    
    # Handle type/category  
    if 'type' in item:
        normalized['type'] = item['type']
    elif 'category' in item:
        normalized['type'] = item['category']
    else:
        normalized['type'] = 'Unknown'
        
    return normalized

def load_and_setup_data():
    """Load food data and setup ChromaDB"""
    print("📂 Loading food data and setting up vector database...")
    
    # Load food data
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        # Normalize all items to consistent format
        food_data = [normalize_food_item(item) for item in raw_data]
        print(f"✅ Loaded {len(food_data)} food items from {JSON_FILE}")
    except Exception as e:
        print(f"❌ Failed to load food data: {e}")
        return None, None
    
    # Setup ChromaDB
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
        print("✅ ChromaDB setup successful")
    except Exception as e:
        print(f"❌ ChromaDB setup failed: {e}")
        return None, None
    
    # Add new items to ChromaDB
    try:
        existing_ids = set(collection.get()['ids'])
        new_items = [item for item in food_data if item['id'] not in existing_ids]

        if new_items:
            print(f"🆕 Adding {len(new_items)} new documents to ChromaDB...")
            for item in new_items:
                # Enhance text with region/type
                enriched_text = item["text"]
                if "region" in item:
                    enriched_text += f" This food is popular in {item['region']}."
                if "type" in item:
                    enriched_text += f" It is a type of {item['type']}."

                emb = get_embedding(enriched_text)

                collection.add(
                    documents=[item["text"]],  # Use original text as retrievable context
                    embeddings=[emb],
                    ids=[item["id"]]
                )
            print("✅ All new documents added to ChromaDB")
        else:
            print("✅ All documents already in ChromaDB")
    
    except Exception as e:
        print(f"❌ Failed to update ChromaDB: {e}")
        return None, None
    
    return food_data, collection

def rag_query(question, groq_client, collection, use_streaming=True):
    """Enhanced RAG query using ChromaDB + Groq with streaming option"""
    try:
        print(f"\n🔍 Processing query: '{question}'")
        
        # Step 1: Get embedding for the question
        print("🧠 Generating question embedding...")
        q_emb = get_embedding(question)

        # Step 2: Query ChromaDB for similar documents
        print("🔍 Searching vector database...")
        results = collection.query(query_embeddings=[q_emb], n_results=3)

        # Step 3: Extract documents and IDs
        top_docs = results['documents'][0] if results['documents'] and results['documents'][0] else []
        top_ids = results['ids'][0] if results['ids'] and results['ids'][0] else []

        if not top_docs:
            return "❌ No relevant food information found in the database."

        # Step 4: Display retrieved information
        print(f"\n📚 Found {len(top_docs)} relevant food items:")
        for i, doc in enumerate(top_docs):
            print(f"🔹 Source {i + 1} (ID: {top_ids[i]}):")
            print(f"    \"{doc}\"\n")

        if use_streaming:
            print("🌊 Generating streaming response with Groq...")
        else:
            print("🤖 Generating response with Groq...")

        # Step 5: Build enhanced prompt for Groq
        context = "\n".join(top_docs)

        prompt = f"""You are a knowledgeable food expert. Use the provided context to give a comprehensive, engaging, and accurate answer about food.

Context about relevant foods:
{context}

User Question: {question}

Please provide a detailed, informative response that:
1. Directly addresses the user's question
2. Uses information from the provided context
3. Is engaging and conversational
4. Includes interesting details about the foods mentioned
5. Is accurate and helpful

Your response:"""

        # Step 6: Generate response with Groq (streaming or non-streaming)
        if use_streaming:
            response = generate_with_groq_streaming(groq_client, prompt)
        else:
            response = generate_with_groq_non_streaming(groq_client, prompt)
            print(f"🤖 Groq AI: {response}")
        
        return response
        
    except Exception as e:
        return f"❌ Error in RAG query: {str(e)}"

def main():
    """Main function with comprehensive setup and error handling"""
    print("🍽️  RAG Food System with Groq AI (Streaming Support)")
    print("=" * 60)
    
    # Step 1: Validate environment
    if not validate_environment():
        print("\n❌ Environment validation failed. Please fix the issues above.")
        return
    
    # Step 2: Initialize Groq client
    groq_client = initialize_groq_client()
    if not groq_client:
        print("\n❌ Failed to initialize Groq client. Please check your setup.")
        return
    
    # Step 3: Test Groq connection
    if not test_groq_connection(groq_client):
        print("\n❌ Groq API connection failed. Please check your API key and credits.")
        return
    
    # Step 4: Load data and setup ChromaDB
    food_data, collection = load_and_setup_data()
    if not food_data or not collection:
        print("\n❌ Failed to setup data. Please check Ollama is running.")
        return
    
    # Step 5: Get user preference for streaming
    print("\n🎛️ Response Mode:")
    print("1. 🌊 Streaming (see response as it's generated)")
    print("2. ⚡ Fast (get complete response at once)")
    
    mode_choice = input("\nChoose mode (1/2, default=1): ").strip()
    use_streaming = mode_choice != "2"
    
    mode_name = "Streaming" if use_streaming else "Fast"
    print(f"✅ Using {mode_name} mode")
    
    # Step 6: Interactive RAG loop
    print(f"\n🧠 RAG System Ready! Ask questions about food (type 'exit' to quit)")
    print(f"🤖 Powered by Groq AI with {mode_name} responses!")
    print("💡 Type 'switch' to toggle between streaming/fast mode")
    print("=" * 60)
    
    while True:
        try:
            question = input("\n💭 You: ").strip()
            
            if question.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye! Thanks for exploring food with RAG + Groq!")
                break
            
            if question.lower() == "switch":
                use_streaming = not use_streaming
                mode_name = "Streaming" if use_streaming else "Fast"
                print(f"🔄 Switched to {mode_name} mode")
                continue
            
            if not question:
                print("⚠️  Please enter a question about food.")
                continue
            
            # Process the question with Groq
            answer = rag_query(question, groq_client, collection, use_streaming)
            
            if not use_streaming:
                # Response already printed for non-streaming
                pass
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again or type 'exit' to quit.")

# Standardized wrapper function
def query_rag(question):
    """Standardized entry point for RAG queries with streaming"""
    groq_client = initialize_groq_client()
    food_data, collection = load_and_setup_data()
    if groq_client and collection:
        return rag_query(question, groq_client, collection, use_streaming=True)
    return "❌ Failed to initialize system components"

if __name__ == "__main__":
    main()