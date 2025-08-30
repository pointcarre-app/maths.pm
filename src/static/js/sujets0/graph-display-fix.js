/**
 * Graph Display Fix Module
 * Handles proper display of SVG graphs with correct div structure
 * and browser-specific rendering (Safari vs others)
 */

import { isSafari } from './index-svg-converter.js';

/**
 * Process and display graph with proper structure
 * @param {Object} question - Question object containing graph data
 * @param {string} processedStatement - Processed question statement HTML
 * @param {number} questionNum - Question number
 * @returns {string} HTML string with properly structured graph display
 */
export function createGraphDisplay(question, processedStatement, questionNum) {
    if (!question.graphSvg) {
        // No graph - just return the statement
        return processedStatement;
    }
    
    // Get dimensions from graphDict or use defaults
    const dimensions = {
        width: question.graphDict?.svg?.width || 340,
        height: question.graphDict?.svg?.height || 340
    };
    
    const isInSafari = isSafari();
    
    // For Safari or when PNG is not available, use SVG directly
    if (isInSafari || !question.graphPng) {
        console.log(`Using SVG for question ${questionNum} (Safari: ${isInSafari})`);
        
        // Use raw SVG - LaTeX will be rendered after display
        // Process SVG to ensure proper display
        const processedSvg = processSvgForDisplay(question.graphSvg, dimensions, isInSafari);
        
        return `
            <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
                <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
                <div style='flex: 0 1 auto; display: flex; align-items: center; justify-content: center;'>
                    <div class="graph-svg-container" style="position: relative; width: ${dimensions.width}px; height: ${dimensions.height}px; overflow: visible;">
                        ${processedSvg}
                    </div>
                </div>
            </div>
        `;
    } else {
        // Use PNG for non-Safari browsers
        console.log(`Using PNG for question ${questionNum}`);
        
        // Scale down for display if needed
        const maxDisplaySize = 200;
        let displayWidth = dimensions.width;
        let displayHeight = dimensions.height;
        
        if (displayWidth > maxDisplaySize || displayHeight > maxDisplaySize) {
            const scale = Math.min(maxDisplaySize / displayWidth, maxDisplaySize / displayHeight);
            displayWidth = Math.round(displayWidth * scale);
            displayHeight = Math.round(displayHeight * scale);
        }
        
        return `
            <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
                <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
                <div style='flex: 0 1 auto; display: flex; align-items: center; justify-content: center;'>
                    <img src="${question.graphPng}" 
                         style="width: ${displayWidth}px; height: ${displayHeight}px; object-fit: contain; display: block;"
                         alt="Graphique question ${questionNum}" />
                </div>
            </div>
        `;
    }
}

/**
 * Process SVG for proper display
 * @param {string} svgString - Original SVG string
 * @param {Object} dimensions - Width and height dimensions
 * @param {boolean} isInSafari - Whether browser is Safari
 * @returns {string} Processed SVG string
 */
function processSvgForDisplay(svgString, dimensions, isInSafari) {
    try {
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
        const svgElement = svgDoc.querySelector('svg');
        
        if (!svgElement) {
            return svgString;
        }
        
        // Set explicit dimensions
        svgElement.setAttribute('width', dimensions.width);
        svgElement.setAttribute('height', dimensions.height);
        
        // Ensure viewBox is set for proper scaling
        if (!svgElement.getAttribute('viewBox')) {
            svgElement.setAttribute('viewBox', `0 0 ${dimensions.width} ${dimensions.height}`);
        }
        
        // Add inline styles for consistent display
        svgElement.style.width = `${dimensions.width}px`;
        svgElement.style.height = `${dimensions.height}px`;
        svgElement.style.display = 'block';
        svgElement.style.maxWidth = '100%';
        svgElement.style.height = 'auto';
        
        // Fix text elements for Safari
        if (isInSafari) {
            const textElements = svgElement.querySelectorAll('.text-2xs, .text-xs, .text-sm');
            textElements.forEach(el => {
                if (el.classList.contains('text-2xs')) {
                    el.style.fontSize = '0.625rem';
                    el.style.lineHeight = '1';
                } else if (el.classList.contains('text-xs')) {
                    el.style.fontSize = '0.75rem';
                    el.style.lineHeight = '1rem';
                } else if (el.classList.contains('text-sm')) {
                    el.style.fontSize = '0.875rem';
                    el.style.lineHeight = '1.25rem';
                }
            });
        }
        
        // Fix foreign objects for proper LaTeX positioning
        const foreignObjects = svgElement.querySelectorAll('foreignObject');
        foreignObjects.forEach(fo => {
            // Ensure foreign objects maintain their positioning
            const x = fo.getAttribute('x');
            const y = fo.getAttribute('y');
            const width = fo.getAttribute('width');
            const height = fo.getAttribute('height');
            
            // Apply styles to inner div for proper rendering
            const innerDiv = fo.querySelector('div');
            if (innerDiv) {
                innerDiv.style.width = '100%';
                innerDiv.style.height = '100%';
                innerDiv.style.display = 'flex';
                innerDiv.style.alignItems = 'center';
                innerDiv.style.justifyContent = 'center';
            }
        });
        
        // Serialize back to string
        const serializer = new XMLSerializer();
        return serializer.serializeToString(svgElement);
        
    } catch (e) {
        console.error('Error processing SVG:', e);
        return svgString; // Return original if processing fails
    }
}

