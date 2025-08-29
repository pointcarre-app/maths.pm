/**
 * SVG to PNG Converter Module
 * Handles conversion of SVG graphs to high-quality PNG images
 */

import domtoimage from 'https://cdn.jsdelivr.net/npm/dom-to-image@2.6.0/+esm';

/**
 * Render LaTeX in foreign objects within a DOM element
 * @param {HTMLElement} container - The DOM element containing SVGs with foreign objects
 */
function renderLatexInForeignObjects(container) {
    if (!container || typeof katex === 'undefined') {
        if (typeof katex === 'undefined') {
            console.warn('KaTeX not available, skipping LaTeX rendering');
        }
        return;
    }
    
    // Find all foreign objects in the container
    const foreignObjects = container.querySelectorAll('foreignObject');
    
    foreignObjects.forEach((fo) => {
        const divs = fo.querySelectorAll('div.svg-latex');
        divs.forEach((div) => {
            const latex = div.textContent.trim();
            if (latex) {
                try {
                    // Preserve original styles
                    const bgColor = div.style.backgroundColor;
                    const color = div.style.color;
                    
                    // Clear and render
                    div.innerHTML = '';
                    katex.render(latex, div, {
                        throwOnError: false,
                        displayMode: false,
                    });
                    
                    // Restore styles
                    if (bgColor) div.style.backgroundColor = bgColor;
                    if (color) {
                        div.querySelectorAll('.katex, .katex *').forEach(el => {
                            el.style.color = color;
                        });
                    }
                } catch (e) {
                    console.error('KaTeX rendering error:', e);
                    div.textContent = latex; // Fallback to raw LaTeX
                }
            }
        });
    });
}

/**
 * Convert SVG string to high-quality PNG data URL
 * @param {string} svgString - The SVG HTML string
 * @param {Object} options - Conversion options
 * @returns {Promise<string>} PNG data URL
 */
export async function convertSvgToPng(svgString, options = {}) {
    // Default options for high quality
    const scale = options.scale || 2; // 2x for high DPI
    let width = options.width || 200;
    let height = options.height || 150;
    
    try {
        // Create a temporary container
        const tempDiv = document.createElement('div');
        tempDiv.style.position = 'absolute';
        tempDiv.style.left = '-9999px';
        tempDiv.style.top = '-9999px';
        tempDiv.innerHTML = svgString;
        document.body.appendChild(tempDiv);
        
        // Get the SVG element
        const svgElement = tempDiv.querySelector('svg');
        if (!svgElement) {
            throw new Error('No SVG element found in the provided string');
        }
        
        // Try to get actual dimensions from the SVG element
        const svgWidth = svgElement.getAttribute('width');
        const svgHeight = svgElement.getAttribute('height');
        const viewBox = svgElement.getAttribute('viewBox');
        
        // If SVG has dimensions, use them
        if (svgWidth && svgHeight) {
            width = parseInt(svgWidth) || width;
            height = parseInt(svgHeight) || height;
        }
        
        // Ensure SVG has explicit dimensions for conversion
        svgElement.setAttribute('width', width);
        svgElement.setAttribute('height', height);
        
        // Ensure viewBox is set if not present
        if (!viewBox) {
            svgElement.setAttribute('viewBox', `0 0 ${width} ${height}`);
        }
        
        // Render LaTeX in foreign objects if they exist
        renderLatexInForeignObjects(tempDiv);
        
        // Wait a bit for rendering to complete
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Convert to PNG using dom-to-image
        const pngDataUrl = await domtoimage.toPng(svgElement, {
            width: width * scale,
            height: height * scale,
            style: {
                transform: `scale(${scale})`,
                transformOrigin: 'top left',
                width: `${width}px`,
                height: `${height}px`
            },
            quality: 1.0
        });
        
        // Clean up
        document.body.removeChild(tempDiv);
        
        return pngDataUrl;
    } catch (error) {
        console.error('Error converting SVG to PNG:', error);
        // Return null on error
        return null;
    }
}

/**
 * Convert all graphs for all students to PNG
 * @param {Function} onProgress - Callback for progress updates
 * @returns {Promise<void>}
 */
export async function convertAllGraphsToPng(generationResults, onProgress) {
    // Count total graphs to convert
    let totalGraphs = 0;
    generationResults.students.forEach(student => {
        student.questions.forEach(question => {
            if (question.graphSvg) totalGraphs++;
        });
    });
    
    if (totalGraphs === 0) {
        console.log('No graphs to convert');
        return;
    }
    
    console.log(`Converting ${totalGraphs} graphs to PNG...`);
    let converted = 0;
    
    // Process each student
    for (const student of generationResults.students) {
        for (const question of student.questions) {
            if (question.graphSvg) {
                // Get dimensions from graphDict if available
                const dimensions = {
                    width: question.graphDict?.svg?.width || 340,
                    height: question.graphDict?.svg?.height || 340
                };
                
                // Convert SVG to PNG
                const pngDataUrl = await convertSvgToPng(question.graphSvg, {
                    width: dimensions.width,
                    height: dimensions.height,
                    scale: 2 // 2x for high quality
                });
                
                if (pngDataUrl) {
                    // Store PNG and dimensions in question
                    question.graphPng = pngDataUrl;
                    question.graphDimensions = dimensions;
                } else {
                    console.warn(`Failed to convert graph for student ${student.id}, question ${question.generator}`);
                }
                
                converted++;
                
                // Call progress callback
                if (onProgress) {
                    onProgress(converted, totalGraphs);
                }
            }
        }
    }
    
    console.log(`✅ Converted ${converted} graphs to PNG`);
}
