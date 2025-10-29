#!/usr/bin/env python3
"""
Check Upstash Vector Database - Comprehensive Inspection Tool
This script helps you verify and inspect your Upstash Vector database
"""

import os
from upstash_vector import Index
from dotenv import load_dotenv
import json

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_database_info():
    """Get and display database statistics"""
    print_header("📊 DATABASE STATISTICS")
    
    try:
        index = Index.from_env()
        info = index.info()
        
        print(f"✅ Connection successful!")
        print(f"\n📈 Database Info:")
        print(f"   Vector Count:        {info.vector_count}")
        print(f"   Dimensions:          {info.dimension}")
        print(f"   Similarity Function: {info.similarity_function}")
        
        return index, info
    
    except Exception as e:
        print(f"❌ Error connecting to Upstash: {e}")
        return None, None

def list_sample_vectors(index, limit=10):
    """List sample vectors from the database"""
    print_header(f"📋 SAMPLE VECTORS (First {limit} items)")
    
    try:
        # Query with a generic term to get sample results
        results = index.query(
            data="food",
            top_k=limit,
            include_metadata=True
        )
        
        print(f"\nFound {len(results)} sample vectors:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. ID: {result.id}")
            print(f"   Score: {result.score:.4f}")
            
            if hasattr(result, 'metadata') and result.metadata:
                # Display metadata
                if 'name' in result.metadata:
                    print(f"   Name: {result.metadata.get('name', 'N/A')}")
                if 'original_text' in result.metadata:
                    text = result.metadata.get('original_text', 'N/A')
                    print(f"   Text: {text[:100]}{'...' if len(text) > 100 else ''}")
                if 'region' in result.metadata:
                    print(f"   Region: {result.metadata.get('region', 'N/A')}")
                if 'type' in result.metadata:
                    print(f"   Type: {result.metadata.get('type', 'N/A')}")
            print()
    
    except Exception as e:
        print(f"❌ Error listing vectors: {e}")

def test_queries(index):
    """Test various queries to verify data"""
    print_header("🔍 TESTING SAMPLE QUERIES")
    
    test_queries = [
        "spicy Indian food",
        "sweet fruit",
        "Japanese cuisine",
        "Italian pasta",
        "healthy breakfast",
        "dessert"
    ]
    
    for query_text in test_queries:
        print(f"\n🔍 Query: '{query_text}'")
        
        try:
            results = index.query(
                data=query_text,
                top_k=3,
                include_metadata=True
            )
            
            print(f"   Found {len(results)} results:")
            
            for i, result in enumerate(results, 1):
                name = result.metadata.get('name', '') if hasattr(result, 'metadata') and result.metadata else ''
                text = result.metadata.get('original_text', '') if hasattr(result, 'metadata') and result.metadata else ''
                
                display_text = name if name else (text[:60] + '...' if len(text) > 60 else text)
                print(f"   {i}. {result.id}: {display_text} (score: {result.score:.4f})")
        
        except Exception as e:
            print(f"   ❌ Query failed: {e}")

def check_food_coverage(index):
    """Check how many food items are in the database"""
    print_header("🍕 FOOD DATABASE COVERAGE")
    
    try:
        # Try to query for different food categories
        categories = {
            "Fruits": "fruit",
            "Main Course": "main course meal",
            "Snacks": "snack food",
            "Desserts": "dessert sweet",
            "Beverages": "drink beverage",
            "Asian Cuisine": "Asian food",
            "European Cuisine": "European food"
        }
        
        print("\nSearching by category:\n")
        
        for category, query in categories.items():
            results = index.query(
                data=query,
                top_k=5,
                include_metadata=True
            )
            print(f"✓ {category}: Found {len(results)} items")
            
            # Show top match
            if results:
                top_match = results[0]
                name = top_match.metadata.get('name', '') if hasattr(top_match, 'metadata') and top_match.metadata else ''
                text = top_match.metadata.get('original_text', '') if hasattr(top_match, 'metadata') and top_match.metadata else ''
                display = name if name else (text[:50] + '...' if len(text) > 50 else text)
                print(f"  Top match: {display}")
    
    except Exception as e:
        print(f"❌ Error checking coverage: {e}")

def check_digital_twin_data(index):
    """Check if digital twin data is present"""
    print_header("👤 DIGITAL TWIN DATA CHECK")
    
    try:
        # Query for digital twin related terms
        twin_queries = [
            "Vivian Pham",
            "AI Data Analyst",
            "Ausbiz Consulting",
            "interview preparation"
        ]
        
        print("\nSearching for digital twin entries:\n")
        
        for query in twin_queries:
            results = index.query(
                data=query,
                top_k=3,
                include_metadata=True
            )
            
            if results:
                print(f"✓ '{query}': Found {len(results)} related entries")
                top = results[0]
                if hasattr(top, 'metadata') and top.metadata:
                    text = top.metadata.get('content', top.metadata.get('original_text', 'N/A'))
                    print(f"  Preview: {text[:80]}...")
            else:
                print(f"- '{query}': No results found")
    
    except Exception as e:
        print(f"❌ Error checking digital twin data: {e}")

def get_specific_vector(index, vector_id):
    """Fetch a specific vector by ID"""
    print_header(f"🔎 FETCHING SPECIFIC VECTOR: {vector_id}")
    
    try:
        # Use fetch to get specific vector
        result = index.fetch(ids=[vector_id])
        
        if result:
            print(f"✅ Found vector {vector_id}:")
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"❌ Vector {vector_id} not found")
    
    except Exception as e:
        print(f"❌ Error fetching vector: {e}")

def main():
    """Main execution function"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "    🔍 UPSTASH VECTOR DATABASE INSPECTOR 🔍".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Load environment variables
    load_dotenv()
    
    # Verify environment
    if not os.getenv("UPSTASH_VECTOR_REST_URL"):
        print("❌ Error: UPSTASH_VECTOR_REST_URL not found in .env")
        return
    
    if not os.getenv("UPSTASH_VECTOR_REST_TOKEN"):
        print("❌ Error: UPSTASH_VECTOR_REST_TOKEN not found in .env")
        return
    
    print(f"\n✅ Environment variables loaded")
    print(f"   URL: {os.getenv('UPSTASH_VECTOR_REST_URL')}")
    
    # 1. Check database info
    index, info = check_database_info()
    
    if not index:
        print("\n❌ Cannot proceed without database connection")
        return
    
    # 2. List sample vectors
    list_sample_vectors(index, limit=10)
    
    # 3. Test queries
    test_queries(index)
    
    # 4. Check food coverage
    check_food_coverage(index)
    
    # 5. Check digital twin data
    check_digital_twin_data(index)
    
    # 6. Fetch specific vectors (examples)
    print_header("🎯 FETCH SPECIFIC VECTORS")
    print("\nTo fetch a specific vector, use:")
    print("  get_specific_vector(index, 'vector_id')")
    print("\nExample IDs in your database:")
    print("  - Food items: '1', '5', '91', '92'")
    print("  - Digital twin: Check the IDs from digital twin queries above")
    
    # Final summary
    print_header("✅ INSPECTION COMPLETE")
    print(f"""
Summary:
  • Total Vectors: {info.vector_count}
  • Dimensions: {info.dimension}
  • Similarity: {info.similarity_function}
  • Database URL: {os.getenv('UPSTASH_VECTOR_REST_URL')}

Your Upstash database is ready to use! 🚀

To query it in your application:
  python3 src/rag_run_upstash.py

To view in web console:
  https://console.upstash.com/vector
""")

if __name__ == "__main__":
    main()
