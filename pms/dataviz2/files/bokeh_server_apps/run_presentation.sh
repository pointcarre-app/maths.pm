#!/bin/bash
# Quick launcher for the Interactive Presentation
# Usage: ./run_presentation.sh

echo "🎯 Starting Interactive Presentation App..."
echo "==========================================="
echo ""
echo "The presentation will be available at:"
echo "  📊 http://localhost:5006/06_interactive_presentation"
echo ""
echo "Features:"
echo "  • 6 interactive slides"
echo "  • Navigation controls"
echo "  • Auto-play mode"
echo "  • Multiple visualizations per slide"
echo "  • All plots are fully interactive!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "==========================================="
echo ""

bokeh serve 06_interactive_presentation.py --port 5006 --show
