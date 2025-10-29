import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { question } = await request.json();

    if (!question || typeof question !== 'string') {
      return NextResponse.json(
        { error: 'Question is required and must be a string' },
        { status: 400 }
      );
    }

    // Path to the Python script (go up to parent ragfood directory)
    const scriptPath = path.join(process.cwd(), '..', 'rag_api.py');
    
    // Execute Python script with the question
    const { stdout, stderr } = await execAsync(
      `python3 "${scriptPath}" "${question.replace(/"/g, '\\"')}"`,
      {
        cwd: path.join(process.cwd(), '..'),
        timeout: 30000, // 30 second timeout
      }
    );

    if (stderr && !stdout) {
      console.error('Python stderr:', stderr);
      return NextResponse.json(
        { error: 'Error executing RAG query', details: stderr },
        { status: 500 }
      );
    }

    // Parse the JSON response from Python
    const result = JSON.parse(stdout);

    if (!result.success) {
      return NextResponse.json(
        { error: result.error || 'Unknown error from RAG system' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      question: result.question,
      answer: result.answer,
    });

  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to process query',
        details: error.message 
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
