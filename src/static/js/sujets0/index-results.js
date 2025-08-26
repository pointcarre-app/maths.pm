/**
 * Results Module for Sujets0
 * Handles displaying results and pagination
 */

import generationResults, { Question, Answer } from './index-data-model.js';

/**
 * Generate pagination buttons with ellipsis for large numbers
 * @param {number} current - Current page index (0-based)
 * @param {number} total - Total number of pages
 * @returns {string} HTML string for pagination buttons
 */
export function generatePaginationButtons(current, total) {
    const currentPage = current + 1; // Convert to 1-based for display
    let buttons = '';
    
    // For small number of pages, show all
    if (total <= 10) {
        for (let i = 1; i <= total; i++) {
            buttons += `
                <button class="join-item btn btn-sm ${i === currentPage ? 'btn-active' : ''}"
                        onclick="navigateToStudent(${i - 1})">
                    ${i}
                </button>
            `;
        }
    } else {
        // For larger numbers, use ellipsis
        const range = 2; // Numbers to show around current
        const showStart = currentPage <= range + 2;
        const showEnd = currentPage >= total - range - 1;
        
        // Always show first page
        buttons += `
            <button class="join-item btn btn-sm ${currentPage === 1 ? 'btn-active' : ''}"
                    onclick="navigateToStudent(0)">
                1
            </button>
        `;
        
        // Show ellipsis or numbers near start
        if (currentPage > range + 2) {
            buttons += `<button class="join-item btn btn-sm btn-disabled">...</button>`;
        }
        
        // Show pages around current
        for (let i = Math.max(2, currentPage - range); 
             i <= Math.min(total - 1, currentPage + range); 
             i++) {
            buttons += `
                <button class="join-item btn btn-sm ${i === currentPage ? 'btn-active' : ''}"
                        onclick="navigateToStudent(${i - 1})">
                    ${i}
                </button>
            `;
        }
        
        // Show ellipsis or numbers near end
        if (currentPage < total - range - 1) {
            buttons += `<button class="join-item btn btn-sm btn-disabled">...</button>`;
        }
        
        // Always show last page
        if (total > 1) {
            buttons += `
                <button class="join-item btn btn-sm ${currentPage === total ? 'btn-active' : ''}"
                        onclick="navigateToStudent(${total - 1})">
                    ${total}
                </button>
            `;
        }
    }
    
    return buttons;
}

/**
 * Navigate directly to a specific student
 * @param {number} studentIndex - Index of student to navigate to (0-based)
 */
export function navigateToStudent(studentIndex) {
    if (studentIndex >= 0 && studentIndex < generationResults.students.length) {
        generationResults.currentStudentIndex = studentIndex;
        displayStudentResults(studentIndex);
    }
}

/**
 * Navigate between students
 * @param {number} direction - -1 for previous, 1 for next
 */
export function navigateStudent(direction) {
    const newIndex = generationResults.currentStudentIndex + direction;
    if (newIndex >= 0 && newIndex < generationResults.students.length) {
        generationResults.currentStudentIndex = newIndex;
        displayStudentResults(newIndex);
    }
}

/**
 * Display results for a specific student with pagination
 * @param {number} studentIndex - Index of student to display
 */
