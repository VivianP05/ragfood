#!/usr/bin/env python3
"""
Upload foods.json data to Upstash Vector Database
This script will upload all food items to your Upstash Vector index.
"""

import os
import json
from upstash_vector import Index
from dotenv import load_dotenv
from typing import List, Dict

def load_food_data(file_path: str = "data/foods.json") -> List[Dict]:
    """Load food data from JSON file"""
    print(f"📂 Loading food data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ Loaded {len(data)} food items")
    return data

def prepare_vectors(food_data: List[Dict]) -> List[tuple]:
    """Prepare vectors for Upstash upload with enhanced text"""
    print(f"\n🔧 Preparing vectors for upload...")
    vectors = []
    
    for item in food_data:
        # Handle different data formats
        # Format 1: Simple format with "text" field (items 1-90)
        # Format 2: Detailed format with "name" and "description" fields (items 91-110)
        
        if "text" in item:
            # Simple format (items 1-90)
            base_text = item["text"]
            enriched_text = base_text
            
            if "region" in item and item["region"]:
                enriched_text += f" This food is popular in {item['region']}."
            
            if "type" in item and item["type"]:
                enriched_text += f" It is a type of {item['type']}."
            
            metadata = {
                "original_text": base_text,
                "region": item.get("region", "Unknown"),
                "type": item.get("type", "Unknown"),
                "enhanced_text": enriched_text
            }
        
        elif "name" in item and "description" in item:
            # Detailed format (items 91-110)
            name = item["name"]
            description = item["description"]
            category = item.get("category", "Unknown")
            origin = item.get("origin", "Unknown")
            
            # Create comprehensive text for embedding
            enriched_text = f"{name}: {description}"
            
            if origin and origin != "Unknown":
                enriched_text += f" This dish is from {origin}."
            
            if category and category != "Unknown":
                enriched_text += f" It is a {category}."
            
            # Add ingredients if available
            if "ingredients" in item and item["ingredients"]:
                ingredients_str = ", ".join(item["ingredients"][:5])  # First 5 ingredients
                enriched_text += f" Main ingredients: {ingredients_str}."
            
            metadata = {
                "original_text": description,
                "name": name,
                "region": origin,
                "type": category,
                "enhanced_text": enriched_text,
                "ingredients": item.get("ingredients", []),
                "cooking_method": item.get("cooking_method", ""),
                "dietary_tags": item.get("dietary_tags", [])
            }
        
        else:
            # Skip items without required fields
            print(f"⚠️  Warning: Item {item.get('id', 'unknown')} missing required fields, skipping...")
            continue
        
        # Create vector tuple: (id, text, metadata)
        vectors.append((
            item["id"],
            enriched_text,  # Upstash will auto-embed this
            metadata
        ))
    
    print(f"✅ Prepared {len(vectors)} vectors")
    return vectors

def upload_to_upstash(vectors: List[tuple]) -> dict:
    """Upload vectors to Upstash Vector Database"""
    print(f"\n🚀 Connecting to Upstash Vector...")
    
    # Initialize Upstash client from environment variables
    index = Index.from_env()
    
    print(f"✅ Connected to Upstash Vector")
    
    # Check current vector count before upload
    try:
        info = index.info()
        print(f"📊 Current database stats:")
        print(f"   - Vector count: {info.vector_count}")
        print(f"   - Dimensions: {info.dimension}")
        print(f"   - Similarity: {info.similarity_function}")
    except Exception as e:
        print(f"⚠️  Could not get database info: {e}")
    
    # Upload vectors in batch
    print(f"\n⬆️  Uploading {len(vectors)} vectors to Upstash...")
    
    try:
        # Upstash Vector accepts tuples of (id, data, metadata)
        result = index.upsert(vectors=vectors)
        print(f"✅ Successfully uploaded {len(vectors)} vectors!")
        
        # Check stats after upload
        info = index.info()
        print(f"\n📊 Updated database stats:")
        print(f"   - Total vectors: {info.vector_count}")
        print(f"   - Dimensions: {info.dimension}")
        print(f"   - Similarity: {info.similarity_function}")
        
        return {
            "success": True,
            "uploaded": len(vectors),
            "total_vectors": info.vector_count
        }
        
    except Exception as e:
        print(f"❌ Error uploading vectors: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def test_query(index: Index):
    """Test the uploaded data with a sample query"""
    print(f"\n🧪 Testing with sample query...")
    
    test_queries = [
        "spicy Indian food",
        "sweet fruit",
        "Japanese cuisine"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        try:
            results = index.query(
                data=query,
                top_k=3,
                include_metadata=True
            )
            
            print(f"   Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result.id} (score: {result.score:.4f})")
                if hasattr(result, 'metadata') and result.metadata:
                    print(f"      Text: {result.metadata.get('original_text', 'N/A')}")
                    print(f"      Region: {result.metadata.get('region', 'N/A')}")
                    print(f"      Type: {result.metadata.get('type', 'N/A')}")
        
        except Exception as e:
            print(f"   ❌ Query failed: {e}")

def main():
    """Main execution function"""
    print("=" * 70)
    print("🍕 UPLOAD FOODS.JSON TO UPSTASH VECTOR DATABASE 🍕")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    # Verify environment variables
    if not os.getenv("UPSTASH_VECTOR_REST_URL"):
        print("❌ Error: UPSTASH_VECTOR_REST_URL not found in .env file")
        return
    
    if not os.getenv("UPSTASH_VECTOR_REST_TOKEN"):
        print("❌ Error: UPSTASH_VECTOR_REST_TOKEN not found in .env file")
        return
    
    print(f"✅ Environment variables loaded")
    print(f"   URL: {os.getenv('UPSTASH_VECTOR_REST_URL')[:50]}...")
    
    # Step 1: Load food data
    try:
        food_data = load_food_data()
    except FileNotFoundError:
        print("❌ Error: data/foods.json not found!")
        print("   Please make sure the file exists in the data/ directory")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return
    
    # Step 2: Prepare vectors
    vectors = prepare_vectors(food_data)
    
    # Step 3: Upload to Upstash
    result = upload_to_upstash(vectors)
    
    if result["success"]:
        print(f"\n" + "=" * 70)
        print(f"🎉 SUCCESS! Uploaded {result['uploaded']} food items to Upstash!")
        print(f"📊 Total vectors in database: {result['total_vectors']}")
        print(f"=" * 70)
        
        # Step 4: Test with sample queries
        index = Index.from_env()
        test_query(index)
        
        print(f"\n" + "=" * 70)
        print(f"✅ UPLOAD COMPLETE - Your food database is ready to use!")
        print(f"=" * 70)
        print(f"\n💡 Next steps:")
        print(f"   1. Run: python3 src/rag_run_upstash.py")
        print(f"   2. Test with food queries")
        print(f"   3. Enjoy your cloud-powered RAG system! 🚀")
        
    else:
        print(f"\n❌ Upload failed: {result.get('error', 'Unknown error')}")
        print(f"   Please check your Upstash credentials and try again")

if __name__ == "__main__":
    main()
