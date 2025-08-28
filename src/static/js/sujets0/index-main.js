/**
 * Sujets0 Main Module
 * Entry point that imports and initializes all other modules
 */

// Import modules
import { loadBackendSettings, getAllProductSettings, processGeneratorLevels } from './index-settings.js';
import { initializeTabs } from './index-ui.js';
import { loadNaginiAndInitialize, getBackendSettings, setBackendSettings } from './index-nagini.js';
import { 
    extractFormValues, 
    validateFormData, 
    applyFormValidationStyles, 
    displayValidationTable, 
    getGeneratorConfig 
} from './index-form.js';
import { executeAllGenerators, generationResults, selectRandomItems } from './index-generators.js';
import { 
    displayStudentResults, 
    navigateStudent, 
    navigateToStudent, 
    generatePaginationButtons 
} from './index-results.js';
import { buildPCAGraph, renderPCAGraph } from './index-graphs.js';
import { printStudentCopy, printAllCopies } from './index-papyrus.js';

// Initialize the module
export async function init() {
    console.log('🚀 Initializing Sujets0 Module');
    
    // Load backend settings first
    const backendSettings = loadBackendSettings();
    setBackendSettings(backendSettings);
    
    // Log all available settings on initialization
    console.group('📋 Available Product Settings');
    const allSettings = getAllProductSettings();
    console.log('All settings loaded:', Object.keys(allSettings));
    console.groupEnd();
    
    // Process generator levels from backend settings
    processGeneratorLevels(backendSettings);
    
    // Initialize tabs
    initializeTabs();
    
    // Load Nagini and initialize
    await loadNaginiAndInitialize(executeAllGenerators);
    
    console.log('✨ Sujets0 Module initialized successfully');
}

// Make navigation functions available globally
window.navigateStudent = navigateStudent;
window.navigateToStudent = navigateToStudent;

// Make functions available globally for debugging
window.executeAllGenerators = executeAllGenerators;
window.extractFormValues = extractFormValues;
window.getGeneratorConfig = getGeneratorConfig;
window.loadBackendSettings = loadBackendSettings;
window.getAllProductSettings = getAllProductSettings;
window.getBackendSettings = getBackendSettings;
window.applyFormValidationStyles = applyFormValidationStyles;
window.displayValidationTable = displayValidationTable;
window.generationResults = generationResults; // Expose results for debugging
window.displayStudentResults = displayStudentResults;
window.renderPCAGraph = renderPCAGraph;
window.buildPCAGraph = buildPCAGraph;
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;

// Export all functions that might be needed by other modules
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
};
