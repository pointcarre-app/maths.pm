/**
 * Papyrus Integration Module for Sujets0
 * Handles conversion of exercise data to Papyrus JSON format for printing
 */

import generationResults from './index-data-model.js';
import { generatePages } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/core/preview/index.js';
import { printPage } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/core/print-manager.js';
import { 
    initializeMargins, 
    setMargins 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/core/margin-config.js';
import { 
    initializeFontSizes, // Default font sizes in px
    setFontSizes 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/core/font-config.js';

import { 
    initializePageNumberConfig,
    setShowPageNumbers 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/core/page-number-config.js';



// Default font sizes in px
// const DEFAULT_FONT_SIZES = {
//     h1: 32,
//     h2: 28,
//     h3: 24,
//     h4: 20,
//     h5: 18,
//     h6: 16,
//     body: 18
// };
import { 
    initializeSpaceBetweenDivs, 
    setSpaceBetweenDivs 
} from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/core/margin-config.js';

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
            "html": `<table style='width: 100%; border-collapse: collapse; border: 0.5px solid #e0e0e0;margin-bottom: 1rem !important;'>
                    <tr>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>Nom :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Classe :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Seed: ${seed}</td>
                    </tr>
                    <tr>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>Prénom :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Date :</td>
                        <td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>Spé</td>
                    </tr>
                </table>`,
            "classes": ["font-mono"],
            "isPapyrusHeader": true
        },
        
        // Title section
        // TODO: anticipate h1 for SEO
        {
            "id": "main-title",
            "html": "<h3>Bac 1<sup>ère</sup> Maths - Première Partie : Automatismes</h3>",
            "style": "font-family: 'Spectral', serif; font-weight: bold; text-align: left; color: var(--color-base-content);margin-bottom: 2rem !important;margin-top: 1rem !important;"
        },
        // {
        //     "id": "subtitle",
        //     "html": "<div>Questions inspirées des Sujets 0</div>",
        //     "style": "font-family: 'Spectral', serif; font-size: 18px; font-weight: 500; text-align: left; color: #5a6c7d; font-style: italic;"
        // }
    ];
    
    // Process each question
    studentExerciseSet.questions.forEach((question, index) => {
        // Extract question number from generator name
        // remove leading 0 of questionNum
        const questionNum = extractQuestionNumber(question.generator).replace(/^0+/, '');

                
        // Get statement HTML, or fallback to regular statement
        const statementHtml = question.getStatementHtml() || question.statement;
        
        // Create the question HTML
        let questionHtml;
        
        // Process statementHtml first to inject question number
        let processedStatement;
        

        // TODO: temporary cause will work for all as checked
        // Special case: Check if statementHtml starts with the flex container structure



        if (statementHtml.startsWith("<div style='display: flex;")) {
            // Insert question number inside the second div (the child div)
            processedStatement = statementHtml.replace(
                "<div style='flex: 1; min-width: 250px;'>",
                `<div style='flex: 1; min-width: 250px;'>${questionNum})&nbsp;&nbsp;`
            );
        } else if (statementHtml.startsWith('<div>')) {
            // Insert question number inside the first div with a non-breaking space
            processedStatement = statementHtml.replace('<div>', `<div>${questionNum})&nbsp;&nbsp;`);
        } else {
            // Wrap in div with question number
            processedStatement = `<div>${questionNum}) ${statementHtml}</div>`;
        }
        
        // If there's a graph SVG, use a layout that prioritizes the graph
        if (question.graphSvg) {
            questionHtml = `
                <div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
                    <div style='flex: 1; min-width: 250px;'>${processedStatement}</div>
                    <div style='flex: 0 1 auto;'>${question.graphSvg}</div>
                </div>
            `;
        } else {
            // Simple layout for questions without graphs
            questionHtml = processedStatement;
        }
        
        // Add to papyrusJson
        papyrusJson.push({
            "id": `question-${questionNum}`,
            "html": questionHtml,
            // border-top: 1px solid #e0e0e0; padding-top: 0.25rem !important;
            "style": "margin-bottom: 2rem !important;"
        });
    });
    
    return papyrusJson;
}

/**
 * Get document settings from form inputs or defaults
 * @returns {Object} The document settings
 */
function getDocumentSettings() {
    // Fixed hardcoded settings
    return {
        margins: {
            top: 5,
            right: 12,
            bottom: 5,
            left: 12
        },
        fontSizes: {
            h1: 28,
            h2: 24,
            h3: 20,
            h4: 18,
            h5: 16,
            h6: 14,
            body: 15
        },
        spacing: 2
    };
}

/**
 * Apply document settings to CSS variables
 * @param {Object} settings - The document settings
 */
