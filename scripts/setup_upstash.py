#!/usr/bin/env python3
"""
Upstash Vector Setup and Validation Script
==========================================

This script helps you set up and validate your Upstash Vector configuration.

Usage:
    python3 scripts/setup_upstash.py --validate    # Check configuration
    python3 scripts/setup_upstash.py --test        # Test connection
    python3 scripts/setup_upstash.py --upload      # Upload data
    python3 scripts/setup_upstash.py --query TEXT  # Test query
"""

import os
import sys
import json
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def check_dependencies():
    """Check if required packages are installed"""
    print_header("🔍 Checking Dependencies")
    
    required = {
        'upstash_vector': 'upstash-vector',
        'dotenv': 'python-dotenv',
        'requests': 'requests'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not installed")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n📦 Install with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed")
    return True

def validate_env_file():
    """Validate .env file exists and has required variables"""
    print_header("🔍 Validating Environment Configuration")
    
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("\n📝 Create .env file with:")
        print("""
UPSTASH_VECTOR_REST_URL=https://your-endpoint.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your-token-here
        """)
        return False
    
    print("✅ .env file exists")
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    url = os.getenv('UPSTASH_VECTOR_REST_URL')
    token = os.getenv('UPSTASH_VECTOR_REST_TOKEN')
    
    if not url:
        print("❌ UPSTASH_VECTOR_REST_URL not set")
        return False
    print(f"✅ UPSTASH_VECTOR_REST_URL found")
    
    if not token:
        print("❌ UPSTASH_VECTOR_REST_TOKEN not set")
        return False
    print(f"✅ UPSTASH_VECTOR_REST_TOKEN found (length: {len(token)})")
    
    return True

def test_connection():
    """Test connection to Upstash Vector"""
    print_header("🧪 Testing Upstash Connection")
    
    try:
        from upstash_vector import Index
        from dotenv import load_dotenv
        
        load_dotenv()
        
        print("🔄 Initializing Upstash Vector client...")
        index = Index.from_env()
        print("✅ Client initialized successfully")
        
        print("\n🔄 Fetching index information...")
        info = index.info()
        
        print(f"\n📊 Index Information:")
        print(f"   Vectors: {info.vector_count}")
        print(f"   Dimension: {info.dimension}")
        print(f"   Similarity: {info.similarity_function}")
        
        if info.vector_count > 0:
            print(f"\n✅ Connection successful! Index has {info.vector_count} vectors")
        else:
            print(f"\n⚠️  Connection successful but index is empty")
            print("   Run with --upload to add data")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Verify credentials in .env file")
        print("2. Check https://console.upstash.com/vector")
        print("3. Ensure index is created with correct embedding model")
        return False

