#!/bin/bash
# Test script for static site generation
# Run this before pushing to ensure the build will work in GitHub Actions

set -e  # Exit on error

echo "🧪 Testing static site build locally..."
echo "======================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source env/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Run the build script
echo "🏗️ Starting build process..."
python scripts/build_static.py

# Check if dist directory was created
if [ -d "dist" ]; then
    echo ""
    echo "✅ Build successful!"
    echo "📊 Build statistics:"
    echo "  - Total size: $(du -sh dist | cut -f1)"
    echo "  - File count: $(find dist -type f | wc -l) files"
    echo "  - Directory count: $(find dist -type d | wc -l) directories"
    echo ""
    echo "📁 Main directories in dist/:"
    ls -la dist/ | head -10
    echo ""
    echo "💡 To test the static site locally, run:"
    echo "   python -m http.server 8080 -d dist"
    echo ""
else
    echo "❌ Build failed - dist directory not created"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo "🎉 Test complete!"
