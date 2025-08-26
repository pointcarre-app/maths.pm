/**
 * Generators Module for Sujets0
 * Handles generator execution logic and management
 */

import { executeGeneratorWithSeed } from './index-nagini.js';
import { getGeneratorConfig, displayValidationTable } from './index-form.js';
import { displayStudentResults } from './index-results.js';
import generationResults, { StudentExerciseSet } from './index-data-model.js';

// Export the generationResults for backward compatibility
export { generationResults };

/**
 * Randomly select N items from an array
 * @param {Array} array - Source array
 * @param {number} n - Number of items to select
 * @returns {Array} Selected items
 */
export function selectRandomItems(array, n) {
    const shuffled = [...array].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
}

/**
 * Execute all generators with pagination
 */
export async function executeAllGenerators() {
    // Check if Nagini is ready (indirectly)
    if (!window.Nagini) {
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
    
    // Select generators based on question count
    // If all 12 are selected, keep them in order; otherwise randomly select
    let selectedGenerators;
    if (config.nbQuestions === 12) {
        // Keep all generators in their original order
        selectedGenerators = [...allGenerators];
    } else {
        // Randomly select subset of generators
        selectedGenerators = selectRandomItems(allGenerators, config.nbQuestions);
    }
    generationResults.selectedGenerators = selectedGenerators;
    
    console.log(`Selected ${config.nbQuestions} generators:`, selectedGenerators);
    
    // Reset results using the data model
    generationResults.reset();
    generationResults.setConfig(config);
    generationResults.setSelectedGenerators(selectedGenerators);
    
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
        // const seed = studentNum; // Use student number as seed
        const seed = Math.floor(Math.random() * 1_000); // Random seed
        const questionResults = [];
        
        // Update progress
        const progressBar = resultsContainer.querySelector('progress');
        if (progressBar) {
            progressBar.value = studentNum - 1;
        }
        
        // Execute each selected generator for this student
        for (const generator of selectedGenerators) {
            const result = await executeGeneratorWithSeed(generator, seed);
            questionResults.push(result);
        }
        
        // Create and store student exercise set using our data model
        const studentExerciseSet = StudentExerciseSet.fromGeneratorResults(
            studentNum,
            seed,
            questionResults,
            selectedGenerators
        );
        
        generationResults.addStudent(studentExerciseSet);
    }
    
    // Display first student's results
    displayStudentResults(0);
    
    // Re-enable button
    if (executeBtn) {
        executeBtn.disabled = false;
        executeBtn.textContent = 'Générer';
    }
}
