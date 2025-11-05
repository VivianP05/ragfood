# 🚀 Vercel Deployment Guide - Digital Twin MCP Server

**Repository**: VivianP05/ragfood  
**Project Directory**: mydigitaltwin  
**Framework**: Next.js 16.0.1  
**Package Manager**: npm (NOT pnpm)  
**Date**: November 4, 2025  

---

## 📋 Pre-Deployment Checklist

Before deploying, verify you have:

- [x] ✅ **GitHub Repository**: https://github.com/VivianP05/ragfood
- [x] ✅ **Production Build**: Tested and passing (`npm run build`)
- [x] ✅ **Environment Variables**: Ready to configure
- [x] ✅ **Vercel Account**: Sign up at https://vercel.com/ (free tier available)

---

## 🎯 Step-by-Step Deployment Instructions

### **Step 1: Import Repository to Vercel**

1. **Go to Vercel Dashboard**  
   → https://vercel.com/new

2. **Click "Add New..." → "Project"**

3. **Select "Import Git Repository"**

4. **Choose "GitHub" as Git provider**  
   (If first time, you'll need to authorize Vercel to access GitHub)

5. **Find and Import Your Repository**  
   - **Repository Name**: `VivianP05/ragfood` ⭐ **IMPORTANT**
   - Click "Import" next to "ragfood"

---

### **Step 2: Configure Project Settings**

**⚠️ CRITICAL CONFIGURATION - Use These Exact Settings:**

#### **Framework & Build Settings**
```
Framework Preset:     Next.js  (should auto-detect ✅)
Root Directory:       mydigitaltwin  ⭐ IMPORTANT - NOT ./
Build Command:        npm run build  ⭐ IMPORTANT - NOT pnpm
Output Directory:     .next  (auto-detect ✅)
Install Command:      npm install  ⭐ IMPORTANT - NOT pnpm
Node.js Version:      18.x  (or 20.x)
```

#### **How to Set Root Directory**
1. Click "Edit" next to "Root Directory"
2. Type: `mydigitaltwin`
3. Click "Continue"

![Root Directory Configuration](https://i.imgur.com/example.png)

**Why This Matters**:
- ❌ `./ ` (default) → Deploys from `/Users/DELL/ragfood/` (WRONG - no Next.js app there)
- ✅ `mydigitaltwin` → Deploys from `/Users/DELL/ragfood/mydigitaltwin/` (CORRECT - has Next.js app)

---

### **Step 3: Configure Environment Variables** ⭐ MOST IMPORTANT

**🛑 DON'T DEPLOY YET!**

Before clicking "Deploy", add your environment variables:

1. **Click "Environment Variables" section**

2. **Add these 3 variables:**

#### **Variable 1: UPSTASH_VECTOR_REST_URL**
```
Name:  UPSTASH_VECTOR_REST_URL
Value: https://free-loon-62438-us1-vector.upstash.io
```

#### **Variable 2: UPSTASH_VECTOR_REST_TOKEN**
```
Name:  UPSTASH_VECTOR_REST_TOKEN
Value: [Get from your .env.local file - starts with "AY..." or similar]
```

**How to Get Your Token**:
```bash
# In terminal
cat /Users/DELL/ragfood/mydigitaltwin/.env.local

# Copy the UPSTASH_VECTOR_REST_TOKEN value
```

#### **Variable 3: GROQ_API_KEY**
```
Name:  GROQ_API_KEY
Value: [Get from your .env.local file - starts with "gsk_..."]
```

**How to Get Your Groq Key**:
```bash
# Same command as above
cat /Users/DELL/ragfood/mydigitaltwin/.env.local

# Copy the GROQ_API_KEY value
```

#### **Environment Selection**
For each variable, select:
- ✅ **Production** (required)
- ✅ **Preview** (optional, recommended)
- ✅ **Development** (optional)

---

### **Step 4: Deploy!**

Once all 3 environment variables are added:

1. **Review Configuration**:
   ```
   ✅ Root Directory: mydigitaltwin
   ✅ Build Command: npm run build
   ✅ Install Command: npm install
   ✅ Environment Variables: 3 added
   ```

2. **Click "Deploy"** 🚀

3. **Wait for Deployment** (usually 1-3 minutes)
   - You'll see real-time build logs
   - Build progress indicators
   - Success or error messages

4. **Success!** 🎉
   - You'll get a deployment URL like: `https://your-project-abc123.vercel.app`

---

## 🧪 Post-Deployment Testing

### **Step 5: Test Your Deployed MCP Server**

#### **Test 1: Health Check**
```bash
# Replace YOUR_URL with your actual Vercel URL
curl https://your-project-abc123.vercel.app/api/mcp

# Expected Response:
{
  "status": "ok",
  "message": "Food RAG MCP Server is running",
  "version": "3.0.0",
  "tools": 9
}
```

✅ **Pass**: You see the JSON response with 9 tools  
❌ **Fail**: Error or timeout → Check logs

---

#### **Test 2: MCP Tools Listing**
```bash
curl -X POST https://your-project-abc123.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# Expected: List of 9 tools
# - 6 digital twin tools
# - 3 food RAG tools
```

✅ **Pass**: You see 9 tools listed  
❌ **Fail**: Error → Check environment variables

---

#### **Test 3: Food Query**
```bash
curl -X POST https://your-project-abc123.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "query_food_database",
      "arguments": {
        "question": "What is Biryani?"
      }
    }
  }'

# Expected: AI-generated response about Biryani
```

✅ **Pass**: You get detailed food description  
❌ **Fail**: Error → Check Upstash/Groq credentials

---

#### **Test 4: Professional Profile Query**
```bash
curl -X POST https://your-project-abc123.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "query_professional_profile",
      "arguments": {
        "question": "What are my salary expectations?"
      }
    }
  }'

# Expected: Response about contract ($500-600/day) and permanent ($55k-70k)
```

✅ **Pass**: You get salary expectations  
❌ **Fail**: Check Python script permissions

---

### **Step 6: Update Claude Desktop Configuration**

Once deployed, update Claude Desktop to use **production URL**:

#### **Edit Claude Desktop Config**
```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### **Update Configuration**
```json
{
  "mcpServers": {
    "vivian-digital-twin-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-project-abc123.vercel.app/api/mcp"
      ]
    }
  }
}
```

**Replace** `https://your-project-abc123.vercel.app` with your **actual Vercel URL**

