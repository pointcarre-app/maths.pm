/**
 * Sujets0 Question Generator - Comprehensive Script Module
 * Generates mathematics questions using Nagini Python execution engine
 * with KaTeX rendering and graph generation support
 */


// At the very top:
window.delayMathRendering = true;



console.log('🎯 Sujets0 Question Generator loading...');


// Write a function to extract the config from the URL query parameters
function extractConfigFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    let nbStudents = parseInt(urlParams.get('nbStudents')) || 2;
    let nbQuestions = parseInt(urlParams.get('nbQuestions')) || 12;
    const curriculum = urlParams.get('curriculum') || 'Spé';
    
    // Cap values at their limits and show toasts
    if (nbStudents > 50) {
        nbStudents = 50;
        setTimeout(() => showToast('📊 Nombre de copies limité à 50 (maximum autorisé)', 'warning'), 100);
    }
    if (nbStudents < 1) {
        nbStudents = 1;
        setTimeout(() => showToast('📊 Nombre de copies ajusté à 1 (minimum requis)', 'warning'), 100);
    }
    
    if (nbQuestions > 12) {
        nbQuestions = 12;
        setTimeout(() => showToast('📝 Nombre de questions limité à 12 (maximum de générateurs disponibles)', 'warning'), 200);
    }
    if (nbQuestions < 1) {
        nbQuestions = 1;
        setTimeout(() => showToast('📝 Nombre de questions ajusté à 1 (minimum requis)', 'warning'), 200);
    }
    
    return { nbStudents, nbQuestions, curriculum };
}



const configFromUrl = extractConfigFromUrl();


function showToast(message, type = 'error') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} fixed top-4 left-1/2 transform -translate-x-1/2 w-auto max-w-md shadow-lg z-50`;
    toast.innerHTML = `
      <div>
          <span>${message}</span>
      </div>
    `;
    document.body.appendChild(toast);
    
    // Auto-remove toast after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Config validation and capping is now handled in extractConfigFromUrl()




console.log("🟪🟪🟪 url config", extractConfigFromUrl());


// Configuration constants
const CONFIG = {
    teachersGitTag: 'v0.0.22',
    naginiGitTag: 'v0.0.21',
    v4PyJsGitTag: 'v0.0.27',
    rootSeed: 14,
    nbStudents: configFromUrl.nbStudents,
    nbQuestions: configFromUrl.nbQuestions,
    curriculum: configFromUrl.curriculum,
    
    // CDN URLs
    naginiJsUrl: 'https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js?bundle',
    naginiPyodideWorkerUrl: 'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js',
    v4PyJsPCAGraphLoaderUrl: 'https://cdn.jsdelivr.net/gh/pointcarre-app/v4.py.js@v0.0.27/scenery/packaged/PCAGraphLoader.js',
    
    // Teacher module URLs
    teachersUrlsToPaths: [
        { url: 'https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@v0.0.22/src/teachers/__init__.py', path: 'teachers/__init__.py' },
        { url: 'https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@v0.0.22/src/teachers/generator.py', path: 'teachers/generator.py' },
        { url: 'https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@v0.0.22/src/teachers/maths.py', path: 'teachers/maths.py' },
        { url: 'https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@v0.0.22/src/teachers/formatting.py', path: 'teachers/formatting.py' },
        { url: 'https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@v0.0.22/src/teachers/corrector.py', path: 'teachers/corrector.py' },
        { url: 'https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@v0.0.22/src/teachers/defaults.py', path: 'teachers/defaults.py' }
    ],
    
    // Generator files
    generators: [
        'spe_sujet1_auto_01_question.py',
        'spe_sujet1_auto_02_question.py',
        'spe_sujet1_auto_03_question.py',
        'spe_sujet1_auto_04_question.py',
        'spe_sujet1_auto_05_question.py',
        'spe_sujet1_auto_06_question.py',
        'spe_sujet1_auto_07_question.py',
        'spe_sujet1_auto_08_question.py',
        'spe_sujet1_auto_09_question.py',
        'spe_sujet1_auto_10_question.py',
        'spe_sujet1_auto_11_question.py',
        'spe_sujet1_auto_12_question.py'
    ],
    
    // Graph mappings
    generatorsToGraphs: {
        'spe_sujet1_auto_07_question.py': ['q7_small'],
        'spe_sujet1_auto_08_question.py': ['q8_small'],
        'spe_sujet1_auto_09_question.py': ['q9_small'],
        'spe_sujet1_auto_10_question.py': ['q10_small'],
        'spe_sujet1_auto_11_question.py': ['q11_case_a_small', 'q11_case_b_small', 'q11_case_c_small'],
        'spe_sujet1_auto_12_question.py': ['parabola_s1_a0', 'parabola_s1_am5', 'parabola_s1_ap5', 'parabola_sm1_a0', 'parabola_sm1_am5', 'parabola_sm1_ap10']
    }
};

// Global state
const STATE = {
    nagini: { module: null, manager: null, ready: false },
    pca: { loaderClass: null, loaderInstance: null },
    results: { questionResults: [] },
    ui: { container: null, loading: false }
};

// Utility functions
function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

function getBasePath() {
    if (window.location.hostname === 'pointcarre-app.github.io') {
        return '/maths.pm';
    } else if (window.location.pathname.startsWith('/maths.pm/')) {
        return '/maths.pm';
    }
    return '';
}

// Core initialization functions
async function loadNagini() {
    try {
        console.log('📦 Loading Nagini...');
        const naginiModule = await import(CONFIG.naginiJsUrl);
        STATE.nagini.module = naginiModule.Nagini;
        window.Nagini = naginiModule.Nagini;
        
        const manager = await naginiModule.Nagini.createManager(
            'pyodide',
            ['sympy', 'pydantic', 'strictyaml'],
            [],
            CONFIG.teachersUrlsToPaths,
            CONFIG.naginiPyodideWorkerUrl
        );
        
        await naginiModule.Nagini.waitForReady(manager);
        STATE.nagini.manager = manager;
        STATE.nagini.ready = true;
        
        console.log('✅ Nagini loaded and ready');
        return true;
    } catch (error) {
        console.error('❌ Failed to initialize Nagini:', error);
        STATE.nagini.ready = false;
        return false;
    }
}

async function loadPCAGraphLoader() {
    try {
        console.log('📊 Loading PCA Graph Loader...');
        const module = await import(CONFIG.v4PyJsPCAGraphLoaderUrl);
        STATE.pca.loaderClass = module.PCAGraphLoader;
        
        // Initialize the loader with proper config
        const instance = new module.PCAGraphLoader({
            debug: false,
            graphConfig: {},
            pcaVersion: CONFIG.v4PyJsGitTag
        });
        
        await instance.initialize();
        STATE.pca.loaderInstance = instance;
        console.log('✅ PCA Graph Loader ready');
        return true;
    } catch (error) {
        console.error('❌ Failed to load PCA Graph Loader:', error);
        return false;
    }
}

// Question generation functions
async function executeGeneratorWithSeed(filename, seed) {
    const manager = STATE.nagini.manager;
    if (!manager) {
        return { success: false, error: 'Nagini manager not initialized' };
    }
    
    const basePath = getBasePath();
    const url = `${basePath}/static/sujets0/generators/${filename}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
        
        let pythonCode = await response.text();
        

        // Also random.Seed in some generators... TODO sel
        // seems better here only
        // Technically the same seed
        // But this doesnt run in doppel:backend..
        // so duplication for safety locally + ?? 
        // compare wiyh a new doppel


        // Inject seed
        const seedInjection = `\nimport random\nrandom.seed(${seed})\n\n# Override the default SEED\nimport teachers.defaults\nteachers.defaults.SEED = ${seed}\n\n`;
        
        pythonCode = pythonCode.replace(
            'components = generate_components(None)',
            `components = generate_components(None, ${seed})`
        );
        pythonCode = seedInjection + pythonCode;
        
        const result = await manager.executeAsync(filename, pythonCode);
        const success = !result.error && (result.exit_code === 0 || result.missive);
        
        if (result.missive && success) {
            try {
                const data = JSON.parse(result.missive);
                return {
                    success: true,
                    statement: data.statement || data.question,
                    statementHtml: data.statement_html,
                    answer: data.answer,
                    data: data,
                    stdout: result.stdout,
                    stderr: result.stderr
                };
            } catch (e) {
                return { success: false, error: 'Failed to parse output' };
            }
        } else {
            return {
                success: false,
                error: result.error || 'Execution failed',
                stdout: result.stdout,
                stderr: result.stderr
            };
        }
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function buildPCAGraph(graphKey, params = {}) {
    if (!STATE.pca.loaderInstance) {
        console.warn('PCA Graph Loader not initialized, skipping graph generation');
        return { svg: null, graphDict: null };
    }
    
    try {
        // Update config if params provided
        if (params && Object.keys(params).length > 0) {
            STATE.pca.loaderInstance.updateConfig(params);
        }
        
        const result = await STATE.pca.loaderInstance.renderGraph(graphKey);
        return {
            svg: result.svg,
            graphDict: result.graphDict || result
        };
    } catch (error) {
        console.error(`Failed to build graph ${graphKey}:`, error);
        return { svg: null, graphDict: null };
    }
}

