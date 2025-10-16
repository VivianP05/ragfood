"""
Performance comparison between Ollama and Groq
"""
import time
import json
import requests
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def test_ollama_performance():
    """Test Ollama local performance"""
    print("🔄 Testing Ollama Performance...")
    
    test_prompt = """Use the following context to answer the question.

Context:
Pizza is a flatbread topped with tomato sauce, cheese, and various toppings, baked in an oven.

Question: What is pizza?
Answer:"""
    
    try:
        start_time = time.time()
        
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": test_prompt,
            "stream": False
        }, timeout=30)
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()["response"].strip()
            response_time = end_time - start_time
            
            return {
                "success": True,
                "response_time": response_time,
                "response": result,
                "error": None
            }
        else:
            return {
                "success": False,
                "response_time": None,
                "response": None,
                "error": f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "response_time": None,
            "response": None,
            "error": str(e)
        }

def test_groq_performance():
    """Test Groq cloud performance"""
    print("☁️ Testing Groq Performance...")
    
    test_prompt = """Use the following context to answer the question.

Context:
Pizza is a flatbread topped with tomato sauce, cheese, and various toppings, baked in an oven.

Question: What is pizza?
Answer:"""
    
    try:
        client = Groq()
        start_time = time.time()
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": test_prompt}],
            temperature=0.7,
            max_tokens=200,
            timeout=30
        )
        
        end_time = time.time()
        
        result = completion.choices[0].message.content.strip()
        response_time = end_time - start_time
        
        return {
            "success": True,
            "response_time": response_time,
            "response": result,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "response_time": None,
            "response": None,
            "error": str(e)
        }

def run_performance_comparison():
    """Run comprehensive performance comparison"""
    print("⚡ RAG Performance Comparison: Ollama vs Groq")
    print("=" * 60)
    
    # Test multiple runs for average
    num_runs = 3
    ollama_times = []
    groq_times = []
    
    print(f"Running {num_runs} tests for each service...\n")
    
    # Test Ollama
    print("🔄 Testing Ollama (Local):")
    for i in range(num_runs):
        print(f"  Run {i+1}/{num_runs}...", end=" ")
        result = test_ollama_performance()
        
        if result["success"]:
            ollama_times.append(result["response_time"])
            print(f"✅ {result['response_time']:.2f}s")
        else:
            print(f"❌ {result['error']}")
        
        time.sleep(1)  # Brief pause between tests
    
    print(f"\n☁️ Testing Groq (Cloud):")
    for i in range(num_runs):
        print(f"  Run {i+1}/{num_runs}...", end=" ")
        result = test_groq_performance()
        
        if result["success"]:
            groq_times.append(result["response_time"])
            print(f"✅ {result['response_time']:.2f}s")
        else:
            print(f"❌ {result['error']}")
        
        time.sleep(2)  # Longer pause for API rate limiting
    
    # Calculate and display results
    print("\n📊 Performance Results:")
    print("=" * 30)
    
    if ollama_times:
        avg_ollama = sum(ollama_times) / len(ollama_times)
        min_ollama = min(ollama_times)
        max_ollama = max(ollama_times)
        
        print(f"🔄 Ollama (Local):")
        print(f"   Average: {avg_ollama:.2f}s")
        print(f"   Best:    {min_ollama:.2f}s")
        print(f"   Worst:   {max_ollama:.2f}s")
        print(f"   Success: {len(ollama_times)}/{num_runs} runs")
    else:
        print(f"🔄 Ollama: ❌ All tests failed")
        avg_ollama = None
    
    if groq_times:
        avg_groq = sum(groq_times) / len(groq_times)
        min_groq = min(groq_times)
        max_groq = max(groq_times)
        
        print(f"\n☁️ Groq (Cloud):")
        print(f"   Average: {avg_groq:.2f}s")
        print(f"   Best:    {min_groq:.2f}s")
        print(f"   Worst:   {max_groq:.2f}s")
        print(f"   Success: {len(groq_times)}/{num_runs} runs")
    else:
        print(f"☁️ Groq: ❌ All tests failed")
        avg_groq = None
    
    # Comparison
    print(f"\n🏆 Comparison:")
    print("=" * 20)
    
    if avg_ollama and avg_groq:
        if avg_groq < avg_ollama:
            improvement = ((avg_ollama - avg_groq) / avg_ollama) * 100
            print(f"🚀 Groq is {improvement:.1f}% faster than Ollama!")
            print(f"   Groq: {avg_groq:.2f}s vs Ollama: {avg_ollama:.2f}s")
        elif avg_ollama < avg_groq:
            improvement = ((avg_groq - avg_ollama) / avg_groq) * 100
            print(f"🏠 Ollama is {improvement:.1f}% faster than Groq!")
            print(f"   Ollama: {avg_ollama:.2f}s vs Groq: {avg_groq:.2f}s")
        else:
            print("🤝 Performance is roughly equivalent")
    elif avg_groq:
        print("✅ Only Groq is available and working")
    elif avg_ollama:
        print("✅ Only Ollama is available and working")
    else:
        print("❌ Neither service is working properly")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    print("=" * 20)
    
    if avg_groq and avg_groq < 3:
        print("🚀 Groq provides excellent response times!")
        print("   Recommended for production use")
    elif avg_ollama and avg_ollama < 5:
        print("🏠 Ollama provides good local performance")
        print("   Good for offline/private deployments")
    
    if avg_groq and avg_ollama:
        print(f"\n🔄 Trade-offs:")
        print(f"   Groq:   Faster, cloud-based, requires internet & API credits")
        print(f"   Ollama: Local, private, no API costs, requires local compute")

def test_quality_comparison():
    """Compare response quality between Ollama and Groq"""
    print("\n🎯 Response Quality Comparison")
    print("=" * 35)
    
    test_question = "What are the health benefits of eating vegetables?"
    context = "Vegetables are rich in vitamins, minerals, fiber, and antioxidants. They help reduce the risk of chronic diseases, support digestive health, and provide essential nutrients for overall wellness."
    
    prompt = f"""Use the following context to answer the question comprehensively.

Context:
{context}

Question: {test_question}
Answer:"""
    
    print(f"Test Question: {test_question}\n")
    
    # Test Ollama
    print("🔄 Ollama Response:")
    print("-" * 20)
    ollama_result = test_ollama_performance()
    if ollama_result["success"]:
        print(ollama_result["response"])
        print(f"\n⏱️ Time: {ollama_result['response_time']:.2f}s")
    else:
        print(f"❌ Failed: {ollama_result['error']}")
    
    print(f"\n☁️ Groq Response:")
    print("-" * 20)
    groq_result = test_groq_performance()
    if groq_result["success"]:
        print(groq_result["response"])
        print(f"\n⏱️ Time: {groq_result['response_time']:.2f}s")
    else:
        print(f"❌ Failed: {groq_result['error']}")
    
    print(f"\n📝 Quality Assessment:")
    print("Compare the responses above for:")
    print("- Accuracy and relevance")
    print("- Completeness and detail")
    print("- Clarity and readability")
    print("- Use of provided context")

if __name__ == "__main__":
    print("🧪 RAG Performance Testing Suite")
    print("=" * 40)
    
    # Check environment
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️ GROQ_API_KEY not found. Groq tests will fail.")
    
    run_performance_comparison()
    
    # Optional quality test
    quality_test = input("\n🤔 Run response quality comparison? (y/n): ").lower().strip()
    if quality_test == 'y':
        test_quality_comparison()
    
    print("\n✅ Performance testing complete!")
    print("Use these results to choose the best LLM for your needs.")