{
  "mcpServers": {
    "food-rag-system": {
      "type": "http",
      "url": "http://localhost:3000/api/mcp",
      "timeout": 30000,
      "description": "Food RAG System - AI-powered food and cuisine knowledge base with 200+ items"
    }
  }
}# 🚀 Vercel Deployment Guide - Food RAG System

## Overview

This guide walks you through deploying your Food RAG System to Vercel, from initial setup to production verification. Total time: 15-20 minutes.

---

## 📋 Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with repository access
- [ ] Vercel account (free tier works)
- [ ] Upstash Vector database credentials
- [ ] Groq API key
- [ ] Local build passes (`npm run build`)
- [ ] All tests passing locally

---

## Step 1: Prepare Your Repository (5 minutes)

### 1.1 Verify Git Status

```bash
cd /Users/DELL/ragfood

# Check what's changed
git status

# View recent commits
git log --oneline -5
```

### 1.2 Commit All Changes

```bash
# Add all files
git add .

# Commit with descriptive message
git commit -m "feat: add performance optimizations and monitoring dashboard"

# Push to GitHub
git push origin cloud-migration
```

### 1.3 Verify GitHub Repository

Visit: https://github.com/VivianP05/ragfood

Ensure all files are uploaded:
- ✅ `mydigitaltwin/src/actions/foodRagActions.ts`
- ✅ `mydigitaltwin/src/components/MonitoringDashboard.tsx`
- ✅ `mydigitaltwin/src/app/dashboard/page.tsx`
- ✅ `mydigitaltwin/src/app/api/cache-stats/route.ts`
- ✅ `mydigitaltwin/src/app/api/clear-cache/route.ts`
- ✅ All documentation files

---

## Step 2: Set Up Vercel Project (5 minutes)

### 2.1 Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your repositories

### 2.2 Import Project

1. Click "Add New..." → "Project"
2. Select "Import Git Repository"
3. Find `VivianP05/ragfood` in the list
4. Click "Import"

### 2.3 Configure Project Settings

**Framework Preset**: Next.js (auto-detected)

**Root Directory**: 
```
mydigitaltwin
```

**Build Command** (default is fine):
```bash
npm run build
```

**Output Directory** (default):
```
.next
```

**Install Command** (default):
```bash
npm install
```

### 2.4 Environment Variables

Click "Environment Variables" and add all three:

**1. UPSTASH_VECTOR_REST_URL**
```
https://free-loon-62438-us1-vector.upstash.io
```
- Type: `Plain Text`
- Environments: ✅ Production, ✅ Preview, ✅ Development

**2. UPSTASH_VECTOR_REST_TOKEN**
```
[Your Upstash token from .env file]
```
- Type: `Sensitive` (will be encrypted)
- Environments: ✅ Production, ✅ Preview, ✅ Development

**3. GROQ_API_KEY**
```
[Your Groq API key from .env file]
```
- Type: `Sensitive` (will be encrypted)
- Environments: ✅ Production, ✅ Preview, ✅ Development

**⚠️ Important**: Never paste actual keys in documentation. Get them from your local `.env.local` file.

### 2.5 Deploy!

Click "Deploy" button and wait 2-3 minutes.

Expected output:
```
Building...
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages
✓ Finalizing page optimization

Deployment completed successfully! 🎉
```

---

## Step 3: Verify Deployment (3 minutes)

### 3.1 Access Your Deployment

Vercel will provide a URL like:
```
https://ragfood-viviap05.vercel.app
```

### 3.2 Test Main Features

**Test 1: Main Chat Interface**

1. Go to: `https://your-app.vercel.app`
2. Type: "What is Biryani?"
3. Expected: Response in 1500-2000ms
4. Type same question again
5. Expected: Response in <50ms (cached) ⚡

**Test 2: Monitoring Dashboard**

1. Go to: `https://your-app.vercel.app/dashboard`
2. Check cache stats are loading
3. Verify auto-refresh works
4. Click "Refresh" button

**Test 3: API Endpoints**

```bash
# Test cache stats
curl https://your-app.vercel.app/api/cache-stats

# Expected response:
# {"success":true,"stats":{"size":1,"maxSize":200,...}}

# Test query endpoint
curl -X POST https://your-app.vercel.app/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Sushi?"}'

# Expected: JSON with success:true and answer
```

---

## Step 4: Configure Custom Domain (Optional, 5 minutes)

### 4.1 Add Domain in Vercel

