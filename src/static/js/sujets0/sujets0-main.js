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
 * Extract all form values from the Arpege form
 * @returns {Object} Form data with validation and type conversion
 */
function extractFormValues() {
    const form = document.getElementById('arpege-form');
    if (!form) {
        throw new Error('Form not found');
    }
    
    // Extract number inputs
    const studentCount = parseInt(document.getElementById('nb-eleves')?.value || '30', 10);
    const questionCount = parseInt(document.getElementById('nb-questions')?.value || '12', 10);
    
    // Extract radio button values
    const programLevel = document.querySelector('input[name="options"]:checked')?.getAttribute('aria-label') || null;
    const specialization = document.querySelector('input[name="sujets0"]:checked')?.getAttribute('aria-label') || null;
    
    // Create structured form data object
    const formData = {
        // Student/Copy configuration
        copies: {
            count: studentCount,
            isValid: studentCount >= 1 && studentCount <= 50
        },
        
        // Question configuration
        questions: {
            perCopy: questionCount,
            isValid: questionCount >= 1 && questionCount <= 12
        },
        
        // Program level selection
        program: {
            level: programLevel, // "2nde" or "2nde & 1ère"
            includesFirstYear: programLevel === "2nde & 1ère",
            isValid: programLevel !== null
        },
        
        // Specialization selection
        track: {
            type: specialization, // "Spé." or "Non Spé." or "Techno"
            isSpeciality: specialization === "Spé.",
            isValid: specialization !== null && specialization !== "Techno"
        },
        
        // Global validation
        isComplete: false,
        errors: []
    };
    
    // Validate all fields
    validateFormData(formData);
    
    return formData;
}

/**
 * Validate form data and populate error messages
 * @param {Object} formData - The form data object to validate
 */
function validateFormData(formData) {
    const errors = [];
    
    // Validate student count
    if (!formData.copies.isValid) {
        errors.push({
            field: 'copies',
            message: 'Le nombre de copies doit être entre 1 et 50'
        });
    }
    
    // Validate question count
    if (!formData.questions.isValid) {
        errors.push({
            field: 'questions',
            message: 'Le nombre de questions doit être entre 1 et 12'
        });
    }
    
    // Validate program level selection
    if (!formData.program.isValid) {
        errors.push({
            field: 'program',
            message: 'Veuillez sélectionner un niveau de programme'
        });
    }
    
    // Validate track selection
    if (!formData.track.isValid) {
        if (formData.track.type === "Techno") {
            errors.push({
                field: 'track',
                message: 'La filière technologique n\'est pas encore disponible'
            });
        } else {
            errors.push({
                field: 'track',
                message: 'Veuillez sélectionner une filière'
            });
        }
    }
    
    formData.errors = errors;
    formData.isComplete = errors.length === 0;
}

/**
 * Get form configuration for generator execution
 * @returns {Object} Simplified configuration object for generators
 */
function getGeneratorConfig() {
    const formData = extractFormValues();
    
    if (!formData.isComplete) {
        console.error('Form validation errors:', formData.errors);
        return null;
    }
    
    return {
        nbStudents: formData.copies.count,
        nbQuestions: formData.questions.perCopy,
        programLevel: formData.program.includesFirstYear ? 'both' : 'seconde',
        track: formData.track.isSpeciality ? 'speciality' : 'common',
        // Additional config can be added here
        timestamp: Date.now(),
        sessionId: crypto.randomUUID?.() || Math.random().toString(36).substr(2, 9)
    };
}

/**
 * Execute all generators
 */
async function executeAllGenerators() {
    if (!Nagini || !naginiManager) {
        alert("Nagini not ready. Please wait a few seconds and try again.");
        return;
    }
    
    // Extract and validate form data
    const config = getGeneratorConfig();
    if (!config) {
        const formData = extractFormValues();
        const errorMessages = formData.errors.map(e => e.message).join('\n');
        alert(`Veuillez corriger les erreurs suivantes:\n${errorMessages}`);
        return;
    }
    
    console.log('Generator configuration:', config);
    
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.disabled = true;
        executeBtn.textContent = 'Génération...';
    }
    
    const testFiles = [
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
        'spe_sujet1_auto_12_question.py',
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
export { 
    executeAllGenerators,
    extractFormValues,
    validateFormData,
    getGeneratorConfig
};

// Make functions available globally for debugging
window.executeAllGenerators = executeAllGenerators;
window.extractFormValues = extractFormValues;
window.getGeneratorConfig = getGeneratorConfig;
