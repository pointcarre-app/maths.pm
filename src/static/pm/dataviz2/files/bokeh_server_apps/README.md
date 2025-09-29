# Bokeh Server Applications

This folder contains multiple Bokeh server applications demonstrating different interactive features that require a Bokeh server (not available in static Jupyter notebooks).

## Prerequisites

Make sure you have Bokeh installed:
```bash
pip install bokeh pandas numpy
```

## Running the Applications

Each script can be run independently using the Bokeh server:

### Method 1: Run Individual Apps

```bash
# Navigate to this directory
cd bokeh_server_apps

# Run any individual app
bokeh serve 01_simple_slider.py
bokeh serve 02_multiple_controls.py
bokeh serve 03_real_time_streaming.py
bokeh serve 04_interactive_data_table.py
bokeh serve 05_linked_plots.py
```

Then open your browser to: `http://localhost:5006/[script_name]`

For example:
- `http://localhost:5006/01_simple_slider`
- `http://localhost:5006/02_multiple_controls`

### Method 2: Run All Apps Together

You can serve multiple apps at once:

```bash
bokeh serve 01_simple_slider.py 02_multiple_controls.py 03_real_time_streaming.py 04_interactive_data_table.py 05_linked_plots.py 06_interactive_presentation.py
```

This will make all apps available at:
- `http://localhost:5006/01_simple_slider`
- `http://localhost:5006/02_multiple_controls`
- `http://localhost:5006/03_real_time_streaming`
- `http://localhost:5006/04_interactive_data_table`
- `http://localhost:5006/05_linked_plots`
- `http://localhost:5006/06_interactive_presentation`

### Method 3: Run Entire Directory

```bash
bokeh serve bokeh_server_apps/*.py
```

## Application Descriptions

### 1. **01_simple_slider.py** - Basic Slider Interaction
- Single amplitude slider controlling a sine wave
- Real-time plot updates
- Console logging of changes

### 2. **02_multiple_controls.py** - Complex Control Panel
- Multiple sliders (amplitude, frequency, phase)
- Select dropdowns for function and line style
- Checkboxes for display options
- Real-time info display
- Demonstrates various Bokeh widgets

### 3. **03_real_time_streaming.py** - Live Data Streaming
- Start/stop streaming controls
- Adjustable update rate
- Window size control
- Real-time statistics
- Demonstrates periodic callbacks

### 4. **04_interactive_data_table.py** - Data Table Integration
- Interactive scatter plot linked to data table
- Filter controls (category, value)
- Add/remove data points
- Selection synchronization
- Live statistics update

### 5. **05_linked_plots.py** - Linked Selection Across Plots
- Four scatter plots with shared data source
- Box and lasso selection tools
- Selection linked across all plots
- Histogram of selected data
- Statistics table for selected points

### 6. **06_interactive_presentation.py** - Full Presentation System 🆕
- Complete presentation framework with 6 slides
- Navigation controls (prev/next/jump to slide)
- Auto-play mode for hands-free presentation
- Progress bar and slide selector
- Multiple interactive visualizations per slide:
  - Welcome slide with animated scatter plot
  - Data overview dashboard with bar, line, and heatmap
  - Interactive function explorer with controls
  - Time series analysis with moving averages
  - Correlation matrix heatmap
  - Conclusions with summary cards
- Each slide contains fully interactive Bokeh plots

## Key Differences from Notebook Bokeh

These server apps demonstrate features NOT available in static notebook output:

1. **Python Callbacks**: Real-time Python function execution
2. **Periodic Updates**: Streaming and animated data
3. **Two-way Communication**: Widgets that update plots and vice versa
4. **Shared State**: Multiple plots sharing selections and data
5. **Dynamic Data**: Add/remove/filter data on the fly
6. **Server-side Processing**: Complex calculations in Python

## Custom Port

To run on a different port:
```bash
bokeh serve --port 5007 01_simple_slider.py
```

## Allow External Connections

To allow connections from other machines:
```bash
bokeh serve --allow-websocket-origin="*" 01_simple_slider.py
```

## Development Mode

For development with auto-reload on file changes:
```bash
bokeh serve --dev 01_simple_slider.py
```

## Troubleshooting

1. **Port already in use**: Kill existing Bokeh server or use different port
2. **Module not found**: Ensure all required packages are installed
3. **No display**: Check browser console for JavaScript errors
4. **Slow updates**: Adjust update rates in streaming apps

## Notes

- These apps require an active Bokeh server connection
- Closing the browser doesn't stop the server (use Ctrl+C)
- Each app maintains its own state
- Console output appears in the terminal, not the browser
