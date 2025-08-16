/**
 * Error Analysis Module
 * Handles filtering, display, and export of generation errors
 */

/**
 * Apply filters to error table
 */
function applyFilters() {
    const generatorFilter = document.getElementById('generator-filter').value;
    const errorTypeFilter = document.getElementById('error-type-filter').value;
    const searchFilter = document.getElementById('search-filter').value.toLowerCase();
    
    const rows = document.querySelectorAll('.error-row');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const generator = row.dataset.generator;
        const errorType = row.dataset.errorType;
        const errorText = row.dataset.error;
        
        let show = true;
        
        if (generatorFilter !== 'all' && generator !== generatorFilter) {
            show = false;
        }
        
        if (errorTypeFilter !== 'all' && errorType !== errorTypeFilter) {
            show = false;
        }
        
        if (searchFilter && !errorText.includes(searchFilter) && !generator.toLowerCase().includes(searchFilter)) {
            show = false;
        }
        
        row.style.display = show ? '' : 'none';
        // Also hide the traceback row
        const nextRow = row.nextElementSibling;
        if (nextRow && nextRow.id && nextRow.id.startsWith('traceback-')) {
            if (!show) nextRow.style.display = 'none';
        }
        
        if (show) visibleCount++;
    });
    
    document.getElementById('visible-count').textContent = visibleCount;
}

/**
 * Toggle traceback visibility
 */
function toggleTraceback(id) {
    const element = document.getElementById(id);
    element.classList.toggle('hidden');
}

/**
 * Copy error details to clipboard
 */
function copyError(index, generator, seed, errorType, error, traceback) {
    const text = `Generator: ${generator}
Seed: ${seed}
Error Type: ${errorType}
Error: ${error}

Traceback:
${traceback}`;
    
    navigator.clipboard.writeText(text).then(() => {
        // Show feedback
        const btn = event.target.closest('button');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '✓';
        setTimeout(() => {
            btn.innerHTML = originalHTML;
        }, 1000);
    });
}

/**
 * Export all visible errors for LLM analysis
 */
function exportErrors() {
    const rows = document.querySelectorAll('.error-row');
    let exportText = `# Error Analysis Report
Generated: ${new Date().toISOString()}
Total Errors: ${document.getElementById('visible-count').textContent}

## Errors by Generator:

`;
    
    const errorsByGenerator = {};
    
    rows.forEach(row => {
        if (row.style.display !== 'none') {
            const generator = row.dataset.generator;
            const cells = row.querySelectorAll('td');
            const seed = cells[2].textContent;
            const errorType = cells[3].textContent.trim();
            const error = cells[4].textContent.trim();
            
            if (!errorsByGenerator[generator]) {
                errorsByGenerator[generator] = [];
            }
            
            errorsByGenerator[generator].push({
                seed,
                errorType,
                error
            });
        }
    });
    
    Object.keys(errorsByGenerator).sort().forEach(generator => {
        exportText += `\n### ${generator} (${errorsByGenerator[generator].length} errors)\n\n`;
        errorsByGenerator[generator].forEach(err => {
            exportText += `- Seed ${err.seed}: [${err.errorType}] ${err.error}\n`;
        });
    });
    
    document.getElementById('export-text').value = exportText;
    document.getElementById('export-modal').showModal();
}

/**
 * Copy export text to clipboard
 */
function copyExportText() {
    const textarea = document.getElementById('export-text');
    textarea.select();
    document.execCommand('copy');
    
    // Show feedback
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '✓ Copié!';
    setTimeout(() => {
        btn.textContent = originalText;
    }, 1500);
}

/**
 * Initialize the module
 */
export function init() {
    console.log('Error Analysis module initializing...');
    
    // Setup event listeners
    const generatorFilter = document.getElementById('generator-filter');
    const errorTypeFilter = document.getElementById('error-type-filter');
    const searchFilter = document.getElementById('search-filter');
    const exportBtn = document.getElementById('export-btn');
    
    if (generatorFilter) {
        generatorFilter.addEventListener('change', applyFilters);
    }
    
    if (errorTypeFilter) {
        errorTypeFilter.addEventListener('change', applyFilters);
    }
    
    if (searchFilter) {
        searchFilter.addEventListener('input', applyFilters);
    }
    
    if (exportBtn) {
        exportBtn.addEventListener('click', exportErrors);
    }
    
    // Make functions available globally for onclick handlers in HTML
    window.toggleTraceback = toggleTraceback;
    window.copyError = copyError;
    window.copyExportText = copyExportText;
    
    console.log('Error Analysis module initialized');
}

// Export functions
export { applyFilters, toggleTraceback, copyError, exportErrors, copyExportText };
