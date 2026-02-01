#!/bin/bash

# Frontend Test Script for AptiFy
# Tests the authentication flow

echo "=========================================="
echo "AptiFy Frontend Authentication Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test URLs
FRONTEND_URL="http://127.0.0.1:3000"
LOGIN_PAGE="$FRONTEND_URL/templates/login.html"
DASHBOARD_PAGE="$FRONTEND_URL/templates/dashboard.html"
INDEX_PAGE="$FRONTEND_URL/templates/index.html"

echo -e "${YELLOW}Test 1: Verify frontend server is running${NC}"
if curl -s "$FRONTEND_URL/" > /dev/null; then
    echo -e "${GREEN}✓ Frontend server is running on port 3000${NC}"
else
    echo -e "${RED}✗ Frontend server is not responding${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}Test 2: Check index.html is accessible${NC}"
if curl -s "$INDEX_PAGE" | grep -q "AptiFy - Loading"; then
    echo -e "${GREEN}✓ index.html loads successfully${NC}"
else
    echo -e "${RED}✗ index.html not found or invalid${NC}"
fi
echo ""

echo -e "${YELLOW}Test 3: Check login.html is accessible${NC}"
if curl -s "$LOGIN_PAGE" | grep -q "Sign In"; then
    echo -e "${GREEN}✓ login.html loads successfully${NC}"
else
    echo -e "${RED}✗ login.html not found or invalid${NC}"
fi
echo ""

echo -e "${YELLOW}Test 4: Check dashboard.html is accessible${NC}"
if curl -s "$DASHBOARD_PAGE" | grep -q "Welcome to AptiFy"; then
    echo -e "${GREEN}✓ dashboard.html loads successfully${NC}"
else
    echo -e "${RED}✗ dashboard.html not found or invalid${NC}"
fi
echo ""

echo -e "${YELLOW}Test 5: Check auth-guard.js is accessible${NC}"
if curl -s "$FRONTEND_URL/static/js/auth-guard.js" | grep -q "AuthGuard"; then
    echo -e "${GREEN}✓ auth-guard.js loads successfully${NC}"
else
    echo -e "${RED}✗ auth-guard.js not found${NC}"
fi
echo ""

echo -e "${YELLOW}Test 6: Check login.js is accessible${NC}"
if curl -s "$FRONTEND_URL/static/js/login.js" | grep -q "loginForm"; then
    echo -e "${GREEN}✓ login.js loads successfully${NC}"
else
    echo -e "${RED}✗ login.js not found${NC}"
fi
echo ""

echo -e "${YELLOW}Test 7: Check dashboard.js is accessible${NC}"
if curl -s "$FRONTEND_URL/static/js/dashboard.js" | grep -q "requireAuth"; then
    echo -e "${GREEN}✓ dashboard.js loads successfully${NC}"
else
    echo -e "${RED}✗ dashboard.js not found${NC}"
fi
echo ""

echo -e "${YELLOW}Test 8: Check styles.css is accessible${NC}"
if curl -s "$FRONTEND_URL/static/css/styles.css" | grep -q "color-primary"; then
    echo -e "${GREEN}✓ styles.css loads successfully${NC}"
else
    echo -e "${RED}✗ styles.css not found${NC}"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}All tests completed!${NC}"
echo "=========================================="
echo ""
echo "Frontend URLs:"
echo "  - Index (Entry Gate): $INDEX_PAGE"
echo "  - Login Page: $LOGIN_PAGE"
echo "  - Dashboard: $DASHBOARD_PAGE"
echo ""
echo "Demo Credentials:"
echo "  - Email: demo@aptify.com"
echo "  - Password: demo123"
echo ""
