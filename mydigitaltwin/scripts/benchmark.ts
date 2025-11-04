/**
 * Performance Benchmark Test Suite
 * 
 * Automated testing for Food RAG System performance optimizations
 * Tests cache performance, response times, concurrent requests, and generates reports
 * 
 * Usage:
 *   npm run benchmark                    # Run all tests
 *   npm run benchmark -- --verbose       # Verbose output
 *   npm run benchmark -- --iterations 10 # Custom iterations
 */

import * as dotenv from 'dotenv';
import * as path from 'path';

// Load environment variables from .env.local
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });

import { queryFoodRAG, searchByCategory, getFoodRecommendations, clearCache, getCacheStats } from '../src/actions/foodRagActions';

// ============================================================================
// CONFIGURATION
// ============================================================================

interface BenchmarkConfig {
  iterations: number;
  warmupRuns: number;
  verbose: boolean;
  reportFormat: 'console' | 'json' | 'markdown';
}

const DEFAULT_CONFIG: BenchmarkConfig = {
  iterations: 5,
  warmupRuns: 2,
  verbose: false,
  reportFormat: 'console',
};

// Test queries for benchmarking
const TEST_QUERIES = {
  simple: [
    "What is Biryani?",
    "Tell me about Sushi",
    "What are samosas?",
  ],
  complex: [
    "What are some healthy vegetarian Indian dishes?",
    "Tell me about traditional Japanese breakfast foods",
    "What desserts are popular in France?",
  ],
  variations: [
    "What is Biryani?",
    "what is biryani",
    "What's Biryani?",
    "Tell me about Biryani",
  ],
};

// ============================================================================
// PERFORMANCE METRICS
// ============================================================================

interface TestResult {
  testName: string;
  iterations: number;
  avgTime: number;
  minTime: number;
  maxTime: number;
  medianTime: number;
  p95Time: number;
  p99Time: number;
  cacheHitRate?: number;
  success: boolean;
  errors: string[];
}

