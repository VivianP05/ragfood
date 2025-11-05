# 👩‍💼 Vivian Pham - Digital Twin Portfolio

AI-powered digital twin that answers questions about Vivian Pham's professional experience, skills, and projects using RAG (Retrieval-Augmented Generation).

## 🎯 Purpose

This is a **professional portfolio application** that demonstrates:
- ✅ Full-stack Next.js 16 development
- ✅ RAG system implementation with Upstash Vector + Groq AI
- ✅ TypeScript type safety
- ✅ Modern UI with Tailwind CSS
- ✅ Real-time chat interface
- ✅ Production deployment on Vercel

## 🚀 Features

- **Intelligent Q&A**: Ask about Vivian's experience, skills, projects, and career goals
- **Real-time Chat**: Interactive chat interface with message history
- **Example Questions**: Pre-populated questions to guide conversations
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode Support**: Automatic theme switching
- **Production Ready**: Optimized for Vercel deployment

## 💼 What You Can Ask

- "What is Vivian's experience with Excel?"
- "Tell me about her Power BI projects"
- "What are her salary expectations?"
- "Describe her technical skills"
- "What is her availability?"
- "Tell me about her data quality project"

## 🛠️ Tech Stack

### Frontend
- **Next.js 16.0.1** - React framework with App Router
- **React 19.2.0** - UI library
- **TypeScript 5** - Type safety
- **Tailwind CSS 4** - Utility-first styling

### Backend
- **Upstash Vector** - Vector database for semantic search
- **Groq AI** - LLM for natural language generation (llama-3.1-8b-instant)
- **Next.js API Routes** - Serverless API endpoints

## 📊 Data Source

Vivian's professional profile stored in Upstash Vector includes:
- ✅ **Basic Information**: Contact details, work authorization, availability
- ✅ **Compensation**: Salary expectations for contract and permanent roles
- ✅ **Technical Skills**: Excel Level 5, Power BI, Python, SQL, TypeScript
- ✅ **Projects**: Data Quality Automation, KPI Dashboard, ragfood RAG system
- ✅ **Soft Skills**: Communication, problem-solving, learning agility
- ✅ **Career Goals**: Target companies and career development plans

## 🚀 Local Development

### Prerequisites
- Node.js 18+ 
- npm
- Upstash Vector database with Vivian's profile data

### Setup

1. **Clone the repository**:
```bash
cd /Users/DELL/ragfood/vivian-digital-twin
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment variables**:
Create `.env.local` file:
```bash
UPSTASH_VECTOR_REST_URL="your-upstash-url"
UPSTASH_VECTOR_REST_TOKEN="your-upstash-token"
GROQ_API_KEY="your-groq-api-key"
```

4. **Run development server**:
```bash
npm run dev
```

5. **Open browser**:
```
http://localhost:3001
```

## 📦 Scripts

```bash
npm run dev      # Start development server (port 3001)
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

## 🌐 Deployment

### Deploy to Vercel

1. **Push to GitHub**:
```bash
git add .
git commit -m "feat: add digital twin app"
git push origin main
```

2. **Import to Vercel**:
- Go to https://vercel.com/new
- Import repository: `VivianP05/ragfood`
- Set **Root Directory**: `vivian-digital-twin`

3. **Add Environment Variables**:
```
UPSTASH_VECTOR_REST_URL = [your-upstash-url]
UPSTASH_VECTOR_REST_TOKEN = [your-upstash-token]
GROQ_API_KEY = [your-groq-api-key]
```

4. **Deploy**:
- Click "Deploy"
- Wait ~2 minutes
- Get your live URL!

## 📁 Project Structure

```
vivian-digital-twin/
├── app/
│   ├── api/
│   │   └── query/
│   │       └── route.ts        # API endpoint for RAG queries
│   ├── globals.css              # Global styles
│   ├── layout.tsx               # Root layout
│   └── page.tsx                 # Main chat interface
├── .env.local                   # Environment variables (gitignored)
├── .gitignore                   # Git ignore rules
├── .npmrc                       # npm configuration
├── next.config.ts               # Next.js configuration
├── package.json                 # Dependencies
├── postcss.config.mjs           # PostCSS configuration
├── tailwind.config.ts           # Tailwind configuration
└── tsconfig.json                # TypeScript configuration
```

## 🔑 Key Components

### 1. Chat Interface (`app/page.tsx`)
- Real-time message rendering
- User input handling
- Example question suggestions
- Loading states and error handling

### 2. RAG API (`app/api/query/route.ts`)
- Vector search with Upstash (top_k=3)
- Context extraction from search results
- AI response generation with Groq
- Error handling and validation

### 3. Styling (`app/globals.css`)
- Tailwind CSS utilities
- Dark mode support
- Responsive design
- Custom animations

## 🎨 UI Features

- **Purple/Blue Gradient Theme**: Professional and modern look
- **Example Questions**: Click to populate input field
- **Message Bubbles**: User (purple) vs Assistant (gray)
- **Timestamps**: Track conversation flow
- **Loading Animation**: Bouncing dots during AI response
- **Responsive Layout**: Works on all screen sizes
- **Dark Mode**: Automatic theme detection

## 🔍 How It Works

1. **User asks a question** → Sent to `/api/query` endpoint
2. **Vector search** → Query embedded and searched in Upstash Vector
3. **Context retrieval** → Top 3 most relevant profile sections retrieved
4. **AI generation** → Groq generates natural language response
5. **Response display** → Answer shown in chat interface

## 📊 Performance

- **Vector Search**: <100ms (Upstash)
- **AI Generation**: ~1-2s (Groq llama-3.1-8b-instant)
- **Total Response Time**: ~2-3s
- **Build Time**: ~30s
- **Deploy Time**: ~2 minutes

## 🐛 Troubleshooting

### "Failed to get response" error
- Check environment variables are set correctly
- Verify Upstash database contains profile data
- Check Groq API key is valid

### Build fails on Vercel
- Ensure Root Directory is set to `vivian-digital-twin`
- Verify all environment variables are added
- Check build logs for specific errors

### No relevant answers
- Verify profile data is uploaded to Upstash
- Check vector search is returning results
- Adjust `topK` parameter if needed

## 📝 License

This is a portfolio project by Vivian Pham. Feel free to use as a reference for your own projects!

## 👥 Contact

**Vivian Pham**
- GitHub: [@VivianP05](https://github.com/VivianP05)
- Portfolio: [Digital Twin Demo](https://vivian-digital-twin.vercel.app)

## 🎯 Related Projects

- **Food RAG**: Separate app for food queries ([ragfood-1w2l.vercel.app](https://ragfood-1w2l.vercel.app))
- **MCP Server**: Model Context Protocol integration for Claude Desktop

---

Built with ❤️ by Vivian Pham | Powered by Next.js 16 + Upstash Vector + Groq AI
