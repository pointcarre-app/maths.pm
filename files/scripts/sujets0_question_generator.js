/**
 * Sujets0 Question Generator - Comprehensive Script Module
 * Generates mathematics questions using Nagini Python execution engine
 * with KaTeX rendering and graph generation support
 */


// At the very top:
window.delayMathRendering = true;



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

// SVG KaTeX Processing (inspired by index-graphs.js)
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
        
        // Find all foreignObject elements
        const foreignObjects = svgElement.querySelectorAll('foreignObject');
        
        foreignObjects.forEach((fo) => {
            // Find div.svg-latex elements (exactly like index-graphs.js)
            const latexDivs = fo.querySelectorAll('div.svg-latex');
            
            
            latexDivs.forEach((div) => {
                div.classList.add('svg-latex');
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
        
        // Serialize back to string with processed KaTeX
        const serializer = new XMLSerializer();
        return serializer.serializeToString(svgElement);
    } catch (error) {
        console.error('SVG KaTeX processing failed:', error);
        return svgString; // Return original on error
    }
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
        return {
            f_type: { value: 'h2_' },
            html: content,
            data: { id_href: slug },
            class_list: classes,
            classes: classes.join(' '),
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
        return {
            f_type: { value: 'hr_' },
            html: '',
            data: {},
            class_list: classes,
            classes: classes.join(' ')
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
                fragmentDiv.innerHTML = fragment.html;
                break;
                
            case 'h2_':
                fragmentDiv.innerHTML = `<h2 id="${fragment.data.id_href || ''}">${fragment.html}</h2>`;
                break;
                
            case 'svg_':
                fragmentDiv.innerHTML = fragment.data.content;
                break;
                
            case 'hr_':
                fragmentDiv.innerHTML = '<hr>';
                break;
                
            default:
                fragmentDiv.innerHTML = fragment.html;
        }
        
        wrapper.appendChild(fragmentDiv);
        return wrapper;
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

// Pure PM Fragment Generation - No Custom UI
function generateFragmentsFromResults(results) {
    const fragments = [];
    
    // Header fragment
    fragments.push(PMFragmentGenerator.createH2('Questions générées'));
    
    // Group by student
    const byStudent = results.reduce((acc, r) => {
        const key = r && r.student != null ? String(r.student) : 'N/A';
        (acc[key] ||= []).push(r);
        return acc;
    }, {});
    
    for (const student of Object.keys(byStudent)) {
        // Student header if multiple students
        if (Object.keys(byStudent).length > 1) {
            fragments.push(PMFragmentGenerator.createH2(`Élève ${student}`));
        }
        
        byStudent[student].forEach((result) => {
            // Statement fragment using statementHtml
            const statementHtml = result.success ? 
                `${result.generatorNum}) ${result.statementHtml}` : 
                `${result.generatorNum}) Erreur de génération`;
            
            fragments.push(PMFragmentGenerator.createParagraph(statementHtml));
            
            // Answer fragment if available
            if (result.success && result.answer) {
                fragments.push(PMFragmentGenerator.createParagraph(`**Réponse:** ${result.answer}`));
            }
            
            // SVG fragment if available
            if (result.graphSvgWithRenderedLatex) {
                fragments.push(PMFragmentGenerator.createSvg(result.graphSvgWithRenderedLatex, result.graphDict));
            }
            
            // Divider between questions
            fragments.push(PMFragmentGenerator.createDivider());
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
    
    // Inject each fragment
    fragments.forEach(fragment => {
        const renderedFragment = PMFragmentRenderer.renderFragment(fragment);
        pmContainer.appendChild(renderedFragment);
    });
    
    console.log(`✅ Injected ${fragments.length} fragments into PM system`);
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
        
        // Fire unified LaTeX rendering for all content (static + dynamic)
        setTimeout(() => {
            console.log('🎯 Triggering unified LaTeX rendering for all content');
            document.dispatchEvent(new CustomEvent('render-math-now'));
        }, 100);
        
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

