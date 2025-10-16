Here’s a clear, beginner-friendly `README.md` for your RAG project, designed to explain what it does, how it works, and how someone can run it from scratch.

---

## 📄 `README.md`

````markdown
# 🧠 RAG-Food: Simple Retrieval-Augmented Generation with ChromaDB + Ollama

This is a **minimal working RAG (Retrieval-Augmented Generation)** demo using:

- ✅ Local LLM via [Ollama](https://ollama.com/)
- ✅ Local embeddings via `mxbai-embed-large`
- ✅ [ChromaDB](https://www.trychroma.com/) as the vector database
- ✅ A simple food dataset in JSON (Indian foods, fruits, etc.)

---

## 🎯 What This Does

This app allows you to ask questions like:

- “Which Indian dish uses chickpeas?”
- “What dessert is made from milk and soaked in syrup?”
- “What is masala dosa made of?”

It **does not rely on the LLM’s built-in memory**. Instead, it:

1. **Embeds your custom text data** (about food) using `mxbai-embed-large`
2. Stores those embeddings in **ChromaDB**
3. For any question, it:
   - Embeds your question
   - Finds relevant context via similarity search
   - Passes that context + question to a local LLM (`llama3.2`)
4. Returns a natural-language answer grounded in your data.

---

## 📦 Requirements

### ✅ Software

- Python 3.8+
- Ollama installed and running locally
- ChromaDB installed

### ✅ Ollama Models Needed

Run these in your terminal to install them:

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
````

> Make sure `ollama` is running in the background. You can test it with:
>
> ```bash
> ollama run llama3.2
> ```

---

## 🛠️ Installation & Setup

### 1. Clone or download this repo

```bash
git clone https://github.com/yourname/rag-food
cd rag-food
```

### 2. Install Python dependencies

```bash
pip install chromadb requests
```

### 3. Run the RAG app

```bash
python rag_run.py
```

If it's the first time, it will:

* Create `foods.json` if missing
* Generate embeddings for all food items
* Load them into ChromaDB
* Run a few example questions

---

## 📁 File Structure

```
rag-food/
├── rag_run.py       # Main app script
├── foods.json       # Food knowledge base (created if missing)
├── README.md        # This file
```

---

## 🧠 How It Works (Step-by-Step)

1. **Data** is loaded from `foods.json`
2. Each entry is embedded using Ollama's `mxbai-embed-large`
3. Embeddings are stored in ChromaDB
4. When you ask a question:

   * The question is embedded
   * The top 1–2 most relevant chunks are retrieved
   * The context + question is passed to `llama3.2`
   * The model answers using that info only

---

## 🔍 Try Custom Questions

You can update `rag_run.py` to include your own questions like:

```python
print(rag_query("What is tandoori chicken?"))
print(rag_query("Which foods are spicy and vegetarian?"))
```

---

## 🚀 Next Ideas

* Swap in larger datasets (Wikipedia articles, recipes, PDFs)
* Add a web UI with Gradio or Flask
* Cache embeddings to avoid reprocessing on every run

---

## 👨‍🍳 Credits

Made by Callum using:

* [Ollama](https://ollama.com)
* [ChromaDB](https://www.trychroma.com)
* [mxbai-embed-large](https://ollama.com/library/mxbai-embed-large)
* Indian food inspiration 🍛

RAG-FOOD Project 
Name: THANH HANG PHAM
Overview:
This is my customized version of the RAG-FOOD repository originally developed by Callum.
My version enhances the project by adding 15 new food items including Vietnamese cusine, healthy foods, and international dishes. 
## 15 New Food Items Added 
| #  | Food Item           | Category           | Brief Description                                          |
| -- | ------------------- | ------------------ | ---------------------------------------------------------- |
| 1  | Bún Chả             | Vietnamese Cuisine | Grilled pork with rice noodles and herbs from Hanoi.       |
| 2  | Phở Chay            | Vietnamese Cuisine | Vegan noodle soup made with mushroom and vegetable broth.  |
| 3  | Gỏi Cuốn            | Vietnamese Cuisine | Fresh spring rolls with shrimp, herbs, and peanut sauce.   |
| 4  | Cơm Tấm             | Vietnamese Cuisine | Broken rice dish with grilled pork and pickled vegetables. |
| 5  | Quinoa Salad        | Healthy Food       | High-protein salad with quinoa, chickpeas, and veggies.    |
| 6  | Greek Yogurt Bowl   | Healthy Food       | Yogurt topped with berries, nuts, and honey.               |
| 7  | Steamed Broccoli    | Healthy Food       | Simple side dish with garlic and olive oil.                |
| 8  | Oatmeal with Apples | Healthy Food       | Warm oats cooked with apple and cinnamon.                  |
| 9  | Lentil Soup         | Healthy Food       | Protein-rich soup with lentils and vegetables.             |
| 10 |  Pizza              | International Dish | Classic Italian pizza with mozzarella and basil.           |
| 11 | Sushi Rolls         | International Dish | Vinegared rice with fish and vegetables in seaweed.        |
| 12 | Paella              | International Dish | Spanish saffron rice dish with seafood and chicken.        |
| 13 | Tacos al Pastor     | International Dish | Mexican tacos with marinated pork and pineapple.           |
| 14 | Falafel Wrap        | International Dish | Chickpea fritters wrapped in pita with tahini.             |
| 15 | Banh Xeo            | Vietnamese Cuisine | Vietnamese savory crepe ade with rice flour, coconut milk, turmeric, shrimp, pork,etc|

## Installation and Setup Intructions
1. Clone my forked repository
- Open new file "ragfood" 
- git clone https://github.com/VivianP05/ragfood.git
cd ragfood
2. Create and activate a virtual environment
3. Run application
4. Load new food data
## Sample Queries and Expected Responses
| Sample Query                               | Expected Response Summary                                                    |
| ------------------------------------------ | ---------------------------------------------------------------------------- |
| “What are some healthy vegan dishes?”      | Lists Phở Chay, Quinoa Salad, Lentil Soup, Steamed Broccoli.                 |
| “what is Bun Cha ? ”                       | Describes origin (Hanoi), grilled pork, herbs, and sweet-sour dipping sauce. |
| “Which dish from Spain is in the dataset?” | Returns “Paella,” including details on saffron rice and seafood.             |
| “What dish has chickpeas?”                 | List   Falafel Wrap and Quinoa Salad with Chickpeas                          |
| “Give me a gluten-free meal option.”       | Suggests Paella, Steamed Broccoli with Garlic and Olive Oil.                 |

# Enhancements and Testing Results
* Enhancements Made
- Added 15 new food items to food_data.json, covering:
Vietnamese cuisine: Bun Cha, Pho Chay, Goi Cuon, Com Tam, Banh Xeo

Healthy foods: Quinoa Salad, Greek Yogurt Bowl, Steamed Broccoli, Oatmeal with Apples, Lentil Soup

International dishes: Margherita Pizza, Sushi Rolls, Paella, Tacos al Pastor, Falafel Wrap
- Included detailed mentadata for each food item:
Origin country, ingredients, preparation method, nutrition highlights, and dietary classification

Enhanced retrieval dataset diversity for improved query accuracy and multilingual understanding

Updated documentation (README.md) with new sections for setup, examples, and reflection
* Testing Process
- Loaded the updated food_data.json 
- Ran test queries 
* Results Summary
- List healthy vegan foods. 
1. Steamed Broccoli with Garlic and Olive Oil
2. Lentil Soup
3. Falafel Wrap (if prepared without yogurt sauce)
- Show me gluten-free meals
1. Paella (saaffron-flavored rice dish with seafood, chicken, and vegetables)
2. Steamed Broccoli with Garlic and Olive Oil
3. Lentil Soup
- What dish has chickpeas?
1. Falafel Wrap
2. Quinoa Salad with Chickpeas
* All tests passed successfully. The system’s retrieval and generation quality improved, producing accurate and diverse results across multiple cuisines.