/**
 * Unified Progress Component for Sujets0
 * Single progress indicator that adapts to different operations
 */

export class UnifiedProgress {
    constructor(containerId = 'unified-status-bar') {
        this.containerId = containerId;
        this.container = null;
        this.currentOperation = null;
        this.startTime = null;
        this.abortController = null;
        
        this.initialize();
    }
    
    /**
     * Initialize the progress component
     */
    initialize() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) {
            console.warn(`Progress container #${this.containerId} not found`);
            return;
        }
        
        // Set initial state
        this.reset();
    }
    
    /**
     * Start a new operation
     */
    startOperation(type, config = {}) {
        this.currentOperation = type;
        this.startTime = Date.now();
        this.abortController = new AbortController();
        
        const operations = {
            'generation': {
                title: 'Génération des exercices',
                icon: '🎲',
                color: 'primary'
            },
            'conversion': {
                title: 'Conversion des graphiques',
                icon: '📊',
                color: 'info'
            },
            'printing': {
                title: 'Préparation de l\'impression',
                icon: '🖨️',
                color: 'secondary'
            },
            'printing-all': {
                title: 'Impression de toutes les copies',
                icon: '📑',
                color: 'secondary'
            },
            'teacher-manifest': {
                title: 'Génération de la fiche enseignant',
                icon: '📊',
                color: 'accent'
            },
            'loading': {
                title: 'Chargement',
                icon: '⏳',
                color: 'neutral'
            }
        };
        
        const operation = operations[type] || operations.loading;
        const { max = 100, detail = '' } = config;
        
        this.render({
            title: operation.title,
            icon: operation.icon,
            color: operation.color,
            progress: 0,
            max: max,
            detail: detail,
            showTime: true,
            showCancel: config.cancellable || false
        });
        
        // Show the container
        if (this.container) {
            this.container.style.display = 'block';
            this.container.classList.remove('opacity-0');
            this.container.classList.add('opacity-100');
        }
    }
    
    /**
     * Update progress
     */
    update(progress, detail = '') {
        if (!this.container || !this.currentOperation) return;
        
        const progressBar = this.container.querySelector('.progress');
        const detailElement = this.container.querySelector('[data-progress-detail]');
        const percentElement = this.container.querySelector('[data-progress-percent]');
        
        if (progressBar) {
            progressBar.value = progress;
            
            // Update percentage display
            if (percentElement && progressBar.max > 0) {
                const percent = Math.round((progress / progressBar.max) * 100);
                percentElement.textContent = `${percent}%`;
            }
        }
        
        if (detailElement && detail) {
            detailElement.textContent = detail;
        }
        
        this.updateElapsedTime();
    }
    
    /**
     * Complete the current operation
     */
    complete(message = '', autoHide = true) {
        if (!this.container) return;
        
        const titleElement = this.container.querySelector('[data-progress-title]');
        const progressBar = this.container.querySelector('.progress');
        const iconElement = this.container.querySelector('[data-progress-icon]');
        
        if (titleElement) {
            titleElement.textContent = message || 'Terminé!';
        }
        
        if (progressBar) {
            progressBar.value = progressBar.max;
            progressBar.classList.add('progress-success');
        }
        
        if (iconElement) {
            iconElement.textContent = '✅';
        }
        
        // Auto-hide after delay
        if (autoHide) {
            setTimeout(() => this.hide(), 3000);
        }
        
        this.currentOperation = null;
    }
    
    /**
     * Show error state
     */
    error(message = '', details = '') {
        if (!this.container) return;
        
        const titleElement = this.container.querySelector('[data-progress-title]');
        const detailElement = this.container.querySelector('[data-progress-detail]');
        const progressBar = this.container.querySelector('.progress');
        const iconElement = this.container.querySelector('[data-progress-icon]');
        
        if (titleElement) {
            titleElement.textContent = message || 'Erreur!';
            titleElement.classList.add('text-error');
        }
        
        if (detailElement && details) {
            detailElement.textContent = details;
            detailElement.classList.add('text-error');
        }
        
        if (progressBar) {
            progressBar.classList.add('progress-error');
        }
        
        if (iconElement) {
            iconElement.textContent = '❌';
        }
        
        this.currentOperation = null;
    }
    
    /**
     * Reset to initial state
     */
    reset() {
        if (!this.container) return;
        
        this.currentOperation = null;
        this.startTime = null;
        
        this.render({
            title: 'En attente...',
            icon: '⏸️',
            color: 'neutral',
            progress: 0,
            max: 100,
            detail: '',
            showTime: false,
            showCancel: false
        });
        
        this.hide();
    }
    
    /**
     * Hide the progress bar
     */
    hide() {
        if (!this.container) return;
        
        this.container.classList.remove('opacity-100');
        this.container.classList.add('opacity-0');
        
        setTimeout(() => {
            if (this.container) {
                this.container.style.display = 'none';
            }
        }, 300);
    }
    
    /**
     * Show the progress bar
     */
    show() {
        if (!this.container) return;
        
        this.container.style.display = 'block';
        setTimeout(() => {
            this.container.classList.remove('opacity-0');
            this.container.classList.add('opacity-100');
        }, 10);
    }
    
    /**
     * Update elapsed time display
     */
    updateElapsedTime() {
        if (!this.startTime || !this.container) return;
        
        const timeElement = this.container.querySelector('[data-progress-time]');
        if (!timeElement) return;
        
        const elapsed = Math.round((Date.now() - this.startTime) / 1000);
        
        if (elapsed < 60) {
            timeElement.textContent = `${elapsed}s`;
        } else {
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            timeElement.textContent = `${minutes}m ${seconds}s`;
        }
    }
    
    /**
     * Render the progress component
     */
    render(config) {
        if (!this.container) return;
        
        const {
            title = '',
            icon = '',
            color = 'primary',
            progress = 0,
            max = 100,
            detail = '',
            showTime = true,
            showCancel = false,
            showPercent = true
        } = config;
        
        this.container.innerHTML = `
            <div class="card bg-base-100 shadow-sm transition-all duration-300">
                <div class="card-body py-3">
                    <div class="flex justify-between items-center mb-2">
                        <div class="flex items-center gap-2">
                            <span data-progress-icon class="text-lg">${icon}</span>
                            <span data-progress-title class="text-sm font-medium">${title}</span>
                            ${detail ? `<span data-progress-detail class="text-xs opacity-70">${detail}</span>` : ''}
                        </div>
                        <div class="flex items-center gap-3">
                            ${showPercent ? '<span data-progress-percent class="text-xs font-mono opacity-60">0%</span>' : ''}
                            ${showTime ? '<span data-progress-time class="text-xs opacity-60">0s</span>' : ''}
                            ${showCancel ? '<button data-progress-cancel class="btn btn-ghost btn-xs">✕</button>' : ''}
                        </div>
                    </div>
                    <progress class="progress progress-${color} w-full transition-all duration-300" 
                              value="${progress}" 
                              max="${max}"></progress>
                </div>
            </div>
        `;
        
        // Attach cancel handler if needed
        if (showCancel) {
            const cancelBtn = this.container.querySelector('[data-progress-cancel]');
            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => this.cancel());
            }
        }
    }
    
    /**
     * Cancel current operation
     */
    cancel() {
        if (this.abortController) {
            this.abortController.abort();
        }
        
        this.error('Opération annulée');
        setTimeout(() => this.reset(), 2000);
    }
    
    /**
     * Get abort signal for async operations
     */
    getAbortSignal() {
        return this.abortController ? this.abortController.signal : null;
    }
}

// Create singleton instance
let progressInstance = null;

export function getProgressManager() {
    if (!progressInstance) {
        progressInstance = new UnifiedProgress();
        
        // Make available globally for debugging
        if (window.location.hostname === 'localhost') {
            window.sujets0Progress = progressInstance;
        }
    }
    return progressInstance;
}
