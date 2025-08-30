/**
 * SVG to PNG Converter Module
 * Handles conversion of SVG graphs to high-quality PNG images
 */

// Import dom-to-image as fallback for local development
import domtoimage from 'https://cdn.jsdelivr.net/npm/dom-to-image@2.6.0/+esm';

/**
 * Detect if browser is Safari
 * @returns {boolean} True if Safari, false otherwise
 */
export function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

/**
 * Convert SVG to PNG using Canvas API (CORS-safe method)
 * @param {string} svgString - The SVG HTML string
 * @param {number} width - Width of the output image
 * @param {number} height - Height of the output image
 * @param {number} scale - Scale factor for high DPI
 * @returns {Promise<string>} PNG data URL
 */
async function convertSvgToPngCanvas(svgString, width, height, scale = 2) {
    return new Promise((resolve, reject) => {
        try {
            // Create a Blob from the SVG string
            const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(svgBlob);
            
            // Create an image element
            const img = new Image();
            
            // Set up the canvas
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas dimensions with scale
            canvas.width = width * scale;
            canvas.height = height * scale;
            
            // Handle image load
            img.onload = function() {
                try {
                    // Fill white background
                    ctx.fillStyle = 'white';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw the SVG image scaled up
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    
                    // Convert to PNG data URL
                    const pngDataUrl = canvas.toDataURL('image/png', 1.0);
                    
                    // Clean up
                    URL.revokeObjectURL(url);
                    
                    resolve(pngDataUrl);
                } catch (err) {
                    URL.revokeObjectURL(url);
                    reject(err);
                }
            };
            
            // Handle image error
            img.onerror = function() {
                URL.revokeObjectURL(url);
                reject(new Error('Failed to load SVG image'));
            };
            
            // Start loading the image
            img.src = url;
        } catch (err) {
            reject(err);
        }
    });
}

/**
 * Pre-render LaTeX in an SVG string
 * @param {string} svgString - The SVG string with raw LaTeX in foreignObjects
 * @returns {Promise<string>} The SVG string with rendered LaTeX
 */
export async function prerenderLatexInSvg(svgString) {
    // If KaTeX is not available, return original
    if (typeof katex === 'undefined') {
        console.warn('KaTeX not available, cannot pre-render LaTeX');
        return svgString;
    }
    
    try {
        // Parse the SVG
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
        const svgElement = svgDoc.querySelector('svg');
        
        if (!svgElement) {
            return svgString;
        }
        
        // Find all foreign objects with LaTeX
        const foreignObjects = svgElement.querySelectorAll('foreignObject');
        let hasUnrenderedLatex = false;
        let renderedCount = 0;
        
        foreignObjects.forEach((fo) => {
            const divs = fo.querySelectorAll('div.svg-latex');
            divs.forEach((div) => {
                // Check if already rendered (has .katex class)
                if (div.querySelector('.katex')) {
                    // Already rendered, skip
                    return;
                }
                
                const latex = div.textContent.trim();
                if (latex) {
                    hasUnrenderedLatex = true;
                    try {
                        // Preserve original styles
                        const bgColor = div.style.backgroundColor;
                        const color = div.style.color;
                        
                        // Render LaTeX to HTML string
                        const rendered = katex.renderToString(latex, {
                            throwOnError: false,
                            displayMode: false
                        });
                        
                        // Set the rendered HTML
                        div.innerHTML = rendered;
                        renderedCount++;
                        
                        // Restore styles
                        if (bgColor) div.style.backgroundColor = bgColor;
                        if (color) {
                            // Apply color to all KaTeX elements
                            const katexElements = div.querySelectorAll('.katex, .katex *');
                            katexElements.forEach(el => {
                                el.style.color = color;
                            });
                        }
                    } catch (e) {
                        console.error('KaTeX rendering error:', e);
                        // Keep original LaTeX text on error
                    }
                }
            });
        });
        
        // If no unrendered LaTeX was found, return original
        if (!hasUnrenderedLatex) {
            return svgString;
        }
        
        if (renderedCount > 0) {
            console.log(`Pre-rendered ${renderedCount} LaTeX expressions in SVG`);
        }
        
        // Serialize back to string
        const serializer = new XMLSerializer();
        return serializer.serializeToString(svgElement);
        
    } catch (error) {
        console.error('Error pre-rendering LaTeX in SVG:', error);
        return svgString;
    }
}

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
    // For Safari, skip PNG conversion entirely to avoid security issues
    // The calling code will fall back to using SVG directly
    if (isSafari()) {
        console.log('Safari detected, skipping PNG conversion (will use SVG directly)');
        return null;
    }
    
    // Don't pre-render LaTeX here - it will be done after display
    
    // Default options for high quality
    const scale = options.scale || 2; // 2x for high DPI
    let width = options.width || 200;
    let height = options.height || 150;
    
    try {
        // Parse the SVG to get dimensions
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
        const svgElement = svgDoc.querySelector('svg');
        
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
        
        // Apply inline styles to ensure they're captured
        svgElement.style.backgroundColor = 'white';
        svgElement.style.fontFamily = "'Lexend', sans-serif";
        
        // Serialize back to string
        const serializer = new XMLSerializer();
        const updatedSvgString = serializer.serializeToString(svgElement);
        
        // First, try the Canvas method (CORS-safe)
        try {
            const pngDataUrl = await convertSvgToPngCanvas(updatedSvgString, width, height, scale);
            if (pngDataUrl) {
                return pngDataUrl;
            }
        } catch (canvasError) {
            console.warn('Canvas conversion failed, trying dom-to-image fallback:', canvasError);
        }
        
        // Fallback to dom-to-image (mainly for local development where CORS is not an issue)
        // Create a temporary container
        const tempDiv = document.createElement('div');
        tempDiv.style.position = 'absolute';
        tempDiv.style.left = '-9999px';
        tempDiv.style.top = '-9999px';
        tempDiv.innerHTML = updatedSvgString;
        document.body.appendChild(tempDiv);
        
        const tempSvgElement = tempDiv.querySelector('svg');
        
        // Render LaTeX in foreign objects if they exist
        renderLatexInForeignObjects(tempDiv);
        
        // Wait a bit for rendering to complete
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Suppress console errors temporarily during conversion
        const originalError = console.error;
        const originalWarn = console.warn;
        console.error = () => {};
        console.warn = () => {};
        
        let pngDataUrl;
        try {
            // Convert to PNG using dom-to-image with CORS-safe options
            pngDataUrl = await domtoimage.toPng(tempSvgElement, {
                width: width * scale,
                height: height * scale,
                style: {
                    transform: `scale(${scale})`,
                    transformOrigin: 'top left',
                    width: `${width}px`,
                    height: `${height}px`
                },
                quality: 1.0,
                // Add options to handle CORS issues
                cacheBust: true,
                imagePlaceholder: undefined,
                // Skip external stylesheets that cause CORS issues
                filter: (node) => {
                    // Filter out link elements that reference external stylesheets
                    if (node.tagName === 'LINK' && node.rel === 'stylesheet') {
                        const href = node.href || '';
                        // Skip external stylesheets
                        if (href.includes('fonts.googleapis.com') || 
                            href.includes('cdn.jsdelivr.net') ||
                            href.includes('cdnjs.cloudflare.com')) {
                            return false;
                        }
                    }
                    return true;
                }
            });
        } finally {
            // Restore console methods
            console.error = originalError;
            console.warn = originalWarn;
        }
        
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
                
                // Don't pre-render - just convert the raw SVG
                // LaTeX will be rendered after display
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