function applySettingsToCss(settings) {
    document.documentElement.style.setProperty('--papyrus-margin-top', `${settings.margins.top}mm`);
    document.documentElement.style.setProperty('--papyrus-margin-right', `${settings.margins.right}mm`);
    document.documentElement.style.setProperty('--papyrus-margin-bottom', `${settings.margins.bottom}mm`);
    document.documentElement.style.setProperty('--papyrus-margin-left', `${settings.margins.left}mm`);
    
    document.documentElement.style.setProperty('--papyrus-font-size-h1', `${settings.fontSizes.h1}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h2', `${settings.fontSizes.h2}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h3', `${settings.fontSizes.h3}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h4', `${settings.fontSizes.h4}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h5', `${settings.fontSizes.h5}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-h6', `${settings.fontSizes.h6}px`);
    document.documentElement.style.setProperty('--papyrus-font-size-body', `${settings.fontSizes.body}px`);


}

/**
 * Configure Papyrus with consistent settings for preview and print
 * @private
 */
function configurePapyrus() {
    // Get settings from form or defaults
    const settings = getDocumentSettings();
    
    // Apply settings to CSS variables
    applySettingsToCss(settings);
    
    // Initialize configurations
    initializeMargins();
    initializeFontSizes();
    initializeSpaceBetweenDivs();
    initializePageNumberConfig(); // Add this
    
    // Set margins from settings
    setMargins({
        top: settings.margins.top,
        right: settings.margins.right,
        bottom: settings.margins.bottom,
        left: settings.margins.left
    });
    
    // Set font sizes from settings
    setFontSizes({
        h1: settings.fontSizes.h1,
        h2: settings.fontSizes.h2,
        h3: settings.fontSizes.h3,
        h4: settings.fontSizes.h4,
        h5: settings.fontSizes.h5,
        h6: settings.fontSizes.h6,
        body: settings.fontSizes.body
    });
    
    // Set spacing between divs
    setSpaceBetweenDivs(settings.spacing);
    
    // Enable page numbers (add this)
    setShowPageNumbers(true); // Set to true to show page numbers
}

/**
 * Update document settings and refresh preview
 */
export async function updateDocumentSettings() {
    // Configure Papyrus with settings
    configurePapyrus();
    
    // Only try to refresh preview if we have student data
    if (generationResults.students && generationResults.students.length > 0) {
        // Get current student index
        const currentIndex = generationResults.currentStudentIndex || 0;
        
        // Update settings and refresh preview
        await previewStudentCopy(currentIndex, false);
    } else {
        // Just update the placeholder
        const pagesContainer = document.getElementById('pages-container');
        if (pagesContainer) {
            pagesContainer.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #4a5568; border: 1px dashed #cbd5e0; margin: 20px;">
                    <h3>Print Preview</h3>
                    <p>Generate exercises first to see a preview here.</p>
                </div>
            `;
            pagesContainer.style.display = 'block';
        }
    }
}

/**
 * Preview a specific student's exercise sheet
 * @param {number} studentIndex - Index of the student to preview
 * @param {boolean} triggerPrint - Whether to trigger the print dialog
 */
export async function previewStudentCopy(studentIndex, triggerPrint = false) {
    // Check if students array exists and has data
    if (!generationResults.students || !Array.isArray(generationResults.students) || generationResults.students.length === 0) {
        console.error('No student data available. Make sure exercises are generated before preview.');
        
        // Display an error message in the preview container if it exists
        const pagesContainer = document.getElementById('pages-container');
        if (pagesContainer) {
            pagesContainer.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #e53e3e; border: 1px solid #e53e3e; margin: 20px;">
                    <h3>No student data available</h3>
                    <p>Please generate exercises before attempting to preview.</p>
                </div>
            `;
            pagesContainer.style.display = 'block';
        }
        
        return;
    }
    
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
        const styleSheet = "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/styles/print.css";
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
    const styleSheet = "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.6/src/styles/print.css";
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
    
    // Create a title for the pagination area
    const title = document.createElement('div');
    title.className = 'flex items-center gap-2 font-medium mb-2';
    title.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
        </svg>
        Naviguer entre les copies (${generationResults.students.length})
    `;
    paginationContainer.appendChild(title);
    
    // Create button container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'flex flex-wrap gap-1 mb-2';
    paginationContainer.appendChild(buttonContainer);
    
    // Create buttons for each student
    generationResults.students.forEach((student, index) => {
        const button = document.createElement('button');
        button.className = 'btn btn-xs btn-outline';
        button.textContent = `${student.id}`;
        button.onclick = () => previewStudentCopy(index);
        button.title = `Voir la copie de l'élève ${student.id}`;
        
        buttonContainer.appendChild(button);
    });
}

/**
 * Update pagination buttons to highlight current student
 * @param {number} currentIndex - Index of the current student
 */
export function updatePaginationButtons(currentIndex) {
    const paginationContainer = document.getElementById('student-pagination');
    if (!paginationContainer) return;
    
    // Find the button container (second child after the title)
    const buttonContainer = paginationContainer.querySelector('div:nth-child(2)');
    if (!buttonContainer) return;
    
    // Update button states
    Array.from(buttonContainer.children).forEach((button, index) => {
        if (index === currentIndex) {
            button.classList.remove('btn-outline');
            button.classList.add('btn-primary');
        } else {
            button.classList.remove('btn-primary');
            button.classList.add('btn-outline');
        }
    });
    
    // Update the title to show current student
    const title = paginationContainer.querySelector('div:first-child');
    if (title) {
        const currentStudent = generationResults.students[currentIndex];
        if (currentStudent) {
            title.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
                </svg>
                Élève ${currentStudent.id} (${currentIndex + 1}/${generationResults.students.length})
            `;
        }
    }
}

/**
 * Initialize document settings
 */
export function initDocumentSettingsForm() {
    // Automatically apply default settings without requiring user interaction
    console.log('Initializing document settings with default values');
    
    // Apply basic configuration without trying to render a preview
    configurePapyrus();
    
    // Display a placeholder message in the preview container
    const pagesContainer = document.getElementById('pages-container');
    if (pagesContainer) {
        pagesContainer.innerHTML = `
            <div style="padding: 20px; text-align: center; color: #4a5568; border: 1px dashed #cbd5e0; margin: 20px;">
                <h3>Print Preview</h3>
                <p>Generate exercises first to see a preview here.</p>
            </div>
        `;
        pagesContainer.style.display = 'block';
    }
}

// Expose functions globally for use in HTML
window.previewStudentCopy = previewStudentCopy;
window.printStudentCopy = printStudentCopy;
window.printAllCopies = printAllCopies;
window.createPaginationButtons = createPaginationButtons;
window.updateDocumentSettings = updateDocumentSettings;
