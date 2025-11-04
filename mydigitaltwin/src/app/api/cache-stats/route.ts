import { NextResponse } from 'next/server';
import { getCacheStats } from '@/src/actions/foodRagActions';

/**
 * GET /api/cache-stats
 * 
 * Returns current cache statistics
 */
export async function GET() {
  try {
    const result = await getCacheStats();
    
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
