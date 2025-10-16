"""
Test Groq API integration and functionality
"""
import os
import time
from dotenv import load_dotenv
from groq import Groq

def test_groq_setup():
    """Comprehensive Groq API testing"""
    print("🧪 Groq API Integration Test")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Step 1: Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment!")
        print("📋 Setup Instructions:")
        print("1. Go to https://console.groq.com/keys")
        print("2. Create a new API key")
        print("3. Copy .env.template to .env")
        print("4. Add GROQ_API_KEY=your_actual_key")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    
    # Step 2: Initialize client
    try:
        client = Groq()
        print("✅ Groq client initialized")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
    
    # Step 3: Test basic completion
    try:
        print("🔍 Testing basic completion...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Say 'Hello, Groq API is working!' and nothing else."}
            ],
            max_tokens=20,
            temperature=0,
            timeout=10
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Basic completion successful: {result}")
        
    except Exception as e:
        print(f"❌ Basic completion failed: {e}")
        return False
    
    # Step 4: Test food-related query
    try:
        print("🍕 Testing food-related query...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Tell me one interesting fact about pizza in exactly one sentence."}
            ],
            max_tokens=100,
            temperature=0.7,
            timeout=15
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Food query successful:")
        print(f"   {result}")
        
    except Exception as e:
        print(f"❌ Food query failed: {e}")
        return False
    
    # Step 5: Test error handling
    try:
        print("⚠️ Testing error handling with invalid model...")
        response = client.chat.completions.create(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10
        )
    except Exception as e:
        print(f"✅ Error handling works: Caught expected error - {type(e).__name__}")
    
    # Step 6: Performance test
    try:
        print("⚡ Testing response speed...")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "What is the capital of France? One word answer."}
            ],
            max_tokens=5,
            temperature=0
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Performance test: {response_time:.2f}s - Response: {result}")
        
        if response_time < 3:
            print("🚀 Excellent response time!")
        elif response_time < 5:
            print("👍 Good response time")
        else:
            print("⚠️ Slower than expected")
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False
    
    # Step 7: Test rate limiting awareness
    print("🔄 Testing multiple quick requests...")
    success_count = 0
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"Count: {i+1}"}],
                max_tokens=5,
                timeout=5
            )
            success_count += 1
            time.sleep(0.5)  # Small delay between requests
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
    
    print(f"✅ {success_count}/3 rapid requests successful")
    
    print("\n🎉 All Groq API tests completed successfully!")
    print("🚀 Your system is ready for Groq-powered RAG!")
    return True

def test_model_comparison():
    """Test different available models"""
    print("\n🔬 Testing Available Models")
    print("=" * 30)
    
    load_dotenv()
    client = Groq()
    
    models = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]
    
    test_prompt = "What is machine learning? Answer in one sentence."
    
    for model in models:
        try:
            print(f"Testing {model}...")
            start_time = time.time()
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": test_prompt}],
                max_tokens=50,
                temperature=0.7,
                timeout=10
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            result = response.choices[0].message.content.strip()
            print(f"✅ {model}: {response_time:.2f}s")
            print(f"   Response: {result[:100]}...")
            
        except Exception as e:
            print(f"❌ {model}: {e}")
        
        time.sleep(1)  # Delay between model tests

if __name__ == "__main__":
    success = test_groq_setup()
    
    if success:
        test_model = input("\n🤔 Test different models? (y/n): ").lower().strip()
        if test_model == 'y':
            test_model_comparison()
    
    print("\n📝 Next Steps:")
    print("1. If all tests passed, run: python3 rag_run_groq.py")
    print("2. If tests failed, check your GROQ_API_KEY and internet connection")
    print("3. Visit https://console.groq.com/ to check your API usage and credits")