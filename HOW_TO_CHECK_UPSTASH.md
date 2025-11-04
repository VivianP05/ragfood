# 🔍 How to Check Your Upstash Vector Database

## ✅ Your Database Status

- **Total Vectors**: 133
  - 110 Food items (from `foods.json`)
  - 21 Digital Twin entries (Vivian's interview prep)
  - 2 Legacy items
- **Embedding Model**: mxbai-embed-large-v1 (1024 dimensions)
- **Similarity**: COSINE
- **Status**: ✅ Fully operational

---

## 🌐 Method 1: Web Console (Recommended)

### Step-by-Step:

1. **Open your browser** and go to:
   ```
   https://console.upstash.com/vector
   ```

2. **Login** to your Upstash account

3. **Click** on your database: **"new-badger-26"**

4. **View Dashboard** - You'll see:
   - Vector Count: 133
   - Namespace: default
   - Embedding Model: mxbai-embed-large-v1
   - Dimensions: 1024

5. **Try the QUERY Tab**:
   - Type a query: `"spicy Indian food"`
   - Set Top K: `5`
   - Click **"Query"**
   - See results with similarity scores!

### Sample Queries to Try:
```
spicy Indian food
sweet fruit
Japanese cuisine
Italian pasta
healthy breakfast
dessert
sushi
Thai food
```

---

## 💻 Method 2: Python Inspection Script

### Full Database Inspection:
```bash
python3 check_upstash_database.py
```

This will show you:
- ✅ Database statistics
- ✅ Sample vectors (first 10)
- ✅ Test queries with results
- ✅ Food coverage by category
- ✅ Digital twin data verification

### Quick Stats Check:
```bash
python3 -c "from upstash_vector import Index; from dotenv import load_dotenv; load_dotenv(); i = Index.from_env(); info = i.info(); print(f'Vectors: {info.vector_count}, Dimensions: {info.dimension}')"
```

### Test Single Query:
```bash
python3 -c "from upstash_vector import Index; from dotenv import load_dotenv; load_dotenv(); i = Index.from_env(); results = i.query(data='sushi', top_k=3); [print(f'{x.id}: {x.score:.3f}') for x in results]"
```

---

## 🧪 Method 3: Use Your RAG System

### Run the RAG System:
```bash
cd /Users/DELL/ragfood
python3 src/rag_run_upstash.py
```

Then ask questions like:
- "What is Biryani?"
- "Recommend a healthy breakfast"
- "Tell me about Japanese ramen"
- "What's a good Italian dish?"

---

## 📊 What's in Your Database

### Food Items (110 total):
```
ID 1   → Banana (Tropical fruit)
ID 5   → Biryani (Indian rice dish)
ID 62  → Ramen (Japanese noodle soup)
ID 91  → Pad Thai (Thai stir-fried noodles)
ID 92  → Greek Moussaka (Mediterranean casserole)
ID 100 → Buddha Bowl (Modern health cuisine)
...and 104 more food items!
```

### Digital Twin Entries (21 total):
```
personal_profile          → Vivian Pham's info
salary_location          → Compensation preferences
experience_ausbiz        → Ausbiz Consulting internship
technical_skills         → Python & Excel skills
soft_skills             → Collaboration, communication
education               → Master of Data Science
projects_digitaltwin    → Digital Twin Workshop project
projects_ragfood        → RAG Food project
career_goals            → Data Scientist path
behavioral_question_1   → Learning quickly (STAR)
behavioral_question_2   → Teamwork example (STAR)
behavioral_question_3   → Balancing priorities (STAR)
weakness_mitigation_1   → Limited experience
weakness_mitigation_2   → Developing Python skills
weakness_mitigation_3   → Large-scale systems
professional_development → Master's program & projects
```

---

## ✅ Verified Working Queries

### Food Queries:
| Query | Top Results |
|-------|------------|
| `spicy Indian food` | chili pepper, raita, samosa |
| `sweet fruit` | apple, banana, lemon |
| `Japanese cuisine` | tempura, ramen |
| `Italian pasta` | risotto, pizza |
| `healthy breakfast` | oatmeal, avocado toast, Greek yogurt |
| `dessert` | baklava, lamingtons, chia pudding |

### Digital Twin Queries:
| Query | Found |
|-------|-------|
| `Vivian Pham` | ✅ Personal profile |
| `AI Data Analyst` | ✅ Work experience |
| `Ausbiz Consulting` | ✅ Internship details |
| `interview preparation` | ✅ Behavioral questions |

---

## 🎯 Quick Reference Commands

```bash
# Upload food data (already done!)
python3 upload_foods_to_upstash.py

# Check database
python3 check_upstash_database.py

# Run RAG system
python3 src/rag_run_upstash.py

# Quick stats
python3 -c "from upstash_vector import Index; from dotenv import load_dotenv; load_dotenv(); print(Index.from_env().info())"
```

---

## 🔗 Important Links

- **Upstash Console**: https://console.upstash.com/vector
- **Your Database**: new-badger-26
- **Database URL**: https://new-badger-26-gcp-usc1-vector.upstash.io

---

## 📝 Database Configuration

Your database is configured in `.env`:
```bash
UPSTASH_VECTOR_REST_URL="https://new-badger-26-gcp-usc1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="ABYFMG5ldy1iYWRnZXItMjYt..." # (masked)
GROQ_API_KEY="gsk_gzMSnFTXmRhcvXt..." # (masked)
```

---

## 🎉 Your Database is Ready!

Everything is uploaded and working perfectly. You can now:
1. ✅ Browse in the web console
2. ✅ Test queries in the console's Query tab
3. ✅ Use your RAG system to ask food questions
4. ✅ Practice interview prep with your digital twin

**Happy querying! 🚀**
