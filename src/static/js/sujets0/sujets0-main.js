/**
 * Sujets0 Main Module
 * Handles the main functionality for the Sujets0 application
 */

// Global state
let Nagini = null;
let naginiManager = null;

/**
 * Initialize tab switching functionality
 */
function initializeTabs() {
    const tabButtons = document.querySelectorAll('[data-tab]');
    const tabContents = document.querySelectorAll('.tab-alt-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update button states
            tabButtons.forEach(btn => btn.classList.remove('btn-active'));
            this.classList.add('btn-active');
            
            // Update content visibility
            const tabName = this.getAttribute('data-tab');
            tabContents.forEach(content => content.classList.add('tab-alt-hidden'));
            
            const selectedContent = document.getElementById(tabName + '-content');
            if (selectedContent) {
                selectedContent.classList.remove('tab-alt-hidden');
            }
        });
    });
}

/**
 * Load Nagini and initialize manager
 */
async function loadNaginiAndInitialize() {
    try {
        // Load Nagini
        const naginiModule = await import('https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js?bundle');
        Nagini = naginiModule.Nagini;
        window.Nagini = Nagini;
        
        // Files for teachers module
        const teachersFiles = [
            { url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.20/src/teachers/__init__.py", path: "teachers/__init__.py" },
            { url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.20/src/teachers/generator.py", path: "teachers/generator.py" },
            { url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.20/src/teachers/maths.py", path: "teachers/maths.py" },
            { url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.20/src/teachers/formatting.py", path: "teachers/formatting.py" },
            { url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.20/src/teachers/corrector.py", path: "teachers/corrector.py" },
            { url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.20/src/teachers/defaults.py", path: "teachers/defaults.py" }
        ];
        
        // Create manager with packages and teachers module
        naginiManager = await Nagini.createManager(
            'pyodide',
            ['sympy', 'pydantic', 'strictyaml'],
            ['antlr4-python3-runtime'],
            teachersFiles,
            'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js'
        );
        
        await Nagini.waitForReady(naginiManager);
        
        displayIndicatorNaginiIsReady();
        enableExecuteButton();
        
        return true;
    } catch (error) {
        console.error('Failed to initialize Nagini:', error);
        showNaginiError();
        return false;
    }
}

/**
 * Show error message if Nagini fails to load
 */
function showNaginiError() {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error mt-4';
    errorDiv.innerHTML = `
        <strong>⚠️ Nagini Loading Error</strong><br />
        Failed to load Python engine. Please refresh the page.
    `;
    document.querySelector('.padding-alt-security')?.appendChild(errorDiv);
}

/**
 * Update Nagini status indicator
 */
function displayIndicatorNaginiIsReady() {
    const naginiDot = document.getElementById("nagini-dot");
    if (naginiDot) {
        naginiDot.classList.replace("badge-warning", "badge-success");
    }
    const naginiLabel = document.getElementById("nagini-label");
    if (naginiLabel) {
        naginiLabel.textContent = "Nagini ready";
    }
}

/**
 * Enable the execute button
 */
function enableExecuteButton() {
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.disabled = false;
        executeBtn.classList.remove('btn-disabled');
        executeBtn.onclick = executeAllGenerators;
    }
}

/**
 * Execute all generators
 */
async function executeAllGenerators() {
    if (!Nagini || !naginiManager) {
        alert("Nagini not ready. Please wait a few seconds and try again.");
        return;
    }
    
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.disabled = true;
        executeBtn.textContent = 'Génération...';
    }
    
    const testFiles = [
        'spe_sujet1_auto_01_question.py',
        'spe_sujet1_auto_02_question.py',
        'spe_sujet1_auto_03_question.py'
    ];
    
    let successCount = 0;
    let failureCount = 0;
    
    // Get or create results container
    let resultsContainer = document.getElementById('generator-results-container');
    if (!resultsContainer) {
        resultsContainer = document.createElement('div');
        resultsContainer.id = 'generator-results-container';
        document.querySelector('.padding-alt-security')?.appendChild(resultsContainer);
    }
    
    resultsContainer.className = 'mt-6';
    resultsContainer.innerHTML = '<div class="text-sm text-gray-600 mb-4">Questions générées:</div>';
    
    // Process each file
    for (const filename of testFiles) {
        const url = `/static/sujets0/generators/${filename}`;
        
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
            
            const pythonCode = await response.text();
            const result = await naginiManager.executeAsync(filename, pythonCode);
            
            const success = !result.error && (result.exit_code === 0 || result.missive);
            if (success) successCount++; else failureCount++;
            
            const div = document.createElement('div');
            div.className = `p-3 mb-4 border-l-4 ${success ? 'border-green-500 bg-base-100' : 'border-red-500 bg-red-50'}`;
            
            let outputHtml = `<div class="text-xs text-gray-500 mb-1">${filename}</div>`;
            
            if (result.missive && success) {
                try {
                    const data = JSON.parse(result.missive);
                    const statement = data.statement || data.question;
                    if (statement) {
                        outputHtml += `<div class="font-medium mb-2">${statement}</div>`;
                        if (data.answer) {
                            const answer = data.answer.simplified_latex || data.answer.latex || 
                                          data.answer.simplified_answer || data.answer;
                            outputHtml += `<div class="text-sm text-gray-600">Réponse: <span class="font-mono">${answer}</span></div>`;
                        }
                    }
                } catch (e) {
                    outputHtml += `<div class="text-sm text-gray-600">Output available</div>`;
                }
            } else if (!success) {
                outputHtml += `<div class="text-sm text-red-600">Execution failed</div>`;
            }
            
            div.innerHTML = outputHtml;
            resultsContainer.appendChild(div);
            
        } catch (error) {
            failureCount++;
            const div = document.createElement('div');
            div.className = 'p-3 mb-4 border-l-4 border-orange-500 bg-orange-50';
            div.innerHTML = `
                <div class="text-xs text-gray-500 mb-1">${filename}</div>
                <div class="text-sm text-orange-700">Error: ${error.message}</div>
            `;
            resultsContainer.appendChild(div);
        }
    }
    
    // Add summary
    const summaryDiv = document.createElement('div');
    summaryDiv.className = 'mt-4 pt-4 border-t text-sm text-gray-600';
    summaryDiv.innerHTML = `${successCount} réussi(s), ${failureCount} échoué(s)`;
    resultsContainer.appendChild(summaryDiv);
    
    // Re-enable button
    if (executeBtn) {
        executeBtn.disabled = false;
        executeBtn.textContent = 'Générer';
    }
}

/**
 * Initialize the module
 */
export async function init() {
    // Initialize tabs
    initializeTabs();
    
    // Load Nagini and initialize
    await loadNaginiAndInitialize();
}

// Export functions for global access if needed
export { executeAllGenerators };

// Make executeAllGenerators available globally for debugging
window.executeAllGenerators = executeAllGenerators;
