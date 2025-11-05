# 🚂 Railway Deployment Guide - Full Digital Twin MCP Server

**Repository**: VivianP05/ragfood  
**Framework**: Next.js 16.0.1 + Python 3.x  
**Platform**: Railway (Supports Python + Next.js)  
**All Tools**: 9 MCP tools (6 digital twin + 3 food RAG) ✅  
**Date**: November 4, 2025  

---

## 🎯 Why Railway?

Railway is the **recommended platform** for this project because:

✅ **Full Python Support** - All 6 digital twin tools work  
✅ **Next.js Support** - All 3 food RAG tools work  
✅ **Auto-Deploy from GitHub** - Push to deploy  
✅ **Environment Variables** - Easy configuration  
✅ **Free Tier** - $5/month credit (covers basic usage)  
✅ **Simple Setup** - One command deployment  

**vs. Vercel**: Vercel doesn't support Python execution (only 3/9 tools would work)

---

## 📋 Prerequisites

Before starting, ensure you have:

- [x] ✅ **GitHub Repository**: https://github.com/VivianP05/ragfood (pushed)
- [x] ✅ **Railway Account**: Sign up at https://railway.app/
- [x] ✅ **Environment Variables**: Ready from `.env.local`
- [x] ✅ **Production Build**: Tested locally (`npm run build` passed)

---

## 🚀 Step-by-Step Railway Deployment

### **Step 1: Install Railway CLI**

```bash
# Install Railway CLI globally
npm install -g @railway/cli

# Verify installation
railway --version
# Expected: Railway CLI version 3.x.x or higher
```

**Alternative**: Use Railway web dashboard (no CLI needed)

---

### **Step 2: Login to Railway**

#### **Method A: CLI Login** (Recommended)

```bash
# Login to Railway
railway login

# This will:
# 1. Open browser for authentication
# 2. Ask you to authorize Railway CLI
# 3. Return to terminal when complete
```

✅ **Success**: You'll see "Logged in as [your-email]"

#### **Method B: Web Dashboard**

Go to https://railway.app/login and sign in with:
- GitHub (recommended - auto-imports repos)
- Google
- Email

---

### **Step 3: Create New Railway Project**

#### **Method A: CLI (From Your Project)**

```bash
# Navigate to your project root
cd /Users/DELL/ragfood

# Initialize Railway project
railway init

# You'll be asked:
# "Project name?" → Enter: vivian-digital-twin-mcp
# "Environment?" → Select: production
```

#### **Method B: Web Dashboard**

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Select **"VivianP05/ragfood"**
4. Railway will auto-detect Next.js

---

### **Step 4: Configure Project Settings**

Railway needs to know which directory contains your Next.js app:

#### **Set Root Directory**

```bash
# Using CLI
railway variables set ROOT_DIRECTORY=mydigitaltwin

# Or in Railway Dashboard:
# Settings → Root Directory → "mydigitaltwin"
```

#### **Configure Build Settings**

Railway **auto-detects** Next.js, but verify these settings:

```yaml
# In Railway Dashboard → Settings

Build Command:     npm run build
Start Command:     npm start
Install Command:   npm install
Root Directory:    mydigitaltwin
```

**Important**: Railway will also detect Python dependencies automatically!

---

### **Step 5: Set Environment Variables** ⭐ **CRITICAL**

Add your 3 required environment variables:

#### **Method A: CLI**

```bash
# Navigate to project
cd /Users/DELL/ragfood

# Set variables (replace with your actual values from .env.local)
railway variables set UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"

railway variables set UPSTASH_VECTOR_REST_TOKEN="your-token-here"

railway variables set GROQ_API_KEY="your-groq-key-here"

# Verify variables are set
railway variables
```

#### **Method B: Web Dashboard**

1. Go to your project in Railway Dashboard
2. Click **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these 3 variables:

**Variable 1:**
```
Name:  UPSTASH_VECTOR_REST_URL
Value: https://free-loon-62438-us1-vector.upstash.io
```