async function attachGraphToResult(result, generator) {
    try {
        if (generator === 'spe_sujet1_auto_07_question.py') {
            const Y_LABEL_FOR_HORIZONTAL_LINE = parseInt(result.data.components.n);
            console.log(`🎨 Generating graph q7_small with Y_LABEL_FOR_HORIZONTAL_LINE=${Y_LABEL_FOR_HORIZONTAL_LINE}`);
            const svgAndDict = await buildPCAGraph('q7_small', { Y_LABEL_FOR_HORIZONTAL_LINE });
            result.graphSvg = svgAndDict.svg;
            result.graphDict = svgAndDict.graphDict;
        } else if (generator === 'spe_sujet1_auto_08_question.py') {
            const A_FLOAT_FOR_AFFINE_LINE = parseFloat(result.data.components_evaluated.a);
            const B_FLOAT_FOR_AFFINE_LINE = parseFloat(result.data.components_evaluated.b);
            console.log(`🎨 Generating graph q8_small with A=${A_FLOAT_FOR_AFFINE_LINE}, B=${B_FLOAT_FOR_AFFINE_LINE}`);
            const svgAndDict = await buildPCAGraph('q8_small', { A_FLOAT_FOR_AFFINE_LINE, B_FLOAT_FOR_AFFINE_LINE });
            result.graphSvg = svgAndDict.svg;
            result.graphDict = svgAndDict.graphDict;
        } else if (generator === 'spe_sujet1_auto_10_question.py') {
            const aFromParabola = parseInt(result.data.components.a);
            const cFromParabola = parseInt(result.data.components.c);
            let PARABOLA_GRAPH_KEY;
            const A_SHIFT_MAGNITUDE = Math.abs(cFromParabola);
            
            if (aFromParabola > 0) {
                if (cFromParabola > 0) PARABOLA_GRAPH_KEY = 'parabola_s1_ap';
                else if (cFromParabola < 0) PARABOLA_GRAPH_KEY = 'parabola_s1_am';
                else PARABOLA_GRAPH_KEY = 'parabola_s1_a0';
            } else {
                if (cFromParabola > 0) PARABOLA_GRAPH_KEY = 'parabola_sm1_ap';
                else if (cFromParabola < 0) PARABOLA_GRAPH_KEY = 'parabola_sm1_am';
                else PARABOLA_GRAPH_KEY = 'parabola_sm1_a0';
            }
            
            const svgAndDict = await buildPCAGraph(PARABOLA_GRAPH_KEY, { A_SHIFT_MAGNITUDE });
            result.graphSvg = svgAndDict.svg;
            result.graphDict = svgAndDict.graphDict;
        } else if (generator === 'spe_sujet1_auto_11_question.py') {
            const caseFromGenerator = result.data.components.case;
            let key;
            if (caseFromGenerator === 'case_a') key = 'q11_case_a_small';
            else if (caseFromGenerator === 'case_b') key = 'q11_case_b_small';
            else if (caseFromGenerator === 'case_c') key = 'q11_case_c_small';
            else throw new Error(`Invalid case: ${caseFromGenerator}`);
            
            const svgAndDict = await buildPCAGraph(key, {});
            result.graphSvg = svgAndDict.svg;
            result.graphDict = svgAndDict.graphDict;
        }
    } catch (error) {
        console.error(`Failed to attach graph for ${generator}:`, error);
    }
}

