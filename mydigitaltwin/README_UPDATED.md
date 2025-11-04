# 🍽️ Food RAG System - Next.js Frontend

A full-stack **Retrieval-Augmented Generation (RAG)** system for food queries powered by **Upstash Vector Database** and **Groq AI**.

## 🌟 Features

- ✅ **AI-Powered Food Search** - Semantic search across 200+ food items
- ✅ **Smart Caching** - 99% faster responses for repeated queries
- ✅ **Comprehensive Error Handling** - Automatic retry logic with exponential backoff
- ✅ **Performance Tracking** - Real-time metrics for all operations
- ✅ **Input Validation** - Prevents invalid requests before API calls
- ✅ **Structured Logging** - Detailed logs for debugging and monitoring
- ✅ **MCP Server** - Model Context Protocol integration for Claude Desktop

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Environment Variables

Create `.env.local` in the project root:

```bash
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="your-token-here"
GROQ_API_KEY="your-groq-api-key-here"
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build MCP Server (Optional)

```bash
npm run build:mcp
```

---

## 📚 Documentation

### Core Guides
- **[Error Handling Guide](ERROR_HANDLING_GUIDE.md)** - Comprehensive error handling documentation
- **[Testing Guide](TESTING_GUIDE.md)** - Step-by-step testing instructions
- **[MCP Setup](GITHUB_MCP_ENABLED.md)** - Model Context Protocol integration
- **[Agents Guide](../agents.md)** - AI agent instructions and architecture

### Quick References
- **[Quick Reference](QUICK_REFERENCE.md)** - Common commands and workflows
- **[GitHub MCP Quick Start](GITHUB_MCP_QUICK_START.md)** - GitHub operations via MCP

---

## 🏗️ Architecture

```
Frontend (Next.js) → API Route → Python RAG Script → Upstash Vector + Groq AI
```

### Key Components

#### **Server Actions** (`src/actions/foodRagActions.ts`)
- `queryFoodRAG()` - Main RAG query with caching and error handling
- `searchByCategory()` - Category-based food search
- `getFoodRecommendations()` - AI-powered personalized recommendations

#### **Error Handling** (`src/lib/errorHandling.ts`)
- Custom error classes (UpstashVectorError, GroqAPIError)
- Error classification (11 categories: NETWORK, TIMEOUT, AUTH, etc.)
- Safe wrappers with automatic retry logic
- Structured logging (5 levels: info, error, warn, debug, perf)

#### **MCP Server** (`src/mcp-server/index.ts`)
- Model Context Protocol server for Claude Desktop
- Tools: `query_food_rag`, `search_by_category`, `get_recommendations`

---

## 🧪 Testing

### Run Linting

```bash
npm run lint
```

### Build Project

```bash
npm run build
```

### Build MCP Server

```bash
npm run build:mcp
```

### Test Error Handling

See **[TESTING_GUIDE.md](TESTING_GUIDE.md)** for comprehensive testing instructions.

Quick test:

```typescript
// In browser console
const result = await fetch('/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: "What is Biryani?" })
}).then(r => r.json());

console.log(result);
```

---

## 📊 Performance

### Response Times (Average)

| Scenario | Time | Cache Hit Rate |
|----------|------|----------------|
| **Cached Query** | 5-15ms | 100% |
| **Vector Search** | 200-400ms | - |
| **AI Generation** | 500-1500ms | - |
| **Total (Uncached)** | 700-1900ms | - |

### Caching
- **Duration**: 5 minutes
- **Max Size**: 100 entries
- **Eviction**: LRU (Least Recently Used)
- **Speed Improvement**: 99% faster for repeated queries

---

## 🛡️ Error Handling

### Features
- ✅ **Automatic Retry** - 3 attempts with exponential backoff
- ✅ **Error Classification** - 11 categories for precise error handling
- ✅ **User-Friendly Messages** - Clear, actionable error messages
- ✅ **Smart Retry Logic** - Only retries transient errors (network, timeout, rate limit)

### Error Categories
- NETWORK - Connection failures (retryable)
- TIMEOUT - Request timeouts (retryable)
- AUTH - Invalid credentials (non-retryable)
- RATE_LIMIT - Too many requests (retryable)
- QUOTA_EXCEEDED - Usage limits reached (non-retryable)
- SERVICE_UNAVAILABLE - Backend issues (retryable)
- INVALID_INPUT - Bad request (non-retryable)
- And more...

See **[ERROR_HANDLING_GUIDE.md](ERROR_HANDLING_GUIDE.md)** for complete details.

---

## 📁 Project Structure

```
mydigitaltwin/
├── app/
│   ├── page.tsx              # Main chat UI
│   └── api/
│       └── query/route.ts    # API endpoint
├── src/
│   ├── actions/
│   │   └── foodRagActions.ts # Server actions (RAG logic)
│   ├── lib/
│   │   └── errorHandling.ts  # Error handling utilities
│   └── mcp-server/
│       └── index.ts          # MCP server
├── dist/
│   └── mcp-server/
│       └── index.js          # Compiled MCP server
├── .env.local                # Environment variables
├── ERROR_HANDLING_GUIDE.md   # Error handling docs
├── TESTING_GUIDE.md          # Testing instructions
└── package.json
```

---

## 🔧 Configuration

### TypeScript

Two TypeScript configurations:

1. **`tsconfig.json`** - Next.js app configuration
2. **`tsconfig.mcp.json`** - MCP server configuration

### ESLint

```bash
npm run lint
```

### Environment Variables

Required in `.env.local`:

```bash
UPSTASH_VECTOR_REST_URL="..."
UPSTASH_VECTOR_REST_TOKEN="..."
GROQ_API_KEY="..."
```

---

## 🚀 Deployment

### Deploy to Vercel

1. Push to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy!

See **[Deployment Guide](../agents.md#deployment-guide)** for detailed instructions.

---

## 📖 Learn More

### Next.js Resources
- [Next.js Documentation](https://nextjs.org/docs) - Features and API
- [Learn Next.js](https://nextjs.org/learn) - Interactive tutorial
- [Next.js GitHub](https://github.com/vercel/next.js) - Source code

### Project Resources
- [Upstash Vector Docs](https://upstash.com/docs/vector) - Vector database
- [Groq API Docs](https://console.groq.com/docs) - AI inference
- [MCP Specification](https://modelcontextprotocol.io/) - Model Context Protocol

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `npm run lint` and `npm run build`
5. Commit: `git commit -m "feat: add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create a Pull Request

---

## 📄 License

This project is part of the Food RAG System.

**Repository**: https://github.com/VivianP05/ragfood

---

## 🙏 Acknowledgments

- **Next.js** - React framework
- **Upstash** - Vector database
- **Groq** - Fast AI inference
- **ShadCN** - UI components
- **Tailwind CSS** - Styling

---

**Last Updated**: October 30, 2025  
**Version**: 2.0.0  
**Maintained By**: VivianP05
