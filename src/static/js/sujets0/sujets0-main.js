/**
 * Sujets0 Main Module
 * Handles the main functionality for the Sujets0 application
 */

// Global state
let Nagini = null;
let naginiManager = null;
let backendSettings = null;

/**
 * Load backend settings from data attributes
 * @returns {Object|null} Backend settings object or null if not found
 */
function loadBackendSettings() {
    const settingsElement = document.getElementById('products-settings');
    if (!settingsElement) {
        console.warn('Products settings element not found');
        return null;
    }
    
    // Try to get data-sujets0 attribute
    const sujets0Data = settingsElement.getAttribute('data-sujets0');
    if (!sujets0Data) {
        console.warn('data-sujets0 attribute not found');
        return null;
    }
    
    try {
        // Parse the JSON data (handles HTML entities automatically)
        const settings = JSON.parse(sujets0Data);
        console.log('✅ Backend settings loaded successfully:', settings);
        
        // Log individual components for clarity
        if (settings.nagini) {
            console.log('📦 Nagini Configuration:', {
                endpoint: settings.nagini.endpoint,
                js_url: settings.nagini.js_url,
                pyodide_worker_url: settings.nagini.pyodide_worker_url
            });
        }
        
        return settings;
    } catch (error) {
        console.error('Failed to parse backend settings:', error);
        return null;
    }
}

/**
 * Get all product settings from data attributes
 * @returns {Object} Object containing all parsed data attributes
 */
