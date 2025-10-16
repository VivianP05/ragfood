#!/usr/bin/env python3
"""
RAG-Food Project - Main Entry Point
Supports multiple RAG implementations with different backends
"""
import sys
import os
import argparse

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    parser = argparse.ArgumentParser(description='RAG-Food Query System')
    parser.add_argument('--implementation', '-i', 
                       choices=['chromadb', 'upstash', 'groq', 'groq-streaming'],
                       default='groq-streaming',
                       help='Choose RAG implementation (default: groq-streaming)')
    parser.add_argument('--query', '-q', type=str, help='Query to search for')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--test', action='store_true', help='Run test suite')
    
    args = parser.parse_args()
    
    if args.test:
        # Run test suite
        os.system('python3 tests/query_test.py')
        return
    
    # Import the selected implementation
    if args.implementation == 'chromadb':
        try:
            from rag_run import query_rag
            print("🔵 Using ChromaDB + Ollama implementation")
        except ImportError as e:
            print(f"❌ ChromaDB implementation not available: {e}")
            return
    elif args.implementation == 'upstash':
        try:
            from rag_run_upstash import query_rag
            print("🟡 Using Upstash Vector implementation")
        except ImportError as e:
            print(f"❌ Upstash implementation not available: {e}")
            return
    elif args.implementation == 'groq':
        try:
            from rag_run_groq import query_rag
            print("🟢 Using Groq API implementation")
        except ImportError as e:
            print(f"❌ Groq implementation not available: {e}")
            return
    elif args.implementation == 'groq-streaming':
        try:
            from rag_run_groq_streaming import query_rag
            print("🚀 Using Groq Streaming implementation")
        except ImportError as e:
            print(f"❌ Groq Streaming implementation not available: {e}")
            return
    
    if args.interactive:
        print("\n🍽️  RAG-Food Interactive Query System")
        print("Type 'quit', 'exit', or 'q' to stop")
        print("-" * 50)
        
        while True:
            try:
                query = input("\n🔍 Enter your food query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                if not query:
                    continue
                    
                print(f"\n💭 Searching for: {query}")
                print("-" * 40)
                
                response = query_rag(query)
                
                # Handle streaming vs non-streaming responses
                if hasattr(response, '__iter__') and not isinstance(response, str):
                    for chunk in response:
                        print(chunk, end="", flush=True)
                    print()  # New line after streaming
                else:
                    print(response)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    elif args.query:
        print(f"\n🔍 Query: {args.query}")
        print("-" * 40)
        
        response = query_rag(args.query)
        
        # Handle streaming vs non-streaming responses
        if hasattr(response, '__iter__') and not isinstance(response, str):
            for chunk in response:
                print(chunk, end="", flush=True)
            print()  # New line after streaming
        else:
            print(response)
    
    else:
        # No query provided, show usage
        parser.print_help()
        print(f"\n💡 Examples:")
        print(f"  python3 {os.path.basename(__file__)} -q 'spicy asian dishes'")
        print(f"  python3 {os.path.basename(__file__)} --interactive")
        print(f"  python3 {os.path.basename(__file__)} --test")

if __name__ == "__main__":
    main()