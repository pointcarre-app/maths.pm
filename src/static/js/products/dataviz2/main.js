/**
 * DataViz2 Product - Nagini Execution Runtime
 * ============================================
 * 
 * Works with PM-CODEX elements AFTER they're created
 */

(function() {
    'use strict';
    
    console.log('[DataViz2] Script loaded');
    
    // Configuration
    const CONFIG = {
        naginiVersion: 'v0.0.24',
        naginiUrl: 'https://esm.sh/gh/pointcarre-app/nagini@v0.0.24/src/nagini.js?bundle',
        pyodideWorkerUrl: 'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.24/src/pyodide/worker/worker-dist.js',
        preloadPackages: ['matplotlib', 'pandas', 'numpy', 'bokeh'],
    };
    
    let naginiManager = null;
    let naginiReady = false;
    let Nagini = null;
    
    /**
     * Initialize Nagini
     */
    async function initializeNagini() {
        if (window.dataviz2InitPromise) {
            return window.dataviz2InitPromise;
        }
        
        window.dataviz2InitPromise = (async () => {
            try {
                console.log('[DataViz2] Loading Nagini...');
                const naginiModule = await import(CONFIG.naginiUrl);
                Nagini = naginiModule.Nagini;
                
                naginiManager = await Nagini.createManager(
                    'pyodide',
                    CONFIG.preloadPackages,
                    [],
                    [],
                    CONFIG.pyodideWorkerUrl
                );
                
                await Nagini.waitForReady(naginiManager);
                naginiReady = true;
                console.log('[DataViz2] ✅ Nagini ready');
                return true;
            } catch (error) {
                console.error('[DataViz2] Failed to initialize:', error);
                return false;
            }
        })();
        
        return window.dataviz2InitPromise;
    }
    
    /**
     * Add execution UI to a codex element
     */
    function addExecutionUI(element, codexDetail) {
        // Skip if already processed
        if (element.hasAttribute('data-dataviz2-ui-added')) {
            return;
        }
        element.setAttribute('data-dataviz2-ui-added', 'true');

        const cm = codexDetail.codeMirror;

        // Make it editable
        cm.setOption('readOnly', false);

        // Create execution UI - insert AFTER CodeMirror, not inside
        const uiContainer = document.createElement('div');
        uiContainer.className = 'dataviz2-execution-ui';
        uiContainer.innerHTML = `
            <div class="btn-group mb-4 mt-[-0.5rem]">
                <button class="dataviz2-execute-btn btn btn-secondary btn-soft btn-sm sm:btn-md">
                    ▶ Execute
                </button>
                <button class="dataviz2-clear-btn btn btn-soft btn-sm sm:btn-md">
                    Clear Output
                </button>
            </div>
            <div class="dataviz2-output" style="display: none;">
            <div class="divider">Output</div>
                <div class="dataviz2-output-content"></div>
            </div>
        `;

        // <div class="divider">Output</div>

        // Find the CodeMirror wrapper element
        const cmWrapper = cm.getWrapperElement();

        // Insert UI AFTER the CodeMirror element (outside it!)
        cmWrapper.parentNode.insertBefore(uiContainer, cmWrapper.nextSibling);

        const executeBtn = uiContainer.querySelector('.dataviz2-execute-btn');
        const clearBtn = uiContainer.querySelector('.dataviz2-clear-btn');
        const outputDiv = uiContainer.querySelector('.dataviz2-output');
        const outputContent = uiContainer.querySelector('.dataviz2-output-content');

        // Execute handler
        executeBtn.addEventListener('click', async () => {
            // Initialize Nagini if needed
            if (!naginiReady) {
                outputDiv.style.display = 'block';
                outputContent.innerHTML = '<div class="flex items-center gap-2"><div class="loading loading-spinner loading-sm"></div> <span class="text-base-content/60">Loading Nagini...</span></div>';

                const success = await initializeNagini();
                if (!success) {
                    outputContent.innerHTML = '<div class="alert alert-error alert-outline"><span>❌ Failed to load Python runtime</span></div>';
                    return;
                }
            }

            const code = cm.getValue();

            outputDiv.style.display = 'block';
            outputContent.innerHTML = '<div class="flex items-center gap-2"><div class="loading loading-spinner loading-sm"></div> <span class="text-base-content/60">Executing...</span></div>';

            try {
                const result = await naginiManager.executeAsync('script.py', code);

                outputContent.innerHTML = '';

                // Check for Python execution errors first (v0.0.24 format)
                if (result.error) {
                    console.log('[DataViz2] Python error detected:', result.error);
                    console.log('[DataViz2] Error stderr:', result.stderr);

                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'alert alert-error alert-outline';
                    errorDiv.innerHTML = `
                        <div>
                            <strong> ${result.error.name || 'Error'}:</strong>
                            <pre class="mt-1 text-sm">${result.stderr || result.error.message || 'Unknown execution error'}</pre>
                        </div>
                    `;
                    outputContent.appendChild(errorDiv);

                    // Still show stdout if there was output before the error
                    if (result.stdout) {
                        const stdoutDiv = document.createElement('div');
                        stdoutDiv.className = 'mt-2';
                        stdoutDiv.innerHTML = '<div class="text-sm text-base-content/70 mb-1">Output before error:</div>';
                        const pre = document.createElement('pre');
                        pre.className = 'bg-base-200 p-2 rounded text-sm';
                        pre.textContent = result.stdout;
                        stdoutDiv.appendChild(pre);
                        outputContent.appendChild(stdoutDiv);
                    }

                    return; // Don't process other outputs if there's an error
                }

                // Stdout
                if (result.stdout) {
                    const pre = document.createElement('pre');
                    pre.className = 'bg-base-200 p-4 rounded-box overflow-x-auto text-base-content';
                    pre.textContent = result.stdout;
                    outputContent.appendChild(pre);
                }

                // Stderr (warnings only, since errors are handled above) - simple approach
                if (result.stderr) {
                    const stderrText = result.stderr.trim();

                    // Just show a simple button for any stderr content
                    const warningContainer = document.createElement('div');
                    warningContainer.style.marginTop = '0.5rem';

                    const warningButton = document.createElement('button');
                    warningButton.className = 'btn btn-sm sm:btn-md btn-outline btn-warning';
                    warningButton.textContent = 'Show warnings';

                    const warningDetails = document.createElement('pre');
                    warningDetails.style.display = 'none';
                    warningDetails.style.marginTop = '0.5rem';
                    warningDetails.style.padding = '0.5rem';
                    warningDetails.style.background = 'var(--color-base-200)';
                    warningDetails.style.borderRadius = '0.25rem';
                    warningDetails.style.fontSize = '0.75rem';
                    warningDetails.style.maxHeight = '200px';
                    warningDetails.style.overflowY = 'auto';
                    warningDetails.style.whiteSpace = 'pre-wrap';
                    warningDetails.textContent = stderrText;

                    warningButton.onclick = function() {
                        const isVisible = warningDetails.style.display === 'block';
                        warningDetails.style.display = isVisible ? 'none' : 'block';
                        warningButton.textContent = isVisible ? 'Show warnings' : 'Hide warnings';
                    };

                    warningContainer.appendChild(warningButton);
                    warningContainer.appendChild(warningDetails);
                    outputContent.appendChild(warningContainer);
                }

                // Matplotlib figures
                if (result.figures && result.figures.length > 0) {
                    result.figures.forEach((base64, index) => {
                        const figureCard = document.createElement('div');
                        figureCard.className = 'card bg-base-100 mt-4';
                        figureCard.innerHTML = `
                            <figure class="px-4 pt-4">
                                <img src="data:image/png;base64,${base64}"
                                     alt="Figure ${index + 1}"
                                     class="rounded-xl" />
                            </figure>
                        `;
                        outputContent.appendChild(figureCard);
                    });
                }


                // Bokeh figures
                if (result.bokeh_figures && result.bokeh_figures.length > 0) {
                    console.log('[DataViz2] Found', result.bokeh_figures.length, 'Bokeh figures');

                    // Check if Bokeh is loaded, if not wait a bit
                    const renderBokeh = async () => {
                        if (!window.Bokeh) {
                            console.log('[DataViz2] Waiting for BokehJS to load...');
                            // Try to wait for Bokeh to load
                            let attempts = 0;
                            while (!window.Bokeh && attempts < 20) {
                                await new Promise(resolve => setTimeout(resolve, 250));
                                attempts++;
                            }

                            if (!window.Bokeh) {
                                const warningDiv = document.createElement('div');
                                warningDiv.className = 'alert alert-info mt-2';
                                warningDiv.innerHTML = `
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    <span>Bokeh plots detected but BokehJS not loaded. Add js_dependencies in your markdown metadata.</span>
                                `;
                                outputContent.appendChild(warningDiv);
                                return;
                            }
                        }

                        console.log('[DataViz2] BokehJS ready, rendering plots...');

                        result.bokeh_figures.forEach((figureJson, index) => {
                            try {
                                const bokehData = JSON.parse(figureJson);
                                const bokehCard = document.createElement('div');
                                bokehCard.className = 'card bg-base-100 shadow-xl mt-4';

                                // Create unique ID for this Bokeh plot
                                const plotId = `bokeh-plot-${Date.now()}-${index}`;

                                bokehCard.innerHTML = `
                                    <div class="card-body">
                                        <div class="text-sm text-base-content/60 mb-2">Interactive Bokeh Plot ${index + 1}</div>
                                        <div id="${plotId}" class="bokeh-container" style="min-height: 300px;"></div>
                                    </div>
                                `;
                                outputContent.appendChild(bokehCard);

                                // Render the Bokeh plot with a small delay to ensure DOM is ready
                                setTimeout(() => {
                                    try {
                                        console.log('[DataViz2] Rendering Bokeh plot', index + 1, 'to', plotId);
                                        window.Bokeh.embed.embed_item(bokehData, plotId);
                                    } catch (embedError) {
                                        console.error('[DataViz2] Embed error:', embedError);
                                        document.getElementById(plotId).innerHTML = `
                                            <div style="color: red;">Failed to embed plot: ${embedError.message}</div>
                                        `;
                                    }
                                }, 200);

                            } catch (e) {
                                console.error('[DataViz2] Failed to process Bokeh figure:', e);
                                const errorDiv = document.createElement('div');
                                errorDiv.className = 'alert alert-warning mt-2';
                                errorDiv.innerHTML = `<span>Failed to render Bokeh plot ${index + 1}: ${e.message}</span>`;
                                outputContent.appendChild(errorDiv);
                            }
                        });
                    };

                    // Start rendering process
                    renderBokeh();
                }

                if (!result.stdout && !result.stderr && (!result.figures || result.figures.length === 0)) {
                    outputContent.innerHTML = '<div class="text-base-content/60 italic">No output</div>';
                }

            } catch (jsError) {
                // This catches JavaScript-level errors (worker issues, timeouts, etc.)
                console.error('[DataViz2] JavaScript error:', jsError);
                outputContent.innerHTML = `
                    <div class="alert alert-error alert-outline">
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <div>
                            <strong>JavaScript Error:</strong>
                            <pre class="mt-1 text-sm">${jsError.message || jsError}</pre>
                        </div>
                    </div>
                `;
            }
        });

        // Clear handler
        clearBtn.addEventListener('click', () => {
            outputDiv.style.display = 'none';
            outputContent.innerHTML = '';
        });

        console.log('[DataViz2] Added execution UI to pm-codex element');
    }

    /**
     * Process a pm-codex element - add execution UI OUTSIDE CodeMirror
     */
    function processCodexElement(element) {
        // Skip if already processed
        if (element.hasAttribute('data-dataviz2-processed')) {
            return;
        }
        element.setAttribute('data-dataviz2-processed', 'true');

        // Listen for pm-codex-ready event (preferred method)
        const handleCodexReady = (event) => {
            if (event.target === element) {
                // Remove event listener to avoid duplicate processing
                element.removeEventListener('pm-codex-ready', handleCodexReady);
                addExecutionUI(element, event.detail);
            }
        };

        // Add event listener
        element.addEventListener('pm-codex-ready', handleCodexReady);

        // Fallback: Wait for CodeMirror to be created (in case event is missed)
        const waitForCM = setInterval(() => {
            const cmElement = element.querySelector('.CodeMirror');
            if (!cmElement) return;

            clearInterval(waitForCM);

            // Check if we already processed this element via event
            if (element.hasAttribute('data-dataviz2-ui-added')) {
                return;
            }
            
            // Get the CodeMirror instance
            const cm = cmElement.CodeMirror;
            if (!cm) {
                console.warn('[DataViz2] No CodeMirror instance found');
                return;
            }
            
            // Make it editable
            cm.setOption('readOnly', false);
            
            // Create execution UI - insert AFTER CodeMirror, not inside
            const uiContainer = document.createElement('div');
            uiContainer.className = 'dataviz2-execution-ui';
            uiContainer.innerHTML = `
                <div class="btn-group mb-4">
                    <button class="dataviz2-execute-btn btn btn-secondary btn-soft btn-sm sm:btn-md">
                        ▶ Execute
                    </button>
                    <button class="dataviz2-clear-btn btn btn-soft btn-sm sm:btn-md">
                        Clear Output
                    </button>
                </div>
                <div class="dataviz2-output" style="display: none;">
                <div class="divider">Output</div>
                    <div class="dataviz2-output-content"></div>
                </div>
            `;

            // <div class="divider">Output</div>
            
            // Insert UI AFTER the CodeMirror element (outside it!)
            cmElement.parentNode.insertBefore(uiContainer, cmElement.nextSibling);
            
            const executeBtn = uiContainer.querySelector('.dataviz2-execute-btn');
            const clearBtn = uiContainer.querySelector('.dataviz2-clear-btn');
            const outputDiv = uiContainer.querySelector('.dataviz2-output');
            const outputContent = uiContainer.querySelector('.dataviz2-output-content');
            
            // Execute handler
            executeBtn.addEventListener('click', async () => {
                // Initialize Nagini if needed
                if (!naginiReady) {
                    outputDiv.style.display = 'block';
                    outputContent.innerHTML = '<div class="flex items-center gap-2"><div class="loading loading-spinner loading-sm"></div> <span class="text-base-content/60">Loading Nagini...</span></div>';
                    
                    const success = await initializeNagini();
                    if (!success) {
                        outputContent.innerHTML = '<div class="alert alert-error alert-outline"><span>❌ Failed to load Python runtime</span></div>';
                        return;
                    }
                }
                
                const code = cm.getValue();
                
                outputDiv.style.display = 'block';
                outputContent.innerHTML = '<div class="flex items-center gap-2"><div class="loading loading-spinner loading-sm"></div> <span class="text-base-content/60">Executing...</span></div>';
                
                try {
                    const result = await naginiManager.executeAsync('script.py', code);
                    
                    outputContent.innerHTML = '';
                    
                    // Check for Python execution errors first (v0.0.24 format)
                    if (result.error) {
                        console.log('[DataViz2] Python error detected:', result.error);
                        console.log('[DataViz2] Error stderr:', result.stderr);
                        
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'alert alert-error alert-outline';
                        errorDiv.innerHTML = `
                            <div>
                                <strong> ${result.error.name || 'Error'}:</strong>
                                <pre class="mt-1 text-sm">${result.stderr || result.error.message || 'Unknown execution error'}</pre>
                            </div>
                        `;
                        outputContent.appendChild(errorDiv);
                        
                        // Still show stdout if there was output before the error
                        if (result.stdout) {
                            const stdoutDiv = document.createElement('div');
                            stdoutDiv.className = 'mt-2';
                            stdoutDiv.innerHTML = '<div class="text-sm text-base-content/70 mb-1">Output before error:</div>';
                            const pre = document.createElement('pre');
                            pre.className = 'bg-base-200 p-2 rounded text-sm';
                            pre.textContent = result.stdout;
                            stdoutDiv.appendChild(pre);
                            outputContent.appendChild(stdoutDiv);
                        }
                        
                        return; // Don't process other outputs if there's an error
                    }
                    
                    // Stdout
                    if (result.stdout) {
                        const pre = document.createElement('pre');
                        pre.className = 'bg-base-200 p-4 rounded-box overflow-x-auto text-base-content';
                        pre.textContent = result.stdout;
                        outputContent.appendChild(pre);
                    }
                    
                    // Stderr (warnings only, since errors are handled above) - simple approach
                    if (result.stderr) {
                        const stderrText = result.stderr.trim();
                        
                        // Just show a simple button for any stderr content
                        const warningContainer = document.createElement('div');
                        warningContainer.style.marginTop = '0.5rem';
                        
                        const warningButton = document.createElement('button');
                        warningButton.className = 'btn btn-sm sm:btn-md btn-outline btn-warning';
                        warningButton.textContent = 'Show warnings';
                        
                        const warningDetails = document.createElement('pre');
                        warningDetails.style.display = 'none';
                        warningDetails.style.marginTop = '0.5rem';
                        warningDetails.style.padding = '0.5rem';
                        warningDetails.style.background = 'var(--color-base-200)';
                        warningDetails.style.borderRadius = '0.25rem';
                        warningDetails.style.fontSize = '0.75rem';
                        warningDetails.style.maxHeight = '200px';
                        warningDetails.style.overflowY = 'auto';
                        warningDetails.style.whiteSpace = 'pre-wrap';
                        warningDetails.textContent = stderrText;
                        
                        warningButton.onclick = function() {
                            const isVisible = warningDetails.style.display === 'block';
                            warningDetails.style.display = isVisible ? 'none' : 'block';
                            warningButton.textContent = isVisible ? 'Show warnings' : 'Hide warnings';
                        };
                        
                        warningContainer.appendChild(warningButton);
                        warningContainer.appendChild(warningDetails);
                        outputContent.appendChild(warningContainer);
                    }
                    
                    // Matplotlib figures
                    if (result.figures && result.figures.length > 0) {
                        result.figures.forEach((base64, index) => {
                            const figureCard = document.createElement('div');
                            figureCard.className = 'card bg-base-100 mt-4';
                            figureCard.innerHTML = `
                                <figure class="px-4 pt-4">
                                    <img src="data:image/png;base64,${base64}" 
                                         alt="Figure ${index + 1}" 
                                         class="rounded-xl" />
                                </figure>
                            `;
                            outputContent.appendChild(figureCard);
                        });
                    }
                    
                //     <div class="card-body py-2">
                //     <p class="text-sm text-base-content/60">Matplotlib Figure ${index + 1}</p>
                // </div>


                    // Bokeh figures
                    if (result.bokeh_figures && result.bokeh_figures.length > 0) {
                        console.log('[DataViz2] Found', result.bokeh_figures.length, 'Bokeh figures');
                        
                        // Check if Bokeh is loaded, if not wait a bit
                        const renderBokeh = async () => {
                            if (!window.Bokeh) {
                                console.log('[DataViz2] Waiting for BokehJS to load...');
                                // Try to wait for Bokeh to load
                                let attempts = 0;
                                while (!window.Bokeh && attempts < 20) {
                                    await new Promise(resolve => setTimeout(resolve, 250));
                                    attempts++;
                                }
                                
                                if (!window.Bokeh) {
                                    const warningDiv = document.createElement('div');
                                    warningDiv.className = 'alert alert-info mt-2';
                                    warningDiv.innerHTML = `
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                        </svg>
                                        <span>Bokeh plots detected but BokehJS not loaded. Add js_dependencies in your markdown metadata.</span>
                                    `;
                                    outputContent.appendChild(warningDiv);
                                    return;
                                }
                            }
                            
                            console.log('[DataViz2] BokehJS ready, rendering plots...');
                            
                            result.bokeh_figures.forEach((figureJson, index) => {
                                try {
                                    const bokehData = JSON.parse(figureJson);
                                    const bokehCard = document.createElement('div');
                                    bokehCard.className = 'card bg-base-100 shadow-xl mt-4';
                                    
                                    // Create unique ID for this Bokeh plot
                                    const plotId = `bokeh-plot-${Date.now()}-${index}`;
                                    
                                    bokehCard.innerHTML = `
                                        <div class="card-body">
                                            <div class="text-sm text-base-content/60 mb-2">Interactive Bokeh Plot ${index + 1}</div>
                                            <div id="${plotId}" class="bokeh-container" style="min-height: 300px;"></div>
                                        </div>
                                    `;
                                    outputContent.appendChild(bokehCard);
                                    
                                    // Render the Bokeh plot with a small delay to ensure DOM is ready
                                    setTimeout(() => {
                                        try {
                                            console.log('[DataViz2] Rendering Bokeh plot', index + 1, 'to', plotId);
                                            window.Bokeh.embed.embed_item(bokehData, plotId);
                                        } catch (embedError) {
                                            console.error('[DataViz2] Embed error:', embedError);
                                            document.getElementById(plotId).innerHTML = `
                                                <div style="color: red;">Failed to embed plot: ${embedError.message}</div>
                                            `;
                                        }
                                    }, 200);
                                    
                                } catch (e) {
                                    console.error('[DataViz2] Failed to process Bokeh figure:', e);
                                    const errorDiv = document.createElement('div');
                                    errorDiv.className = 'alert alert-warning mt-2';
                                    errorDiv.innerHTML = `<span>Failed to render Bokeh plot ${index + 1}: ${e.message}</span>`;
                                    outputContent.appendChild(errorDiv);
                                }
                            });
                        };
                        
                        // Start rendering process
                        renderBokeh();
                    }
                    
                    if (!result.stdout && !result.stderr && (!result.figures || result.figures.length === 0)) {
                        outputContent.innerHTML = '<div class="text-base-content/60 italic">No output</div>';
                    }
                    
                } catch (jsError) {
                    // This catches JavaScript-level errors (worker issues, timeouts, etc.)
                    console.error('[DataViz2] JavaScript error:', jsError);
                    outputContent.innerHTML = `
                        <div class="alert alert-error alert-outline">
                            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                                <strong>JavaScript Error:</strong>
                                <pre class="mt-1 text-sm">${jsError.message || jsError}</pre>
                            </div>
                        </div>
                    `;
                }
            });
            
            // Clear handler
            clearBtn.addEventListener('click', () => {
                outputDiv.style.display = 'none';
                outputContent.innerHTML = '';
            });
            
            console.log('[DataViz2] Added execution UI to pm-codex element');
        }, 100);
        
        // Timeout after 5 seconds
        setTimeout(() => clearInterval(waitForCM), 5000);
    }
    
    /**
     * Find and process all pm-codex elements
     */
    function processAllCodexElements() {
        const elements = document.querySelectorAll('pm-codex:not([data-dataviz2-processed])');
        console.log(`[DataViz2] Processing ${elements.length} pm-codex elements`);
        elements.forEach(processCodexElement);
    }
    
    /**
     * Main initialization
     */
    function initialize() {
        console.log('[DataViz2] Initializing...');
        
        // Start Nagini init in background
        initializeNagini();
        
        // Process elements when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', processAllCodexElements);
        } else {
            // Small delay to let PMRuntime create pm-codex elements
            setTimeout(processAllCodexElements, 1000);
        }
        
        // Watch for new pm-codex elements
        const observer = new MutationObserver((mutations) => {
            let hasNewCodex = false;
            
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        if (node.tagName === 'PM-CODEX' || 
                            (node.querySelector && node.querySelector('pm-codex'))) {
                            hasNewCodex = true;
                        }
                    }
                });
            });
            
            if (hasNewCodex) {
                setTimeout(processAllCodexElements, 100);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Also check periodically for first 10 seconds
        let checks = 0;
        const checkInterval = setInterval(() => {
            checks++;
            processAllCodexElements();
            if (checks > 20) clearInterval(checkInterval);
        }, 500);
    }
    
    // Start
    initialize();
    
    // Debug exports
    window.DataViz2 = {
        processAll: processAllCodexElements,
        naginiReady: () => naginiReady,
        elements: () => document.querySelectorAll('pm-codex')
    };
    
})();