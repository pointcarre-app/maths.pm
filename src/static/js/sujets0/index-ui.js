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
    // Create a brief notification at the top of the page
    const executeBtn = document.getElementById('execute-all-generators-btn');
    if (executeBtn) {
        executeBtn.title = "Failed to load Python engine. Please refresh the page.";
        executeBtn.innerHTML = `<strong>⚠️ Nagini Loading Error</strong>`;
    }
}

/**
 * Update Nagini status indicator (now only affects the execute button)
 */
export function displayIndicatorNaginiIsReady() {
    // Journal de session section has been removed
    // This function is now simplified to a no-op as the visual indicators are gone
    // Functionality is preserved through enableExecuteButton
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