// SVG Inline Styles Mapping (from pm.css and utility classes)
const SVG_INLINE_STYLES = {
    svg: {
        'display': 'block',
        'max-width': '100%',
        'height': 'auto'
    },
    foreignObject: {
        'overflow': 'visible'
    },
    'foreignObject > div': {
        'width': '100%',
        'height': '100%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    },
    '.svg-latex': {
        'line-height': '1.2',
        'text-align': 'center'
    },
    '.svg-latex .katex': {
        'font-family': "'KaTeX_Main', sans-serif"
    },
    // Font size utility classes
    '.text-sm': {
        'font-size': '0.875rem',
        'line-height': '1.25rem'
    },
    '.text-xs': {
        'font-size': '0.75rem',
        'line-height': '1rem'
    },
    '.text-2xs': {
        'font-size': '0.625rem',
        'line-height': '1rem'
    }
};

// Helper function to apply inline styles to an element
function applyInlineStyles(element, styles) {
    Object.entries(styles).forEach(([property, value]) => {
        // Convert kebab-case to camelCase for style properties
        const camelProperty = property.replace(/-([a-z])/g, (match, letter) => letter.toUpperCase());
        element.style[camelProperty] = value;
    });
}

// Helper function to apply styles based on CSS classes
function applyStylesFromClasses(element) {
    const classList = Array.from(element.classList);
    
    classList.forEach(className => {
        const styleKey = `.${className}`;
        if (SVG_INLINE_STYLES[styleKey]) {
            applyInlineStyles(element, SVG_INLINE_STYLES[styleKey]);
        }
    });
    
    // Also apply to nested elements with these classes
    ['text-sm', 'text-xs', 'text-2xs'].forEach(textClass => {
        const elements = element.querySelectorAll(`.${textClass}`);
        elements.forEach(el => {
            if (SVG_INLINE_STYLES[`.${textClass}`]) {
                applyInlineStyles(el, SVG_INLINE_STYLES[`.${textClass}`]);
            }
        });
    });
}

// SVG KaTeX Processing with Inline Styles (inspired by index-graphs.js)
async function processKatexInSvg(svgString) {
    if (typeof katex === 'undefined') {
        console.warn('KaTeX not available for SVG processing');
        return svgString;
    }
    
    try {
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
        const svgElement = svgDoc.querySelector('svg');
        if (!svgElement) return svgString;

        // Apply inline styles to SVG element
        svgElement.classList.add('graph-svg-container');
        applyInlineStyles(svgElement, SVG_INLINE_STYLES.svg);
        console.log('🎨 Applied inline styles to SVG element');
        
        // Find all foreignObject elements and apply styles
        const foreignObjects = svgElement.querySelectorAll('foreignObject');
        
        foreignObjects.forEach((fo) => {
            // Apply inline styles to foreignObject
            applyInlineStyles(fo, SVG_INLINE_STYLES.foreignObject);
            
            // Apply styles to direct child divs of foreignObject
            const childDivs = fo.querySelectorAll(':scope > div');
            childDivs.forEach(div => {
                applyInlineStyles(div, SVG_INLINE_STYLES['foreignObject > div']);
                // Apply font size classes if present
                applyStylesFromClasses(div);
            });
        });
        
        foreignObjects.forEach((fo) => {
            // Find div.svg-latex elements (exactly like index-graphs.js)
            const latexDivs = fo.querySelectorAll('div.svg-latex');
            
            
            latexDivs.forEach((div) => {
                div.classList.add('svg-latex');
                // Apply inline styles to svg-latex elements
                applyInlineStyles(div, SVG_INLINE_STYLES['.svg-latex']);
                // Apply font size classes if present
                applyStylesFromClasses(div);
                
                const latex = div.textContent.trim();
                if (!latex) return;
                
                try {
                    // Preserve original styling
                    const bgColor = div.style.backgroundColor;
                    const color = div.style.color;
                    
                    // Clear and render KaTeX directly (like index-graphs.js line 94-98)
                    div.innerHTML = '';
                    katex.render(latex, div, {
                        throwOnError: false,
                        displayMode: false
                    });
                    
                    // Apply inline styles to rendered KaTeX elements
                    const katexElements = div.querySelectorAll('.katex');
                    katexElements.forEach(katexEl => {
                        applyInlineStyles(katexEl, SVG_INLINE_STYLES['.svg-latex .katex']);
                        
                        // Apply font family AND size to all nested elements in KaTeX
                        katexEl.querySelectorAll('*').forEach(nestedEl => {
                            nestedEl.style.fontFamily = "'KaTeX_Main', sans-serif";
                            // Inherit font size from parent div (which has text-2xs, text-xs, etc.)
                            nestedEl.style.fontSize = 'inherit';
                        });
                        
                        // Also ensure the katex root element inherits size
                        katexEl.style.fontSize = 'inherit';
                    });
                    
                    // Restore colors (like index-graphs.js line 99-105)
                    if (bgColor) div.style.backgroundColor = bgColor;
                    if (color) {
                        div.querySelectorAll('.katex, .katex *').forEach(el => {
                            el.style.color = color;
                        });
                    }
                } catch (e) {
                    console.error('KaTeX error in SVG:', e);
                    div.textContent = latex; // Fallback to original
                }
            });
        });
        
        // Final pass: apply font size classes to any remaining elements in the entire SVG
        ['text-sm', 'text-xs', 'text-2xs'].forEach(textClass => {
            const elements = svgElement.querySelectorAll(`.${textClass}`);
            elements.forEach(el => {
                if (SVG_INLINE_STYLES[`.${textClass}`]) {
                    applyInlineStyles(el, SVG_INLINE_STYLES[`.${textClass}`]);
                    
                    // AGGRESSIVE: Force font size on all nested elements too
                    const fontSize = SVG_INLINE_STYLES[`.${textClass}`]['font-size'];
                    const lineHeight = SVG_INLINE_STYLES[`.${textClass}`]['line-height'];
                    
                    el.querySelectorAll('*').forEach(nestedEl => {
                        nestedEl.style.fontSize = fontSize;
                        nestedEl.style.lineHeight = lineHeight;
                    });
                    
                    console.log(`🎨 Applied ${textClass} inline styles (${fontSize}) to element and all children`);
                }
            });
        });
        
        // Serialize back to string with processed KaTeX and inlined styles
        const serializer = new XMLSerializer();
        return serializer.serializeToString(svgElement);
    } catch (error) {
        console.error('SVG KaTeX processing failed:', error);
        return svgString; // Return original on error
    }
}

// Print functionality
function addPrintButton(container) {
    const printButtonContainer = document.createElement('div');
    printButtonContainer.className = 'print-button-container mb-4 text-right';
    printButtonContainer.innerHTML = `
        <div class="flex flex-col items-end gap-2">
            <button id="print-questions-btn" class="btn btn-primary btn-sm print-hide">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z">
                    </path>
                </svg>
                Imprimer
            </button>
            <div class="text-xs text-gray-600 print-hide text-right">
                 Optimisé pour Chrome ✅<br>
                 Corrigé enseignant inclus 📝<br>
                 Activer les "Graphiques d'arrière-plan" 💡<br>
                 Possibilité d'ajuster les marges 🛠️
            </div>
        </div>
    `;
    
    // Create Table of Contents container
    const tocContainer = document.createElement('div');
    tocContainer.className = 'toc-container w-full mb-4 print-hide';
    tocContainer.innerHTML = `
        <h3 class="text-lg font-semibold mb-3 text-gray-800">📑 Sommaire</h3>
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-3">
            <div id="toc-links" class="max-h-[300px] overflow-y-auto space-y-1">
                <div class="text-xs text-gray-500 italic">Le sommaire sera généré après le chargement des questions...</div>
            </div>
        </div>
    `;
    
    container.appendChild(printButtonContainer);
    container.appendChild(tocContainer);
    
    // Add click handler
    const printBtn = printButtonContainer.querySelector('#print-questions-btn');
    printBtn.addEventListener('click', handlePrint);
}

function handlePrint() {
    // Create print-specific styles if they don't exist
    addPrintStyles();
    
    // Mark the container for printing
    const pmContainer = document.querySelector('.pm-container .max-w-\\[640px\\]');
    if (pmContainer) {
        pmContainer.classList.add('print-target');
    }
    
    // Force open teacher details for printing
    const teacherDetails = document.querySelector('.teacher-answer-details');
    const wasOpen = teacherDetails ? teacherDetails.open : false;
    
    if (teacherDetails && !wasOpen) {
        teacherDetails.open = true;
        console.log('🖨️ Temporarily opened teacher details for printing');
    }
    
    // Try to use the modern print API with no margins
    if (window.navigator && window.navigator.userAgent.includes('Chrome')) {
        // For Chrome, we can try to influence print settings via CSS
        // The print dialog will open but user may need to select "More settings" > "Margins" > "None"
        console.log('💡 Chrome detected: Please select "More settings" > "Margins" > "None" in print dialog');
    }
    
    // Trigger print dialog
    window.print();
    
    // Clean up after print dialog closes
    setTimeout(() => {
        if (pmContainer) {
            pmContainer.classList.remove('print-target');
        }
        
        // Restore original details state
        if (teacherDetails && !wasOpen) {
            teacherDetails.open = false;
            console.log('🖨️ Restored teacher details to closed state');
        }
    }, 1000);
}

function addPrintStyles() {
    const existingStyles = document.querySelector('#sujets0-print-styles');
    if (existingStyles) return;
    
    const printStyles = document.createElement('style');
    printStyles.id = 'sujets0-print-styles';
    printStyles.textContent = `
        @media print {
            /* Remove all default margins and padding */
            @page {
                margin: 0 !important;
                padding: 1cm !important;
                size: A4;
            }
            
            /* Hide everything by default */
            body * {
                visibility: hidden;
            }
            
            /* Show only the print target and its children */
            .print-target,
            .print-target * {
                visibility: visible;
            }
            
            /* Position the print target with minimal margins */
            .print-target {
                position: absolute;
                left: 0;
                top: 0;
                width: 100% !important;
                max-width: none !important;
                margin: 0 !important;
                padding: 10px !important;
            }
            
            /* Remove body margins */
            body {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* Hide print button and other UI elements */
            .print-hide,
            .print-button-container,
            .toc-container,
            .navbar,
            .footer,
            .sidebar-fixed {
                display: none !important;
            }
            
            /* Page break before each h2 EXCEPT the teacher copy */
            .fragment-wrapper[data-f_type="h2_"]:not(:first-of-type) {
                page-break-before: always;
            }
            
            /* Keep header and teacher table together - more specific targeting */
            .fragment-wrapper:first-child,
            .fragment-wrapper:first-child + .fragment-wrapper,
            .fragment-wrapper:nth-child(2),
            .fragment-wrapper:nth-child(3) {
                page-break-before: avoid !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
            }
            
            /* Force teacher answer details to be open when printing */
            .teacher-answer-details {
                display: block !important;
            }
            
            .teacher-answer-details summary {
                display: none !important;
            }
            
            .teacher-answer-details > div {
                display: block !important;
                margin-top: 0 !important;
            }
            
            /* Specifically target the teacher answer table to stay with header */
            #teacher-answer-table,
            .teacher-table-section,
            .fragment-wrapper.teacher-table-section,
            .fragment-wrapper:has(#teacher-answer-table),
            .fragment-wrapper[data-f_type="p_"]:has(#teacher-answer-table) {
                page-break-before: avoid !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            
            /* Keep table together with previous content - multiple approaches for browser compatibility */
            .fragment-wrapper[data-f_type="p_"] table,
            table {
                page-break-before: avoid !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            
            /* Force first several fragments to stay together - multiple approaches */
            .fragment-wrapper:nth-child(-n+4) {
                page-break-before: avoid !important;
                page-break-after: avoid !important;
                break-after: avoid !important;
            }
            
            /* Alternative approach: explicitly target the sequence we want together */
            .fragment-wrapper:first-of-type ~ .fragment-wrapper.teacher-table-section {
                page-break-before: avoid !important;
                break-before: avoid !important;
            }
            
            /* Ensure the divider after teacher table doesn't force a break */
            .fragment-wrapper[data-f_type="hr_"]:nth-child(-n+5) {
                page-break-before: avoid !important;
                page-break-after: auto;
            }
            
            /* Avoid breaking inside divisions/questions */
            .fragment-wrapper {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Special handling for question blocks with graphs */
            .fragment-wrapper[data-f_type="p_"] {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Ensure graphs don't get cut */
            .graph-svg-container {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Adjust font sizes for print */
            body {
                font-size: 12pt;
                line-height: 1.4;
            }
            
            /* Specific paragraph and content font sizes */
            .print-target p,
            .print-target .fragment p,
            .print-target .fragment-wrapper p,
            .print-target div {
                font-size: 12pt !important;
                line-height: 1.5 !important;
            }
            
            /* Question text in flex containers */
            .print-target .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] > div,
            .print-target .fragment-wrapper[data-f_type="p_"] div > div {
                font-size: 12pt !important;
                line-height: 1.5 !important;
            }
            
            /* Headers */
            h1, .print-target h1 { font-size: 18pt !important; }
            h2, .print-target h2 { foformat: Copy-Seed-Q#nt-size: 16pt !important; }
            h3, .print-target h3 { font-size: 14pt !important; }
            
            /* Math expressions */
            .katex, .print-target .katex {
                font-size: 12pt !important;
                color: black;
            }
            
            /* Ensure SVGs scale properly */
            svg {
                max-width: 100%;
                height: auto;
            }

            /* Utilities */
            .text-primary {
                color: black;
            }

            .text-secondary {
                color: black;
            }

            .text-accent {
                color: black;
            }
            
            /* Hide details styling for print */
            .teacher-answer-details[open] summary::before,
            .teacher-answer-details summary::before {
                display: none !important;
            }
            
            /* Hide the native disclosure triangle for print */
            .teacher-answer-details summary::-webkit-details-marker,
            .teacher-answer-details summary::marker {
                display: none !important;
            }
            
            /* Preserve flex layouts for print - keep question and graph side by side */
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] {
                display: flex !important;
                flex-wrap: wrap !important;
                gap: 15px !important;
                align-items: flex-start !important;
            }
            
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] > div {
                margin-bottom: 0 !important;
            }
            
            /* Ensure text content has proper width in flex */
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] > div:first-child {
                flex: 1 1 250px !important;
                min-width: 250px !important;
            }
            
            /* Ensure graph containers maintain their size */
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] .graph-svg-container {
                flex: 0 1 auto !important;
                max-width: 300px !important;
            }
            
            /* Note: SVG styles are now inlined directly into SVG elements for better print compatibility */
            /* Container wrapper still needs this for layout */
            .graph-svg-container {
                position: relative !important;
                display: block !important;
                overflow: hidden !important;
            }
        }
    `;
    
    document.head.appendChild(printStyles);
}

// Add screen styles for the details/summary animation
function addScreenStyles() {
    const existingStyles = document.querySelector('#sujets0-screen-styles');
    if (existingStyles) return;
    
    const screenStyles = document.createElement('style');
    screenStyles.id = 'sujets0-screen-styles';
    screenStyles.textContent = `
        /* Teacher answer details styling */
        .teacher-answer-details summary {
            position: relative;
            list-style: none;
            padding-left: 1.5rem;
            transition: color 0.2s ease;
        }
        
        /* Hide default browser markers */
        .teacher-answer-details summary::-webkit-details-marker,
        .teacher-answer-details summary::marker {
            display: none;
        }
        
        /* Custom arrow */
        .teacher-answer-details summary::before {
            content: '▶';
            position: absolute;
            left: 0;
            top: 0;
            font-size: 0.875rem;
            transition: transform 0.3s ease;
            transform-origin: center;
        }
        
        /* Rotate arrow when open */
        .teacher-answer-details[open] summary::before {
            transform: rotate(90deg);
        }
        
        /* Hover effects */
        .teacher-answer-details summary:hover::before {
            color: #4b5563;
        }
    `;
    
    document.head.appendChild(screenStyles);
}

// Table of Contents functionality
function populateTableOfContents() {
    const tocLinksContainer = document.querySelector('#toc-links');
    if (!tocLinksContainer) {
        console.warn('TOC container not found');
        return;
    }
    
    // Clear the placeholder text
    tocLinksContainer.innerHTML = '';
    
    let linkCount = 0;
    
    // First, add the teacher table if it exists
    const teacherTable = document.querySelector('#teacher-answer-table');
    if (teacherTable) {
        const linkElement = document.createElement('div');
        linkElement.className = 'toc-link-wrapper';
        linkElement.innerHTML = `
            <a href="#teacher-answer-table" class="toc-link block px-2 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors duration-150 border-l-2 border-transparent hover:border-blue-300">
                Corrigé Enseignant
            </a>
        `;
        
        tocLinksContainer.appendChild(linkElement);
        linkCount++;
        
        // Add smooth scroll behavior to the link
        const link = linkElement.querySelector('a');
        link.addEventListener('click', (e) => {
            e.preventDefault();
            teacherTable.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Update URL hash without jumping
            history.pushState(null, null, '#teacher-answer-table');
        });
    }
    
    // Then, find all H2 elements that were generated as fragments
    const h2Elements = document.querySelectorAll('.fragment-wrapper[data-f_type="h2_"] h2[id]');
    
    // Create links for each H2
    h2Elements.forEach((h2, index) => {
        const id = h2.getAttribute('id');
        const text = h2.textContent.trim();
        
        if (id && text) {
            const linkElement = document.createElement('div');
            linkElement.className = 'toc-link-wrapper';
            linkElement.innerHTML = `
                <a href="#${id}" class="toc-link block px-2 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors duration-150 border-l-2 border-transparent hover:border-blue-300">
                    ${text}
                </a>
            `;
            
            tocLinksContainer.appendChild(linkElement);
            linkCount++;
            
            // Add smooth scroll behavior to the link
            const link = linkElement.querySelector('a');
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetElement = document.querySelector(`#${id}`);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Update URL hash without jumping
                    history.pushState(null, null, `#${id}`);
                }
            });
        }
    });
    
    // Show message if no links found
    if (linkCount === 0) {
        tocLinksContainer.innerHTML = '<div class="text-xs text-gray-500 italic">Aucun titre trouvé</div>';
    }
    
    console.log(`✅ TOC populated with ${linkCount} links (${teacherTable ? '1 table + ' : ''}${h2Elements.length} sections)`);
}

