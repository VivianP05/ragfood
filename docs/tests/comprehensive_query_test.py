#!/usr/bin/env python3
"""
Comprehensive RAG System Testing Suite
=====================================

This script performs extensive testing of the RAG-Food system with:
- 15+ diverse test queries across multiple categories
- Performance comparison between implementations
- Quality assessment and relevance scoring
- Detailed documentation and analysis

Test Categories:
1. Semantic Similarity Tests
2. Multi-Criteria Searches
3. Nutritional Queries
4. Cultural Exploration
5. Cooking Method Queries
6. Dietary Restriction Queries
7. Regional Cuisine Queries
"""

import time
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import statistics

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import RAG implementations
implementations = {}

try:
    from rag_run import query_rag as query_rag_chromadb
    implementations['ChromaDB + Ollama'] = query_rag_chromadb
    print("✅ ChromaDB + Ollama implementation loaded")
except ImportError as e:
    print(f"⚠️  ChromaDB + Ollama implementation not available: {e}")

try:
    from rag_run_upstash import query_rag as query_rag_upstash
    implementations['Upstash Vector'] = query_rag_upstash
    print("✅ Upstash Vector implementation loaded")
except ImportError as e:
    print(f"⚠️  Upstash Vector implementation not available: {e}")

try:
    from rag_run_groq import query_rag as query_rag_groq
    implementations['Groq API'] = query_rag_groq
    print("✅ Groq API implementation loaded")
except ImportError as e:
    print(f"⚠️  Groq API implementation not available: {e}")

try:
    from rag_run_groq_streaming import query_rag as query_rag_groq_streaming
    implementations['Groq Streaming'] = query_rag_groq_streaming
    print("✅ Groq Streaming implementation loaded")
except ImportError as e:
    print(f"⚠️  Groq Streaming implementation not available: {e}")

