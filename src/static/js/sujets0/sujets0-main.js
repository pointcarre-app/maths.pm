/**
 * Sujets0 Main Module
 * Handles the main functionality for the Sujets0 application
 */

// Global state
let Nagini = null;
let naginiManager = null;
let generatedQuestions = [];

/**
 * Initialize tab switching functionality
 */
function initializeTabs() {
    console.log('Initializing tabs...');
    
    const tabButtons = document.querySelectorAll('[data-tab]');
    const tabContents = document.querySelectorAll('.tab-alt-content');
    
    console.log('Found buttons:', tabButtons.length);
    console.log('Found content areas:', tabContents.length);
    
    // Add click event listeners to all buttons
    tabButtons.forEach(button => {
        console.log('Adding listener to button:', button.getAttribute('data-tab'));
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Button clicked:', this.getAttribute('data-tab'));
            
            // Remove active class from all buttons
            tabButtons.forEach(btn => {
                btn.classList.remove('btn-active');
            });
            
            // Add active class to clicked button
            this.classList.add('btn-active');
            
            // Get the tab name from data-tab attribute
            const tabName = this.getAttribute('data-tab');
            
            // Hide all tab contents
            tabContents.forEach(content => {
                content.classList.add('tab-alt-hidden');
            });
            
            // Show the selected tab content
            const selectedContent = document.getElementById(tabName + '-content');
            if (selectedContent) {
                selectedContent.classList.remove('tab-alt-hidden');
                console.log('Showing content:', selectedContent.id);
            }
        });
    });
}

/**
 * Load Nagini from CDN
 */
async function loadNagini() {
    console.log('⏳ Loading Nagini from esm.sh...');
    
    try {
        // Try loading with the standard approach
        const naginiModule = await import('https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js');
        Nagini = naginiModule.Nagini;
        
        if (Nagini) {
            window.Nagini = Nagini;
            console.log('✅ Nagini loaded successfully from esm.sh!');
            return true;
        }
    } catch (e) {
        console.error('Failed to load Nagini:', e.message);
        
        try {
            // Fallback with bundle parameter
            const naginiModule = await import('https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js?bundle');
            Nagini = naginiModule.Nagini;
            
            if (Nagini) {
                window.Nagini = Nagini;
                console.log('✅ Loaded with bundle parameter');
                return true;
            }
        } catch (fallbackError) {
            console.error('❌ Failed to load Nagini with fallback:', fallbackError);
            showNaginiError();
            return false;
        }
    }
    
    return false;
}

/**
 * Show error message if Nagini fails to load
 */
function showNaginiError() {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error mt-4';
    errorDiv.innerHTML = `
        <strong>⚠️ Nagini Loading Error</strong><br />
        Failed to load Python engine from CDN. Please refresh the page.
    `;
    document.querySelector('.padding-alt-security')?.appendChild(errorDiv);
}

/**
 * Test basic Nagini execution
 */
async function testNaginiExecution() {
    if (!Nagini) return false;
    
    try {
        console.log("🧪 Testing Python execution...");
        
        // Create manager with simple setup
        const manager = await Nagini.createManager(
            'pyodide',
            [], // No extra packages for now
            [],
            [],
            'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js'
        );
        
        await Nagini.waitForReady(manager);
        
        // Execute simple Python code
        const result = await manager.executeAsync('test.py', `
result = 42 * 2
print(f"The answer is {result}")
result
        `);
        
        console.log("✅ Python execution successful!");
        console.log("Output:", result.stdout);
        
        // Store the manager
        naginiManager = manager;
        
        return true;
    } catch (error) {
        console.error("❌ Test failed:", error);
        return false;
    }
}

/**
 * Load packages and teachers module
 */
