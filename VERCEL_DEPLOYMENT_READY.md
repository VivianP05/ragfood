# 🚀 Vercel Deployment Guide - Vivian's Resume RAG

## ✅ Pre-Deployment Checklist

### 1. Local Testing Complete
- [x] Resume uploaded to Upstash (15 chunks)
- [x] Professional profile uploaded (29 items)
- [x] Next.js app updated with resume queries
- [x] Server running locally at http://localhost:3000
- [x] Environment variables configured

### 2. Code Changes Summary
- [x] Created `resumeRagActions.ts` server action
- [x] Updated `page.tsx` with resume-focused UI
- [x] Updated `app/api/query/route.ts` to use resume RAG
- [x] Example questions updated for professional context

---

## 📦 Deployment Steps

### Step 1: Push to GitHub

```bash
cd /Users/DELL/ragfood

# Check current status
git status

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: update Next.js app with resume RAG and deploy to Vercel

- Created resumeRagActions.ts server action for resume queries
- Updated UI with professional theme and resume-focused questions
- Modified API route to use queryResumeRAG instead of food RAG
- Updated example questions: Jung Talents, Tableau, Power BI, achievements
- Ready for Vercel deployment with environment variables"

# Push to GitHub
git push origin cloud-migration
```

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI (Recommended)

```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from mydigitaltwin directory
cd /Users/DELL/ragfood/mydigitaltwin

# Deploy to production
vercel --prod

# Follow prompts:
# - Link to existing project? No (first time) or Yes (if exists)
# - Project name: vivian-resume-rag (or your choice)
# - Directory: ./ (current directory)
# - Override settings? No
```

#### Option B: Vercel Dashboard (Alternative)

1. Go to https://vercel.com/new
2. Import Git Repository
3. Select: `VivianP05/ragfood`
4. Configure Project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `mydigitaltwin`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 3: Configure Environment Variables in Vercel

**CRITICAL**: Add these environment variables in Vercel Dashboard

1. Go to Project Settings → Environment Variables
2. Add the following variables:

```bash
# Upstash Vector Database
UPSTASH_VECTOR_REST_URL=<your-upstash-vector-url>
UPSTASH_VECTOR_REST_TOKEN=<your-upstash-vector-token>

# Groq AI API
GROQ_API_KEY=<your-groq-api-key>
```

**Get your actual values from `/Users/DELL/ragfood/mydigitaltwin/.env.local`**

3. Set for: **Production**, **Preview**, **Development**
4. Click **Save**

### Step 4: Trigger Deployment

After adding environment variables:
- Go to Deployments tab
- Click **Redeploy** on latest deployment
- Wait for build to complete (~2-3 minutes)

---

## 🧪 Post-Deployment Testing

### Test URLs

Once deployed, you'll get a URL like:
- **Production**: `https://vivian-resume-rag.vercel.app`
- **Preview**: `https://vivian-resume-rag-git-cloud-migration-vivianp05.vercel.app`

### Test Queries

Visit your deployed site and test these questions:

1. **Jung Talents Experience**
   - "Tell me about Vivian's experience at Jung Talents"
   - Expected: 5-month Data Dashboard project with Tableau + Power BI

2. **Technical Skills**
   - "What are Vivian's Tableau and Power BI skills?"
   - Expected: Both Level 3, Microsoft certified, LOD expressions, DAX

3. **Achievements**
   - "What are Vivian's biggest achievements?"
   - Expected: 572 hours saved, 97% accuracy, 15+ stakeholders

4. **Career Goals**
   - "What are Vivian's career goals?"
   - Expected: Master's degree, Data Scientist role, target companies

5. **Availability**
   - "Is Vivian available for full-time work?"
   - Expected: Yes, immediate start (2 weeks notice), full-time capacity

### Success Criteria

- [ ] All 5 test queries return accurate responses
- [ ] Response time < 3 seconds
- [ ] Sources displayed correctly
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Dark mode working

---

## 🔧 Troubleshooting

### Issue: Build Fails

**Symptoms**: Vercel deployment fails during build

**Solutions**:
```bash
# Test build locally first
cd /Users/DELL/ragfood/mydigitaltwin
npm run build

# If build fails, check:
# 1. TypeScript errors
npm run lint

# 2. Missing dependencies
npm install

# 3. Node version (should be 18+)
node --version
```

