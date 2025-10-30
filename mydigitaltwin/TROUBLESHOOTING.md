# Troubleshooting Guide - Food RAG MCP Server

## 🐛 Common Issues & Solutions

### 1. TypeScript Type Errors

#### Issue: Property 'metadata' does not exist on type 'QueryResult'

**Error:**
```typescript
Property 'metadata' does not exist on type 'QueryResult<Record<string, unknown>>'
```

**Solution:**
The @upstash/vector SDK types are correct. Use proper type assertion:

```typescript
// ✅ CORRECT - Cast metadata to Record
const metadata = result.metadata as Record<string, any>;
const name = metadata.name || metadata.text;
```

**Already Fixed In:**
- `src/actions/foodRagActions.ts` (line 63)
- `src/mcp-server/index.ts` (line 157)

---

### 2. Environment Variable Issues

#### Issue: UPSTASH_VECTOR_REST_URL is undefined

**Error:**
```
Error: Missing required environment variables
```

**Checklist:**
- [x] ✅ `.env.local` exists in `mydigitaltwin/` directory
- [x] ✅ Variables are properly quoted
- [x] ✅ No trailing spaces
- [x] ✅ File is loaded by Next.js

**Verify:**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
cat .env.local
```

**Expected Output:**
```bash
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="YOUR_TOKEN_HERE"
GROQ_API_KEY="YOUR_KEY_HERE"
```

**If Missing:**
```bash
# Copy from parent .env
cp ../.env .env.local

# Or create new:
echo 'UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"' > .env.local
echo 'UPSTASH_VECTOR_REST_TOKEN="your-token"' >> .env.local
echo 'GROQ_API_KEY="your-key"' >> .env.local
```

---

### 3. MCP Protocol Errors

#### Issue: Invalid MCP response format

**Error:**
```
Error: MCP response does not match schema
```

**Solution:**
Ensure response follows MCP specification:

```typescript
// ✅ CORRECT MCP Response Format
return {
  content: [
    {
      type: "text",
      text: answer  // Must be a string
    }
  ]
};

// ❌ INCORRECT - Missing content wrapper
return { text: answer };

// ❌ INCORRECT - Wrong type
return {
  content: [
    {
      type: "json",  // Should be "text" for string responses
      data: answer
    }
  ]
};
```

**Already Implemented:**
- `src/mcp-server/index.ts` (lines 176, 204, 239, 267)

**Reference:**
- Roll dice pattern: https://github.com/gocallum/rolldice-mcpserver.git
- MCP spec: https://spec.modelcontextprotocol.io/

---

### 4. Server Action Errors

#### Issue: Server actions must be async functions

**Error:**
```
Error: Server actions must be async functions
```

**Solution:**
Add `"use server"` directive and ensure async/await:

```typescript
// ✅ CORRECT - At top of file
"use server";

import { Index } from "@upstash/vector";

export async function queryFoodRAG(question: string) {
  // ... async implementation
}

// ❌ INCORRECT - Missing "use server"
import { Index } from "@upstash/vector";

export function queryFoodRAG(question: string) {
  // ... sync implementation
}
```

**Already Fixed:**
- `src/actions/foodRagActions.ts` (line 1)

---

### 5. Dependency Issues

#### Issue: Module '@upstash/vector' not found

**Error:**
```
Error: Cannot find module '@upstash/vector'
```

**Solution:**

**For This Project (uses npm, NOT pnpm):**
```bash
cd /Users/DELL/ragfood/mydigitaltwin
npm install @upstash/vector groq-sdk @modelcontextprotocol/sdk
```

**Verify Installation:**
```bash
npm list @upstash/vector groq-sdk @modelcontextprotocol/sdk
```

**Expected Output:**
```
mydigitaltwin@0.1.0
├── @modelcontextprotocol/sdk@1.20.2
├── @upstash/vector@1.2.2
└── groq-sdk@0.34.0
```

**If Still Not Found:**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

---

### 6. Import Path Errors

#### Issue: Cannot find module '@/src/actions/foodRagActions'

**Error:**
```
Module not found: Can't resolve '@/src/actions/foodRagActions'
```

**Solution:**
Use relative paths from app directory:

```typescript
// ✅ CORRECT - Relative path
import { queryFoodRAG } from '../../../src/actions/foodRagActions';

// ❌ INCORRECT - @ alias doesn't work for src/
import { queryFoodRAG } from '@/src/actions/foodRagActions';
```

**Already Fixed:**
- `app/api/query/route.ts` (line 2)

---

### 7. Build Errors

#### Issue: MCP server build fails

**Error:**
```
error TS2307: Cannot find module '@modelcontextprotocol/sdk/server/index.js'
```

**Solution:**
Ensure tsconfig.mcp.json is configured correctly:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "esModuleInterop": true
  },
  "include": ["src/mcp-server/**/*"]
}
```

