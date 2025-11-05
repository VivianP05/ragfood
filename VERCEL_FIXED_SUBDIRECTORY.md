# 🔧 Vercel Setup - FIXED for Subdirectory

**Issue**: Vercel doesn't show `mydigitaltwin` option in Root Directory  
**Solution**: Added `vercel.json` configuration file ✅  
**Status**: Configuration pushed to GitHub (commit 7d6c14b)  

---

## ✅ What I Just Fixed

I created a `vercel.json` file in your repository that tells Vercel:
- Your Next.js app is in the `mydigitaltwin` subdirectory
- How to build and deploy from that subdirectory

This file is now pushed to GitHub, so Vercel will automatically detect it!

---

## 🚀 New Deployment Steps (SIMPLIFIED)

### **Option 1: Re-import Repository** (Recommended - Easiest)

If you're still on the Vercel import page:

1. **Cancel/Go back** if you already started importing
2. **Click "Add New..." → "Project"** again
3. **Import "VivianP05/ragfood"** again
4. **This time Vercel should auto-detect** the `vercel.json` configuration!

**You'll see**:
- ✅ Framework: Next.js (auto-detected)
- ✅ Build settings: Already configured via vercel.json
- ✅ **NO NEED to manually set Root Directory!**

---

### **Option 2: If Already Started Deploying**

If you already clicked "Deploy":

1. **Let it fail** (it will fail without proper config)
2. **Go to Project Settings** after failed deployment
3. Vercel will **auto-detect the new vercel.json**
4. **Click "Redeploy"**

---

## 📝 Environment Variables (STILL REQUIRED)

Even with `vercel.json`, you **still need** to add these 3 environment variables:

### **In Vercel Dashboard → Environment Variables**

**Variable 1:**
```
Name:  UPSTASH_VECTOR_REST_URL
Value: https://free-loon-62438-us1-vector.upstash.io
```

**Variable 2:**
```
Name:  UPSTASH_VECTOR_REST_TOKEN
Value: ABMFMGZyZWUtbG9vbi02MjQzOC11czFhZG1pbk1qWTBaamhqTVRRdFkyVmxaUzAwTldKbUxUZzBNVFF0TXpBek5HVXdOR1V6TXpNdw==
```

**Variable 3:**
```
Name:  GROQ_API_KEY
Value: [Get from your .env.local file]
```

**For each variable**: Check ✅ Production

---

## 🎯 What the vercel.json Does

```json
{
  "buildCommand": "cd mydigitaltwin && npm install && npm run build",
  "devCommand": "cd mydigitaltwin && npm run dev",
  "installCommand": "cd mydigitaltwin && npm install",
  "framework": "nextjs",
  "outputDirectory": "mydigitaltwin/.next"
}
```

This tells Vercel:
- 📁 Your app is in `mydigitaltwin/` subdirectory
- 🔨 How to build: `cd mydigitaltwin && npm run build`
- 📦 Where output is: `mydigitaltwin/.next`
- ⚡ Framework: Next.js

---

## ✅ Simplified Steps Now

### **Step 1: Go to Vercel**
https://vercel.com/new

### **Step 2: Import Repository**
- Click "Import" next to **VivianP05/ragfood**

### **Step 3: Vercel Auto-Detects Configuration**
You should see:
- ✅ Framework: Next.js ✅
- ✅ Build Command: Configured via vercel.json ✅
- ✅ Install Command: Configured via vercel.json ✅
- ✅ Output Directory: Configured via vercel.json ✅

**No manual Root Directory needed!** 🎉

### **Step 4: Add Environment Variables** ⭐
Expand "Environment Variables" and add the 3 variables above

### **Step 5: Deploy!** 🚀
Click the big blue "Deploy" button

---

## 🧪 After Deployment

Once deployed, you'll get a URL like:
```
https://ragfood-vivianp05.vercel.app
```

**Test it**:
```bash
curl https://YOUR_URL.vercel.app/api/mcp

# Expected:
{
  "status": "ok",
  "message": "Food RAG MCP Server is running",
  "version": "3.0.0",
  "tools": 9
}
```

---

## 🎉 What This Means

✅ **No more manual Root Directory configuration**  
✅ **Vercel auto-detects everything from vercel.json**  
✅ **Simpler deployment process**  
✅ **Can redeploy anytime from GitHub**  

---

## 🔄 If You Already Started

**If you're in the middle of deployment**:

1. **Cancel current deployment** (if still configuring)
2. **Start fresh**: Click "Add New Project" again
3. **Import VivianP05/ragfood** again
4. **Vercel will now see vercel.json** ✅
5. **Add environment variables**
6. **Deploy!**

---

## 📞 Next Steps

1. **Try importing again** in Vercel
2. **Add the 3 environment variables**
3. **Click Deploy**
4. **Share your deployment URL** with me!

Then I'll help you:
- Test the MCP endpoint
- Update Claude Desktop config
- Verify everything works

---

**Fixed**: November 4, 2025  
**Commit**: 7d6c14b  
**Configuration**: vercel.json added ✅

🚀 **Try deploying again now!**
