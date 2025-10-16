import os
import json
from upstash_vector import Index
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "../data/foods.json" if os.path.exists("../data/foods.json") else "data/foods.json"
LLM_MODEL = "llama3.2"

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
        
        print("✅ Environment variables found")
        return True
        
    except Exception as e:
        print(f"❌ Upstash Vector setup validation failed: {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Create a Vector Index in Upstash Console: https://console.upstash.com/")
        print("2. Choose embedding model: mixedbread-ai/mxbai-embed-large-v1")
        print("3. Copy .env.template to .env")
        print("4. Add your UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN")
        return False

def initialize_upstash_index():
    """Initialize Upstash Vector index with error handling"""
    try:
        index = Index.from_env()
        print("✅ Upstash Vector client initialized successfully")
        return index
    except Exception as e:
        print(f"❌ Failed to initialize Upstash Vector: {e}")
        return None

def load_food_data():
    """Load and validate food data"""
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            food_data = json.load(f)
        print(f"✅ Loaded {len(food_data)} food items from {JSON_FILE}")
        return food_data
    except Exception as e:
        print(f"❌ Failed to load food data: {e}")
        return None

def prepare_vectors_for_upsert(food_data):
    """Prepare all vectors for batch upload to Upstash"""
    vectors_to_upsert = []
    
    for item in food_data:
        # Enhance text with region/type context
        enriched_text = item["text"]
        if "region" in item:
            enriched_text += f" This food is popular in {item['region']}."
        if "type" in item:
            enriched_text += f" It is a type of {item['type']}."
        
        # Prepare vector tuple: (id, text, metadata)
        vectors_to_upsert.append(
            (
                item["id"],
                enriched_text,  # This gets auto-embedded by Upstash
                {
                    "original_text": item["text"],
                    "region": item.get("region", "Unknown"),
                    "type": item.get("type", "Unknown"),
                    "enriched_text": enriched_text
                }
            )
        )
    
    return vectors_to_upsert

def upsert_food_data(index, vectors):
    """Upload all food data to Upstash Vector in a single batch"""
    try:
        print(f"🚀 Uploading {len(vectors)} documents to Upstash Vector...")
        
        # Single batch upsert - no delays needed!
        index.upsert(vectors=vectors)
        
        print("✅ All documents uploaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to upload data: {e}")
        return False

def rag_query(index, question):
    """
    Perform RAG query using Upstash Vector
    """
    try:
        print(f"\n🔍 Processing query: '{question}'")
        
        # Step 1: Query Upstash Vector (automatic embedding + search)
        print("🧠 Searching Upstash Vector database...")
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        if not results:
            return "❌ No relevant food information found for your question."
        
        # Step 2: Extract and display retrieved information
        print(f"\n📚 Found {len(results)} relevant food items:\n")
        
        top_docs = []
        for i, result in enumerate(results):
            print(f"🔹 Match {i + 1} (ID: {result.id}, Relevance: {result.score:.3f}):")
            print(f"    \"{result.metadata['original_text']}\"\n")
            top_docs.append(result.metadata['original_text'])
        
        # Step 3: Build context for LLM
        context = "\n".join(top_docs)
        prompt = f"""Use the following food information to answer the question comprehensively.

Food Context:
{context}

Question: {question}
Answer:"""
        
        # Step 4: Generate answer with Ollama
        print("🤖 Generating response with Ollama...")
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"❌ Error connecting to Ollama LLM (status: {response.status_code})"
        
    except Exception as e:
        return f"❌ Error during RAG query: {str(e)}"

# Standardized wrapper function
def query_rag(question):
    index = initialize_upstash_index()
    if index:
        return rag_query(index, question)
    return "❌ Failed to initialize Upstash Vector"

def main():
    """Main execution function"""
    print("🍽️  RAG Food System with Upstash Vector")
    print("="*50)
    
    # Step 1: Validate setup
    if not validate_upstash_setup():
        return
    
    # Step 2: Initialize Upstash Vector
    index = initialize_upstash_index()
    if not index:
        return
    
    # Step 3: Load food data
    food_data = load_food_data()
    if not food_data:
        return
    
    # Step 4: Prepare and upload data
    vectors = prepare_vectors_for_upsert(food_data)
    if not upsert_food_data(index, vectors):
        return
    
    # Step 5: Interactive RAG loop
    print("\n🧠 RAG System Ready! Ask questions about food (type 'exit' to quit)")
    print("="*50)
    
    while True:
        try:
            question = input("\n💭 You: ").strip()
            
            if question.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye! Thanks for exploring food with RAG!")
                break
            
            if not question:
                print("⚠️  Please enter a question about food.")
                continue
            
            # Process the question
            answer = rag_query(index, question)
            print(f"\n🤖 Assistant: {answer}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