**Variable 2:**
```
Name:  UPSTASH_VECTOR_REST_TOKEN
Value: [Copy from /Users/DELL/ragfood/mydigitaltwin/.env.local]
```

**Variable 3:**
```
Name:  GROQ_API_KEY
Value: [Copy from /Users/DELL/ragfood/mydigitaltwin/.env.local]
```

---

### **Step 6: Create Railway Configuration File** (Optional but Recommended)

Create a `railway.json` in your project root:

```bash
# Create Railway config
cat > /Users/DELL/ragfood/railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "cd mydigitaltwin && npm install && npm run build"
  },
  "deploy": {
    "startCommand": "cd mydigitaltwin && npm start",
    "healthcheckPath": "/api/mcp",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
```

This ensures Railway:
- ✅ Builds from `mydigitaltwin` directory
- ✅ Uses npm (not pnpm)
- ✅ Health checks your MCP endpoint
- ✅ Auto-restarts on failures

---

### **Step 7: Deploy to Railway** 🚀

#### **Method A: CLI Deployment**

```bash
# Navigate to project
cd /Users/DELL/ragfood

# Deploy to Railway
railway up

# Railway will:
# 1. Detect Next.js app in mydigitaltwin/
# 2. Install npm dependencies
# 3. Install Python dependencies (for digital twin tools)
# 4. Build Next.js app
# 5. Start production server
# 6. Provide deployment URL
```

**Expected Output**:
```
🚂 Deploying...
✓ Building...
✓ Deploying...
✓ Success! Deployed to https://your-project.up.railway.app
```

#### **Method B: GitHub Auto-Deploy** (Recommended)

1. **Connect GitHub** (if not already):
   - Railway Dashboard → Project Settings
   - Connect to GitHub
   - Select `VivianP05/ragfood`
   - Select branch: `cloud-migration`

2. **Enable Auto-Deploy**:
   - Settings → Deployments
   - Enable "Auto-deploy on push"
   - Every GitHub push will auto-deploy!

3. **Trigger First Deployment**:
   ```bash
   # Push to trigger deployment
   git push origin cloud-migration
   ```

Railway will automatically deploy whenever you push to GitHub!

---

### **Step 8: Monitor Deployment** 📊

#### **View Deployment Logs**

```bash
# CLI
railway logs

# Or in Dashboard:
# Project → Deployments → Click latest deployment → View logs
```

**What to Look For**:
```
✓ Installing dependencies...
✓ Building Next.js app...
✓ Detected Python requirements
✓ Installing Python packages...
✓ Build completed
✓ Starting server on port 3000...
✓ Ready on http://0.0.0.0:3000
```

#### **Check Deployment Status**

```bash
# CLI
railway status

# Expected output:
# Status: RUNNING
# URL: https://your-project.up.railway.app
```

---

## 🧪 Post-Deployment Testing

### **Step 9: Test Your Deployed MCP Server**

Once deployed, you'll get a Railway URL like: `https://vivian-digital-twin-mcp-production.up.railway.app`

#### **Test 1: Health Check** ✅

```bash
# Replace with YOUR Railway URL
curl https://your-project.up.railway.app/api/mcp

# Expected Response:
{
  "status": "ok",
  "message": "Food RAG MCP Server is running",
  "version": "3.0.0",
  "tools": 9
}
```

✅ **Pass**: JSON response with 9 tools  
❌ **Fail**: Check logs with `railway logs`

---

#### **Test 2: MCP Tools Listing** ✅

```bash
curl -X POST https://your-project.up.railway.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/list"
  }'

# Expected: List of 9 tools
# 1. query_food_database
# 2. get_food_nutrition
# 3. get_food_statistics
# 4. query_professional_profile
# 5. get_skill_information
# 6. get_work_experience
# 7. get_education
# 8. get_certifications
# 9. get_projects
```

✅ **Pass**: All 9 tools listed  
❌ **Fail**: Check environment variables

---

#### **Test 3: Food RAG Query** 🍛

