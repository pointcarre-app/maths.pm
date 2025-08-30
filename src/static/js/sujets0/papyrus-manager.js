/**
 * Papyrus Manager - Robust integration with Papyrus library
 * Handles initialization, rendering, and printing with proper fallbacks
 */

import { generatePages } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/core/preview/index.js';
import { printPage } from 'https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/core/print-manager.js';
import { isSafari } from './index-svg-converter.js';
import { getStateManager } from './state-manager.js';

export class PapyrusManager {
    constructor() {
        this.ready = false;
        this.renderFunction = null;
        this.initialized = false;
        this.initPromise = null;
    }
    
    /**
     * Initialize Papyrus and wait for it to be ready
     */
    async initialize() {
        // Prevent multiple initializations
        if (this.initialized) return true;
        if (this.initPromise) return this.initPromise;
        
        this.initPromise = this._doInitialize();
        return this.initPromise;
    }
    
    async _doInitialize() {
        try {
            console.log('Initializing Papyrus Manager...');
            
            // Wait for Papyrus to load
            const loaded = await this.waitForPapyrus();
            
            if (!loaded) {
                console.warn('Papyrus failed to load, using fallback mode');
                this.renderFunction = this.fallbackRender.bind(this);
            } else {
                // Set up Papyrus globals if needed
                this.setupPapyrusGlobals();
                
                // Cache the render function
                this.renderFunction = window.renderContent || this.papyrusRender.bind(this);
            }
            
            this.ready = true;
            this.initialized = true;
            
            // Update state
            const state = getStateManager();
            state.updateState({ papyrusReady: true });
            
            console.log('Papyrus Manager initialized successfully');
            return true;
            
        } catch (error) {
            console.error('Failed to initialize Papyrus:', error);
            
            // Use fallback
            this.renderFunction = this.fallbackRender.bind(this);
            this.ready = true;
            this.initialized = true;
            
            return false;
        }
    }
    
    /**
     * Wait for Papyrus library to load
     */
    async waitForPapyrus(maxAttempts = 20, delay = 500) {
        for (let i = 0; i < maxAttempts; i++) {
            // Check for Papyrus globals
            if (window.DocumentManager || 
                window.renderContent || 
                typeof generatePages === 'function') {
                return true;
            }
            
            // Also check if Papyrus modules are available
            try {
                // Try to access Papyrus functions
                if (generatePages && typeof generatePages === 'function') {
                    return true;
                }
            } catch (e) {
                // Continue waiting
            }
            
            await new Promise(resolve => setTimeout(resolve, delay));
        }
        
        return false;
    }
    
    /**
     * Set up required Papyrus globals
     */
    setupPapyrusGlobals() {
        // Ensure contentModel exists
        if (!window.contentModel) {
            window.contentModel = {
                items: [],
                loadFromJSON: function(json) { 
                    this.items = Array.isArray(json) ? json : [];
                },
                updateMargins: function(margins) { 
                    this.margins = margins;
                },
                getItems: function() {
                    return this.items;
                }
            };
        }
        
        // Ensure renderContent exists
        if (!window.renderContent) {
            window.renderContent = async () => {
                if (!window.contentModel || !window.contentModel.items) {
                    console.warn('No content to render');
                    return;
                }
                
                const container = document.getElementById('pages-container');
                if (!container) {
                    console.warn('Pages container not found');
                    return;
                }
                
                // Use generatePages from Papyrus
                try {
                    const pages = await generatePages(
                        window.contentModel.items,
                        container,
                        this.getDocumentSettings()
                    );
                    return pages;
                } catch (error) {
                    console.error('Error rendering with Papyrus:', error);
                    // Fall back to direct HTML
                    return this.fallbackRender();
                }
            };
        }
        
        // Ensure getCurrentSpaceBetweenDivs exists
        if (!window.getCurrentSpaceBetweenDivs) {
            window.getCurrentSpaceBetweenDivs = () => 3; // Default 3mm spacing
        }
    }
    
    /**
     * Render content using Papyrus
     */
    async papyrusRender(papyrusJson, container) {
        if (!container) {
            container = document.getElementById('pages-container');
        }
        
        if (!container) {
            throw new Error('No container provided for rendering');
        }
        
        // Load JSON into content model
        window.contentModel.loadFromJSON(papyrusJson);
        
        // Generate pages using Papyrus
        const pages = await generatePages(
            papyrusJson,
            container,
            this.getDocumentSettings()
        );
        
        return container.innerHTML;
    }
    
