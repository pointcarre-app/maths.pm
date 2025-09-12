/**
 * Nagini Integration Module for Sujets0
 * Handles loading and initializing Nagini for Python execution
 */

import { displayIndicatorNaginiIsReady, showNaginiError, enableExecuteButton } from './index-ui.js';
import { loadBackendSettings } from './index-settings.js';



// Global state
let Nagini = null;
let naginiManager = null;
let backendSettings = null;

/**
 * Load Nagini and initialize manager
 * @param {Function} executeAllGenerators - The function to call when Execute button is clicked
 * @returns {Promise<boolean>} Whether initialization was successful
 */
export async function loadNaginiAndInitialize(executeAllGenerators) {
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



        const teachersGitTag = 'v0.0.24';
        
        // Files for teachers module
        const teachersFiles = [
            { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/__init__.py`, path: "teachers/__init__.py" },
            { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/generator.py`, path: "teachers/generator.py" },
            { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/maths.py`, path: "teachers/maths.py" },
            { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/formatting.py`, path: "teachers/formatting.py" },
            { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/corrector.py`, path: "teachers/corrector.py" },
            { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/defaults.py`, path: "teachers/defaults.py" }
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
        enableExecuteButton(executeAllGenerators);
        
        return true;
    } catch (error) {
        console.error('Failed to initialize Nagini:', error);
        showNaginiError();
        return false;
    }
}

/**
 * Execute a generator with a specific seed
 * @param {string} filename - Generator filename
 * @param {number} seed - Random seed
 * @returns {Object} Execution result
 */
export async function executeGeneratorWithSeed(filename, seed) {
    // Detect if we're on GitHub Pages or similar static hosting and adjust the URL accordingly
    let basePath = '';
    
    // Method 1: Check if we're on GitHub Pages
    if (window.location.hostname === 'pointcarre-app.github.io') {
        basePath = '/maths.pm';
        console.log('🌐 GitHub Pages detected, using base path:', basePath);
    }
    // Method 2: Check if we're already in a subdirectory (more generic)
    else if (window.location.pathname.startsWith('/maths.pm/')) {
        basePath = '/maths.pm';
        console.log('📁 Subdirectory deployment detected, using base path:', basePath);
    }
    
    const url = `${basePath}/static/sujets0/generators/${filename}`;
    console.log('📦 Loading generator from:', url);
    
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
                    statement: data.statement || data.question, //TODO:  why not only one ? and the html ?
                    answer: data.answer,  // Pass the entire answer object to preserve structure
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
 * Get the Nagini manager instance
 * @returns {Object|null} Nagini manager or null if not initialized
 */
export function getNaginiManager() {
    return naginiManager;
}

/**
 * Get the backend settings
 * @returns {Object|null} Backend settings or null if not loaded
 */
export function getBackendSettings() {
    return backendSettings;
}

/**
 * Set the backend settings
 * @param {Object} settings - The settings object to set
 */
export function setBackendSettings(settings) {
    backendSettings = settings;
}