```bash
curl -X POST https://your-project.up.railway.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "query_food_database",
      "arguments": {
        "question": "What is Biryani and how is it prepared?"
      }
    }
  }'

# Expected: Detailed AI response about Biryani
# - Ingredients (rice, meat, spices)
# - Origin (Hyderabad, India)
# - Cooking method (layered, dum-cooked)
# - Regional variations
```

✅ **Pass**: Detailed food information  
❌ **Fail**: Check Upstash credentials

---

#### **Test 4: Digital Twin Query** 👤 (This is the key test!)

```bash
curl -X POST https://your-project.up.railway.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "query_professional_profile",
      "arguments": {
        "question": "What are my Excel skills and experience?"
      }
    }
  }'

# Expected: Response about Excel Level 5 proficiency
# - Advanced formulas (INDEX-MATCH, array formulas)
# - Pivot tables and data modeling
# - Macros and VBA automation
# - Experience with large datasets
```

✅ **Pass**: Python script executed, profile data returned (THIS PROVES RAILWAY WORKS!)  
❌ **Fail on Vercel**: This would fail (no Python support)

---

#### **Test 5: Salary Expectations Query** 💰

```bash
curl -X POST https://your-project.up.railway.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "tools/call",
    "params": {
      "name": "query_professional_profile",
      "arguments": {
        "question": "What are my salary expectations for the Data Analyst role?"
      }
    }
  }'

# Expected Response:
# - Contract: $500-600 per day
# - Permanent: $55,000-70,000 annually
# - Open to negotiation based on role scope
```

✅ **Pass**: Salary expectations returned  
❌ **Fail**: Check Python script permissions

---

### **Step 10: Update Claude Desktop Configuration**

Once all tests pass, update Claude Desktop to use **Railway production URL**:

#### **Edit Claude Desktop Config**

```bash
# macOS
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use nano
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
        "https://your-project.up.railway.app/api/mcp"
      ]
    }
  }
}
```

**Replace** `https://your-project.up.railway.app` with **your actual Railway URL**

#### **Restart Claude Desktop**

```bash
# macOS - Quit completely
osascript -e 'quit app "Claude"'

# Wait 2 seconds
sleep 2

# Reopen Claude Desktop
open -a Claude
```

#### **Verify in Claude Desktop**

1. Open Claude Desktop
2. Look for MCP tools icon
3. You should see **9 tools** available:
   - 🍛 Food RAG (3): query_food_database, get_food_nutrition, get_food_statistics
   - 👤 Digital Twin (6): query_professional_profile, get_skill_information, get_work_experience, get_education, get_certifications, get_projects

4. **Test a query**: "What is Biryani?"
5. **Test digital twin**: "What are my Excel skills?"

✅ **Success**: Claude uses MCP tools to answer from your data!

---

## 🔧 Troubleshooting

### **Issue 1: Build Fails - "Cannot find module"**

**Error**: `Error: Cannot find module 'next'`

**Solution**:
```bash
# Verify package.json exists in mydigitaltwin/
ls /Users/DELL/ragfood/mydigitaltwin/package.json

# If missing root directory setting:
railway variables set ROOT_DIRECTORY=mydigitaltwin

# Redeploy
railway up --detach
```

---

### **Issue 2: Python Script Fails**

**Error**: `python3: command not found` or `vivian_profile_query.py: No such file`

**Solution**:

Railway auto-detects Python, but verify:

1. **Check Python files exist**:
   ```bash
   ls /Users/DELL/ragfood/vivian_profile_query.py
   ```

2. **Create Procfile** (if needed):
   ```bash
   cat > /Users/DELL/ragfood/Procfile << 'EOF'
   web: cd mydigitaltwin && npm start
   EOF
   ```

3. **Commit and push**:
   ```bash
   git add Procfile
   git commit -m "feat: add Procfile for Railway"
   git push origin cloud-migration
   ```

Railway will auto-redeploy!

---

### **Issue 3: Environment Variables Not Loading**

**Error**: `Missing UPSTASH_VECTOR_REST_URL`