function getAllProductSettings() {
    const settingsElement = document.getElementById('products-settings');
    if (!settingsElement) {
        console.warn('Products settings element not found');
        return {};
    }
    
    const settings = {};
    
    // Get all data attributes
    const dataAttributes = settingsElement.dataset;
    
    // Parse each data attribute
    for (const [key, value] of Object.entries(dataAttributes)) {
        try {
            settings[key] = JSON.parse(value);
            console.log(`✅ Parsed data-${key}:`, settings[key]);
        } catch (error) {
            console.warn(`Failed to parse data-${key}:`, error);
            settings[key] = value; // Store as string if parsing fails
        }
    }
    
    return settings;
}

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
        // Load backend settings first
        backendSettings = loadBackendSettings();
        
        // Determine which URLs to use (from settings or fallback to defaults)
        let naginiJsUrl = 'https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js?bundle';
        let pyodideWorkerUrl = 'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js';
        
        if (backendSettings?.nagini) {
            // Use settings from data attribute
            naginiJsUrl = backendSettings.nagini.js_url + '?bundle';
            pyodideWorkerUrl = backendSettings.nagini.pyodide_worker_url;
            console.log('🔧 Using Nagini URLs from backend settings');
        } else {
            console.log('⚠️ Using default Nagini URLs (settings not found)');
        }
        
        console.log('📥 Loading Nagini from:', naginiJsUrl);
        
        // Load Nagini
        const naginiModule = await import(naginiJsUrl);
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
        
        console.log('🔨 Creating Nagini manager with worker:', pyodideWorkerUrl);
        
        // Create manager with packages and teachers module
        naginiManager = await Nagini.createManager(
            'pyodide',
            ['sympy', 'pydantic', 'strictyaml'],
            [],//['antlr4-python3-runtime'],
            teachersFiles,
            pyodideWorkerUrl
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
    
    // Apply visual validation feedback
    applyFormValidationStyles(formData);
    
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
 * Apply visual validation styles to form fields
 * @param {Object} formData - The validated form data
 */
function applyFormValidationStyles(formData) {
    // Reset all error styles first
    document.getElementById('nb-eleves')?.classList.remove('input-error');
    document.getElementById('nb-questions')?.classList.remove('input-error');
    document.querySelectorAll('input[name="options"]').forEach(el => 
        el.closest('.join')?.classList.remove('ring-2', 'ring-error')
    );
    document.querySelectorAll('input[name="sujets0"]').forEach(el => 
        el.closest('.join')?.classList.remove('ring-2', 'ring-error')
    );
    
    // Apply error styles based on validation
    if (!formData.copies.isValid) {
        document.getElementById('nb-eleves')?.classList.add('input-error');
    }
    
    if (!formData.questions.isValid) {
        document.getElementById('nb-questions')?.classList.add('input-error');
    }
    
    if (!formData.program.isValid) {
        document.querySelector('input[name="options"]')?.closest('.join')?.classList.add('ring-2', 'ring-error');
    }
    
    if (!formData.track.isValid) {
        document.querySelector('input[name="sujets0"]')?.closest('.join')?.classList.add('ring-2', 'ring-error');
    }
}

/**
 * Display validation status in a table
 * @param {Object} formData - The form data with validation results
 */
function displayValidationTable(formData) {
    // Find or create validation container
    let validationContainer = document.getElementById('validation-status-container');
    if (!validationContainer) {
        // Insert after "Génération d'exercices" heading
        const targetElement = document.querySelector('#journal-content .text-base.mt-4.mb-2');
        if (targetElement) {
            validationContainer = document.createElement('div');
            validationContainer.id = 'validation-status-container';
            validationContainer.className = 'mt-4';
            targetElement.parentNode.insertBefore(validationContainer, targetElement.nextSibling);
        }
    }
    
    if (!validationContainer) return;
    
    // Build status table HTML
    const timestamp = new Date().toLocaleTimeString('fr-FR');
    const statusRows = [
        {
            field: 'Nombre de copies',
            value: formData.copies.count,
            status: formData.copies.isValid,
            error: formData.errors.find(e => e.field === 'copies')?.message
        },
        {
            field: 'Questions par copie',
            value: formData.questions.perCopy,
            status: formData.questions.isValid,
            error: formData.errors.find(e => e.field === 'questions')?.message
        },
        {
            field: 'Programme',
            value: formData.program.level || 'Non sélectionné',
            status: formData.program.isValid,
            error: formData.errors.find(e => e.field === 'program')?.message
        },
        {
            field: 'Filière',
            value: formData.track.type || 'Non sélectionnée',
            status: formData.track.isValid,
            error: formData.errors.find(e => e.field === 'track')?.message
        }
    ];
    
    const tableHtml = `
        <div class="overflow-x-auto">
            <table class="table table-sm w-full" style="border-radius:var(--radius-box); border: 1px solid var(--color-base-content);">
                <thead>
                    <tr>
                        <th colspan="3" class="text-left bg-base-200 font-mono">
                            Tentative de génération - ${timestamp}
                        </th>
                    </tr>
                    <tr>
                        <th>Paramètre</th>
                        <th>Valeur</th>
                        <th>Statut</th>
                    </tr>
                </thead>
                <tbody>
                    ${statusRows.map(row => `
                        <tr class="${!row.status ? 'bg-error/10' : ''}">
                            <td>${row.field}</td>
                            <td>${row.value}</td>
                            <td>
                                ${row.status 
                                    ? '<span class="badge badge-success badge-sm">✓</span>' 
                                    : `<span class="text-error text-sm">${row.error || 'Invalide'}</span>`
                                }
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
                <tfoot>
                    <tr>
                        <th colspan="3" class="text-center ${formData.isComplete ? 'bg-success/20' : 'bg-error/20'}">
                            ${formData.isComplete 
                                ? '✓ Formulaire valide - Génération en cours...' 
                                : '✗ Veuillez corriger les erreurs ci-dessus'
                            }
                        </th>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    validationContainer.innerHTML = tableHtml;

    
}

/**
 * Get form configuration for generator execution
 * @returns {Object} Simplified configuration object for generators
 */
function getGeneratorConfig() {
    const formData = extractFormValues();
    
    // Display validation table
    displayValidationTable(formData);
    
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
 * Global state for generation results
 */
let generationResults = {
    students: [],
    selectedGenerators: [],
    currentStudentIndex: 0,
    config: null
};

/**
 * Randomly select N items from an array
 * @param {Array} array - Source array
 * @param {number} n - Number of items to select
 * @returns {Array} Selected items
 */
function selectRandomItems(array, n) {
    const shuffled = [...array].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
}

/**
 * Execute a generator with a specific seed
 * @param {string} filename - Generator filename
 * @param {number} seed - Random seed
 * @returns {Object} Execution result
 */
async function executeGeneratorWithSeed(filename, seed) {
    const url = `/static/sujets0/generators/${filename}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
        
        let pythonCode = await response.text();
        
        // Inject seed and replace generate_components call
        // We need to pass the seed to generate_components function
        const seedInjection = `
import random
random.seed(${seed})

# Override the default SEED
import teachers.defaults
teachers.defaults.SEED = ${seed}

`;
        
        // Replace generate_components(None) with generate_components(None, seed)
        pythonCode = pythonCode.replace(
            'components = generate_components(None)',
            `components = generate_components(None, ${seed})`
        );
        
        pythonCode = seedInjection + pythonCode;
        
        const result = await naginiManager.executeAsync(filename, pythonCode);
        
        const success = !result.error && (result.exit_code === 0 || result.missive);
        
        if (result.missive && success) {
            try {
                const data = JSON.parse(result.missive);
                return {
                    success: true,
                    statement: data.statement || data.question,
                    answer: data.answer?.simplified_latex || data.answer?.latex || 
                           data.answer?.simplified_answer || data.answer,
                    data: data
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

/**
 * Generate pagination buttons with ellipsis for large numbers
 * @param {number} current - Current page index (0-based)
 * @param {number} total - Total number of pages
 * @returns {string} HTML string for pagination buttons
 */
function generatePaginationButtons(current, total) {
    const currentPage = current + 1; // Convert to 1-based for display
    let buttons = '';
    
    // For small number of pages, show all
    if (total <= 10) {
        for (let i = 1; i <= total; i++) {
            buttons += `
                <button class="join-item btn btn-sm ${i === currentPage ? 'btn-active' : ''}"
                        onclick="navigateToStudent(${i - 1})">
                    ${i}
                </button>
            `;
        }
    } else {
        // For larger numbers, use ellipsis
        const range = 2; // Numbers to show around current
        const showStart = currentPage <= range + 2;
        const showEnd = currentPage >= total - range - 1;
        
        // Always show first page
        buttons += `
            <button class="join-item btn btn-sm ${currentPage === 1 ? 'btn-active' : ''}"
                    onclick="navigateToStudent(0)">
                1
            </button>
        `;
        
        // Show ellipsis or numbers near start
        if (currentPage > range + 2) {
            buttons += `<button class="join-item btn btn-sm btn-disabled">...</button>`;
        }
        
        // Show pages around current
        for (let i = Math.max(2, currentPage - range); 
             i <= Math.min(total - 1, currentPage + range); 
             i++) {
            buttons += `
                <button class="join-item btn btn-sm ${i === currentPage ? 'btn-active' : ''}"
                        onclick="navigateToStudent(${i - 1})">
                    ${i}
                </button>
            `;
        }
        
        // Show ellipsis or numbers near end
        if (currentPage < total - range - 1) {
            buttons += `<button class="join-item btn btn-sm btn-disabled">...</button>`;
        }
        
        // Always show last page
        if (total > 1) {
            buttons += `
                <button class="join-item btn btn-sm ${currentPage === total ? 'btn-active' : ''}"
                        onclick="navigateToStudent(${total - 1})">
                    ${total}
                </button>
            `;
        }
    }
    
    return buttons;
}

/**
 * Navigate directly to a specific student
 * @param {number} studentIndex - Index of student to navigate to (0-based)
 */
function navigateToStudent(studentIndex) {
    if (studentIndex >= 0 && studentIndex < generationResults.students.length) {
        generationResults.currentStudentIndex = studentIndex;
        displayStudentResults(studentIndex);
    }
}

/**
 * Display results for a specific student with pagination
 * @param {number} studentIndex - Index of student to display
 */
function displayStudentResults(studentIndex) {
    const container = document.getElementById('generator-results-container');
    if (!container || !generationResults.students.length) return;
    
    const student = generationResults.students[studentIndex];
    const totalStudents = generationResults.students.length;
    
    // Build HTML for student results
    let html = `
        <div class="mb-6">
            <!-- Pagination Header -->
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold">Copie ${studentIndex + 1} sur ${totalStudents}</h3>
                
                <!-- Pagination Controls -->
                <div class="join">
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(-1)"
                            ${studentIndex === 0 ? 'disabled' : ''}>
                        «
                    </button>
                    <button class="join-item btn btn-sm btn-active">
                        ${studentIndex + 1} / ${totalStudents}
                    </button>
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(1)"
                            ${studentIndex === totalStudents - 1 ? 'disabled' : ''}>
                        »
                    </button>
                </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="w-full bg-base-200 rounded-full h-2 mb-4">
                <div class="bg-primary h-2 rounded-full transition-all duration-300" 
                     style="width: ${((studentIndex + 1) / totalStudents) * 100}%"></div>
            </div>
            
            <!-- Questions Grid -->
            <div class="grid gap-4">
    `;
    
    // Add each question
    student.questions.forEach((question, qIndex) => {
        const bgColor = question.success ? 'bg-base-100' : 'bg-error/10';
        const borderColor = question.success ? 'border-primary' : 'border-error';
        
        html += `
            <div class="card ${bgColor} border ${borderColor} shadow-sm">
                <div class="card-body">
                    <div class="flex justify-between items-start mb-2">
                        <h4 class="font-semibold text-sm">
                            Question ${qIndex + 1}
                            <span class="text-xs text-base-content/60 ml-2">
                                (${question.generator})
                            </span>
                        </h4>
                        ${question.success 
                            ? '<span class="badge badge-success badge-sm">✓</span>'
                            : '<span class="badge badge-error badge-sm">✗</span>'
                        }
                    </div>
                    
                    ${question.success ? `
                        <div class="space-y-2">
                            <div class="text-sm">
                                <strong>Énoncé:</strong>
                                <div class="mt-1">${question.statement || 'Pas d\'énoncé'}</div>
                            </div>
                            ${question.answer ? `
                                <div class="text-sm">
                                    <strong>Réponse:</strong>
                                    <span class="font-mono ml-2">$${question.answer}$</span>
                                </div>
                            ` : ''}
                        </div>
                    ` : `
                        <div class="text-sm text-error">
                            Erreur: ${question.error}
                        </div>
                    `}
                </div>
            </div>
        `;
    });
    
    html += `
            </div>
            
            <!-- Summary Stats -->
            <div class="stats shadow mt-6">
                <div class="stat">
                    <div class="stat-title">Questions réussies</div>
                    <div class="stat-value text-success">
                        ${student.questions.filter(q => q.success).length}
                    </div>
                    <div class="stat-desc">
                        sur ${student.questions.length} questions
                    </div>
                </div>
                
                <div class="stat">
                    <div class="stat-title">Seed utilisé</div>
                    <div class="stat-value text-primary">
                        ${student.seed}
                    </div>
                    <div class="stat-desc">
                        Identifiant unique de la copie
                    </div>
                </div>
            </div>
            
            <!-- Full Pagination at Bottom -->
            <div class="flex justify-center mt-6">
                <div class="join">
                    <!-- Previous Button -->
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(-1)"
                            ${studentIndex === 0 ? 'disabled' : ''}>
                        «
                    </button>
                    
                    <!-- Page Numbers -->
                    ${generatePaginationButtons(studentIndex, totalStudents)}
                    
                    <!-- Next Button -->
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(1)"
                            ${studentIndex === totalStudents - 1 ? 'disabled' : ''}>
                        »
                    </button>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Render LaTeX with KaTeX
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(container, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
        });
    }
}

