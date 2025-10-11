/**
 * AccessibilityManager - Centralized state management for themes, fonts, and UI settings
 * Ensures consistency across all UI controls and persists settings in localStorage
 */
class AccessibilityManager {
    constructor() {
        // Priority: localStorage > current DOM > default
        // This ensures we restore the user's saved preference on page refresh
        const savedTheme = localStorage.getItem('theme');
        const currentTheme = document.documentElement.getAttribute('data-theme');
        
        // Initialize state from localStorage first, then fall back to DOM or defaults
        this.state = {
            theme: savedTheme || currentTheme || 'anchor',
            fontType: localStorage.getItem('font-type') || 'default',
            width: localStorage.getItem('pm-width') || '640px'
        };
        
        // If we have a saved theme that differs from current DOM, we'll apply it in init()
        
        // Track if theme is enforced (e.g., for PDF generation)
        this.enforcedTheme = null;
        
        // Subscribers for state changes
        this.listeners = [];
        
        // Font configurations using CSS variables from root.css
        this.fontConfigs = {
            'default': {
                '--font-sans': 'var(--font-lexend)',
                '--font-body': 'var(--font-lexend)',
                '--font-heading': 'var(--font-spectral)'
            },
            'dyslexic': {
                '--font-sans': 'var(--font-opendyslexic-regular)',
                '--font-body': 'var(--font-opendyslexic-regular)',
                '--font-heading': 'var(--font-opendyslexic-regular)'
            }
        };
        
        // Initialize the manager
        this.init();
    }
    
    init() {
        // Apply initial state - ALWAYS apply what's in our state (from localStorage)
        this.applyTheme(this.state.theme);
        this.applyFont(this.state.fontType);
        this.applyWidth(this.state.width);
        
        // Ensure localStorage is in sync with what we just applied
        localStorage.setItem('theme', this.state.theme);
        localStorage.setItem('font-type', this.state.fontType);
        localStorage.setItem('pm-width', this.state.width);
        
        // Set up event delegation for all controls
        this.setupEventDelegation();
        
        // Update UI to reflect initial state
        // Use a small delay to ensure all DOM elements are ready
        this.updateAllUI();
        
        // Also update after a small delay to catch any late-loading elements
        setTimeout(() => {
            this.updateAllUI();
        }, 100);
        
        // Listen for system theme changes
        this.setupSystemThemeListener();
    }
    
    // ===== THEME MANAGEMENT =====
    
