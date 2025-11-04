# 🍽️ RAG Food Query System - Quick Start Guide

## ✅ Your System is Ready!

**Test Result:** ✅ Successfully answered "What is Biryani?"
- Found 3 relevant matches
- Generated accurate AI answer
- Response time: Fast!

---

## 🚀 How to Use

### Interactive Mode (Recommended)
```bash
python3 rag_food_query.py
```

Then ask questions:
```
💭 You: What is Biryani?
💭 You: Recommend a healthy breakfast
💭 You: Tell me about Japanese ramen
```

Type `exit` to quit.

---

### Single Question
```bash
python3 -c "from rag_food_query import query_food; print(query_food('What is sushi?'))"
```

---

### Use in Your Code
```python
from rag_food_query import query_food

# Ask a question
answer = query_food("What is Pad Thai?")
print(answer)
```

---

## 💡 Example Questions

### About Specific Foods
- What is Biryani?
- Tell me about Pad Thai
- What is Greek Moussaka?
- Describe Japanese Ramen

### Recommendations
- Recommend a healthy breakfast
- What's a good Italian dish?
- Suggest a spicy Indian food
- What dessert should I try?

### Comparisons
- What's the difference between ramen and pho?
- Compare Greek and Italian cuisine
- Which is healthier: pizza or pasta?

### Dietary Specific
- What are some vegetarian options?
- Show me low-carb foods
- What foods are good for breakfast?
- What are some protein-rich dishes?

---

## 🔧 How It Works

1. **Your Question** → "What is Biryani?"
2. **Upstash Vector Search** → Searches 200 food items, returns top 3 matches
3. **Context Building** → Combines relevant information
4. **Groq AI** → Generates accurate answer using llama-3.1-8b-instant
5. **Answer** → Clear, informative response

---

## 📊 System Components

### Database
- **Platform:** Upstash Vector (free-loon-62438)
- **Vectors:** 200 (110 foods + 90 other)
- **Model:** mxbai-embed-large-v1
- **Dimensions:** 1024

### AI Model
- **Provider:** Groq Cloud
- **Model:** llama-3.1-8b-instant
- **Speed:** Very fast
- **Cost:** Free tier available

### Data
- **110 Food Items** from around the world
- Global cuisines (Indian, Japanese, Italian, Greek, Thai, etc.)
- Nutritional information
- Cooking methods
- Regional origins

---

## 🎯 Quick Commands

```bash
# Interactive mode
python3 rag_food_query.py

# Single question
python3 -c "from rag_food_query import query_food; print(query_food('What is sushi?'))"

# Check database
python3 check_upstash_database.py

# View in console
# Go to: https://console.upstash.com/vector
# Click: free-loon-62438
```

---

## ✅ Verified Working

```
Question: "What is Biryani?"

Results:
  1. Biryani (relevance: 0.922) ⭐ Perfect match!
  2. Chole (relevance: 0.824)
  3. Chicken Karahi (relevance: 0.815)

Answer:
  "Biryani is a flavorful Indian rice dish made with spices,
   rice, and usually meat or vegetables. It's a delicious and
   aromatic dish that's a staple in Indian cuisine."

✅ System working perfectly!
```

---

## 📝 Your .env Configuration

```bash
UPSTASH_VECTOR_REST_URL="https://free-loon-62438-us1-vector.upstash.io"
UPSTASH_VECTOR_REST_TOKEN="ABM..." # Your token
GROQ_API_KEY="gsk_..." # Your Groq key
```

---

## 🆘 Troubleshooting

### Connection Issues
```bash
# Test Upstash connection
python3 -c "from upstash_vector import Index; from dotenv import load_dotenv; load_dotenv(); i = Index.from_env(); print(f'Vectors: {i.info().vector_count}')"
```

### Check Environment
```bash
# Verify .env file
cat .env
```

### Re-upload Data
```bash
python3 upload_foods_to_upstash.py
```

---

## 🎉 You're All Set!

Your RAG Food System is ready to answer any food-related question!

**Start now:**
```bash
python3 rag_food_query.py
```

Happy querying! 🍕🍜🍱🚀