/**
 * Navigate between students
 * @param {number} direction - -1 for previous, 1 for next
 */
function navigateStudent(direction) {
    const newIndex = generationResults.currentStudentIndex + direction;
    if (newIndex >= 0 && newIndex < generationResults.students.length) {
        generationResults.currentStudentIndex = newIndex;
        displayStudentResults(newIndex);
    }
}

/**
 * Execute all generators with pagination
 */
async function executeAllGenerators() {
    if (!Nagini || !naginiManager) {
        // Display error in validation table
        const errorData = {
            copies: { count: '-', isValid: false },
            questions: { perCopy: '-', isValid: false },
            program: { level: null, isValid: false },
            track: { type: null, isValid: false },
            isComplete: false,
            errors: [{ field: 'system', message: 'Nagini n\'est pas prêt. Veuillez patienter quelques secondes.' }]
        };
        displayValidationTable(errorData);
        return;
    }
    
    // Extract and validate form data (this will display the validation table)
    const config = getGeneratorConfig();
    if (!config) {
        // Validation table already displayed by getGeneratorConfig
        return;
    }
    
    console.log('Generator configuration:', config);
    generationResults.config = config;
    
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.disabled = true;
        executeBtn.textContent = 'Génération en cours...';
    }
    
    const allGenerators = [
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
    
    // Randomly select generators based on question count
    const selectedGenerators = selectRandomItems(allGenerators, config.nbQuestions);
    generationResults.selectedGenerators = selectedGenerators;
    
    console.log(`Selected ${config.nbQuestions} generators:`, selectedGenerators);
    
    // Reset results
    generationResults.students = [];
    generationResults.currentStudentIndex = 0;
    
    // Get or create results container in the wrapper area
    let resultsContainer = document.getElementById('generator-results-container');
    const wrapper = document.getElementById('generator-results-wrapper');
    
    if (!resultsContainer) {
        resultsContainer = document.createElement('div');
        resultsContainer.id = 'generator-results-container';
        
        // Place it in the wrapper that's below the journal
        if (wrapper) {
            wrapper.appendChild(resultsContainer);
        } else {
            // Fallback to after validation container if wrapper not found
            const validationContainer = document.getElementById('validation-status-container');
            if (validationContainer && validationContainer.parentNode) {
                validationContainer.parentNode.appendChild(resultsContainer);
            }
        }
    }
    
    resultsContainer.className = 'mt-6';
    resultsContainer.innerHTML = `
        <div class="alert alert-info">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>Génération de ${config.nbStudents} copies avec ${config.nbQuestions} questions chacune...</span>
        </div>
        <progress class="progress progress-primary w-full mt-4" value="0" max="${config.nbStudents}"></progress>
    `;
    
    // Process each student
    for (let studentNum = 1; studentNum <= config.nbStudents; studentNum++) {
        const seed = studentNum; // Use student number as seed
        const studentQuestions = [];
        
        // Update progress
        const progressBar = resultsContainer.querySelector('progress');
        if (progressBar) {
            progressBar.value = studentNum - 1;
        }
        
        // Execute each selected generator for this student
        for (const generator of selectedGenerators) {
            const result = await executeGeneratorWithSeed(generator, seed);
            studentQuestions.push({
                generator: generator.replace('.py', ''),
                ...result
            });
        }
        
        // Store student results
        generationResults.students.push({
            id: studentNum,
            seed: seed,
            questions: studentQuestions
        });
    }
    
    // Display first student's results
    displayStudentResults(0);
    
    // Re-enable button
    if (executeBtn) {
        executeBtn.disabled = false;
        executeBtn.textContent = 'Générer';
    }
}