async function loadPackagesAndTeachers() {
    if (!Nagini) return false;
    
    try {
        console.log("🧪 Loading packages and teachers module...");
        
        // Files to load for teachers module
        //const filesToLoad = [
            //{
                //url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.4/src/teachers/__init__.py",
                //path: "teachers/__init__.py",
            //},
            //{
                //url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.4/src/teachers/generator.py",
                //path: "teachers/generator.py",
            //},
            //{
                //url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.4/src/teachers/maths.py",
                //path: "teachers/maths.py",
            //},
            //{
                //url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.4/src/teachers/formatting.py",
                //path: "teachers/formatting.py",
            //},
            //{
                //url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.4/src/teachers/corrector.py",
                //path: "teachers/corrector.py",
            //},
            //{
                //url: "https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@0.0.4/src/teachers/defaults.py",
                //path: "teachers/defaults.py",
            //}
        //];


        const filesToLoad = [
            {
                url: "http://127.0.0.1:8001/src/teachers/__init__.py",
                path: "teachers/__init__.py",
            },
            {
                url: "http://127.0.0.1:8001/src/teachers/generator.py",
                path: "teachers/generator.py",
            },
            {
                url: "http://127.0.0.1:8001/src/teachers/maths.py",
                path: "teachers/maths.py",
            },
            {
                url: "http://127.0.0.1:8001/src/teachers/formatting.py",
                path: "teachers/formatting.py",
            },
            {
                url: "http://127.0.0.1:8001/src/teachers/corrector.py",
                path: "teachers/corrector.py",
            },
            {
                url: "http://127.0.0.1:8001/src/teachers/defaults.py",
                path: "teachers/defaults.py",
            }
        ];
        
        // Create a new manager with packages and teachers module
        const manager = await Nagini.createManager(
            'pyodide',
            ['sympy', 'pydantic', 'strictyaml'], // Regular packages
            ['antlr4-python3-runtime'], // Micropip packages  
            filesToLoad, // Teachers module files
            'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js'
        );
        
        await Nagini.waitForReady(manager);
        
        // Test sympy
        const result = await manager.executeAsync('sympy_test.py', `
import sympy as sp
x = sp.Symbol('x')
expr = x**2 + 2*x + 1
factored = sp.factor(expr)
print(f"Expression: {expr}")
print(f"Factored: {factored}")
        `);
        
        console.log("✅ Sympy test successful!");
        console.log("Output:", result.stdout);
        
        // Test if teachers module is available
        const teachersTest = await manager.executeAsync('teachers_test.py', `
import teachers
print("Teachers module loaded successfully!")
print("Available modules:", dir(teachers))
        `);
        
        if (teachersTest.exit_code === 0) {
            console.log("✅ Teachers module loaded!");
            console.log(teachersTest.stdout);
        } else {
            console.warn("⚠️ Teachers module test failed:", teachersTest.stderr);
        }
        
        // Update manager
        naginiManager = manager;
        
        console.log("📦 All packages and modules loaded successfully!");
        
        return true;
    } catch (error) {
        console.warn("⚠️ Package test failed (this is okay):", error.message);
        return false;
    }
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
 * Execute all generators
 */
async function executeAllGenerators() {
    console.log("🚀 executeAllGenerators called!");
    
    if (!Nagini || !naginiManager) {
        console.error("❌ Nagini or manager not ready");
        alert("Nagini not ready. Wait a few seconds and try again.");
        return;
    }
    
    console.log("✅ Nagini and manager are ready, proceeding...");
    
    // Disable button
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.disabled = true;
        executeBtn.textContent = 'Génération...';
    }
    
    console.log("🚀 Starting generator execution...");
    
    // Only test actual generator files, not test files
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
    
    // Simple results display
    resultsContainer.className = 'mt-6';
    resultsContainer.innerHTML = `
        <div class="text-sm text-gray-600 mb-4">Questions générées:</div>
    `;
    
    // Process each file
    for (const filename of testFiles) {
        console.log(`\n🔄 Executing ${filename}...`);
        
        const url = `/static/sujets0/generators/${filename}`;
        
        try {
            // Fetch the file
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Failed to fetch: ${response.status}`);
            }
            const pythonCode = await response.text();
            console.log(`Fetched ${filename}, size: ${pythonCode.length} chars`);
            
            // Execute with Nagini
            const result = await naginiManager.executeAsync(filename, pythonCode);
            console.log(`Result for ${filename}:`, result);
            
            // Display result with enhanced formatting for missive data
            const div = document.createElement('div');
            // Consider it successful if there's no error and either exit_code is 0 or there's a missive
            const success = !result.error && (result.exit_code === 0 || result.missive);
            
            if (success) {
                successCount++;
            } else {
                failureCount++;
            }
            
            div.className = `p-3 mb-4 border-l-4 ${success ? 'border-green-500 bg-base-100' : 'border-red-500 bg-red-50'}`;
            
            let outputHtml = '';
            
            // Simple filename display
            outputHtml += `<div class="text-xs text-gray-500 mb-1">${filename}</div>`;
            
            // If there's a missive with question data, display it minimally
            if (result.missive && success) {
                try {
                    const missiveData = JSON.parse(result.missive);
                    if (missiveData.statement || missiveData.question) {
                        // Question statement
                        outputHtml += `<div class="font-medium mb-2">${missiveData.statement || missiveData.question}</div>`;
                        
                        // Answer in a subtle way
                        if (missiveData.answer) {
                            const answerDisplay = missiveData.answer.simplified_latex ||
                                missiveData.answer.latex ||
                                missiveData.answer.simplified_answer ||
                                missiveData.answer;
                            outputHtml += `<div class="text-sm text-gray-600">Réponse: <span class="font-mono">${answerDisplay}</span></div>`;
                        }
                    }
                } catch (e) {
                    // Fallback for non-JSON missive
                    console.log("Missive parsing failed:", e);
                    outputHtml += `<div class="text-sm text-gray-600">Output available but not formatted</div>`;
                }
            } else if (!success) {
                outputHtml += `<div class="text-sm text-red-600">Execution failed</div>`;
            }
            
            // Only show detailed errors in console, not in UI (for cleaner display)
            if (result.stderr) {
                console.error(`Full stderr for ${filename}:`, result.stderr);
            }
            
            div.innerHTML = outputHtml;
            resultsContainer.appendChild(div);
            
        } catch (error) {
            console.error(`Error with ${filename}:`, error);
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
    if (successCount > 0 || failureCount > 0) {
        const summaryDiv = document.createElement('div');
        summaryDiv.className = 'mt-4 pt-4 border-t text-sm text-gray-600';
        summaryDiv.innerHTML = `${successCount} réussi(s), ${failureCount} échoué(s)`;
        resultsContainer.appendChild(summaryDiv);
    }
    
    // Re-enable button
    if (executeBtn) {
        executeBtn.disabled = false;
        executeBtn.textContent = 'Générer';
    }
    
    console.log("✅ Test complete");
}

/**
 * Setup execute button
 */
function setupExecuteButton() {
    console.log("Setting up execute button...");
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        console.log("Button found, adding click listener");
        executeBtn.onclick = async function() {
            console.log("Button clicked!");
            await executeAllGenerators();
        };
    } else {
        console.log("Button not found!");
    }
}

/**
 * Initialize the module
 */
export async function init() {
    console.log('Sujets0 Main Module initializing...');
    
    // Initialize tabs
    initializeTabs();
    
    // Load Nagini
    const naginiLoaded = await loadNagini();
    
    if (naginiLoaded) {
        // Run tests
        const basicTest = await testNaginiExecution();
        if (basicTest) {
            displayIndicatorNaginiIsReady();
            
            // Test with packages after a delay
            setTimeout(async () => {
                const packagesLoaded = await loadPackagesAndTeachers();
                
                // Enable the execute button once packages are loaded
                if (packagesLoaded) {
                    const executeBtn = document.getElementById('execute-all-generators-btn');
                    if (executeBtn) {
                        console.log("Enabling execute button...");
                        executeBtn.disabled = false;
                        executeBtn.classList.remove('btn-disabled');
                        executeBtn.title = 'Click to run generator tests';
                        
                        // Make sure onclick is set
                        executeBtn.onclick = async function() {
                            console.log("Button clicked from enable!");
                            await executeAllGenerators();
                        };
                        
                        console.log("Button enabled and onclick set");
                    }
                }
            }, 2000);
        }
    }
    
    // Setup execute button
    setupExecuteButton();
    
    // Also try after a delay as backup
    setTimeout(setupExecuteButton, 1000);
    
    console.log('Sujets0 Main Module initialized');
}

// Export functions for global access if needed
export { executeAllGenerators };

// Make executeAllGenerators available globally for debugging
window.executeAllGenerators = executeAllGenerators;
