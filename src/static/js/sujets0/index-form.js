/**
 * Form Module for Sujets0
 * Handles form handling, validation, and configuration
 */

/**
 * Extract all form values from the Arpege form
 * @returns {Object} Form data with validation and type conversion
 */
export function extractFormValues() {
    const form = document.getElementById('arpege-form');
    if (!form) {
        throw new Error('Form not found');
    }
    
    // Extract number inputs
    const studentCount = parseInt(document.getElementById('nb-eleves')?.value || '30', 10);
    const questionCount = parseInt(document.getElementById('nb-questions')?.value || '12', 10);
    
    // Extract radio button values
    // Program level is now hardcoded as it's been removed from the UI
    const programLevel = "2nde"; // Default to "2nde" since the UI option has been removed
    const specialization = document.querySelector('input[name="sujets0"]:checked')?.getAttribute('aria-label') || null;
    
    // Create structured form data object
    const formData = {
        // Student/Copy configuration
        copies: {
            count: studentCount,
            isValid: studentCount >= 1 && studentCount <= 50
        },
        
        // Question configuration
        questions: {
            perCopy: questionCount,
            isValid: questionCount >= 1 && questionCount <= 12
        },
        
        // Program level selection - hardcoded since UI option was removed
        program: {
            level: programLevel, // Always "2nde" since the UI option has been removed
            includesFirstYear: false, // Always false since we're using "2nde" as default
            isValid: true // Always valid since we're using a hardcoded value
        },
        
        // Specialization selection
        track: {
            type: specialization, // "Spé." or "Non Spé." or "Techno"
            isSpeciality: specialization === "Spé.",
            isValid: specialization !== null && specialization !== "Techno"
        },
        
        // Global validation
        isComplete: false,
        errors: []
    };
    
    // Validate all fields
    validateFormData(formData);
    
    // Apply visual validation feedback
    applyFormValidationStyles(formData);
    
    return formData;
}

/**
 * Validate form data and populate error messages
 * @param {Object} formData - The form data object to validate
 */
export function validateFormData(formData) {
    const errors = [];
    
    // Validate student count
    if (!formData.copies.isValid) {
        errors.push({
            field: 'copies',
            message: 'Le nombre de copies doit être entre 1 et 50'
        });
    }
    
    // Validate question count
    if (!formData.questions.isValid) {
        errors.push({
            field: 'questions',
            message: 'Le nombre de questions doit être entre 1 et 12'
        });
    }
    
    // Program level validation is skipped as it's now hardcoded
    // and always valid
    
    // Validate track selection
    if (!formData.track.isValid) {
        if (formData.track.type === "Techno") {
            errors.push({
                field: 'track',
                message: 'La filière technologique n\'est pas encore disponible'
            });
        } else {
            errors.push({
                field: 'track',
                message: 'Veuillez sélectionner une filière'
            });
        }
    }
    
    formData.errors = errors;
    formData.isComplete = errors.length === 0;
}

/**
 * Apply visual validation styles to form fields
 * @param {Object} formData - The validated form data
 */
export function applyFormValidationStyles(formData) {
    // Reset all error styles first
    document.getElementById('nb-eleves')?.classList.remove('input-error');
    document.getElementById('nb-questions')?.classList.remove('input-error');
    // Program level inputs no longer exist in UI, so we don't need to reset their styles
    document.querySelectorAll('input[name="sujets0"]').forEach(el => 
        el.closest('.join')?.classList.remove('ring-2', 'ring-error')
    );
    
    // Apply error styles based on validation
    if (!formData.copies.isValid) {
        document.getElementById('nb-eleves')?.classList.add('input-error');
    }
    
    if (!formData.questions.isValid) {
        document.getElementById('nb-questions')?.classList.add('input-error');
    }
    
    // Program level is no longer in the UI and is always valid
    
    if (!formData.track.isValid) {
        document.querySelector('input[name="sujets0"]')?.closest('.join')?.classList.add('ring-2', 'ring-error');
    }
}

/**
 * Display validation status in a table
 * @param {Object} formData - The form data with validation results
 */
export function displayValidationTable(formData) {
    // Find or create validation container
    let validationContainer = document.getElementById('validation-status-container');
    if (!validationContainer) {
        // Insert after "Génération d'exercices" heading
        const targetElement = document.querySelector('#journal-content .text-base.mt-4.mb-2');
        if (targetElement) {
            validationContainer = document.createElement('div');
            validationContainer.id = 'validation-status-container';
            validationContainer.className = 'mt-4';
            targetElement.parentNode.insertBefore(validationContainer, targetElement.nextSibling);
        }
    }
    
    if (!validationContainer) return;
    
    // Build status table HTML
    const timestamp = new Date().toLocaleTimeString('fr-FR');
    const statusRows = [
        {
            field: 'Nombre de copies',
            value: formData.copies.count,
            status: formData.copies.isValid,
            error: formData.errors.find(e => e.field === 'copies')?.message
        },
        {
            field: 'Questions par copie',
            value: formData.questions.perCopy,
            status: formData.questions.isValid,
            error: formData.errors.find(e => e.field === 'questions')?.message
        },
        // Program level row removed as it's no longer in the UI
        {
            field: 'Filière',
            value: formData.track.type || 'Non sélectionnée',
            status: formData.track.isValid,
            error: formData.errors.find(e => e.field === 'track')?.message
        }
    ];
    
    const tableHtml = `
        <div class="overflow-x-auto">
            <table class="table table-sm w-full" style="border-radius:var(--radius-box); border: 1px solid var(--color-base-content);">
                <thead>
                    <tr>
                        <th colspan="3" class="text-left bg-base-200 font-mono">
                            Tentative de génération - ${timestamp}
                        </th>
                    </tr>
                    <tr>
                        <th>Paramètre</th>
                        <th>Valeur</th>
                        <th>Statut</th>
                    </tr>
                </thead>
                <tbody>
                    ${statusRows.map(row => `
                        <tr class="${!row.status ? 'bg-error/10' : ''}">
                            <td>${row.field}</td>
                            <td>${row.value}</td>
                            <td>
                                ${row.status 
                                    ? '<span class="badge badge-success badge-sm">✓</span>' 
                                    : `<span class="text-error text-sm">${row.error || 'Invalide'}</span>`
                                }
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
                <tfoot>
                    <tr>
                        <th colspan="3" class="text-center ${formData.isComplete ? 'bg-success/20' : 'bg-error/20'}">
                            ${formData.isComplete 
                                ? '✓ Formulaire valide - Génération en cours...' 
                                : '✗ Veuillez corriger les erreurs ci-dessus'
                            }
                        </th>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    validationContainer.innerHTML = tableHtml;
}

/**
 * Get form configuration for generator execution
 * @returns {Object} Simplified configuration object for generators
 */
export function getGeneratorConfig() {
    const formData = extractFormValues();
    
    // Display validation table
    displayValidationTable(formData);
    
    if (!formData.isComplete) {
        console.error('Form validation errors:', formData.errors);
        return null;
    }
    
    return {
        nbStudents: formData.copies.count,
        nbQuestions: formData.questions.perCopy,
        programLevel: 'seconde', // Always 'seconde' since the UI option has been removed
        track: formData.track.isSpeciality ? 'speciality' : 'common',
        // Additional config can be added here
        timestamp: Date.now(),
        sessionId: crypto.randomUUID?.() || Math.random().toString(36).substr(2, 9)
    };
}
