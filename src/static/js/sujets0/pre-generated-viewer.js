/**
 * Pre-generated Questions Viewer Module
 * Handles loading and displaying pre-generated math questions with pagination
 */

// Global state
let allQuestions = [];
let filteredQuestions = [];
let currentPage = 1;
let questionsPerPage = 20;
let currentGenerator = 'all';
let currentStatus = 'all';
let searchTerm = '';

// Data from Jinja2 (will be loaded from data attributes)
let QUESTIONS_INDEX = null;
let QUESTIONS_BASE_URL = null;

/**
 * Initialize the viewer
 */
export function init() {
    // Load data from data attributes
    const dataElement = document.getElementById('jinja-data');
    if (!dataElement) {
        console.error('jinja-data element not found');
        return;
    }
    
    QUESTIONS_INDEX = JSON.parse(dataElement.dataset.questionsIndex);
    QUESTIONS_BASE_URL = dataElement.dataset.questionsBaseUrl;
    
    console.log('Pre-generated questions viewer initialized');
    console.log('Total questions available:', QUESTIONS_INDEX.total_questions);
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize KaTeX auto-render
    setupKatexRendering();
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    const generatorSelect = document.getElementById('generator-select');
    const statusSelect = document.getElementById('status-select');
    const perPageSelect = document.getElementById('per-page-select');
    const searchInput = document.getElementById('search-input');
    const loadAllBtn = document.getElementById('load-all-btn');
    
    if (generatorSelect) {
        generatorSelect.addEventListener('change', handleGeneratorChange);
    }
    
    if (statusSelect) {
        statusSelect.addEventListener('change', handleStatusChange);
    }
    
    if (perPageSelect) {
        perPageSelect.addEventListener('change', handlePerPageChange);
    }
    
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
    
    if (loadAllBtn) {
        loadAllBtn.addEventListener('click', loadAllQuestions);
    }
}

/**
 * Setup KaTeX rendering
 */
function setupKatexRendering() {
    if (window.renderMathInElement) {
        document.addEventListener('questions-rendered', () => {
            renderMathInElement(document.getElementById('questions-container'), {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false}
                ]
            });
        });
    }
}

/**
 * Load all questions from JSON files
 */
async function loadAllQuestions() {
    const btn = document.getElementById('load-all-btn');
    const loading = document.getElementById('loading-indicator');
    const container = document.getElementById('questions-container');
    
    // Show loading
    btn.disabled = true;
    btn.innerHTML = '<span class="loading loading-spinner"></span> Chargement...';
    loading.classList.remove('hidden');
    container.innerHTML = '';
    
    try {
        allQuestions = [];
        const generators = QUESTIONS_INDEX.generators;
        
        // Load questions from each generator
        for (const generator of generators) {
            // Load ALL questions (both successful and failed)
            const totalQuestions = 100; // We always generate 100 questions per generator
            for (let seed = 0; seed < totalQuestions; seed++) {
                const url = `${QUESTIONS_BASE_URL}${generator.name}/${seed}.json`;
                try {
                    const response = await fetch(url);
                    if (response.ok) {
                        const question = await response.json();
                        question.generator_name = generator.name;
                        question.generator_file = generator.file;
                        question.url = url;
                        question.seed = seed; // Ensure seed is set
                        allQuestions.push(question);
                    }
                } catch (e) {
                    console.error(`Failed to load ${generator.name}/${seed}:`, e);
                }
            }
        }
        
        // Count successful and failed questions
        const successCount = allQuestions.filter(q => q.success !== false).length;
        const failedCount = allQuestions.filter(q => q.success === false).length;
        
        console.log(`Loaded ${allQuestions.length} questions (${successCount} successful, ${failedCount} failed)`);
        
        // Apply initial filters and display
        applyFilters();
        
        // Update button with statistics
        btn.innerHTML = `✓ ${allQuestions.length} questions chargées (${successCount} réussies, ${failedCount} échouées)`;
        btn.classList.add('btn-success');
        setTimeout(() => {
            btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>Recharger';
            btn.classList.remove('btn-success');
            btn.disabled = false;
        }, 3000);
        
    } catch (error) {
        console.error('Error loading questions:', error);
        container.innerHTML = `
            <div class="alert alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Erreur lors du chargement des questions: ${error.message}</span>
            </div>
        `;
        btn.innerHTML = 'Réessayer';
        btn.disabled = false;
    } finally {
        loading.classList.add('hidden');
    }
}

