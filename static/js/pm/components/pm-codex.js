import { LitElement, html, css } from 'https://cdn.jsdelivr.net/npm/lit@3/+esm';

export class PMCodex extends LitElement {
  static styles = css` :host { display: block; } `;

  firstUpdated() {
    // Lazy-initialize CodeMirror when the component becomes visible
    const containerAttr = this.querySelector('[data-codex-container]');
    const container = containerAttr || this;
    console.debug('[pm-codex] init: container found?', Boolean(containerAttr), 'fallbackSelf?', !containerAttr);
    const initEditor = () => {
      const textarea = container.querySelector('textarea.codex-editor');
      console.debug('[pm-codex] initEditor: textarea present?', Boolean(textarea));
      if (!textarea) return;
      if (!textarea.id) {
        textarea.id = `pm-codex-textarea-${Math.random().toString(36).slice(2, 8)}`;
        console.debug('[pm-codex] assigned id to textarea:', textarea.id);
      }
      const start = () => {
        try {
          // eslint-disable-next-line no-undef
          const cm = CodeMirror.fromTextArea(textarea, {
            mode: textarea.dataset.language || 'python',
            lineNumbers: true,
            readOnly: 'nocursor',
            viewportMargin: Infinity,
          });
          console.debug('[pm-codex] CodeMirror started');
          container.querySelectorAll('.skeleton').forEach((sk) => sk.classList.add('hidden'));
        } catch (e) {
          console.warn('[pm-codex] CodeMirror init failed, revealing textarea', e);
          textarea.classList.remove('hidden');
        }
      };

      if (typeof CodeMirror === 'undefined') {
        // Wait for CodeMirror to be available (retry like original inline script)
        let attempts = 0;
        const maxAttempts = 200; // ~10s at 50ms
        const interval = setInterval(() => {
          console.debug('[pm-codex] waiting CodeMirror...', attempts);
          if (typeof CodeMirror !== 'undefined') {
            clearInterval(interval);
            start();
          } else if (++attempts >= maxAttempts) {
            clearInterval(interval);
            // fallback: reveal textarea
            textarea.classList.remove('hidden');
            container.querySelectorAll('.skeleton').forEach((sk) => sk.classList.add('hidden'));
          }
        }, 50);
        return;
      }
      start();
    };

    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            console.debug('[pm-codex] visible, initializing');
            initEditor();
            io.disconnect();
          }
        });
      }, { rootMargin: '200px 0px', threshold: 0.01 });
      io.observe(this);
    } else {
      // immediate init
      console.debug('[pm-codex] no IO, initializing immediately');
      initEditor();
    }
  }

  render() { return html`<slot></slot>`; }
}

export default PMCodex;


