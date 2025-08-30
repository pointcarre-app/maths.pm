/**
 * Sujets0 Main Module - REFACTORED
 * Coordinates all components with proper state management
 */

import { getStateManager } from './state-manager.js';
import { getProgressManager } from './unified-progress.js';
import { getPapyrusManager } from './papyrus-manager.js';
import { loadNaginiAndInitialize } from './index-nagini.js';
import { executeAllGenerators } from './index-generators.js';
import { 
    initializePapyrus,
    previewStudentCopy,
    printStudentCopy,
    printAllCopies,
    openTeacherManifest 
} from './index-papyrus-refactored.js';
import generationResults from './index-data-model.js';

/**
 * Initialize the Sujets0 module
 */
export async function init() {
    console.log('🚀 Initializing Sujets0 Module (Refactored)');
    
    const state = getStateManager();
    const progress = getProgressManager();
    
    try {
        // Show initialization progress
        progress.startOperation('loading', {
            detail: 'Chargement des composants...'
        });
        
        // Initialize KaTeX and Papyrus in parallel
        await Promise.all([
            initializeKatex(),
            initializePapyrus()
        ]);
        
        // Initialize Nagini with the generate handler
        const naginiReady = await loadNaginiAndInitialize(handleGenerate);
        
        // Update state when Nagini is ready
        if (naginiReady) {
            state.updateState({ naginiReady: true });
        }
        
        // Set up UI components
        setupFormHandlers();
        setupButtonStates();
        
        // Initialize state subscriptions
        setupStateSubscriptions();
        
        progress.complete('Système prêt');
        
        console.log('✅ Sujets0 module initialized successfully');
        
    } catch (error) {
        console.error('Failed to initialize Sujets0:', error);
        progress.error('Erreur d\'initialisation', error.message);
    }
}

/**
 * Initialize KaTeX for math rendering
 */
async function initializeKatex() {
    const state = getStateManager();
    
    // Check if KaTeX is already loaded
    if (window.katex) {
        state.updateState({ katexReady: true });
        return;
    }
    
    // Wait for KaTeX to load
    let attempts = 0;
    while (!window.katex && attempts < 20) {
        await new Promise(resolve => setTimeout(resolve, 250));
        attempts++;
    }
    
    if (window.katex) {
        console.log('✅ KaTeX loaded');
        state.updateState({ katexReady: true });
    } else {
        console.warn('⚠️ KaTeX failed to load');
    }
}

/**
 * Set up form event handlers
 */
function setupFormHandlers() {
    const state = getStateManager();
    const form = document.getElementById('arpege-form');
    
    if (!form) {
        console.warn('Form not found');
        return;
    }
    
    // Number of students input
    const nbEleves = document.getElementById('nb-eleves');
    if (nbEleves) {
        nbEleves.addEventListener('change', (e) => {
            const value = parseInt(e.target.value) || 2;
            const clamped = Math.max(1, Math.min(50, value));
            e.target.value = clamped;
            state.updateState({ 
                formData: { ...state.state.formData, nbEleves: clamped }
            });
        });
    }
    
    // Number of questions input
    const nbQuestions = document.getElementById('nb-questions');
    if (nbQuestions) {
        nbQuestions.addEventListener('change', (e) => {
            const value = parseInt(e.target.value) || 12;
            const clamped = Math.max(1, Math.min(12, value));
            e.target.value = clamped;
            state.updateState({ 
                formData: { ...state.state.formData, nbQuestions: clamped }
            });
        });
    }
    
    // Specialty radio buttons
    const specialtyRadios = document.querySelectorAll('input[name="sujets0"]');
    specialtyRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.checked) {
                const specialty = e.target.getAttribute('aria-label') || 'Spé.';
                state.updateState({ 
                    formData: { ...state.state.formData, specialty }
                });
            }
        });
    });
    
    // Generate button handler is set by Nagini's enableExecuteButton
    // We don't set it here to avoid conflicts
}