interface BenchmarkReport {
  timestamp: string;
  config: BenchmarkConfig;
  results: TestResult[];
  summary: {
    totalTests: number;
    passedTests: number;
    failedTests: number;
    avgCacheHitRate: number;
    totalDuration: number;
  };
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Calculate statistics from an array of numbers
 */
function calculateStats(times: number[]) {
  const sorted = [...times].sort((a, b) => a - b);
  const sum = times.reduce((a, b) => a + b, 0);
  
  return {
    avg: sum / times.length,
    min: sorted[0],
    max: sorted[sorted.length - 1],
    median: sorted[Math.floor(sorted.length / 2)],
    p95: sorted[Math.floor(sorted.length * 0.95)],
    p99: sorted[Math.floor(sorted.length * 0.99)],
  };
}

/**
 * Sleep for specified milliseconds
 */
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Format time in human-readable format
 */
function formatTime(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

/**
 * Log with timestamp
 */
function log(message: string, verbose: boolean = false) {
  if (verbose || !DEFAULT_CONFIG.verbose) {
    const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
    console.log(`[${timestamp}] ${message}`);
  }
}

// ============================================================================
// TEST FUNCTIONS
// ============================================================================

/**
 * Test 1: Cache Performance
 * Measures the performance difference between cached and uncached queries
 */
async function testCachePerformance(config: BenchmarkConfig): Promise<TestResult> {
  log('🧪 Test 1: Cache Performance', config.verbose);
  
  const times: { uncached: number[]; cached: number[] } = { uncached: [], cached: [] };
  const errors: string[] = [];
  let cacheHits = 0;
  
  try {
    for (let i = 0; i < config.iterations; i++) {
      // Clear cache before each iteration
      await clearCache();
      await sleep(100);
      
      // Test uncached query
      const query = TEST_QUERIES.simple[i % TEST_QUERIES.simple.length];
      const start1 = Date.now();
      const result1 = await queryFoodRAG(query);
      const uncachedTime = Date.now() - start1;
      
      if (!result1.success) {
        errors.push(`Uncached query failed: ${result1.error}`);
        continue;
      }
      
      times.uncached.push(uncachedTime);
      log(`  Iteration ${i + 1}: Uncached = ${formatTime(uncachedTime)}`, config.verbose);
      
      // Test cached query (same query)
      await sleep(50);
      const start2 = Date.now();
      const result2 = await queryFoodRAG(query);
      const cachedTime = Date.now() - start2;
      
      if (!result2.success) {
        errors.push(`Cached query failed: ${result2.error}`);
        continue;
      }
      
      times.cached.push(cachedTime);
      
      if (result2.metadata?.cached) {
        cacheHits++;
      }
      
      log(`  Iteration ${i + 1}: Cached = ${formatTime(cachedTime)} (${Math.round((1 - cachedTime / uncachedTime) * 100)}% improvement)`, config.verbose);
    }
    
    const uncachedStats = calculateStats(times.uncached);
    const cachedStats = calculateStats(times.cached);
    const improvement = Math.round((1 - cachedStats.avg / uncachedStats.avg) * 100);
    
    log(`✅ Cache Performance: ${improvement}% improvement (${formatTime(uncachedStats.avg)} → ${formatTime(cachedStats.avg)})`, true);
    
    return {
      testName: 'Cache Performance',
      iterations: config.iterations,
      ...cachedStats,
      avgTime: cachedStats.avg,
      minTime: cachedStats.min,
      maxTime: cachedStats.max,
      medianTime: cachedStats.median,
      p95Time: cachedStats.p95,
      p99Time: cachedStats.p99,
      cacheHitRate: (cacheHits / config.iterations) * 100,
      success: errors.length === 0,
      errors,
    };
  } catch (error) {
    return {
      testName: 'Cache Performance',
      iterations: config.iterations,
      avgTime: 0,
      minTime: 0,
      maxTime: 0,
      medianTime: 0,
      p95Time: 0,
      p99Time: 0,
      success: false,
      errors: [error instanceof Error ? error.message : 'Unknown error'],
    };
  }
}

/**
 * Test 2: Query Preprocessing Effectiveness
 * Tests if different query variations hit the same cache
 */
async function testQueryPreprocessing(config: BenchmarkConfig): Promise<TestResult> {
  log('🧪 Test 2: Query Preprocessing Effectiveness', config.verbose);
  
  const times: number[] = [];
  const errors: string[] = [];
  let cacheHits = 0;
  
  try {
    // Clear cache
    await clearCache();
    
    // First query (uncached)
    const firstQuery = TEST_QUERIES.variations[0];
    await queryFoodRAG(firstQuery);
    await sleep(100);
    
    // Test variations (should all be cached)
    for (let i = 0; i < TEST_QUERIES.variations.length; i++) {
      const query = TEST_QUERIES.variations[i];
      const start = Date.now();
      const result = await queryFoodRAG(query);
      const time = Date.now() - start;
      
      if (!result.success) {
        errors.push(`Query failed: ${result.error}`);
        continue;
      }
      
      times.push(time);
      
      if (result.metadata?.cached) {
        cacheHits++;
        log(`  ✓ "${query}" → Cached (${formatTime(time)})`, config.verbose);
      } else {
        log(`  ✗ "${query}" → Uncached (${formatTime(time)})`, config.verbose);
      }
      
      await sleep(50);
    }
    
    const stats = calculateStats(times);
    const hitRate = (cacheHits / TEST_QUERIES.variations.length) * 100;
    
    log(`✅ Preprocessing: ${hitRate}% cache hit rate for variations`, true);
    
    return {
      testName: 'Query Preprocessing',
      iterations: TEST_QUERIES.variations.length,
      ...stats,
      avgTime: stats.avg,
      minTime: stats.min,
      maxTime: stats.max,
      medianTime: stats.median,
      p95Time: stats.p95,
      p99Time: stats.p99,
      cacheHitRate: hitRate,
      success: hitRate >= 75, // At least 75% should be cached
      errors: hitRate < 75 ? ['Cache hit rate below 75%'] : errors,
    };
  } catch (error) {
    return {
      testName: 'Query Preprocessing',
      iterations: TEST_QUERIES.variations.length,
      avgTime: 0,
      minTime: 0,
      maxTime: 0,
      medianTime: 0,
      p95Time: 0,
      p99Time: 0,
      success: false,
      errors: [error instanceof Error ? error.message : 'Unknown error'],
    };
  }
}

/**
 * Test 3: Concurrent Request Deduplication
 * Tests if concurrent identical requests share results
 */
async function testRequestDeduplication(config: BenchmarkConfig): Promise<TestResult> {
  log('🧪 Test 3: Request Deduplication', config.verbose);
  
  const times: number[] = [];
  const errors: string[] = [];
  
  try {
    for (let i = 0; i < config.iterations; i++) {
      // Clear cache
      await clearCache();
      await sleep(100);
      
      // Send 3 concurrent identical requests
      const query = TEST_QUERIES.simple[i % TEST_QUERIES.simple.length];
      const start = Date.now();
      
      const [result1, result2, result3] = await Promise.all([
        queryFoodRAG(query),
        queryFoodRAG(query),
        queryFoodRAG(query),
      ]);
      
      const totalTime = Date.now() - start;
      times.push(totalTime);
      
      const allSuccess = result1.success && result2.success && result3.success;
      
      if (!allSuccess) {
        errors.push(`One or more requests failed in iteration ${i + 1}`);
      }
      
      log(`  Iteration ${i + 1}: 3 concurrent requests completed in ${formatTime(totalTime)}`, config.verbose);
    }
    
    const stats = calculateStats(times);
    
    // Expected: Should be close to single query time (~1700ms), not 3x
    const withinThreshold = stats.avg < 2500; // Should be less than 2.5 seconds
    
    log(`✅ Deduplication: ${formatTime(stats.avg)} for 3 concurrent requests`, true);
    
    return {
      testName: 'Request Deduplication',
      iterations: config.iterations,
      ...stats,
      avgTime: stats.avg,
      minTime: stats.min,
      maxTime: stats.max,
      medianTime: stats.median,
      p95Time: stats.p95,
      p99Time: stats.p99,
      success: withinThreshold && errors.length === 0,
      errors: withinThreshold ? errors : [...errors, 'Deduplication time exceeds threshold'],
    };
  } catch (error) {
    return {
      testName: 'Request Deduplication',
      iterations: config.iterations,
      avgTime: 0,
      minTime: 0,
      maxTime: 0,
      medianTime: 0,
      p95Time: 0,
      p99Time: 0,
      success: false,
      errors: [error instanceof Error ? error.message : 'Unknown error'],
    };
  }
}

/**
 * Test 4: Response Time Consistency
 * Tests if response times are consistent across iterations
 */
async function testResponseConsistency(config: BenchmarkConfig): Promise<TestResult> {
  log('🧪 Test 4: Response Time Consistency', config.verbose);
  
  const times: number[] = [];
  const errors: string[] = [];
  
  try {
    await clearCache();
    
    for (let i = 0; i < config.iterations * 2; i++) {
      const query = TEST_QUERIES.simple[i % TEST_QUERIES.simple.length];
      const start = Date.now();
      const result = await queryFoodRAG(query);
      const time = Date.now() - start;
      
      if (!result.success) {
        errors.push(`Query ${i + 1} failed: ${result.error}`);
        continue;
      }
      
      times.push(time);
      log(`  Query ${i + 1}: ${formatTime(time)}`, config.verbose);
      
      await sleep(50);
    }
    
    const stats = calculateStats(times);
    
    // Calculate coefficient of variation (CV)
    const mean = stats.avg;
    const variance = times.reduce((sum, t) => sum + Math.pow(t - mean, 2), 0) / times.length;
    const stdDev = Math.sqrt(variance);
    const cv = (stdDev / mean) * 100;
    
    // Low CV (<30%) indicates consistent performance
    const isConsistent = cv < 30;
    
    log(`✅ Consistency: CV = ${cv.toFixed(2)}% (${isConsistent ? 'Good' : 'High variance'})`, true);
    
    return {
      testName: 'Response Consistency',
      iterations: times.length,
      ...stats,
      avgTime: stats.avg,
      minTime: stats.min,
      maxTime: stats.max,
      medianTime: stats.median,
      p95Time: stats.p95,
      p99Time: stats.p99,
      success: isConsistent && errors.length === 0,
      errors: isConsistent ? errors : [...errors, `High variance (CV: ${cv.toFixed(2)}%)`],
    };
  } catch (error) {
    return {
      testName: 'Response Consistency',
      iterations: config.iterations,
      avgTime: 0,
      minTime: 0,
      maxTime: 0,
      medianTime: 0,
      p95Time: 0,
      p99Time: 0,
      success: false,
      errors: [error instanceof Error ? error.message : 'Unknown error'],
    };
  }
}

/**
 * Test 5: Category Search Performance
 * Tests searchByCategory function performance
 */
async function testCategorySearch(config: BenchmarkConfig): Promise<TestResult> {
  log('🧪 Test 5: Category Search Performance', config.verbose);
  
  const times: number[] = [];
  const errors: string[] = [];
  
  const categories = ['Dessert', 'Main Course', 'Appetizer', 'Beverage'];
  
  try {
    for (let i = 0; i < config.iterations; i++) {
      const category = categories[i % categories.length];
      const start = Date.now();
      const result = await searchByCategory(category, 10);
      const time = Date.now() - start;
      
      if (!result.success) {
        errors.push(`Category search failed: ${result.error}`);
        continue;
      }
      
      times.push(time);
      log(`  ${category}: ${formatTime(time)} (${result.results?.length || 0} results)`, config.verbose);
      
      await sleep(50);
    }
    
    const stats = calculateStats(times);
    
    log(`✅ Category Search: ${formatTime(stats.avg)} average`, true);
    
    return {
      testName: 'Category Search',
      iterations: config.iterations,
      ...stats,
      avgTime: stats.avg,
      minTime: stats.min,
      maxTime: stats.max,
      medianTime: stats.median,
      p95Time: stats.p95,
      p99Time: stats.p99,
      success: stats.avg < 3000 && errors.length === 0,
      errors,
    };
  } catch (error) {
    return {
      testName: 'Category Search',
      iterations: config.iterations,
      avgTime: 0,
      minTime: 0,
      maxTime: 0,
      medianTime: 0,
      p95Time: 0,
      p99Time: 0,
      success: false,
      errors: [error instanceof Error ? error.message : 'Unknown error'],
    };
  }
}

// ============================================================================
// REPORT GENERATION
// ============================================================================

/**
 * Generate console report
 */
function generateConsoleReport(report: BenchmarkReport) {
  console.log('\n' + '='.repeat(80));
  console.log('📊 PERFORMANCE BENCHMARK REPORT');
  console.log('='.repeat(80));
  console.log(`Timestamp: ${report.timestamp}`);
  console.log(`Iterations: ${report.config.iterations} per test`);
  console.log('='.repeat(80));
  console.log('');
  
  report.results.forEach((result, index) => {
    const status = result.success ? '✅ PASS' : '❌ FAIL';
    console.log(`${index + 1}. ${result.testName} ${status}`);
    console.log(`   Average: ${formatTime(result.avgTime)}`);
    console.log(`   Median:  ${formatTime(result.medianTime)}`);
    console.log(`   Min/Max: ${formatTime(result.minTime)} / ${formatTime(result.maxTime)}`);
    console.log(`   P95/P99: ${formatTime(result.p95Time)} / ${formatTime(result.p99Time)}`);
    
    if (result.cacheHitRate !== undefined) {
      console.log(`   Cache Hit Rate: ${result.cacheHitRate.toFixed(1)}%`);
    }
    
    if (result.errors.length > 0) {
      console.log(`   Errors: ${result.errors.join(', ')}`);
    }
    
    console.log('');
  });
  
  console.log('='.repeat(80));
  console.log('📈 SUMMARY');
  console.log('='.repeat(80));
  console.log(`Total Tests: ${report.summary.totalTests}`);
  console.log(`Passed: ${report.summary.passedTests}`);
  console.log(`Failed: ${report.summary.failedTests}`);
  console.log(`Average Cache Hit Rate: ${report.summary.avgCacheHitRate.toFixed(1)}%`);
  console.log(`Total Duration: ${formatTime(report.summary.totalDuration)}`);
  console.log('='.repeat(80));
  console.log('');
}

/**
 * Generate JSON report
 */
function generateJSONReport(report: BenchmarkReport) {
  console.log(JSON.stringify(report, null, 2));
}

/**
 * Generate Markdown report
 */
function generateMarkdownReport(report: BenchmarkReport) {
  let md = `# Performance Benchmark Report\n\n`;
  md += `**Generated**: ${report.timestamp}\n\n`;
  md += `**Configuration**: ${report.config.iterations} iterations per test\n\n`;
  md += `## Results\n\n`;
  
  md += `| Test | Status | Avg | Median | P95 | P99 | Cache Hit % |\n`;
  md += `|------|--------|-----|--------|-----|-----|-------------|\n`;
  
  report.results.forEach(result => {
    const status = result.success ? '✅' : '❌';
    const cacheHit = result.cacheHitRate !== undefined ? `${result.cacheHitRate.toFixed(1)}%` : 'N/A';
    md += `| ${result.testName} | ${status} | ${formatTime(result.avgTime)} | ${formatTime(result.medianTime)} | ${formatTime(result.p95Time)} | ${formatTime(result.p99Time)} | ${cacheHit} |\n`;
  });
  
  md += `\n## Summary\n\n`;
  md += `- **Total Tests**: ${report.summary.totalTests}\n`;
  md += `- **Passed**: ${report.summary.passedTests}\n`;
  md += `- **Failed**: ${report.summary.failedTests}\n`;
  md += `- **Average Cache Hit Rate**: ${report.summary.avgCacheHitRate.toFixed(1)}%\n`;
  md += `- **Total Duration**: ${formatTime(report.summary.totalDuration)}\n`;
  
  console.log(md);
}

// ============================================================================
// MAIN BENCHMARK RUNNER
// ============================================================================

/**
 * Run all benchmarks
 */
export async function runBenchmarks(config: Partial<BenchmarkConfig> = {}): Promise<BenchmarkReport> {
  const finalConfig: BenchmarkConfig = { ...DEFAULT_CONFIG, ...config };
  
  console.log('🚀 Starting Performance Benchmarks...\n');
  console.log(`Configuration: ${finalConfig.iterations} iterations, ${finalConfig.warmupRuns} warmup runs\n`);
  
  const startTime = Date.now();
  const results: TestResult[] = [];
  
  // Run warmup
  if (finalConfig.warmupRuns > 0) {
    log(`🔥 Running ${finalConfig.warmupRuns} warmup queries...`);
    for (let i = 0; i < finalConfig.warmupRuns; i++) {
      await queryFoodRAG("warmup query");
    }
    log('✅ Warmup complete\n');
  }
  
  // Run tests
  results.push(await testCachePerformance(finalConfig));
  results.push(await testQueryPreprocessing(finalConfig));
  results.push(await testRequestDeduplication(finalConfig));
  results.push(await testResponseConsistency(finalConfig));
  results.push(await testCategorySearch(finalConfig));
  
  const totalDuration = Date.now() - startTime;
  
  // Calculate summary
  const passedTests = results.filter(r => r.success).length;
  const failedTests = results.filter(r => !r.success).length;
  const cacheHitRates = results.filter(r => r.cacheHitRate !== undefined).map(r => r.cacheHitRate!);
  const avgCacheHitRate = cacheHitRates.length > 0 
    ? cacheHitRates.reduce((a, b) => a + b, 0) / cacheHitRates.length 
    : 0;
  
  const report: BenchmarkReport = {
    timestamp: new Date().toISOString(),
    config: finalConfig,
    results,
    summary: {
      totalTests: results.length,
      passedTests,
      failedTests,
      avgCacheHitRate,
      totalDuration,
    },
  };
  
  // Generate report
  switch (finalConfig.reportFormat) {
    case 'json':
      generateJSONReport(report);
      break;
    case 'markdown':
      generateMarkdownReport(report);
      break;
    default:
      generateConsoleReport(report);
  }
  
  return report;
}

// ============================================================================
// CLI INTERFACE
// ============================================================================

if (require.main === module) {
  const args = process.argv.slice(2);
  const config: Partial<BenchmarkConfig> = {};
  
  // Parse command line arguments
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--iterations' && args[i + 1]) {
      config.iterations = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--verbose') {
      config.verbose = true;
    } else if (args[i] === '--format' && args[i + 1]) {
      config.reportFormat = args[i + 1] as 'console' | 'json' | 'markdown';
      i++;
    }
  }
  
  runBenchmarks(config)
    .then((report) => {
      process.exit(report.summary.failedTests > 0 ? 1 : 0);
    })
    .catch((error) => {
      console.error('❌ Benchmark failed:', error);
      process.exit(1);
    });
}