# Comprehensive Test Query Suite
TEST_QUERIES = [
    # 1. Semantic Similarity Tests
    {
        "category": "Semantic Similarity",
        "query": "healthy Mediterranean options",
        "expected_keywords": ["olive oil", "vegetables", "Mediterranean", "healthy", "fiber"],
        "expected_regions": ["Greece", "Mediterranean", "Italy"],
        "difficulty": "Easy"
    },
    {
        "category": "Semantic Similarity", 
        "query": "light refreshing summer meals",
        "expected_keywords": ["fresh", "light", "vegetables", "salad", "cool"],
        "expected_regions": ["Global", "Mediterranean"],
        "difficulty": "Medium"
    },
    {
        "category": "Semantic Similarity",
        "query": "comfort food for cold weather",
        "expected_keywords": ["warm", "soup", "hearty", "comfort", "hot"],
        "expected_regions": ["Various", "Global"],
        "difficulty": "Medium"
    },
    
    # 2. Multi-Criteria Searches
    {
        "category": "Multi-Criteria",
        "query": "spicy vegetarian Asian dishes", 
        "expected_keywords": ["spicy", "vegetarian", "Asian", "chili", "vegetables"],
        "expected_regions": ["Asia", "Korea", "Thailand", "India"],
        "difficulty": "Hard"
    },
    {
        "category": "Multi-Criteria",
        "query": "gluten-free vegan breakfast options",
        "expected_keywords": ["gluten-free", "vegan", "breakfast", "plant-based"],
        "expected_regions": ["Global"],
        "difficulty": "Hard"
    },
    {
        "category": "Multi-Criteria", 
        "query": "low-calorie high-fiber dinner foods",
        "expected_keywords": ["low-calorie", "fiber", "dinner", "vegetables", "healthy"],
        "expected_regions": ["Global"],
        "difficulty": "Hard"
    },
    
    # 3. Nutritional Queries
    {
        "category": "Nutritional",
        "query": "high-protein low-carb foods",
        "expected_keywords": ["protein", "low-carb", "meat", "fish", "eggs"],
        "expected_regions": ["Global"],
        "difficulty": "Medium"
    },
    {
        "category": "Nutritional",
        "query": "foods rich in omega-3 fatty acids",
        "expected_keywords": ["omega-3", "fish", "salmon", "healthy fats"],
        "expected_regions": ["Global", "Western"],
        "difficulty": "Medium"
    },
    {
        "category": "Nutritional",
        "query": "calcium-rich dairy-free options",
        "expected_keywords": ["calcium", "dairy-free", "plant-based", "vegetables"],
        "expected_regions": ["Global"],
        "difficulty": "Hard"
    },
    
    # 4. Cultural Exploration  
    {
        "category": "Cultural",
        "query": "traditional comfort foods from different cultures",
        "expected_keywords": ["traditional", "comfort", "cultural", "family"],
        "expected_regions": ["Various", "Global"],
        "difficulty": "Medium"
    },
    {
        "category": "Cultural",
        "query": "festive holiday dishes and celebrations",
        "expected_keywords": ["festive", "holiday", "celebration", "traditional"],
        "expected_regions": ["Various", "Global"],
        "difficulty": "Medium"
    },
    {
        "category": "Cultural",
        "query": "street food popular in Asian countries",
        "expected_keywords": ["street food", "Asian", "popular", "noodles"],
        "expected_regions": ["Asia", "Thailand", "Vietnam", "Japan"],
        "difficulty": "Medium"
    },
    
    # 5. Cooking Method Queries
    {
        "category": "Cooking Method",
        "query": "dishes that can be grilled or barbecued",
        "expected_keywords": ["grilled", "barbecue", "meat", "vegetables"],
        "expected_regions": ["Global"],
        "difficulty": "Easy"
    },
    {
        "category": "Cooking Method", 
        "query": "slow-cooked hearty stews and soups",
        "expected_keywords": ["slow-cooked", "stew", "soup", "hearty", "simmered"],
        "expected_regions": ["Global"],
        "difficulty": "Easy"
    },
    {
        "category": "Cooking Method",
        "query": "quick stir-fry meals under 30 minutes",
        "expected_keywords": ["stir-fry", "quick", "fast", "noodles", "vegetables"],
        "expected_regions": ["Asia", "China", "Thailand"],
        "difficulty": "Medium"
    },
    
    # 6. Dietary Restriction Queries
    {
        "category": "Dietary Restrictions",
        "query": "meals safe for people with nut allergies",
        "expected_keywords": ["safe", "allergy", "nut-free", "allergen"],
        "expected_regions": ["Global"],
        "difficulty": "Hard"
    },
    {
        "category": "Dietary Restrictions",
        "query": "pescatarian-friendly protein sources",
        "expected_keywords": ["pescatarian", "fish", "seafood", "protein"],
        "expected_regions": ["Global"],
        "difficulty": "Medium"
    },
    
    # 7. Regional Cuisine Queries
    {
        "category": "Regional Cuisine",
        "query": "authentic Italian pasta and rice dishes",
        "expected_keywords": ["Italian", "pasta", "rice", "authentic"],
        "expected_regions": ["Italy"],
        "difficulty": "Easy"
    },
    {
        "category": "Regional Cuisine",
        "query": "traditional Middle Eastern spiced foods",
        "expected_keywords": ["Middle Eastern", "spiced", "traditional", "herbs"],
        "expected_regions": ["Middle East"],
        "difficulty": "Medium"
    }
]

