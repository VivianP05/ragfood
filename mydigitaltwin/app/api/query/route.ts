import { NextRequest, NextResponse } from 'next/server';
import { queryFoodRAG } from '../../../src/actions/foodRagActions';

export async function POST(request: NextRequest) {
  try {
    const { question } = await request.json();

    if (!question || typeof question !== 'string') {
      return NextResponse.json(
        { error: 'Question is required and must be a string' },
        { status: 400 }
      );
    }

    // Use the server action to query Food RAG
    const result = await queryFoodRAG(question);

    if (!result.success) {
      return NextResponse.json(
        { error: result.error || 'Unknown error from RAG system' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      question: question,
      answer: result.answer,
      metadata: result.metadata,
    });

  } catch (error: unknown) {
    console.error('API Error:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json(
      { 
        error: 'Failed to process query',
        details: errorMessage 
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'RAG Query API',
    usage: 'POST with { "question": "your question" }',
    example: {
      question: 'What is Biryani?'
    }
  });
}
