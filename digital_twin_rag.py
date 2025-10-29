"""
Digital Twin RAG Application
Based on Binal's production implementation
- Upstash Vector: Built-in embeddings and vector storage
- Groq: Ultra-fast LLM inference
"""

import os
import json
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

# Load environment variables
load_dotenv()

# Constants
JSON_FILE = "digitaltwin.json"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
DEFAULT_MODEL = "llama-3.1-8b-instant"

def setup_groq_client():
    """Setup Groq client"""
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found in .env file")
        return None
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq client initialized successfully!")
        return client
    except Exception as e:
        print(f"❌ Error initializing Groq client: {str(e)}")
        return None

def setup_vector_database():
    """Setup Upstash Vector database with built-in embeddings"""
    print("🔄 Connecting to Upstash Vector database...")
    
    try:
        index = Index.from_env()
        print("✅ Connected to Upstash Vector successfully!")
        
        # Check current vector count
        try:
            info = index.info()
            current_count = getattr(info, 'vector_count', 0)
            print(f"📊 Current vectors in database: {current_count}")
            
            if current_count == 0:
                print("⚠️  Database is empty! Please upload data first.")
                print("💡 Run: python3 upload_foods_to_upstash.py")
                return None
            
        except Exception as e:
            print(f"⚠️  Could not check vector count: {e}")
        
        return index
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return None

def query_vectors(index, query_text, top_k=3):
    """Query Upstash Vector for similar vectors"""
    try:
        results = index.query(
            data=query_text,
            top_k=top_k,
            include_metadata=True
        )
        return results
    except Exception as e:
        print(f"❌ Error querying vectors: {str(e)}")
        return None

def generate_response_with_groq(client, prompt, model=DEFAULT_MODEL):
    """Generate response using Groq"""
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI digital twin. Answer questions as if you are the person, speaking in first person about your background, skills, and experience."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return completion.choices[0].message.content.strip()
        
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

def rag_query(index, groq_client, question):
    """Perform RAG query using Upstash Vector + Groq"""
    try:
        # Step 1: Query vector database
        results = query_vectors(index, question, top_k=3)
        
        if not results or len(results) == 0:
            return "I don't have specific information about that topic."
        
        # Step 2: Extract relevant content
        print("\n🧠 Searching database...")
        
        top_docs = []
        for result in results:
            metadata = result.metadata or {}
            
            # Handle different metadata formats
            if 'original_text' in metadata:
                # Food database format
                text = metadata.get('original_text', '')
                title = f"{metadata.get('type', 'Item')} from {metadata.get('region', 'Unknown')}"
            elif 'content' in metadata:
                # Digital twin format
                text = metadata.get('content', '')
                title = metadata.get('title', 'Information')
            elif 'name' in metadata:
                # Named item format
                text = metadata.get('description', metadata.get('enhanced_text', ''))
                title = metadata.get('name', 'Item')
            else:
                # Fallback
                text = str(metadata)
                title = "Information"
            
            score = result.score
            
            print(f"🔹 Found: {title} (Relevance: {score:.3f})")
            if text:
                top_docs.append(f"{title}: {text}")
        
        if not top_docs:
            return "I found some information but couldn't extract details."
        
        print(f"⚡ Generating response...\n")
        
        # Step 3: Generate response with context
        context = "\n".join(top_docs)
        prompt = f"""Based on the following information, answer the question helpfully and accurately.

Information:
{context}

Question: {question}

Provide a helpful, informative response:"""
        
        response = generate_response_with_groq(groq_client, prompt)
        return response
    
    except Exception as e:
        return f"❌ Error during query: {str(e)}"

def main():
    """Main application loop"""
    print("🤖 RAG Query System - Upstash Vector + Groq AI")
    print("=" * 50)
    print("🔗 Vector Storage: Upstash (built-in embeddings)")
    print(f"⚡ AI Inference: Groq ({DEFAULT_MODEL})")
    print("📋 Data Source: Your Upstash Database\n")
    
    # Setup clients
    groq_client = setup_groq_client()
    if not groq_client:
        return
    
    index = setup_vector_database()
    if not index:
        return
    
    print("✅ System ready!\n")
    
    # Interactive chat loop
    print("🤖 Ask questions about the data in your database!")
    print("Type 'exit' to quit.\n")
    
    print("💭 Example questions:")
    print("  - 'What is Biryani?'")
    print("  - 'Recommend a healthy breakfast'")
    print("  - 'Tell me about Japanese cuisine'")
    print("  - 'What desserts do you have?'")
    print()
    
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("👋 Thanks for using the RAG system!")
            break
        
        if question.strip():
            answer = rag_query(index, groq_client, question)
            print(f"\n🤖 Answer: {answer}\n")

if __name__ == "__main__":
    main()
