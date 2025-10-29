#!/usr/bin/env python3
"""
Simple RAG Food Query System - Upstash Vector + Groq
Ask questions about food and get AI-powered answers!
"""

# Essential imports for RAG System
import os
import json
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

# Load environment variables
load_dotenv()

def query_food(question: str) -> str:
    """
    Query the food database and get AI-powered answer
    
    Args:
        question: Your food-related question
        
    Returns:
        AI-generated answer based on your food database
    """
    try:
        # Initialize Upstash Vector
        print(f"🔍 Searching for: '{question}'")
        index = Index.from_env()
        
        # Step 1: Search for relevant food items (auto-embedding + search)
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        if not results:
            return "❌ No relevant food information found."
        
        # Step 2: Display what we found
        print(f"\n📚 Found {len(results)} relevant items:\n")
        
        context_docs = []
        for i, result in enumerate(results, 1):
            text = result.metadata.get('original_text', result.metadata.get('enhanced_text', 'N/A'))
            score = result.score
            
            print(f"   {i}. {text[:80]}... (relevance: {score:.3f})")
            context_docs.append(text)
        
        # Step 3: Build context for AI
        context = "\n".join(context_docs)
        
        # Step 4: Generate answer with Groq
        print(f"\n🤖 Generating answer with Groq AI...")
        
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful food expert assistant. Use the provided food information to answer questions accurately and enthusiastically. If the information doesn't fully answer the question, say so honestly."
                },
                {
                    "role": "user",
                    "content": f"""Use this food information to answer the question:

Food Information:
{context}

Question: {question}

Please provide a helpful, accurate answer based on the information above."""
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500
        )
        
        answer = chat_completion.choices[0].message.content
        
        return answer
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Interactive RAG system"""
    print("=" * 70)
    print("  🍽️  FOOD RAG SYSTEM - Powered by Upstash + Groq")
    print("=" * 70)
    print()
    print("Ask questions about food! Examples:")
    print("  • What is Biryani?")
    print("  • Recommend a healthy breakfast")
    print("  • Tell me about Japanese ramen")
    print("  • What's a good Italian dish?")
    print()
    print("Type 'exit' to quit")
    print("=" * 70)
    
    while True:
        try:
            print()
            question = input("💭 You: ").strip()
            
            if question.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye! Enjoy your culinary adventures!")
                break
            
            if not question:
                print("⚠️  Please enter a question.")
                continue
            
            # Get answer
            print()
            answer = query_food(question)
            
            print(f"\n{'=' * 70}")
            print(f"🤖 Answer:")
            print(f"{'=' * 70}")
            print(answer)
            print(f"{'=' * 70}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
