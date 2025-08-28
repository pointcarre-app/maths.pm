/**
 * Papyrus Integration Module for Sujets0
 * Handles conversion of exercise data to Papyrus JSON format for printing
 */

import generationResults from './index-data-model.js';
import { generatePages } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/preview/index.js';
import { printPage } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/print-manager.js';

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
 * Print a specific student's exercise sheet
 * @param {number} studentIndex - Index of the student to print
 */
export async function printStudentCopy(studentIndex) {
    const student = generationResults.students[studentIndex];
    if (!student) {
        console.error(`No student found at index ${studentIndex}`);
        return;
    }
    
    // Create Papyrus JSON
    const papyrusJson = createPapyrusJson(student);
    
    // Log the JSON to console for debugging
    console.log('Papyrus JSON for printing:', papyrusJson);
    
    // Set the JSON data to the input field
    document.getElementById('json-input').value = JSON.stringify(papyrusJson);
    
    // Generate pages
    generatePages();
    
    // Wait for rendering
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Trigger print
    printPage(document.getElementById('pages-container').innerHTML, "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/styles/print.css");
}

/**
 * Print all student copies
 */
export async function printAllCopies() {
    // Just log how many copies would be printed
    console.log(`Would print all ${generationResults.students.length} copies`);
    
    // For now, just print the first student's copy
    await printStudentCopy(0);
}

// Expose functions globally for use in HTML
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;