// Helper function to inject question number into statementHtml
function injectQuestionNumber(statementHtml, questionNum) {
    if (!statementHtml || !questionNum) return statementHtml;
    
    // Create a temporary DOM element to parse the HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = statementHtml;
    
    // Recursive function to find the first text node in the DOM tree
    function findFirstTextLocation(element) {
        for (let child of element.childNodes) {
            if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
                // Found a non-empty text node
                return { textNode: child, parent: element };
            } else if (child.nodeType === Node.ELEMENT_NODE) {
                // Recursively search in child elements
                const result = findFirstTextLocation(child);
                if (result) return result;
            }
        }
        return null;
    }
    
    // Find the first div and then search for the first text content within it
    const firstDiv = tempDiv.querySelector('div');
    if (firstDiv) {
        const textLocation = findFirstTextLocation(firstDiv);
        if (textLocation) {
            // Prepend question number to the found text node
            textLocation.textNode.textContent = `${questionNum})  ${textLocation.textNode.textContent}`;
        } else {
            // If no text found, insert at the beginning of the first div
            const questionText = document.createTextNode(`${questionNum})  `);
            firstDiv.insertBefore(questionText, firstDiv.firstChild);
        }
        return tempDiv.innerHTML;
    }
    
    // Fallback: if no div found, just prepend the question number
    return `${questionNum})  ${statementHtml}`;
}

