# RAG-Food Project

A Retrieval-Augmented Generation (RAG) system for food-related queries with multiple backend implementations.

## 🏗️ Project Structure

```
ragfood/
├── ragfood.py              # Main entry point
├── .env                    # Environment variables (create from .env.template)
├── .env.template           # Environment template
├── package-lock.json       # Dependencies
├── src/                    # Source code
│   ├── rag_run.py         #   ChromaDB + Ollama implementation
│   ├── rag_run_upstash.py #   Upstash Vector implementation  
│   ├── rag_run_groq.py    #   Groq API implementation
│   └── rag_run_groq_streaming.py # Groq Streaming implementation
├── tests/                  # Test files
│   ├── query_test.py      #   Comprehensive testing suite
│   ├── test_groq_*.py     #   Groq-specific tests
│   └── performance_comparison.py # Performance benchmarks
├── data/                   # Data files
│   ├── foods.json         #   Food database (110 items)
│   └── test_queries.txt   #   Sample queries
├── docs/                   # Documentation
│   ├── README.md          #   Main documentation
│   ├── Migration_Plan.md  #   Cloud migration strategy
│   └── *.md              #   Setup guides and design docs
├── chroma_db/             # ChromaDB storage (local)
└── chroma_db_backup/      # ChromaDB backup
```

## 🚀 Quick Start

### 1. Choose Your Implementation

The project supports multiple RAG backends:

- **🚀 Groq Streaming** (Recommended) - Fast cloud API with streaming
- **🟢 Groq API** - Fast cloud API  
- **🟡 Upstash Vector** - Cloud vector database
- **🔵 ChromaDB + Ollama** - Local implementation

### 2. Setup Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your API keys (if using cloud services)
# GROQ_API_KEY=your_groq_key_here
# UPSTASH_VECTOR_REST_URL=your_upstash_url
# UPSTASH_VECTOR_REST_TOKEN=your_upstash_token
```

### 3. Run the System

#### Interactive Mode
```bash
python3 ragfood.py --interactive
```

#### Single Query
```bash
python3 ragfood.py -q "spicy Asian dishes"
```

#### Choose Implementation
```bash
python3 ragfood.py -i groq-streaming -q "healthy Mediterranean food"
python3 ragfood.py -i upstash --interactive
```

#### Run Tests
```bash
python3 ragfood.py --test
```

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--interactive` | Start interactive mode | `python3 ragfood.py --interactive` |
| `--query "text"` | Single query | `python3 ragfood.py -q "pasta dishes"` |
| `--implementation name` | Choose backend | `python3 ragfood.py -i groq-streaming` |
| `--test` | Run test suite | `python3 ragfood.py --test` |

## 🔧 Implementation Details

### Groq Streaming (Recommended)
- ⚡ Fastest response times (0.5-2s)  
- 🔄 Real-time streaming output
- ☁️ Zero maintenance
- 💰 Pay-per-use pricing

### Upstash Vector
- 🌐 Cloud vector database
- 🤖 Built-in embeddings (mixedbread-ai)
- 📈 Auto-scaling
- 🔒 Enterprise security

### ChromaDB + Ollama (Local)
- 🏠 Runs entirely locally
- 🔒 Complete privacy
- 💻 Requires Ollama installation
- ⚙️ Manual setup required

## 📊 Performance Comparison

| Implementation | Avg Response Time | Setup Complexity | Cost |
|----------------|------------------|------------------|------|
| Groq Streaming | 0.8s | Easy | ~$0.10/1K tokens |
| Upstash Vector | 1.2s | Easy | ~$0.40/1K queries |
| ChromaDB Local | 3.5s | Complex | Hardware only |

## 🧪 Testing

Run comprehensive tests on all implementations:

```bash
python3 ragfood.py --test
```

Or test specific components:
```bash
cd tests/
python3 test_groq_api.py
python3 performance_comparison.py
```

## 📚 Documentation

- **[Migration Plan](docs/Migration_Plan.md)** - Complete cloud migration strategy
- **[Setup Guides](docs/)** - Implementation-specific setup
- **[API Documentation](src/)** - Code documentation

## 🏷️ Sample Queries

Try these example queries:
- "spicy vegetarian Asian dishes"
- "healthy Mediterranean options" 
- "gluten-free comfort foods"
- "high-protein low-carb meals"
- "traditional holiday dishes"

## 🤝 Contributing

1. Add new food items to `data/foods.json`
2. Create tests in `tests/` directory
3. Update documentation in `docs/`
4. Follow the established project structure

## 📄 License

MIT License - See LICENSE file for details