import { LitElement, html, css } from 'https://cdn.jsdelivr.net/npm/lit@3/+esm';

export class PMRadio extends LitElement {
  static styles = css`
    :host { display: block; }
  `;

  constructor() {
    super();
    this._resizeObservers = new WeakMap();
    this._boundOnTransitionEnd = new WeakMap();
    this._disabledGroups = new Set();
  }

  firstUpdated() {
    // Event delegation: handle clicks on any radio button within this fragment
    this.addEventListener('click', (e) => {
      // Find the actual clicked button even through shadow boundary retargeting
      const path = (typeof e.composedPath === 'function') ? e.composedPath() : [];
      let btn = null;
      for (const node of path) {
        if (node && typeof node.matches === 'function' && node.matches('button[data-radio-group]')) {
          btn = node; break;
        }
      }
      if (!btn) {
        // Fallback to closest from target if available
        const t = e.target;
        btn = t && typeof t.closest === 'function' ? t.closest('button[data-radio-group]') : null;
      }
      if (!btn || !this.contains(btn)) return;
      const flag = Number(btn.getAttribute('data-flag'));
      const feedback = btn.getAttribute('data-feedback') || '';
      const groupIndexAttr = btn.getAttribute('data-radio-group');
      const groupIndex = Number(groupIndexAttr);
      // Prevent interaction if group is already locked
      if (this._disabledGroups.has(groupIndex)) return;
      this._handleClick(groupIndex, flag, btn, feedback);
    });

    // Initialize collapsible areas to be fully collapsed with no reserved space
    this._initializeCollapsibles();
  }

  _findGroupIndex() {
    // Try to infer from closest wrapper index in the page (fallback to 0)
    const wrapper = this.closest('.fragment-wrapper');
    if (!wrapper) return 0;
    const all = Array.from(document.querySelectorAll('.fragment-wrapper[data-f_type]'));
    return Math.max(0, all.indexOf(wrapper));
  }