export function displayStudentResults(studentIndex) {
    const container = document.getElementById('generator-results-container');
    if (!container || !generationResults.students.length) return;
    
    const student = generationResults.students[studentIndex];
    const totalStudents = generationResults.students.length;
    
    // Build HTML for student results
    let html = `
        <div class="mb-6">
            <!-- Pagination Header -->
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold">Copie ${studentIndex + 1} sur ${totalStudents}</h3>
                
                <!-- Pagination Controls -->
                <div class="join">
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(-1)"
                            ${studentIndex === 0 ? 'disabled' : ''}>
                        «
                    </button>
                    <button class="join-item btn btn-sm btn-active">
                        ${studentIndex + 1} / ${totalStudents}
                    </button>
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(1)"
                            ${studentIndex === totalStudents - 1 ? 'disabled' : ''}>
                        »
                    </button>
                </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="w-full bg-base-200 rounded-full h-2 mb-4">
                <div class="bg-primary h-2 rounded-full transition-all duration-300" 
                     style="width: ${((studentIndex + 1) / totalStudents) * 100}%"></div>
            </div>
            
            <!-- Questions Grid -->
            <div class="grid gap-4">
    `;
    
    // Add each question
    student.questions.forEach((question, qIndex) => {
        if (!question) {
            throw new Error(`Question at index ${qIndex} is undefined or null`);
        }
        
        // Define styles based on question success
        const rowClass = question.success ? '' : 'bg-error/20';
        const generatorName = question.generator || `Question ${qIndex + 1}`;
        
        // Create a simple display for question data
        const questionContent = `
            <div class="card ${rowClass} shadow-sm mb-8 overflow-hidden">
                <div class="card-header bg-base-200 p-2">
                    <h3 class="card-title font-mono text-base-content/70">${generatorName}</h3>
                </div>
                <div class="card-body">
                    ${question.success ? `
                        ${question.getBeacon() ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">beacon</p>
                                <code class="break-words">${question.getBeacon() || ''}</code>
                            </div>
                        ` : ''}
                        
                        <div class="mb-4">
                            <p class="font-bold mb-2">statement</p>
                            <div class="break-words overflow-wrap-anywhere">${question.statement || 'Non disponible'}</div>
                        </div>
                        
                        ${question.getStatementHtml() ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">statement_html</p>
                                <div class="break-words overflow-wrap-anywhere">${question.getStatementHtml()}</div>
                            </div>
                        ` : ''}
                        
                        <div class="mb-4">
                            <p class="font-bold mb-2">answers.latex (${question.getAllAnswers().length} total)</p>
                            ${question.getAllAnswers().length > 0 ? 
                                question.getAllAnswers().map((ans, idx) => `
                                    <div class="mb-2 break-words overflow-wrap-anywhere">
                                        ${question.getAllAnswers().length > 1 ? `<span class="badge badge-neutral mr-2">${idx + 1}</span>` : ''}
                                        <span class="font-mono inline-block">$${ans}$</span>
                                    </div>
                                `).join('')
                            : '<div class="text-base-content/50">No answers available</div>'}
                        </div>
                        
                        ${question.answer && question.answer.simplified_latex ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">answer.simplified_latex${Array.isArray(question.answer.simplified_latex) ? ` (${question.answer.simplified_latex.length} total)` : ''}</p>
                                ${Array.isArray(question.answer.simplified_latex) ? 
                                    question.answer.simplified_latex.map((simplified, idx) => `
                                        <div class="mb-2 break-words overflow-wrap-anywhere">
                                            ${question.answer.simplified_latex.length > 1 ? `<span class="badge badge-neutral mr-2">${idx + 1}</span>` : ''}
                                            <span class="font-mono inline-block">$${simplified}$</span>
                                        </div>
                                    `).join('')
                                : `
                                    <div class="break-words overflow-wrap-anywhere">
                                        <span class="font-mono inline-block">$${question.answer.simplified_latex}$</span>
                                    </div>
                                `}
                            </div>
                        ` : ''}
                        
                        ${question.answer && question.answer.formal_repr ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">answer.formal_repr</p>
                                <code class="break-words text-xs">${question.answer.formal_repr}</code>
                            </div>
                        ` : ''}
                        
                        ${question.answer && question.answer.sympy_exp_data ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">answer.sympy_exp_data</p>
                                <pre class="text-xs overflow-x-auto whitespace-pre-wrap break-words">${JSON.stringify(question.answer.sympy_exp_data, null, 2)}</pre>
                            </div>
                        ` : ''}
                        
                        ${question.getMask() ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">mask</p>
                                <code class="break-words">${question.getMask()}</code>
                            </div>
                        ` : ''}
                        
                        ${question.components ? `
                            <div class="mb-4">
                                <p class="font-bold mb-2">components</p>
                                <div class="collapse collapse-arrow">
                                    <input type="checkbox" /> 
                                    <div class="collapse-title text-sm font-medium">
                                        Afficher les composants
                                    </div>
                                    <div class="collapse-content"> 
                                        <pre class="text-xs overflow-x-auto whitespace-pre-wrap break-words">${JSON.stringify(question.components, null, 2)}</pre>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                    ` : `
                        <div class="mb-4">
                            <p class="font-bold mb-2">Erreur</p>
                            <div class="text-error">${question.error || 'Erreur inconnue'}</div>
                        </div>
                    `}
                </div>
            </div>
        `;
        
        // Add to the main HTML
        html += questionContent;
    });
    
    html += `
            </div>
            
            <!-- Summary Stats -->
            <div class="stats shadow mt-6">
                <div class="stat">
                    <div class="stat-title">Questions réussies</div>
                    <div class="stat-value text-success">
                        ${student.getSuccessCount()}
                    </div>
                    <div class="stat-desc">
                        sur ${student.getTotalCount()} questions
                    </div>
                </div>
                
                <div class="stat">
                    <div class="stat-title">Seed utilisé</div>
                    <div class="stat-value text-primary">
                        ${student.seed}
                    </div>
                    <div class="stat-desc">
                        Identifiant unique de la copie
                    </div>
                </div>
            </div>
            
            <!-- Full Pagination at Bottom -->
            <div class="flex justify-center mt-6">
                <div class="join">
                    <!-- Previous Button -->
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(-1)"
                            ${studentIndex === 0 ? 'disabled' : ''}>
                        «
                    </button>
                    
                    <!-- Page Numbers -->
                    ${generatePaginationButtons(studentIndex, totalStudents)}
                    
                    <!-- Next Button -->
                    <button class="join-item btn btn-sm" 
                            onclick="navigateStudent(1)"
                            ${studentIndex === totalStudents - 1 ? 'disabled' : ''}>
                        »
                    </button>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Render LaTeX with KaTeX
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(container, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
        });
    }
}
