# 🔐 Vercel Environment Variables - Copy & Paste Reference

**For Deployment**: Copy these values exactly into Vercel dashboard

---

## 📋 Environment Variables to Add in Vercel

### **Variable 1: UPSTASH_VECTOR_REST_URL**

```
Name:  UPSTASH_VECTOR_REST_URL
Value: https://free-loon-62438-us1-vector.upstash.io
```

**Environments**: ✅ Production, ✅ Preview, ✅ Development

---

### **Variable 2: UPSTASH_VECTOR_REST_TOKEN**

```
Name:  UPSTASH_VECTOR_REST_TOKEN
Value: ABMFMGZyZWUtbG9vbi02MjQzOC11czFhZG1pbk1qWTBaamhqTVRRdFkyVmxaUzAwTldKbUxUZzBNVFF0TXpBek5HVXdOR1V6TXpNdw==
```

**Environments**: ✅ Production, ✅ Preview, ✅ Development

---

### **Variable 3: GROQ_API_KEY**

```
Name:  GROQ_API_KEY
Value: [Get from your .env.local file - starts with "gsk_"]
```

**Environments**: ✅ Production, ✅ Preview, ✅ Development

---

## ✅ Vercel Configuration Checklist

Before clicking "Deploy", verify:

- [ ] **Root Directory**: `mydigitaltwin` (MUST be set!)
- [ ] **Framework**: Next.js (auto-detected)
- [ ] **Build Command**: `npm run build` (auto-detected)
- [ ] **Install Command**: `npm install` (auto-detected)
- [ ] **Environment Variable 1**: UPSTASH_VECTOR_REST_URL ✅
- [ ] **Environment Variable 2**: UPSTASH_VECTOR_REST_TOKEN ✅
- [ ] **Environment Variable 3**: GROQ_API_KEY ✅

---

## 🚀 Deployment Steps

1. **Go to**: https://vercel.com/new
2. **Sign in** with GitHub
3. **Import**: VivianP05/ragfood
4. **Set Root Directory**: `mydigitaltwin` ⭐
5. **Add 3 environment variables** (copy from above)
6. **Click "Deploy"** 🚀
7. **Wait ~2 minutes** for build to complete
8. **Copy your deployment URL** (e.g., https://ragfood-xyz.vercel.app)

---

## 🧪 After Deployment - Test MCP Endpoint

Once deployed, test your MCP server:

```bash
# Replace YOUR_URL with your actual Vercel deployment URL
curl https://YOUR_URL.vercel.app/api/mcp

# Expected Response:
{
  "status": "ok",
  "message": "Food RAG MCP Server is running",
  "version": "3.0.0",
  "tools": 9
}
```

✅ **Success**: You see JSON response with status "ok"

---

## 📱 Share Your Deployment URL

After deployment completes, you'll get a URL like:
- `https://ragfood-vivianp05.vercel.app`
- `https://ragfood-xyz123.vercel.app`

**Share it with me** so I can help you:
1. Test the MCP endpoint
2. Verify food queries work
3. Update Claude Desktop config
4. Test in Claude Desktop

---

## ⚠️ Important Reminder

**What Will Work**:
- ✅ Food RAG queries (3 tools)
- ✅ MCP server endpoints
- ✅ Next.js frontend

**What Won't Work** (requires Python):
- ❌ Digital twin profile queries
- ❌ Professional background questions
- ❌ Skill/experience queries

**Solution for Digital Twin**:
- Use Railway instead (supports Python), OR
- Migrate digital twin logic to TypeScript later

---

**Date**: November 4, 2025  
**Repository**: VivianP05/ragfood  
**Deployment**: Vercel (Food RAG Only)

🚀 **Ready to deploy!**