/**
 * Set up button state management
 */
function setupButtonStates() {
    const state = getStateManager();
    
    // Note: The generate button is managed by Nagini's enableExecuteButton
    // We only manage its state during operations
    // Don't register it here to avoid conflicts
    
    state.registerButton('print-current-btn', (s) => 
        s.hasGeneratedContent && !s.isPrinting
    );
    
    state.registerButton('print-all-btn', (s) => 
        s.hasGeneratedContent && s.papyrusReady && !s.isPrinting
    );
    
    state.registerButton('teacher-manifest-btn', (s) => 
        s.hasGeneratedContent
    );
}

/**
 * Set up state subscriptions for UI updates
 */
function setupStateSubscriptions() {
    const state = getStateManager();
    
    // Subscribe to generation state changes
    state.subscribe('generation', (newState, oldState) => {
        if (newState.hasGeneratedContent && !oldState.hasGeneratedContent) {
            // New content generated - show first student
            if (generationResults.students.length > 0) {
                previewStudentCopy(0);
            }
        }
    });
    
    // Subscribe to error state
    state.subscribe('errors', (newState) => {
        if (newState.errors.length > 0) {
            const latestError = newState.errors[newState.errors.length - 1];
            console.error('Error:', latestError);
            // Could show a toast notification here
        }
    });
}

/**
 * Handle generate button click
 */
async function handleGenerate() {
    const state = getStateManager();
    const progress = getProgressManager();
    
    // Get form data
    const formData = state.state.formData;
    
    // Validate
    if (!formData.nbEleves || !formData.nbQuestions) {
        console.error('Invalid form data');
        return;
    }
    
    // Update state and disable generate button
    state.updateState({ 
        isGenerating: true,
        hasGeneratedContent: false 
    });
    
    // Manually disable generate button during operation
    const generateBtn = document.getElementById('execute-all-generators-btn');
    if (generateBtn) {
        generateBtn.disabled = true;
        generateBtn.classList.add('btn-disabled');
    }
    
    // Start progress
    progress.startOperation('generation', {
        max: formData.nbQuestions * 3, // 3 generators
        detail: 'Initialisation...'
    });
    
    try {
        // Execute generators
        const results = await executeAllGenerators(
            {
                nbEleves: formData.nbEleves,
                nbQuestions: formData.nbQuestions,
                sujets0: formData.specialty
            },
            (current, total, message) => {
                progress.update(current, message);
            }
        );
        
        // Store results
        generationResults.students = results.students || [];
        generationResults.totalQuestions = formData.nbQuestions;
        generationResults.currentStudentIndex = 0;
        
        // Update state
        state.updateState({
            isGenerating: false,
            hasGeneratedContent: true,
            totalStudents: results.students.length,
            students: results.students
        });
        
        // Complete progress
        progress.complete(`${results.students.length} copies générées avec succès`);
        
        console.log('Generation complete:', results);
        
        // Re-enable generate button
        const generateBtn = document.getElementById('execute-all-generators-btn');
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.classList.remove('btn-disabled');
        }
        
    } catch (error) {
        console.error('Generation failed:', error);
        progress.error('Erreur lors de la génération', error.message);
        state.updateState({ 
            isGenerating: false,
            hasGeneratedContent: false 
        });
        state.addError(error);
        
        // Re-enable generate button on error
        const generateBtn = document.getElementById('execute-all-generators-btn');
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.classList.remove('btn-disabled');
        }
    }
}

/**
 * Export functions for global use
 */
window.sujets0State = getStateManager();
window.executeAllGenerators = handleGenerate;
window.previewStudentCopy = previewStudentCopy;
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;
window.openTeacherManifest = openTeacherManifest;
window.generationResults = generationResults;

// Export for module use
export {
    handleGenerate as executeAllGenerators,
    previewStudentCopy,
    printStudentCopy,
    printAllCopies,
    openTeacherManifest
};
