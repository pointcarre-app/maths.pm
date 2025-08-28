/**
 * Papyrus Integration Module for Sujets0
 * Handles conversion of exercise data to Papyrus JSON format for printing
 */

import generationResults from './index-data-model.js';
import { generatePages } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/preview/index.js';
import { printPage } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/print-manager.js';
import { 
    initializeMargins, 
    setMargins 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/margin-config.js';
import { 
    initializeFontSizes, 
    setFontSizes 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/font-config.js';
import { 
    initializeSpaceBetweenDivs, 
    setSpaceBetweenDivs 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/core/margin-config.js';

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
 * Configure Papyrus with consistent settings for preview and print
 * @private
 */
function configurePapyrus() {
    // Initialize configurations
    initializeMargins();
    initializeFontSizes();
    initializeSpaceBetweenDivs();
    
    // Set standard margins (in mm)
    setMargins({
        top: 15,
        right: 15,
        bottom: 15,
        left: 15
    });
    
    // Set font sizes (in px)
    setFontSizes({
        h1: 28,
        h2: 24,
        h3: 20,
        h4: 18,
        h5: 16,
        h6: 14,
        body: 12
    });
    
    // Set spacing between divs
    setSpaceBetweenDivs(8);
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
    
    // Configure Papyrus with consistent settings
    configurePapyrus();
    
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
    const pagesContainer = document.getElementById('pages-container');
    pagesContainer.style.display = 'block';
    
    // Update the current student indicator in the pagination
    updatePaginationButtons(studentIndex);
    
    // Trigger print if requested
    if (triggerPrint) {
        // Use the same CSS for both preview and print
        const styleSheet = "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/styles/print.css";
        printPage(pagesContainer.innerHTML, styleSheet);
    }
}

/**
 * Print a specific student's exercise sheet
 * @param {number} studentIndex - Index of the student to print
 */
export async function printStudentCopy(studentIndex) {
    // First preview, then print
    await previewStudentCopy(studentIndex, true);
}

/**
 * Print all student copies
 */
export async function printAllCopies() {
    // Log how many copies will be printed
    console.log(`Printing all ${generationResults.students.length} copies`);
    
    // Configure Papyrus with consistent settings first
    configurePapyrus();
    
    // Store all student content
    let allContent = '';
    
    // For each student
    for (let i = 0; i < generationResults.students.length; i++) {
        // Generate JSON for this student
        const student = generationResults.students[i];
        if (!student) continue;
        
        // Create Papyrus JSON
        const papyrusJson = createPapyrusJson(student);
        
        // Update the JSON input field to generate the preview
        document.getElementById('json-input').value = JSON.stringify(papyrusJson);
        
        // Generate pages in the normal container
        generatePages();
        
        // Wait for rendering
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Get the rendered content
        const pagesContainer = document.getElementById('pages-container');
        if (pagesContainer) {
            // Add student content to the combined content
            allContent += pagesContainer.innerHTML;
            
            // Add a page break between students
            if (i < generationResults.students.length - 1) {
                allContent += '<div style="page-break-after: always;"></div>';
            }
        }
    }
    
    // Print all content with consistent styling
    const styleSheet = "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.4/src/styles/print.css";
    printPage(allContent, styleSheet);
    
    // Return to the first student after printing
    setTimeout(() => {
        previewStudentCopy(0, false);
    }, 1000);
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
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;
window.createPaginationButtons = createPaginationButtons;
