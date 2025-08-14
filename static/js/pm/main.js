// PM namespace runtime entrypoint
// Provides progressive enhancement init and reveal modes

const FTYPE_TO_TAG = {
  'radio_': 'pm-radio',
  'codex_': 'pm-codex',
  // Future mappings:
  // 'graph_': 'pm-graph',
  // 'tabvar_': 'pm-tabvar',
  // 'svg_': 'pm-svg',
  // 'image_': 'pm-image',
  // 'table_': 'pm-table',
  // 'code_': 'pm-code',
  // 'h1_': 'pm-h1', 'h2_': 'pm-h2', 'h3_': 'pm-h3', 'h4_': 'pm-h4',
  // 'p_': 'pm-p', 'q_': 'pm-q', 'ul_': 'pm-ul', 'ol_': 'pm-ol', 'lbl_': 'pm-lbl', 'hr_': 'pm-hr', 'toc_': 'pm-toc',
};

function defineOnce(name, ctor) {
  if (!customElements.get(name)) customElements.define(name, ctor);
}

export class PMRuntime {
  /**
   * @param {Object} options
   * @param {'all'|'step'} [options.mode]
   * @param {string|Element} [options.container]
   * @param {boolean} [options.autoRegister]
   */
  constructor(options = {}) {
    this.options = {
      mode: options.mode ?? 'all',
      container: options.container ?? '.pm-container',
      autoRegister: options.autoRegister ?? true,
    };
    this.fragments = [];
    this.currentIndex = 0;
  }

  async init() {
    if (this.options.autoRegister) await this.registerComponents();
    // Apply layout wrappers before we snapshot fragment wrappers
    this.applyLayoutDirectives();
    this.fragments = this.queryWrappers();
    this.applyModeInitialState();
    this.initAllInteractive();
    // Mark document as ready for transitions once enhancement is done
    queueMicrotask(() => {
      document.documentElement.classList.add('pm-ready');
      document.body?.classList.add('pm-ready');
    });
  }

  async registerComponents() {
    // Dynamic imports to keep main light; only register used components
    const needed = new Set(
      this.queryWrappers().map((el) => el.dataset.f_type).filter(Boolean)
    );
    const registrations = [];
    for (const ftype of needed) {
      const tag = FTYPE_TO_TAG[ftype];
      if (!tag) continue;
      if (customElements.get(tag)) continue;
      if (ftype === 'radio_') {
        registrations.push(
          import('./components/pm-radio.js').then((m) => defineOnce(tag, m.PMRadio))
        );
      } else if (ftype === 'codex_') {
        registrations.push(
          import('./components/pm-codex.js').then((m) => defineOnce(tag, m.PMCodex))
        );
      }
    }
    await Promise.all(registrations);
  }

  queryWrappers() {
    const root = typeof this.options.container === 'string'
      ? document.querySelector(this.options.container)
      : this.options.container;
    if (!root) return [];
    return Array.from(root.querySelectorAll('.fragment-wrapper[data-f_type]'));
  }

