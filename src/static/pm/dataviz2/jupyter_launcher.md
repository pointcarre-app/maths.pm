---
title: JupyterLite Data Visualization Launcher
description: Direct access to interactive Jupyter notebooks for data visualization
chapter: Interactive Tools

# Page-specific metatags
title: "JupyterLite Launcher - Interactive Data Visualization"
description: "Direct access to Jupyter notebooks with data visualization examples and datasets"
keywords: "jupyter, python, data visualization, interactive, notebooks"
author: "Maths.pm - DataViz Team"
robots: "index, follow"

# Open Graph metatags
og:title: "JupyterLite Launcher"
og:description: "Interactive Jupyter environment for data visualization"
og:type: "application"
og:url: "https://maths.pm/pm/dataviz2/jupyter_launcher.md"

# Twitter Card metatags
twitter:card: "summary"
twitter:title: "JupyterLite Launcher"
twitter:description: "Interactive Python environment"

# Additional metatags
topic: "Interactive Tools"
category: "Data Visualization, Python"
revised: "2025-01-15"
pagename: "JupyterLite Launcher"

---

# 🚀 JupyterLite Data Visualization Launcher

Interactive Python environment with pre-loaded datasets and visualization examples.

## 📊 **Quick Start Notebooks**

## 🚀 **DIRECT ACCESS LINKS** (No JavaScript Required)

**[📋 Simple Direct Access Page](http://localhost:8000/static/jupyter_direct.html)** - Guaranteed to work!

### Individual Notebooks:
- **[🔬 Corsica Data Analysis](http://localhost:8000/static/jupyterlite/_output/lab/index.html?path=corsica_a_0_transform_data.ipynb&cache=false&nocache=1&direct=true)** - Geographic data transformation
- **[📈 P5.js Graphics](http://localhost:8000/static/jupyterlite/_output/lab/index.html?path=p5js_example.ipynb&cache=false&nocache=1&direct=true)** - Interactive visualizations  
- **[🐍 Python Examples](http://localhost:8000/static/jupyterlite/_output/lab/index.html?path=python_example.ipynb&cache=false&nocache=1&direct=true)** - Basic data visualization
- **[🧪 Test Environment](http://localhost:8000/static/jupyterlite/_output/lab/index.html?path=notebook_test.ipynb&cache=false&nocache=1&direct=true)** - Sandbox for experiments

### Alternative Interfaces:
- **[🔬 Full JupyterLite Lab](http://localhost:8000/static/jupyterlite/_output/lab/index.html?cache=false&nocache=1)** - Complete interface
- **[📂 File Browser](http://localhost:8000/static/jupyterlite/_output/tree/index.html?cache=false&nocache=1)** - Browse all files
- **[💻 Python REPL](http://localhost:8000/static/jupyterlite/_output/repl/index.html?cache=false&nocache=1)** - Quick Python console

## 🔧 **Alternative Access Methods**

### Direct Links (No Cache)
- **[🔬 JupyterLite Lab](http://localhost:8000/static/jupyterlite/_output/lab/index.html?cache=false&t={timestamp})** - Full Lab interface
- **[📂 File Browser](http://localhost:8000/static/jupyterlite/_output/tree/index.html?cache=false)** - Browse all files
- **[💻 Python REPL](http://localhost:8000/static/jupyterlite/_output/repl/index.html?cache=false)** - Quick Python console

### Production URLs (For deployment)
- **[🌐 Production Lab](https://maths.pm/static/jupyterlite/_output/lab/index.html)** - Deployed version
- **[🌐 Production Files](https://maths.pm/static/jupyterlite/_output/tree/index.html)** - Deployed file browser

## 📁 **Available Datasets**

### Geographic Data
- **Corsica Maps**: `data/processed/corsica/`
  - PNG images: Grid maps at different resolutions
  - SVG vectors: Scalable geographic representations
- **GeoJSON**: `data/raw/geojson/france/region.json`
  - French regional boundaries

### Example Files
- **Jupyter Notebooks**: `.ipynb` files with examples
- **Vector Graphics**: `.svg` files for visualization
- **Data Files**: JSON, CSV, and other formats

## 🛠️ **Troubleshooting**

### If notebooks don't load:
1. **Clear browser cache** (Ctrl+F5 or Cmd+Shift+R)
2. **Try incognito/private mode**
3. **Use direct links** with cache-busting parameters
4. **Check browser console** for errors

### Cache Issues:
- Links include `?cache=false` to bypass caching
- Timestamps added for unique URLs
- Service worker cache is disabled

<script>
// Get current timestamp for cache busting
function getTimestamp() {
    return new Date().getTime();
}

// Get base URL
function getBaseUrl() {
    return window.location.protocol + '//' + window.location.host;
}

// Open specific notebook
function openJupyter(filename) {
    const baseUrl = getBaseUrl();
    const timestamp = getTimestamp();
    const randomId = Math.random().toString(36).substr(2, 9);
    const jupyterUrl = `${baseUrl}/static/jupyterlite/_output/lab/index.html?path=${filename}&cache=false&t=${timestamp}&nocache=1&r=${randomId}`;
    
    console.log('Opening JupyterLite:', filename, 'URL:', jupyterUrl);
    window.open(jupyterUrl, '_blank');
    
    // Fallback: try direct access if the first fails
    setTimeout(() => {
        console.log('Fallback URL available:', jupyterUrl);
    }, 1000);
}

// Alternative function names for compatibility
window.openNotebook = openJupyter;
window.openJupyterNotebook = openJupyter;

// Add timestamp to direct links on page load
document.addEventListener('DOMContentLoaded', function() {
    const timestamp = new Date().getTime();
    const links = document.querySelectorAll('a[href*="jupyterlite"]');
    
    links.forEach(link => {
        const url = new URL(link.href);
        url.searchParams.set('t', timestamp);
        url.searchParams.set('cache', 'false');
        link.href = url.toString();
    });
});
</script>

<style>
.jupyter-launcher {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    text-align: center;
}

.jupyter-launcher a {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 5px;
    display: inline-block;
    margin: 5px;
    backdrop-filter: blur(10px);
}

.jupyter-launcher a:hover {
    background: rgba(255,255,255,0.3);
}
</style>
