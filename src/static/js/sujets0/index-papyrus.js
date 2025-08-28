/**
 * Papyrus Integration Module for Sujets0
 * Handles conversion of exercise data to Papyrus JSON format for printing
 */

import generationResults from './index-data-model.js';
import { generatePages } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.1/src/core/preview/index.js';
import { printPage } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.1/src/core/print-manager.js';

/**
 * Extract question number from generator name
 * @param {string} generator - Generator filename (e.g., 'spe_sujet1_auto_01_question')
 * @returns {string} Question number as a string
 */
function extractQuestionNumber(generator) {
    const match = generator.match(/auto_(\d+)_question/);
    return match ? match[1] : '?';
}

/**
 * Create the Papyrus JSON structure for a single student
 * @param {Object} studentExerciseSet - Student exercise set from generationResults
 * @returns {Array} Array of Papyrus JSON objects
 */
export function createPapyrusJson(studentExerciseSet) {
    // Extract student info
    const studentId = studentExerciseSet.id;
    const seed = studentExerciseSet.seed;
    
    console.log(`Creating Papyrus JSON for student ${studentId} with seed ${seed}`);
    
    // Initialize JSON array with header and title
    const papyrusJson = [
        // Header section with student info
        {
            "id": "header-section",
            "html": `<table style='width: 100%; border-collapse: collapse; border: 0.5px solid #e0e0e0;'>
                    <tr>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>Nom :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Classe :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Seed: ${seed}</td>
                    </tr>
                    <tr>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>Prénom :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Date :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>2nde&1ère|Spé</td>
                    </tr>
                </table>`,
            "classes": ["font-mono"],
            "isPapyrusHeader": true
        },
        
        // Title section
        {
            "id": "main-title",
            "html": "<div>Bac 1ère Spé. Maths : Partie 1 automatismes</div>",
            "style": "font-family: 'Spectral', serif; font-size: 24px; font-weight: bold; text-align: left; color: #2c3e50;"
        },
        {
            "id": "subtitle",
            "html": "<div>Questions inspirées des Sujets 0</div>",
            "style": "font-family: 'Spectral', serif; font-size: 18px; font-weight: 500; text-align: left; color: #5a6c7d; font-style: italic;"
        }
    ];
    
    // Process each question
    studentExerciseSet.questions.forEach((question, index) => {
        // Extract question number from generator name
        const questionNum = extractQuestionNumber(question.generator);
        
        // Get statement HTML, or fallback to regular statement
        const statementHtml = question.getStatementHtml() || question.statement;
        
        // Create the question HTML
        let questionHtml;
        
        // If there's a graph SVG, use a layout that prioritizes the graph
        if (question.graphSvg) {
            questionHtml = `
                <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
                    <div style='flex: 1; min-width: 250px;'>${questionNum}) ${statementHtml}</div>
                    <div style='flex: 0 1 auto;'>${question.graphSvg}</div>
                </div>
            `;
        } else {
            // Simple layout for questions without graphs
            questionHtml = `<div>${questionNum}) ${statementHtml}</div>`;
        }
        
        // Add to papyrusJson
        papyrusJson.push({
            "id": `question-${questionNum}`,
            "html": questionHtml,
            "classes": []
        });
    });
    
    return papyrusJson;
}

/**
 * Preview a specific student's exercise sheet
 * @param {number} studentIndex - Index of the student to preview
 * @param {boolean} triggerPrint - Whether to trigger the print dialog
 */
export async function previewStudentCopy(studentIndex, triggerPrint = false) {
    const student = generationResults.students[studentIndex];
    if (!student) {
        console.error(`No student found at index ${studentIndex}`);
        return;
    }
    
    // Create Papyrus JSON
    const papyrusJson = createPapyrusJson(student);
    
    // Log the JSON to console for debugging
    console.log('Papyrus JSON for preview:', papyrusJson);
    
    // Set the JSON data to the input field
    document.getElementById('json-input').value = JSON.stringify(papyrusJson);
    
    // Generate pages
    generatePages();
    
    // Wait for rendering
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Make sure pages container is visible
    document.getElementById('pages-container').style.display = 'block';
    
    // Update the current student indicator in the pagination
    updatePaginationButtons(studentIndex);
    
    // Trigger print if requested
    if (triggerPrint) {
        printPage();
    }
}

/**
 * Print the currently displayed student copy
 */
export async function printCurrentCopy() {
    printPage();
}

/**
 * Print all student copies (one by one)
 */
export async function printAllCopies() {
    // Just log how many copies would be printed
    console.log(`Would print all ${generationResults.students.length} copies`);
    
    // For now, just print the first student's copy
    await previewStudentCopy(0, true);
}

/**
 * Create pagination buttons for all students
 */
export function createPaginationButtons() {
    const paginationContainer = document.getElementById('student-pagination');
    if (!paginationContainer) return;
    
    // Clear existing buttons
    paginationContainer.innerHTML = '';
    
    // Create buttons for each student
    generationResults.students.forEach((student, index) => {
        const button = document.createElement('button');
        button.className = 'btn btn-sm';
        button.textContent = `Élève ${student.id}`;
        button.onclick = () => previewStudentCopy(index);
        
        paginationContainer.appendChild(button);
    });
}

/**
 * Update pagination buttons to highlight current student
 * @param {number} currentIndex - Index of the current student
 */
export function updatePaginationButtons(currentIndex) {
    const paginationContainer = document.getElementById('student-pagination');
    if (!paginationContainer) return;
    
    // Update button states
    Array.from(paginationContainer.children).forEach((button, index) => {
        if (index === currentIndex) {
            button.classList.add('btn-primary');
        } else {
            button.classList.remove('btn-primary');
        }
    });
}

// Expose functions globally for use in HTML
window.previewStudentCopy = previewStudentCopy;
window.printCurrentCopy = printCurrentCopy;
window.printAllCopies = printAllCopies;