**Solution**:
```bash
# List current variables
railway variables

# If missing, add them:
railway variables set UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
railway variables set UPSTASH_VECTOR_REST_TOKEN="your-token"
railway variables set GROQ_API_KEY="your-key"

# Restart service
railway restart
```

---

### **Issue 4: Port Binding Error**

**Error**: `EADDRINUSE: address already in use :::3000`

**Solution**:

Railway provides `PORT` environment variable automatically. Update your Next.js config:

```bash
# Check if package.json start script uses PORT
cat /Users/DELL/ragfood/mydigitaltwin/package.json | grep start

# Should be:
"start": "next start -p ${PORT:-3000}"
```

If needed:
```bash
# Update start script
railway variables set PORT=3000
railway restart
```

---

### **Issue 5: Health Check Fails**

**Error**: `Service unhealthy: health check timeout`

**Solution**:
```bash
# Increase timeout in railway.json
# Health check path must return 200 OK

# Test health check endpoint locally first:
curl http://localhost:3000/api/mcp

# If works locally, increase Railway timeout:
# Dashboard → Settings → Health Check Timeout → 300s
```

---

## 📊 Railway Dashboard Overview

### **Key Sections**

1. **Deployments**
   - View deployment history
   - Monitor build progress
   - Access logs

2. **Variables**
   - Manage environment variables
   - Add/edit/delete secrets

3. **Settings**
   - Configure root directory
   - Set build commands
   - Custom domains

4. **Metrics**
   - CPU usage
   - Memory usage
   - Network traffic

5. **Logs**
   - Real-time application logs
   - Build logs
   - Error logs

---

## 💰 Railway Pricing

### **Free Tier** (Hobby Plan)

✅ **$5/month credit** (covers basic usage)  
✅ **500 hours execution time** per month  
✅ **Unlimited projects**  
✅ **512MB RAM** per service  
✅ **1GB disk** per service  

**Estimated Cost for This Project**:
- Next.js app: ~$3-5/month (always running)
- Total: **Within free tier** if low traffic

### **Upgrade if Needed**

**Developer Plan**: $20/month
- $10 credit included
- More resources
- Priority support

**Link**: https://railway.app/pricing

---

## 🎯 Deployment Checklist

After Railway deployment completes:

- [ ] ✅ Health check passes (`/api/mcp` returns 200 OK)
- [ ] ✅ MCP tools listing returns 9 tools
- [ ] ✅ Food query works (Biryani test)
- [ ] ✅ **Digital twin query works** (Excel skills test) ⭐ **KEY DIFFERENCE FROM VERCEL**
- [ ] ✅ Salary expectations query works
- [ ] ✅ Claude Desktop config updated with Railway URL
- [ ] ✅ Claude Desktop restarted
- [ ] ✅ All 9 MCP tools visible in Claude Desktop
- [ ] ✅ Test queries in Claude Desktop work
- [ ] ✅ Monitor logs for errors
- [ ] ✅ Set up custom domain (optional)
- [ ] ✅ Enable auto-deploy from GitHub

---

## 🚀 Auto-Deploy Setup (Recommended)

Enable auto-deployment so every GitHub push deploys automatically:

### **Configure Auto-Deploy**

1. **Railway Dashboard** → Your Project
2. Click **"Settings"** → **"Service"**
3. Under **"Source"**, click **"Connect Repo"**
4. Select: `VivianP05/ragfood`
5. Select branch: `cloud-migration`
6. Enable: **"Auto-deploy on push"** ✅

### **Test Auto-Deploy**

```bash
# Make a small change
echo "# Railway Auto-Deploy Test" >> /Users/DELL/ragfood/README.md

# Commit and push
git add README.md
git commit -m "test: verify Railway auto-deploy"
git push origin cloud-migration

# Railway will automatically:
# 1. Detect the push
# 2. Start new deployment
# 3. Build and deploy
# 4. Notify you when complete
```

**Deployment Notifications**: Enable in Railway Settings → Notifications

---

## 📈 Monitoring Your Deployment

### **View Real-Time Logs**

```bash
# CLI - Stream logs
railway logs --follow

# Filter by type
railway logs --type build    # Build logs only
railway logs --type deploy   # Deployment logs only
railway logs --type app      # Application logs only
```

