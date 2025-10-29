# 🎯 Quick Reference - Food RAG Project

## 🚀 Start Development

### Next.js Web App
```bash
cd mydigitaltwin
npm run dev
# Visit: http://localhost:3000
```

### Python CLI
```bash
python3 rag_food_query.py
```

## 🔧 Git Commands

### Daily Workflow
```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "feat: your change description"

# Push to GitHub
git push origin cloud-migration

# Pull latest
git pull origin cloud-migration
```

### Create New Feature
```bash
# Create branch
git checkout -b feature/my-feature

# Make changes, then:
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature
```

## 🔐 Environment Setup

### Required Environment Variables
```bash
# In .env and mydigitaltwin/.env.local
UPSTASH_VECTOR_REST_URL="your-upstash-url"
UPSTASH_VECTOR_REST_TOKEN="your-upstash-token"
GROQ_API_KEY="your-groq-api-key"
```

## 🔍 Useful Scripts

### Check Database
```bash
python3 check_upstash_database.py
```

### Upload Food Data
```bash
python3 upload_foods_to_upstash.py
```

### Test API
```bash
python3 rag_api.py "What is Biryani?"
```

## 🌐 URLs

- **GitHub Repo**: https://github.com/VivianP05/ragfood
- **Local Dev**: http://localhost:3000
- **API Endpoint**: http://localhost:3000/api/query

## 📝 Commit Message Convention

```bash
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Code formatting
refactor: Code restructuring
test: Add tests
chore: Maintenance tasks
```

## 🆘 Troubleshooting

### Next.js won't start
```bash
cd mydigitaltwin
rm -rf node_modules .next
npm install
npm run dev
```

### Python dependencies missing
```bash
pip install python-dotenv upstash-vector groq
```

### API returns errors
```bash
# Check environment variables
cat .env
cat mydigitaltwin/.env.local

# Test Python script directly
python3 rag_api.py "test query"
```

### Git conflicts
```bash
# Abort merge
git merge --abort

# Or reset to remote
git fetch origin
git reset --hard origin/cloud-migration
```

## 📚 Documentation Files

- `README_PROJECT.md` - Main project documentation
- `GITHUB_SETUP_COMPLETE.md` - GitHub setup guide
- `RAG_QUICK_START.md` - RAG system quick start
- `HOW_TO_CHECK_UPSTASH.md` - Database inspection guide

---

**Keep this file handy for quick reference!**
