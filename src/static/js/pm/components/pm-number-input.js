import { LitElement, html, css } from 'https://cdn.jsdelivr.net/npm/lit@3/+esm';

export class PMNumberInput extends LitElement {
  static properties = {
    data: { type: Object },
    debug: { type: Boolean, reflect: true },
    _value: { state: true },
    _status: { state: true }, // 'correct' | 'incorrect' | null
    _message: { state: true },
    _locked: { state: true },
  };

  // Use light DOM so DaisyUI/Tailwind classes apply
  createRenderRoot() { return this; }

  static styles = css`
    :host { display: block; }
    .unit { opacity: 0.8; }
    .hint { font-size: 0.9em; opacity: 0.8; margin-top: 0.25rem; }
    .feedback { margin-top: 0.5rem; }
  `;

  constructor() {
    super();
    this.data = {};
    this.debug = false;
    this._value = '';
    this._status = null;
    this._message = '';
    this._locked = false;
    this._resizeObservers = new WeakMap();
    this._boundOnTransitionEnd = new WeakMap();
  }

  connectedCallback() {
    super.connectedCallback();
    // If no data provided programmatically, try reading from attribute
    if (!this.data || Object.keys(this.data).length === 0) {
      const payload = this.getAttribute('data-payload');
      if (payload) {
        try { this.data = JSON.parse(payload); } catch {}
      }
    }
    // Initialize any existing feedback containers to be collapsed
    this._initializeCollapsibles();
  }

  render() {
    const d = this.data || {};
    const min = d.min ?? undefined;
    const max = d.max ?? undefined;
    const step = d.step ?? 'any';
    const unit = d.unit ?? '';
    const useMathField = d.math_input === true || d.use_mathfield === true || d.useMathField === true || d.render_latex_input === true;

    return html`
      ${d.label ? html`<label class="label"><span class="label-text">${d.label}</span></label>` : null}
      ${this.debug ? this._renderParamsTable(d) : null}
      <div class="flex items-center gap-2 flex-wrap justify-end mb-3">
        ${useMathField ? html`
          <math-field class="input input-bordered"
                      style="font-size:1rem; font-family:'KaTeX_Main','KaTeX_Math','Times New Roman',serif;"
                      virtual-keyboard-mode="manual"
                      ?readOnly=${this._locked}
                      @input=${this._onMathInput}></math-field>
        ` : html`
          <input type="number"
                 class="input input-bordered w-128"
                 style="width:120px;font-size:1rem; font-family:'KaTeX_Main','KaTeX_Math','Times New Roman',serif;"
                 .value=${String(this._value ?? '')}
                 min=${min ?? ''}
                 max=${max ?? ''}
                 step=${step}
                 ?disabled=${this._locked}
                 @input=${this._onInput} />
        `}
        ${unit ? html`<div class="opacity-80 whitespace-nowrap">${unit}</div>` : null}
        <button class="btn btn-soft btn-outline" @click=${this._onCheck} ?disabled=${this._locked} aria-disabled=${this._locked ? 'true' : 'false'}>Valider</button>
      </div>
      ${d.hint ? html`<div class="hint">${unsafeHTMLIfNeeded(d.hint)}</div>` : null}
    `;
  }

  _renderParamsTable(d) {
    const entries = [
      ['id', d.id],
      ['min', d.min],
      ['max', d.max],
      ['step', d.step],
      ['unit', d.unit],
      ['correct', d.correct],
      ['tolerance', d.tolerance],
      ['correct_values', Array.isArray(d.correct_values) ? JSON.stringify(d.correct_values) : undefined],
      ['flag', d.flag],
    ].filter(([_, v]) => v !== undefined && v !== null && v !== '');
    if (entries.length === 0) return null;
    return html`
      <div class="overflow-x-auto" style="margin: 0.25rem 0 0.5rem;">
        <table class="fragment-table" style="font-size: 0.9rem;">
          <tbody>
            ${entries.map(([k, v]) => html`<tr><td style="opacity:.7;">${k}</td><td>${String(v)}</td></tr>`)}
          </tbody>
        </table>
      </div>
    `;
  }