// PM Fragment Generation System
class PMFragmentGenerator {
    static createParagraph(content, classes = []) {
        return {
            f_type: { value: 'p_' },
            html: content,
            data: {},
            class_list: classes,
            classes: classes.join(' ')
        };
    }
    
    static createH2(content, classes = []) {
        const slug = content.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
        const allClasses = [...classes, "text-xl", "mb-4"];
        return {
            f_type: { value: 'h2_' },
            html: content,
            data: { id_href: slug },
            class_list: allClasses,
            classes: allClasses.join(' '),
            slug: slug
        };
    }
    
    static createSvg(svgContent, graphDict = {}, classes = []) {
        return {
            f_type: { value: 'svg_' },
            html: '',
            data: {
                src: '',
                content: svgContent
            },
            class_list: classes,
            classes: classes.join(' ')
        };
    }
    
    static createDivider(classes = []) {
        const allClasses = [...classes, "my-4", "border-base-300"];
        return {
            f_type: { value: 'hr_' },
            html: '',
            data: {},
            class_list: allClasses,
            classes: allClasses.join(' ')
        };
    }
}

class PMFragmentRenderer {
    static renderFragment(fragment) {
        const wrapper = document.createElement('div');
        wrapper.className = `fragment-wrapper ${fragment.classes}`;
        wrapper.setAttribute('data-f_type', fragment.f_type.value);
        
        const fragmentDiv = document.createElement('div');
        fragmentDiv.className = 'fragment';
        fragmentDiv.setAttribute('data-f_type', fragment.f_type.value);
        
        // Render based on fragment type (matching PM templates exactly)
        switch (fragment.f_type.value) {
            case 'p_':
                // Apply classes to the fragment div for paragraphs
                if (fragment.classes) {
                    fragmentDiv.className += ` ${fragment.classes}`;
                }
                fragmentDiv.innerHTML = fragment.html;
                break;
                
            case 'h2_':
                const h2Classes = fragment.classes ? ` class="${fragment.classes}"` : '';
                fragmentDiv.innerHTML = `<h2 id="${fragment.data.id_href || ''}"${h2Classes}>${fragment.html}</h2>`;
                break;
                
            case 'svg_':
                // Apply classes to the fragment div for SVGs
                if (fragment.classes) {
                    fragmentDiv.className += ` ${fragment.classes}`;
                }
                fragmentDiv.innerHTML = fragment.data.content;
                break;
                
            case 'hr_':
                const hrClasses = fragment.classes ? ` class="${fragment.classes}"` : '';
                fragmentDiv.innerHTML = `<hr${hrClasses}>`;
                break;
                
            default:
                if (fragment.classes) {
                    fragmentDiv.className += ` ${fragment.classes}`;
                }
                fragmentDiv.innerHTML = fragment.html;
        }
        
        wrapper.appendChild(fragmentDiv);
        return wrapper;
    }
}

