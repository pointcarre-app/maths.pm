/**
 * Papyrus Integration Module for Sujets0
 * Handles conversion of exercise data to Papyrus JSON format for printing
 * 
 * ARCHITECTURE:
 * - Papyrus creates proper A4 pages with automatic pagination
 * - Page structure: .page-wrapper > .page-preview > .page-content
 * - ONLY .page-content has padding (document margins)
 * - Margins: 3mm top/bottom, 8mm left/right for optimal space usage
 * - Each element has 1rem padding-bottom for spacing
 * - Chrome print: Set margins to "None" in print dialog (@page rule handles this)
 * 
 * IMPORTANT FIXES:
 * - All heading margins are explicitly set to 0 to prevent browser defaults
 * - We override both --papyrus-margin-* and --page-margin-* variables
 * - Print media queries ensure consistent spacing between preview and print
 */

import generationResults from './index-data-model.js';
import { generatePages } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/core/preview/index.js';
import { printPage } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/core/print-manager.js';
import { convertSvgToPng, isSafari } from './index-svg-converter.js';
import { 
    initializeMargins, 
    setMargins,
    getCurrentMargins
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/core/margin-config.js';
import { 
    initializeFontSizes, // Default font sizes in px
    setFontSizes 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/core/font-config.js';

import { 
    initializePageNumberConfig,
    setShowPageNumbers 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/core/page-number-config.js';



/**
 * Log page dimensions for debugging
 * @param {HTMLElement} container - The pages container
 */
function logPageDimensions(container) {
    // Try different selectors for Papyrus pages
    let pages = container.querySelectorAll('.papyrus-page');
    
    // If no .papyrus-page, try .page-wrapper (what Papyrus actually uses)
    if (pages.length === 0) {
        pages = container.querySelectorAll('.page-wrapper');
        console.log('Using .page-wrapper elements as pages');
    }
    
    // If still nothing, try .page-preview
    if (pages.length === 0) {
        pages = container.querySelectorAll('.page-preview');
        console.log('Using .page-preview elements as pages');
    }
    
    console.log('=== PAPYRUS PAGE DIMENSIONS DEBUG ===');
    console.log(`Total pages found: ${pages.length}`);
    
    // Check the actual structure
    const pageWrappers = container.querySelectorAll('.page-wrapper');
    const pagePreviews = container.querySelectorAll('.page-preview');
    const pageContents = container.querySelectorAll('.page-content');
    
    console.log(`Structure: ${pageWrappers.length} .page-wrapper, ${pagePreviews.length} .page-preview, ${pageContents.length} .page-content`);
    console.log('PADDING RESPONSIBILITY: Only .page-content should have padding (the document margins)');
    
    if (pages.length === 0) {
        console.warn('⚠️ NO page elements found! Checking container structure...');
        console.log('Container classes:', container.className);
        console.log('Container first child:', container.firstElementChild?.className);
        console.log('Container HTML preview:', container.innerHTML.substring(0, 500) + '...');
    }
    
    pages.forEach((page, index) => {
        const rect = page.getBoundingClientRect();
        const computedStyle = window.getComputedStyle(page);
        
        // Get actual dimensions
        const heightPx = rect.height;
        const widthPx = rect.width;
        
        // Convert to mm (1mm = 3.7795275591 pixels at 96 DPI)
        const pxToMm = 1 / 3.7795275591;
        const heightMm = heightPx * pxToMm;
        const widthMm = widthPx * pxToMm;
        
        // Get padding values
        const paddingTop = computedStyle.paddingTop;
        const paddingBottom = computedStyle.paddingBottom;
        const paddingLeft = computedStyle.paddingLeft;
        const paddingRight = computedStyle.paddingRight;
        
        // Check padding at each level of the structure
        console.log(`  - .page-wrapper padding: ${paddingTop} ${paddingRight} ${paddingBottom} ${paddingLeft}`);
        
        const pagePreview = page.querySelector('.page-preview');
        if (pagePreview) {
            const previewStyle = window.getComputedStyle(pagePreview);
            console.log(`  - .page-preview padding: ${previewStyle.paddingTop} ${previewStyle.paddingRight} ${previewStyle.paddingBottom} ${previewStyle.paddingLeft}`);
        }
        
        const pageContent = page.querySelector('.page-content');
        if (pageContent) {
            const contentStyle = window.getComputedStyle(pageContent);
            const contentPaddingTop = parseFloat(contentStyle.paddingTop) * pxToMm;
            const contentPaddingRight = parseFloat(contentStyle.paddingRight) * pxToMm;
            const contentPaddingBottom = parseFloat(contentStyle.paddingBottom) * pxToMm;
            const contentPaddingLeft = parseFloat(contentStyle.paddingLeft) * pxToMm;
            
            console.log(`  - .page-content padding (DOCUMENT MARGINS): T:${contentPaddingTop.toFixed(1)}mm R:${contentPaddingRight.toFixed(1)}mm B:${contentPaddingBottom.toFixed(1)}mm L:${contentPaddingLeft.toFixed(1)}mm`);
            
            const expectedSettings = getDocumentSettings();
            if (Math.abs(contentPaddingTop - expectedSettings.margins.top) > 0.5 ||
                Math.abs(contentPaddingRight - expectedSettings.margins.right) > 0.5 ||
                Math.abs(contentPaddingBottom - expectedSettings.margins.bottom) > 0.5 ||
                Math.abs(contentPaddingLeft - expectedSettings.margins.left) > 0.5) {
                console.warn('    ⚠️ MISMATCH: Expected T:' + expectedSettings.margins.top + 'mm R:' + expectedSettings.margins.right + 'mm B:' + expectedSettings.margins.bottom + 'mm L:' + expectedSettings.margins.left + 'mm');
            }
        }
        
        // Get content height
        const contentHeight = page.scrollHeight;
        const contentHeightMm = contentHeight * pxToMm;
        
        console.log(`Page ${index + 1}:`);
        console.log(`  - Dimensions: ${widthMm.toFixed(1)}mm × ${heightMm.toFixed(1)}mm (should be 210mm × 297mm)`);
        console.log(`  - Pixels: ${widthPx}px × ${heightPx}px`);
        console.log(`  - Padding: T:${paddingTop} R:${paddingRight} B:${paddingBottom} L:${paddingLeft}`);
        console.log(`  - Content height: ${contentHeightMm.toFixed(1)}mm (${contentHeight}px)`);
        console.log(`  - Overflow: ${contentHeightMm > 297 ? '⚠️ YES' : '✓ NO'}`);
        
        // Check if content overflows
        if (heightMm > 297) {
            console.warn(`  ⚠️ PAGE ${index + 1} EXCEEDS A4 HEIGHT by ${(heightMm - 297).toFixed(1)}mm`);
        }
        
        // Check children for overflow
        const children = page.children;
        let totalChildrenHeight = 0;
        for (let child of children) {
            totalChildrenHeight += child.offsetHeight;
        }
        const totalChildrenHeightMm = totalChildrenHeight * pxToMm;
        console.log(`  - Children total height: ${totalChildrenHeightMm.toFixed(1)}mm`);
        
        // Log individual element heights
        const elements = page.querySelectorAll('[id^="question-"], [id="header-section"], [id="main-title"]');
        console.log(`  - Elements on page: ${elements.length}`);
        elements.forEach(elem => {
            const elemHeight = elem.offsetHeight * pxToMm;
            console.log(`    - ${elem.id}: ${elemHeight.toFixed(1)}mm`);
        });
    });
    
    // If only one page but content is too tall, that's the problem
    if (pages.length === 1) {
        const singlePage = pages[0];
        const heightPx = singlePage.getBoundingClientRect().height;
        const pxToMm = 1 / 3.7795275591;
        const heightMm = heightPx * pxToMm;
        
        // Get current margin settings
        const settings = getDocumentSettings();
        const usableHeight = 297 - settings.margins.top - settings.margins.bottom;
        
        if (heightMm > 297) {
            console.error(`⚠️⚠️ CRITICAL: Single page is ${heightMm.toFixed(1)}mm tall (exceeds A4 by ${(heightMm - 297).toFixed(1)}mm)`);
            console.error(`With margins (${settings.margins.top}mm top, ${settings.margins.bottom}mm bottom), usable height is ${usableHeight}mm`);
            console.error('Papyrus should have split this into multiple pages but did not!');
            
            // Check if we're in a single container situation
            const contentDiv = singlePage.querySelector('.page-content') || singlePage;
            const contentHeight = contentDiv.scrollHeight * pxToMm;
            console.error(`Content height: ${contentHeight.toFixed(1)}mm - needs ${Math.ceil(contentHeight / usableHeight)} pages`);
        }
    }
    
    console.log('=== END PAGE DIMENSIONS DEBUG ===');
}

/**
 * Apply inline styles to SVG elements for Safari compatibility
 * @param {HTMLElement} container - The DOM element containing SVGs
 */
function applySafariSVGStyles(container) {
    if (!container || !isSafari()) return;
    
    // First, ensure all SVG elements have explicit dimensions
    const svgElements = container.querySelectorAll('svg');
    svgElements.forEach(svg => {
        // Get current dimensions from attributes or viewBox
        let width = svg.getAttribute('width');
        let height = svg.getAttribute('height');
        
        // If no width/height, try to extract from viewBox
        if (!width || !height) {
            const viewBox = svg.getAttribute('viewBox');
            if (viewBox) {
                const parts = viewBox.split(' ');
                if (parts.length === 4) {
                    width = parts[2];
                    height = parts[3];
                }
            }
        }
        
        // Default to 340x340 if still no dimensions
        width = width || 340;
        height = height || 340;
        
        // Remove any units (px, %, etc) and ensure it's a number
        width = parseFloat(width);
        height = parseFloat(height);
        
        // Apply inline styles with explicit pixel dimensions
        const currentStyle = svg.getAttribute('style') || '';
        if (!currentStyle.includes('width:')) {
            svg.style.width = `${width}px`;
        }
        if (!currentStyle.includes('height:')) {
            svg.style.height = `${height}px`;
        }
        
        console.log(`Safari: Set SVG dimensions to ${width}x${height}px`);
    });
    
    // Find all elements with text-2xs class within SVGs
    const textElements = container.querySelectorAll('svg .text-2xs');
    textElements.forEach(el => {
        // Apply inline styles directly
        el.style.fontSize = '0.625rem';
        el.style.lineHeight = '1';
    });
    
    // Also check for other common text size classes
    const textXsElements = container.querySelectorAll('svg .text-xs');
    textXsElements.forEach(el => {
        el.style.fontSize = '0.75rem';
        el.style.lineHeight = '1rem';
    });
    
    const textSmElements = container.querySelectorAll('svg .text-sm');
    textSmElements.forEach(el => {
        el.style.fontSize = '0.875rem';
        el.style.lineHeight = '1.25rem';
    });
    
    console.log(`Applied Safari SVG styles to ${svgElements.length} SVGs and ${textElements.length + textXsElements.length + textSmElements.length} text elements`);
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
 * Render LaTeX in foreign objects within an HTML string
 * @param {string} htmlString - HTML string containing SVGs with foreign objects
 * @returns {string} Processed HTML string with rendered LaTeX
 */
function renderLatexInHTMLString(htmlString) {
    if (typeof katex === 'undefined') {
        console.warn('KaTeX not available, returning original HTML');
        return htmlString;
    }
    
    // Create a temporary container to work with the HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlString;
    
    // Render LaTeX in the temporary container
    renderLatexInForeignObjects(tempDiv);
    
    // Return the processed HTML
    return tempDiv.innerHTML;
}

// Default font sizes in px
// const DEFAULT_FONT_SIZES = {
//     h1: 32,
//     h2: 28,
//     h3: 24,
//     h4: 20,
//     h5: 18,
//     h6: 16,
//     body: 18
// };
import { 
    initializeSpaceBetweenDivs, 
    setSpaceBetweenDivs,
    getCurrentSpaceBetweenDivs
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/core/margin-config.js';

/**
 * Get fallback dimensions for different graph types
 * Used when graphDict is not available or doesn't contain dimensions
 * @param {string} generator - The generator name
 * @returns {Object} Width and height for the graph
 */
function getGraphDimensions(generator) {
    // Define fallback sizes for different graph types
    // These are only used if graphDict.svg dimensions are not available
    const dimensions = {
        'spe_sujet1_auto_07_question': { width: 340, height: 340 },
        'spe_sujet1_auto_08_question': { width: 340, height: 340 },
        'spe_sujet1_auto_09_question': { width: 340, height: 340 },
        'spe_sujet1_auto_10_question': { width: 340, height: 340 },
        'spe_sujet1_auto_11_question': { width: 340, height: 340 },
        'spe_sujet1_auto_12_question': { width: 340, height: 340 }
    };
    
    // Extract base generator name without .py extension
    const baseName = generator.replace('.py', '');
    
    return dimensions[baseName] || { width: 340, height: 340 }; // Default size matching typical SVG output
}

/**
 * Extract question number from generator name
 * @param {string} generator - Generator filename (e.g., 'spe_sujet1_auto_01_question')
 * @returns {string} Question number as a string
 */
function extractQuestionNumber(generator) {
    const match = generator.match(/auto_(\d+)_question/);
    return match ? match[1] : '?';
}

/**
 * Create the Papyrus JSON structure for a single student
 * @param {Object} studentExerciseSet - Student exercise set from generationResults
 * @returns {Promise<Array>} Array of Papyrus JSON objects
 * 
 * MARGINS REMOVED TO LET PAPYRUS HANDLE ALL SPACING:
 * - Header table: removed margin-bottom: 1rem
 * - Main title: removed margin-bottom: 2rem and margin-top: 1rem  
 * - Each question: removed margin-bottom: 2rem
 * - All spacing is now controlled by Papyrus's setSpaceBetweenDivs()
 * 
 * SVG TO PNG CONVERSION:
 * - Graphs with foreignObjects are converted to high-quality PNGs
 * - 2x scaling for print quality (effectively 144 DPI on screen, 288 DPI in print)
 * - Uses actual dimensions from graphDict.svg (typically 340x340)
 * - Falls back to default dimensions if graphDict not available
 * - Scales down proportionally to max 200px for display while keeping full resolution in PNG
 */
export async function createPapyrusJson(studentExerciseSet) {
    // Extract student info
    const studentId = studentExerciseSet.id;
    const seed = studentExerciseSet.seed;
    
    console.log(`Creating Papyrus JSON for student ${studentId} with seed ${seed}`);
    
    // Initialize JSON array with header that repeats on each page
    const papyrusJson = [
        // Header section with student info - REPEATING HEADER
        // REMOVED: margin-bottom: 1rem from table
        {
            "id": "header-section",
            "html": `<table style='width: 100%; border-collapse: collapse; border: 0.5px solid #e0e0e0;'>
                    <tr>
                        <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 50%;'>Nom :</td>
                        <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Classe :</td>
                        <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Copie n°${studentId} (${seed})</td>
                    </tr>
                    <tr>
                        <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 50%;'>Prénom :</td>
                        <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Date :</td>
                        <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Spécialité </td>
                    </tr>
                </table>`,
            "classes": ["font-mono"],
            "isPapyrusHeader": true,  // This tells Papyrus to repeat on each page
            "style": "padding-bottom: 1rem;"
        },
        
        // Title section - only on first page
        {
            "id": "main-title",
            "html": "<h3 style='margin: 0;'>Bac 1<sup>ère</sup> Maths - Première Partie : Automatismes</h3>",
            "style": "font-family: 'Spectral', serif; font-weight: bold; text-align: left; color: var(--color-base-content); padding-bottom: 1rem; margin: 0;"
        }
    ];




    // TODO: dynamically but in config not here
    // There is in the css static/css/root  .css a data-theme="bolt" : take the color of the --color-base-content
    // --color-base-content: oklch(22% 0.015 240);  /* Deep charcoal with slight blue undertone */
    
    
    // Process each question as a separate JSON item for proper pagination
    // Now using for...of to support async operations
    for (const [index, question] of studentExerciseSet.questions.entries()) {
        // Use sequential numbering (1, 2, 3...) instead of extracting from generator name
        // This ensures proper incremental numbering when less than 12 questions are selected
        const questionNum = index + 1;
        
        // Also extract original question number for reference (can be used for debugging)
        const originalQuestionNum = extractQuestionNumber(question.generator).replace(/^0+/, '');
                
        // Get statement HTML, or fallback to regular statement
        const statementHtml = question.getStatementHtml() || question.statement;
        
        // Create the question HTML
        let questionHtml;
        let processedStatement;
        
        // Process statement to add question number
        if (statementHtml.startsWith("<div style='display: flex;")) {
            // Insert question number inside the flex child
            processedStatement = statementHtml.replace(
                "<div style='flex: 1; min-width: 250px;'>",
                `<div style='flex: 1; min-width: 250px;'>${questionNum})&nbsp;&nbsp;`
            );
        } else if (statementHtml.startsWith('<div>')) {
            // Insert question number inside the first div
            processedStatement = statementHtml.replace('<div>', `<div>${questionNum})&nbsp;&nbsp;`);
        } else {
            // Wrap in div with question number
            processedStatement = `<div>${questionNum}) ${statementHtml}</div>`;
        }
        
        // If there's a graph, use the pre-converted PNG or convert on the fly
        if (question.graphSvg) {
            // Check if PNG was already pre-converted
            let pngDataUrl = question.graphPng;
            let dimensions = question.graphDimensions;
            
            if (!pngDataUrl) {
                // Fallback: convert on the fly (shouldn't normally happen)
                console.warn(`PNG not pre-converted for question ${questionNum}, converting now...`);
                
                // Get dimensions
                if (question.graphDict && question.graphDict.svg) {
                    dimensions = {
                        width: question.graphDict.svg.width || 200,
                        height: question.graphDict.svg.height || 150
                    };
                } else {
                    dimensions = getGraphDimensions(question.generator);
                }
                
                // Try to convert SVG to PNG
                pngDataUrl = await convertSvgToPng(question.graphSvg, {
                    width: dimensions.width,
                    height: dimensions.height,
                    scale: 2 // 2x for high quality
                });
            } else {
                console.log(`Using pre-converted PNG for question ${questionNum}`);
            }
            
            if (pngDataUrl) {
                // Use PNG image with size constraints for large graphs
                // Scale down proportionally if either dimension is larger than 200px
                const maxDisplaySize = 200;
                let displayWidth = dimensions.width;
                let displayHeight = dimensions.height;
                
                if (dimensions.width > maxDisplaySize || dimensions.height > maxDisplaySize) {
                    const scale = Math.min(maxDisplaySize / dimensions.width, maxDisplaySize / dimensions.height);
                    displayWidth = Math.round(dimensions.width * scale);
                    displayHeight = Math.round(dimensions.height * scale);
                }
                
                questionHtml = `
                    <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
                        <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
                        <div style='flex: 0 1 auto;'>
                            <img src="${pngDataUrl}" 
                                 style="width: ${displayWidth}px; height: ${displayHeight}px; object-fit: contain; display: block;"
                                 alt="Graphique question ${questionNum}" />
                        </div>
                    </div>
                `;
            } else {
                // Fallback to original SVG if conversion failed
                console.warn(`⚠️ Failed to convert SVG to PNG for question ${questionNum}, using original SVG`);
                
                // For Safari, inject critical styles inline to ensure they work
                let svgWithStyles = question.graphSvg;
                
                // Check if this is Safari - apply inline styles for critical classes AND size
                if (typeof isSafari !== 'undefined' && isSafari()) {
                    // First, ensure SVG has explicit size in pixels
                    // Get dimensions from graphDict or use fallback
                    let svgDimensions;
                    if (question.graphDict && question.graphDict.svg) {
                        svgDimensions = {
                            width: question.graphDict.svg.width || 340,
                            height: question.graphDict.svg.height || 340
                        };
                    } else {
                        svgDimensions = getGraphDimensions(question.generator);
                    }
                    
                    // Add or update width and height inline styles on the SVG element
                    // First check if the SVG already has style attribute
                    if (svgWithStyles.match(/<svg[^>]*style\s*=/)) {
                        // SVG has style attribute, append to it
                        svgWithStyles = svgWithStyles.replace(
                            /(<svg[^>]*style\s*=\s*["'])([^"']*)(["'])/,
                            `$1$2; width: ${svgDimensions.width}px !important; height: ${svgDimensions.height}px !important;$3`
                        );
                    } else {
                        // SVG doesn't have style attribute, add one
                        svgWithStyles = svgWithStyles.replace(
                            /<svg([^>]*)>/,
                            `<svg$1 style="width: ${svgDimensions.width}px !important; height: ${svgDimensions.height}px !important;">`
                        );
                    }
                    
                    // Also ensure width and height attributes are set (as backup)
                    svgWithStyles = svgWithStyles.replace(
                        /<svg([^>]*?)(?:\s+width\s*=\s*["'][^"']*["'])?([^>]*?)(?:\s+height\s*=\s*["'][^"']*["'])?([^>]*)>/,
                        `<svg$1 width="${svgDimensions.width}" height="${svgDimensions.height}"$2$3>`
                    );
                    
                    // Map of CSS classes to their inline styles
                    const classToStyles = {
                        'text-2xs': 'font-size: 0.625rem !important; line-height: 1 !important;',
                        'text-xs': 'font-size: 0.75rem !important; line-height: 1rem !important;',
                        'text-sm': 'font-size: 0.875rem !important; line-height: 1.25rem !important;',
                        'text-base': 'font-size: 1rem !important; line-height: 1.5rem !important;'
                    };
                    
                    // Apply inline styles for each class found
                    for (const [className, styles] of Object.entries(classToStyles)) {
                        if (svgWithStyles.includes(className)) {
                            // Handle elements with only the class
                            const classOnlyRegex = new RegExp(`class\\s*=\\s*["']${className}["']`, 'g');
                            svgWithStyles = svgWithStyles.replace(classOnlyRegex, `class="${className}" style="${styles}"`);
                            
                            // Handle elements with the class among others (no existing style)
                            const classAmongOthersRegex = new RegExp(`(class\\s*=\\s*["'][^"']*\\b)${className}(\\b[^"']*["'])(?![^>]*style)`, 'g');
                            svgWithStyles = svgWithStyles.replace(classAmongOthersRegex, `$1${className}$2 style="${styles}"`);
                            
                            // Handle elements that already have style attribute
                            const withStyleRegex = new RegExp(`(<[^>]+class\\s*=\\s*["'][^"']*\\b${className}\\b[^"']*["'][^>]*style\\s*=\\s*["'])([^"']*)(["'])`, 'g');
                            svgWithStyles = svgWithStyles.replace(withStyleRegex, `$1$2; ${styles}$3`);
                        }
                    }
                    
                    console.log(`Safari: Applied explicit dimensions ${svgDimensions.width}x${svgDimensions.height}px to SVG for question ${questionNum}`);
                }
                
                questionHtml = `
                    <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
                        <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
                        <div style='flex: 0 1 auto;'>${svgWithStyles}</div>
                    </div>
                `;
            }
        } else {
            // Simple layout for questions without graphs
            questionHtml = processedStatement;
        }
        
        // Add each question as a separate JSON item
        // This allows Papyrus to properly measure and paginate
        // REMOVED: margin-bottom: 2rem from each question
        papyrusJson.push({
            "id": `question-${questionNum}`,
            "html": questionHtml,
             "style": "padding-bottom: 1.25rem; color: oklch(22% 0.015 240) !important;",  // No margins - let Papyrus handle spacing
            // "classes": ["text-base-content"]  // Can add classes if needed
        });
    }
    
    console.log(`Created ${papyrusJson.length} items for Papyrus (1 header, 1 title, ${studentExerciseSet.questions.length} questions)`);
    
    return papyrusJson;
}

/**
 * Get document settings from form inputs or defaults
 * @returns {Object} The document settings
 */
function getDocumentSettings() {
    // Fixed hardcoded settings - REDUCED margins for more content space
    // IMPORTANT: These margins must match the CSS variables
    return {
        margins: {
            top: 3,     // Small top margin for breathing room
            right: 8,   // Side margins for readability
            bottom: 3,  // Small bottom margin for page numbers
            left: 8     // Side margins for readability
        },
        fontSizes: {
            h1: 28,
            h2: 24,
            h3: 20,
            h4: 18,
            h5: 16,
            h6: 14,
            body: 15
        },
        spacing: 0  // Spacing between elements in mm // TODO sel: not sure reflected in Papyrus
    };
}

/**
 * Apply document settings to CSS variables
 * @param {Object} settings - The document settings
 */
function applySettingsToCss(settings) {
    // Override our custom variables
    document.documentElement.style.setProperty('--papyrus-margin-top', `${settings.margins.top}mm`);
    document.documentElement.style.setProperty('--papyrus-margin-right', `${settings.margins.right}mm`);
    document.documentElement.style.setProperty('--papyrus-margin-bottom', `${settings.margins.bottom}mm`);
    document.documentElement.style.setProperty('--papyrus-margin-left', `${settings.margins.left}mm`);
    
    // Also override Papyrus's default variables if they exist
    document.documentElement.style.setProperty('--page-margin-top', `${settings.margins.top}mm`);
    document.documentElement.style.setProperty('--page-margin-right', `${settings.margins.right}mm`);
    document.documentElement.style.setProperty('--page-margin-bottom', `${settings.margins.bottom}mm`);
    document.documentElement.style.setProperty('--page-margin-left', `${settings.margins.left}mm`);
    
    // Font sizes
    document.documentElement.style.setProperty('--papyrus-font-size-h1', `${settings.fontSizes.h1}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h2', `${settings.fontSizes.h2}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h3', `${settings.fontSizes.h3}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h4', `${settings.fontSizes.h4}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h5', `${settings.fontSizes.h5}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h6', `${settings.fontSizes.h6}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-body', `${settings.fontSizes.body}px`);
    
    // Also set default font-size variables if Papyrus uses them
    document.documentElement.style.setProperty('--font-size-h1', `${settings.fontSizes.h1}px`);
    document.documentElement.style.setProperty('--font-size-h2', `${settings.fontSizes.h2}px`);
    document.documentElement.style.setProperty('--font-size-h3', `${settings.fontSizes.h3}px`);
    document.documentElement.style.setProperty('--font-size-h4', `${settings.fontSizes.h4}px`);
    document.documentElement.style.setProperty('--font-size-h5', `${settings.fontSizes.h5}px`);
    document.documentElement.style.setProperty('--font-size-h6', `${settings.fontSizes.h6}px`);
    document.documentElement.style.setProperty('--font-size-body', `${settings.fontSizes.body}px`);
}

/**
 * Configure Papyrus with consistent settings for preview and print
 * @private
 */
function configurePapyrus() {
    // Get settings from form or defaults
    const settings = getDocumentSettings();
    
    console.log('Configuring Papyrus with margins:', settings.margins);
    console.log('Spacing between divs:', settings.spacing, 'mm');
    
    // Apply settings to CSS variables FIRST
    applySettingsToCss(settings);
    
    // Initialize configurations
    initializeMargins();
    initializeFontSizes();
    initializeSpaceBetweenDivs();
    initializePageNumberConfig();
    
    // Set margins from settings - these should match CSS variables
    setMargins({
        top: settings.margins.top,
        right: settings.margins.right,
        bottom: settings.margins.bottom,
        left: settings.margins.left
    });
    
    // Verify margins were set correctly
    const currentMargins = getCurrentMargins();
    console.log('Margins after setting:', currentMargins);
    
    // Set font sizes from settings
    setFontSizes({
        h1: settings.fontSizes.h1,
        h2: settings.fontSizes.h2,
        h3: settings.fontSizes.h3,
        h4: settings.fontSizes.h4,
        h5: settings.fontSizes.h5,
        h6: settings.fontSizes.h6,
        body: settings.fontSizes.body
    });
    
    // Set spacing between divs
    setSpaceBetweenDivs(settings.spacing);
    
    // Enable page numbers
    // setShowPageNumbers(true);
}

/**
 * Update document settings and refresh preview
 */
export async function updateDocumentSettings() {
    // Configure Papyrus with settings
    configurePapyrus();
    
    // Only try to refresh preview if we have student data
    if (generationResults.students && generationResults.students.length > 0) {
        // Get current student index
        const currentIndex = generationResults.currentStudentIndex || 0;
        
        // Update settings and refresh preview
        await previewStudentCopy(currentIndex, false);
    } else {
        // Just update the placeholder
        const pagesContainer = document.getElementById('pages-container');
        if (pagesContainer) {
            pagesContainer.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #4a5568; border: 1px dashed #cbd5e0; margin: 20px;">
                    <h3>Affichage des fichiers PDFs</h3>
                </div>
            `;
            pagesContainer.style.display = 'block';
        }
    }
}

/**
 * Preview a specific student's exercise sheet
 * @param {number} studentIndex - Index of the student to preview
 * @param {boolean} triggerPrint - Whether to trigger the print dialog
 */
export async function previewStudentCopy(studentIndex, triggerPrint = false) {
    // Check if students array exists and has data
    if (!generationResults.students || !Array.isArray(generationResults.students) || generationResults.students.length === 0) {
        console.error('No student data available. Make sure exercises are generated before preview.');
        
        // Display an error message in the preview container if it exists
        const pagesContainer = document.getElementById('pages-container');
        if (pagesContainer) {
            pagesContainer.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #e53e3e; border: 1px solid #e53e3e; margin: 20px;">
                    <h3>No student data available</h3>
                    <p>Please generate exercises before attempting to preview.</p>
                </div>
            `;
            pagesContainer.style.display = 'block';
        }
        
        return;
    }
    
    const student = generationResults.students[studentIndex];
    if (!student) {
        console.error(`No student found at index ${studentIndex}`);
        return;
    }
    
    // Store current index right away
    generationResults.currentStudentIndex = studentIndex;
    
    // Show loading indicator immediately
    const pagesContainer = document.getElementById('pages-container');
    pagesContainer.innerHTML = `
        <div style="padding: 30px; text-align: center; background: rgba(255,255,255,0.98); border-radius: 8px; margin: 20px;">
            <h3 style="margin-bottom: 15px;">Chargement en cours...</h3>
            <progress class="progress w-full" style="height: 10px;"></progress>
        </div>
    `;
    pagesContainer.style.display = 'block';
    
    // Configure Papyrus with consistent settings FIRST
    configurePapyrus();
    
    try {
        // Create Papyrus JSON (now async due to SVG to PNG conversion)
        const papyrusJson = await createPapyrusJson(student);
        
        // Log the JSON to console for debugging
        console.log(`JSON contains ${papyrusJson.length} items`);
        
        // Set the JSON data to the input field (Papyrus reads from here)
        const jsonInput = document.getElementById('json-input');
        jsonInput.value = JSON.stringify(papyrusJson, null, 2);
        
        // Set up Papyrus globals (required for proper pagination)
        if (!window.contentModel) {
            window.contentModel = { 
                items: [],
                loadFromJSON: function(json) { this.items = json; },
                updateMargins: function(margins) { this.margins = margins; }
            };
        }
        
        // Make getCurrentSpaceBetweenDivs available globally (Papyrus expects this)
        if (!window.getCurrentSpaceBetweenDivs) {
            window.getCurrentSpaceBetweenDivs = getCurrentSpaceBetweenDivs;
        }
        
        // Set papyrus debug mode based on toggle state
        const debugToggle = document.getElementById('papyrus-debug-toggle');
        window.papyrusDebugMode = debugToggle ? debugToggle.checked : false;
        
        // CRITICAL: Clear the container before Papyrus generates pages
        pagesContainer.innerHTML = '';
        
        // Generate pages - let Papyrus fully control the rendering
        console.log('Calling Papyrus generatePages()...');
        console.log('Current spacing:', getCurrentSpaceBetweenDivs(), 'mm');
        
        generatePages();
        
        // Wait longer for Papyrus to complete pagination
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        pagesContainer.style.display = 'block';
        
        // Log page dimensions for debugging
        if (window.papyrusDebugMode) {
            logPageDimensions(pagesContainer);
        }
        
        // CRITICAL: Render LaTeX in foreign objects AFTER pages are built
        renderLatexInForeignObjects(pagesContainer);
        
        // Apply Safari-specific SVG styles if needed
        applySafariSVGStyles(pagesContainer);
        
        // Trigger print if requested
        if (triggerPrint) {
            // Wait for LaTeX rendering to complete
            await new Promise(resolve => setTimeout(resolve, 200));
            
            // Apply Safari inline styles if needed (for SVG text rendering)
            if (isSafari()) {
                console.log('Safari: Applying inline styles to SVGs');
                applySafariSVGStyles(pagesContainer);
                // Minimal delay for style application
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            
            // Get the fully rendered content after styles are applied
            const renderedContent = pagesContainer.innerHTML;
            
            // Use Papyrus's print function for all browsers
            // Papyrus v0.0.10+ handles iframe creation, cleanup, and browser quirks
            const styleSheet = "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/styles/print.css";
            printPage(renderedContent, styleSheet);
        }
    } catch (error) {
        console.error('Error generating preview:', error);
        pagesContainer.innerHTML = `
            <div style="padding: 20px; text-align: center; color: #e53e3e; border: 1px solid #e53e3e; margin: 20px;">
                <h3>Error generating preview</h3>
                <p>${error.message || 'Unknown error'}</p>
            </div>
        `;
    }
}

/**
 * Print a specific student's exercise sheet
 * @param {number} studentIndex - Index of the student to print
 * 
 * NOTE: Chrome users should set print margins to "None" in the print dialog
 * for best results. The @page CSS rule should handle this automatically.
 */
export async function printStudentCopy(studentIndex) {
    // First preview, then print
    await previewStudentCopy(studentIndex, true);
}

/**
 * Print all student copies
 */
export async function printAllCopies() {
    // Log how many copies will be printed
    console.log(`Printing all ${generationResults.students.length} copies`);
    
    // Configure Papyrus with consistent settings first
    configurePapyrus();
    
    // Get progress elements
    const printMessage = document.getElementById('print-all-message');
    const printProgress = document.getElementById('print-all-progress');
    const printTime = document.getElementById('print-all-time');
    
    // Initialize the progress card
    if (printProgress) {
        printProgress.max = generationResults.students.length;
        printProgress.value = 0;
    }
    if (printMessage) {
        printMessage.textContent = `Traitement copie 1 sur ${generationResults.students.length}`;
    }
    if (printTime) {
        printTime.textContent = '⏱️ Cela peut prendre quelques secondes...';
    }
    
    const startTime = Date.now();
    
    // Create a hidden container for processing
    const hiddenContainer = document.createElement('div');
    hiddenContainer.id = 'hidden-print-container';
    hiddenContainer.style.position = 'absolute';
    hiddenContainer.style.left = '-9999px';
    hiddenContainer.style.top = '-9999px';
    hiddenContainer.style.width = '210mm';
    document.body.appendChild(hiddenContainer);
    
    // Store all student content
    let allContent = '';
    
    // For each student
    for (let i = 0; i < generationResults.students.length; i++) {
        // Update progress
        if (printProgress) printProgress.value = i;
        if (printMessage) printMessage.textContent = `Traitement copie ${i + 1} sur ${generationResults.students.length}`;
        
        // Update elapsed time
        if (printTime) {
            const elapsed = Math.round((Date.now() - startTime) / 1000);
            printTime.textContent = `${elapsed}s écoulées`;
        }
        
        // Generate JSON for this student
        const student = generationResults.students[i];
        if (!student) continue;
        
        // Create Papyrus JSON (uses pre-converted PNGs, should be fast)
        const papyrusJson = await createPapyrusJson(student);
        
        // Update the JSON input field
        document.getElementById('json-input').value = JSON.stringify(papyrusJson);
        
        // Generate pages in the hidden container
        hiddenContainer.innerHTML = '';
        
        // Temporarily swap containers for Papyrus
        const originalPagesContainer = document.getElementById('pages-container');
        hiddenContainer.id = 'pages-container';
        originalPagesContainer.id = 'pages-container-temp';
        
        // Generate pages (will use hidden container)
        generatePages();
        
        // Wait a bit for Papyrus to complete
        await new Promise(resolve => setTimeout(resolve, 200));
        
        // Swap IDs back
        hiddenContainer.id = 'hidden-print-container';
        originalPagesContainer.id = 'pages-container';
        
        // IMPORTANT: Render LaTeX in the DOM before getting innerHTML
        renderLatexInForeignObjects(hiddenContainer);
        
        // Apply Safari SVG styles if needed
        if (isSafari()) {
            applySafariSVGStyles(hiddenContainer);
        }
        
        // Add student content to the combined content
        allContent += hiddenContainer.innerHTML;
    }
    
    // Clean up hidden container
    document.body.removeChild(hiddenContainer);
    
    // Update progress to complete
    if (printProgress) printProgress.value = generationResults.students.length;
    if (printMessage) printMessage.textContent = `✅ Impression prête! La boîte de dialogue d'impression va s'ouvrir...`;
    if (printTime) {
        const elapsed = Math.round((Date.now() - startTime) / 1000);
        printTime.textContent = `Terminé en ${elapsed}s`;
    }
    
    // Apply Safari inline styles if needed (for SVG text rendering)
    if (isSafari()) {
        console.log('Safari: Applying inline styles to all copies');
        
        // Temporarily apply styles to the combined content
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = allContent;
        applySafariSVGStyles(tempDiv);
        allContent = tempDiv.innerHTML;
    }
    
    // Use Papyrus's print function for all browsers
    // Papyrus v0.0.10+ handles iframe creation, cleanup, and browser quirks
    const styleSheet = "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/styles/print.css";
    printPage(allContent, styleSheet);
    
    // Reset the progress card to waiting state after 3 seconds
    setTimeout(() => {
        if (printMessage) printMessage.textContent = 'En attente d\'impression groupée...';
        if (printProgress) printProgress.value = 0;
        if (printTime) printTime.textContent = '';
    }, 3000);
}

/**
 * Create pagination buttons for all students
 */
export function createPaginationButtons() {
    const paginationContainer = document.getElementById('student-pagination');
    if (!paginationContainer) return;
    
    // Clear existing buttons
    paginationContainer.innerHTML = '';
    
    // Create button container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'flex flex-wrap gap-1 mb-2';
    paginationContainer.appendChild(buttonContainer);
    
    // Create buttons for each student
    generationResults.students.forEach((student, index) => {
        const button = document.createElement('button');
        button.className = index === 0 ? 'btn btn-xs sm:btn-sm btn-primary' : 'btn btn-xs sm:btn-sm btn-outline';
        button.textContent = `${student.id}`;
        button.onclick = () => {
            // Immediately update UI before the heavy processing
            updatePaginationButtons(index);
            // Then start the content generation process
            setTimeout(() => previewStudentCopy(index), 10);
        };
        button.title = `Voir la copie de l'élève ${student.id}`;
        
        buttonContainer.appendChild(button);
    });
    
    // Set the initial student index if it's not already set
    if (generationResults.currentStudentIndex === undefined && generationResults.students.length > 0) {
        generationResults.currentStudentIndex = 0;
    }
    
    // Update the badge in the legend to show current student count
    updateStudentBadge(generationResults.currentStudentIndex || 0);
    
    // Enable the print buttons if we have students
    if (generationResults.students.length > 0) {
        const printCurrentBtn = document.getElementById('print-current-copy-btn');
        const printAllBtn = document.getElementById('print-all-copies-btn');
        const teacherManifestBtn = document.getElementById('teacher-manifest-btn');
        
        if (printCurrentBtn) printCurrentBtn.disabled = false;
        if (printAllBtn) printAllBtn.disabled = false;
        if (teacherManifestBtn) teacherManifestBtn.disabled = false;
    }
}

/**
 * Updates the student badge in the legend with current student information
 * @param {number} studentIndex - Index of the student to display
 */
function updateStudentBadge(studentIndex) {
    const studentBadge = document.querySelectorAll('.fieldset-legend .badge.badge-soft')[1];
    if (!studentBadge || !generationResults.students || generationResults.students.length === 0) return;
    
    // Make sure we have a valid index
    const validIndex = Math.min(Math.max(0, studentIndex), generationResults.students.length - 1);
    const currentStudent = generationResults.students[validIndex];
    
    if (currentStudent) {
        studentBadge.innerHTML = `
            Copies - Copie ${validIndex + 1}/${generationResults.students.length}
        `;
    }
}

/**
 * Update pagination buttons to highlight current student
 * @param {number} currentIndex - Index of the current student
 */
export function updatePaginationButtons(currentIndex) {
    const paginationContainer = document.getElementById('student-pagination');
    if (!paginationContainer) return;
    
    // Find the button container
    const buttonContainer = paginationContainer.querySelector('div.flex.flex-wrap.gap-1');
    if (!buttonContainer) return;
    
    // Update button states
    Array.from(buttonContainer.children).forEach((button, index) => {
        if (index === currentIndex) {
            button.classList.remove('btn-outline');
            button.classList.add('btn-primary');
        } else {
            button.classList.remove('btn-primary');
            button.classList.add('btn-outline');
        }
    });
    
    // Update the student badge with the current student info
    updateStudentBadge(currentIndex);
}

/**
 * Initialize document settings
 */
export function initDocumentSettingsForm() {
    // Automatically apply default settings without requiring user interaction
    console.log('Initializing document settings with default values');
    
    // Apply basic configuration without trying to render a preview
    configurePapyrus();
    
    // Set up debug toggle event listener
    const debugToggle = document.getElementById('papyrus-debug-toggle');
    if (debugToggle) {
        debugToggle.addEventListener('change', function() {
            window.papyrusDebugMode = debugToggle.checked;
            console.log('Debug mode:', window.papyrusDebugMode ? 'ON' : 'OFF');
            
            // Regenerate preview with debug mode change if we have data
            if (generationResults.students && generationResults.students.length > 0) {
                const currentIndex = generationResults.currentStudentIndex || 0;
                previewStudentCopy(currentIndex, false);
            }
        });
    }
    
    // Display a placeholder message in the preview container
    const pagesContainer = document.getElementById('pages-container');
    if (pagesContainer) {
        pagesContainer.innerHTML = `
            <div style="padding: 20px; text-align: center; color: #4a5568; border: 1px dashed #cbd5e0; margin: 20px;">
                <h3>Affichage des fichiers PDFs</h3>
                <p>En attente de la génération de copies.</p>
            </div>
        `;
        pagesContainer.style.display = 'block';
    }
}

/**
 * Generate teacher manifest URL with compressed data
 * @returns {string} The full URL with encoded data in hash fragment
 */
function generateTeacherManifestURL() {
    console.log('Generating teacher manifest URL...');
    
    if (!generationResults || !generationResults.students || generationResults.students.length === 0) {
        console.error('No student data available for manifest');
        return null;
    }
    
    try {
        // Generate filename based on current date and configuration
        const now = new Date();
        const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD
        const timeStr = now.toTimeString().split(':').slice(0, 2).join('h'); // HHhMM
        const nbStudents = generationResults.students.length;
        const nbQuestions = generationResults.students[0]?.questions.length || 0;
        const filename = `fiche_reponses_${nbStudents}copies_${nbQuestions}questions_${dateStr}_${timeStr}`;
        
        // Build compact manifest structure
        const manifest = {
            v: 1,  // Version for future compatibility
            ts: Date.now(),  // Timestamp
            filename: filename,  // Suggested filename for saving/printing
            cfg: {
                n: nbStudents,  // Number of students
                q: nbQuestions  // Questions per student
            },
            data: []
        };
        
        // Extract data for each student
        generationResults.students.forEach(student => {
            const studentData = [
                student.id,  // Student ID
                student.seed,  // Seed
                []  // Questions array
            ];
            
            // Extract each question's answers
            student.questions.forEach(question => {
                let answer = null;
                let simplified = null;
                let generator = question.generator || 'unknown_generator';
                
                // Get regular answer(s)
                try {
                    const answers = question.getAllAnswers();
                    if (answers && answers.length > 0) {
                        answer = answers.length === 1 ? answers[0] : answers;
                    }
                } catch (e) {
                    console.error('Error getting answers:', e);
                }
                
                // Get simplified answer(s)
                try {
                    if (question.answer && question.answer.simplified_latex) {
                        const simplifiedLatex = question.answer.simplified_latex;
                        simplified = Array.isArray(simplifiedLatex) ? 
                            (simplifiedLatex.length === 1 ? simplifiedLatex[0] : simplifiedLatex) : 
                            simplifiedLatex;
                    }
                } catch (e) {
                    console.error('Error getting simplified answers:', e);
                }
                
                // Add question data [answer, simplified, generator]
                studentData[2].push([answer, simplified, generator]);
            });
            
            manifest.data.push(studentData);
        });
        
        // Compress the manifest
        const jsonString = JSON.stringify(manifest);
        console.log('Manifest size (uncompressed):', jsonString.length, 'bytes');
        
        // Use LZ-String compression
        const compressed = LZString.compressToBase64(jsonString);
        console.log('Manifest size (compressed):', compressed.length, 'bytes');
        
        // Check URL length (browsers typically support up to 2048 chars, but some support more)
        const fullURL = `/sujets0/teacher-manifest#${compressed}`;
        console.log('Full URL length:', fullURL.length, 'chars');
        
        if (fullURL.length > 8000) {
            console.warn('URL is very long and may not work in all browsers');
        }
        
        return fullURL;
        
    } catch (error) {
        console.error('Error generating manifest URL:', error);
        return null;
    }
}

/**
 * Open teacher manifest in new tab
 */
function openTeacherManifest() {
    const url = generateTeacherManifestURL();
    if (url) {
        // Open in new tab
        window.open(url, '_blank');
    } else {
        alert('Impossible de générer la fiche enseignant. Générez d\'abord les copies.');
    }
}

// Expose functions globally for use in HTML
window.previewStudentCopy = previewStudentCopy;
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;
window.createPaginationButtons = createPaginationButtons;
window.updateDocumentSettings = updateDocumentSettings;
window.generateTeacherManifestURL = generateTeacherManifestURL;
window.openTeacherManifest = openTeacherManifest;
