import { NextRequest, NextResponse } from 'next/server';
import { queryResumeRAG } from '../../../src/actions/resumeRagActions';

export async function POST(request: NextRequest) {
  try {
    const { question } = await request.json();

    if (!question || typeof question !== 'string') {
      return NextResponse.json(
        { error: 'Question is required and must be a string' },
        { status: 400 }
      );
    }

    // Use the resume RAG server action
    const result = await queryResumeRAG(question);

    if (!result.success) {
      return NextResponse.json(
        { error: result.error || 'Unknown error from RAG system' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      question: question,
      answer: result.answer,
      sources: result.sources,
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
    message: 'Resume RAG Query API',
    usage: 'POST with { "question": "your question" }',
    example: {
      question: 'What is Vivian\'s Tableau experience?'
    }
  });
}