// Main execution function
async function executeAllGenerators() {
    console.log('🚀 Starting question generation...');
    
    // Select generators up to the requested amount (capped at 12)
    const selectedGenerators = CONFIG.generators.slice(0, CONFIG.nbQuestions);
    console.log(`📝 Selected ${selectedGenerators.length} generators`);
    const questionResults = [];
    
    for (let studentNum = 1; studentNum <= CONFIG.nbStudents; studentNum++) {
        const seed = CONFIG.rootSeed + studentNum;
        
        let generatorNum = 1;
        for (const generator of selectedGenerators) {
            try {
                console.log(`📝 Generating Q${generatorNum} for Student ${studentNum} (${generator})`);
                const result = await executeGeneratorWithSeed(generator, seed);
                
                result.student = studentNum;
                result.seed = seed;
                result.generator = generator;
                result.generatorNum = generatorNum;
                generatorNum++;
                
                // Attach graphs where needed
                await attachGraphToResult(result, generator);
                
                // Process KaTeX directly in SVG foreignObjects
                if (result.graphSvg) {
                    result.graphSvgWithRenderedLatex = await processKatexInSvg(result.graphSvg);
                }
                
                questionResults.push(result);
            } catch (error) {
                console.error(`❌ Error generating Q${generatorNum}:`, error);
                questionResults.push({
                    success: false,
                    error: error.message,
                    student: studentNum,
                    generator: generator,
                    generatorNum: generatorNum
                });
                generatorNum++;
            }
        }
    }
    
    STATE.results.questionResults = questionResults;
    console.log(`✅ Generated ${questionResults.length} questions`);
    return questionResults;
}

