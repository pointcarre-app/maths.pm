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
          // Configuration optimized for read-only code display with educational features
          // eslint-disable-next-line no-undef
          const cm = CodeMirror.fromTextArea(textarea, {
            mode: textarea.dataset.language || 'python', // Language mode from data attribute, default Python
            lineNumbers: true,                           // Show line numbers for reference
            readOnly: 'nocursor',                       // Read-only: users can see but not edit
            viewportMargin: Infinity,                   // Render all content (good for printing/export)
          });
          console.debug('[pm-codex] CodeMirror started');
          
          // STEP 5: UI CLEANUP
          // Hide skeleton loading indicators now that the real editor is ready
          // This provides smooth transition from loading state to ready state
          container.querySelectorAll('.skeleton').forEach((sk) => sk.classList.add('hidden'));
        } catch (e) {
          // STEP 6: FALLBACK HANDLING
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
   * RENDER METHOD
   * =============
   * Simple slot-based rendering allows the template to define the exact HTML structure
   * The component acts as a progressive enhancement wrapper around existing HTML
   * This approach provides maximum flexibility for template authors
   */
  render() { return html`<slot></slot>`; }
}

export default PMCodex;


