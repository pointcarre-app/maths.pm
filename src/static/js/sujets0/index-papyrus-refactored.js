/**
 * Papyrus Integration Module for Sujets0 - REFACTORED
 * Handles document generation, preview, and printing with proper state management
 */

import generationResults from './index-data-model.js';
import { getPapyrusManager } from './papyrus-manager.js';
import { getStateManager } from './state-manager.js';
import { getProgressManager } from './unified-progress.js';
import { convertSvgToPng, isSafari } from './index-svg-converter.js';

// Store current state
let currentPapyrusJson = null;

/**
 * Initialize the Papyrus module
 */
export async function initializePapyrus() {
    const state = getStateManager();
    const papyrus = getPapyrusManager();
    
    try {
        // Initialize Papyrus
        await papyrus.initialize();
        
        // Update document settings
        updateDocumentSettings();
        
        // Set up event listeners
        setupEventListeners();
        
        console.log('Papyrus module initialized successfully');
        
    } catch (error) {
        console.error('Failed to initialize Papyrus:', error);
        state.addError(error);
    }
}

/**
 * Set up event listeners for Papyrus functionality
 */
function setupEventListeners() {
    // Debug toggle
    const debugToggle = document.getElementById('papyrus-debug-toggle');
    if (debugToggle) {
        debugToggle.addEventListener('change', (e) => {
            const container = document.getElementById('pages-container');
            if (container) {
                if (e.target.checked) {
                    container.classList.add('debug-mode');
                } else {
                    container.classList.remove('debug-mode');
                }
            }
        });
    }
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
 * Get fallback dimensions for different graph types
 * @param {string} generator - The generator name
 * @returns {Object} Width and height for the graph
 */
function getGraphDimensions(generator) {
    const dimensions = {
        'spe_sujet1_auto_07_question': { width: 340, height: 340 },
        'spe_sujet1_auto_08_question': { width: 340, height: 340 },
        'spe_sujet1_auto_09_question': { width: 340, height: 340 },
        'spe_sujet1_auto_10_question': { width: 340, height: 340 },
        'spe_sujet1_auto_11_question': { width: 340, height: 340 },
        'spe_sujet1_auto_12_question': { width: 340, height: 340 }
    };
    
    const baseName = generator.replace('.py', '');
    return dimensions[baseName] || { width: 340, height: 340 };
}

/**
 * Create Papyrus JSON from student exercise data - EXACT COPY FROM ORIGINAL
 * @param {Object} studentExerciseSet - Student data with exercises
 * @returns {Array} Papyrus JSON array
 */
export async function createPapyrusJson(studentExerciseSet) {
    const studentId = studentExerciseSet.id;
    const seed = studentExerciseSet.seed;
    
    console.log(`Creating Papyrus JSON for student ${studentId} with seed ${seed}`);
    
    // Initialize JSON array with header that repeats on each page
    // const papyrusJson = [
    //     // Header section with student info - REPEATING HEADER
    //     {
    //         "id": "header-section",
    //         "html": `<table style='width: 100%; border-collapse: collapse; border: 0.5px solid #e0e0e0;'>
    //                 <tr>
    //                     <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 50%;'>Nom :</td>
    //                     <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Classe :</td>
    //                     <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Copie n°${studentId} (${seed})</td>
    //                 </tr>
    //                 <tr>
    //                     <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 50%;'>Prénom :</td>
    //                     <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Date :</td>
    //                     <td style='font-size:0.85rem !important; border: 0.5px solid #e0e0e0; padding: 0.25rem; vertical-align: middle; width: 25%;'>Spécialité </td>
    //                 </tr>
    //             </table>`,
    //         "classes": ["font-mono"],
    //         "isPapyrusHeader": true,  // This tells Papyrus to repeat on each page
    //         "style": "padding-bottom: 1rem;"
    //     },
        
    //     // Title section - only on first page
    //     {
    //         "id": "main-title",
    //         "html": "<h3 style='margin: 0;'>Bac 1<sup>ère</sup> Maths - Première Partie : Automatismes</h3>",
    //         "style": "font-family: 'Spectral', serif; font-weight: bold; text-align: left; color: var(--color-base-content); padding-bottom: 1rem; margin: 0;"
    //     }
    // ];
    
    // Process each question as a separate JSON item for proper pagination
    // Now using for...of to support async operations
    // for (const [index, question] of studentExerciseSet.questions.entries()) {
    //     // Use sequential numbering (1, 2, 3...) instead of extracting from generator name
    //     const questionNum = index + 1;
        
    //     // Also extract original question number for reference (can be used for debugging)
    //     const originalQuestionNum = extractQuestionNumber(question.generator).replace(/^0+/, '');
                
    //     // Get statement HTML, or fallback to regular statement
    //     const statementHtml = question.getStatementHtml() || question.statement;
        
    //     // Create the question HTML
    //     let questionHtml;
    //     let processedStatement;
        
    //     // Process statement to add question number
    //     if (statementHtml.startsWith("<div style='display: flex;")) {
    //         // Insert question number inside the flex child
    //         processedStatement = statementHtml.replace(
    //             "<div style='flex: 1; min-width: 250px;'>",
    //             `<div style='flex: 1; min-width: 250px;'>${questionNum})&nbsp;&nbsp;`
    //         );
    //     } else if (statementHtml.startsWith('<div>')) {
    //         // Insert question number inside the first div
    //         processedStatement = statementHtml.replace('<div>', `<div>${questionNum})&nbsp;&nbsp;`);
    //     } else {
    //         // Wrap in div with question number
    //         processedStatement = `<div>${questionNum}) ${statementHtml}</div>`;
    //     }
        
    //     // If there's a graph, use the pre-converted PNG or convert on the fly
    //     if (question.graphSvg) {
    //         // Check if PNG was already pre-converted
    //         let pngDataUrl = question.graphPng;
    //         let dimensions = question.graphDimensions;
            
    //         if (!pngDataUrl) {
    //             // Fallback: convert on the fly (shouldn't normally happen)
    //             console.warn(`PNG not pre-converted for question ${questionNum}, converting now...`);
                
    //             // Get dimensions
    //             if (question.graphDict && question.graphDict.svg) {
    //                 dimensions = {
    //                     width: question.graphDict.svg.width || 200,
    //                     height: question.graphDict.svg.height || 150
    //                 };
    //             } else {
    //                 dimensions = getGraphDimensions(question.generator);
    //             }
                
    //             // Try to convert SVG to PNG
    //             pngDataUrl = await convertSvgToPng(question.graphSvg, {
    //                 width: dimensions.width,
    //                 height: dimensions.height,
    //                 scale: 2 // 2x for high quality
    //             });
    //         } else {
    //             console.log(`Using pre-converted PNG for question ${questionNum}`);
    //         }
            
    //         if (pngDataUrl) {
    //             // Use PNG image with size constraints for large graphs
    //             // Scale down proportionally if either dimension is larger than 200px
    //             const maxDisplaySize = 200;
    //             let displayWidth = dimensions.width;
    //             let displayHeight = dimensions.height;
                
    //             if (dimensions.width > maxDisplaySize || dimensions.height > maxDisplaySize) {
    //                 const scale = Math.min(maxDisplaySize / dimensions.width, maxDisplaySize / dimensions.height);
    //                 displayWidth = Math.round(dimensions.width * scale);
    //                 displayHeight = Math.round(dimensions.height * scale);
    //             }
                
    //             questionHtml = `
    //                 <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
    //                     <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
    //                     <div style='flex: 0 1 auto;'>
    //                         <img src="${pngDataUrl}" 
    //                              style="width: ${displayWidth}px; height: ${displayHeight}px; object-fit: contain; display: block;"
    //                              alt="Graphique question ${questionNum}" />
    //                     </div>
    //                 </div>
    //             `;
    //         } else {
    //             // Fallback to original SVG if conversion failed
    //             console.warn(`⚠️ Failed to convert SVG to PNG for question ${questionNum}, using original SVG`);
                
    //             // For Safari, inject critical styles inline to ensure they work
    //             let svgWithStyles = question.graphSvg;
                
    //             // Check if this is Safari - apply inline styles for critical classes AND size
    //             if (typeof isSafari !== 'undefined' && isSafari()) {
    //                 // Get dimensions from graphDict or use fallback
    //                 let svgDimensions;
    //                 if (question.graphDict && question.graphDict.svg) {
    //                     svgDimensions = {
    //                         width: question.graphDict.svg.width || 340,
    //                         height: question.graphDict.svg.height || 340
    //                     };
    //                 } else {
    //                     svgDimensions = getGraphDimensions(question.generator);
    //                 }
                    
    //                 // Add or update width and height inline styles on the SVG element
    //                 if (svgWithStyles.match(/<svg[^>]*style\s*=/)) {
    //                     // SVG has style attribute, append to it
    //                     svgWithStyles = svgWithStyles.replace(
    //                         /(<svg[^>]*style\s*=\s*["'])([^"']*)(["'])/,
    //                         `$1$2; width: ${svgDimensions.width}px !important; height: ${svgDimensions.height}px !important;$3`
    //                     );
    //                 } else {
    //                     // SVG doesn't have style attribute, add one
    //                     svgWithStyles = svgWithStyles.replace(
    //                         /<svg([^>]*)>/,
    //                         `<svg$1 style="width: ${svgDimensions.width}px !important; height: ${svgDimensions.height}px !important;">`
    //                     );
    //                 }
                    
    //                 // Also ensure width and height attributes are set (as backup)
    //                 svgWithStyles = svgWithStyles.replace(
    //                     /<svg([^>]*?)(?:\s+width\s*=\s*["'][^"']*["'])?([^>]*?)(?:\s+height\s*=\s*["'][^"']*["'])?([^>]*)>/,
    //                     `<svg$1 width="${svgDimensions.width}" height="${svgDimensions.height}"$2$3>`
    //                 );
                    
    //                 // Apply inline styles for text classes
    //                 svgWithStyles = applySafariInlineStyles(svgWithStyles);
                    
    //                 console.log(`Safari: Applied explicit dimensions ${svgDimensions.width}x${svgDimensions.height}px to SVG for question ${questionNum}`);
    //             }
                
    //             questionHtml = `
    //                 <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
    //                     <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
    //                     <div style='flex: 0 1 auto;'>${svgWithStyles}</div>
    //                 </div>
    //             `;
    //         }
    //     } else {
    //         // Simple layout for questions without graphs
    //         questionHtml = processedStatement;
    //     }
        
    //     // Add each question as a separate JSON item
    //     papyrusJson.push({
    //         "id": `question-${questionNum}`,
    //         "html": questionHtml,
    //         "style": "padding-bottom: 1.25rem; color: oklch(22% 0.015 240) !important;",
    //         // "classes": ["text-base-content"]  // Can add classes if needed
    //     });
    // }


    const papyrusJson = [
        {
          "id": "header-section",
          "html": "<table style='width: 100%; border-collapse: collapse; border: 0.5px solid #e0e0e0; '><tr><td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>Nom :</td><td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Classe :</td><td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>BolzanoBleu</td></tr><tr><td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>Prénom :</td><td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Date :</td><td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>2nde&1ère|Spé</td></tr></table>",
          "classes": [
            "font-mono"
          ],
          "style": "",
          "isPapyrusHeader": true
        },
        {
          "id": "main-title",
          "html": "<div>Bac 1ère Spé. Maths : Partie 1 automatismes</div>",
          "classes": [],
          "style": "font-family: 'Spectral', serif; font-size: 24px; font-weight: bold; text-align: left; color: #2c3e50;"
        },
        {
          "id": "subtitle",
          "html": "<div>Questions inspirées des Sujets 0</div>",
          "classes": [],
          "style": "font-family: 'Spectral', serif; font-size: 18px; font-weight: 500; text-align: left; color: #5a6c7d; font-style: italic;"
        },
        {
          "id": "question-1",
          "html": "<div><div>1) Quel est l'inverse du quintuple de $7$ ?</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-2",
          "html": "<div><div>2) On considère la relation $F=a+\\dfrac{b}{cd}$. Lorsque $a=\\dfrac{1}{7}$, $b = 7$, $c = 1$, $d = -\\dfrac{1}{5}$, quelle est la valeur de $F$ ?</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-3",
          "html": "<div><div>3) Le prix d'un article est multiplié par $1,495$. De combien de pourcent le prix de cet article a-t-il augmenté ?</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-4",
          "html": "<div style='display: flex; gap: 20px; align-items: flex-start;'><div style='flex: 1;'>4) Le prix d'un article est noté $P$. Ce prix augmente de $65\\%$ puis diminue de $65\\%$. A l'issue de ces deux variations, de combien le prix a-t-il varié en pourcentage ?<br/><br/>Référez-vous au graphique de la fonction carré ci-contre pour visualiser la croissance quadratique.</div><div style='flex: 0 0 250px;'><svg width='250' height='150' xmlns='http://www.w3.org/2000/svg' style='border: 1px solid #ddd; background: #f9f9f9;'><defs><marker id='arrowhead' markerWidth='6' markerHeight='4' refX='6' refY='2' orient='auto'><polygon points='0 0, 6 2, 0 4' fill='#333' /></marker></defs><!-- X axis --><line x1='20' y1='110' x2='230' y2='110' stroke='#333' stroke-width='1' marker-end='url(#arrowhead)' /><!-- Y axis --><line x1='125' y1='140' x2='125' y2='10' stroke='#333' stroke-width='1' marker-end='url(#arrowhead)' /><!-- Grid marks --><line x1='95' y1='108' x2='95' y2='112' stroke='#666' stroke-width='0.5' /><line x1='155' y1='108' x2='155' y2='112' stroke='#666' stroke-width='0.5' /><line x1='123' y1='90' x2='127' y2='90' stroke='#666' stroke-width='0.5' /><line x1='123' y1='50' x2='127' y2='50' stroke='#666' stroke-width='0.5' /><!-- Actual square function y = x² points: (-2,4), (-1,1), (0,0), (1,1), (2,4) scaled --><path d='M 65 140 L 80 125 L 95 115 L 110 110.5 L 125 110 L 140 110.5 L 155 115 L 170 125 L 185 140' stroke='#e74c3c' stroke-width='2' fill='none' /><!-- LaTeX labels using foreignObject --><foreignObject x='232' y='112' width='15' height='15'><div xmlns='http://www.w3.org/1999/xhtml' style='font-size: 12px;'>$x$</div></foreignObject><foreignObject x='128' y='8' width='15' height='15'><div xmlns='http://www.w3.org/1999/xhtml' style='font-size: 12px;'>$y$</div></foreignObject><!-- Origin --><circle cx='125' cy='110' r='1.5' fill='#333' /></svg></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-5",
          "html": "<div><div>5) On lance un dé à 4 faces. La probabilité d'obtenir chacune des faces est donnée dans le tableau suivant:<br />- Face numéro 1: $\\dfrac{13}{24}$<br />- Face numéro 2: $\\dfrac{13}{24}$<br />- Face numéro 3: $\\dfrac{13}{24}$<br />- Face numéro 4: $x$</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-6",
          "html": "<div><div>6) On considère $x$, $y$, et $u$ des réels non nuls tels que $\\dfrac{1}{x}+ \\dfrac{1}{y} = \\dfrac{1}{u}$. Exprimer $u$ en fonction $x$ et $y$.</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-7",
          "html": "<div><div>7) On a représenté ci-contre la parabole d'équation $y = x^2$. On note (J) l'inéquation, sur $\\mathbb{R}$, $x^{2} > 49$. Donner la ou les inéquation(s) du premier degré équivalente à J.</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-8",
          "html": "<div><div>8) On a représenté ci-contre une droite D dans un repère orthonormé. Donner l'équation de la droite D sous la forme $y=ax+b$</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-9",
          "html": "<div><div>9) Parmi les 3 fonctions $$f1: x \\mapsto x^{2} -\\left(x + 2\\right)^{2}$$, $$f2: x \\mapsto \\dfrac{1}{7}x --9 + \\dfrac{1}{5^{\\dfrac{1}{2}}}$$, $$f3: x \\mapsto \\dfrac{\\dfrac{9}{8}x + 2}{0,5}$$ Au sein des fonctions affines parmis $f1, f2, f3$, quel est le coefficient directeur avec la plus grande valeur absolue ?</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-10",
          "html": "<div><div>10) La courbe ci-contre représente la courbe d'équation $ax^2 + bx + c$. On suppose $\\lvert a \\rvert = 1$. Donner l'équation de la parabole.</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-11",
          "html": "<div><div>11) On a représenté ci-contre la courbe $\\mathcal{C}$ d'une fonction ${f}$. On note $A$ le point d'abscisse $x_A=-2$ tel que le point appartienne à la courbe $\\mathcal{C}$. Ecrire l'inégalité correcte de la forme $x\\times f(x) ? 0$</div><div></div></div>",
          "classes": [],
          "style": ""
        },
        {
          "id": "question-12",
          "html": "<div><div>12) Voici une série de notes avec les coefficients associés<br />-12 coefficient 3<br />-13 coefficient 5<br />-1 coefficient $x$<br />On note $m$ la moyenne de cette série. Que doit valoir $x$ pour que $m = 8.75$ ?</div><div></div></div>",
          "classes": [],
          "style": ""
        }
      ];

    
    
    console.log(`Created ${papyrusJson.length} items for Papyrus (1 header, 1 title, ${studentExerciseSet.questions.length} questions)`);
    
    return papyrusJson;
}

/**
 * Apply Safari-specific inline styles to SVG
 */
function applySafariInlineStyles(svgString) {
    // Map of CSS classes to their inline styles
    const classToStyles = {
        'text-2xs': 'font-size: 0.625rem !important; line-height: 1 !important;',
        'text-xs': 'font-size: 0.75rem !important; line-height: 1rem !important;',
        'text-sm': 'font-size: 0.875rem !important; line-height: 1.25rem !important;',
        'text-base': 'font-size: 1rem !important; line-height: 1.5rem !important;'
    };
    
    // Apply inline styles for each class found
    for (const [className, styles] of Object.entries(classToStyles)) {
        if (svgString.includes(className)) {
            // Handle elements with only the class
            const classOnlyRegex = new RegExp(`class\\s*=\\s*["']${className}["']`, 'g');
            svgString = svgString.replace(classOnlyRegex, `class="${className}" style="${styles}"`);
            
            // Handle elements with the class among others (no existing style)
            const classAmongOthersRegex = new RegExp(`(class\\s*=\\s*["'][^"']*\\b)${className}(\\b[^"']*["'])(?![^>]*style)`, 'g');
            svgString = svgString.replace(classAmongOthersRegex, `$1${className}$2 style="${styles}"`);
            
            // Handle elements that already have style attribute
            const withStyleRegex = new RegExp(`(<[^>]+class\\s*=\\s*["'][^"']*\\b${className}\\b[^"']*["'][^>]*style\\s*=\\s*["'])([^"']*)(["'])`, 'g');
            svgString = svgString.replace(withStyleRegex, `$1$2; ${styles}$3`);
        }
    }
    
    return svgString;
}

/**
 * Preview a student's copy
 */
export async function previewStudentCopy(studentIndex, triggerPrint = false) {
    const state = getStateManager();
    const papyrus = getPapyrusManager();
    const progress = getProgressManager();
    
    // Check if we have student data
    if (!generationResults.students || studentIndex >= generationResults.students.length) {
        console.error('No student data available');
        return;
    }
    
    const student = generationResults.students[studentIndex];
    
    // Update state
    state.updateState({ currentStudentIndex: studentIndex });
    generationResults.currentStudentIndex = studentIndex;
    
    // Show loading
    const container = document.getElementById('pages-container');
    if (!container) return;
    
    container.innerHTML = '<div class="text-center p-8">Chargement...</div>';
    
    try {
        // Create Papyrus JSON
        const papyrusJson = await createPapyrusJson(student);
        currentPapyrusJson = papyrusJson;
        
        // Store in student object for reuse
        student.papyrusJson = papyrusJson;
        
        // Set JSON in textarea for Papyrus to read
        const jsonInput = document.getElementById('json-input');
        if (jsonInput) {
            jsonInput.value = JSON.stringify(papyrusJson, null, 2);
        }
        
        // Set up content model for Papyrus
        if (!window.contentModel) {
            window.contentModel = {
                items: [],
                loadFromJSON: function(json) { this.items = json; },
                updateMargins: function(margins) { this.margins = margins; }
            };
        }
        window.contentModel.loadFromJSON(papyrusJson);
        
        // Render using Papyrus manager
        await papyrus.renderStudent(papyrusJson, container);
        
        // Update pagination UI
        updatePaginationUI(studentIndex);
        
        // Trigger print if requested
        if (triggerPrint) {
            setTimeout(() => {
                const content = container.innerHTML;
                papyrus.print(content);
            }, 200);
        }
        
    } catch (error) {
        console.error('Error previewing student copy:', error);
        container.innerHTML = '<div class="alert alert-error">Erreur lors du chargement</div>';
    }
}

/**
 * Print current student copy
 */
export async function printStudentCopy(studentIndex) {
    await previewStudentCopy(studentIndex, true);
}

/**
 * Print all student copies - OPTIMIZED
 */
export async function printAllCopies() {
    const state = getStateManager();
    const papyrus = getPapyrusManager();
    const progress = getProgressManager();
    
    // Check system readiness
    if (!state.state.papyrusReady) {
        console.error('Papyrus not ready');
        return;
    }
    
    if (!generationResults.students || generationResults.students.length === 0) {
        console.error('No students to print');
        return;
    }
    
    // Update state
    state.updateState({ isPrinting: true });
    
    // Start progress
    progress.startOperation('printing-all', {
        max: generationResults.students.length,
        detail: `0 / ${generationResults.students.length} copies`
    });
    
    try {
        // Prepare student data with Papyrus JSON
        const studentsWithJson = [];
        
        for (let i = 0; i < generationResults.students.length; i++) {
            const student = generationResults.students[i];
            
            // Update progress
            progress.update(i, `Préparation copie ${i + 1} / ${generationResults.students.length}`);
            
            // Create or reuse Papyrus JSON
            if (!student.papyrusJson) {
                student.papyrusJson = await createPapyrusJson(student);
            }
            
            studentsWithJson.push(student);
        }
        
        // Render all students (in hidden container, not affecting preview)
        const allContent = await papyrus.renderAllStudents(
            studentsWithJson,
            (current, total) => {
                progress.update(current, `Rendu ${current} / ${total}`);
            }
        );
        
        // Complete progress
        progress.complete(`${generationResults.students.length} copies prêtes à imprimer`);
        
        // Trigger print
        setTimeout(() => {
            papyrus.print(allContent);
        }, 500);
        
    } catch (error) {
        console.error('Error printing all copies:', error);
        progress.error('Erreur lors de l\'impression', error.message);
    } finally {
        // Update state
        state.updateState({ isPrinting: false });
    }
}

/**
 * Generate teacher manifest
 */
export async function openTeacherManifest() {
    const state = getStateManager();
    const progress = getProgressManager();
    
    if (!generationResults.students || generationResults.students.length === 0) {
        console.error('No data for teacher manifest');
        return;
    }
    
    progress.startOperation('teacher-manifest', {
        max: 100,
        detail: 'Génération de la fiche enseignant'
    });
    
    try {
        // Generate manifest data
        const manifestData = {
            date: new Date().toLocaleDateString('fr-FR'),
            totalStudents: generationResults.students.length,
            totalQuestions: generationResults.students[0]?.selectedQuestions?.length || 0,
            answers: []
        };
        
        // Collect all answers
        generationResults.students.forEach((student, studentIndex) => {
            student.selectedQuestions?.forEach((question, questionIndex) => {
                if (!manifestData.answers[questionIndex]) {
                    manifestData.answers[questionIndex] = {
                        questionNumber: questionIndex + 1,
                        statement: question.statement,
                        studentAnswers: []
                    };
                }
                
                manifestData.answers[questionIndex].studentAnswers.push({
                    studentId: student.id,
                    answer: question.correctAnswer || question.expected || 'N/A'
                });
            });
        });
        
        progress.update(50, 'Formatage du document');
        
        // Create manifest HTML
        const manifestHtml = generateTeacherManifestHTML(manifestData);
        
        // Compress and create URL (if LZString is available)
        let url;
        if (typeof LZString !== 'undefined') {
            const compressed = LZString.compressToEncodedURIComponent(manifestHtml);
            url = `/sujets0/teacher-manifest#${compressed}`;
        } else {
            // Fallback: create data URL
            const blob = new Blob([manifestHtml], { type: 'text/html' });
            url = URL.createObjectURL(blob);
        }
        
        progress.complete('Fiche enseignant prête');
        
        // Open in new tab
        window.open(url, '_blank');
        
    } catch (error) {
        console.error('Error generating teacher manifest:', error);
        progress.error('Erreur lors de la génération');
    }
}

/**
 * Generate teacher manifest HTML
 */
function generateTeacherManifestHTML(data) {
    let html = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fiche Réponses Enseignant</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .question-section { margin-top: 30px; }
            </style>
        </head>
        <body>
            <h1>Fiche Réponses Enseignant</h1>
            <p>Date: ${data.date}</p>
            <p>Nombre d'élèves: ${data.totalStudents}</p>
            <p>Nombre de questions: ${data.totalQuestions}</p>
    `;
    
    data.answers.forEach(question => {
        html += `
            <div class="question-section">
                <h3>Question ${question.questionNumber}</h3>
                <p><strong>Énoncé:</strong> ${question.statement}</p>
                <table>
                    <thead>
                        <tr>
                            <th>Copie n°</th>
                            <th>Réponse attendue</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        question.studentAnswers.forEach(answer => {
            html += `
                <tr>
                    <td>${answer.studentId}</td>
                    <td>${answer.answer}</td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
    });
    
    html += `
        </body>
        </html>
    `;
    
    return html;
}

/**
 * Update pagination UI
 */
function updatePaginationUI(currentIndex) {
    const container = document.getElementById('student-pagination');
    if (!container) return;
    
    // If no current index provided, try to use the global one
    if (currentIndex === undefined) {
        currentIndex = generationResults.currentStudentIndex || 0;
    }
    
    container.innerHTML = '';
    
    const wrapper = document.createElement('div');
    wrapper.className = 'flex flex-wrap gap-1';
    
    generationResults.students.forEach((student, index) => {
        const button = document.createElement('button');
        button.className = index === currentIndex ? 
            'btn btn-xs btn-primary' : 
            'btn btn-xs btn-outline';
        button.textContent = (index + 1).toString();
        button.title = `Voir la copie de l'élève ${index + 1}`;
        button.onclick = () => previewStudentCopy(index);
        wrapper.appendChild(button);
    });
    
    container.appendChild(wrapper);
    
    // Update legend
    const legend = document.querySelector('[data-student-legend]');
    if (legend) {
        legend.textContent = `Copies - Copie ${currentIndex + 1}/${generationResults.students.length}`;
    }
}

/**
 * Update document settings
 */
function updateDocumentSettings() {
    const papyrus = getPapyrusManager();
    const settings = papyrus.getDocumentSettings();
    
    // Update CSS variables
    const root = document.documentElement;
    
    // Margins
    root.style.setProperty('--papyrus-margin-top', `${settings.margins.top}mm`);
    root.style.setProperty('--papyrus-margin-right', `${settings.margins.right}mm`);
    root.style.setProperty('--papyrus-margin-bottom', `${settings.margins.bottom}mm`);
    root.style.setProperty('--papyrus-margin-left', `${settings.margins.left}mm`);
    
    // Font sizes
    root.style.setProperty('--papyrus-font-size-h1', `${settings.fontSizes.h1}px`);
    root.style.setProperty('--papyrus-font-size-h2', `${settings.fontSizes.h2}px`);
    root.style.setProperty('--papyrus-font-size-h3', `${settings.fontSizes.h3}px`);
    root.style.setProperty('--papyrus-font-size-h4', `${settings.fontSizes.h4}px`);
    root.style.setProperty('--papyrus-font-size-h5', `${settings.fontSizes.h5}px`);
    root.style.setProperty('--papyrus-font-size-h6', `${settings.fontSizes.h6}px`);
    root.style.setProperty('--papyrus-font-size-body', `${settings.fontSizes.body}px`);
}

// Export functions for use in HTML
window.previewStudentCopy = previewStudentCopy;
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;
window.openTeacherManifest = openTeacherManifest;
window.createPaginationButtons = updatePaginationUI;

export {
    updateDocumentSettings,
    updatePaginationUI
};
