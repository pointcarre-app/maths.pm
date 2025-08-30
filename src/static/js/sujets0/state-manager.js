/**
 * Centralized State Management for Sujets0
 * Manages the entire application state and coordinates between components
 */

export class Sujets0State {
    constructor() {
        // Initialize state
        this.state = {
            // System readiness
            papyrusReady: false,
            naginiReady: false,
            katexReady: false,
            
            // Operation states
            isGenerating: false,
            isConverting: false,
            isPrinting: false,
            
            // Content state
            hasGeneratedContent: false,
            currentStudentIndex: 0,
            totalStudents: 0,
            students: [],
            
            // Form data
            formData: {
                nbEleves: 2,
                nbQuestions: 12,
                specialty: 'Spé.'
            },
            
            // Error tracking
            errors: [],
            warnings: []
        };
        
        // State change listeners
        this.listeners = new Map();
        this.buttonStateHandlers = new Map();
    }
    
    /**
     * Update state and notify listeners
     */
    updateState(updates) {
        const prevState = { ...this.state };
        this.state = { ...this.state, ...updates };
        
        // Log state changes in development
        if (window.location.hostname === 'localhost') {
            console.log('State updated:', updates);
        }
        
        this.notifyListeners(prevState);
        this.updateButtonStates();
    }
    
    /**
     * Get current state
     */
    getState() {
        return { ...this.state };
    }
    
    /**
     * Subscribe to state changes
     */
    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, []);
        }
        this.listeners.get(key).push(callback);
        
        // Return unsubscribe function
        return () => {
            const callbacks = this.listeners.get(key);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        };
    }
    
    /**
     * Notify all listeners of state changes
     */
    notifyListeners(prevState) {
        this.listeners.forEach((callbacks, key) => {
            callbacks.forEach(callback => {
                try {
                    callback(this.state, prevState);
                } catch (error) {
                    console.error(`Error in state listener for ${key}:`, error);
                }
            });
        });
    }
    
    /**
     * Register button state handler
     */
    registerButton(buttonId, stateCondition) {
        this.buttonStateHandlers.set(buttonId, stateCondition);
        this.updateButtonState(buttonId);
    }
    
    /**
     * Update all button states based on current state
     */
    updateButtonStates() {
        this.buttonStateHandlers.forEach((condition, buttonId) => {
            this.updateButtonState(buttonId);
        });
    }
    
    /**
     * Update single button state
     */
    updateButtonState(buttonId) {
        const button = document.getElementById(buttonId);
        if (!button) return;
        
        const condition = this.buttonStateHandlers.get(buttonId);
        if (!condition) return;
        
        const shouldEnable = condition(this.state);
        
        if (shouldEnable) {
            button.disabled = false;
            button.classList.remove('btn-disabled');
            button.removeAttribute('title');
        } else {
            button.disabled = true;
            button.classList.add('btn-disabled');
            
            // Add helpful tooltip based on state
            const tooltip = this.getButtonTooltip(buttonId);
            if (tooltip) {
                button.setAttribute('title', tooltip);
            }
        }
    }
    
    /**
     * Get appropriate tooltip for disabled button
     */
    getButtonTooltip(buttonId) {
        const tooltips = {
            'execute-all-generators-btn': () => {
                if (!this.state.naginiReady) return 'En attente du chargement de Nagini...';
                if (this.state.isGenerating) return 'Génération en cours...';
                return 'Prêt à générer';
            },
            'print-current-btn': () => {
                if (!this.state.hasGeneratedContent) return 'Générez d\'abord des exercices';
                if (this.state.isPrinting) return 'Impression en cours...';
                return 'Imprimer la copie actuelle';
            },
            'print-all-btn': () => {
                if (!this.state.hasGeneratedContent) return 'Générez d\'abord des exercices';
                if (!this.state.papyrusReady) return 'En attente du système d\'impression...';
                if (this.state.isPrinting) return 'Impression en cours...';
                return 'Imprimer toutes les copies';
            },
            'teacher-manifest-btn': () => {
                if (!this.state.hasGeneratedContent) return 'Générez d\'abord des exercices';
                return 'Afficher la fiche enseignant';
            }
        };
        
        const getTooltip = tooltips[buttonId];
        return getTooltip ? getTooltip() : '';
    }
    
    /**
     * Add error to state
     */
    addError(error) {
        this.updateState({
            errors: [...this.state.errors, {
                message: error.message || error,
                timestamp: Date.now(),
                stack: error.stack
            }]
        });
    }
    
    /**
     * Clear errors
     */
    clearErrors() {
        this.updateState({ errors: [] });
    }
    
    /**
     * Check if system is ready for operations
     */
    isSystemReady() {
        return this.state.naginiReady && this.state.papyrusReady && this.state.katexReady;
    }
    
    /**
     * Check if any operation is in progress
     */
    isOperationInProgress() {
        return this.state.isGenerating || this.state.isConverting || this.state.isPrinting;
    }
    
    /**
     * Reset to initial state
     */
    reset() {
        this.updateState({
            hasGeneratedContent: false,
            currentStudentIndex: 0,
            totalStudents: 0,
            students: [],
            errors: [],
            warnings: []
        });
    }
}

// Create singleton instance
let stateInstance = null;

export function getStateManager() {
    if (!stateInstance) {
        stateInstance = new Sujets0State();
        
        // Make available globally for debugging
        if (window.location.hostname === 'localhost') {
            window.sujets0State = stateInstance;
        }
    }
    return stateInstance;
}