class QueryTester:
    """Comprehensive query testing and analysis system"""
    
    def __init__(self):
        self.results = []
        self.performance_metrics = {}
        self.quality_scores = {}
        
    def calculate_relevance_score(self, query_data: Dict, response: str) -> float:
        """Calculate relevance score based on expected keywords and content quality"""
        if not response or response.startswith("❌"):
            return 0.0
            
        response_lower = response.lower()
        
        # Keyword matching (40% of score)
        expected_keywords = query_data.get('expected_keywords', [])
        keyword_matches = sum(1 for keyword in expected_keywords 
                            if keyword.lower() in response_lower)
        keyword_score = (keyword_matches / len(expected_keywords)) * 0.4 if expected_keywords else 0.2
        
        # Region/culture relevance (30% of score)
        expected_regions = query_data.get('expected_regions', [])
        region_matches = sum(1 for region in expected_regions 
                           if region.lower() in response_lower)
        region_score = (region_matches / len(expected_regions)) * 0.3 if expected_regions else 0.15
        
        # Response quality indicators (30% of score)
        quality_indicators = [
            'nutritional', 'cultural', 'traditional', 'flavor', 'ingredient',
            'cooking', 'preparation', 'served', 'popular', 'dish'
        ]
        quality_matches = sum(1 for indicator in quality_indicators 
                            if indicator in response_lower)
        quality_score = min(quality_matches / 10, 1.0) * 0.3
        
        total_score = keyword_score + region_score + quality_score
        return min(total_score, 1.0)  # Cap at 1.0
    
    def test_implementation(self, name: str, query_func, queries: List[Dict]) -> List[Dict]:
        """Test a specific RAG implementation with all queries"""
        print(f"\n🧪 Testing {name}")
        print("=" * 60)
        
        implementation_results = []
        response_times = []
        
        for i, query_data in enumerate(queries, 1):
            query = query_data['query']
            category = query_data['category']
            
            try:
                print(f"\n[{i:2d}] {category}: {query}")
                
                start_time = time.time()
                response = query_func(query)
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                # Handle streaming responses
                if hasattr(response, '__iter__') and not isinstance(response, str):
                    full_response = ""
                    for chunk in response:
                        full_response += str(chunk)
                    response = full_response
                
                # Calculate relevance score
                relevance_score = self.calculate_relevance_score(query_data, str(response))
                
                # Truncate response for logging
                response_preview = str(response)[:200] + "..." if len(str(response)) > 200 else str(response)
                
                print(f"     ⏱️  Response time: {response_time:.2f}s")
                print(f"     📊 Relevance score: {relevance_score:.2f}")
                print(f"     💬 Response: {response_preview}")
                
                result = {
                    "implementation": name,
                    "query": query,
                    "category": category,
                    "difficulty": query_data.get('difficulty', 'Medium'),
                    "response": str(response),
                    "response_time": response_time,
                    "relevance_score": relevance_score,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                print(f"     ❌ Error: {e}")
                result = {
                    "implementation": name,
                    "query": query,
                    "category": category,
                    "difficulty": query_data.get('difficulty', 'Medium'),
                    "error": str(e),
                    "response_time": 0,
                    "relevance_score": 0,
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                }
                
            implementation_results.append(result)
        
        # Calculate performance metrics
        if response_times:
            self.performance_metrics[name] = {
                "avg_response_time": statistics.mean(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "median_response_time": statistics.median(response_times),
                "total_queries": len(queries),
                "successful_queries": sum(1 for r in implementation_results if r['success']),
                "avg_relevance_score": statistics.mean([r['relevance_score'] for r in implementation_results])
            }
        
        return implementation_results
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive testing on all available implementations"""
        print("🚀 RAG-Food Comprehensive Testing Suite")
        print("=" * 80)
        print(f"📊 Testing {len(TEST_QUERIES)} queries across {len(implementations)} implementations")
        print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_results = []
        
        # Test each implementation
        for name, query_func in implementations.items():
            try:
                results = self.test_implementation(name, query_func, TEST_QUERIES)
                all_results.extend(results)
            except Exception as e:
                print(f"\n❌ Failed to test {name}: {e}")
        
        # Generate summary
        summary = self.generate_summary(all_results)
        
        return {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_queries": len(TEST_QUERIES),
                "implementations_tested": list(implementations.keys()),
                "test_categories": list(set(q['category'] for q in TEST_QUERIES))
            },
            "results": all_results,
            "performance_metrics": self.performance_metrics,
            "summary": summary
        }
    
    def generate_summary(self, all_results: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive test summary and analysis"""
        
        summary = {
            "overall_statistics": {},
            "implementation_rankings": {},
            "category_analysis": {},
            "quality_assessment": {},
            "recommendations": []
        }
        
        # Overall statistics
        total_tests = len(all_results)
        successful_tests = sum(1 for r in all_results if r['success'])
        
        summary["overall_statistics"] = {
            "total_tests_run": total_tests,
            "successful_tests": successful_tests,
            "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            "implementations_tested": len(implementations)
        }
        
        # Implementation rankings
        impl_scores = {}
        for impl_name in implementations.keys():
            impl_results = [r for r in all_results if r['implementation'] == impl_name and r['success']]
            if impl_results:
                avg_time = statistics.mean([r['response_time'] for r in impl_results])
                avg_relevance = statistics.mean([r['relevance_score'] for r in impl_results])
                success_rate = len(impl_results) / len([r for r in all_results if r['implementation'] == impl_name])
                
                # Combined score: relevance (50%) + speed (30%) + reliability (20%)
                speed_score = max(0, 1 - (avg_time - 0.5) / 10)  # Faster = better
                combined_score = (avg_relevance * 0.5) + (speed_score * 0.3) + (success_rate * 0.2)
                
                impl_scores[impl_name] = {
                    "avg_response_time": avg_time,
                    "avg_relevance_score": avg_relevance,
                    "success_rate": success_rate,
                    "combined_score": combined_score
                }
        
        # Rank by combined score
        ranked_implementations = sorted(impl_scores.items(), 
                                      key=lambda x: x[1]['combined_score'], 
                                      reverse=True)
        summary["implementation_rankings"] = dict(ranked_implementations)
        
        # Category analysis
        categories = set(q['category'] for q in TEST_QUERIES)
        category_performance = {}
        
        for category in categories:
            category_results = [r for r in all_results if r['category'] == category and r['success']]
            if category_results:
                category_performance[category] = {
                    "avg_relevance_score": statistics.mean([r['relevance_score'] for r in category_results]),
                    "avg_response_time": statistics.mean([r['response_time'] for r in category_results]),
                    "success_rate": len(category_results) / len([r for r in all_results if r['category'] == category])
                }
        
        summary["category_analysis"] = category_performance
        
        # Quality assessment
        if successful_tests > 0:
            all_relevance_scores = [r['relevance_score'] for r in all_results if r['success']]
            summary["quality_assessment"] = {
                "avg_relevance_score": statistics.mean(all_relevance_scores),
                "min_relevance_score": min(all_relevance_scores),
                "max_relevance_score": max(all_relevance_scores),
                "high_quality_responses": sum(1 for score in all_relevance_scores if score >= 0.7),
                "poor_quality_responses": sum(1 for score in all_relevance_scores if score < 0.4)
            }
        
        # Recommendations
        recommendations = []
        
        if ranked_implementations:
            best_impl = ranked_implementations[0]
            recommendations.append(f"🏆 Best Overall: {best_impl[0]} (Score: {best_impl[1]['combined_score']:.2f})")
        
        if 'Groq Streaming' in impl_scores:
            groq_metrics = impl_scores['Groq Streaming']
            if groq_metrics['avg_response_time'] < 2.0:
                recommendations.append("⚡ Groq Streaming recommended for real-time applications")
        
        if any(score['success_rate'] < 0.8 for score in impl_scores.values()):
            recommendations.append("⚠️  Some implementations have reliability issues - check configurations")
        
        avg_relevance = statistics.mean([r['relevance_score'] for r in all_results if r['success']])
        if avg_relevance > 0.7:
            recommendations.append("✅ Overall response quality is excellent")
        elif avg_relevance < 0.5:
            recommendations.append("⚠️  Response quality needs improvement - consider fine-tuning")
        
        summary["recommendations"] = recommendations
        
        return summary
    
    def print_detailed_report(self, test_data: Dict[str, Any]):
        """Print a detailed test report to console"""
        
        print(f"\n" + "="*80)
        print("📋 COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        # Test metadata
        metadata = test_data["test_metadata"]
        print(f"🕐 Test completed: {metadata['timestamp']}")
        print(f"📊 Total queries: {metadata['total_queries']}")
        print(f"🔧 Implementations: {', '.join(metadata['implementations_tested'])}")
        print(f"📁 Categories: {', '.join(metadata['test_categories'])}")
        
        # Overall statistics
        stats = test_data["summary"]["overall_statistics"]
        print(f"\n📈 OVERALL STATISTICS")
        print(f"   Total tests: {stats['total_tests_run']}")
        print(f"   Successful: {stats['successful_tests']} ({stats['success_rate']:.1f}%)")
        print(f"   Implementations: {stats['implementations_tested']}")
        
        # Performance metrics
        print(f"\n⚡ PERFORMANCE METRICS")
        for impl, metrics in test_data["performance_metrics"].items():
            print(f"   {impl}:")
            print(f"      Avg response time: {metrics['avg_response_time']:.2f}s")
            print(f"      Success rate: {metrics['successful_queries']}/{metrics['total_queries']}")
            print(f"      Avg relevance: {metrics['avg_relevance_score']:.2f}")
        
        # Implementation rankings
        print(f"\n🏆 IMPLEMENTATION RANKINGS")
        rankings = test_data["summary"]["implementation_rankings"]
        for i, (impl, scores) in enumerate(rankings.items(), 1):
            medal = ["🥇", "🥈", "🥉", "🏅"][min(i-1, 3)]
            print(f"   {medal} {i}. {impl}")
            print(f"      Combined Score: {scores['combined_score']:.3f}")
            print(f"      Relevance: {scores['avg_relevance_score']:.3f}")
            print(f"      Speed: {scores['avg_response_time']:.2f}s")
            print(f"      Reliability: {scores['success_rate']:.1%}")
        
        # Category analysis
        print(f"\n📊 CATEGORY ANALYSIS")
        category_analysis = test_data["summary"]["category_analysis"]
        for category, metrics in category_analysis.items():
            print(f"   {category}:")
            print(f"      Avg relevance: {metrics['avg_relevance_score']:.3f}")
            print(f"      Avg time: {metrics['avg_response_time']:.2f}s")
            print(f"      Success rate: {metrics['success_rate']:.1%}")
        
        # Quality assessment
        quality = test_data["summary"]["quality_assessment"]
        if quality:
            print(f"\n🎯 QUALITY ASSESSMENT")
            print(f"   Average relevance score: {quality['avg_relevance_score']:.3f}")
            print(f"   High quality responses (≥0.7): {quality['high_quality_responses']}")
            print(f"   Poor quality responses (<0.4): {quality['poor_quality_responses']}")
        
        # Recommendations
        recommendations = test_data["summary"]["recommendations"]
        if recommendations:
            print(f"\n💡 RECOMMENDATIONS")
            for rec in recommendations:
                print(f"   {rec}")
        
        print("="*80)

def main():
    """Main execution function"""
    
    if len(implementations) == 0:
        print("❌ No RAG implementations available. Please check your setup.")
        return
    
    # Initialize tester
    tester = QueryTester()
    
    # Run comprehensive tests
    test_data = tester.run_comprehensive_test()
    
    # Print detailed report
    tester.print_detailed_report(test_data)
    
    # Save results to file
    output_file = "../docs/comprehensive_test_results.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    # Create markdown report
    markdown_file = "../docs/test_results_report.md" 
    create_markdown_report(test_data, markdown_file)
    print(f"📄 Markdown report saved to: {markdown_file}")

def create_markdown_report(test_data: Dict[str, Any], filename: str):
    """Create a formatted markdown report"""
    
    metadata = test_data["test_metadata"]
    stats = test_data["summary"]["overall_statistics"]
    rankings = test_data["summary"]["implementation_rankings"]
    
    markdown_content = f"""# RAG-Food System - Comprehensive Test Report

**Generated:** {metadata['timestamp']}  
**Total Queries:** {metadata['total_queries']}  
**Implementations Tested:** {len(metadata['implementations_tested'])}

## 📊 Executive Summary

- **Total Tests Run:** {stats['total_tests_run']}
- **Success Rate:** {stats['success_rate']:.1f}%
- **Categories Tested:** {len(metadata['test_categories'])}

## 🏆 Implementation Rankings

"""
    
    for i, (impl, scores) in enumerate(rankings.items(), 1):
        medal = ["🥇", "🥈", "🥉", "🏅"][min(i-1, 3)]
        markdown_content += f"""
### {medal} {i}. {impl}

- **Combined Score:** {scores['combined_score']:.3f}/1.000
- **Average Relevance:** {scores['avg_relevance_score']:.3f}
- **Average Response Time:** {scores['avg_response_time']:.2f}s
- **Success Rate:** {scores['success_rate']:.1%}
"""

    # Performance comparison table
    markdown_content += f"""
## ⚡ Performance Comparison

| Implementation | Avg Time (s) | Relevance Score | Success Rate | Combined Score |
|---------------|--------------|-----------------|--------------|----------------|
"""
    
    for impl, scores in rankings.items():
        markdown_content += f"| {impl} | {scores['avg_response_time']:.2f} | {scores['avg_relevance_score']:.3f} | {scores['success_rate']:.1%} | {scores['combined_score']:.3f} |\n"
    
    # Category analysis
    category_analysis = test_data["summary"]["category_analysis"]
    markdown_content += f"""
## 📈 Category Analysis

| Category | Avg Relevance | Avg Time (s) | Success Rate |
|----------|---------------|--------------|--------------|
"""
    
    for category, metrics in category_analysis.items():
        markdown_content += f"| {category} | {metrics['avg_relevance_score']:.3f} | {metrics['avg_response_time']:.2f} | {metrics['success_rate']:.1%} |\n"
    
    # Quality assessment
    quality = test_data["summary"]["quality_assessment"]
    if quality:
        markdown_content += f"""
## 🎯 Quality Assessment

- **Average Relevance Score:** {quality['avg_relevance_score']:.3f}
- **High Quality Responses (≥0.7):** {quality['high_quality_responses']}
- **Poor Quality Responses (<0.4):** {quality['poor_quality_responses']}
- **Quality Range:** {quality['min_relevance_score']:.3f} - {quality['max_relevance_score']:.3f}
"""

    # Recommendations
    recommendations = test_data["summary"]["recommendations"]
    if recommendations:
        markdown_content += f"""
## 💡 Recommendations

"""
        for rec in recommendations:
            markdown_content += f"- {rec}\n"
    
    # Test queries reference
    markdown_content += f"""
## 📋 Test Queries Reference

The following {len(TEST_QUERIES)} queries were used across {len(set(q['category'] for q in TEST_QUERIES))} categories:

"""
    
    current_category = None
    for i, query_data in enumerate(TEST_QUERIES, 1):
        if query_data['category'] != current_category:
            current_category = query_data['category']
            markdown_content += f"\n### {current_category}\n\n"
        
        markdown_content += f"{i}. \"{query_data['query']}\" ({query_data['difficulty']})\n"
    
    markdown_content += f"""
## 📝 Notes

- **Relevance Score:** Calculated based on keyword matching, regional relevance, and response quality indicators
- **Combined Score:** Weighted average of relevance (50%), speed (30%), and reliability (20%)
- **Success Rate:** Percentage of queries that completed without errors
- **Response Time:** End-to-end query processing time including LLM generation

---

*Report generated by RAG-Food Comprehensive Testing Suite*
"""

    # Write markdown file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == "__main__":
    main()