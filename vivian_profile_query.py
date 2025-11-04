#!/usr/bin/env python3
"""
Professional Profile RAG Query System
Query Vivian's professional profile using RAG (Retrieval-Augmented Generation)

This script queries the professional profile vectors (vivian-001 to vivian-027)
stored in Upstash Vector database and generates AI-powered responses using Groq.

Usage:
    python3 vivian_profile_query.py "What are my salary expectations?"
    python3 vivian_profile_query.py  # Interactive mode

Environment Variables Required:
    UPSTASH_VECTOR_REST_URL - Your Upstash Vector database URL
    UPSTASH_VECTOR_REST_TOKEN - Your Upstash Vector authentication token
    GROQ_API_KEY - Your Groq API key for AI generation

Author: Vivian Pham
Date: October 29, 2025
"""

import sys
import json
import os
from dotenv import load_dotenv
from upstash_vector import Index
from groq import Groq

# Load environment variables
load_dotenv()

def query_profile(question: str, silent: bool = False) -> dict:
    """
    Query Vivian's professional profile and get AI-powered answer
    
    Args:
        question: Question about Vivian's professional background
        silent: If True, only return JSON (no progress output)
        
    Returns:
        Dictionary with success, question, answer, and sources
    """
    try:
        if not silent:
            print(f"\n🤔 Question: {question}")
            print("🔍 Searching professional profile...\n")
        
        # Initialize Upstash Vector
        index = Index.from_env()
        
        # Search for relevant profile entries
        # Note: Database has 227 vectors total (200 food + 27 professional)
        # We want to find vivian-* vectors specifically
        results = index.query(
            data=question,
            top_k=5,  # Get more results to ensure we catch vivian-* vectors
            include_metadata=True
        )
        
        if not results:
            return {
                "success": False,
                "question": question,
                "error": "No relevant profile information found."
            }
        
        # Filter for profile vectors (vivian-*) and build context
        profile_results = []
        context_docs = []
        
        for result in results:
            # Prioritize vivian-* vectors
            if result.id.startswith('vivian-'):
                profile_results.append(result)
                
                # Extract text from metadata or use default
                text = result.metadata.get('text', '')
                name = result.metadata.get('name', '')
                category = result.metadata.get('category', '')
                section = result.metadata.get('section', '')
                
                # Build rich context
                context_entry = f"[{section.upper()}] {name}\n{text}"
                context_docs.append(context_entry)
                
                if not silent:
                    print(f"✓ Found: {name} (relevance: {result.score:.3f})")
        
        # If no profile vectors found, try to extract text from any results
        if not profile_results:
            # Fall back to any results (might be food items, but better than nothing)
            for result in results[:3]:
                text = result.metadata.get('text', result.metadata.get('enhanced_text', 'N/A'))
                context_docs.append(text)
        
        if not context_docs:
            return {
                "success": False,
                "question": question,
                "error": "No relevant information found in profile database."
            }
        
        context = "\n\n".join(context_docs)
        
        if not silent:
            print(f"\n💭 Generating AI response...\n")
        
        # Generate answer with Groq
        groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Vivian Pham's professional digital twin assistant. "
                        "Answer questions about Vivian's professional background, skills, experience, "
                        "projects, compensation expectations, availability, and career goals. "
                        "Use the provided profile information to give accurate, detailed, and enthusiastic answers. "
                        "When discussing compensation, mention both contract rates ($500-600/day) and permanent salary ranges ($55k-70k). "
                        "When discussing Power BI, emphasize the Microsoft Power BI Certification Training from The Knowledge Academy. "
                        "When discussing projects, use STAR format (Situation, Task, Action, Result) if appropriate. "
                        "Be professional, confident, and highlight Vivian's strengths."
                    )
                },
                {
                    "role": "user",
                    "content": f"Profile Information:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500
        )
        
        answer = completion.choices[0].message.content
        
        # Build sources list
        sources = []
        for result in profile_results[:3]:
            sources.append({
                "id": result.id,
                "name": result.metadata.get('name', 'N/A'),
                "section": result.metadata.get('section', 'N/A'),
                "relevance": f"{result.score:.3f}"
            })
        
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "sources": sources,
            "profile_vectors_found": len(profile_results)
        }
        
    except Exception as e:
        return {
            "success": False,
            "question": question,
            "error": str(e)
        }

def interactive_mode():
    """Interactive query mode"""
    print("=" * 80)
    print("🎯 Vivian's Professional Profile - Interactive Query System")
    print("=" * 80)
    print()
    print("Ask questions about Vivian's professional background:")
    print("  • Salary expectations and compensation")
    print("  • Technical skills (Excel, Power BI, Python, SQL)")
    print("  • Work experience and projects (STAR format)")
    print("  • Availability and work authorization")
    print("  • Career goals and target companies")
    print("  • Soft skills and behavioral interview answers")
    print()
    print("Type 'exit' or 'quit' to end the session")
    print("=" * 80)
    print()
    
    while True:
        try:
            question = input("💬 Your question: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using the profile query system!")
                break
            
            # Query profile
            result = query_profile(question, silent=False)
            
            if result["success"]:
                print(f"🤖 Answer:\n{result['answer']}\n")
                
                if result.get('sources'):
                    print("📚 Sources:")
                    for src in result['sources']:
                        print(f"  • {src['name']} (relevance: {src['relevance']})")
                    print()
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}\n")
            
            print("-" * 80)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Session ended. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

def main():
    """Main execution function"""
    
    # Check environment variables
    if not os.getenv("UPSTASH_VECTOR_REST_URL") or not os.getenv("UPSTASH_VECTOR_REST_TOKEN"):
        print("❌ ERROR: Missing Upstash Vector credentials in .env file")
        sys.exit(1)
    
    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: Missing GROQ_API_KEY in .env file")
        sys.exit(1)
    
    # Check if question provided as argument
    if len(sys.argv) > 1:
        # CLI mode with question
        question = " ".join(sys.argv[1:])
        result = query_profile(question, silent=True)
        print(json.dumps(result, indent=2))
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