### **Check Service Health**

```bash
# CLI
railway status

# Expected output:
Service:    vivian-digital-twin-mcp
Status:     RUNNING
URL:        https://your-project.up.railway.app
Memory:     124MB / 512MB
CPU:        5%
```

### **Monitor Resource Usage**

Railway Dashboard → Metrics:
- **CPU**: Should be < 50% average
- **Memory**: Should be < 400MB
- **Network**: Monitor bandwidth usage

---

## 🎉 Success Criteria

Your Railway deployment is successful when:

✅ **Build**: Completes in < 3 minutes  
✅ **Health Check**: `/api/mcp` returns 200 OK  
✅ **All 9 Tools**: Listed in MCP response  
✅ **Food Queries**: Work in < 3 seconds  
✅ **Digital Twin Queries**: Work (Python executes) ⭐ **KEY**  
✅ **Claude Desktop**: Shows all 9 tools  
✅ **Uptime**: 99%+ (Railway SLA)  
✅ **Auto-Deploy**: GitHub pushes trigger deployments  

---

## 🔄 Next Steps After Deployment

### **1. Test Thoroughly**

```bash
# Test all 9 MCP tools
# Food RAG tools (3)
curl -X POST https://your-url/api/mcp -d '{"method":"tools/call","params":{"name":"query_food_database","arguments":{"question":"What is Biryani?"}}}'

# Digital Twin tools (6)
curl -X POST https://your-url/api/mcp -d '{"method":"tools/call","params":{"name":"query_professional_profile","arguments":{"question":"What are my skills?"}}}'
```

### **2. Custom Domain** (Optional)

```bash
# Add custom domain in Railway Dashboard
# Settings → Domains → Add Custom Domain
# Example: digitaltwin.yourname.com
```

### **3. Enable Monitoring**

- Railway Dashboard → Metrics
- Set up alerts for downtime
- Monitor resource usage

### **4. Interview Preparation**

Now that your digital twin is live:

✅ Use it for **Interview Simulation #2** (Technical Interview)  
✅ Query your professional profile during practice  
✅ Test STAR format responses  
✅ Demo your digital twin in actual interviews  

---

## 📞 Support & Resources

- **Railway Docs**: https://docs.railway.app/
- **Railway Discord**: https://discord.gg/railway
- **Railway Status**: https://status.railway.app/
- **Your Project**: https://github.com/VivianP05/ragfood

---

## ✅ Quick Command Reference

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd /Users/DELL/ragfood
railway init

# Set environment variables
railway variables set UPSTASH_VECTOR_REST_URL="your-url"
railway variables set UPSTASH_VECTOR_REST_TOKEN="your-token"
railway variables set GROQ_API_KEY="your-key"

# Deploy
railway up

# View logs
railway logs --follow

# Check status
railway status

# Restart service
railway restart

# Open dashboard
railway open
```

---

## 🎯 Comparison: Railway vs Vercel

| Feature | Railway ✅ | Vercel ❌ |
|---------|-----------|-----------|
| **Next.js** | ✅ Full support | ✅ Full support |
| **Python** | ✅ Full support | ❌ No support |
| **Food RAG (3 tools)** | ✅ Work | ✅ Work |
| **Digital Twin (6 tools)** | ✅ **Work** | ❌ **Fail** |
| **Auto-Deploy** | ✅ Yes | ✅ Yes |
| **Free Tier** | ✅ $5 credit | ✅ Generous |
| **Setup Complexity** | 🟡 Medium | 🟢 Easy |
| **Best For** | **Full MCP system** | Food RAG only |

**Verdict**: Railway is **required** for full digital twin functionality (9 tools)

---

**Last Updated**: November 4, 2025  
**Created by**: GitHub Copilot + Vivian Pham  
**Project**: Digital Twin MCP Server v3.0.0  
**Platform**: Railway (Full Python + Next.js Support)  

🚂 **Ready to deploy all 9 MCP tools? Let's go!**
