# ⚡ Vercel Deployment - Quick Start Guide

**Platform**: Vercel (Best for Next.js)  
**Working Tools**: 3/9 (Food RAG only - TypeScript-based)  
**Note**: Digital Twin tools (6) require Python - won't work on Vercel  
**Date**: November 4, 2025  

---

## 🎯 What Will Work on Vercel?

✅ **Food RAG Tools (3 tools)**:
- `query_food_database` - Query 200+ food items with AI
- `get_food_nutrition` - Get nutritional information
- `get_food_statistics` - Database statistics

❌ **Digital Twin Tools (6 tools)** - Require Python:
- `query_professional_profile` - Won't work (needs Python)
- `get_skill_information` - Won't work (needs Python)
- `get_work_experience` - Won't work (needs Python)
- `get_education` - Won't work (needs Python)
- `get_certifications` - Won't work (needs Python)
- `get_projects` - Won't work (needs Python)

**Solution**: We'll deploy to Vercel now for food queries, then migrate digital twin to TypeScript later if needed.

---

## 🚀 Vercel Deployment Steps

### **Step 1: Go to Vercel**

Open in browser: https://vercel.com/new

You'll need to:
1. Sign in with GitHub (recommended)
2. Authorize Vercel to access your repositories

---

### **Step 2: Import Your Repository**

1. **Click "Add New..." → "Project"**

2. **Import Git Repository**:
   - You'll see your GitHub repositories
   - Find: **"VivianP05/ragfood"**
   - Click **"Import"**

---

### **Step 3: Configure Project Settings** ⭐ CRITICAL

**Framework Preset**: Next.js ✅ (auto-detected)

**Root Directory**: ⚠️ **MUST SET THIS!**
```
Root Directory: mydigitaltwin
```

Click **"Edit"** next to Root Directory and type: `mydigitaltwin`

**Build and Output Settings**:
```
Framework:        Next.js (auto-detected)
Root Directory:   mydigitaltwin  ⭐ REQUIRED
Build Command:    npm run build  (auto-detected)
Output Directory: .next          (auto-detected)
Install Command:  npm install    (auto-detected)
```

---

### **Step 4: Add Environment Variables** ⭐ CRITICAL

Before clicking "Deploy", add these 3 environment variables:

Click **"Environment Variables"** section (expand if collapsed)

#### **Variable 1: UPSTASH_VECTOR_REST_URL**
```
Name:  UPSTASH_VECTOR_REST_URL
Value: https://free-loon-62438-us1-vector.upstash.io
```

#### **Variable 2: UPSTASH_VECTOR_REST_TOKEN**

You need to get this from your `.env.local` file.

**Your .env.local is already open in editor!** Copy the value after `UPSTASH_VECTOR_REST_TOKEN=`

```
Name:  UPSTASH_VECTOR_REST_TOKEN
Value: [Paste from your .env.local file]
```

#### **Variable 3: GROQ_API_KEY**

Also from your `.env.local` file:

```
Name:  GROQ_API_KEY
Value: [Paste from your .env.local file]
```

#### **Environment Selection**

For each variable, check:
- ✅ Production
- ✅ Preview (optional)
- ✅ Development (optional)

---

### **Step 5: Deploy!** 🚀

Once all configured:

1. **Review settings**:
   - ✅ Root Directory: `mydigitaltwin`
   - ✅ Framework: Next.js
   - ✅ Environment Variables: 3 added

2. **Click "Deploy"**

3. **Wait 1-2 minutes** for deployment to complete

---

## 🎉 After Deployment

You'll get a URL like: `https://ragfood-vivianp05.vercel.app`

Let me know your deployment URL and I'll help you:
1. Test the MCP endpoint
2. Verify food RAG queries work
3. Update Claude Desktop configuration
4. Test in Claude Desktop

---

## 📝 Important Notes

### **What Works**:
✅ Food queries: "What is Biryani?"
✅ Nutrition info: "Nutritional value of mangoes"
✅ Food statistics: "How many Indian dishes?"

### **What Won't Work** (Python required):
❌ Profile queries: "What are my Excel skills?"
❌ Salary expectations
❌ Work experience
❌ Education background

### **Future Migration**:
If you need digital twin tools on Vercel, we'll need to:
1. Rewrite Python RAG logic in TypeScript
2. Use Upstash Vector TypeScript SDK directly
3. Use Groq TypeScript SDK for AI generation

---

**Ready to deploy?** 

Follow the steps above in Vercel dashboard, then share your deployment URL with me!

---

**Last Updated**: November 4, 2025  
**Platform**: Vercel (Food RAG Only)  
**Repository**: VivianP05/ragfood
