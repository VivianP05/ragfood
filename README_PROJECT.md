# 🍽️ Food RAG System - Full Stack Application

A complete Retrieval-Augmented Generation (RAG) system for food queries, combining Python backend with Next.js frontend.

## 🌟 Features

- **Vector Database**: Upstash Vector with 200+ food items
- **AI-Powered Responses**: Groq AI (llama-3.1-8b-instant)
- **Dual Interface**: 
  - Python CLI for terminal users
  - Next.js web app for interactive chat
- **Semantic Search**: Finds relevant food information using embeddings
- **Real-time Chat**: Beautiful, responsive UI with message history

## 🏗️ Architecture

```
┌─────────────────┐
│   Next.js App   │  (Port 3000)
│   /mydigitaltwin│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   API Route     │  (/api/query)
│   route.ts      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Python RAG     │
│  rag_api.py     │
└────────┬────────┘
         │
         ├─────────────────┐
         ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ Upstash      │   │ Groq AI      │
│ Vector DB    │   │ LLM          │
└──────────────┘   └──────────────┘
```

## 📦 Project Structure

```
ragfood/
├── mydigitaltwin/           # Next.js Frontend
│   ├── app/
│   │   ├── api/query/      # API endpoint for RAG
│   │   ├── page.tsx        # Chat UI
│   │   └── layout.tsx
│   ├── .env.local          # Environment variables
│   └── package.json
│
├── Python Backend & RAG System
│   ├── rag_api.py          # JSON API wrapper
│   ├── rag_food_query.py   # Interactive CLI
│   ├── digital_twin_rag.py # Advanced RAG system
│   ├── upload_foods_to_upstash.py
│   └── check_upstash_database.py
│
├── Data
│   ├── foods.json          # 110 food items
│   └── chroma_db/          # Local vector DB (gitignored)
│
└── Configuration
    ├── .env                # Credentials (gitignored)
    ├── .gitignore
    └── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Upstash Vector account
- Groq API key

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/VivianP05/ragfood.git
cd ragfood

# Install Python dependencies
pip install python-dotenv upstash-vector groq

# Install Next.js dependencies
cd mydigitaltwin
npm install
```

### 2. Configure Environment

Create `.env` in the root directory:

```bash
UPSTASH_VECTOR_REST_URL="your-upstash-url"
UPSTASH_VECTOR_REST_TOKEN="your-upstash-token"
GROQ_API_KEY="your-groq-api-key"
```

Copy to Next.js:
```bash
cp .env mydigitaltwin/.env.local
```

### 3. Run the Application

**Option A: Web Interface (Recommended)**

```bash
cd mydigitaltwin
npm run dev
```

Visit http://localhost:3000

**Option B: Python CLI**

```bash
python3 rag_food_query.py
```

**Option C: Advanced Interactive CLI**

```bash
python3 digital_twin_rag.py
```

## 💡 Usage Examples

### Web Interface

1. Open http://localhost:3000
2. Click example questions or type your own:
   - "What is Biryani?"
   - "Recommend a healthy breakfast"
   - "Tell me about Japanese cuisine"

### Python CLI

```bash
# Simple query
python3 rag_api.py "What is Biryani?"

# Interactive mode
python3 rag_food_query.py
```

## 🔧 Development

### Testing the API

```bash
# Test Python API wrapper
python3 rag_api.py "What is sushi?"

# Test Next.js API endpoint
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Biryani?"}'
```

### Adding More Food Data

1. Edit `foods.json`
2. Run upload script:
```bash
python3 upload_foods_to_upstash.py
```

### Check Database

```bash
python3 check_upstash_database.py
```

## 📊 Database Statistics

- **Total Vectors**: 200
- **Food Items**: 110
- **Embedding Model**: mxbai-embed-large-v1
- **Dimensions**: 1024
- **Similarity**: COSINE

## 🛠️ Technologies

### Backend
- **Python 3.13.7**: Core language
- **Upstash Vector**: Vector database
- **Groq**: LLM inference
- **python-dotenv**: Environment management

### Frontend
- **Next.js 16.0.1**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Turbopack**: Fast bundler

## 📝 API Reference

### POST /api/query

Request:
```json
{
  "question": "What is Biryani?"
}
```

Response:
```json
{
  "question": "What is Biryani?",
  "answer": "Biryani is a flavorful Indian rice dish..."
}
```

## 🔐 Security

- Environment variables in `.env` (gitignored)
- API keys never committed to repository
- Secure Upstash connection with REST tokens

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - feel free to use this project for learning and development!

## 🙏 Acknowledgments

- Upstash for vector database infrastructure
- Groq for lightning-fast LLM inference
- Next.js team for excellent framework
- OpenAI for inspiration

## 📞 Support

- GitHub Issues: [Report bugs or request features](https://github.com/VivianP05/ragfood/issues)
- Repository: https://github.com/VivianP05/ragfood

## 🗺️ Roadmap

- [ ] Add user authentication
- [ ] Implement conversation memory
- [ ] Add more cuisines and recipes
- [ ] Deploy to Vercel
- [ ] Add image generation for dishes
- [ ] Multi-language support

---

**Built with ❤️ by Vivian Pham**

*Powered by Upstash Vector + Groq AI*