#### **Restart Claude Desktop**
1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Verify 9 MCP tools appear
4. Test a query: "What is Biryani?"

---

## 🔧 Troubleshooting

### **Issue 1: Build Fails with "Root Directory Not Found"**

**Error**: `Error: Cannot find package.json`

**Solution**:
- ✅ Set Root Directory to `mydigitaltwin` (not `./`)
- Go to Project Settings → General → Root Directory
- Change to `mydigitaltwin`
- Redeploy

---

### **Issue 2: Build Fails with TypeScript Errors**

**Error**: `Type error: Property 'X' does not exist`

**Solution**:
- Check your local build first: `npm run build`
- Fix TypeScript errors locally
- Commit and push fixes to GitHub
- Vercel will auto-redeploy

---

### **Issue 3: Environment Variables Not Working**

**Error**: `Error: Missing UPSTASH_VECTOR_REST_URL`

**Solution**:
1. Go to Project Settings → Environment Variables
2. Verify all 3 variables are set:
   - ✅ UPSTASH_VECTOR_REST_URL
   - ✅ UPSTASH_VECTOR_REST_TOKEN
   - ✅ GROQ_API_KEY
3. Click "Redeploy" → "Use existing Build Cache" → "Redeploy"

---

### **Issue 4: MCP Server Returns 404**

**Error**: `GET /api/mcp returns 404 Not Found`

**Solution**:
- Verify route file exists: `mydigitaltwin/app/api/mcp/route.ts`
- Check build logs for route compilation
- Ensure Next.js App Router is used (not Pages Router)

---

### **Issue 5: Python Script Fails**

**Error**: `Error: python3: command not found` or `vivian_profile_query.py failed`

**Solution**:

⚠️ **Important**: Vercel **does not support Python execution** in Next.js deployments

**Your Options**:

**Option A: Digital Twin Tools Will Not Work on Vercel**
- Food RAG tools will work (TypeScript/JavaScript)
- Digital twin tools require Python script (will fail)
- This is a limitation of Vercel's Next.js hosting

**Option B: Deploy Python Backend Separately**
1. Deploy `vivian_profile_query.py` to:
   - **Railway** (supports Python + Next.js)
   - **Render** (supports Python)
   - **Heroku** (supports Python)

2. Update `digitalTwinActions.ts` to call remote Python API instead of local script

**Option C: Rewrite Digital Twin in TypeScript**
- Migrate `vivian_profile_query.py` logic to TypeScript
- Use Upstash Vector TypeScript SDK directly
- Use Groq TypeScript SDK for AI generation
- Update `digitalTwinActions.ts` to use TypeScript functions

**Recommendation**: Use **Railway** for full-stack deployment (Python + Next.js)

---

## 🌐 Alternative: Deploy to Railway (Supports Python)

If you need Python script support for digital twin queries:

### **Railway Deployment**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Navigate to project root
cd /Users/DELL/ragfood

# Initialize Railway project
railway init

# Deploy
railway up

# Set environment variables
railway variables set UPSTASH_VECTOR_REST_URL=https://free-loon-62438-us1-vector.upstash.io
railway variables set UPSTASH_VECTOR_REST_TOKEN=your-token
railway variables set GROQ_API_KEY=your-key