  _handleClick(groupIndex, flag, button, feedback) {
    const allButtons = this.querySelectorAll(`button[data-radio-group="${groupIndex}"]`);
    
    // Remove all pre-click classes from all buttons in the group (first interaction)
    this._removePreClickClasses(allButtons);
    
    // Reset visual state for the group
    allButtons.forEach((btn) => {
      // Remove all DaisyUI color classes to ensure clean state
      btn.classList.remove('btn-success', 'btn-error', 'btn-primary', 'btn-secondary', 'btn-accent', 'btn-neutral', 'btn-info', 'btn-warning');
      btn.classList.add('btn-outline');
    });

    // Styling depending on correctness
    if (flag === 20) {
      // Correct clicked: highlight selected as solid success
      button.classList.remove('btn-outline');
      button.classList.add('btn-success');
    } else if (flag === 21) {
      // Wrong clicked: keep selected as solid error, softly show the correct choices
      button.classList.remove('btn-outline');
      button.classList.add('btn-error');
      // Soft-highlight all correct answers (flag 20) using outline success
      allButtons.forEach((btn) => {
        const f = Number(btn.getAttribute('data-flag'));
        if (f === 20) {
          // Remove any existing color classes that might interfere
          btn.classList.remove('btn-primary', 'btn-secondary', 'btn-accent', 'btn-neutral', 'btn-info', 'btn-warning', 'btn-error');
          btn.classList.add('btn-success');
          // keep outline to appear soft
          if (!btn.classList.contains('btn-outline')) btn.classList.add('btn-outline');
        }
      });
    } else {
      // Neutral/other choice clicked; keep outline style
      // Already has btn-outline from the reset, no additional styling needed
    }

    // Build feedback area and render multiple alerts based on rules
    let feedbackArea = this._byId(`radio-feedback-${groupIndex}`);
    if (!feedbackArea) {
      feedbackArea = this._ensureFeedbackContainer(groupIndex);
    }

    // Collect candidate alerts from buttons
    const alerts = [];
    const getFeedbackText = (btn, f) => {
      const txt = btn.getAttribute('data-feedback') || '';
      if (txt) return txt;
      if (f === 20) return 'Bonne réponse.';
      if (f === 21) return 'Ce n\'est pas la bonne réponse.';
      return '';
    };

    const clickedBtn = button;
    const clickedFlag = Number(clickedBtn.getAttribute('data-flag'));

    const buttonsArray = Array.from(allButtons);
    const correctButtons = buttonsArray.filter((b) => Number(b.getAttribute('data-flag')) === 20);
    const otherButtons = buttonsArray.filter((b) => {
      const f = Number(b.getAttribute('data-flag'));
      return f !== 20 && f !== 21;
    });

    if (clickedFlag === 21) {
      // Wrong: show 21 first, then 20, then others
      const dangerText = getFeedbackText(clickedBtn, 21);
      if (dangerText) alerts.push({ cls: 'alert-error', text: dangerText });
      correctButtons.forEach((b) => {
        const customText = b.getAttribute('data-feedback') || '';
        if (customText) alerts.push({ cls: 'alert-success', text: customText });
      });
      otherButtons.forEach((b) => {
        const customText = b.getAttribute('data-feedback') || '';
        if (customText) alerts.push({ cls: 'alert-info', text: customText });
      });
    } else if (clickedFlag === 20) {
      // Correct: show only 20 then any other informational alerts
      const customText = clickedBtn.getAttribute('data-feedback') || '';
      if (customText) alerts.push({ cls: 'alert-success', text: customText });
      otherButtons.forEach((b) => {
        const customText = b.getAttribute('data-feedback') || '';
        if (customText) alerts.push({ cls: 'alert-info', text: customText });
      });
    } else {
      // Other: show its own info alert (if any)
      const customText = clickedBtn.getAttribute('data-feedback') || '';
      if (customText) alerts.push({ cls: 'alert-info', text: customText });
    }

    if (feedbackArea) {
      // Render alerts in order; apply soft style uniformly and add spacing between them
      const htmlAlerts = alerts.map((a) => `<div class="alert alert-soft mb-3 ${a.cls}"><span>${a.text}</span></div>`).join('');
      feedbackArea.innerHTML = htmlAlerts || '';
      if (htmlAlerts) this._expand(feedbackArea); else this._collapse(feedbackArea);
      // Ensure LaTeX is rendered in newly injected feedback content
      this._renderLatex(feedbackArea);
    }

    // Always expand explanation if present
    const explanationArea = this._byId(`radio-explanation-${groupIndex}`);
    if (explanationArea) {
      this._expand(explanationArea);
      this._renderLatex(explanationArea);
    }

    // Color the statement above based on answer
    this._colorPreviousStatement(flag);

    // Disable the whole radio group after first click while keeping it visible
    this._disableGroup(groupIndex);

    const storageKey = `i-radio-answer-${window.location.pathname}-${groupIndex}`;
    const answerData = {
      flag,
      timestamp: new Date().toISOString(),
      isCorrect: flag === 20,
      feedback: feedback || null,
    };
    try { localStorage.setItem(storageKey, JSON.stringify(answerData)); } catch {}

    const event = new CustomEvent('i-radio-answered', {
      detail: { fragmentIndex: groupIndex, flag, isCorrect: flag === 20, feedback: feedback || null, timestamp: new Date().toISOString() },
    });
    document.dispatchEvent(event);
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

  _removePreClickClasses(buttons) {
    // Remove all classes that start with 'pre-' from all buttons in the group
    buttons.forEach((btn) => {
      const classList = Array.from(btn.classList);
      classList.forEach((className) => {
        if (className.startsWith('pre-')) {
          btn.classList.remove(className);
        }
      });
    });
  }

  _colorPreviousStatement(flag) {
    try {
      // Find the wrapper of this radio component
      const currentWrapper = this.closest('.fragment-wrapper');
      if (!currentWrapper) return;
      
      // Look for previous sibling that contains a statement
      let prevElement = currentWrapper.previousElementSibling;
      while (prevElement) {
        // Check if this element has the statement class
        const statement = prevElement.querySelector('.statement') || 
                         (prevElement.classList.contains('statement') ? prevElement : null);
        if (statement) {
          // Remove any existing answer classes
          statement.classList.remove('statement-correct', 'statement-incorrect', 'statement-info');
          
          // Add appropriate class based on flag
          if (flag === 20) {
            statement.classList.add('statement-correct');
          } else if (flag === 21) {
            statement.classList.add('statement-incorrect');
          } else {
            statement.classList.add('statement-info');
          }
          break;
        }
        prevElement = prevElement.previousElementSibling;
      }
    } catch (e) {
      // Fail silently
    }
  }

  _disableGroup(groupIndex) {
    // Logical lock: do not use native disabled to keep visual styles vivid
    this._disabledGroups.add(groupIndex);
    const groupButtons = this.querySelectorAll(`button[data-radio-group="${groupIndex}"]`);
    groupButtons.forEach((btn) => {
      try {
        btn.setAttribute('aria-disabled', 'true');
        btn.setAttribute('tabindex', '-1');
      } catch {}
    });
    // Mark host as completed for styling hooks if needed
    this.setAttribute('data-radio-disabled', 'true');
  }

  _byId(id) {
    // query inside shadow first, then in document (SSR content may be outside)
    return this.querySelector(`#${id}`) || document.getElementById(id);
  }

  _initializeCollapsibles() {
    const candidates = Array.from(this.querySelectorAll('[id]'));
    const nodes = candidates.filter((el) => /^(radio-feedback|radio-explanation)-\d+$/.test(el.id));
    nodes.forEach((el) => {
      // Start fully collapsed without space
      el.classList.add('pm-collapsed');
      el.classList.remove('pm-open');
      // Ensure no stale inline max-height on container only
      el.style.maxHeight = '0px';
    });
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
    // Clean any accidental collapsed states on children (e.g., feedback span)
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

  _ensureFeedbackContainer(groupIndex) {
    // Check again in DOM
    let container = document.getElementById(`radio-feedback-${groupIndex}`);
    if (container) return container;

    const currentWrapper = this.closest('.fragment-wrapper');
    const dynamicWrapper = document.createElement('div');
    dynamicWrapper.className = 'fragment-wrapper fragment-dynamic';

    const fragment = document.createElement('div');
    fragment.className = 'fragment';

    container = document.createElement('div');
    container.id = `radio-feedback-${groupIndex}`;
    container.className = 'pm-collapsed';

    const alert = document.createElement('div');
    alert.className = 'alert';

    const span = document.createElement('span');
    span.id = `radio-feedback-text-${groupIndex}`;

    alert.appendChild(span);
    container.appendChild(alert);
    fragment.appendChild(container);
    dynamicWrapper.appendChild(fragment);

    if (currentWrapper && currentWrapper.parentElement) {
      currentWrapper.parentElement.insertBefore(dynamicWrapper, currentWrapper.nextSibling);
    } else {
      // Fallback: append after host
      this.parentElement?.insertBefore(dynamicWrapper, this.nextSibling);
    }

    return container;
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

  render() {
    // Project SSR children; enhancement wires events only
    return html`<slot></slot>`;
  }
}

export default PMRadio;