1. Go to Project Settings → Domains
2. Enter your domain (e.g., `foodrag.example.com`)
3. Click "Add"

### 4.2 Configure DNS

Vercel will provide DNS records to add:

**Option A: CNAME Record (Recommended)**
```
Type:  CNAME
Name:  foodrag (or your subdomain)
Value: cname.vercel-dns.com
```

**Option B: A Record**
```
Type:  A
Name:  @ (or your subdomain)
Value: 76.76.21.21
```

### 4.3 Verify Domain

- Wait 5-30 minutes for DNS propagation
- Vercel will auto-verify and issue SSL certificate
- Access via your custom domain!

---

## Step 5: Production Optimization (5 minutes)

### 5.1 Enable Analytics

1. Go to Project → Analytics
2. Enable "Web Analytics"
3. Optionally add "Speed Insights"

### 5.2 Configure Caching Headers

Create `vercel.json` in `mydigitaltwin/`:

```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=1, stale-while-revalidate"
        }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

Commit and push:
```bash
git add mydigitaltwin/vercel.json
git commit -m "feat: add Vercel configuration"
git push origin cloud-migration
```

Vercel will auto-deploy the update.

### 5.3 Set Up Environment Secrets

For production secrets rotation:

1. Go to Project Settings → Environment Variables
2. For sensitive variables, use Vercel's secret management
3. Update secrets without redeployment

---

## Step 6: Monitoring & Alerts (3 minutes)

### 6.1 Set Up Vercel Monitoring

1. Go to Project → Deployments
2. Click on latest deployment
3. View "Build Logs" for errors
4. Check "Function Logs" for runtime issues

### 6.2 Configure Upstash Alerts

1. Go to Upstash Console
2. Enable usage alerts (90% capacity)
3. Add email for notifications

### 6.3 Configure Groq Alerts

1. Go to Groq Console
2. Monitor API usage
3. Set rate limit warnings

---

## Step 7: Performance Verification (5 minutes)

### 7.1 Run Lighthouse Audit

1. Open your deployed URL in Chrome
2. Open DevTools (F12)
3. Go to "Lighthouse" tab
4. Click "Analyze page load"

**Target Scores**:
- Performance: 90+ ✅
- Accessibility: 90+ ✅
- Best Practices: 90+ ✅
- SEO: 90+ ✅

### 7.2 Test Global Performance

Use https://tools.pingdom.com/:

1. Enter your Vercel URL
2. Test from multiple locations
3. Verify response times <2000ms globally

### 7.3 Load Testing (Optional)

```bash
# Install Apache Bench (if not installed)
# macOS:
brew install httpd

# Run load test (100 requests, 10 concurrent)
ab -n 100 -c 10 -p query.json -T application/json \
  https://your-app.vercel.app/api/query
