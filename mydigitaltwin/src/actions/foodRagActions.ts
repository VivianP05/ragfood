"use server";

import { Index } from "@upstash/vector";
import Groq from "groq-sdk";

/**
 * Food RAG Server Action
 * Searches Upstash Vector database for relevant food items
 * and generates AI responses using Groq
 */

// Initialize Upstash Vector Index
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

// Initialize Groq client
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY!,
});

/**
 * Query the Food RAG system
 * @param question - User's question about food, cuisines, recipes, or dietary information
 * @returns AI-generated response with relevant food context
 */
export async function queryFoodRAG(question: string): Promise<{
  success: boolean;
  answer?: string;
  error?: string;
  context?: string[];
  metadata?: {
    searchResults: number;
    model: string;
    processingTime: number;
  };
}> {
  const startTime = Date.now();

  try {
    // Validate input
    if (!question || question.trim().length === 0) {
      return {
        success: false,
        error: "Question cannot be empty",
      };
    }

    // Step 1: Search Upstash Vector for relevant food items
    console.log("🔍 Searching food database for:", question);
    
    const results = await index.query({
      data: question,
      topK: 3,
      includeMetadata: true,
    });

    console.log(`✅ Found ${results.length} relevant food items`);

    // Step 2: Extract context from search results
    const contextItems: string[] = [];
    
    results.forEach((result, idx) => {
      const metadata = result.metadata as Record<string, any>;
      
      // Handle both data formats (simple and detailed)
      let foodInfo: string;
      
      if (metadata.name) {
        // Detailed format
        foodInfo = `${metadata.name}: ${metadata.description || ""}`;
        if (metadata.origin) foodInfo += ` (Origin: ${metadata.origin})`;
        if (metadata.category) foodInfo += ` [${metadata.category}]`;
        if (metadata.ingredients) foodInfo += `\nIngredients: ${metadata.ingredients}`;
        if (metadata.cooking_method) foodInfo += `\nPreparation: ${metadata.cooking_method}`;
        if (metadata.dietary_tags) foodInfo += `\nDietary: ${metadata.dietary_tags}`;
      } else {
        // Simple format
        foodInfo = metadata.text || "";
        if (metadata.region) foodInfo += ` (${metadata.region})`;
        if (metadata.type) foodInfo += ` [${metadata.type}]`;
      }
      
      contextItems.push(foodInfo);
      console.log(`📍 Result ${idx + 1} (score: ${result.score?.toFixed(3)}):`, foodInfo.substring(0, 100));
    });

    const context = contextItems.join("\n\n");

    // Step 3: Generate AI response with Groq
    console.log("🤖 Generating AI response with Groq...");
    
    const completion = await groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content: `You are a helpful food expert assistant with deep knowledge of global cuisines, dishes, recipes, and dietary information. 

Use the provided food database context to answer questions accurately and enthusiastically. Include details about:
- Origins and cultural significance
- Key ingredients and flavors
- Preparation methods
- Dietary considerations
- Regional variations

Be conversational, informative, and encouraging. If the context doesn't contain exact information, use your knowledge to provide helpful general information while noting what's from the database vs general knowledge.`,
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

    const answer = completion.choices[0]?.message?.content || "No response generated.";
    const processingTime = Date.now() - startTime;

    console.log(`✨ Response generated in ${processingTime}ms`);

    return {
      success: true,
      answer,
      context: contextItems,
      metadata: {
        searchResults: results.length,
        model: "llama-3.1-8b-instant",
        processingTime,
      },
    };
  } catch (error) {
    console.error("❌ Error in queryFoodRAG:", error);
    
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error occurred",
    };
  }
}

/**
 * Search food database by category
 * @param category - Food category (e.g., "Main Course", "Dessert", "Fruit")
 * @param limit - Number of results to return
 */
export async function searchByCategory(
  category: string,
  limit: number = 5
): Promise<{
  success: boolean;
  results?: Array<{
    name: string;
    description: string;
    region?: string;
    type?: string;
  }>;
  error?: string;
}> {
  try {
    // Search with category-focused query
    const results = await index.query({
      data: `${category} food items`,
      topK: limit,
      includeMetadata: true,
    });

    const foodItems = results.map((result) => {
      const metadata = result.metadata as Record<string, any>;
      return {
        name: metadata.name || metadata.text || "Unknown",
        description: metadata.description || metadata.text || "",
        region: metadata.region || metadata.origin,
        type: metadata.type || metadata.category,
      };
    });

    return {
      success: true,
      results: foodItems,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

/**
 * Get food recommendations based on preferences
 * @param preferences - User preferences (e.g., "vegetarian", "spicy", "quick meals")
 */
export async function getFoodRecommendations(
  preferences: string
): Promise<{
  success: boolean;
  recommendations?: string;
  error?: string;
}> {
  try {
    // Search for foods matching preferences
    const results = await index.query({
      data: preferences,
      topK: 5,
      includeMetadata: true,
    });

    // Build context from results
    const foodList = results
      .map((r, idx) => {
        const metadata = r.metadata as Record<string, any>;
        const name = metadata.name || metadata.text;
        const desc = metadata.description || "";
        return `${idx + 1}. ${name}${desc ? `: ${desc}` : ""}`;
      })
      .join("\n");

    // Generate personalized recommendations
    const completion = await groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content:
            "You are a food recommendation expert. Provide personalized, enthusiastic recommendations based on user preferences.",
        },
        {
          role: "user",
          content: `User preferences: ${preferences}\n\nRelevant foods from our database:\n${foodList}\n\nProvide 3-5 personalized recommendations with brief explanations why they match the preferences.`,
        },
      ],
      model: "llama-3.1-8b-instant",
      temperature: 0.8,
      max_tokens: 400,
    });

    return {
      success: true,
      recommendations: completion.choices[0]?.message?.content || "No recommendations generated.",
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