  /**
   * Convert markdown layout directives into responsive column containers.
   *
   * Syntax in markdown (using attr_list on hr):
   * --- {: .pm-cols-md-2 }
   * Wraps the next 2 fragments in a 2-col container at md breakpoint.
   * Supported: pm-cols-sm-2, pm-cols-md-2, pm-cols-lg-2 (and -3 variants).
   */
  applyLayoutDirectives() {
    const root = typeof this.options.container === 'string'
      ? document.querySelector(this.options.container)
      : this.options.container;
    if (!root) return;

    const directiveWrappers = Array.from(
      root.querySelectorAll('.fragment-wrapper[data-f_type="hr_"]')
    );

    for (const wrapper of directiveWrappers) {
      const classes = Array.from(wrapper.classList);
      // Find first pm-cols directive class on the wrapper
      const directive = classes.find((c) => c.startsWith('pm-cols-'));
      if (!directive) continue;

      const match = directive.match(/^pm-cols-(sm|md|lg)?-?(2|3)$/);
      if (!match) continue;

      const bp = match[1] ?? 'md';
      const count = parseInt(match[2], 10);

      // Prepare container
      const container = document.createElement('div');
      container.className = `pm-cols pm-cols-${bp}-${count}`;
      // Carry over non-directive utility classes from the directive wrapper (e.g., gap-4)
      for (const cls of classes) {
        if (!cls.startsWith('pm-cols-')) container.classList.add(cls);
      }

      // Move the next N fragment-wrappers under the container
      let moved = 0;
      let nextEl = wrapper.nextElementSibling;
      while (nextEl && moved < count) {
        const isWrapper = nextEl.classList?.contains('fragment-wrapper');
        if (isWrapper) {
          const toMove = nextEl;
          nextEl = nextEl.nextElementSibling;
          container.appendChild(toMove);
          moved += 1;
        } else {
          // Skip non-wrapper nodes
          nextEl = nextEl.nextElementSibling;
        }
      }

      // Insert container at the wrapper position and remove wrapper
      wrapper.parentElement?.insertBefore(container, wrapper);
      wrapper.remove();
    }

    // Fallback: support inline directive typed on same line (parsed as paragraph)
    // Pattern: <p>--- {: .pm-cols-md-2 .gap-4 }</p>
    const paraWrappers = Array.from(
      root.querySelectorAll('.fragment-wrapper[data-f_type="p_"]')
    );
    for (const pWrap of paraWrappers) {
      const p = pWrap.querySelector('.fragment');
      if (!p) continue;
      const text = (p.textContent || '').trim();
      const m = text.match(/^---\s*\{:\s*([^}]+)\}$/);
      if (!m) continue;
      const attr = m[1];
      const tokens = attr.split(/\s+/).filter(Boolean);
      // Extract pm-cols directive and optional utility classes
      const directiveToken = tokens.find((t) => t.replace(/^\./, '').startsWith('pm-cols-'));
      if (!directiveToken) continue;
      const directive = directiveToken.replace(/^\./, '');
      const match = directive.match(/^pm-cols-(sm|md|lg)?-?(2|3)$/);
      if (!match) continue;
      const bp = match[1] ?? 'md';
      const count = parseInt(match[2], 10);

      const container = document.createElement('div');
      container.className = `pm-cols pm-cols-${bp}-${count}`;
      // carry over utility classes (strip leading '.')
      for (const t of tokens) {
        const cls = t.replace(/^\./, '');
        if (!cls.startsWith('pm-cols-')) container.classList.add(cls);
      }

      // Move next N fragment wrappers after this p_ wrapper
      let moved = 0;
      let nextEl = pWrap.nextElementSibling;
      while (nextEl && moved < count) {
        const isWrapper = nextEl.classList?.contains('fragment-wrapper');
        if (isWrapper) {
          const toMove = nextEl;
          nextEl = nextEl.nextElementSibling;
          container.appendChild(toMove);
          moved += 1;
        } else {
          nextEl = nextEl.nextElementSibling;
        }
      }
      pWrap.parentElement?.insertBefore(container, pWrap);
      pWrap.remove();
    }
  }

  initFragment(wrapperEl) {
    const fType = wrapperEl?.dataset?.f_type;
    if (!fType) return;
    const tag = FTYPE_TO_TAG[fType];
    if (!tag) return; // no enhancement

    // Upgrade by wrapping existing content in the component tag
    if (!wrapperEl.querySelector(tag)) {
      const fragment = wrapperEl.querySelector('.fragment');
      const host = document.createElement(tag);
      // Pass minimal context via dataset for PE
      host.setAttribute('data-f_type', fType);
      // Preserve original fragment semantic classes (e.g., 'codex', 'image', etc.)
      if (fragment && fragment.classList) {
        fragment.classList.forEach((cls) => {
          if (cls !== 'fragment') host.classList.add(cls);
        });
      }
      // Move existing child content into the component slot (clone and sanitize)
      // Keep classes on wrapper; component handles behavior only
      if (fragment) {
        const clone = fragment.cloneNode(true);
        // Remove legacy inline handlers to avoid ReferenceError
        clone.querySelectorAll('[onclick]').forEach((el) => el.removeAttribute('onclick'));
        // Project original children rather than nested wrapper divs
        while (clone.firstChild) host.appendChild(clone.firstChild);
      }
      // Replace fragment with component
      if (fragment && fragment.parentElement) {
        fragment.parentElement.replaceChild(host, fragment);
      } else {
        wrapperEl.appendChild(host);
      }
    }
  }

  initAllInteractive() {
    for (const el of this.fragments) this.initFragment(el);
  }

  setMode(mode) {
    this.options.mode = mode;
    this.applyModeInitialState();
  }

  applyModeInitialState() {
    if (this.options.mode === 'all') {
      this.fragments.forEach((el) => el.removeAttribute('data-pm-hidden'));
    } else {
      this.fragments.forEach((el, i) =>
        i === 0 ? el.removeAttribute('data-pm-hidden') : el.setAttribute('data-pm-hidden', '1')
      );
      this.currentIndex = 0;
    }
  }

  next() { this.showAtIndex(this.currentIndex + 1); }
  prev() { this.showAtIndex(this.currentIndex - 1); }
  goTo(index) { this.showAtIndex(index); }

  showAtIndex(index) {
    if (index < 0 || index >= this.fragments.length) return;
    if (this.options.mode === 'step') {
      this.fragments[this.currentIndex]?.setAttribute('data-pm-hidden', '1');
      this.fragments[index]?.removeAttribute('data-pm-hidden');
    }
    this.currentIndex = index;
    this.initFragment(this.fragments[index]);
  }
}

export const fragmentRegistry = { ...FTYPE_TO_TAG };

export default PMRuntime;


