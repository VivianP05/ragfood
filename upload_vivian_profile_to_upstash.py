#!/usr/bin/env python3
"""
Upload Vivian's Professional Profile to Upstash Vector Database

This script uploads Vivian Pham's enhanced professional profile to Upstash Vector
for use in the digital twin RAG system. The profile includes:
- Basic information and contact details
- Compensation expectations ($500-600/day contracts, $55k-$70k permanent)
- Work authorization and availability (Australian citizen, immediate start, full-time)
- Technical skills (Excel Level 5, Power BI certified, Python, SQL, TypeScript)
- Three STAR format projects (Data Quality Automation, KPI Dashboard, ragfood)
- Soft skills with evidence (Communication, Problem-Solving, Learning Agility, Time Management)
- Career goals and target companies
- Behavioral interview answers
- Weakness mitigation strategies

The script uses Upstash Vector's auto-embedding feature with the mxbai-embed-large-v1 model.

Usage:
    python3 upload_vivian_profile_to_upstash.py

Environment Variables Required:
    UPSTASH_VECTOR_REST_URL - Your Upstash Vector database URL
    UPSTASH_VECTOR_REST_TOKEN - Your Upstash Vector authentication token

Author: Vivian Pham
Date: October 29, 2025
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
from upstash_vector import Index

# Load environment variables
load_dotenv()

# Verify environment variables
if not os.getenv("UPSTASH_VECTOR_REST_URL") or not os.getenv("UPSTASH_VECTOR_REST_TOKEN"):
    print("❌ ERROR: Missing environment variables!")
    print("Please set UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN in .env file")
    sys.exit(1)


def load_profile_data(file_path: str = "data/vivian_professional_profile.json") -> List[Dict]:
    """
    Load Vivian's professional profile data from JSON file.
    
    Args:
        file_path: Path to the JSON file containing profile data
        
    Returns:
        List of profile entry dictionaries
        
    Raises:
        FileNotFoundError: If the JSON file doesn't exist
        json.JSONDecodeError: If the JSON file is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        print(f"✅ Loaded {len(profile_data)} profile entries from {file_path}")
        return profile_data
        
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {file_path}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Please ensure the profile JSON file exists at: {file_path}")
        sys.exit(1)
        
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in {file_path}")
        print(f"Error details: {e}")
        sys.exit(1)


def prepare_vectors(profile_data: List[Dict]) -> List[Tuple[str, str, Dict]]:
    """
    Prepare profile data for upload to Upstash Vector.
    
    Creates enriched text descriptions combining all relevant information
    from each profile entry for better semantic search results.
    
    Args:
        profile_data: List of profile entry dictionaries
        
    Returns:
        List of tuples (id, enriched_text, metadata) ready for upsertion
    """
    vectors = []
    
    for entry in profile_data:
        # Extract core fields
        entry_id = entry.get("id", "unknown")
        section = entry.get("section", "general")
        name = entry.get("name", "")
        category = entry.get("category", "")
        text = entry.get("text", "")
        metadata = entry.get("metadata", {})
        
        # Create enriched text for better search results
        # Combine name, category, and full text
        enriched_text = f"{name}\n\nCategory: {category}\n\n{text}"
        
        # Add section to metadata
        enhanced_metadata = {
            "section": section,
            "category": category,
            "name": name,
            **metadata  # Include all original metadata
        }
        
        # Create vector tuple: (id, text, metadata)
        # Upstash will automatically embed the text using mxbai-embed-large-v1
        vectors.append((entry_id, enriched_text, enhanced_metadata))
        
        print(f"  ✓ Prepared: {entry_id} - {name[:50]}...")
    
    print(f"✅ Prepared {len(vectors)} vectors for upload")
    return vectors


def upload_to_upstash(vectors: List[Tuple[str, str, Dict]]) -> Dict:
    """
    Upload profile vectors to Upstash Vector database.
    
    Uses Upstash Vector's auto-embedding feature to automatically
    generate embeddings using the mxbai-embed-large-v1 model.
    
    Args:
        vectors: List of tuples (id, text, metadata)
        
    Returns:
        Dictionary with upload statistics
    """
    try:
        # Initialize Upstash Vector index
        print("\n📡 Connecting to Upstash Vector database...")
        index = Index.from_env()
        print("✅ Connected successfully")
        
        # Upload vectors (auto-embedding enabled)
        print(f"\n📤 Uploading {len(vectors)} professional profile vectors...")
        print("   (Upstash will auto-embed using mxbai-embed-large-v1 model)")
        
        # Upsert vectors to database
        # Format: index.upsert(vectors=[(id, text, metadata), ...])
        result = index.upsert(vectors=vectors)
        
        print("✅ Upload complete!")
        print(f"   Uploaded: {len(vectors)} vectors")
        
        return {
            "success": True,
            "uploaded_count": len(vectors),
            "result": result
        }
        
    except Exception as e:
        print(f"❌ ERROR during upload: {e}")
        print(f"Error type: {type(e).__name__}")
        return {
            "success": False,
            "error": str(e)
        }


