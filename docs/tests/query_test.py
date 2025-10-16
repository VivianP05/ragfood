#!/usr/bin/env python3
import time
import json
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import your RAG implementations
try:
    from rag_run import query_rag as query_rag_chromadb
except ImportError:
    print("Warning: ChromaDB implementation not available")
    query_rag_chromadb = None

try:
    from rag_run_upstash import query_rag as query_rag_upstash
except ImportError:
    print("Warning: Upstash implementation not available")
    query_rag_upstash = None

try:
    from rag_run_groq_streaming import query_rag as query_rag_groq
except ImportError:
    print("Warning: Groq implementation not available") 
    query_rag_groq = None

# Load test queries
queries = [
    "healthy Mediterranean options",
    "meals with olive oil and herbs",
    "light dishes with fresh vegetables",
    "spicy vegetarian Asian dishes",
    "gluten-free vegan meals",
    "low-calorie dinner foods",
    "high-protein low-carb foods",
    "foods rich in omega-3",
    "fiber-rich meals with low sugar",
    "traditional comfort foods",
    "popular Asian street foods",
    "festive holiday dishes",
    "dishes that can be grilled",
    "baked vegetarian meals",
    "slow-cooked hearty dishes"
]

def test_implementation(name, query_func, queries):
    """Test a specific RAG implementation"""
    if query_func is None:
        print(f"\n❌ {name} implementation not available")
        return []
    
    print(f"\n🚀 Testing {name} Implementation")
    print("=" * 60)
    
    results = []
    
    for i, query in enumerate(queries[:3], 1):  # Test first 3 queries
        try:
            start = time.time()
            response = query_func(query)
            end = time.time()
            duration = round(end - start, 2)

            print(f"\n[{i}] QUERY: {query}")
            print(f"RESPONSE ({duration}s):")
            if hasattr(response, '__iter__') and not isinstance(response, str):
                # Handle streaming responses
                full_response = ""
                for chunk in response:
                    print(chunk, end="", flush=True)
                    full_response += chunk
                print()  # New line after streaming
                response = full_response
            else:
                print(response)

            results.append({
                "implementation": name,
                "query": query,
                "response": str(response)[:300],  # First 300 chars
                "time": duration,
                "success": True
            })

        except Exception as e:
            print(f"\n❌ Error with query '{query}': {e}")
            results.append({
                "implementation": name,
                "query": query,
                "error": str(e),
                "success": False
            })
    
    return results

def main():
    """Run tests on all available RAG implementations"""
    print("🧪 RAG System Testing Suite")
    print("=" * 60)
    
    all_results = []
    
    # Test each implementation
    implementations = [
        ("ChromaDB + Ollama", query_rag_chromadb),
        ("Upstash Vector", query_rag_upstash), 
        ("Groq Streaming", query_rag_groq)
    ]
    
    for name, func in implementations:
        results = test_implementation(name, func, queries)
        all_results.extend(results)
    
    # Save results
    os.makedirs("../docs", exist_ok=True)
    with open("../docs/query_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Summary
    print(f"\n📊 TESTING SUMMARY")
    print("=" * 60)
    successful = sum(1 for r in all_results if r.get('success', False))
    total = len(all_results)
    print(f"✅ Successful queries: {successful}/{total}")
    print(f"📁 Results saved to: docs/query_results.json")

if __name__ == "__main__":
    main()
