# 🎯 Your AI Systems - Quick Reference Guide

## 📚 Two Separate Systems for Different Purposes

You have **two independent AI systems**, each optimized for different use cases:

---

## 🍽️ System 1: Food RAG System

**Location:** `/Users/DELL/ragfood/`  
**Repository:** https://github.com/VivianP05/ragfood  
**Branch:** `cloud-migration`

### **Purpose:**
Answer questions about food, cuisines, recipes, and dietary information

### **Database:**
- **Upstash Vector:** `free-loon-62438-us1-vector.upstash.io`
- **Vectors:** 200 food items (110 detailed + 90 others)
- **Content:** Biryani, Indian cuisine, fruits, spices, desserts, etc.

### **How to Start:**
```bash
cd /Users/DELL/ragfood/mydigitaltwin

# Method 1: Direct command
node mcp-server.js

# Method 2: Shell script
./start-mcp-standalone.sh

# Method 3: VS Code Task
# Cmd+Shift+P → "Tasks: Run Task" → "Start Food RAG MCP Server"
```

### **Available Tools:**
1. `query_food_database` - AI-powered food queries
2. `search_by_category` - Search by food category
3. `get_cache_statistics` - System status

### **Example Questions:**
```
✅ "What is Biryani?"
✅ "Tell me about Japanese cuisine"
✅ "What are healthy breakfast options?"
✅ "Search for Indian desserts"
✅ "Find vegetarian dishes"
```

### **Tech Stack:**
- Next.js 16.0.1
- Upstash Vector Database
- Groq AI (llama-3.1-8b-instant)
- MCP Server (standalone)

---

## 👤 System 2: Professional Digital Twin

**Location:** `/Users/DELL/digital-twin-workshop/`  
**Repository:** (Your local project)  
**Purpose:** Interview preparation & professional background

### **Purpose:**
Answer questions about YOUR work experience, skills, and career

### **Database:**
- **Upstash Vector:** (Separate database instance)
- **Vectors:** 133 professional profile vectors
- **Content:** Ausbiz internship, Python skills, career goals, projects

### **Your Professional Data:**

#### **Work Experience:**
- **Ausbiz Consulting - AI Data Analyst Intern** (2025 - Present)
  - Automated data cleaning workflows (30% time reduction)
  - Created Excel dashboards
  - Collaborated with senior analysts

#### **Skills:**
- Python (1 year - pandas, NumPy)
- Excel (2 years - Advanced formulas, Pivot Tables)
- AI/ML (RAG systems, Vector databases)

#### **Projects:**
1. Digital Twin Workshop - AI interview prep
2. RAG Food - Cloud food recommendation system

#### **Education:**
- Current: Bachelor of Information Systems Management (Victoria University)
- Future: Master of Data Science (2-year program)

### **How to Start:**
```bash
cd /Users/DELL/digital-twin-workshop

# Run the professional digital twin
python3 digital_twin_mcp_server.py

# Or test directly
python3 test_vivian.py
```

### **Example Questions:**
```
✅ "Tell me about my Ausbiz Consulting experience"
✅ "What Python projects have I worked on?"
✅ "Describe my data analysis skills"
✅ "What are my career goals?"
✅ "Give me STAR examples from my internship"
✅ "What's on my resume?"
```

### **Use Cases:**
- 🎤 Interview preparation
- 📄 Resume writing
- 💼 Cover letter generation
- 🎯 Career planning
- 🗣️ STAR response practice

---

## 🔀 Which System to Use?

| Question Type | Use This System |
|---------------|-----------------|
| **Food, recipes, cuisine** | 🍽️ Food RAG (`/ragfood/`) |
| **Work experience** | 👤 Digital Twin (`/digital-twin-workshop/`) |
| **Professional skills** | 👤 Digital Twin |
| **Career goals** | 👤 Digital Twin |
| **Dietary information** | 🍽️ Food RAG |
| **Interview prep** | 👤 Digital Twin |
| **Restaurant recommendations** | 🍽️ Food RAG |
| **Resume help** | 👤 Digital Twin |

---

