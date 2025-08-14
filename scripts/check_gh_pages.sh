#!/bin/bash
# Script to check the gh-pages branch structure

echo "🔍 Checking gh-pages branch structure..."

# Save current branch
CURRENT_BRANCH=$(git branch --show-current)

# Fetch gh-pages branch
echo "📥 Fetching gh-pages branch..."
git fetch origin gh-pages

# Check if gh-pages exists
if git show-ref --verify --quiet refs/remotes/origin/gh-pages; then
    echo "✅ gh-pages branch exists"
    
    # List files in gh-pages branch
    echo ""
    echo "📁 Files in gh-pages branch root:"
    git ls-tree --name-only origin/gh-pages | head -20
    
    echo ""
    echo "📊 File count in gh-pages:"
    git ls-tree -r --name-only origin/gh-pages | wc -l
    
    # Check if index.html exists
    if git ls-tree --name-only origin/gh-pages | grep -q "^index.html$"; then
        echo "✅ index.html found in root"
    else
        echo "❌ index.html NOT found in root - this is the problem!"
    fi
else
    echo "❌ gh-pages branch does not exist!"
fi

echo ""
echo "📍 Current branch: $CURRENT_BRANCH"
echo "🌐 Your site should be available at: https://pointcarre-app.github.io/maths.pm/"
echo ""
echo "💡 If index.html is missing or in wrong location, the deployment needs to be fixed."