**Build Command:**
```bash
npm run build:mcp
```

**Already Configured:**
- `tsconfig.mcp.json`

---

### 8. Runtime Errors

#### Issue: Groq API rate limit exceeded

**Error:**
```
Error: Rate limit exceeded. Please try again later.
```

**Solution:**
```typescript
// Add retry logic with exponential backoff
async function queryWithRetry(fn: () => Promise<any>, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.message.includes('rate limit') && i < retries - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        continue;
      }
      throw error;
    }
  }
}
```

**Temporary Solution:**
- Wait 60 seconds between requests
- Check Groq dashboard: https://console.groq.com/

---

### 9. Claude Desktop Integration Issues

#### Issue: MCP server not appearing in Claude Desktop

**Checklist:**
1. ✅ MCP server is built: `npm run build:mcp`
2. ✅ Config file exists: `~/Library/Application Support/Claude/claude_desktop_config.json`
3. ✅ Config has valid JSON (no trailing commas)
4. ✅ Absolute paths used (not relative)
5. ✅ Claude Desktop restarted after config changes

**Verify Config:**
```bash
# Check file exists
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Validate JSON
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Correct Config:**
```json
{
  "mcpServers": {
    "food-rag": {
      "command": "node",
      "args": ["/Users/DELL/ragfood/mydigitaltwin/dist/mcp-server/index.js"],
      "env": {
        "UPSTASH_VECTOR_REST_URL": "https://free-loon-62438-us1-vector.upstash.io",
        "UPSTASH_VECTOR_REST_TOKEN": "your-token",
        "GROQ_API_KEY": "your-key"
      }
    }
  }
}
```

**Debug:**
```bash
# Test MCP server standalone
cd /Users/DELL/ragfood/mydigitaltwin
npm run mcp

# Should output:
# 🚀 Starting Food RAG MCP Server...
# ✅ Server ready for connections
```

---

### 10. Next.js Dev Server Issues

#### Issue: Port 3000 already in use

**Error:**
```
Error: Port 3000 is already in use
```

**Solution:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

---

## 🔍 Debugging Commands

### Check Project Status
```bash
cd /Users/DELL/ragfood/mydigitaltwin

# Check environment variables
cat .env.local

# Check dependencies
npm list @upstash/vector groq-sdk @modelcontextprotocol/sdk

# Check TypeScript errors
npx tsc --noEmit

# Check MCP build
npm run build:mcp
ls -la dist/mcp-server/
```

### Test Individual Components
```bash
# Test Upstash connection
node -e "
const { Index } = require('@upstash/vector');
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN
});
console.log('Connected!');
"

# Test Groq connection
node -e "
const Groq = require('groq-sdk').default;
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
console.log('Connected!');
"
```

---

## ✅ Verification Checklist

Before running the system, verify:

- [ ] `.env.local` exists with all variables
- [ ] Dependencies installed: `npm list`
- [ ] MCP server built: `ls dist/mcp-server/index.js`
- [ ] No TypeScript errors: `npx tsc --noEmit`
- [ ] Server actions have `"use server"`
- [ ] Import paths are correct
- [ ] Port 3000 is available

---

## 🚀 Quick Fix Commands

### Full Reset & Rebuild
```bash
cd /Users/DELL/ragfood/mydigitaltwin

# Clean everything
rm -rf node_modules package-lock.json dist .next

# Reinstall
npm install

# Rebuild MCP
npm run build:mcp

# Start dev server
npm run dev
```

### Fix TypeScript Errors
```bash
# Check for errors
npx tsc --noEmit

# If errors, rebuild
npm run build:mcp
```

### Fix Environment Variables
```bash
# Verify .env.local
cat .env.local

# If missing, copy from parent
cp ../.env .env.local

# Restart dev server
pkill -f "next dev"
npm run dev
```

---

## 📚 Additional Resources

- **Project Docs:** `MCP_IMPLEMENTATION.md`
- **Setup Guide:** `MCP_SERVER_SETUP.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **MCP Spec:** https://spec.modelcontextprotocol.io/
- **Upstash Docs:** https://upstash.com/docs/vector
- **Groq Docs:** https://console.groq.com/docs

---

## 🆘 Still Having Issues?

1. Check this file first: `TROUBLESHOOTING.md`
2. Review error logs: Check terminal output
3. Verify file structure matches `MCP_IMPLEMENTATION.md`
4. Test web UI first (simpler than MCP)
5. Check GitHub issues: https://github.com/VivianP05/ragfood/issues

---

**Last Updated:** October 30, 2025  
**Status:** All known issues documented with solutions ✅
