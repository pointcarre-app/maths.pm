#!/bin/bash
# Launcher script for Bokeh server apps
# Usage: ./run_all.sh

echo "Starting Bokeh Server with all applications..."
echo "==========================================="
echo ""
echo "Applications will be available at:"
echo "  • http://localhost:5006/01_simple_slider"
echo "  • http://localhost:5006/02_multiple_controls"
echo "  • http://localhost:5006/03_real_time_streaming"
echo "  • http://localhost:5006/04_interactive_data_table"
echo "  • http://localhost:5006/05_linked_plots"
echo "  • http://localhost:5006/06_interactive_presentation  🆕 PRESENTATION!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "==========================================="
echo ""

bokeh serve \
    01_simple_slider.py \
    02_multiple_controls.py \
    03_real_time_streaming.py \
    04_interactive_data_table.py \
    05_linked_plots.py \
    06_interactive_presentation.py \
    --port 5006