```

Create `query.json`:
```json
{"question":"What is Biryani?"}
```

**Expected Results**:
- Mean response time: <2000ms
- No failed requests
- Consistent performance

---

## Troubleshooting

### Issue: Build Fails

**Symptoms**:
```
Error: Build failed with exit code 1
```

**Solutions**:

1. **Check Build Logs**:
   - Go to Deployment → View Build Logs
   - Look for TypeScript errors
   
2. **Test Locally First**:
   ```bash
   cd mydigitaltwin
   npm run build
   ```
   
3. **Common Fixes**:
   ```bash
   # Clear cache and reinstall
   rm -rf node_modules .next
   npm install
   npm run build
   ```

### Issue: Environment Variables Not Working

**Symptoms**:
- "Missing required environment variables" error
- API calls failing

**Solutions**:

1. **Verify in Vercel Dashboard**:
   - Go to Settings → Environment Variables
   - Ensure all 3 variables are set
   - Check they're enabled for Production

2. **Redeploy After Adding**:
   - Environment variable changes require redeployment
   - Click "Redeploy" in Deployments tab

3. **Check Variable Names**:
   - Must match exactly: `UPSTASH_VECTOR_REST_URL` (not `UPSTASH_URL`)
   - No extra spaces
   - No quotes around values

### Issue: Slow Performance in Production

**Symptoms**:
- Queries taking >5000ms
- Timeout errors

**Diagnosis**:

1. **Check Region**:
   ```bash
   # Test from different locations
   curl -w "@curl-format.txt" https://your-app.vercel.app/api/query
   ```

2. **View Function Logs**:
   - Vercel Dashboard → Functions
   - Check execution times
   - Look for errors

**Solutions**:

1. **Optimize Upstash Region**:
   - Use Upstash database in same region as Vercel deployment
   - US East (Vercel) + US East (Upstash) = Optimal

2. **Check API Rate Limits**:
   - Groq: Monitor usage in console
   - Upstash: Check connection logs

3. **Increase Cache**:
   ```typescript
   const CACHE_CONFIG = {
     MAX_SIZE: 500,  // Increase for production
     TTL_MS: 15 * 60 * 1000,  // 15 minutes
   };
   ```

### Issue: Dashboard Not Loading

**Symptoms**:
- `/dashboard` shows 404
- Components not rendering

**Solutions**:

1. **Check File Structure**:
   ```bash
   # Verify files exist
   ls mydigitaltwin/src/app/dashboard/
   ls mydigitaltwin/src/components/
   ```

2. **Rebuild**:
   ```bash
   npm run build
   git push
   ```

3. **Check Build Output**:
   - Look for "Generating static pages"
   - Ensure `/dashboard` is listed

---

## Post-Deployment Checklist

After deployment is complete:

- [ ] Main chat interface works
- [ ] Dashboard loads and shows stats
- [ ] API endpoints respond correctly
- [ ] Cache is functioning (<50ms for cached)
- [ ] Environment variables are set
- [ ] Custom domain configured (if applicable)
- [ ] Analytics enabled
- [ ] Performance meets targets
- [ ] Error monitoring set up
- [ ] Documentation updated with live URL

---

## Continuous Deployment

### Automatic Deployments

Vercel automatically deploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "feat: add new feature"
git push origin cloud-migration

# Vercel automatically:
# 1. Detects push
# 2. Runs build
# 3. Deploys to production
# 4. Notifies you via email
```

### Preview Deployments

Every branch/PR gets a preview URL:

1. Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make changes and push:
   ```bash
   git push origin feature/new-feature
   ```

3. Vercel creates preview URL:
   ```
   https://ragfood-feature-new-feature-viviap05.vercel.app
   ```

4. Test preview before merging
5. Merge to main → Auto-deploys to production

---

## Best Practices

### Security

- ✅ Never commit `.env.local` or `.env` files
- ✅ Use Vercel's environment variable encryption
- ✅ Rotate API keys every 90 days
- ✅ Enable 2FA on Vercel account
- ✅ Review security headers in `vercel.json`

### Performance

- ✅ Monitor cache hit rates (target >50%)
- ✅ Use Edge Functions for API routes (coming soon)
- ✅ Enable compression in Vercel
- ✅ Optimize images with Next.js Image component
- ✅ Review Web Vitals regularly

### Monitoring

- ✅ Check deployment logs daily
- ✅ Review function execution times
- ✅ Monitor error rates
- ✅ Track cache statistics
- ✅ Set up alerts for failures

### Costs

**Free Tier Limits** (Vercel):
- 100 GB bandwidth/month
- 100 serverless function executions/day
- Unlimited deployments

**Upgrade When**:
- >100 GB bandwidth
- Need custom domains
- Require team collaboration
- Need advanced analytics

---

## Support Resources

### Vercel

- **Documentation**: https://vercel.com/docs
- **Support**: https://vercel.com/support
- **Community**: https://github.com/vercel/vercel/discussions

### Upstash

- **Docs**: https://upstash.com/docs/vector
- **Discord**: https://upstash.com/discord
- **Status**: https://status.upstash.com

### Groq

- **Docs**: https://console.groq.com/docs
- **Status**: https://status.groq.com

---

## Next Steps After Deployment

1. **Share Your App**:
   - Add link to README.md
   - Share with stakeholders
   - Get user feedback

2. **Monitor Performance**:
   - Check dashboard daily
   - Review metrics weekly
   - Optimize based on usage

3. **Iterate**:
   - Add new features
   - Improve based on feedback
   - Scale as needed

4. **Document**:
   - Update README with live URL
   - Create user guide
   - Document API endpoints

---

## Success! 🎉

Your Food RAG System is now live on Vercel!

**Your Live URLs**:
- Main App: `https://your-app.vercel.app`
- Dashboard: `https://your-app.vercel.app/dashboard`
- API: `https://your-app.vercel.app/api/query`

**Share it**:
- Update GitHub README with live link
- Share on social media
- Show it off!

---

**Last Updated**: October 31, 2025  
**Version**: 2.0 (Performance Optimized)  
**Maintained By**: VivianP05
