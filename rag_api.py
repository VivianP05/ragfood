#!/usr/bin/env python3
"""
RAG API Wrapper for Next.js Integration
Provides a simple CLI interface for the RAG system
"""

import sys
import json
import os
from io import StringIO
from contextlib import redirect_stdout
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

# Load environment variables
load_dotenv()

def query_food_silent(question: str) -> str:
    """
    Query the food database and get AI-powered answer (silent mode for API)
    
    Args:
        question: Your food-related question
        
    Returns:
        AI-generated answer based on your food database
    """
    try:
        # Initialize Upstash Vector
        index = Index.from_env()
        
        # Search for relevant food items
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        if not results:
            return "No relevant food information found."
        
        # Build context
        context_docs = []
        for result in results:
            text = result.metadata.get('original_text', result.metadata.get('enhanced_text', 'N/A'))
            context_docs.append(text)
        
        context = "\n".join(context_docs)
        
        # Generate answer with Groq
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
        raise Exception(f"RAG query failed: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No question provided",
            "usage": "python3 rag_api.py 'Your question here'"
        }))
        sys.exit(1)
    
    question = sys.argv[1]
    
    try:
        # Query the RAG system (silent mode, no print statements)
        result = query_food_silent(question)
        
        # Return JSON response
        response = {
            "success": True,
            "question": question,
            "answer": result
        }
        print(json.dumps(response))
        
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "question": question
        }
        print(json.dumps(error_response))
        sys.exit(1)

if __name__ == "__main__":
    main()