### Issue: Environment Variables Not Working

**Symptoms**: 500 errors, "Missing environment variables"

**Solutions**:
1. Check Vercel Dashboard → Settings → Environment Variables
2. Ensure all 3 variables are set
3. Verify they're set for Production environment
4. Redeploy after adding variables

### Issue: Vector Search Returns No Results

**Symptoms**: "No relevant information found" errors

**Solutions**:
1. Verify Upstash database has 244 vectors
   ```bash
   python3 check_upstash_database.py
   ```
2. Check resume chunks uploaded:
   ```bash
   python3 upload_resume_to_upstash.py
   ```
3. Verify UPSTASH_VECTOR_REST_URL is correct in Vercel

### Issue: Groq API Rate Limits

**Symptoms**: "Rate limit exceeded" errors

**Solutions**:
1. Response caching is enabled (10 minutes)
2. Check Groq dashboard: https://console.groq.com/
3. Upgrade Groq plan if needed
4. Implement longer cache TTL if needed

---

## 📊 Performance Optimization

### Vercel Configuration

Add to `next.config.ts`:

```typescript
const nextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  // Optional: Enable compression
  compress: true,
};
```

### Edge Functions (Optional)

For faster responses, consider deploying API routes to Edge:

```typescript
// In app/api/query/route.ts
export const runtime = 'edge';
```

### Monitoring

Enable Vercel Analytics:
1. Go to Project → Analytics
2. Enable Web Analytics
3. Monitor performance metrics

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain

1. Go to Project Settings → Domains
2. Add domain: `resume.vivianpham.dev` (or your choice)
3. Configure DNS:
   - Type: CNAME
   - Name: resume
   - Value: cname.vercel-dns.com
4. Wait for DNS propagation (~5-30 minutes)

### SSL Certificate

- Vercel automatically provisions SSL certificate
- HTTPS enabled by default
- No configuration needed

---

## 📱 Sharing Your Resume RAG

### Public Links

Share your deployed app:
- **Production**: `https://your-project.vercel.app`
- **LinkedIn**: Add to profile projects section
- **Resume**: Include as portfolio link
- **GitHub README**: Add deployment badge

### Deployment Badge

Add to README.md:

```markdown
[![Deployed on Vercel](https://vercel.com/button)](https://your-project.vercel.app)
```

### Demo Video

Record a quick demo:
1. Open deployed site
2. Ask: "Tell me about Jung Talents experience"
3. Show: Response with Tableau/Power BI details
4. Ask: "What are the biggest achievements?"
5. Show: 572 hours saved, 97% accuracy

---

## 🔐 Security Checklist

- [x] Environment variables not in code
- [x] `.env.local` in `.gitignore`
- [x] API keys stored in Vercel securely
- [x] CORS not overly permissive
- [x] Input validation in API routes
- [x] Rate limiting via Groq API
- [x] No sensitive data in responses

---

## 📈 Next Steps After Deployment

### 1. Monitor Performance
- Check Vercel Analytics dashboard
- Monitor response times
- Track cache hit rates

### 2. Gather Feedback
- Share with friends/colleagues
- Test different question types
- Collect usage analytics

### 3. Iterate & Improve
- Add more resume sections if needed
- Implement feedback
- Optimize response quality
- Add more example questions

### 4. Update Resume
- Keep Upstash data synchronized with resume
- Re-upload when experience changes
- Test new queries after updates

---

## 🎯 Deployment Commands Summary

```bash
# 1. Commit and push changes
git add .
git commit -m "feat: update Next.js app with resume RAG"
git push origin cloud-migration

# 2. Deploy to Vercel
cd mydigitaltwin
vercel --prod

# 3. Test deployment
curl https://your-project.vercel.app/api/query \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Vivian's Tableau experience?"}'

# 4. Monitor logs
vercel logs
```

---

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **Upstash Support**: https://upstash.com/docs
- **Groq Docs**: https://console.groq.com/docs

---

**Status**: Ready for deployment 🚀  
**Last Updated**: November 19, 2025  
**Deployed By**: Vivian Pham
