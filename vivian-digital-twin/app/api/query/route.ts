import { NextRequest, NextResponse } from 'next/server';
import { Index } from '@upstash/vector';
import Groq from 'groq-sdk';

// Initialize Upstash Vector client
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

// Initialize Groq client
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY!,
});

export async function POST(request: NextRequest) {
  try {
    const { question } = await request.json();

    if (!question || typeof question !== 'string') {
      return NextResponse.json(
        { success: false, error: 'Question is required and must be a string' },
        { status: 400 }
      );
    }

    // Search Upstash Vector for relevant profile information
    const results = await index.query({
      data: question,
      topK: 3,
      includeMetadata: true,
    });

    // Extract context from search results
    const context = results
      .map((result) => {
        // Handle different metadata formats
        const metadata = result.metadata as Record<string, unknown>;
        
        // For profile data with text field
        if (metadata?.text) {
          return `${metadata.text}`;
        }
        
        // For profile data with name and description
        if (metadata?.name && metadata?.description) {
          return `${metadata.name}: ${metadata.description}`;
        }
        
        // For profile data with category and content
        if (metadata?.category && metadata?.content) {
          return `${metadata.category}: ${metadata.content}`;
        }
        
        // Fallback: stringify the entire metadata
        return JSON.stringify(metadata);
      })
      .join('\n\n');

    // Generate response using Groq
    const completion = await groq.chat.completions.create({
      messages: [
        {
          role: 'system',
          content: `You are Vivian Pham's digital twin assistant. You have access to Vivian's professional profile, including her skills, experience, projects, and career goals. 

Your role is to answer questions about Vivian's professional background accurately and enthusiastically. Use the provided context to give detailed, specific answers. If the context doesn't contain the information needed, acknowledge that honestly.

Key information about Vivian:
- AI Data Analyst with expertise in Excel (Level 5), Power BI, Python, SQL, and TypeScript
- Australian citizen, available for immediate start
- Salary expectations: $500-600/day for contracts, $55k-$70k for permanent roles
- Proven experience in data quality automation, KPI dashboards, and RAG systems
- Strong communication, problem-solving, and learning agility skills

When answering:
1. Be professional but friendly
2. Provide specific examples from her projects when relevant
3. Highlight her technical skills and achievements
4. Be honest if you don't have specific information`,
        },
        {
          role: 'user',
          content: `Context from Vivian's Profile:\n${context}\n\nQuestion: ${question}`,
        },
      ],
      model: 'llama-3.1-8b-instant',
      temperature: 0.7,
      max_tokens: 500,
    });

    const answer = completion.choices[0]?.message?.content || 'Sorry, I could not generate a response.';

    return NextResponse.json({
      success: true,
      question,
      answer,
    });

  } catch (error) {
    console.error('Error processing query:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'An unknown error occurred',
        question: '',
      },
      { status: 500 }
    );
  }
}
