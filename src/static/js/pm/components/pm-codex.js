import { LitElement, html, css } from 'https://cdn.jsdelivr.net/npm/lit@3/+esm';

/**
 * PMCodex Web Component - Interactive Code Editor for Math.pm Platform
 * 
 * This LitElement-based web component provides a sophisticated code editing interface
 * that integrates with the Math.pm fragment system. It's specifically designed to handle
 * "codex" fragments that contain Python code for mathematical exercises and interactive
 * learning content.
 * 
 * INTEGRATION WITH FRAGMENT BUILDER:
 * ================================
 * The component works in conjunction with FragmentBuilder.from_code() method in 
 * src/core/pm/services/fragment_builder.py. When a YAML code block with 
 * `f_type: codex_` is processed:
 * 
 * 1. FragmentBuilder parses the script_path and loads the Python file
 * 2. PythonParser splits the code into sections (foreground, background, checks)
 * 3. The foreground_script (user-editable code) is stored in data["content"]
 * 4. The template renders a textarea with this content
 * 5. PMCodex component enhances the textarea with CodeMirror editor
 * 
 * EXPECTED HTML STRUCTURE:
 * =======================
 * The component expects to find within its scope:
 * - A textarea element with class "codex-editor"
 * - Optional: An element with attribute [data-codex-container] as the search scope
 * - Optional: .skeleton elements that are hidden once CodeMirror loads
 * 
 * Example template structure:
 * <pm-codex>
 *   <div data-codex-container>
 *     <div class="skeleton">Loading...</div>
 *     <textarea class="codex-editor hidden" data-language="python">
 *       # Python code from data["content"] goes here
 *     </textarea>
 *   </div>
 * </pm-codex>
 * 
 * PERFORMANCE OPTIMIZATIONS:
 * =========================
 * - Lazy initialization: CodeMirror only loads when component becomes visible
 * - Intersection Observer: Uses modern browser API for efficient visibility detection
 * - Graceful degradation: Falls back to plain textarea if CodeMirror fails to load
 * - Async loading: Waits for CodeMirror library with timeout fallback
 * 
 * LIFECYCLE AND BEHAVIOR:
 * ======================
 * 1. Component mounts and renders slot content
 * 2. firstUpdated() sets up intersection observer or immediate initialization
 * 3. When visible, initEditor() searches for textarea and sets up CodeMirror
 * 4. CodeMirror enhances textarea with syntax highlighting, line numbers, etc.
 * 5. Skeleton loading indicators are hidden once editor is ready
 * 6. If any step fails, gracefully falls back to showing plain textarea
 * 
 * CONFIGURATION:
 * =============
 * CodeMirror editor is configured with:
 * - Language mode: From textarea's data-language attribute (defaults to 'python')
 * - Line numbers: Always enabled for code readability
 * - Read-only: Set to 'nocursor' - users can see but not edit the code
 * - Viewport margin: Infinity ensures all content is rendered (good for printing/export)
 * 
 * ERROR HANDLING:
 * ==============
 * The component includes comprehensive error handling:
 * - Missing textarea: Silently returns without error
 * - CodeMirror load failure: Shows plain textarea as fallback
 * - Initialization timeout: 10-second timeout with fallback
 * - Missing CodeMirror library: Polling mechanism with max attempts
 */
export class PMCodex extends LitElement {
  static styles = css` :host { display: block; } `;

