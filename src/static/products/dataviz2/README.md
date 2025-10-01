# DataViz2 Product Assets

This folder contains all static assets for the DataViz2 product.

## Structure

```
dataviz2/
├── js/
│   ├── main.js           # Main DataViz2 runtime with Nagini integration
│   └── bokeh-detector.js # Bokeh library detection utility
├── css/
│   ├── pm.css           # Core PM styles
│   ├── toc.css          # Table of contents styles
│   └── dataviz2.css     # DataViz2-specific styles
└── README.md            # This file
```

## Configuration

These assets are referenced in `products/04_dataviz2.yml`:

```yaml
backend_settings:
  js_dependencies:
    - "/static/products/dataviz2/js/bokeh-detector.js"
    - "/static/products/dataviz2/js/main.js"
  css_dependencies:
    - "/static/products/dataviz2/css/pm.css"
    - "/static/products/dataviz2/css/toc.css"
    - "/static/products/dataviz2/css/dataviz2.css"
```

## Features

- **Interactive Python Execution**: Uses Nagini to run Python code in the browser
- **Bokeh Support**: Automatic detection and rendering of Bokeh plots
- **Matplotlib Support**: Renders matplotlib figures as images
- **Error Handling**: Comprehensive error display for Python execution
- **Editable Code**: CodeMirror integration for code editing

## Dependencies

- Nagini v0.0.24 (loaded dynamically)
- Pyodide (via Nagini)
- CodeMirror (provided by PM runtime)
- BokehJS (optional, loaded via PM metadata)

## Usage

The DataViz2 product automatically activates for PM pages under `/pm/dataviz2/`.
When active, it:

1. Makes code blocks editable
2. Adds execution buttons
3. Handles Python code execution
4. Renders outputs (text, plots, errors)
