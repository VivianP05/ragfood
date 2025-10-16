"""
Test Groq streaming functionality
"""
import os
from dotenv import load_dotenv
from groq import Groq
import time

def test_groq_streaming():
    """Test Groq streaming responses"""
    print("🌊 Groq Streaming Test")
    print("=" * 30)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    if not os.getenv('GROQ_API_KEY'):
        print("❌ GROQ_API_KEY not found in .env file")
        return False
    
    try:
        # Initialize client
        client = Groq()
        print("✅ Groq client initialized")
        
        # Test streaming response
        print("\n🧪 Testing streaming response...")
        print("Question: Tell me about pizza in 3 sentences")
        print("🤖 Groq AI: ", end="", flush=True)
        
        start_time = time.time()
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": "Tell me about pizza in exactly 3 sentences. Make it interesting!"
                }
            ],
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            stream=True,
            stop=None
        )
        
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
                time.sleep(0.02)  # Small delay to see streaming effect
        
        end_time = time.time()
        
        print(f"\n\n⏱️ Total time: {end_time - start_time:.2f} seconds")
        print(f"📝 Full response length: {len(full_response)} characters")
        print("✅ Streaming test successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
        return False

def compare_streaming_vs_non_streaming():
    """Compare streaming vs non-streaming performance"""
    print("\n⚡ Streaming vs Non-Streaming Comparison")
    print("=" * 45)
    
    client = Groq()
    test_prompt = "Explain the health benefits of eating vegetables in 4 sentences."
    
    # Test non-streaming
    print("🔄 Testing non-streaming...")
    start_time = time.time()
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": test_prompt}],
        temperature=0.7,
        max_tokens=200,
        stream=False
    )
    
    end_time = time.time()
    non_streaming_response = completion.choices[0].message.content
    non_streaming_time = end_time - start_time
    
    print(f"✅ Non-streaming completed in {non_streaming_time:.2f}s")
    print(f"Response: {non_streaming_response[:100]}...")
    
    time.sleep(1)  # Brief pause
    
    # Test streaming
    print(f"\n🌊 Testing streaming...")
    print("🤖 Response: ", end="", flush=True)
    
    start_time = time.time()
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": test_prompt}],
        temperature=0.7,
        max_tokens=200,
        stream=True
    )
    
    streaming_response = ""
    first_chunk_time = None
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            if first_chunk_time is None:
                first_chunk_time = time.time()
            
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            streaming_response += content
    
    end_time = time.time()
    streaming_time = end_time - start_time
    time_to_first_token = first_chunk_time - start_time if first_chunk_time else 0
    
    print(f"\n\n📊 Comparison Results:")
    print(f"Non-streaming total time: {non_streaming_time:.2f}s")
    print(f"Streaming total time: {streaming_time:.2f}s")
    print(f"Time to first token: {time_to_first_token:.2f}s")
    
    print(f"\n💡 Benefits:")
    print(f"- Streaming feels more interactive")
    print(f"- Users see response immediately (first token in {time_to_first_token:.2f}s)")
    print(f"- Better user experience for longer responses")
    print(f"- Can stop generation early if needed")

def demo_interactive_streaming():
    """Demo interactive streaming with user input"""
    print("\n🎮 Interactive Streaming Demo")
    print("=" * 35)
    
    client = Groq()
    
    while True:
        question = input("\n💭 Ask about food (or 'exit' to quit): ").strip()
        
        if question.lower() in ['exit', 'quit', 'q']:
            break
            
        if not question:
            continue
            
        print(f"🤖 Groq AI: ", end="", flush=True)
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": f"Answer this food question concisely and engagingly: {question}"
                    }
                ],
                temperature=0.8,
                max_tokens=300,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
            
            print()  # New line after response
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("🌊 Groq Streaming Functionality Test Suite")
    print("=" * 50)
    
    # Basic streaming test
    success = test_groq_streaming()
    
    if success:
        # Performance comparison
        compare_choice = input("\n🤔 Run streaming vs non-streaming comparison? (y/n): ").lower()
        if compare_choice == 'y':
            compare_streaming_vs_non_streaming()
        
        # Interactive demo
        demo_choice = input("\n🎮 Try interactive streaming demo? (y/n): ").lower()
        if demo_choice == 'y':
            demo_interactive_streaming()
    
    print("\n✅ Streaming tests complete!")
    print("🚀 Ready to use rag_run_groq_streaming.py with streaming support!")