## 📁 Directory Structure

```
/Users/DELL/
├── ragfood/                          # Food RAG System
│   ├── mydigitaltwin/
│   │   ├── mcp-server.js            # MCP server for food queries
│   │   ├── .env.local               # Upstash + Groq credentials
│   │   └── start-mcp-standalone.sh  # Easy start script
│   ├── .vscode/
│   │   ├── mcp.json                 # MCP configuration
│   │   └── tasks.json               # VS Code tasks
│   └── data/
│       └── foods.json               # 110 food items
│
└── digital-twin-workshop/            # Professional Digital Twin
    ├── digital_twin_mcp_server.py   # MCP server for professional queries
    ├── test_vivian.py               # Test your profile
    ├── cloud-version/
    │   └── VIVIAN_PROFILE_SUMMARY.md # Your work experience
    └── data/
        └── professional_data.json    # 133 professional vectors
```

---

## 🚀 Quick Start Commands

### **Food Queries:**
```bash
# Terminal 1: Start Food RAG
cd /Users/DELL/ragfood/mydigitaltwin
node mcp-server.js

# Terminal 2: Test
# Use GitHub Copilot or test via stdin
```

### **Professional Queries:**
```bash
# Terminal 1: Start Digital Twin
cd /Users/DELL/digital-twin-workshop
python3 digital_twin_mcp_server.py

# Terminal 2: Test
python3 test_vivian.py
```

---

## 💡 Best Practices

### ✅ **DO:**
- Keep systems separate (cleaner, more focused)
- Use Food RAG for cooking/dining questions
- Use Digital Twin for career/interview prep
- Run only one at a time (different ports/purposes)

### ❌ **DON'T:**
- Mix food data with professional data
- Try to merge databases (keeps them specialized)
- Run both simultaneously on same port
- Use Food RAG for work experience questions

---

## 🔧 Maintenance

### **Food RAG System:**
```bash
# Add more food items
cd /Users/DELL/ragfood
python3 upload_foods_to_upstash.py

# Check database
python3 check_upstash_database.py
```

### **Digital Twin System:**
```bash
# Update your profile
cd /Users/DELL/digital-twin-workshop
# Edit cloud-version/VIVIAN_PROFILE_SUMMARY.md
# Re-upload vectors if needed
```

---

## 📊 System Status

| System | Status | Database | Vectors | AI Model |
|--------|--------|----------|---------|----------|
| **Food RAG** | ✅ Running | Upstash (free-loon-62438) | 200 food items | Groq llama-3.1-8b |
| **Digital Twin** | ✅ Ready | Upstash (separate) | 133 professional | Groq llama-3.1-8b |

---

## 🎯 Your Current Setup (Confirmed)

✅ **Food RAG System** - Fully operational in `/ragfood/`  
✅ **Professional Digital Twin** - Ready in `/digital-twin-workshop/`  
✅ **Separate databases** - Clean separation of concerns  
✅ **MCP servers** - Both systems MCP-compatible  
✅ **Documentation** - Complete guides for both  

---

## 📚 Documentation Files

### **Food RAG:**
- `HOW_TO_START_MCP.md` - How to start the MCP server
- `VSCODE_MCP_QUICK_START.md` - VS Code integration guide
- `agents.md` - Complete project documentation

### **Digital Twin:**
- `VIVIAN_PROFILE_SUMMARY.md` - Your professional background
- `README.md` - Digital twin documentation
- `test_vivian.py` - Testing script

---

## 🎉 Summary

You now have **two specialized AI systems** working perfectly:

1. 🍽️ **Food RAG** (`/ragfood/`) → Food & cuisine questions
2. 👤 **Digital Twin** (`/digital-twin-workshop/`) → Professional background

**Both systems are independent, optimized, and ready to use!**

---

**Quick Reference:**
- Food questions? → `cd /Users/DELL/ragfood/mydigitaltwin && node mcp-server.js`
- Career questions? → `cd /Users/DELL/digital-twin-workshop && python3 digital_twin_mcp_server.py`

**Need help with either system? Just ask!** 🚀
