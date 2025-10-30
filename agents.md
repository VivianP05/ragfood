# 🤖 Agents Guide - Food RAG System

## 📋 Table of Contents

1. [Project Architecture & Technical Constraints](#project-architecture--technical-constraints)
2. [Reference Links & Code Examples](#reference-links--code-examples)
3. [Project Overview](#project-overview)
4. [System Architecture](#system-architecture)
5. [Agent Instructions](#agent-instructions)
6. [Development Workflow](#development-workflow)
7. [GitHub MCP Integration](#github-mcp-integration)
8. [Deployment Guide](#deployment-guide)
9. [Troubleshooting](#troubleshooting)

---

## 🏛️ Project Architecture & Technical Constraints

### Food RAG System - Your Project

**Goal**: Build a full-stack Retrieval-Augmented Generation (RAG) system for food queries that provides intelligent, AI-powered responses about cuisines, dishes, and recipes using Upstash Vector Database and Groq AI.

**Your Repository**: https://github.com/VivianP05/ragfood

### Reference Repositories

#### Pattern Reference
- **Repository**: https://github.com/gocallum/rolldice-mcpserver.git
- **Purpose**: MCP server architecture pattern - reference for building MCP servers
- **Key Learnings**: MCP server architecture, request/response patterns, server actions

#### Logic Reference
- **Repository**: https://github.com/gocallum/binal_digital-twin_py.git
- **Purpose**: Python RAG implementation reference using Upstash Vector + Groq
- **Key Learnings**: RAG implementation, vector search logic, AI generation patterns

### Core Functionality Requirements

1. **Food Query System Capabilities**
   - Accept user questions about food, cuisines, recipes, and dietary information
   - Search Upstash Vector database with 200+ food items
   - Return semantically relevant food information with AI-generated responses
   - Support both CLI and web interfaces

2. **Database Schema**
   Your Upstash Vector database contains food items with this structure:
   ```json
   {
     "id": "1-110",
     "text": "Food description",
     "region": "Geographic origin (e.g., Hyderabad, Tropical, Global)",
     "type": "Category (e.g., Main Course, Fruit, Spice, Dessert)"
   }
   ```
   
   Or detailed format:
   ```json
   {
     "id": "91-110",
     "name": "Dish name",
     "category": "Food category",
     "origin": "Country/region",
     "description": "Detailed description",
     "ingredients": "List of ingredients",
     "cooking_method": "Preparation method",
     "dietary_tags": "e.g., Vegetarian, Vegan"
   }
   ```

3. **Search Logic Alignment**
   - Vector search with `top_k=3` for optimal results
   - Metadata includes: text, region, type, name, category, origin
   - Cosine similarity scoring with mxbai-embed-large-v1 model
   - Preserve embedding and retrieval patterns across Python and TypeScript

### Technical Stack & Constraints

#### Framework & Tooling
```typescript
// YOUR PROJECT VERSIONS
Next.js: 16.0.1 (currently installed)
React: 19.2.0
Package Manager: npm (project uses npm, not pnpm)
Commands: macOS/zsh (NOT Windows PowerShell)
TypeScript: 5+ with strict type safety
Platform: macOS (not Windows)
```

**Important Note**: This project was initialized with `npm`, so continue using npm for consistency. The original constraint about pnpm and PowerShell was from the reference project.

#### Architecture Patterns
- ✅ **Server Actions**: Use server actions wherever possible
- ✅ **Type Safety**: Enforce strong TypeScript type safety throughout
- ✅ **Styling**: Use `globals.css` instead of inline styling
- ✅ **UI Framework**: ShadCN with dark mode theme
- ✅ **Priority**: MCP functionality > UI (UI is primarily for MCP server configuration)

### Environment Variables

**File**: `.env` (project root) and `mydigitaltwin/.env.local` (Next.js root)

**Your Actual Configuration**:
```bash
# Root .env file (for Python scripts)
# ⚠️  IMPORTANT: Get your actual credentials from /Users/DELL/ragfood/.env (not committed to git)
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="your-token-here"  # Get from .env file
GROQ_API_KEY="your-groq-api-key-here"  # Get from .env file
```

**Upstash Database Details**:
- **Database Name**: free-loon-62438
- **Region**: us1 (US East)
- **Vector Count**: 200 vectors
- **Dimensions**: 1024
- **Embedding Model**: mxbai-embed-large-v1
- **Similarity**: COSINE
- **Current Data**: 110 food items + 90 other vectors

**Groq Model**:
- **Model**: llama-3.1-8b-instant
- **Temperature**: 0.7
- **Max Tokens**: 500

**Security Notes**:
- ✅ `.env` and `.env.local` are gitignored
- ✅ Never commit these files to git
- ✅ Always use environment variables for secrets
- ✅ Tokens are already configured correctly

### Setup Commands

#### Initial Setup (macOS/zsh)
```bash
# Clone YOUR repository
git clone https://github.com/VivianP05/ragfood.git
cd ragfood

# Python dependencies (already installed)
pip install python-dotenv upstash-vector groq

# Next.js setup
cd mydigitaltwin
npm install

# Run development server
npm run dev
```

#### ShadCN Installation (if needed)
```bash
npx shadcn@latest init
```

**Reference**: https://ui.shadcn.com/docs/installation/next

#### Project Structure
```
/Users/DELL/ragfood/
├── mydigitaltwin/          # Next.js app (port 3000)
├── rag_api.py              # Python API wrapper
├── rag_food_query.py       # CLI query system
├── digital_twin_rag.py     # Advanced RAG
├── data/foods.json         # 110 food items
├── .env                    # Environment variables
└── agents.md              # This file!
```

---

## 📚 Reference Links & Code Examples

### Upstash Vector Integration

#### Official Documentation
1. **Getting Started**: https://upstash.com/docs/vector/overall/getstarted
2. **Embedding Models**: https://upstash.com/docs/vector/features/embeddingmodels
3. **TypeScript SDK**: https://upstash.com/docs/vector/sdks/ts/getting-started
4. **REST API**: https://upstash.com/docs/vector/api/get-started

#### TypeScript Implementation Example (Your Food RAG)

```typescript
import { Index } from "@upstash/vector";

// Initialize index with YOUR environment variables
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

// Search for food items (top_k=3 for best results)
const results = await index.query({
  data: "What is Biryani?",  // User's food query
  topK: 3,
  includeMetadata: true,
});

// Process food results
results.forEach((result) => {
  console.log(`Food: ${result.metadata?.text || result.metadata?.name}`);
  console.log(`Region: ${result.metadata?.region || result.metadata?.origin}`);
  console.log(`Type: ${result.metadata?.type || result.metadata?.category}`);
  console.log(`Relevance: ${result.score}`);
});
```

#### Server Action Example (Your Food RAG System)

```typescript
"use server";

import { Index } from "@upstash/vector";
import { Groq } from "groq-sdk";

export async function queryFoodRAG(question: string) {
  // Initialize Upstash Vector (YOUR database: free-loon-62438)
  const index = new Index({
    url: process.env.UPSTASH_VECTOR_REST_URL!,
    token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
  });

  // Search for relevant food items (top_k=3)
  const results = await index.query({
    data: question,
    topK: 3,
    includeMetadata: true,
  });

  // Extract food context (handle both data formats)
  const context = results
    .map((r) => {
      const text = r.metadata?.text || 
                   `${r.metadata?.name}: ${r.metadata?.description}`;
      const region = r.metadata?.region || r.metadata?.origin || "Unknown";
      const type = r.metadata?.type || r.metadata?.category || "Food";
      return `${text} (${type} from ${region})`;
    })
    .join("\n\n");

  // Generate response with Groq (YOUR model: llama-3.1-8b-instant)
  const groq = new Groq({
    apiKey: process.env.GROQ_API_KEY!,
  });

  const completion = await groq.chat.completions.create({
    messages: [
      {
        role: "system",
        content: "You are a helpful food expert assistant. Use the provided food information to answer questions about cuisines, dishes, recipes, and dietary information accurately and enthusiastically.",
      },
      {
        role: "user",
        content: `Food Database Context:\n${context}\n\nQuestion: ${question}`,
      },
    ],
    model: "llama-3.1-8b-instant",
    temperature: 0.7,
    max_tokens: 500,
  });

  return completion.choices[0]?.message?.content || "No response generated.";
}
```

### Groq AI Integration

#### Official Documentation
1. **Groq Console**: https://console.groq.com/
2. **API Documentation**: https://console.groq.com/docs
3. **Quickstart**: https://console.groq.com/docs/quickstart
4. **Models**: https://console.groq.com/docs/models

#### TypeScript Implementation

```typescript
import Groq from "groq-sdk";

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY!,
});

async function generateResponse(prompt: string, context: string) {
  const chatCompletion = await groq.chat.completions.create({
    messages: [
      {
        role: "system",
        content: "You are a digital twin assistant with expertise in professional profiles.",
      },
      {
        role: "user",
        content: `${context}\n\nQuestion: ${prompt}`,
      },
    ],
    model: "llama-3.1-8b-instant",
    temperature: 0.7,
    max_tokens: 500,
    top_p: 1,
    stream: false,
  });

  return chatCompletion.choices[0]?.message?.content;
}
```

### Model Context Protocol (MCP)

#### Official Resources
1. **MCP Documentation**: https://modelcontextprotocol.io/
2. **MCP Specification**: https://spec.modelcontextprotocol.io/
3. **GitHub MCP Tools**: https://github.com/modelcontextprotocol

#### MCP Server Structure (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Create MCP server
const server = new Server(
  {
    name: "digital-twin-rag",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tool for RAG query
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query_digital_twin",
        description: "Query the digital twin's professional background using RAG",
        inputSchema: {
          type: "object",
          properties: {
            question: {
              type: "string",
              description: "Question about the person's professional background",
            },
          },
          required: ["question"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_digital_twin") {
    const question = request.params.arguments?.question as string;
    const answer = await queryDigitalTwin(question);
    
    return {
      content: [
        {
          type: "text",
          text: answer,
        },
      ],
    };
  }
  
  throw new Error("Tool not found");
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

### Next.js 15+ & ShadCN

#### Official Documentation
1. **Next.js**: https://nextjs.org/docs
2. **Server Actions**: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
3. **ShadCN**: https://ui.shadcn.com/
4. **Theming**: https://ui.shadcn.com/docs/theming

#### ShadCN Component Example

```typescript
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function ChatInterface() {
  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Digital Twin Assistant</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input 
            placeholder="Ask about professional background..." 
            className="w-full"
          />
          <Button className="w-full">Send Query</Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Package Management

#### NPM Commands (Your Project Uses npm)

```bash
# Install dependencies
npm install

# Add package
npm install <package-name>

# Add dev dependency
npm install --save-dev <package-name>

# Remove package
npm uninstall <package-name>

# Run scripts
npm run dev       # Development server
npm run build     # Production build
npm start         # Start production server
npm run lint      # Run linter

# Update packages
npm update        # Update all packages
npm update <pkg>  # Update specific package
```

**Note**: This project uses `npm` (not pnpm or yarn) based on your package.json and package-lock.json. The reference project uses pnpm, but yours uses npm.

### Type Safety Best Practices

```typescript
// Define strict types for RAG results
interface RAGResult {
  score: number;
  metadata: {
    text: string;
    source?: string;
    timestamp?: string;
  };
}

// Use type guards
function isValidRAGResult(result: unknown): result is RAGResult {
  return (
    typeof result === "object" &&
    result !== null &&
    "score" in result &&
    "metadata" in result
  );
}

// Server action with strict typing
export async function queryWithValidation(
  question: string
): Promise<{ success: true; answer: string } | { success: false; error: string }> {
  try {
    if (!question || question.trim().length === 0) {
      return { success: false, error: "Question cannot be empty" };
    }

    const answer = await queryDigitalTwin(question);
    return { success: true, answer };
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error.message : "Unknown error" 
    };
  }
}
```

### Additional Useful Resources

#### Development & Testing
- **Vercel Deployment**: https://vercel.com/docs
- **Next.js Deployment**: https://nextjs.org/docs/deployment
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **Tailwind CSS**: https://tailwindcss.com/docs

#### AI & Vector Search
- **Upstash Blog**: https://upstash.com/blog
- **Groq Cookbook**: https://github.com/groq/groq-cookbook
- **LangChain TypeScript**: https://js.langchain.com/docs/

#### MCP Protocol
- **MCP GitHub**: https://github.com/modelcontextprotocol
- **MCP Examples**: https://github.com/modelcontextprotocol/servers
- **MCP Quickstart**: https://modelcontextprotocol.io/quickstart

---

## 🎯 Project Overview

### What is This Project?

A **full-stack Retrieval-Augmented Generation (RAG) system** for food queries that combines:
- **Backend**: Python with Upstash Vector DB + Groq AI
- **Frontend**: Next.js 16 with TypeScript and Tailwind CSS
- **Integration**: RESTful API connecting Python RAG to Next.js
- **Version Control**: GitHub with MCP-enabled workflow

### Key Features

- ✅ 200+ food items in vector database
- ✅ Semantic search with AI-powered responses
- ✅ Dual interface: CLI and Web
- ✅ Real-time chat with message history
- ✅ GitHub MCP integration for seamless development

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Web Browser (localhost:3000)    Terminal (CLI)            │
│         │                              │                    │
│         ▼                              ▼                    │
│  ┌──────────────┐            ┌──────────────────┐         │
│  │  Next.js App │            │  Python CLI      │         │
│  │  page.tsx    │            │  rag_food_query  │         │
│  └──────┬───────┘            └──────────────────┘         │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                          │
│  │  API Route   │                                          │
│  │  /api/query  │                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────┐                 │
│  │     Python RAG API (rag_api.py)      │                 │
│  │  • Receives JSON requests            │                 │
│  │  • Queries Upstash Vector DB         │                 │
│  │  • Generates AI responses via Groq   │                 │
│  │  • Returns JSON responses            │                 │
│  └──────┬───────────────────────────────┘                 │
│         │                                                   │
│    ┌────┴────┐                                             │
│    ▼         ▼                                             │
│ ┌──────┐  ┌──────┐                                        │
│ │Upstash│  │ Groq │                                        │
│ │Vector │  │  AI  │                                        │
│ │  DB   │  │ LLM  │                                        │
│ └───────┘  └──────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

External Services:
- Upstash Vector: free-loon-62438 (200 vectors, 1024 dimensions)
- Groq: llama-3.1-8b-instant (fast inference)
- GitHub: VivianP05/ragfood (version control)
```

---

## 🤖 Agent Instructions

### For AI Coding Assistants (GitHub Copilot, etc.)

When working with this project, follow these guidelines:

#### 1. Understanding the Codebase

**Key Files to Know:**
- `mydigitaltwin/app/page.tsx` - Main chat UI component
- `mydigitaltwin/app/api/query/route.ts` - API endpoint for Python integration
- `rag_api.py` - JSON API wrapper for RAG system
- `rag_food_query.py` - Interactive CLI RAG system
- `digital_twin_rag.py` - Advanced RAG with detailed feedback
- `upload_foods_to_upstash.py` - Database population script
- `check_upstash_database.py` - Database inspection tool

**Data Flow:**
1. User inputs question in Next.js UI
2. Frontend sends POST to `/api/query`
3. API route executes Python script via child_process
4. Python queries Upstash Vector for relevant food items
5. Python sends context to Groq for AI generation
6. Response flows back through stack to user

#### 2. Code Modification Guidelines

**When Adding New Features:**

```markdown
1. ✅ Read existing code structure first
2. ✅ Maintain TypeScript types in Next.js
3. ✅ Keep Python functions modular and testable
4. ✅ Update documentation when changing APIs
5. ✅ Test both CLI and web interfaces
6. ✅ Commit with conventional commit messages
```

**Commit Message Convention:**
```bash
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Code formatting (no logic change)
refactor: Code restructuring (no behavior change)
test: Add or update tests
chore: Maintenance tasks
perf: Performance improvements
```

#### 3. Environment Variables

**Required in `.env` and `mydigitaltwin/.env.local`:**
```bash
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="your-token-here"
GROQ_API_KEY="your-groq-key-here"
```

**Never commit these files!** They are gitignored.

#### 4. Testing Protocol

**Before Committing:**
```bash
# Test Python API
python3 rag_api.py "What is Biryani?"

# Test CLI
python3 rag_food_query.py

# Test Next.js (in separate terminal)
cd mydigitaltwin
npm run dev
# Visit http://localhost:3000 and test queries
```

**Expected Results:**
- Python API: JSON response with `success: true`
- CLI: Interactive chat with emoji output
- Web: Chat UI with real-time responses

#### 5. Database Operations

**Check Database Status:**
```bash
python3 check_upstash_database.py
```

**Add More Food Data:**
1. Edit `data/foods.json` (if you have additional data)
2. Run: `python3 upload_foods_to_upstash.py`
3. Verify: `python3 check_upstash_database.py`

**Database Schema:**
```json
{
  "id": "unique-id",
  "text": "Food description",
  "region": "Geographic origin",
  "type": "Category (Main Course, Dessert, etc.)"
}
```

or

```json
{
  "id": "unique-id",
  "name": "Dish name",
  "category": "Food category",
  "origin": "Country/region",
  "description": "Detailed description",
  "ingredients": "List of ingredients",
  "cooking_method": "How it's prepared",
  "dietary_tags": "Vegetarian, Vegan, etc."
}
```

#### 6. API Response Format

**Python to Next.js:**
```json
{
  "success": true,
  "question": "What is Biryani?",
  "answer": "Biryani is a flavorful Indian rice dish..."
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "question": "Original question"
}
```

---

## 🔄 Development Workflow

### Daily Development Cycle

```bash
# 1. Start Development Server
cd mydigitaltwin
npm run dev
# Runs on http://localhost:3000

# 2. Make Changes
# Edit files in VS Code

# 3. Test Changes
# Test in browser or CLI

# 4. Check Git Status
git status

# 5. Stage Changes
git add .

# 6. Commit with Descriptive Message
git commit -m "feat: add new feature description"

# 7. Push to GitHub
git push origin cloud-migration

# 8. Optionally Create PR
# Use GitHub MCP or web interface
```

### Branch Strategy

**Main Branches:**
- `main` - Production-ready code
- `cloud-migration` - Active development (current)

**Feature Branches:**
```bash
# Create feature branch
git checkout -b feature/authentication

# Work on feature
git add .
git commit -m "feat: add user authentication"

# Push to GitHub
git push origin feature/authentication

# Create PR when ready
# GitHub MCP: "Create PR from feature/authentication to cloud-migration"
```

### Code Review Checklist

Before creating PR:
- [ ] All tests pass
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No console.log or print statements (unless intentional)
- [ ] Environment variables not hardcoded
- [ ] TypeScript types defined
- [ ] Error handling implemented
- [ ] Commit messages are clear

---

## 🔌 GitHub MCP Integration

### What is GitHub MCP?

**Model Context Protocol (MCP)** enables AI assistants to interact directly with GitHub, allowing natural language GitHub operations.

### Available Operations

#### Repository Management
```
"Show repository information"
"List all branches"
"Create a new repository called my-new-repo"
```

#### Branch Operations
```
"Create a new branch called feature/deployment"
"Switch to main branch"
"Delete branch old-feature"
"List all tags"
```

#### Pull Requests
```
"Create a pull request from cloud-migration to main"
"List open pull requests"
"Merge PR #5"
"Close PR #3"
```

#### File Operations
```
"Push this file to GitHub"
"Create file config.yaml on GitHub with content..."
"Update README.md on GitHub"
"Delete old-file.txt from GitHub"
```

#### Issues
```
"Create an issue for adding unit tests"
"List open issues"
"Close issue #10"
"Add comment to issue #5"
```

### GitHub MCP Best Practices

**DO:**
- ✅ Use clear, descriptive PR titles
- ✅ Review changes before pushing
- ✅ Test locally before creating PR
- ✅ Add meaningful commit messages
- ✅ Link issues to PRs

**DON'T:**
- ❌ Force push to main branch
- ❌ Push without testing
- ❌ Commit sensitive data
- ❌ Skip code review process
- ❌ Create PRs with failing tests

---

## 🚀 Deployment Guide

### Deploy to Vercel (Recommended)

#### Prerequisites
- GitHub account with repository
- Vercel account (free tier available)

#### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "feat: prepare for deployment"
git push origin cloud-migration
```

2. **Import to Vercel**
- Go to https://vercel.com
- Click "Import Project"
- Select your GitHub repository: `VivianP05/ragfood`
- Root directory: `mydigitaltwin`

3. **Configure Environment Variables**
Add in Vercel dashboard:
```
UPSTASH_VECTOR_REST_URL = your-upstash-url
UPSTASH_VECTOR_REST_TOKEN = your-upstash-token
GROQ_API_KEY = your-groq-key
```

4. **Deploy**
- Click "Deploy"
- Wait for build to complete
- Access your live URL!

### Deploy Python Backend (Optional)

If you want separate Python API:

**Railway:**
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

**Heroku:**
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create
git push heroku main
```

### Environment Setup for Production

**Vercel Environment Variables:**
- Go to Project Settings → Environment Variables
- Add all required variables
- Separate for Production/Preview/Development

**Security Checklist:**
- [ ] All API keys in environment variables
- [ ] `.env` files in `.gitignore`
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Error messages don't expose secrets

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Next.js API Returns 500 Error

**Symptoms:**
- API endpoint returns error
- Console shows Python execution failed

**Solutions:**
```bash
# Check Python script works
python3 rag_api.py "test query"

# Verify environment variables
cat mydigitaltwin/.env.local

# Check Python dependencies
pip list | grep -E "upstash|groq|dotenv"

# Restart Next.js server
cd mydigitaltwin
npm run dev
```

#### Issue 2: Python Script Returns Invalid JSON

**Symptoms:**
- API error: "Unexpected token"
- JSON parse error in console

**Solution:**
Ensure `rag_api.py` uses the clean version without emoji in JSON output. The current version is correct.

#### Issue 3: Database Connection Failed

**Symptoms:**
- Upstash connection errors
- Authentication failed messages

**Solutions:**
```bash
# Verify credentials
cat .env

# Test connection
python3 check_upstash_database.py

# If wrong database, update credentials
# Copy correct values from Upstash console
```

#### Issue 4: Git Push Rejected

**Symptoms:**
- Push fails with "rejected" message
- Branch diverged error

**Solutions:**
```bash
# Pull latest changes first
git pull origin cloud-migration

# If conflicts, resolve them
git status
# Edit conflicting files
git add .
git commit -m "fix: resolve conflicts"

# Push again
git push origin cloud-migration
```

#### Issue 5: Next.js Build Fails

**Symptoms:**
- TypeScript errors
- Build compilation fails

**Solutions:**
```bash
# Clean install
cd mydigitaltwin
rm -rf node_modules .next
npm install

# Check TypeScript errors
npm run build

# Fix type errors in code
# Then rebuild
npm run dev
```

### Debug Mode

**Enable Verbose Logging:**

In `mydigitaltwin/app/api/query/route.ts`:
```typescript
console.log('Received question:', question);
console.log('Python script path:', scriptPath);
console.log('Python stdout:', stdout);
console.log('Python stderr:', stderr);
```

In `rag_api.py`:
```python
import sys
sys.stderr.write(f"Processing question: {question}\n")
sys.stderr.write(f"Results count: {len(results)}\n")
```

### Getting Help

**Resources:**
- Project README: `README_PROJECT.md`
- GitHub Issues: https://github.com/VivianP05/ragfood/issues
- Quick Reference: `QUICK_REFERENCE.md`
- GitHub MCP Guide: `GITHUB_MCP_ENABLED.md`

**Community:**
- Next.js Docs: https://nextjs.org/docs
- Upstash Docs: https://upstash.com/docs
- Groq Docs: https://console.groq.com/docs

---

## 📚 Additional Resources

### Documentation Files

- `README_PROJECT.md` - Complete project documentation
- `GITHUB_SETUP_COMPLETE.md` - GitHub setup guide
- `GITHUB_MCP_ENABLED.md` - MCP integration details
- `QUICK_REFERENCE.md` - Quick command reference
- `GITHUB_MCP_QUICK_START.md` - MCP quick start guide

### Code Examples

**Add New Food Item:**
```python
# In upload_foods_to_upstash.py
new_food = {
    "id": "111",
    "name": "Sushi",
    "category": "Main Course",
    "origin": "Japan",
    "description": "Japanese dish with vinegared rice and seafood",
    "dietary_tags": "Pescatarian"
}
```

**Add New API Endpoint:**
```typescript
// In mydigitaltwin/app/api/recommend/route.ts
export async function POST(request: NextRequest) {
  const { preferences } = await request.json();
  // Your recommendation logic
  return NextResponse.json({ recommendations });
}
```

**Custom RAG Query:**
```python
# In rag_api.py
def query_with_filters(question: str, category: str):
    # Add category filtering to query
    results = index.query(
        data=question,
        top_k=3,
        include_metadata=True,
        filter=f"category = '{category}'"
    )
```

---

## 🎯 Quick Commands Reference

```bash
# Development
npm run dev              # Start Next.js
python3 rag_api.py "Q"   # Test Python API
python3 rag_food_query.py # Start CLI

# Git
git status               # Check status
git add .                # Stage all
git commit -m "msg"      # Commit
git push origin branch   # Push

# Database
python3 check_upstash_database.py  # Check DB
python3 upload_foods_to_upstash.py # Upload data

# Deployment
vercel                   # Deploy to Vercel
railway up               # Deploy to Railway
```

---

**Last Updated**: October 29, 2025  
**Maintained By**: VivianP05  
**Repository**: https://github.com/VivianP05/ragfood
# Digital Twin MCP Server Project Instructions

## Project Overview
Build an MCP server using the roll dice pattern to create a digital twin assistant that can answer questions about a person's professional profile using RAG (Retrieval-Augmented Generation).

## Reference Repositories
- **Pattern Reference**: https://github.com/gocallum/rolldice-mcpserver.git
  - Roll dice MCP server - use same technology and pattern for our MCP server
- **Logic Reference**: https://github.com/gocallum/binal_digital-twin_py.git
  - Python code using Upstash Vector for RAG search with Groq and LLaMA for generations

## Core Functionality
- MCP server accepts user questions about the person's professional background
- Create server actions that search Upstash Vector database and return RAG results
- Search logic must match the Python version exactly

## Environment Variables (.env.local)
```
UPSTASH_VECTOR_REST_URL=
UPSTASH_VECTOR_REST_TOKEN=
GROQ_API_KEY=
```

## Technical Requirements
- **Framework**: Next.js 15.5.3+ (use latest available)
- **Package Manager**: Always use pnpm (never npm or yarn)
- **Commands**: Always use Windows PowerShell commands
- **Type Safety**: Enforce strong TypeScript type safety throughout
- **Architecture**: Always use server actions where possible
- **Styling**: Use globals.css instead of inline styling
- **UI Framework**: ShadCN with dark mode theme
- **Focus**: Prioritize MCP functionality over UI - UI is primarily for MCP server configuration

## Setup Commands
```bash
pnpm dlx shadcn@latest init
```
Reference: https://ui.shadcn.com/docs/installation/next

## Upstash Vector Integration

### Key Documentation
- Getting Started: https://upstash.com/docs/vector/overall/getstarted
- Embedding Models: https://upstash.com/docs/vector/features/embeddingmodels
- TypeScript SDK: https://upstash.com/docs/vector/sdks/ts/getting-started

### Example Implementation
```typescript
import { Index } from "@upstash/vector"

const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
})

// RAG search example
await index.query({
  data: "What is Upstash?",
  topK: 3,
  includeMetadata: true,
})
```

## Additional Useful Resources
- Add any other relevant documentation links as needed
- Include specific API references for integrations
- Reference MCP protocol specifications
- Add deployment and testing guidelines

---

