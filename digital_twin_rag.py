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
            include_metadata=True,
            include_data=True  # Important: request the actual text data
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
                    "content": "You are Vivian Pham's AI assistant. Answer questions about her professional background, skills, experience, projects, and career goals based on the provided context. Be specific, use actual achievements and metrics when available, and speak professionally. If asked about her directly, you can refer to her in third person or use 'I' to represent her."
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
            
            # Get the actual text content from the 'data' attribute
            # This is where Upstash stores the indexed text
            text_content = getattr(result, 'data', None)
            
            # Build a descriptive title from metadata
            if 'name' in metadata:
                # Professional profile or resume format
                name = metadata.get('name', 'Information')
                
                # Build descriptive title based on metadata
                if metadata.get('company'):
                    title = f"{name} at {metadata.get('company')}"
                elif metadata.get('skill'):
                    level = metadata.get('level', metadata.get('proficiency', 'N/A'))
                    title = f"{metadata.get('skill')} Skills (Level {level})"
                else:
                    title = name
            elif 'original_text' in metadata:
                # Food database format
                title = f"{metadata.get('type', 'Item')} from {metadata.get('region', 'Unknown')}"
                text_content = metadata.get('original_text', text_content)
            elif 'content' in metadata:
                # Alternative format
                title = metadata.get('title', 'Information')
                text_content = metadata.get('content', text_content)
            else:
                # Fallback to ID
                title = result.id
            
            score = result.score
            
            print(f"🔹 Found: {title} (Relevance: {score:.3f})")
            
            # Add to context if we have text
            if text_content:
                top_docs.append(f"{title}:\n{text_content}")
        
        if not top_docs:
            return "I found some information but couldn't extract details."
        
        print(f"⚡ Generating response with {len(top_docs)} sources...\n")
        
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