/**
 * Apply filters and update display
 */
function applyFilters() {
    // Filter by generator, status, and search term
    filteredQuestions = allQuestions.filter(q => {
        // Filter by generator
        if (currentGenerator !== 'all' && q.generator_name !== currentGenerator) {
            return false;
        }
        
        // Filter by status
        if (currentStatus !== 'all') {
            const isSuccess = q.success !== false;
            if (currentStatus === 'success' && !isSuccess) return false;
            if (currentStatus === 'failed' && isSuccess) return false;
        }
        
        // Filter by search term
        if (searchTerm) {
            const searchLower = searchTerm.toLowerCase();
            const searchableText = [
                q.statement || '',
                q.generator_name || '',
                q.error || '',
                q.error_type || ''
            ].join(' ').toLowerCase();
            
            return searchableText.includes(searchLower);
        }
        
        return true;
    });
    
    // Reset to page 1 when filters change
    currentPage = 1;
    displayQuestions();
}

/**
 * Display questions for current page
 */
function displayQuestions() {
    const container = document.getElementById('questions-container');
    const start = (currentPage - 1) * questionsPerPage;
    const end = start + questionsPerPage;
    const pageQuestions = filteredQuestions.slice(start, end);
    
    if (pageQuestions.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>Aucune question trouvée. Cliquez sur "Charger toutes les questions" pour commencer.</span>
            </div>
        `;
        updatePagination();
        return;
    }
    
    // Render questions
    container.innerHTML = pageQuestions.map((q, idx) => {
        const isSuccess = q.success !== false;
        const cardClass = isSuccess ? 'bg-base-100' : 'bg-error/10 border-error/20';
        const badgeClass = isSuccess ? 'badge-outline' : 'badge-error';
        
        return `
        <div class="card ${cardClass} shadow-xl">
            <div class="card-body">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="card-title text-sm">
                        Question ${start + idx + 1} / ${filteredQuestions.length}
                        ${!isSuccess ? '<span class="text-error ml-2">[Échec]</span>' : ''}
                    </h3>
                    <div class="badge ${badgeClass}">${q.generator_name || 'Unknown'}</div>
                </div>
                
                <div class="divider my-2"></div>
                
                <div class="prose max-w-none">
                    ${isSuccess ? `
                        <div class="text-lg mb-3">
                            ${q.statement || 'Pas d\'énoncé disponible'}
                        </div>
                        
                        ${q.answer ? `
                            <div class="alert alert-success">
                                <div>
                                    <div class="font-bold mb-1">Réponse:</div>
                                    <div class="font-mono text-lg">
                                        ${typeof q.answer === 'object' ? 
                                            (q.answer.simplified_latex || q.answer.latex || JSON.stringify(q.answer)) : 
                                            q.answer}
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                    ` : `
                        <div class="alert alert-error mb-3">
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                                <div class="font-bold">Erreur de génération</div>
                                <div class="text-sm mt-1">${q.error || 'Erreur inconnue'}</div>
                                ${q.error_type ? `<div class="text-xs mt-1 opacity-70">Type: ${q.error_type}</div>` : ''}
                            </div>
                        </div>
                        
                        ${q.traceback ? `
                            <details class="collapse collapse-arrow bg-base-200 mt-3">
                                <summary class="collapse-title text-sm font-medium">
                                    Traceback complet
                                </summary>
                                <div class="collapse-content">
                                    <pre class="text-xs overflow-x-auto text-error">${q.traceback}</pre>
                                </div>
                            </details>
                        ` : ''}
                        
                        ${q.stdout ? `
                            <details class="collapse collapse-arrow bg-base-200 mt-2">
                                <summary class="collapse-title text-sm font-medium">
                                    Sortie standard
                                </summary>
                                <div class="collapse-content">
                                    <pre class="text-xs overflow-x-auto">${q.stdout}</pre>
                                </div>
                            </details>
                        ` : ''}
                        
                        ${q.stderr ? `
                            <details class="collapse collapse-arrow bg-base-200 mt-2">
                                <summary class="collapse-title text-sm font-medium">
                                    Sortie d'erreur
                                </summary>
                                <div class="collapse-content">
                                    <pre class="text-xs overflow-x-auto text-warning">${q.stderr}</pre>
                                </div>
                            </details>
                        ` : ''}
                    `}
                    
                    ${q.components ? `
                        <details class="collapse collapse-arrow bg-base-200 mt-3">
                            <summary class="collapse-title text-sm font-medium">
                                Détails de génération
                            </summary>
                            <div class="collapse-content">
                                <pre class="text-xs overflow-x-auto">${JSON.stringify(q.components, null, 2)}</pre>
                            </div>
                        </details>
                    ` : ''}
                </div>
                
                <div class="card-actions justify-end mt-4">
                    <div class="text-xs text-gray-500">
                        Seed: ${q.seed !== undefined ? q.seed : 'N/A'} | 
                        ${q.beacon ? `Beacon: ${q.beacon} | ` : ''}
                        ${isSuccess ? 'Succès ✓' : 'Échec ✗'}
                    </div>
                </div>
            </div>
        </div>
        `;
    }).join('');
    
    updatePagination();
    
    // Trigger math rendering
    document.dispatchEvent(new Event('questions-rendered'));
}

