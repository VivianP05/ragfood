#!/usr/bin/env python3
"""
Interactive script to update Upstash credentials in .env file
"""

import os

def update_env_file():
    print("=" * 70)
    print("  🔑 UPDATE UPSTASH VECTOR CREDENTIALS")
    print("=" * 70)
    print()
    
    print("📍 Your database URL: https://free-loon-62438-us1-vector.upstash.io")
    print()
    print("To get your token:")
    print("1. Go to: https://console.upstash.com/vector")
    print("2. Click on: 'free-loon-62438'")
    print("3. Click the 'Connect' tab")
    print("4. Copy the REST_TOKEN")
    print()
    print("=" * 70)
    print()
    
    # Get token from user
    print("Please paste your UPSTASH_VECTOR_REST_TOKEN here:")
    print("(It should start with 'AByf' or similar)")
    print()
    token = input("Token: ").strip()
    
    if not token:
        print("❌ Error: No token provided!")
        return
    
    if len(token) < 20:
        print("⚠️  Warning: Token seems too short. Are you sure it's correct?")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
    
    # Get Groq API key (keep existing or ask for new)
    groq_key = "your-groq-api-key-here"  # Replace with your actual key
    print()
    print(f"Current Groq API Key: {groq_key[:20]}...")
    use_existing = input("Keep this Groq key? (y/n): ").strip().lower()
    
    if use_existing != 'y':
        groq_key = input("Enter new Groq API key: ").strip()
    
    # Create .env content
    env_content = f'''UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="{token}"
GROQ_API_KEY="{groq_key}"
'''
    
    # Show preview
    print()
    print("=" * 70)
    print("  📝 NEW .ENV FILE CONTENT:")
    print("=" * 70)
    print(env_content)
    print("=" * 70)
    print()
    
    # Confirm
    confirm = input("Save this to .env file? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # Backup existing .env
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                old_content = f.read()
            with open('.env.backup', 'w') as f:
                f.write(old_content)
            print("✅ Backed up old .env to .env.backup")
        
        # Write new .env
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file updated successfully!")
        print()
        print("=" * 70)
        print("  🎯 NEXT STEPS:")
        print("=" * 70)
        print()
        print("1. Test connection:")
        print("   python3 -c \"from upstash_vector import Index; from dotenv import load_dotenv; load_dotenv(); i = Index.from_env(); print('Connected!'); print(f'Vectors: {i.info().vector_count}')\"")
        print()
        print("2. Upload food data:")
        print("   python3 upload_foods_to_upstash.py")
        print()
        print("3. Check database:")
        print("   python3 check_upstash_database.py")
        print()
        print("=" * 70)
    else:
        print("❌ Cancelled. .env file not updated.")

if __name__ == "__main__":
    try:
        update_env_file()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
