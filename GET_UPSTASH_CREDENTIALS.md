# 🔑 How to Get Your Upstash Vector Credentials

## 🎯 Your Database Information

**Database Name:** `free-loon-62438`  
**Database URL:** `https://free-loon-62438-us1-vector.upstash.io`

---

## 📋 Step-by-Step: Get Your Credentials

### 1. Open Upstash Console
Go to: **https://console.upstash.com/vector**

### 2. Login to Your Account
Use your Upstash credentials

### 3. Click on Your Database
Click on: **"free-loon-62438"**

### 4. Find the "Connect" Tab
Look for tabs at the top:
- Details
- **Connect** ← Click this one
- Query
- Logs

### 5. Copy Your Credentials

You'll see something like this:

```bash
# REST API Credentials
UPSTASH_VECTOR_REST_URL=https://free-loon-62438-us1-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=AbYf1a2b3c4d5e6f7g8h9i0j... (long token)
```

**Copy both:**
- ✅ The URL (you already have this)
- ✅ The TOKEN (this is what you need!)

---

## 🔧 Update Your `.env` File

Once you have the token, run this command (replace YOUR_TOKEN_HERE):

```bash
cat > .env << 'EOF'
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="YOUR_TOKEN_HERE"
GROQ_API_KEY="your-groq-api-key-here"
EOF
```

**OR** manually edit `.env` file:
```bash
nano .env
```

Then paste:
```
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="YOUR_ACTUAL_TOKEN_FROM_CONSOLE"
GROQ_API_KEY="your-groq-api-key-here"
```

---

## ✅ After Updating

Once you've updated the `.env` file:

### 1. Test Connection
```bash
python3 -c "from upstash_vector import Index; from dotenv import load_dotenv; load_dotenv(); i = Index.from_env(); print('✅ Connected!'); info = i.info(); print(f'Vectors: {info.vector_count}')"
```

### 2. Upload Food Data
```bash
python3 upload_foods_to_upstash.py
```

### 3. Check Database
```bash
python3 check_upstash_database.py
```

---

## 🆘 Need Help?

If you can't find the token:
1. In the Upstash console
2. Click your database: `free-loon-62438`
3. Look for "REST API" section
4. Click "Show" or "Copy" button next to the token

The token usually starts with: `AByf`, `ABz`, or similar

---

## 📸 Visual Guide

In the Upstash Console, you should see:

```
┌─────────────────────────────────────────────┐
│ free-loon-62438                             │
├─────────────────────────────────────────────┤
│ Tabs: [Details] [Connect] [Query] [Logs]   │
├─────────────────────────────────────────────┤
│                                             │
│ REST API Credentials:                       │
│                                             │
│ Endpoint:                                   │
│ https://free-loon-62438-us1-vector.upstash  │
│                                             │
│ Token:                                      │
│ AByf... [Copy]                             │
│                                             │
└─────────────────────────────────────────────┘
```

Click the **[Copy]** button to copy your token!

---

## 🎯 Quick Summary

**What you need:**
1. ✅ URL: `https://free-loon-62438-us1-vector.upstash.io` (you have this!)
2. ❓ TOKEN: Get from console → Connect tab → Copy token

**What to do:**
1. Open console: https://console.upstash.com/vector
2. Click: free-loon-62438
3. Click: Connect tab
4. Copy: The token
5. Update: `.env` file with the token
6. Run: `python3 upload_foods_to_upstash.py`

**Once I have your token, I can help you update the file!** 🚀