  firstUpdated() {
    // STEP 1: CONTAINER DETECTION
    // Look for an explicit container element with data-codex-container attribute
    // This allows for more flexible HTML structure and better scoping of editor search
    const containerAttr = this.querySelector('[data-codex-container]');
    const container = containerAttr || this;
    console.debug('[pm-codex] init: container found?', Boolean(containerAttr), 'fallbackSelf?', !containerAttr);
    
    /**
     * CORE EDITOR INITIALIZATION FUNCTION
     * ===================================
     * This function handles the actual CodeMirror setup process.
     * It's separated into its own function so it can be called either
     * immediately (for older browsers) or when the component becomes visible
     * (for modern browsers with IntersectionObserver support).
     */
    const initEditor = () => {
      // STEP 2: TEXTAREA DETECTION
      // Search for the textarea that contains the code content
      // The textarea should have class "codex-editor" and contain the code from data["content"]
      const textarea = container.querySelector('textarea.codex-editor');
      console.debug('[pm-codex] initEditor: textarea present?', Boolean(textarea));
      if (!textarea) return; // Graceful exit if no textarea found
      
      // STEP 3: ID ASSIGNMENT
      // Ensure textarea has a unique ID for CodeMirror integration
      // CodeMirror needs an ID to properly replace the textarea element
      if (!textarea.id) {
        textarea.id = `pm-codex-textarea-${Math.random().toString(36).slice(2, 8)}`;
        console.debug('[pm-codex] assigned id to textarea:', textarea.id);
      }
      
      /**
       * CODEMIRROR STARTUP FUNCTION
       * ===========================
       * This function actually creates the CodeMirror instance.
       * It's wrapped in a try-catch for error handling and separated
       * so it can be called either immediately or after waiting for CodeMirror to load.
       */
      const start = () => {
        try {
          // STEP 4: CODEMIRROR CREATION
          // Create CodeMirror instance from the textarea
          // Check if this codex should be editable
          // Also check the parent wrapper for attributes
          const wrapper = this.closest('.fragment-wrapper[data-f_type="codex_"]');
          const isExecutable = this.hasAttribute('data-executable') || 
                             container.hasAttribute('data-executable') ||
                             wrapper?.hasAttribute('data-executable');
          const isEditable = this.hasAttribute('data-editable') || 
                           container.hasAttribute('data-editable') ||
                           wrapper?.hasAttribute('data-editable');
          
          // eslint-disable-next-line no-undef
          const cm = CodeMirror.fromTextArea(textarea, {
            mode: textarea.dataset.language || 'python', // Language mode from data attribute, default Python
            lineNumbers: true,                           // Show line numbers for reference
            readOnly: isEditable ? false : 'nocursor',  // Editable if marked, otherwise read-only
            viewportMargin: Infinity,                   // Render all content (good for printing/export)
          });
          console.debug('[pm-codex] CodeMirror started', { isExecutable, isEditable });
          
          // STEP 4.1: APPLY HEIGHT CONFIGURATION
          // Check for height configuration in data attributes
          // Priority: pm-codex element > container > wrapper
          const heightInPx = this.getAttribute('data-height-in-px') || 
                           container.getAttribute('data-height-in-px') ||
                           wrapper?.getAttribute('data-height-in-px');
          
          const cmWrapper = cm.getWrapperElement();
          
          if (heightInPx) {
            const height = parseInt(heightInPx, 10);
            if (!isNaN(height) && height > 0) {
              // Set the custom height on the CodeMirror wrapper
              cmWrapper.style.height = `${height}px`;
              cmWrapper.style.maxHeight = `${height}px`;
              console.debug('[pm-codex] Applied custom height:', height + 'px');
            } else {
              // Invalid height, use default
              cmWrapper.style.height = '600px';
              cmWrapper.style.maxHeight = '600px';
              console.debug('[pm-codex] Invalid height, using default: 600px');
            }
          } else {
            // No height specified, use default 600px
            cmWrapper.style.height = '600px';
            cmWrapper.style.maxHeight = '600px';
            console.debug('[pm-codex] No height specified, using default: 600px');
          }
          
          // Refresh CodeMirror to ensure proper rendering with new height
          setTimeout(() => cm.refresh(), 10);
          
          // Store CodeMirror instance for external access
          this._codeMirror = cm;
          container._codeMirror = cm;
          
          // STEP 5: ADD EXECUTION UI (if executable)
          // Add execution controls that product-specific scripts can hook into
          if (isExecutable) {
            this._addExecutionUI(container, cm);
          }
          
          // STEP 6: UI CLEANUP
          // Hide skeleton loading indicators now that the real editor is ready
          // This provides smooth transition from loading state to ready state
          container.querySelectorAll('.skeleton').forEach((sk) => sk.classList.add('hidden'));
        } catch (e) {
          // STEP 7: FALLBACK HANDLING
          // If CodeMirror fails to initialize, show the plain textarea as fallback
          // This ensures users can still see the code even if enhanced editor fails
          console.warn('[pm-codex] CodeMirror init failed, revealing textarea', e);
          textarea.classList.remove('hidden');
        }
      };

      // STEP 7: CODEMIRROR AVAILABILITY CHECK
      // CodeMirror might not be loaded yet (async script loading)
      // We need to wait for it or provide fallback
      if (typeof CodeMirror === 'undefined') {
        // STEP 8: POLLING MECHANISM
        // Wait for CodeMirror to be available with exponential backoff
        // This handles cases where CodeMirror script is loaded asynchronously
        let attempts = 0;
        const maxAttempts = 200; // ~10 seconds at 50ms intervals
        const interval = setInterval(() => {
          console.debug('[pm-codex] waiting CodeMirror...', attempts);
          if (typeof CodeMirror !== 'undefined') {
            // CodeMirror is now available, start the editor
            clearInterval(interval);
            start();
          } else if (++attempts >= maxAttempts) {
            // Timeout reached, fall back to plain textarea
            clearInterval(interval);
            console.warn('[pm-codex] CodeMirror load timeout, falling back to textarea');
            textarea.classList.remove('hidden');
            container.querySelectorAll('.skeleton').forEach((sk) => sk.classList.add('hidden'));
          }
        }, 50);
        return;
      }
      // CodeMirror is already available, start immediately
      start();
    };

    // STEP 9: VISIBILITY-BASED INITIALIZATION
    // Use IntersectionObserver for performance - only initialize when component is visible
    // This prevents unnecessary CodeMirror instances for off-screen content
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            console.debug('[pm-codex] visible, initializing');
            initEditor();
            io.disconnect(); // One-time initialization, then disconnect observer
          }
        });
      }, { 
        rootMargin: '200px 0px',  // Start loading 200px before component enters viewport
        threshold: 0.01           // Trigger when even 1% of component is visible
      });
      io.observe(this);
    } else {
      // STEP 10: FALLBACK FOR OLDER BROWSERS
      // If IntersectionObserver is not supported, initialize immediately
      // This ensures compatibility with older browsers while sacrificing some performance
      console.debug('[pm-codex] no IO, initializing immediately');
      initEditor();
    }
  }

  /**
   * ADD EXECUTION UI
   * ================
   * Adds execution controls (buttons and output area) to the codex
   * Product-specific scripts can listen for the 'codex-execute' event
   * to handle the actual execution logic
   */
  _addExecutionUI(container, codeMirror) {
    // Create execution UI container
    const uiContainer = document.createElement('div');
    uiContainer.className = 'codex-execution-ui mt-3';
    
    // Create button group
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'flex gap-2 mb-3';
    
    // Execute button with DaisyUI styling
    const executeBtn = document.createElement('button');
    executeBtn.className = 'btn btn-primary btn-sm';
    executeBtn.innerHTML = `
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      Execute
    `;
    
    // Clear button (initially hidden)
    const clearBtn = document.createElement('button');
    clearBtn.className = 'btn btn-ghost btn-sm hidden';
    clearBtn.innerHTML = `
      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
      </svg>
      Clear Output
    `;
    
    buttonGroup.appendChild(executeBtn);
    buttonGroup.appendChild(clearBtn);
    uiContainer.appendChild(buttonGroup);
    
    // Output area (initially hidden)
    const outputArea = document.createElement('div');
    outputArea.className = 'codex-output-area hidden';
    
    // Output header
    const outputHeader = document.createElement('div');
    outputHeader.className = 'text-sm font-semibold mb-2 text-base-content/70';
    outputHeader.textContent = 'Output:';
    
    // Output content with DaisyUI mockup-code styling
    const outputContent = document.createElement('div');
    outputContent.className = 'codex-output-content mockup-code bg-base-200 relative';
    outputContent.innerHTML = '<pre class="text-sm"><code></code></pre>';
    
    outputArea.appendChild(outputHeader);
    outputArea.appendChild(outputContent);
    uiContainer.appendChild(outputArea);
    
    // Insert UI after the CodeMirror wrapper
    const cmWrapper = codeMirror.getWrapperElement();
    cmWrapper.parentNode.insertBefore(uiContainer, cmWrapper.nextSibling);
    
    // Event handlers
    executeBtn.addEventListener('click', () => {
      const code = codeMirror.getValue();
      
      // Show output area and clear button
      outputArea.classList.remove('hidden');
      clearBtn.classList.remove('hidden');
      
      // Show loading state
      outputContent.innerHTML = `
        <pre class="text-sm"><code class="text-info">Executing code...</code></pre>
      `;
      
      // Dispatch custom event for product-specific handlers
      const event = new CustomEvent('codex-execute', {
        detail: {
          code: code,
          codeMirror: codeMirror,
          outputElement: outputContent,
          codexElement: this,
          container: container
        },
        bubbles: true
      });
      this.dispatchEvent(event);
      console.debug('[pm-codex] Dispatched codex-execute event');
    });
    
    clearBtn.addEventListener('click', () => {
      // Clear output and hide areas
      outputContent.innerHTML = '<pre class="text-sm"><code></code></pre>';
      outputArea.classList.add('hidden');
      clearBtn.classList.add('hidden');
    });
    
    // Store references for external access
    this._executionUI = {
      container: uiContainer,
      executeBtn: executeBtn,
      clearBtn: clearBtn,
      outputArea: outputArea,
      outputContent: outputContent
    };
  }

  /**
   * RENDER METHOD
   * =============
   * Simple slot-based rendering allows the template to define the exact HTML structure
   * The component acts as a progressive enhancement wrapper around existing HTML
   * This approach provides maximum flexibility for template authors
   */
  render() { return html`<slot></slot>`; }
}

export default PMCodex;


