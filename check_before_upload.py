#!/usr/bin/env python3
"""
Quick check of Upstash Vector database before uploading profile.

This script verifies:
1. Database connection is working
2. Current vector count
3. Sample existing vectors to avoid duplicates

Usage:
    python3 check_before_upload.py
"""

import os
import sys
from dotenv import load_dotenv
from upstash_vector import Index

# Load environment variables
load_dotenv()

def main():
    print("=" * 80)
    print("🔍 Checking Upstash Vector Database Before Upload")
    print("=" * 80)
    print()
    
    # Verify environment variables
    if not os.getenv("UPSTASH_VECTOR_REST_URL") or not os.getenv("UPSTASH_VECTOR_REST_TOKEN"):
        print("❌ ERROR: Missing environment variables!")
        print("Please set UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN in .env file")
        sys.exit(1)
    
    try:
        # Connect to database
        print("📡 Connecting to Upstash Vector database...")
        index = Index.from_env()
        print("✅ Connected successfully")
        print()
        
        # Get database info
        info = index.info()
        print("📊 Database Statistics:")
        print(f"   Vector Count: {info.vector_count}")
        print(f"   Dimensions: {info.dimension}")
        print(f"   Similarity: {getattr(info, 'similarity_function', 'COSINE')}")
        print()
        
        # Check for existing vivian- prefixed IDs
        print("🔍 Checking for existing profile vectors (ID prefix: vivian-)...")
        
        # Query with a profile-related question to see what exists
        test_results = index.query(
            data="Tell me about Vivian's professional experience",
            top_k=5,
            include_metadata=True
        )
        
        existing_profile_vectors = [r for r in test_results if r.id.startswith('vivian-')]
        
        if existing_profile_vectors:
            print(f"⚠️  Found {len(existing_profile_vectors)} existing profile vectors:")
            for vec in existing_profile_vectors:
                print(f"   - {vec.id}: {vec.metadata.get('name', 'N/A')}")
            print()
            print("   These will be UPDATED with new data (upsert operation)")
        else:
            print("✅ No existing profile vectors found (fresh upload)")
        print()
        
        # Show sample vectors for context
        print("📋 Sample existing vectors in database:")
        sample_query = index.query(
            data="food",
            top_k=3,
            include_metadata=True
        )
        
        for i, result in enumerate(sample_query, 1):
            print(f"   {i}. ID: {result.id}")
            print(f"      Metadata: {result.metadata.get('text', result.metadata.get('name', 'N/A'))[:60]}...")
        print()
        
        print("=" * 80)
        print("✅ Pre-Upload Check Complete!")
        print("=" * 80)
        print()
        print("🚀 Ready to upload? Run:")
        print("   python3 upload_vivian_profile_to_upstash.py")
        print()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    main()
