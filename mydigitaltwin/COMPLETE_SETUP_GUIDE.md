# 📘 Complete Setup Guide - Food RAG System

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Development Setup](#development-setup)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Python**: 3.9+ (for data upload scripts)
- **Git**: For version control

### Required Accounts

- **Upstash Account**: For Vector Database
  - Sign up at: https://upstash.com
  - Free tier available (10K vectors)
  
- **Groq Account**: For AI Generation
  - Sign up at: https://console.groq.com
  - Free tier available

- **GitHub Account**: For repository access
  - Repository: https://github.com/VivianP05/ragfood

---

## Installation

### 1. Clone Repository

```bash
# Clone the repository
git clone https://github.com/VivianP05/ragfood.git

# Navigate to project directory
cd ragfood

# Navigate to Next.js app
cd mydigitaltwin
```

### 2. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Verify installation
npm list --depth=0
```

**Expected Dependencies**:
```
@upstash/vector@^1.x
groq-sdk@^0.x
next@16.0.1
react@19.2.0
typescript@^5.x
tailwindcss@^3.x
```

### 3. Install Python Dependencies (Optional)

For database management scripts:

```bash
# Navigate back to root
cd ..

# Install Python packages
pip install python-dotenv upstash-vector groq
```

---

## Environment Configuration

### 1. Create Environment Files

Create `.env.local` in `mydigitaltwin/` directory:

```bash
cd mydigitaltwin
touch .env.local
```

### 2. Get Upstash Credentials

1. Go to https://console.upstash.com/vector
2. Select your vector database (or create new one)
3. Click "Connect" tab
4. Copy REST URL and REST Token

### 3. Get Groq API Key

1. Go to https://console.groq.com/keys
2. Click "Create API Key"
3. Copy the generated key
4. **Important**: Save it immediately (shown only once)

### 4. Configure Environment Variables

Edit `mydigitaltwin/.env.local`:

```bash
# Upstash Vector Database
UPSTASH_VECTOR_REST_URL="https://your-database.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="your-upstash-token"

# Groq AI
GROQ_API_KEY="your-groq-api-key"
```

**Security Notes**:
- ✅ Never commit `.env.local` to git (already in `.gitignore`)
- ✅ Use different credentials for development/production
- ✅ Rotate API keys periodically
- ✅ Don't share credentials in screenshots or logs

### 5. Verify Environment Setup

Create `scripts/verify-env.ts`:

```typescript
import { Index } from "@upstash/vector";

async function verifyEnv() {
  console.log("🔍 Verifying environment configuration...\n");

  // Check environment variables
  const required = [
    "UPSTASH_VECTOR_REST_URL",
    "UPSTASH_VECTOR_REST_TOKEN",
    "GROQ_API_KEY"
  ];

  let allPresent = true;
  for (const key of required) {
    if (process.env[key]) {
      console.log(`✅ ${key}: Set`);
    } else {
      console.log(`❌ ${key}: Missing`);
      allPresent = false;
    }
  }

  if (!allPresent) {
    console.log("\n❌ Some environment variables are missing!");
    process.exit(1);
  }

  // Test Upstash connection
  try {
    console.log("\n🔗 Testing Upstash connection...");
    const index = new Index({
      url: process.env.UPSTASH_VECTOR_REST_URL!,
      token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
    });

    const info = await index.info();
    console.log(`✅ Connected! Vector count: ${info.vectorCount}`);
  } catch (error) {
    console.log("❌ Upstash connection failed:", error);
    process.exit(1);
  }

  console.log("\n✅ All checks passed!");
}

verifyEnv();
```

Run verification:

```bash
npx tsx scripts/verify-env.ts
```

---

## Database Setup

### Option 1: Use Existing Database

Your database already has 200 food vectors:

```bash
# Check database status
python3 ../check_upstash_database.py
```

Expected output:
```
✅ Database: free-loon-62438
✅ Vector Count: 200
✅ Dimensions: 1024
✅ Model: mxbai-embed-large-v1
```

### Option 2: Upload New Data

If you need to add or update food data:

1. **Prepare Data File**:

Edit `data/foods.json`:

```json
[
  {
    "id": "1",
    "name": "Biryani",
    "category": "Main Course",
    "origin": "India",
    "description": "Aromatic rice dish with spices and meat",
    "ingredients": "Rice, meat, spices, herbs",
    "cooking_method": "Layered and slow-cooked",
    "dietary_tags": "Non-vegetarian"
  }
]
```

2. **Upload to Upstash**:

```bash
# Navigate to root directory
cd ..

# Run upload script
python3 upload_foods_to_upstash.py
```

3. **Verify Upload**:

```bash
python3 check_upstash_database.py
```

---

## Development Setup

### 1. Start Development Server

```bash
cd mydigitaltwin
npm run dev
```

Expected output:
```
▲ Next.js 16.0.1
- Local:        http://localhost:3000
- Network:      http://192.168.1.x:3000

✓ Ready in 2.1s
```

### 2. Access Web Interface

Open browser to: http://localhost:3000

You should see the Food RAG chat interface.

### 3. Test Basic Query

In the chat interface, try:
```
What is Biryani?
```

Expected response time:
- First query: ~1700ms (uncached)
- Second query: <50ms (cached)

### 4. Monitor Logs

Development logs show in terminal:

```
[INFO] Processing food query { question: "What is Biryani?", length: 16 }
[PERF] Vector search: 487ms { resultsCount: 3 }
[PERF] AI response generation: 1243ms
[PERF] Complete food query: 1730ms { cached: false }
```

### 5. Development Workflow

```bash
# Make changes to code
# Save file (hot reload automatically)

# Check for TypeScript errors
npm run build

# Run linter
npm run lint

# Format code (if Prettier is configured)
npm run format
```

---

## Testing

### 1. Test Server Actions

Create `tests/server-actions.test.ts`:

```typescript
import { queryFoodRAG, searchByCategory, getCacheStats, clearCache } from '@/actions/foodRagActions';

async function testServerActions() {
  console.log("🧪 Testing Server Actions\n");

  // Test 1: Basic query
  console.log("Test 1: Basic query");
  const result1 = await queryFoodRAG("What is Biryani?");
  console.assert(result1.success, "Query should succeed");
  console.assert(result1.answer, "Should have answer");
  console.log("✅ Passed\n");

  // Test 2: Cache hit
  console.log("Test 2: Cache hit");
  const result2 = await queryFoodRAG("What is Biryani?");
  console.assert(result2.metadata?.cached, "Should be cached");
  console.assert(result2.metadata?.processingTime < 100, "Should be fast");
  console.log("✅ Passed\n");

  // Test 3: Category search
  console.log("Test 3: Category search");
  const result3 = await searchByCategory("Dessert", 5);
  console.assert(result3.success, "Search should succeed");
  console.assert(result3.results && result3.results.length > 0, "Should have results");
  console.log("✅ Passed\n");

  // Test 4: Cache stats
  console.log("Test 4: Cache statistics");
  const stats = await getCacheStats();
  console.assert(stats.success, "Stats should succeed");
  console.assert(stats.stats && stats.stats.size >= 0, "Should have valid stats");
  console.log("✅ Passed\n");

  // Test 5: Clear cache
  console.log("Test 5: Clear cache");
  const clear = await clearCache();
  console.assert(clear.success, "Clear should succeed");
  console.log("✅ Passed\n");

  console.log("✅ All tests passed!");
}

testServerActions().catch(console.error);
```

Run tests:

```bash
npx tsx tests/server-actions.test.ts
```

### 2. Performance Testing

Create `tests/performance.test.ts`:

```typescript
async function performanceTest() {
  console.log("⚡ Performance Testing\n");

  // Test uncached query
  await clearCache();
  
  const start1 = Date.now();
  await queryFoodRAG("What is Sushi?");
  const uncached = Date.now() - start1;
  
  console.log(`Uncached query: ${uncached}ms`);
  console.assert(uncached < 3000, "Should be under 3000ms");

  // Test cached query
  const start2 = Date.now();
  await queryFoodRAG("What is Sushi?");
  const cached = Date.now() - start2;
  
  console.log(`Cached query: ${cached}ms`);
  console.assert(cached < 100, "Should be under 100ms");

  console.log(`\n⚡ Speed improvement: ${Math.round((1 - cached/uncached) * 100)}%`);
}
```

### 3. Error Handling Testing

Test error scenarios:

```typescript
// Test invalid input
const result1 = await queryFoodRAG("");
console.assert(!result1.success, "Empty query should fail");

// Test very long input
const longQuery = "What is ".repeat(100) + "Biryani?";
const result2 = await queryFoodRAG(longQuery);
console.assert(!result2.success, "Long query should fail");
```

---

## Production Deployment

### Deployment to Vercel (Recommended)

#### 1. Prepare for Deployment

```bash
# Build locally to verify
npm run build

# Check for errors
npm run lint
```

#### 2. Deploy to Vercel

**Option A: Vercel CLI**

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel
```

**Option B: GitHub Integration**

1. Go to https://vercel.com
2. Click "Import Project"
3. Select GitHub repository: `VivianP05/ragfood`
4. Set root directory: `mydigitaltwin`
5. Click "Deploy"

#### 3. Configure Environment Variables

In Vercel dashboard:

1. Go to Project Settings → Environment Variables
2. Add all three variables:
   - `UPSTASH_VECTOR_REST_URL`
   - `UPSTASH_VECTOR_REST_TOKEN`
   - `GROQ_API_KEY`
3. Set scope: Production, Preview, Development
4. Save and redeploy

#### 4. Verify Deployment

Visit your deployed URL:
```
https://your-app.vercel.app
```

Test with a query to ensure everything works.

### Deployment to Other Platforms

#### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

#### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
```

### Production Checklist

Before going live:

- [ ] All environment variables configured
- [ ] Build completes without errors
- [ ] All tests passing
- [ ] Error handling tested
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Monitoring set up
- [ ] Backup plan in place

---

## Troubleshooting

### Common Issues

#### Issue 1: "Module not found" Error

**Symptoms**:
```
Error: Cannot find module '@upstash/vector'
```

**Solution**:
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### Issue 2: Environment Variables Not Loading

**Symptoms**:
```
Error: Missing required environment variables
```

**Solutions**:
1. Verify `.env.local` exists in `mydigitaltwin/` directory
2. Check file has no typos in variable names
3. Restart development server
4. Verify file is not `.env.local.example`

```bash
# Check if file exists
ls -la mydigitaltwin/.env.local

# Restart server
npm run dev
```

#### Issue 3: Upstash Connection Failed

**Symptoms**:
```
Error: Failed to connect to Upstash Vector
```

**Solutions**:
1. Verify credentials are correct
2. Check database is active in Upstash console
3. Verify no typos in URL/token
4. Test with verification script

```bash
npx tsx scripts/verify-env.ts
```

#### Issue 4: Slow Query Performance

**Symptoms**:
- Queries taking >3000ms
- Timeout errors

**Solutions**:
1. Check internet connection
2. Verify Upstash region (use closest)
3. Check Groq API status
4. Review performance logs

```typescript
// Check cache hit rate
const stats = await getCacheStats();
console.log(stats);
```

#### Issue 5: Build Fails in Production

**Symptoms**:
```
Error: Build failed with exit code 1
```

**Solutions**:
1. Test build locally first
2. Check for TypeScript errors
3. Verify all imports are correct
4. Check for missing dependencies

```bash
# Local build test
npm run build

# Check for TypeScript errors
npx tsc --noEmit

# Verify dependencies
npm list
```

### Getting Help

1. **Check Documentation**:
   - `README_PROJECT.md` - Main documentation
   - `PERFORMANCE_OPTIMIZATION_GUIDE.md` - Performance info
   - `ERROR_HANDLING_GUIDE.md` - Error handling
   - `agents.md` - Development guide

2. **GitHub Issues**:
   - Search existing issues: https://github.com/VivianP05/ragfood/issues
   - Create new issue with details

3. **Logs and Debugging**:
   - Enable debug logging
   - Check browser console
   - Review server logs
   - Use performance monitoring

---

## Next Steps

After setup is complete:

1. **Customize for Your Needs**:
   - Modify system prompts in `foodRagActions.ts`
   - Adjust cache configuration
   - Add custom food categories
   - Enhance UI with additional features

2. **Monitor Performance**:
   - Track cache hit rates
   - Monitor query response times
   - Review error rates
   - Optimize based on usage patterns

3. **Scale as Needed**:
   - Upgrade Upstash plan for more vectors
   - Increase cache size for more traffic
   - Add rate limiting for production
   - Implement user authentication

4. **Continuous Improvement**:
   - Update food database regularly
   - Fine-tune AI prompts
   - Optimize based on user feedback
   - Add new features incrementally

---

## Resources

- **Upstash Docs**: https://upstash.com/docs/vector
- **Groq Docs**: https://console.groq.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Project Repository**: https://github.com/VivianP05/ragfood

---

**Last Updated**: {{ Current Date }}  
**Version**: 2.0 (Performance Optimized)  
**Maintained By**: VivianP05