# Access deployment URL
railway open
```

**Railway Advantages**:
- ✅ Supports Python execution
- ✅ Supports Next.js
- ✅ Auto-deploys from GitHub
- ✅ All 9 MCP tools will work
- ✅ Free tier available

**Railway Dashboard**: https://railway.app/

---

## 📊 Deployment Comparison

| Feature | Vercel | Railway | Netlify |
|---------|--------|---------|---------|
| **Next.js Support** | ✅ Excellent | ✅ Good | ✅ Good |
| **Python Support** | ❌ No | ✅ Yes | ❌ No |
| **Auto-Deploy** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Free Tier** | ✅ Generous | ✅ Available | ✅ Available |
| **Speed** | ⚡ Fastest | ⚡ Fast | ⚡ Fast |
| **Food RAG Tools** | ✅ Work | ✅ Work | ✅ Work |
| **Digital Twin Tools** | ❌ Fail (Python) | ✅ Work | ❌ Fail (Python) |

**Recommendation**:
- **Food RAG only**: Use Vercel (best Next.js hosting)
- **Full system (Food + Digital Twin)**: Use Railway (Python support)

---

## 🎯 Post-Deployment Checklist

After successful deployment:

- [ ] ✅ Health check passes (`/api/mcp` returns status ok)
- [ ] ✅ MCP tools listing returns 9 tools
- [ ] ✅ Food query test passes (Biryani query works)
- [ ] ✅ Professional profile query tested (if using Railway)
- [ ] ✅ Claude Desktop config updated with production URL
- [ ] ✅ Claude Desktop restarted
- [ ] ✅ Test queries in Claude Desktop
- [ ] ✅ Monitor deployment logs for errors
- [ ] ✅ Set up custom domain (optional)
- [ ] ✅ Enable analytics (optional)

---

## 📈 Monitoring Your Deployment

### **Vercel Dashboard Monitoring**

1. **Analytics** (if enabled):
   - Page views
   - Response times
   - Error rates

2. **Deployment Logs**:
   - Build logs
   - Runtime logs
   - Function logs

3. **Function Metrics**:
   - Invocations
   - Duration
   - Errors

### **Upstash Monitoring**

Monitor your Upstash Vector usage:
- Dashboard: https://console.upstash.com/vector
- Database: `free-loon-62438`
- Metrics:
  - Query count
  - Vector count (should be 227)
  - Bandwidth usage

### **Groq Monitoring**

Monitor your Groq API usage:
- Dashboard: https://console.groq.com/
- Metrics:
  - API calls
  - Token usage
  - Response times

---

## 🎉 Success Metrics

Your deployment is successful when:

✅ **Build**: Completes in < 2 minutes  
✅ **Health Check**: Returns 200 OK with 9 tools  
✅ **Food Queries**: Return AI responses in < 3 seconds  
✅ **Profile Queries**: Work (if using Railway)  
✅ **Claude Desktop**: Shows 9 MCP tools  
✅ **Uptime**: 99.9%+ (Vercel's SLA)  

---

## 🚀 Next Steps After Deployment

1. **Test Thoroughly**:
   - Run all 9 MCP tools
   - Test edge cases
   - Monitor error rates

2. **Optional Enhancements**:
   - Add custom domain
   - Enable Vercel Analytics
   - Set up error tracking (Sentry)
   - Add API rate limiting

3. **Interview Preparation**:
   - Use deployed digital twin for mock interviews
   - Test professional profile queries
   - Practice STAR format responses

4. **Share Your Work**:
   - Add deployment URL to resume
   - Share in LinkedIn post
   - Demo in interviews

---

## 📞 Support & Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **Next.js Deployment**: https://nextjs.org/docs/deployment
- **Upstash Docs**: https://upstash.com/docs/vector
- **Groq Docs**: https://console.groq.com/docs

**Your Repository**: https://github.com/VivianP05/ragfood

---

## ✅ Ready to Deploy?

**Your Configuration Summary**:
```
Repository:           VivianP05/ragfood
Root Directory:       mydigitaltwin
Framework:            Next.js 16.0.1
Package Manager:      npm
Build Command:        npm run build
Environment Vars:     3 required

Tools Available:
  • Food RAG (3):     ✅ Will work on Vercel
  • Digital Twin (6): ⚠️  Requires Railway (Python)
```

**Choose Your Platform**:
- **Vercel**: Best for Food RAG (3 tools) - https://vercel.com/new
- **Railway**: Full system (9 tools) - https://railway.app/new

---

**Last Updated**: November 4, 2025  
**Created by**: GitHub Copilot + Vivian Pham  
**Project**: Digital Twin MCP Server v3.0.0  

🚀 **Ready to deploy? Let's go!**