// Make navigation functions available globally
window.navigateStudent = navigateStudent;
window.navigateToStudent = navigateToStudent;

/**
 * Initialize the module
 */
export async function init() {
    console.log('🚀 Initializing Sujets0 Module');
    
    // Log all available settings on initialization
    console.group('📋 Available Product Settings');
    const allSettings = getAllProductSettings();
    console.log('All settings loaded:', Object.keys(allSettings));
    console.groupEnd();
    
    // Initialize tabs
    initializeTabs();
    
    // Load Nagini and initialize
    await loadNaginiAndInitialize();
    
    console.log('✨ Sujets0 Module initialized successfully');
}

// Export functions for global access if needed
export { 
    executeAllGenerators,
    extractFormValues,
    validateFormData,
    getGeneratorConfig,
    loadBackendSettings,
    getAllProductSettings,
    applyFormValidationStyles,
    displayValidationTable,
    selectRandomItems,
    executeGeneratorWithSeed,
    displayStudentResults,
    navigateStudent,
    navigateToStudent,
    generatePaginationButtons
};

// Make functions available globally for debugging
window.executeAllGenerators = executeAllGenerators;
window.extractFormValues = extractFormValues;
window.getGeneratorConfig = getGeneratorConfig;
window.loadBackendSettings = loadBackendSettings;
window.getAllProductSettings = getAllProductSettings;
window.getBackendSettings = () => backendSettings; // Getter for current settings
window.applyFormValidationStyles = applyFormValidationStyles;
window.displayValidationTable = displayValidationTable;
window.generationResults = generationResults; // Expose results for debugging
window.displayStudentResults = displayStudentResults;