  _getFragmentIndex() {
    const attr = this.getAttribute('data-fragment-index');
    if (attr !== null && attr !== undefined && String(attr).trim() !== '') {
      const n = Number(attr);
      return Number.isFinite(n) ? n : 0;
    }
    try {
      const wrapper = this.closest('.fragment-wrapper');
      if (!wrapper) return 0;
      const all = Array.from(document.querySelectorAll('.fragment-wrapper[data-f_type]'));
      const idx = all.indexOf(wrapper);
      return Math.max(0, idx);
    } catch (_) {
      return 0;
    }
  }

  _renderExternalFeedback() {
    const d = this.data || {};
    const idx = this._getFragmentIndex();
    const container = document.getElementById(`number-feedback-${idx}`);
    if (!container) return;
    
    if (!this._status) { 
      container.innerHTML = '';
      this._collapse(container);
      return; 
    }
    
    const ok = this._status === 'correct';
    const alerts = [];
    if (ok) {
      const textOk = d.feedback_correct || 'Bonne réponse.';
      alerts.push(`<div class="alert alert-soft alert-success mb-3"><span>${textOk}</span></div>`);
    } else {
      const textBad = d.feedback_incorrect || 'Ce n\'est pas la bonne réponse.';
      alerts.push(`<div class="alert alert-soft alert-error mb-3"><span>${textBad}</span></div>`);
      if (d.feedback_correct) {
        alerts.push(`<div class="alert alert-soft alert-success mb-3"><span>${d.feedback_correct}</span></div>`);
      }
    }
    
    const htmlAlerts = alerts.join('');
    container.innerHTML = htmlAlerts;
    
    // Expand container with animation if there's content
    if (htmlAlerts) {
      this._expand(container);
    } else {
      this._collapse(container);
    }
    
    // Render LaTeX in the feedback content
    this._renderLatex(container);
  }