/**
 * Post-process rendered graphs in the DOM
 * This should be called after graphs are inserted into the DOM
 * @param {HTMLElement} container - Container element with rendered graphs
 */
export function postProcessGraphs(container) {
    if (!container) return;
    
    // Find all graph containers
    const graphContainers = container.querySelectorAll('.graph-svg-container');
    
    graphContainers.forEach(graphContainer => {
        const svg = graphContainer.querySelector('svg');
        if (!svg) return;
        
        // Ensure SVG fills its container properly
        const containerWidth = graphContainer.offsetWidth;
        const containerHeight = graphContainer.offsetHeight;
        
        if (containerWidth && containerHeight) {
            svg.style.width = `${containerWidth}px`;
            svg.style.height = `${containerHeight}px`;
        }
    });
    
    console.log(`Post-processed ${graphContainers.length} graph containers`);
}

/**
 * Render LaTeX in all visible SVGs sequentially
 * Call this after all graphs are displayed
 * @param {number} delay - Delay between rendering each LaTeX expression (ms)
 * @returns {Promise<void>}
 */
export async function renderAllSvgLatexSequentially(delay = 10) {
    if (typeof katex === 'undefined') {
        console.warn('KaTeX not available, cannot render LaTeX');
        return;
    }
    
    // Find all SVG containers in the document
    const svgContainers = document.querySelectorAll('.graph-svg-container svg');
    let totalLatexExpressions = 0;
    let renderedCount = 0;
    
    console.log(`Found ${svgContainers.length} SVG containers to process`);
    
    // Collect all LaTeX divs to render
    const latexDivsToRender = [];
    
    svgContainers.forEach(svg => {
        const foreignObjects = svg.querySelectorAll('foreignObject');
        foreignObjects.forEach(fo => {
            const latexDivs = fo.querySelectorAll('div.svg-latex');
            latexDivs.forEach(div => {
                // Only add if not already rendered
                if (!div.querySelector('.katex')) {
                    const latex = div.textContent.trim();
                    if (latex) {
                        latexDivsToRender.push({ div, latex });
                        totalLatexExpressions++;
                    }
                }
            });
        });
    });
    
    console.log(`Found ${totalLatexExpressions} LaTeX expressions to render`);
    
    // Render sequentially with delay
    for (const { div, latex } of latexDivsToRender) {
        try {
            // Preserve original styles
            const bgColor = div.style.backgroundColor;
            const color = div.style.color;
            
            // Render LaTeX
            const rendered = katex.renderToString(latex, {
                throwOnError: false,
                displayMode: false
            });
            
            div.innerHTML = rendered;
            renderedCount++;
            
            // Restore styles
            if (bgColor) div.style.backgroundColor = bgColor;
            if (color) {
                div.querySelectorAll('.katex, .katex *').forEach(el => {
                    el.style.color = color;
                });
            }
            
            // Small delay to avoid blocking UI
            if (delay > 0 && renderedCount < totalLatexExpressions) {
                await new Promise(resolve => setTimeout(resolve, delay));
            }
            
            // Log progress every 10 expressions
            if (renderedCount % 10 === 0) {
                console.log(`Rendered ${renderedCount}/${totalLatexExpressions} LaTeX expressions`);
            }
            
        } catch (e) {
            console.error('Error rendering LaTeX:', e, latex);
        }
    }
    
    console.log(`✅ Rendered ${renderedCount}/${totalLatexExpressions} LaTeX expressions in SVGs`);
}
