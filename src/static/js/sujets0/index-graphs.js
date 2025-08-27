// Import PCAGraphLoader from CDN
import {
    PCAGraphLoader
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/v4.py.js@v0.0.18-unstable/scenery/packaged/PCAGraphLoader.js';

// Make PCAGraphLoader available globally for use in your application
// window.PCAGraphLoader = PCAGraphLoader;



// Helper function to render a graph into a container
export async function buildPCAGraph(graphKey, config = {}) {

    try {
        // Create or reuse loader instance
        if (!window._pcaLoader) {
            window._pcaLoader = new PCAGraphLoader({
                debug: false,
                graphConfig: config
            });
            await window._pcaLoader.initialize();
        } else if (config && Object.keys(config).length > 0) {
            // Update config if provided
            window._pcaLoader.updateConfig(config);
        }

        // Render the graph (returns {svg, graphDict})
        const result = await window._pcaLoader.renderGraph(graphKey);

        return result;


    } catch (error) {
        container.innerHTML = `<div class="pca-graph-error">Error loading graph: ${error.message}</div>`;
        console.error('PCA Graph Error:', error);
    }
};




// Helper function to render a graph into a container
export async function renderPCAGraph(containerId, graphKey, config = {}) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container with id '${containerId}' not found`);
        return;
    }

    // Add loading state
    container.innerHTML = '<div class="pca-graph-loading">Loading graph...</div>';
    container.className = 'pca-graph-container';

    try {
        // Create or reuse loader instance
        if (!window._pcaLoader) {
            window._pcaLoader = new PCAGraphLoader({
                debug: false,
                graphConfig: config
            });
            await window._pcaLoader.initialize();
        } else if (config && Object.keys(config).length > 0) {
            // Update config if provided
            window._pcaLoader.updateConfig(config);
        }

        // Render the graph (returns {svg, graphDict})
        const result = await window._pcaLoader.renderGraph(graphKey);

        // Create proper frame structure
        const frameDiv = document.createElement('div');
        frameDiv.className = 'pca-graph-frame';
        frameDiv.innerHTML = result.svg;

        container.innerHTML = '';
        container.appendChild(frameDiv);

        // Store graph dictionary as data attribute for access if needed
        container.dataset.graphDict = JSON.stringify(result.graphDict);

        // Render LaTeX if KaTeX is available
        if (typeof katex !== 'undefined') {
            setTimeout(() => {
                const foreignObjects = container.querySelectorAll('foreignObject');
                foreignObjects.forEach((fo) => {
                    const divs = fo.querySelectorAll('div.svg-latex');
                    divs.forEach((div) => {
                        const latex = div.textContent.trim();
                        if (latex) {
                            try {
                                const bgColor = div.style.backgroundColor;
                                const color = div.style.color;
                                div.innerHTML = '';
                                katex.render(latex, div, {
                                    throwOnError: false,
                                    displayMode: false,
                                });
                                if (bgColor) div.style.backgroundColor = bgColor;
                                if (color) {
                                    div.querySelectorAll('.katex, .katex *').forEach(el => {
                                        el.style.color = color;
                                    });
                                }
                            } catch (e) {
                                console.error('KaTeX error:', e);
                                div.textContent = latex;
                            }
                        }
                    });
                });
            }, 100);
        }

    } catch (error) {
        container.innerHTML = `<div class="pca-graph-error">Error loading graph: ${error.message}</div>`;
        console.error('PCA Graph Error:', error);
    }
};

// Log availability
console.log('✅ PCAGraphLoader ready. Use window.renderPCAGraph(containerId, graphKey, config) to render graphs.');


