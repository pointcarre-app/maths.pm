/**
 * UI Module for Sujets0
 * Handles UI interactions and tab management
 */

/**
 * Initialize tab switching functionality
 */
export function initializeTabs() {
    const tabLinks = document.querySelectorAll('.tabs .tab');
    const tabContents = document.querySelectorAll('.tab-alt-content');
    
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update link states
            tabLinks.forEach(lnk => lnk.classList.remove('tab-active'));
            this.classList.add('tab-active');
            
            // Update content visibility
            const tabName = this.getAttribute('data-tab');
            tabContents.forEach(content => content.classList.add('tab-alt-hidden'));
            
            const selectedContent = document.getElementById(tabName + '-content');
            if (selectedContent) {
                selectedContent.classList.remove('tab-alt-hidden');
            }
        });
    });
}

/**
 * Show error message if Nagini fails to load
 */
export function showNaginiError() {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error mt-4';
    errorDiv.innerHTML = `
        <strong>⚠️ Nagini Loading Error</strong><br />
        Failed to load Python engine. Please refresh the page.
    `;
    document.querySelector('.padding-alt-security')?.appendChild(errorDiv);
}

/**
 * Update Nagini status indicator
 */
export function displayIndicatorNaginiIsReady() {
    const naginiDot = document.getElementById("nagini-dot");
    if (naginiDot) {
        naginiDot.classList.replace("badge-warning", "badge-success");
    }
    const naginiLabel = document.getElementById("nagini-label");
    if (naginiLabel) {
        naginiLabel.textContent = "Nagini ready";
    }
}

/**
 * Enable the execute button
 * @param {Function} executeAllGenerators - The function to call when the button is clicked
 */
export function enableExecuteButton(executeAllGenerators) {
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.disabled = false;
        executeBtn.classList.remove('btn-disabled');
        executeBtn.onclick = executeAllGenerators;
    }
}