/**
 * Update pagination controls
 */
function updatePagination() {
    const container = document.getElementById('pagination-container');
    const totalPages = Math.ceil(filteredQuestions.length / questionsPerPage);
    
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    // Create pagination HTML
    let paginationHtml = '<div class="join">';
    
    // Previous button
    paginationHtml += `
        <button class="join-item btn ${currentPage === 1 ? 'btn-disabled' : ''}" 
                onclick="preGeneratedViewer.changePage(${currentPage - 1})">«</button>
    `;
    
    // Page numbers
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, startPage + 4);
    
    if (endPage - startPage < 4) {
        startPage = Math.max(1, endPage - 4);
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHtml += `
            <button class="join-item btn ${i === currentPage ? 'btn-active' : ''}" 
                    onclick="preGeneratedViewer.changePage(${i})">${i}</button>
        `;
    }
    
    // Next button
    paginationHtml += `
        <button class="join-item btn ${currentPage === totalPages ? 'btn-disabled' : ''}" 
                onclick="preGeneratedViewer.changePage(${currentPage + 1})">»</button>
    `;
    
    paginationHtml += '</div>';
    
    // Add page info
    paginationHtml += `
        <div class="mt-4 text-center text-sm text-gray-600">
            Page ${currentPage} sur ${totalPages} 
            (${filteredQuestions.length} questions trouvées)
        </div>
    `;
    
    container.innerHTML = paginationHtml;
}

/**
 * Change page
 */
export function changePage(page) {
    const totalPages = Math.ceil(filteredQuestions.length / questionsPerPage);
    if (page < 1 || page > totalPages) return;
    
    currentPage = page;
    displayQuestions();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Handle generator change
 */
function handleGeneratorChange(e) {
    currentGenerator = e.target.value;
    applyFilters();
}

/**
 * Handle status change
 */
function handleStatusChange(e) {
    currentStatus = e.target.value;
    applyFilters();
}

/**
 * Handle per page change
 */
function handlePerPageChange(e) {
    questionsPerPage = parseInt(e.target.value);
    currentPage = 1;
    displayQuestions();
}

/**
 * Handle search
 */
function handleSearch(e) {
    searchTerm = e.target.value;
    applyFilters();
}

// Export the module
const preGeneratedViewer = {
    init,
    changePage,
    loadAllQuestions
};

// Make it available globally for onclick handlers
window.preGeneratedViewer = preGeneratedViewer;

export default preGeneratedViewer;