    setTheme(theme) {
        // Don't change if theme is enforced
        if (this.enforcedTheme) {
            console.log('Theme is enforced as:', this.enforcedTheme);
            return false;
        }
        
        console.log('Setting theme from', this.state.theme, 'to', theme);
        
        if (this.state.theme !== theme) {
            this.state.theme = theme;
            this.applyTheme(theme);
            localStorage.setItem('theme', theme);
            
            // Force immediate UI update
            requestAnimationFrame(() => {
                this.updateAllUI();
            });
            
            this.notifyListeners('theme', theme);
        } else {
            console.log('Theme already set to:', theme);
            // Even if theme is the same, update UI to ensure consistency
            this.updateAllUI();
        }
        return true;
    }
    
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }
    
    enforceTheme(theme, message = null) {
        this.enforcedTheme = theme;
        this.setTheme(theme);
        this.disableThemeControls();
        
        if (message) {
            this.showToast(message, 'info');
        }
    }
    
    clearEnforcedTheme() {
        this.enforcedTheme = null;
        this.enableThemeControls();
    }
    
    // ===== FONT MANAGEMENT =====
    
    setFont(fontType) {
        console.log('Setting font from', this.state.fontType, 'to', fontType);
        
        if (this.state.fontType !== fontType) {
            this.state.fontType = fontType;
            this.applyFont(fontType);
            localStorage.setItem('font-type', fontType);
            
            // Force immediate UI update
            requestAnimationFrame(() => {
                this.updateAllUI();
            });
            
            this.notifyListeners('font', fontType);
        } else {
            console.log('Font already set to:', fontType);
            // Even if font is the same, update UI to ensure consistency
            this.updateAllUI();
        }
    }
    
    applyFont(fontType) {
        const config = this.fontConfigs[fontType];
        if (config) {
            Object.entries(config).forEach(([property, value]) => {
                document.documentElement.style.setProperty(property, value);
            });
        }
    }
    
    // ===== WIDTH MANAGEMENT =====
    
    setWidth(width) {
        if (this.state.width !== width) {
            this.state.width = width;
            this.applyWidth(width);
            localStorage.setItem('pm-width', width);
            this.updateAllUI();
            this.notifyListeners('width', width);
        }
    }
    
    applyWidth(width) {
        const pmWrapper = document.getElementById('pm-wrapper-max-width');
        if (pmWrapper) {
            pmWrapper.style.maxWidth = width;
        }
    }
    
    // ===== UI UPDATE METHODS =====
    
    updateAllUI() {
        this.updateThemeUI();
        this.updateFontUI();
        this.updateWidthUI();
    }
    
    updateThemeUI() {
        console.log('Updating theme UI for:', this.state.theme);
        
        // Define contrast themes
        const contrastThemes = ['anchor', 'reinforced-contrast', 'inversed-contrast'];
        const isContrastTheme = contrastThemes.includes(this.state.theme);
        
        // First, handle the "other theme" radio button for contrast section
        const otherThemeRadio = document.querySelector('[data-contrast-other="true"]');
        if (otherThemeRadio) {
            // Always keep it disabled
            otherThemeRadio.disabled = true;
            
            if (!isContrastTheme) {
                // Current theme is not a contrast theme, so check the "other" option
                otherThemeRadio.checked = true;
                console.log('Checking "other theme" radio');
            } else {
                // Current theme is a contrast theme, so uncheck it
                otherThemeRadio.checked = false;
                console.log('Unchecking "other theme" radio');
            }
        }
        
        // Update all theme-related UI elements
        const themeElements = document.querySelectorAll('[data-theme-selector]');
        console.log('Found', themeElements.length, 'theme selector elements');
        
        themeElements.forEach(element => {
            const theme = element.dataset.themeSelector;
            
            if (element.type === 'radio' || element.type === 'checkbox') {
                // Only check the radio if it matches current theme
                const shouldCheck = (theme === this.state.theme);
                element.checked = shouldCheck;
                if (shouldCheck) {
                    console.log('Checking radio/checkbox for theme:', theme);
                }
            } else if (element.tagName === 'BUTTON') {
                // Add active class to current theme button
                if (theme === this.state.theme) {
                    element.classList.add('btn-active');
                    console.log('Adding btn-active to button for theme:', theme);
                } else {
                    element.classList.remove('btn-active');
                }
            }
            
            // Disable if theme is enforced
            if (this.enforcedTheme && element.tagName === 'BUTTON') {
                element.disabled = true;
                element.classList.add('btn-disabled');
            }
        });
    }
    
    updateFontUI() {
        console.log('Updating font UI for:', this.state.fontType);
        
        // Update all font-related UI elements
        const fontElements = document.querySelectorAll('[data-font-selector]');
        console.log('Found', fontElements.length, 'font selector elements');
        
        fontElements.forEach(element => {
            const fontType = element.dataset.fontSelector;
            
            if (element.type === 'radio' || element.type === 'checkbox') {
                // Set checked state for radio/checkbox inputs
                const shouldCheck = (fontType === this.state.fontType);
                element.checked = shouldCheck;
                if (shouldCheck) {
                    console.log('Checking radio/checkbox for font:', fontType);
                }
            } else if (element.tagName === 'BUTTON') {
                // Add active class to current font button
                if (fontType === this.state.fontType) {
                    element.classList.add('btn-active');
                    console.log('Adding btn-active to button for font:', fontType);
                } else {
                    element.classList.remove('btn-active');
                }
            }
        });
    }
    
    updateWidthUI() {
        // Update all width-related UI elements
        document.querySelectorAll('[data-width-selector]').forEach(element => {
            const width = element.dataset.widthSelector;
            
            if (element.tagName === 'BUTTON') {
                // Add active class to current width button
                if (width === this.state.width) {
                    element.classList.add('btn-active');
                } else {
                    element.classList.remove('btn-active');
                }
            }
        });
    }
    
    // ===== EVENT HANDLING =====
    
    setupEventDelegation() {
        // Use event delegation for all controls
        document.addEventListener('click', (e) => {
            // Theme selector - handle both buttons and radio labels
            const themeSelector = e.target.closest('[data-theme-selector]');
            if (themeSelector && themeSelector.tagName === 'BUTTON') {
                e.preventDefault();
                console.log('Theme button clicked:', themeSelector.dataset.themeSelector);
                this.setTheme(themeSelector.dataset.themeSelector);
            }
            
            // Font selector - handle buttons only
            const fontSelector = e.target.closest('[data-font-selector]');
            if (fontSelector && fontSelector.tagName === 'BUTTON') {
                e.preventDefault();
                console.log('Font button clicked:', fontSelector.dataset.fontSelector);
                this.setFont(fontSelector.dataset.fontSelector);
            }
            
            // Width selector
            const widthSelector = e.target.closest('[data-width-selector]');
            if (widthSelector) {
                e.preventDefault();
                console.log('Width button clicked:', widthSelector.dataset.widthSelector);
                this.setWidth(widthSelector.dataset.widthSelector);
            }
        });
        
        // Handle radio button changes (for radio inputs specifically)
        document.addEventListener('change', (e) => {
            if (e.target.matches('[data-theme-selector][type="radio"]')) {
                console.log('Theme radio changed:', e.target.dataset.themeSelector);
                this.setTheme(e.target.dataset.themeSelector);
            }
            
            if (e.target.matches('[data-font-selector][type="radio"]')) {
                console.log('Font radio changed:', e.target.dataset.fontSelector);
                this.setFont(e.target.dataset.fontSelector);
            }
        });
    }
    
    setupSystemThemeListener() {
        // Listen for system theme preference changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            // Only apply system preference if user has never selected a theme
            // Once a user selects a theme, we respect their choice over system preference
            if (!localStorage.getItem('theme') && !this.enforcedTheme) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
    
    // ===== CONTROL MANAGEMENT =====
    
    disableThemeControls() {
        document.querySelectorAll('[data-theme-selector]').forEach(element => {
            element.disabled = true;
            if (element.tagName === 'BUTTON') {
                element.classList.add('btn-disabled');
            }
        });
    }
    
    enableThemeControls() {
        document.querySelectorAll('[data-theme-selector]').forEach(element => {
            element.disabled = false;
            if (element.tagName === 'BUTTON') {
                element.classList.remove('btn-disabled');
            }
        });
    }
    
    // ===== OBSERVER PATTERN =====
    
    subscribe(callback) {
        this.listeners.push(callback);
        // Return unsubscribe function
        return () => {
            const index = this.listeners.indexOf(callback);
            if (index > -1) {
                this.listeners.splice(index, 1);
            }
        };
    }
    
    notifyListeners(type, value) {
        this.listeners.forEach(callback => {
            try {
                callback(type, value);
            } catch (error) {
                console.error('Error in accessibility listener:', error);
            }
        });
    }
    
    // ===== UTILITY METHODS =====
    
    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;
        
        // Clear existing toasts
        toastContainer.innerHTML = '';
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        
        const messageSpan = document.createElement('span');
        messageSpan.textContent = message;
        
        alert.appendChild(messageSpan);
        toastContainer.appendChild(alert);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            toastContainer.innerHTML = '';
        }, 3000);
    }
    
    // ===== PUBLIC API =====
    
    getState() {
        return { ...this.state };
    }
    
    isThemeEnforced() {
        return this.enforcedTheme !== null;
    }
    
    getCurrentTheme() {
        return this.state.theme;
    }
    
    getCurrentFont() {
        return this.state.fontType;
    }
    
    getCurrentWidth() {
        return this.state.width;
    }
}

// Initialize the manager when DOM is ready
let accessibilityManager = null;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        accessibilityManager = new AccessibilityManager();
        
        // Make it globally available for debugging
        window.accessibilityManager = accessibilityManager;
        
        // Check for special pages that need theme enforcement
        const path = window.location.pathname;
        if (path === '/sujets0' || 
            path === '/sujets0/teacher_manifest' || 
            path === '/maths.pm/sujets0/' || 
            path === '/maths.pm/sujets0/teacher_manifest') {
            
            const currentTheme = accessibilityManager.getCurrentTheme();
            if (currentTheme !== 'anchor') {
                accessibilityManager.enforceTheme('anchor', 'Le thème pour la génération de PDF est forcément anchor.');
            }
        }
    });
} else {
    // DOM already loaded
    accessibilityManager = new AccessibilityManager();
    window.accessibilityManager = accessibilityManager;
}

// Export for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AccessibilityManager;
}