def test_query(index: Optional[Index] = None, question: str = "What are your salary expectations?") -> None:
    """
    Test the uploaded profile with a sample query.
    
    Args:
        index: Upstash Vector index (will create if None)
        question: Test question to ask
    """
    try:
        print(f"\n🧪 Testing with query: '{question}'")
        
        # Initialize index if not provided
        if index is None:
            index = Index.from_env()
        
        # Query the database
        results = index.query(
            data=question,
            top_k=3,
            include_metadata=True
        )
        
        print(f"✅ Found {len(results)} relevant profile entries:\n")
        
        for i, result in enumerate(results, 1):
            score = result.score
            metadata = result.metadata
            
            print(f"{i}. Score: {score:.4f}")
            print(f"   ID: {result.id}")
            print(f"   Section: {metadata.get('section', 'N/A')}")
            print(f"   Category: {metadata.get('category', 'N/A')}")
            print(f"   Name: {metadata.get('name', 'N/A')}")
            print()
        
    except Exception as e:
        print(f"❌ ERROR during test query: {e}")


def main():
    """
    Main execution function.
    
    Workflow:
    1. Load profile data from JSON
    2. Prepare vectors with enriched text
    3. Upload to Upstash Vector database
    4. Test with sample queries
    """
    print("=" * 80)
    print("🚀 Vivian's Professional Profile Upload to Upstash Vector")
    print("=" * 80)
    print()
    
    # Step 1: Load profile data
    print("📂 STEP 1: Loading profile data...")
    profile_data = load_profile_data()
    
    # Print profile statistics
    sections = {}
    for entry in profile_data:
        section = entry.get("section", "unknown")
        sections[section] = sections.get(section, 0) + 1
    
    print("\n📊 Profile Statistics:")
    print(f"   Total entries: {len(profile_data)}")
    print(f"   Sections breakdown:")
    for section, count in sorted(sections.items()):
        print(f"      - {section}: {count} entries")
    print()
    
    # Step 2: Prepare vectors
    print("🔧 STEP 2: Preparing vectors...")
    vectors = prepare_vectors(profile_data)
    print()
    
    # Step 3: Upload to Upstash
    print("📤 STEP 3: Uploading to Upstash Vector...")
    upload_result = upload_to_upstash(vectors)
    print()
    
    if not upload_result["success"]:
        print("❌ Upload failed. Exiting...")
        sys.exit(1)
    
    # Step 4: Test queries
    print("🧪 STEP 4: Testing with sample queries...")
    
    # Initialize index for testing
    index = Index.from_env()
    
    # Test queries relevant to ICG Data Analyst role
    test_queries = [
        "What are your salary expectations?",
        "Do you have Power BI experience?",
        "Tell me about your Excel skills",
        "What data quality projects have you worked on?",
        "Are you available for full-time work?",
        "What are your career goals?"
    ]
    
    for query in test_queries:
        test_query(index, query)
        print("-" * 80)
    
    # Final summary
    print()
    print("=" * 80)
    print("✅ UPLOAD COMPLETE!")
    print("=" * 80)
    print()
    print("📊 Summary:")
    print(f"   ✓ Uploaded: {upload_result['uploaded_count']} professional profile vectors")
    print(f"   ✓ Embedding model: mxbai-embed-large-v1 (1024 dimensions)")
    print(f"   ✓ Database: Upstash Vector (free-loon-62438)")
    print()
    print("🎯 Your Digital Twin is now ready for:")
    print("   • Recruiter questions about salary, availability, skills")
    print("   • Interview practice with STAR format project stories")
    print("   • Technical skills assessment queries")
    print("   • Behavioral interview preparation")
    print()
    print("🚀 Next Steps:")
    print("   1. Test your digital twin with: python3 digital_twin_rag.py")
    print("   2. Run interactive queries with: python3 rag_food_query.py")
    print("   3. Use the web interface at: cd mydigitaltwin && npm run dev")
    print()
    print("💡 Sample questions to try:")
    print("   • 'What's your salary expectation for contract roles?'")
    print("   • 'Tell me about your Power BI certification'")
    print("   • 'Describe a data quality project using the STAR format'")
    print("   • 'What are your Excel skills and achievements?'")
    print()


if __name__ == "__main__":
    main()
