"""
Test Upstash Vector connection and basic functionality
"""
import os
from dotenv import load_dotenv
from upstash_vector import Index

def test_upstash_connection():
    """Test basic Upstash Vector connectivity"""
    print("🧪 Testing Upstash Vector Connection")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    url = os.getenv('UPSTASH_VECTOR_REST_URL')
    token = os.getenv('UPSTASH_VECTOR_REST_TOKEN')
    
    if not url or not token:
        print("❌ Missing environment variables!")
        print("Please set UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN in .env file")
        return False
    
    print(f"✅ URL found: {url[:50]}...")
    print(f"✅ Token found: {token[:20]}...")
    
    try:
        # Initialize index
        index = Index.from_env()
        print("✅ Upstash Vector client initialized")
        
        # Test with a simple query (this will work even with empty index)
        print("🔍 Testing query functionality...")
        results = index.query(
            data="test query",
            top_k=1,
            include_metadata=True
        )
        
        print(f"✅ Query successful! Found {len(results)} results")
        
        # Test upsert functionality
        print("📤 Testing upsert functionality...")
        test_vector = [
            ("test_id", "This is a test food item", {"type": "test"})
        ]
        
        index.upsert(vectors=test_vector)
        print("✅ Upsert successful!")
        
        # Test query with actual data
        print("🔍 Testing query with test data...")
        results = index.query(
            data="test food",
            top_k=1,
            include_metadata=True
        )
        
        if results:
            print(f"✅ Found test data! Score: {results[0].score:.3f}")
        else:
            print("⚠️  No results found, but connection works")
        
        print("\n🎉 All tests passed! Upstash Vector is ready!")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_upstash_connection()