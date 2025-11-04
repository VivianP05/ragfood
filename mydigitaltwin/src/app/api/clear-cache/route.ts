import { NextResponse } from 'next/server';
import { clearCache } from '@/src/actions/foodRagActions';

/**
 * POST /api/clear-cache
 * 
 * Clears the response cache
 */
export async function POST() {
  try {
    const result = await clearCache();
    
    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    );
  }
}