    /**
     * Fallback render without Papyrus
     */
    async fallbackRender(papyrusJson, container) {
        console.warn('Using fallback renderer (Papyrus not available)');
        
        if (!container) {
            container = document.getElementById('pages-container');
        }
        
        if (!container) {
            throw new Error('No container provided for rendering');
        }
        
        // Generate HTML directly
        let html = '<div class="page-wrapper"><div class="page-preview"><div class="page-content">';
        
        const items = papyrusJson || window.contentModel?.items || [];
        
        for (const item of items) {
            if (item.html) {
                html += item.html;
            } else if (item.svg) {
                html += `<div style="${item.style || ''}">${item.svg}</div>`;
            } else if (item.pngDataUrl) {
                html += `<img src="${item.pngDataUrl}" style="${item.style || ''}" alt="Graph">`;
            } else if (item.katex) {
                // Render KaTeX if available
                if (window.katex) {
                    try {
                        const rendered = window.katex.renderToString(item.katex, {
                            throwOnError: false,
                            displayMode: item.displayMode || false
                        });
                        html += `<div style="${item.style || ''}">${rendered}</div>`;
                    } catch (e) {
                        html += `<div style="${item.style || ''}">$$${item.katex}$$</div>`;
                    }
                } else {
                    html += `<div style="${item.style || ''}">$$${item.katex}$$</div>`;
                }
            }
            
            // Add spacing
            if (item.marginBottom) {
                html += `<div style="height: ${item.marginBottom}"></div>`;
            }
            
            // Handle page breaks
            if (item.pageBreak === 'after') {
                html += '</div></div></div>';
                html += '<div class="page-wrapper"><div class="page-preview"><div class="page-content">';
            }
        }
        
        html += '</div></div></div>';
        
        container.innerHTML = html;
        return html;
    }
    
    /**
     * Render a single student's content
     */
    async renderStudent(papyrusJson, container) {
        if (!this.ready) {
            await this.initialize();
        }
        
        return this.renderFunction(papyrusJson, container);
    }
    
    /**
     * Render all students for printing (in memory, not in DOM)
     */
    async renderAllStudents(students, progressCallback) {
        if (!this.ready) {
            await this.initialize();
        }
        
        let allContent = '';
        
        // Create a temporary hidden container
        const tempContainer = document.createElement('div');
        tempContainer.style.cssText = 'position: absolute; left: -9999px; visibility: hidden; width: 210mm;';
        tempContainer.className = 'papyrus-document';
        document.body.appendChild(tempContainer);
        
        try {
            for (let i = 0; i < students.length; i++) {
                if (progressCallback) {
                    progressCallback(i + 1, students.length);
                }
                
                const student = students[i];
                if (!student || !student.papyrusJson) continue;
                
                // Clear temp container
                tempContainer.innerHTML = '';
                
                // Render student content
                await this.renderFunction(student.papyrusJson, tempContainer);
                
                // Apply Safari fixes if needed
                if (isSafari()) {
                    this.applySafariStyles(tempContainer);
                }
                
                // Accumulate HTML
                allContent += tempContainer.innerHTML;
            }
        } finally {
            // Clean up temp container
            if (tempContainer.parentNode) {
                tempContainer.parentNode.removeChild(tempContainer);
            }
        }
        
        return allContent;
    }
    
    /**
     * Print content using Papyrus print manager
     */
    print(content, styleSheet) {
        // Use Papyrus print manager which handles Safari iframe issues
        const printStyleSheet = styleSheet || 
            "/static/css/papyrus-print.css";
        
        printPage(content, printStyleSheet);
    }
    
    /**
     * Get document settings
     */
    getDocumentSettings() {
        // Check if Safari for font size adjustments
        const isSafariBrowser = isSafari();
        
        let fontSizes = {
            h1: 28,
            h2: 24,
            h3: 20,
            h4: 18,
            h5: 16,
            h6: 14,
            body: 15
        };
        
        // Safari font size adjustment
        if (isSafariBrowser) {
            fontSizes = {
                h1: 24,
                h2: 20,
                h3: 17,
                h4: 15,
                h5: 14,
                h6: 12,
                body: 13
            };
        }
        
        return {
            margins: {
                top: 3,
                right: 8,
                bottom: 3,
                left: 8
            },
            fontSizes: fontSizes,
            spacing: 0
        };
    }
    
    /**
     * Apply Safari-specific styles
     */
    applySafariStyles(container) {
        if (!container) return;
        
        // Apply text size classes
        const textElements = container.querySelectorAll('.text-2xs, .text-xs, .text-sm');
        textElements.forEach(el => {
            const styles = window.getComputedStyle(el);
            const fontSize = styles.getPropertyValue('font-size');
            el.style.fontSize = fontSize;
            el.style.lineHeight = '1';
        });
        
        // Fix SVG dimensions
        const svgElements = container.querySelectorAll('svg');
        svgElements.forEach(svg => {
            if (!svg.getAttribute('width') || !svg.getAttribute('height')) {
                const viewBox = svg.getAttribute('viewBox');
                if (viewBox) {
                    const [, , width, height] = viewBox.split(' ').map(Number);
                    svg.setAttribute('width', width);
                    svg.setAttribute('height', height);
                }
            }
        });
    }
}

// Singleton instance
let papyrusInstance = null;

export function getPapyrusManager() {
    if (!papyrusInstance) {
        papyrusInstance = new PapyrusManager();
        
        // Make available globally for debugging
        if (window.location.hostname === 'localhost') {
            window.papyrusManager = papyrusInstance;
        }
    }
    return papyrusInstance;
}
