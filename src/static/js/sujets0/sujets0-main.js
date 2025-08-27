/**
 * Sujets0 Main Module
 * Handles the main functionality for the Sujets0 application
 * 
 * This is now a lightweight wrapper around the modular implementation.
 * All functionality has been refactored into separate modules with the prefix 'index-'.
 */

// Import all functionality from the modular implementation
import * as Sujets0 from './index-main.js';

/**
 * Initialize the module - now delegating to the modular implementation
 */
export async function init() {
    console.log('🚀 Delegating to modular Sujets0 implementation');
    await Sujets0.init();
}

// Export all functions from the modular implementation
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
    displayStudentResults,
    navigateStudent,
    navigateToStudent,
    generatePaginationButtons,
    renderPCAGraph,
    buildPCAGraph
} from './index-main.js';