// Helper function to format answers for teacher table
function formatAnswersForTeacherTable(result, answerType) {
    if (!result.success || !result.answer) {
        return 'Erreur';
    }
    
    const answers = result.answer[answerType];
    
    // Handle both array and single answer formats
    if (Array.isArray(answers)) {
        // Join multiple answers with semicolon and non-breaking spaces
        return answers.map(answer => `$${answer}$`).join('&nbsp;;&nbsp;');
    } else {
        // Single answer format (some sujet2 generators)
        return `$${answers}$`;
    }
}

// Pure PM Fragment Generation - No Custom UI
function generateFragmentsFromResults(results) {
    const fragments = [];
    
    // Header fragment
    fragments.push(PMFragmentGenerator.createParagraph('<span class="font-mono">Spécialité Maths - 12 questions par copie</span>'));
    
    // Create Teacher Copy section first
    
    // Generate teacher answer table with ID for TOC
    let tableHtml = `
        <div id="teacher-answer-table">
            <details class="teacher-answer-details">
                <summary class="text-lg mb-3 text-gray-800 cursor-pointer hover:text-gray-600 select-none">
                    Corrigé Enseignant
                </summary>
                <div class="mt-3">
                    <table class="table table-zebra w-full border border-gray-300">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-3 py-2" style="text-align:left !important; width: 25%; min-width: 200px;">
                            ID
                        </th>
                        <th class="border border-gray-300 px-3 py-2" style="text-align:right !important; width: 37.5%;">Réponse</th>
                        <th class="border border-gray-300 px-3 py-2" style="text-align:right !important; width: 37.5%;">Simplifiée</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    // Sort results by student, then by question number
    const sortedResults = results.slice().sort((a, b) => {
        if (a.student !== b.student) {
            return a.student - b.student;
        }
        return a.generatorNum - b.generatorNum;
    });
    
    // Add table rows
    sortedResults.forEach(result => {
        const latexAnswers = formatAnswersForTeacherTable(result, 'latex');
        const simplifiedAnswers = formatAnswersForTeacherTable(result, 'simplified_latex');
        
        // Create combined column content: [StudentNum]-([seed])-[QuestionNum]<br>generator
        const studentNum = result.student || 'N/A';
        const seed = result.seed || 'N/A';
        const questionNum = result.generatorNum || 'N/A';
        const generator = result.generator || 'N/A';
        
        // Generate the correct URL for the generator file
        const basePath = getBasePath();
        const generatorUrl = `${basePath}/static/sujets0/generators/${generator}`;
        
        const combinedInfo = `${studentNum}-(${seed})-${questionNum}<br><a href="${generatorUrl}" target="_blank" class="font-mono text-xs text-blue-600 hover:text-base-content underline">${generator}</a>`;
        
        tableHtml += `
            <tr>
                <td class="border border-gray-300 px-3 py-2" style="text-align:left !important; vertical-align:top !important; line-height:1.3;">${combinedInfo}</td>
                <td class="border border-gray-300 px-3 py-2" style="text-align:right !important; vertical-align:middle !important;">${latexAnswers}</td>
                <td class="border border-gray-300 px-3 py-2" style="text-align:right !important; vertical-align:middle !important;">${simplifiedAnswers}</td>
            </tr>
        `;
    });
    
    tableHtml += `
                </tbody>
                    </table>
                </div>
            </details>
        </div>
    `;
    
    fragments.push(PMFragmentGenerator.createParagraph(tableHtml, ['teacher-table-section']));
    
    // Add separator between teacher section and student copies
    fragments.push(PMFragmentGenerator.createDivider());
    
    // Group by student
    const byStudent = results.reduce((acc, r) => {
        const key = r && r.student != null ? String(r.student) : 'N/A';
        (acc[key] ||= []).push(r);
        return acc;
    }, {});
    
    for (const student of Object.keys(byStudent)) {
        // Student header if multiple students

        
        if (Object.keys(byStudent).length > 1) {
            fragments.push(PMFragmentGenerator.createH2(`Bac 1ère - Première Partie : Automatismes - n°${student}`, ['font-mono']));
        }
        
        byStudent[student].forEach((result) => {
            // Preprocess statementHtml to inject question number properly
            let processedStatementHtml;
            if (result.success) {
                processedStatementHtml = injectQuestionNumber(result.statementHtml, result.generatorNum);
            } else {
                processedStatementHtml = `${result.generatorNum}) Erreur de génération`;
            }
            
            // Check if we have a graph to display alongside the question
            if (result.success && result.graphSvgWithRenderedLatex) {
                // DEBUG: Log what we're working with
                console.log('DEBUG processedStatementHtml:', processedStatementHtml);
                
                // For flex layout, we need to extract the content from the div and put the question number inside the flex text container
                // Use DOM parsing for more reliable content extraction
                let textContent;
                try {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(`<html><body>${processedStatementHtml}</body></html>`, 'text/html');
                    const firstDiv = doc.querySelector('div');
                    textContent = firstDiv ? firstDiv.innerHTML : processedStatementHtml;
                    console.log('DEBUG extracted textContent:', textContent);
                } catch (e) {
                    console.log('DEBUG DOM parsing failed, using fallback');
                    // Fallback to regex if DOM parsing fails
                    const contentMatch = processedStatementHtml.match(/^<div[^>]*>(.*)<\/div>$/s);
                    textContent = contentMatch ? contentMatch[1] : processedStatementHtml;
                    console.log('DEBUG regex textContent:', textContent);
                }
                
                // Create combined layout with question text and graph side by side
                const combinedHtml = `
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;">
                        <div style="flex: 1; min-width: 250px;">
                            ${textContent}
                        </div>
                        <div class="graph-svg-container" style="flex: 0 1 auto;">
                            ${result.graphSvgWithRenderedLatex}
                        </div>
                    </div>
                `;
                fragments.push(PMFragmentGenerator.createParagraph(combinedHtml, ["py-2"]));
            } else {
                // Standard layout without graph
                fragments.push(PMFragmentGenerator.createParagraph(processedStatementHtml, ["py-"]));
            }
            
            // Answer fragment if available
            // if (result.success && result.answer) {
            //     fragments.push(PMFragmentGenerator.createParagraph(`**Réponse:** ${result.answer}`));
            // }
            
            // Divider between questions
            // fragments.push(PMFragmentGenerator.createDivider());
        });
    }
    
    return fragments;
}

function injectFragmentsIntoPM(fragments) {
    // Find PM's main content container
    const pmContainer = document.querySelector('.pm-container .max-w-\\[640px\\]');
    if (!pmContainer) {
        console.error('PM container not found');
        return;
    }
    
    // Inject first fragment (header) first
    if (fragments.length > 0) {
        const headerFragment = PMFragmentRenderer.renderFragment(fragments[0]);
        pmContainer.appendChild(headerFragment);
        
        // Add print button and TOC after the header
        addPrintButton(pmContainer);
        
        // Inject remaining fragments
        fragments.slice(1).forEach(fragment => {
            const renderedFragment = PMFragmentRenderer.renderFragment(fragment);
            pmContainer.appendChild(renderedFragment);
        });
    } else {
        // Fallback: add print button at the beginning if no fragments
        addPrintButton(pmContainer);
    }
    
    console.log(`✅ Injected ${fragments.length} fragments into PM system`);
}

// Main initialization and execution
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎯 Sujets0 Question Generator starting...');
    
    // Force Bolt theme for exercise generation and show toast if needed
    const currentTheme = document.documentElement.getAttribute('data-theme');
    if (currentTheme !== 'bolt') {
        // Set theme to 'bolt'
        document.documentElement.setAttribute('data-theme', 'bolt');
        localStorage.setItem('theme', 'bolt');
        
        // Show toast notification
        setTimeout(() => {
            showToast('⚡ Le thème Bolt est obligatoire pour l\'impression des exercices', 'info');
        }, 500);
        
        console.log('🎨 Thème forcé à Bolt pour la génération d\'exercices');
    }
    
    // Set up mutation observer to keep theme as 'bolt' during exercise generation
    const observeTheme = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.attributeName === 'data-theme') {
                const newTheme = document.documentElement.getAttribute('data-theme');
                if (newTheme !== 'bolt') {
                    document.documentElement.setAttribute('data-theme', 'bolt');
                    localStorage.setItem('theme', 'bolt');
                    showToast('⚡ Le thème Bolt doit rester activé pour l\'impression des exercices', 'warning');
                    console.log('🎨 Thème forcé à Bolt pour maintenir la génération d\'exercices');
                }
            }
        });
    });
    
    // Start observing theme changes
    observeTheme.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme']
    });
    
    // Find target container (look for existing table or create after current script)
    let targetContainer = document.querySelector('[data-f_type="table_"]');
    if (!targetContainer) {
        // Fallback: insert after the script module fragment
        const scriptFragment = document.querySelector('[data-f_type="script_module_"]');
        if (scriptFragment) {
            targetContainer = scriptFragment;
        } else {
            targetContainer = document.body;
        }
    }
    
    // Show loading indicator
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'sujets0-loading mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200';
    loadingDiv.innerHTML = `
        <div class="flex items-center space-x-3">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <div class="text-blue-800 font-medium">Chargement du générateur de questions...</div>
        </div>
        <div id="loading-progress" class="mt-2 text-sm text-blue-600"></div>
    `;
    
    targetContainer.insertAdjacentElement('afterend', loadingDiv);
    STATE.ui.container = loadingDiv;
    
    const progressEl = loadingDiv.querySelector('#loading-progress');
    
    try {
        // Add screen styles for details/summary animation
        addScreenStyles();
        
        // Initialize core components
        progressEl.textContent = '📦 Chargement de Nagini...';
        const naginiReady = await loadNagini();
        
        if (!naginiReady) {
            throw new Error('Failed to initialize Nagini');
        }
        
        progressEl.textContent = '📊 Chargement du générateur de graphiques...';
        const pcaReady = await loadPCAGraphLoader();
        if (!pcaReady) {
            console.warn('PCA Graph Loader failed to initialize - graphs will be skipped');
        }
        
        progressEl.textContent = '🚀 Génération des questions en cours...';
        
        // Generate questions
        const results = await executeAllGenerators();
        
        // Generate pure PM fragments
        const fragments = generateFragmentsFromResults(results);
        
        // Remove loading
        loadingDiv.remove();
        
        // Inject fragments into PM system
        injectFragmentsIntoPM(fragments);
        
        // Populate table of contents after fragments are rendered
        setTimeout(() => {
            populateTableOfContents();
        }, 50);
        
        // Fire unified LaTeX rendering for all content (static + dynamic)
        setTimeout(() => {
            console.log('🎯 Triggering unified LaTeX rendering for all content');
            document.dispatchEvent(new CustomEvent('render-math-now'));
        }, 100);
        
        // Add listener for native browser print (Ctrl+P)
        window.addEventListener('beforeprint', () => {
            const teacherDetails = document.querySelector('.teacher-answer-details');
            if (teacherDetails && !teacherDetails.open) {
                teacherDetails.open = true;
                teacherDetails.setAttribute('data-was-closed-for-print', 'true');
                console.log('🖨️ Auto-opened teacher details for native print');
            }
        });
        
        window.addEventListener('afterprint', () => {
            const teacherDetails = document.querySelector('.teacher-answer-details');
            if (teacherDetails && teacherDetails.getAttribute('data-was-closed-for-print')) {
                teacherDetails.open = false;
                teacherDetails.removeAttribute('data-was-closed-for-print');
                console.log('🖨️ Restored teacher details after native print');
            }
        });
        
        // Expose for debugging
        window.sujets0Results = results;
        window.sujets0State = STATE;
        
        console.log('🎉 Questions generated as PM fragments with processed SVGs!');
        
    } catch (error) {
        console.error('❌ Sujets0 Question Generator failed:', error);
        // Create error fragment
        const errorFragment = PMFragmentGenerator.createParagraph(`❌ Erreur: ${error.message}`);
        const errorElement = PMFragmentRenderer.renderFragment(errorFragment);
        loadingDiv.replaceWith(errorElement);
    }

});

console.log('📜 Sujets0 Question Generator script loaded and ready');

