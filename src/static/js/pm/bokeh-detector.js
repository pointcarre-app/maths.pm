/**
 * Bokeh Detection and Verification Script
 * 
 * This script handles Bokeh library detection and verification for PM pages
 * that include Bokeh dependencies. It's loaded separately to avoid template
 * formatting issues with inline JavaScript.
 */

class BokehDetector {
    constructor() {
        this.pmDependencies = null;
        this.initialized = false;
    }

    /**
     * Initialize the detector with PM dependencies
     * @param {Array} dependencies - Array of JS dependencies from PM
     */
    init(dependencies) {
        this.pmDependencies = dependencies || [];
        this.initialized = true;
        this.checkBokehDependency();
    }

    /**
     * Check if Bokeh is expected based on dependencies
     * @returns {boolean} True if Bokeh should be loaded
     */
    isBokehExpected() {
        if (!this.pmDependencies) return false;
        return this.pmDependencies.some(dep => dep.includes('bokeh'));
    }

    /**
     * Verify Bokeh is properly loaded
     */
    checkBokehDependency() {
        if (!this.isBokehExpected()) {
            console.debug('[PM] No Bokeh dependency expected');
            return;
        }

        // Check on DOM ready
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            this.verifyBokeh();
        } else {
            window.addEventListener('DOMContentLoaded', () => this.verifyBokeh(), {
                once: true
            });
        }
    }

    /**
     * Verify Bokeh is loaded and log status
     */
    verifyBokeh() {
        if (window.Bokeh) {
            console.log('[PM] BokehJS loaded successfully:', window.Bokeh.version);
            
            // Dispatch custom event for other scripts
            window.dispatchEvent(new CustomEvent('pm:bokeh-ready', {
                detail: { version: window.Bokeh.version }
            }));
        } else {
            console.error('[PM] BokehJS expected but not loaded!');
            
            // Try to wait a bit more and check again
            setTimeout(() => {
                if (window.Bokeh) {
                    console.log('[PM] BokehJS loaded (delayed):', window.Bokeh.version);
                    window.dispatchEvent(new CustomEvent('pm:bokeh-ready', {
                        detail: { version: window.Bokeh.version }
                    }));
                } else {
                    console.warn('[PM] BokehJS still not available after delay');
                    window.dispatchEvent(new CustomEvent('pm:bokeh-failed'));
                }
            }, 1000);
        }
    }

    /**
     * Get Bokeh status information
     * @returns {Object} Status object with loaded state and version
     */
    getStatus() {
        return {
            expected: this.isBokehExpected(),
            loaded: !!window.Bokeh,
            version: window.Bokeh ? window.Bokeh.version : null,
            dependencies: this.pmDependencies
        };
    }
}

// Create global instance
window.pmBokehDetector = new BokehDetector();

// Auto-detect from DOM script tags when loaded
function autoDetectFromDOM() {
    const scripts = Array.from(document.querySelectorAll('script[src]'));
    const jsDependencies = scripts.map(script => script.src).filter(src => src);
    
    if (jsDependencies.length > 0) {
        console.debug('[PM] Bokeh detector auto-detected dependencies from DOM:', jsDependencies.length);
        window.pmBokehDetector.init(jsDependencies);
    }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    autoDetectFromDOM();
} else {
    window.addEventListener('DOMContentLoaded', autoDetectFromDOM, { once: true });
}

// Also initialize if PM dependencies are available in global scope
if (window.pmJsDependencies) {
    window.pmBokehDetector.init(window.pmJsDependencies);
}

export default BokehDetector;
