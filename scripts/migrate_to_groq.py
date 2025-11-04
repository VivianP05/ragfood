#!/usr/bin/env python3
"""
Quick Migration Implementation Script
=====================================
This script helps you quickly migrate from Ollama to Groq Cloud API.

Usage:
    python migrate_to_groq.py --validate    # Check setup
    python migrate_to_groq.py --migrate     # Perform migration
    python migrate_to_groq.py --test        # Test migration
    python migrate_to_groq.py --rollback    # Rollback if needed
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_step(step_num, total_steps, description):
    """Print step progress"""
    print(f"[{step_num}/{total_steps}] {description}")

def validate_environment():
    """Validate environment setup"""
    print_header("🔍 STEP 1: Validating Environment")
    
    issues = []
    
    # Check .env file
    if not Path(".env").exists():
        issues.append("❌ .env file not found")
        print("❌ .env file not found")
    else:
        print("✅ .env file exists")
        
        # Check for GROQ_API_KEY
        with open(".env", "r") as f:
            content = f.read()
            if "GROQ_API_KEY" not in content:
                issues.append("❌ GROQ_API_KEY not in .env")
                print("❌ GROQ_API_KEY not found in .env")
            else:
                print("✅ GROQ_API_KEY found in .env")
    
    # Check Python packages
    print("\n🔍 Checking Python packages...")
    required_packages = ["groq", "python-dotenv", "chromadb", "requests"]
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} installed")
        except ImportError:
            issues.append(f"❌ {package} not installed")
            print(f"❌ {package} not installed")
    
    # Check source files
    print("\n🔍 Checking source files...")
    if not Path("src/rag_run.py").exists():
        issues.append("❌ src/rag_run.py not found")
        print("❌ src/rag_run.py not found")
    else:
        print("✅ src/rag_run.py exists")
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("\n✅ All validation checks passed!")
        return True

def test_groq_connection():
    """Test Groq API connection"""
    print_header("🧪 STEP 2: Testing Groq API Connection")
    
    try:
        from groq import Groq
        from dotenv import load_dotenv
        
        load_dotenv()
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ GROQ_API_KEY not found in environment")
            return False
        
        print(f"✅ API key found (length: {len(api_key)})")
        
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
        
        print("🔄 Testing API with simple query...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'Connection successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ API Response: {result}")
        print("✅ Groq API connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Verify your GROQ_API_KEY is correct")
        print("2. Check https://console.groq.com/keys")
        print("3. Ensure you have internet connection")
        return False

def backup_files():
    """Backup current implementation"""
    print_header("💾 STEP 3: Backing Up Current Files")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backups/pre_groq_migration_{timestamp}")
    
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup rag_run.py
        if Path("src/rag_run.py").exists():
            shutil.copy2("src/rag_run.py", backup_dir / "rag_run.py")
            print(f"✅ Backed up src/rag_run.py")
        
        # Backup ChromaDB
        if Path("chroma_db").exists():
            shutil.copytree("chroma_db", backup_dir / "chroma_db")
            print(f"✅ Backed up chroma_db/")
        
        print(f"\n✅ Backup completed: {backup_dir}")
        return str(backup_dir)
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def create_migration_branch():
    """Create Git branch for migration"""
    print_header("🌿 STEP 4: Creating Git Branch")
    
    try:
        # Check if in git repo
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("⚠️  Not in a Git repository - skipping branch creation")
            return True
        
        # Create and checkout branch
        branch_name = f"groq-migration-{datetime.now().strftime('%Y%m%d')}"
        
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"✅ Created and checked out branch: {branch_name}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Git branch creation failed: {e}")
        print("⚠️  Continuing without git branch...")
        return True

def apply_migration():
    """Apply migration changes"""
    print_header("🔧 STEP 5: Applying Migration Changes")
    
    print("📝 Migration changes to apply:")
    print("  1. Add Groq imports and client initialization")
    print("  2. Add rate limiter class")
    print("  3. Replace LLM generation function")
    print("  4. Add error handling")
    print("  5. Add usage tracking")
    
    print("\n⚠️  Note: This is a complex migration.")
    print("   Please refer to GROQ_MIGRATION_COMPLETE_PLAN.md for detailed code changes.")
    print("   Or use the pre-built rag_run_groq.py implementation.")
    
    response = input("\n❓ Copy rag_run_groq.py to rag_run.py? (y/n): ")
    
    if response.lower() == 'y':
        try:
            if Path("src/rag_run_groq.py").exists():
                shutil.copy2("src/rag_run_groq.py", "src/rag_run.py")
                print("✅ Migrated to Groq implementation")
                return True
            else:
                print("❌ src/rag_run_groq.py not found")
                return False
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    else:
        print("⚠️  Manual migration required - see documentation")
        return False

def test_migration():
    """Test migrated implementation"""
    print_header("🧪 STEP 6: Testing Migration")
    
    try:
        print("🔄 Running test query...")
        
        # Import the migrated version
        sys.path.insert(0, 'src')
        from rag_run import query_rag
        
        test_question = "What are healthy foods?"
        print(f"📝 Test query: '{test_question}'")
        
        answer = query_rag(test_question)
        
        if answer and not answer.startswith("❌"):
            print(f"\n✅ Migration successful!")
            print(f"📄 Sample answer: {answer[:200]}...")
            return True
        else:
            print(f"❌ Query failed: {answer}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def rollback_migration(backup_dir):
    """Rollback to previous version"""
    print_header("⏮️  Rolling Back Migration")
    
    if not backup_dir or not Path(backup_dir).exists():
        print("❌ No backup found to rollback")
        return False
    
    try:
        # Restore rag_run.py
        if Path(backup_dir, "rag_run.py").exists():
            shutil.copy2(Path(backup_dir, "rag_run.py"), "src/rag_run.py")
            print("✅ Restored src/rag_run.py")
        
        print("✅ Rollback completed")
        return True
        
    except Exception as e:
        print(f"❌ Rollback failed: {e}")
        return False

def print_next_steps():
    """Print next steps after migration"""
    print_header("🎯 Next Steps")
    
    print("1. Monitor performance and costs")
    print("   - Check response times")
    print("   - Monitor API usage at https://console.groq.com")
    print("   - Track costs with usage_tracker")
    
    print("\n2. Test thoroughly")
    print("   - Run comprehensive test suite")
    print("   - Test error scenarios")
    print("   - Verify rate limiting works")
    
    print("\n3. Optimize")
    print("   - Fine-tune prompts")
    print("   - Adjust rate limits if needed")
    print("   - Consider caching frequently asked questions")
    
    print("\n4. Deploy")
    print("   - Merge migration branch to main")
    print("   - Update documentation")
    print("   - Notify users of improvements")
    
    print("\n📚 Documentation:")
    print("   - Full plan: docs/GROQ_MIGRATION_COMPLETE_PLAN.md")
    print("   - Groq docs: https://console.groq.com/docs")

def main():
    """Main migration workflow"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python migrate_to_groq.py --validate")
        print("  python migrate_to_groq.py --migrate")
        print("  python migrate_to_groq.py --test")
        print("  python migrate_to_groq.py --rollback")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--validate":
        print_header("🚀 Groq Migration - Validation Mode")
        success = validate_environment()
        if success:
            success = test_groq_connection()
        sys.exit(0 if success else 1)
    
    elif command == "--migrate":
        print_header("🚀 Groq Migration - Full Migration")
        
        # Step 1: Validate
        if not validate_environment():
            print("\n❌ Validation failed - fix issues before migrating")
            sys.exit(1)
        
        # Step 2: Test connection
        if not test_groq_connection():
            print("\n❌ Groq connection failed - check API key")
            sys.exit(1)
        
        # Step 3: Backup
        backup_dir = backup_files()
        if not backup_dir:
            print("\n❌ Backup failed - aborting migration")
            sys.exit(1)
        
        # Step 4: Git branch
        create_migration_branch()
        
        # Step 5: Apply migration
        if not apply_migration():
            print("\n❌ Migration failed")
            response = input("❓ Rollback? (y/n): ")
            if response.lower() == 'y':
                rollback_migration(backup_dir)
            sys.exit(1)
        
        # Step 6: Test
        if not test_migration():
            print("\n⚠️  Migration applied but tests failed")
            response = input("❓ Rollback? (y/n): ")
            if response.lower() == 'y':
                rollback_migration(backup_dir)
            sys.exit(1)
        
        print_next_steps()
        print("\n✅ Migration completed successfully!")
    
    elif command == "--test":
        print_header("🧪 Testing Groq Migration")
        success = test_migration()
        sys.exit(0 if success else 1)
    
    elif command == "--rollback":
        print_header("⏮️  Rolling Back Migration")
        print("⚠️  This will restore the backed-up version")
        
        # Find latest backup
        backups = sorted(Path("backups").glob("pre_groq_migration_*"))
        if not backups:
            print("❌ No backups found")
            sys.exit(1)
        
        latest_backup = backups[-1]
        print(f"📁 Latest backup: {latest_backup}")
        
        response = input("❓ Confirm rollback? (y/n): ")
        if response.lower() == 'y':
            success = rollback_migration(str(latest_backup))
            sys.exit(0 if success else 1)
        else:
            print("❌ Rollback cancelled")
            sys.exit(0)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
