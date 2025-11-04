#!/usr/bin/env python3
"""
Complete System Testing Script
===============================

Tests the entire RAG system with Upstash Vector + Groq Cloud:
- Database connectivity
- Embedding generation
- Query functionality
- LLM responses
- Performance benchmarking

Usage:
    python3 scripts/test_complete_system.py
"""

import os
import sys
import time
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_header(text, char="="):
    """Print formatted header"""
    print(f"\n{char*70}")
    print(f"  {text}")
    print(f"{char*70}\n")

def print_test(name, status, details=""):
    """Print test result"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {name}")
    if details:
        print(f"   {details}")

class SystemTester:
    """Complete system testing"""
    
    def __init__(self):
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'tests': []
        }
        self.start_time = None
        self.upstash_index = None
        self.groq_client = None
    
    def record_test(self, name, passed, details="", duration=None):
        """Record test result"""
        self.results['total'] += 1
        if passed:
            self.results['passed'] += 1
        else:
            self.results['failed'] += 1
        
        self.results['tests'].append({
            'name': name,
            'passed': passed,
            'details': details,
            'duration': duration
        })
        
        print_test(name, passed, details)
    
    def test_dependencies(self):
        """Test 1: Check all dependencies are installed"""
        print_header("TEST 1: Dependencies Check")
        
        required = {
            'upstash_vector': 'upstash-vector',
            'groq': 'groq',
            'dotenv': 'python-dotenv'
        }
        
        all_installed = True
        for module, package in required.items():
            try:
                __import__(module)
                print_test(f"{package} installed", True)
            except ImportError:
                print_test(f"{package} installed", False, f"Run: pip install {package}")
                all_installed = False
        
        self.record_test("Dependencies Check", all_installed)
        return all_installed
    
    def test_environment_config(self):
        """Test 2: Validate environment configuration"""
        print_header("TEST 2: Environment Configuration")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        checks = {
            'UPSTASH_VECTOR_REST_URL': os.getenv('UPSTASH_VECTOR_REST_URL'),
            'UPSTASH_VECTOR_REST_TOKEN': os.getenv('UPSTASH_VECTOR_REST_TOKEN'),
            'GROQ_API_KEY': os.getenv('GROQ_API_KEY')
        }
        
        all_set = True
        for key, value in checks.items():
            if value:
                print_test(f"{key} configured", True, f"Length: {len(value)}")
            else:
                print_test(f"{key} configured", False, "Missing in .env")
                all_set = False
        
        self.record_test("Environment Configuration", all_set)
        return all_set
    
    def test_upstash_connection(self):
        """Test 3: Test Upstash Vector connectivity"""
        print_header("TEST 3: Upstash Vector Connection")
        
        try:
            from upstash_vector import Index
            from dotenv import load_dotenv
            load_dotenv()
            
            start = time.time()
            self.upstash_index = Index.from_env()
            duration = time.time() - start
            
            print_test("Initialize client", True, f"Took {duration:.2f}s")
            
            # Get index info
            start = time.time()
            info = self.upstash_index.info()
            duration = time.time() - start
            
            details = f"Vectors: {info.vector_count}, Dim: {info.dimension}, Took {duration:.2f}s"
            print_test("Fetch index info", True, details)
            
            self.record_test("Upstash Vector Connection", True, details, duration)
            return True
            
        except Exception as e:
            print_test("Upstash connection", False, str(e))
            self.record_test("Upstash Vector Connection", False, str(e))
            return False
    
    def test_groq_connection(self):
        """Test 4: Test Groq API connectivity"""
        print_header("TEST 4: Groq Cloud Connection")
        
        try:
            from groq import Groq
            from dotenv import load_dotenv
            load_dotenv()
            
            start = time.time()
            self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            duration = time.time() - start
            
            print_test("Initialize client", True, f"Took {duration:.2f}s")
            
            # Test simple API call
            start = time.time()
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": "Say 'OK' if you can hear me."}],
                model="llama-3.1-8b-instant",
                max_tokens=10
            )
            duration = time.time() - start
            
            answer = response.choices[0].message.content.strip()
            print_test("Test API call", True, f"Response: '{answer}', Took {duration:.2f}s")
            
            self.record_test("Groq Cloud Connection", True, f"API working, {duration:.2f}s", duration)
            return True
            
        except Exception as e:
            print_test("Groq connection", False, str(e))
            self.record_test("Groq Cloud Connection", False, str(e))
            return False
    
    def test_embedding_generation(self):
        """Test 5: Test embedding generation (via Upstash)"""
        print_header("TEST 5: Embedding Generation")
        
        if not self.upstash_index:
            self.record_test("Embedding Generation", False, "Upstash not connected")
            return False
        
        try:
            test_text = "Pho is a Vietnamese soup"
            
            start = time.time()
            # Upstash auto-embeds during query
            results = self.upstash_index.query(
                data=test_text,
                top_k=1,
                include_metadata=True
            )
            duration = time.time() - start
            
            if results:
                print_test("Auto-embedding", True, f"Query embedded and searched in {duration:.2f}s")
                self.record_test("Embedding Generation", True, f"Automatic via Upstash, {duration:.2f}s", duration)
                return True
            else:
                print_test("Auto-embedding", False, "No results returned")
                self.record_test("Embedding Generation", False, "Query failed")
                return False
                
        except Exception as e:
            print_test("Embedding generation", False, str(e))
            self.record_test("Embedding Generation", False, str(e))
            return False
    
    def test_query_functionality(self):
        """Test 6: Test vector search functionality"""
        print_header("TEST 6: Query Functionality")
        
        if not self.upstash_index:
            self.record_test("Query Functionality", False, "Upstash not connected")
            return False
        
        test_queries = [
            ("Vietnamese food", "Pho"),
            ("Japanese cuisine", "Sushi"),
            ("healthy breakfast", "Oatmeal")
        ]
        
        all_passed = True
        total_duration = 0
        
        for query, expected_keyword in test_queries:
            try:
                start = time.time()
                results = self.upstash_index.query(
                    data=query,
                    top_k=3,
                    include_metadata=True
                )
                duration = time.time() - start
                total_duration += duration
                
                if results and len(results) > 0:
                    top_result = results[0].metadata.get('original_text', '')
                    found = expected_keyword.lower() in top_result.lower()
                    
                    if found:
                        print_test(f"Query: '{query}'", True, f"Found '{expected_keyword}' in {duration:.2f}s")
                    else:
                        print_test(f"Query: '{query}'", False, f"Expected '{expected_keyword}', got '{top_result[:50]}...'")
                        all_passed = False
                else:
                    print_test(f"Query: '{query}'", False, "No results")
                    all_passed = False
                    
            except Exception as e:
                print_test(f"Query: '{query}'", False, str(e))
                all_passed = False
        
        avg_duration = total_duration / len(test_queries)
        self.record_test("Query Functionality", all_passed, f"Avg {avg_duration:.2f}s per query", avg_duration)
        return all_passed
    
    def test_llm_responses(self):
        """Test 7: Test LLM response generation"""
        print_header("TEST 7: LLM Response Generation")
        
        if not self.groq_client or not self.upstash_index:
            self.record_test("LLM Response Generation", False, "Missing client")
            return False
        
        test_question = "What is Pho?"
        
        try:
            # Get context from vector DB
            start = time.time()
            results = self.upstash_index.query(
                data=test_question,
                top_k=2,
                include_metadata=True
            )
            vector_time = time.time() - start
            
            if not results:
                self.record_test("LLM Response Generation", False, "No context found")
                return False
            
            context = "\n".join([r.metadata['original_text'] for r in results])
            
            # Generate response
            start = time.time()
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a food expert."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {test_question}"}
                ],
                model="llama-3.1-8b-instant",
                max_tokens=150
            )
            llm_time = time.time() - start
            
            answer = response.choices[0].message.content.strip()
            total_time = vector_time + llm_time
            
            # Check if answer is relevant
            relevant = len(answer) > 10 and ("pho" in answer.lower() or "vietnamese" in answer.lower())
            
            if relevant:
                print_test("Generate answer", True, f"Vector: {vector_time:.2f}s, LLM: {llm_time:.2f}s, Total: {total_time:.2f}s")
                print(f"\n   Question: {test_question}")
                print(f"   Answer: {answer[:200]}...\n")
                self.record_test("LLM Response Generation", True, f"Total {total_time:.2f}s", total_time)
                return True
            else:
                print_test("Generate answer", False, "Response not relevant")
                self.record_test("LLM Response Generation", False, "Irrelevant response")
                return False
                
        except Exception as e:
            print_test("LLM response", False, str(e))
            self.record_test("LLM Response Generation", False, str(e))
            return False
    
    def test_performance(self):
        """Test 8: Performance benchmarking"""
        print_header("TEST 8: Performance Benchmarking")
        
        if not self.groq_client or not self.upstash_index:
            self.record_test("Performance Benchmark", False, "Missing client")
            return False
        
        test_queries = [
            "Tell me about Italian pasta",
            "What are healthy breakfast options?",
            "Recommend spicy Asian dishes"
        ]
        
        timings = []
        
        for query in test_queries:
            try:
                start = time.time()
                
                # Vector search
                results = self.upstash_index.query(data=query, top_k=3, include_metadata=True)
                context = "\n".join([r.metadata['original_text'] for r in results]) if results else ""
                
                # LLM generation
                response = self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a food expert."},
                        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
                    ],
                    model="llama-3.1-8b-instant",
                    max_tokens=100
                )
                
                duration = time.time() - start
                timings.append(duration)
                
                print_test(f"Query: '{query[:40]}...'", True, f"{duration:.2f}s")
                
            except Exception as e:
                print_test(f"Query: '{query[:40]}...'", False, str(e))
                return False
        
        avg_time = sum(timings) / len(timings)
        min_time = min(timings)
        max_time = max(timings)
        
        details = f"Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s"
        
        # Performance is good if average < 3 seconds
        passed = avg_time < 3.0
        
        print(f"\n   {details}")
        self.record_test("Performance Benchmark", passed, details, avg_time)
        
        return passed
    
    def run_all_tests(self):
        """Run all tests"""
        print_header("🧪 COMPLETE SYSTEM TESTING", "=")
        print("Testing RAG System: Upstash Vector + Groq Cloud\n")
        
        self.start_time = time.time()
        
        # Run tests in sequence
        tests = [
            self.test_dependencies,
            self.test_environment_config,
            self.test_upstash_connection,
            self.test_groq_connection,
            self.test_embedding_generation,
            self.test_query_functionality,
            self.test_llm_responses,
            self.test_performance
        ]
        
        for test in tests:
            test()
            print()  # Spacing
        
        # Summary
        total_time = time.time() - self.start_time
        self.print_summary(total_time)
    
    def print_summary(self, total_time):
        """Print test summary"""
        print_header("📊 TEST SUMMARY", "=")
        
        print(f"Total Tests: {self.results['total']}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"⏱️  Total Time: {total_time:.2f}s")
        
        success_rate = (self.results['passed'] / self.results['total'] * 100) if self.results['total'] > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.results['failed'] > 0:
            print("\n❌ Failed Tests:")
            for test in self.results['tests']:
                if not test['passed']:
                    print(f"   • {test['name']}: {test['details']}")
        
        print("\n" + "="*70)
        
        if self.results['failed'] == 0:
            print("🎉 All tests passed! System is fully operational.")
        else:
            print("⚠️  Some tests failed. Please check the configuration.")
        
        print("="*70 + "\n")

def main():
    """Main execution"""
    tester = SystemTester()
    tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if tester.results['failed'] == 0 else 1)

if __name__ == "__main__":
    main()
