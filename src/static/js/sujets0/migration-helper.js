/**
 * Migration Helper - Allows switching between old and refactored versions
 * This helps with testing and gradual migration
 */

export class MigrationHelper {
    constructor() {
        this.useRefactored = this.checkRefactoredMode();
    }
    
    /**
     * Check if refactored mode should be used
     */
    checkRefactoredMode() {
        // Check URL parameter
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('refactored')) {
            const value = urlParams.get('refactored');
            return value !== 'false' && value !== '0';
        }
        
        // Check localStorage preference
        const stored = localStorage.getItem('sujets0_use_refactored');
        if (stored !== null) {
            return stored === 'true';
        }
        
        // Default to refactored for new features
        return true;
    }
    
    /**
     * Get the appropriate module path
     */
    getModulePath(moduleName) {
        const modules = {
            'main': {
                old: '/static/js/sujets0/sujets0-main.js',
                new: '/static/js/sujets0/sujets0-main-refactored.js'
            },
            'papyrus': {
                old: '/static/js/sujets0/index-papyrus.js',
                new: '/static/js/sujets0/index-papyrus-refactored.js'
            }
        };
        
        const module = modules[moduleName];
        if (!module) {
            throw new Error(`Unknown module: ${moduleName}`);
        }
        
        return this.useRefactored ? module.new : module.old;
    }
    
    /**
     * Get the appropriate template path
     */
    getTemplatePath(templateName) {
        const templates = {
            'generate-content': {
                old: 'sujets0/generate-content.html',
                new: 'sujets0/generate-content-refactored.html'
            }
        };
        
        const template = templates[templateName];
        if (!template) {
            throw new Error(`Unknown template: ${templateName}`);
        }
        
        return this.useRefactored ? template.new : template.old;
    }
    
    /**
     * Switch to refactored version
     */
    enableRefactored() {
        localStorage.setItem('sujets0_use_refactored', 'true');
        console.log('Switched to refactored version. Reloading...');
        window.location.reload();
    }
    
    /**
     * Switch to old version
     */
    disableRefactored() {
        localStorage.setItem('sujets0_use_refactored', 'false');
        console.log('Switched to old version. Reloading...');
        window.location.reload();
    }
    
    /**
     * Toggle between versions
     */
    toggle() {
        if (this.useRefactored) {
            this.disableRefactored();
        } else {
            this.enableRefactored();
        }
    }
    
    /**
     * Add version switcher UI
     */
    addVersionSwitcher() {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            background: white;
            padding: 10px;
            border: 2px solid #333;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            font-family: monospace;
            font-size: 12px;
        `;
        
        container.innerHTML = `
            <div style="margin-bottom: 5px;">
                <strong>Version:</strong> ${this.useRefactored ? 'REFACTORED' : 'ORIGINAL'}
            </div>
            <button id="version-toggle" style="
                padding: 5px 10px;
                background: ${this.useRefactored ? '#10b981' : '#ef4444'};
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            ">
                Switch to ${this.useRefactored ? 'Original' : 'Refactored'}
            </button>
        `;
        
        document.body.appendChild(container);
        
        document.getElementById('version-toggle').addEventListener('click', () => {
            this.toggle();
        });
    }
    
    /**
     * Load the appropriate template content
     */
    async loadTemplateContent() {
        const container = document.getElementById('generate-content-container');
        if (!container) {
            console.warn('Template container not found');
            return;
        }
        
        try {
            // Determine which template to load
            const templatePath = this.useRefactored ? 
                '/static/templates/generate-content-refactored.html' :
                '/static/templates/generate-content-original.html';
            
            // For now, we'll inject the content directly
            // In production, this would be loaded from the server
            if (this.useRefactored) {
                // Load refactored template content
                const response = await fetch('/sujets0/template-content?version=refactored');
                if (response.ok) {
                    const html = await response.text();
                    container.innerHTML = html;
                } else {
                    // Fallback: inject the refactored template inline
                    this.injectRefactoredTemplate(container);
                }
            } else {
                // Load original template content
                const response = await fetch('/sujets0/template-content?version=original');
                if (response.ok) {
                    const html = await response.text();
                    container.innerHTML = html;
                } else {
                    // Fallback: keep the original content
                    console.log('Using original template (already loaded)');
                }
            }
        } catch (error) {
            console.error('Failed to load template:', error);
            // Fallback to inline injection
            if (this.useRefactored) {
                this.injectRefactoredTemplate(container);
            }
        }
    }
    
    /**
     * Inject refactored template inline (fallback)
     */
    injectRefactoredTemplate(container) {
        // This is a simplified version - in production, load from server
        container.innerHTML = `
            <div class="alert alert-info mb-4">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>Version refactorisée chargée. Les templates seront chargés dynamiquement.</span>
            </div>
        `;
        
        // Load the actual refactored content via script
        import('/static/js/sujets0/template-loader.js').then(module => {
            module.loadRefactoredTemplate(container);
        });
    }
    
    /**
     * Log migration status
     */
    logStatus() {
        console.group('🔄 Migration Status');
        console.log(`Using ${this.useRefactored ? 'REFACTORED' : 'ORIGINAL'} version`);
        console.log('To switch versions:');
        console.log('  - Add ?refactored=true to URL for refactored version');
        console.log('  - Add ?refactored=false to URL for original version');
        console.log('  - Or call window.migrationHelper.toggle()');
        console.groupEnd();
    }
}

// Create global instance
window.migrationHelper = new MigrationHelper();

// Add switcher UI in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.migrationHelper.addVersionSwitcher();
}

// Log status
window.migrationHelper.logStatus();

export default window.migrationHelper;
