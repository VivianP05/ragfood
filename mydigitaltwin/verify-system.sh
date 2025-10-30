#!/bin/bash

# Food RAG MCP Server - System Verification Script
# Run this to verify your setup is correct

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         🔍 Food RAG System Verification Script 🔍             ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to check and report
check() {
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED++))
  else
    echo -e "${RED}❌ $1${NC}"
    ((FAILED++))
  fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  CHECKING PROJECT STRUCTURE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd /Users/DELL/ragfood/mydigitaltwin

# Check directories
test -d "src/actions"
check "src/actions/ directory exists"

test -d "src/mcp-server"
check "src/mcp-server/ directory exists"

test -d "app/api/query"
check "app/api/query/ directory exists"

# Check files
test -f "src/actions/foodRagActions.ts"
check "foodRagActions.ts exists"

test -f "src/mcp-server/index.ts"
check "MCP server index.ts exists"

test -f "tsconfig.mcp.json"
check "tsconfig.mcp.json exists"

test -f ".env.local"
check ".env.local exists"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  CHECKING ENVIRONMENT VARIABLES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Source .env.local
if [ -f .env.local ]; then
  source .env.local
fi

test -n "$UPSTASH_VECTOR_REST_URL"
check "UPSTASH_VECTOR_REST_URL is set"

test -n "$UPSTASH_VECTOR_REST_TOKEN"
check "UPSTASH_VECTOR_REST_TOKEN is set"

test -n "$GROQ_API_KEY"
check "GROQ_API_KEY is set"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  CHECKING NPM DEPENDENCIES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

npm list @upstash/vector --depth=0 > /dev/null 2>&1
check "@upstash/vector installed"

npm list groq-sdk --depth=0 > /dev/null 2>&1
check "groq-sdk installed"

npm list @modelcontextprotocol/sdk --depth=0 > /dev/null 2>&1
check "@modelcontextprotocol/sdk installed"

npm list next --depth=0 > /dev/null 2>&1
check "Next.js installed"

npm list react --depth=0 > /dev/null 2>&1
check "React installed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  CHECKING BUILD STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test -d "dist/mcp-server"
check "MCP server dist/ directory exists"

test -f "dist/mcp-server/index.js"
check "MCP server compiled (index.js)"

test -f "dist/mcp-server/index.d.ts"
check "MCP server types (index.d.ts)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  CHECKING TYPESCRIPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if TypeScript compiles without errors
npx tsc --noEmit > /dev/null 2>&1
check "TypeScript compilation (no errors)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  CHECKING DOCUMENTATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test -f "MCP_SERVER_SETUP.md"
check "MCP_SERVER_SETUP.md exists"

test -f "MCP_IMPLEMENTATION.md"
check "MCP_IMPLEMENTATION.md exists"

test -f "QUICK_REFERENCE.md"
check "QUICK_REFERENCE.md exists"

test -f "TROUBLESHOOTING.md"
check "TROUBLESHOOTING.md exists"

test -f "../agents.md"
check "agents.md exists in parent directory"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 VERIFICATION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo -e "Total Checks: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo -e "Success Rate: $PERCENTAGE%"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo -e "${GREEN}🎉 ALL CHECKS PASSED! System is ready to use! 🎉${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Next steps:"
  echo "  1. Start the web UI:"
  echo "     npm run dev"
  echo ""
  echo "  2. Visit: http://localhost:3000"
  echo ""
  echo "  3. Try: 'What is Biryani?'"
  echo ""
else
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo -e "${YELLOW}⚠️  SOME CHECKS FAILED${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "See TROUBLESHOOTING.md for solutions"
  echo ""
  echo "Quick fixes:"
  echo "  1. Install dependencies: npm install"
  echo "  2. Build MCP server: npm run build:mcp"
  echo "  3. Check environment: cat .env.local"
  echo ""
fi

exit $FAILED
