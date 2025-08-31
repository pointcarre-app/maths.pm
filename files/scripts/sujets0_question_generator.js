/**
 * Sujets0 Question Generator - Comprehensive Script Module
 * Generates mathematics questions using Nagini Python execution engine
 * with KaTeX rendering and graph generation support
 */

console.log('🎯 Sujets0 Question Generator loading...');

// Configuration constants
const CONFIG = {
    teachersGitTag: 'v0.0.22',
    naginiGitTag: 'v0.0.21',
    v4PyJsGitTag: 'v0.0.27',
    rootSeed: 14,
    nbStudents: 2,
    nbQuestions: 12,
    
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
        STATE.pca.loaderInstance = new module.PCAGraphLoader();
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
        throw new Error('PCA Graph Loader not initialized');
    }
    
    try {
        const result = await STATE.pca.loaderInstance.loadGraph(graphKey, params);
        return {
            svg: result.svg,
            graphDict: result.graphDict
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
            const svgAndDict = await buildPCAGraph('q7_small', { Y_LABEL_FOR_HORIZONTAL_LINE });
            result.graphSvg = svgAndDict.svg;
            result.graphDict = svgAndDict.graphDict;
        } else if (generator === 'spe_sujet1_auto_08_question.py') {
            const A_FLOAT_FOR_AFFINE_LINE = parseFloat(result.data.components_evaluated.a);
            const B_FLOAT_FOR_AFFINE_LINE = parseFloat(result.data.components_evaluated.b);
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

// KaTeX rendering functions
async function prerenderLatexInSvg(svgString) {
    if (typeof katex === 'undefined') {
        return svgString;
    }
    
    try {
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
        const svgElement = svgDoc.querySelector('svg');
        if (!svgElement) return svgString;
        
        const foreignObjects = svgElement.querySelectorAll('foreignObject');
        let hasUnrenderedLatex = false;
        
        foreignObjects.forEach((fo) => {
            const divs = fo.querySelectorAll('div.svg-latex');
            divs.forEach((div) => {
                if (div.querySelector('.katex')) return;
                const latex = div.textContent.trim();
                if (!latex) return;
                hasUnrenderedLatex = true;
                try {
                    const bgColor = div.style.backgroundColor;
                    const color = div.style.color;
                    const rendered = katex.renderToString(latex, {
                        throwOnError: false,
                        displayMode: false
                    });
                    div.innerHTML = rendered;
                    if (bgColor) div.style.backgroundColor = bgColor;
                    if (color) {
                        const katexEls = div.querySelectorAll('.katex, .katex *');
                        katexEls.forEach((el) => {
                            el.style.color = color;
                        });
                    }
                } catch (e) {
                    // keep original
                }
            });
        });
        
        if (!hasUnrenderedLatex) return svgString;
        
        // Inject KaTeX fonts
        await injectKatexFont(svgElement);
        
        const serializer = new XMLSerializer();
        return serializer.serializeToString(svgElement);
    } catch (error) {
        return svgString;
    }
}

async function injectKatexFont(svgElement) {
    try {
        const KATEX_VERSION = '0.16.9';
        const KATEX_MATH_ITALIC_URL = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/fonts/KaTeX_Math-Italic.woff2`;
        
        if (!window._katexMathItalicDataUrl) {
            const resp = await fetch(KATEX_MATH_ITALIC_URL, { cache: 'force-cache' });
            if (resp.ok) {
                const buffer = await resp.arrayBuffer();
                const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
                window._katexMathItalicDataUrl = `data:font/woff2;base64,${base64}`;
            }
        }
        
        if (window._katexMathItalicDataUrl) {
            const css = `
@font-face {
  font-family: 'KaTeX_Math';
  font-style: italic;
  src: url('${window._katexMathItalicDataUrl}') format('woff2');
  font-display: swap;
}
.katex { font-family: 'KaTeX_Math', 'KaTeX_Main', serif; }
.katex * { font-family: inherit !important; }
.text-sm { font-size: 0.875rem !important; line-height: 1.25rem !important; }
.text-xs { font-size: 0.75rem !important; line-height: 1rem !important; }
.svg-latex .katex { font-size: inherit; }
`;
            
            const svgStyle = svgElement.ownerDocument.createElementNS('http://www.w3.org/2000/svg', 'style');
            svgStyle.textContent = css;
            svgElement.insertBefore(svgStyle, svgElement.firstChild);
        }
    } catch (error) {
        console.warn('Failed to inject KaTeX font:', error);
    }
}

// Main execution function
async function executeAllGenerators() {
    console.log('🚀 Starting question generation...');
    
    const selectedGenerators = CONFIG.generators.slice(0, CONFIG.nbQuestions);
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
                
                // Prerender LaTeX in SVGs
                if (result.graphSvg) {
                    result.graphSvgWithRenderedLatex = await prerenderLatexInSvg(result.graphSvg);
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

// UI rendering functions
function createResultsTable(results) {
    const container = document.createElement('div');
    container.className = 'sujets0-results-container mt-6 p-4 bg-white rounded-lg border';
    
    container.innerHTML = `
        <div class="mb-4">
            <h3 class="text-xl font-bold text-gray-800 mb-2">📋 Sujets 0 - Questions générées</h3>
            <div class="text-sm text-gray-600">
                <span class="font-medium">${results.length}</span> questions générées pour 
                <span class="font-medium">${CONFIG.nbStudents}</span> étudiants
            </div>
        </div>
        
        <div class="overflow-x-auto">
            <table class="min-w-full border-collapse border border-gray-300">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">Q#</th>
                        <th class="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">Étudiant</th>
                        <th class="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">Énoncé</th>
                        <th class="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">Réponse</th>
                        <th class="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">Graphique</th>
                        <th class="border border-gray-300 px-3 py-2 text-left text-sm font-medium text-gray-700">Statut</th>
                    </tr>
                </thead>
                <tbody id="results-tbody">
                </tbody>
            </table>
        </div>
        
        <div class="mt-4 text-xs text-gray-500">
            Générateur: Sujets0 Question Generator v1.0 | Seed racine: ${CONFIG.rootSeed}
        </div>
    `;
    
    const tbody = container.querySelector('#results-tbody');
    
    results.forEach((result, index) => {
        const row = document.createElement('tr');
        row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';
        
        const statusClass = result.success ? 'text-green-600' : 'text-red-600';
        const statusIcon = result.success ? '✅' : '❌';
        
        row.innerHTML = `
            <td class="border border-gray-300 px-3 py-2 text-sm font-mono">${result.generatorNum || '?'}</td>
            <td class="border border-gray-300 px-3 py-2 text-sm text-center">${result.student || '?'}</td>
            <td class="border border-gray-300 px-3 py-2 text-sm statement-cell" style="max-width: 300px;">
                <div class="statement-wrapper">
                    ${result.success ? (result.statement || 'N/A') : 'Erreur de génération'}
                </div>
            </td>
            <td class="border border-gray-300 px-3 py-2 text-sm answer-cell" style="max-width: 200px;">
                <div class="answer-wrapper">
                    ${result.success ? (result.answer || 'N/A') : '—'}
                </div>
            </td>
            <td class="border border-gray-300 px-3 py-2 text-sm text-center">
                ${result.graphSvg ? 
                    `<div class="graph-container" style="max-width: 150px; max-height: 150px; overflow: hidden;">
                        ${result.graphSvgWithRenderedLatex || result.graphSvg}
                    </div>` : 
                    '—'
                }
            </td>
            <td class="border border-gray-300 px-3 py-2 text-sm ${statusClass}">
                ${statusIcon} ${result.success ? 'OK' : 'Erreur'}
            </td>
        `;
        
        tbody.appendChild(row);
    });
    
    return container;
}

function renderKaTeX(container) {
    if (window.renderMathInElement) {
        try {
            window.renderMathInElement(container, {
                delimiters: [
                    { left: '$$', right: '$$', display: true },
                    { left: '$', right: '$', display: false },
                    { left: '\\(', right: '\\)', display: false },
                    { left: '\\[', right: '\\]', display: true }
                ],
                throwOnError: false
            });
        } catch (e) {
            console.error('KaTeX rendering failed:', e);
        }
    } else {
        // Retry after delay
        setTimeout(() => {
            if (window.renderMathInElement) {
                try {
                    window.renderMathInElement(container, {
                        delimiters: [
                            { left: '$$', right: '$$', display: true },
                            { left: '$', right: '$', display: false }
                        ],
                        throwOnError: false
                    });
                } catch (e) {
                    console.error('KaTeX rendering failed (delayed):', e);
                }
            }
        }, 500);
    }
}

// Main initialization and execution
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎯 Sujets0 Question Generator starting...');
    
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
        // Initialize core components
        progressEl.textContent = '📦 Chargement de Nagini...';
        const naginiReady = await loadNagini();
        
        if (!naginiReady) {
            throw new Error('Failed to initialize Nagini');
        }
        
        progressEl.textContent = '📊 Chargement du générateur de graphiques...';
        await loadPCAGraphLoader();
        
        progressEl.textContent = '🚀 Génération des questions en cours...';
        
        // Generate questions
        const results = await executeAllGenerators();
        
        // Create and render results table
        const resultsTable = createResultsTable(results);
        loadingDiv.replaceWith(resultsTable);
        
        // Render KaTeX in the results
        renderKaTeX(resultsTable);
        
        // Expose results globally for debugging
        window.sujets0Results = results;
        window.sujets0State = STATE;
        
        console.log('🎉 Sujets0 Question Generator completed successfully!');
        console.log(`Generated ${results.length} questions:`, results);
        
    } catch (error) {
        console.error('❌ Sujets0 Question Generator failed:', error);
        loadingDiv.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <div class="flex items-center space-x-2 text-red-800 font-medium mb-2">
                    <span>❌</span>
                    <span>Erreur lors de la génération des questions</span>
                </div>
                <div class="text-sm text-red-600">${error.message}</div>
                <div class="mt-2 text-xs text-red-500">
                    Vérifiez la console pour plus de détails.
                </div>
            </div>
        `;
    }
});

console.log('📜 Sujets0 Question Generator script loaded and ready');