  _renderLatex(targetElement) {
    try {
      if (!targetElement) return;
      // Prefer global auto-render helper if present
      const renderFn = (window && (window.renderMathInElement || (window.katex && window.katex.renderMathInElement))) || null;
      if (renderFn) {
        // Slight delay to allow layout/reflow in case of CSS transitions
        setTimeout(() => {
          try {
            renderFn(targetElement, {
              delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '\\[', right: '\\]', display: true },
                { left: '\\(', right: '\\)', display: false },
              ],
              throwOnError: false,
            });
          } catch (_) {
            // no-op
          }
        }, 0);
      }
    } catch (_) {
      // no-op
    }
  }


  _onInput = (e) => {
    this._value = e.target.value;
    this._status = null;
    this._message = '';
  };

  _onMathInput = (e) => {
    // MathLive emits LaTeX in e.target.value; extract a numeric if possible
    const latex = (e.target?.value || '').trim();
    const numeric = this._latexToNumber(latex);
    this._value = numeric;
    this._status = null;
    this._message = '';
  };

  _latexToNumber(latex) {
    if (!latex) return '';
    // Simple parsing: keep digits, minus and decimal separator
    const cleaned = String(latex).replace(/[^0-9+\-.,]/g, '').replace(/,/g, '.');
    const n = parseFloat(cleaned);
    return Number.isFinite(n) ? String(n) : '';
  }

  _onCheck = () => {
    const d = this.data || {};
    if (this._locked) return;
    const value = Number(this._value);
    if (Number.isNaN(value)) {
      this._status = 'incorrect';
      this._message = 'Please enter a number';
      this.requestUpdate();
      this._renderExternalFeedback();
      return;
    }

    let isCorrect = false;
    if (Array.isArray(d.correct_values) && d.correct_values.length > 0) {
      isCorrect = d.correct_values.some((cv) => withinTolerance(value, Number(cv.value), Number(cv.tolerance ?? 0)));
    } else if (typeof d.correct === 'number') {
      isCorrect = withinTolerance(value, Number(d.correct), Number(d.tolerance ?? 0));
    }

    this._status = isCorrect ? 'correct' : 'incorrect';
    this._locked = true;
    try { this.setAttribute('data-number-disabled', 'true'); } catch {}
    this.requestUpdate();
    this._renderExternalFeedback();
  };

  _initializeCollapsibles() {
    // Find number feedback containers for this component's index
    const idx = this._getFragmentIndex();
    const container = document.getElementById(`number-feedback-${idx}`);
    if (container) {
      // Start fully collapsed without space
      container.classList.add('pm-collapsed');
      container.classList.remove('pm-open');
      // Ensure no stale inline max-height
      container.style.maxHeight = '0px';
    }
  }

  _expand(el) {
    if (!el) return;
    // Measure content and set max-height to animate open
    const target = Math.max(1, el.scrollHeight);
    this._stripLegacyVisibilityClasses(el);
    el.classList.add('pm-open');
    el.classList.remove('pm-collapsed');
    el.removeAttribute('aria-hidden');
    el.style.opacity = '';
    // First set to current computed height to allow transition from 0 → value
    el.style.maxHeight = `${target}px`;
    // Clean any accidental collapsed states on children
    el.querySelectorAll('.pm-collapsed').forEach((child) => {
      child.classList.remove('pm-collapsed');
      if (child.style && 'maxHeight' in child.style) child.style.maxHeight = '';
    });

    // Dynamically grow height if content reflows (e.g., fonts/images/KaTeX)
    this._observeDuringExpand(el);

    // After transition completes, let it be auto height to prevent cropping
    this._attachTransitionEnd(el, () => {
      // If still open, clear explicit max-height so content can grow freely
      if (el.classList.contains('pm-open')) {
        el.style.maxHeight = '';
      }
      this._disconnectObserver(el);
    });
  }

  _collapse(el) {
    if (!el) return;
    // Animate close by setting max-height to 0
    this._stripLegacyVisibilityClasses(el);
    // If max-height is not set (auto), set it to current height to enable transition
    const computed = getComputedStyle(el).maxHeight;
    if (!el.style.maxHeight || computed === 'none') {
      el.style.maxHeight = `${Math.max(1, el.scrollHeight)}px`;
      // Force reflow so the browser registers the starting height
      // eslint-disable-next-line no-unused-expressions
      el.offsetHeight;
    }
    el.style.maxHeight = '0px';
    el.classList.add('pm-collapsed');
    el.classList.remove('pm-open');
    el.setAttribute('aria-hidden', 'true');
    this._disconnectObserver(el);
  }

  _stripLegacyVisibilityClasses(el) {
    const legacy = ['opacity-0', 'opacity-100', 'scale-95', 'scale-100', '-translate-y-2', '-translate-y-4', 'translate-y-0', 'pointer-events-none'];
    legacy.forEach((cls) => el.classList.remove(cls));
  }

  _observeDuringExpand(el) {
    // Avoid duplicate observers
    if (this._resizeObservers.has(el)) return;
    if (typeof ResizeObserver === 'function') {
      const ro = new ResizeObserver(() => {
        if (!el.classList.contains('pm-open')) return;
        // Update to new content height while animating
        el.style.maxHeight = `${Math.max(1, el.scrollHeight)}px`;
      });
      ro.observe(el);
      this._resizeObservers.set(el, ro);
    } else {
      // Fallback: update a few times
      let ticks = 0;
      const id = setInterval(() => {
        if (!el.classList.contains('pm-open') || ++ticks > 10) return clearInterval(id);
        el.style.maxHeight = `${Math.max(1, el.scrollHeight)}px`;
      }, 50);
      this._resizeObservers.set(el, { disconnect() { clearInterval(id); } });
    }
  }

  _disconnectObserver(el) {
    const ro = this._resizeObservers.get(el);
    if (ro && typeof ro.disconnect === 'function') ro.disconnect();
    this._resizeObservers.delete(el);
  }

  _attachTransitionEnd(el, handler) {
    const bound = (evt) => {
      if (evt.propertyName !== 'max-height') return;
      handler();
    };
    // Detach previous listener if any
    const prev = this._boundOnTransitionEnd.get(el);
    if (prev) el.removeEventListener('transitionend', prev);
    el.addEventListener('transitionend', bound);
    this._boundOnTransitionEnd.set(el, bound);
  }
}

function withinTolerance(x, target, tol) {
  const t = Number.isFinite(tol) ? Math.abs(tol) : 0;
  return Math.abs(x - target) <= t;
}

// Helper function - just return text as-is since we're using innerHTML
function unsafeHTMLIfNeeded(text) {
  if (typeof text !== 'string') return '';
  return text;
}

customElements.define('pm-number-input', PMNumberInput);

export default PMNumberInput;