def upload_data():
    """Upload food data to Upstash Vector"""
    print_header("📤 Uploading Data to Upstash Vector")
    
    try:
        from upstash_vector import Index
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Load food data
        json_file = "data/foods.json"
        if not Path(json_file).exists():
            print(f"❌ {json_file} not found")
            return False
        
        with open(json_file, "r", encoding="utf-8") as f:
            food_data = json.load(f)
        
        print(f"✅ Loaded {len(food_data)} food items")
        
        # Initialize index
        print("🔄 Connecting to Upstash Vector...")
        index = Index.from_env()
        print("✅ Connected")
        
        # Prepare vectors
        print(f"\n🔄 Preparing {len(food_data)} vectors for upload...")
        vectors = []
        
        for item in food_data:
            # Handle two data formats: simple (text/region/type) and detailed (name/description/origin)
            if "text" in item:
                # Format 1: Simple format
                enriched_text = item["text"]
                if "region" in item:
                    enriched_text += f" This food is popular in {item['region']}."
                if "type" in item:
                    enriched_text += f" It is a type of {item['type']}."
                
                vectors.append((
                    item["id"],
                    enriched_text,
                    {
                        "original_text": item["text"],
                        "region": item.get("region", "Unknown"),
                        "type": item.get("type", "Unknown")
                    }
                ))
            else:
                # Format 2: Detailed format (name/description/origin/ingredients)
                enriched_text = f"{item['name']}: {item['description']}"
                if "origin" in item:
                    enriched_text += f" This dish originates from {item['origin']}."
                if "ingredients" in item:
                    ingredients = ", ".join(item['ingredients'][:5])  # First 5 ingredients
                    enriched_text += f" Main ingredients: {ingredients}."
                
                vectors.append((
                    item["id"],
                    enriched_text,
                    {
                        "original_text": item.get("description", item.get("name", "")),
                        "name": item.get("name", "Unknown"),
                        "origin": item.get("origin", "Unknown"),
                        "category": item.get("category", "Unknown")
                    }
                ))
        
        print("✅ Vectors prepared")
        
        # Upload
        print(f"\n📤 Uploading to Upstash...")
        index.upsert(vectors=vectors)
        print("✅ Upload complete!")
        
        # Verify
        info = index.info()
        print(f"\n✅ Success! Index now has {info.vector_count} vectors")
        
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_query(query_text):
    """Test a query against Upstash Vector"""
    print_header(f"🔍 Testing Query: '{query_text}'")
    
    try:
        from upstash_vector import Index
        from dotenv import load_dotenv
        
        load_dotenv()
        
        print("🔄 Connecting to Upstash Vector...")
        index = Index.from_env()
        print("✅ Connected")
        
        print(f"\n🔍 Searching for: '{query_text}'")
        results = index.query(
            data=query_text,
            top_k=3,
            include_metadata=True
        )
        
        if not results:
            print("❌ No results found")
            return False
        
        print(f"\n📚 Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  ID: {result.id}")
            print(f"  Score: {result.score:.4f}")
            print(f"  Text: {result.metadata.get('original_text', 'N/A')[:100]}...")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False

def main():
    """Main execution"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 scripts/setup_upstash.py --validate")
        print("  python3 scripts/setup_upstash.py --test")
        print("  python3 scripts/setup_upstash.py --upload")
        print("  python3 scripts/setup_upstash.py --query 'your query here'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--validate":
        print_header("🚀 Upstash Vector - Validation Mode")
        
        if not check_dependencies():
            sys.exit(1)
        
        if not validate_env_file():
            sys.exit(1)
        
        print_header("✅ Validation Complete")
        print("All checks passed! You're ready to use Upstash Vector.")
        print("\nNext steps:")
        print("  1. Test connection: python3 scripts/setup_upstash.py --test")
        print("  2. Upload data: python3 scripts/setup_upstash.py --upload")
        
    elif command == "--test":
        print_header("🚀 Upstash Vector - Connection Test")
        
        if not check_dependencies():
            sys.exit(1)
        
        if not validate_env_file():
            sys.exit(1)
        
        if test_connection():
            print("\n✅ Connection test successful!")
        else:
            sys.exit(1)
    
    elif command == "--upload":
        print_header("🚀 Upstash Vector - Data Upload")
        
        if not check_dependencies():
            sys.exit(1)
        
        if not validate_env_file():
            sys.exit(1)
        
        response = input("\n⚠️  This will upload all food data to Upstash. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Upload cancelled")
            sys.exit(0)
        
        if upload_data():
            print("\n✅ Data upload successful!")
        else:
            sys.exit(1)
    
    elif command == "--query":
        if len(sys.argv) < 3:
            print("❌ Please provide a query text")
            print("Example: python3 scripts/setup_upstash.py --query 'healthy foods'")
            sys.exit(1)
        
        query_text = ' '.join(sys.argv[2:])
        
        if not check_dependencies():
            sys.exit(1)
        
        if not validate_env_file():
            sys.exit(1)
        
        if test_query(query_text):
            print("\n✅ Query test successful!")
        else:
            sys.exit(1)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
