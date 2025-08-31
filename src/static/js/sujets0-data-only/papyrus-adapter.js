import { S0 } from "./state.js";

/**
 * Build a Papyrus blocks array from sujets0-data-only results.
 * - The first item is a header block with a table (isPapyrusHeader=true)
 * - Then title and subtitle blocks
 * - Then one block per question
 *   - If a question has an SVG, render a two-column flex container with
 *     statement on the left and the SVG on the right
 *   - Otherwise, render the statement inside a single div
 *
 * @param {Array<Object>} results - Array of question results (S0.results.questionResults)
 * @param {Object} options - Optional overrides for header/title text
 * @returns {Array<Object>} Papyrus blocks
 */
export function buildPapyrusBlocks(results, options = {}) {
  const opts = {
    header: {
      labelTitle: options?.header?.labelTitle ?? "Nom :",
      labelClass: options?.header?.labelClass ?? "Classe :",
      labelRight: options?.header?.labelRight ?? "BolzanoBleu",
      labelFirstname: options?.header?.labelFirstname ?? "Prénom :",
      labelDate: options?.header?.labelDate ?? "Date :",
      labelRight2: options?.header?.labelRight2 ?? "Spé",
      classes: options?.header?.classes ?? ["font-mono"],
      style: options?.header?.style ?? "",
    },
    title: options?.title ?? "Bac 1ère - Première Partie : Automatismes",
    subtitle: options?.subtitle ?? "Questions inspirées des Sujets 0",
  };

  const blocks = [];

  // Header block
  const headerHtml = (
    `<table style='width: 100%; border-collapse: collapse; border: 0.5px solid #e0e0e0; '>` +
    `<tr>` +
    `<td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>${opts.header.labelTitle}</td>` +
    `<td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>${opts.header.labelClass}</td>` +
    `<td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>${opts.header.labelRight}</td>` +
    `</tr>` +
    `<tr>` +
    `<td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 50%;'>${opts.header.labelFirstname}</td>` +
    `<td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>${opts.header.labelDate}</td>` +
    `<td style='border: 0.5px solid #e0e0e0; padding: 2mm; vertical-align: middle; width: 25%;'>${opts.header.labelRight2}</td>` +
    `</tr>` +
    `</table>`
  );
  blocks.push({
    id: "header-section",
    html: headerHtml,
    classes: opts.header.classes,
    style: opts.header.style,
    isPapyrusHeader: true,
  });

  // Title blocks
  blocks.push({
    id: "main-title",
    html: `<div>${opts.title}</div>`,
    classes: [],
    style: "font-family: 'Spectral', serif; font-size: 24px; font-weight: bold; text-align: left; color: #2c3e50;",
  });
  blocks.push({
    id: "subtitle",
    html: `<div>${opts.subtitle}</div>`,
    classes: [],
    style: "font-family: 'Spectral', serif; font-size: 18px; font-weight: 500; text-align: left; color: #5a6c7d; font-style: italic;",
  });

  // Question blocks
  (results || []).forEach((result, index) => {
    const num = index + 1;
    const questionId = `question-${num}-block`;
    const rawStatementHtml = (result?.data?.statement_html ?? "").trim();

    let html;
    if (result?.graphSvgWithRenderedLatex) {
      // Two-column layout: statement left, SVG right
      const width = result?.graphDict?.svg?.width || 250;
      const height = result?.graphDict?.svg?.height || undefined;
      const containerStyle = "display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;";
      const leftColStyle = "flex: 1; min-width: 250px;";
      const rightColStyle = `flex: 0 1 auto;${width ? ` width: ${width}px;` : ''}${height ? ` height: ${height}px;` : ''}`;

      let sizedSvg = ensureSvgDimensionsInString(result.graphSvgWithRenderedLatex, width, height);
      // sizedSvg = ensureKatexFontFaceInSvg(sizedSvg);
      sizedSvg = inlineSvgStylesBasedOnCssRules(sizedSvg);
      const leftCol = buildLeftColumnHtml(rawStatementHtml, num, leftColStyle);
      html = (
        `<div style='${containerStyle}'>` +
        `${leftCol}` +
        `<div style='${rightColStyle}' class='graph-svg-container'>${sizedSvg}</div>` +
        `</div>`
      );
    } else {
      // No SVG attached. If statement already comes with a two-column wrapper, inject id/numbering inside the left column.
      const transformed = transformPreWrappedTwoColumns(rawStatementHtml, num);
      if (transformed) {
        html = transformed;
      } else {
        // Single DIV case: inject numbering inside that div with the id
        const singleDiv = buildSingleDivWithIdAndNumber(rawStatementHtml, num);
        if (singleDiv) {
          html = singleDiv;
        } else {
          // Fallback simple wrapper
          html = `<div id='question-${num}'>${num}) ${rawStatementHtml}</div>`;
        }
      }
    }

    blocks.push({ id: questionId, html, classes: [], style: "" });
  });

  return blocks;
}

/**
 * Convenience: build from the current global S0 results.
 * @param {Object} options
 * @returns {Array<Object>}
 */
export function buildPapyrusBlocksFromS0(options = {}) {
  const results = S0?.results?.questionResults || [];
  return buildPapyrusBlocks(results, options);
}

/**
 * Serialize blocks to a pretty JSON string.
 * @param {Array<Object>} blocks
 * @returns {string}
 */
export function serializePapyrusBlocks(blocks) {
  return JSON.stringify(blocks, null, 2);
}

// Expose in browser for quick access from console or other scripts
if (typeof window !== "undefined") {
  window.PapyrusAdapter = {
    buildPapyrusBlocks,
    buildPapyrusBlocksFromS0,
    serializePapyrusBlocks,
  };
}

// --- helpers ---

/**
 * Escape HTML while preserving inline math segments between $...$ and block math $$...$$.
 * This keeps LaTeX delimiters intact and only escapes the non-math parts.
 * @param {string} input
 * @returns {string}
 */
function escapeHtmlPreservingMath(input) {
  if (!input) return "";
  const parts = splitByMath(input);
  return parts
    .map((p) => (p.isMath ? p.text : escapeHtml(p.text)))
    .join("");
}

function splitByMath(text) {
  const result = [];
  let i = 0;
  while (i < text.length) {
    if (text.startsWith("$$", i)) {
      const end = text.indexOf("$$", i + 2);
      if (end !== -1) {
        result.push({ isMath: true, text: text.slice(i, end + 2) });
        i = end + 2;
        continue;
      }
    }
    if (text[i] === "$") {
      const end = text.indexOf("$", i + 1);
      if (end !== -1) {
        result.push({ isMath: true, text: text.slice(i, end + 1) });
        i = end + 1;
        continue;
      }
    }
    // collect non-math run
    let j = i;
    while (j < text.length && text[j] !== "$") j++;
    result.push({ isMath: false, text: text.slice(i, j) });
    i = j;
  }
  return result;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Ensure width/height attributes exist in the outermost <svg> string.
 * If width/height are provided, set/override them and ensure viewBox exists.
 * @param {string} svgString
 * @param {number|undefined} width
 * @param {number|undefined} height
 * @returns {string}
 */
function ensureSvgDimensionsInString(svgString, width, height) {
  try {
    if (!svgString || (width == null && height == null)) return svgString;
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgString, "image/svg+xml");
    const svg = doc.querySelector('svg');
    if (!svg) return svgString;

    // Existing numeric attrs, if present
    const currentW = parseInt(svg.getAttribute('width') || '0', 10);
    const currentH = parseInt(svg.getAttribute('height') || '0', 10);
    const finalW = width || currentW || 340;
    const finalH = height || currentH || 340;

    svg.setAttribute('width', String(finalW));
    svg.setAttribute('height', String(finalH));
    if (!svg.getAttribute('viewBox')) {
      svg.setAttribute('viewBox', `0 0 ${finalW} ${finalH}`);
    }

    const serializer = new XMLSerializer();
    return serializer.serializeToString(svg);
  } catch (_) {
    return svgString;
  }
}

/**
 * If the statement is an already HTML-encoded two-column wrapper, inject the
 * question id into the left column and prepend the numbering. Keep it simple:
 * - Detect a top-level flex container and two inner divs
 * - Insert id on the first inner div and prefix the text with "{num}) "
 * - Return an HTML string; otherwise return null to fall back
 *
 * Note: Works on raw statement (not escaped) to keep logic simple, but we
 * escape the injected numbering to be safe.
 */
function transformPreWrappedTwoColumns(rawStatementHtml, num) {
  if (!rawStatementHtml) return null;
  // Remove any leading numbering like "9) " that may have been prefixed
  const stripped = rawStatementHtml.replace(/^\s*\d+\)\s*/, "");
  let outer = null;
  try {
    if (typeof document !== 'undefined' && document.createElement) {
      const temp = document.createElement('div');
      temp.innerHTML = stripped;
      outer = temp.firstElementChild;
    }
  } catch (_) {
    outer = null;
  }
  if (!outer) {
    try {
      const parser = new DOMParser();
      const doc = parser.parseFromString(stripped, 'text/html');
      outer = doc?.body?.firstElementChild || null;
    } catch (_) {
      outer = null;
    }
  }
  // If still no element, try decoding entities and parsing again
  if (!outer) {
    try {
      const decoded = decodeHtmlEntities(stripped);
      const temp = document.createElement('div');
      temp.innerHTML = decoded;
      outer = temp.firstElementChild || null;
    } catch (_) {
      outer = null;
    }
  }
  if (!outer || outer.tagName.toLowerCase() !== 'div') return null;
  const style = (outer.getAttribute('style') || '').replace(/\s+/g, ' ').trim();
  const isFlexLike = /display:\s*flex/i.test(style);
  if (!isFlexLike) return null;

  const innerDivs = outer.querySelectorAll(':scope > div');
  if (innerDivs.length < 1) return null;

  const left = innerDivs[0];
  const prefix = `${num}) `;
  // Clean leading numbering/whitespace in the outer left div so we don't duplicate
  try {
    while (left.firstChild && left.firstChild.nodeType === Node.TEXT_NODE) {
      const txt = left.firstChild.textContent || '';
      if (!txt.trim()) { left.removeChild(left.firstChild); continue; }
      if (/^\s*\d+\)\s*/.test(txt)) { left.removeChild(left.firstChild); continue; }
      break;
    }
  } catch (_) { /* ignore */ }

  // Choose the actual content container (prefer a single inner div if present)
  let target = left;
  try {
    // Skip leading whitespace-only text for accurate child count
    while (target.firstChild && target.firstChild.nodeType === Node.TEXT_NODE && !target.firstChild.textContent.trim()) {
      target.removeChild(target.firstChild);
    }
    if (target.childNodes && target.childNodes.length >= 1 && target.firstElementChild && target.firstElementChild.tagName && target.firstElementChild.tagName.toLowerCase() === 'div') {
      target = target.firstElementChild;
    }
  } catch (_) { /* ignore */ }

  // If the target already starts with a numbering, do nothing; else insert NBSP+NBSP and prefix
  const existingText = (target.textContent || '').trim();
  if (!/^\d+\)\s/.test(existingText)) {
    const nbspNode = (outer.ownerDocument || document).createTextNode('\u00A0');
    const prefixNode = (outer.ownerDocument || document).createTextNode(prefix);
    target.insertBefore(nbspNode, target.firstChild);
    target.insertBefore(prefixNode, target.firstChild);
    
  }
  left.setAttribute('id', `question-${num}`);

  return outer.outerHTML;
}

function decodeHtmlEntities(input) {
  if (!input) return "";
  return input
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&amp;/g, "&");
}

/**
 * Build left column HTML from statement_html by either:
 * - Pulling the first inner div of a flex wrapper and injecting id+numbering, or
 * - Wrapping the raw statement_html as a single left column with id+numbering.
 */
function buildLeftColumnHtml(rawStatementHtml, num, leftColStyle) {
  const transformed = transformPreWrappedTwoColumns(rawStatementHtml, num);
  if (transformed) {
    // transformed returns the entire outer flex wrapper; extract just the left inner div
    try {
      const temp = document.createElement('div');
      temp.innerHTML = transformed;
      const outer = temp.firstElementChild;
      const left = outer?.querySelector(':scope > div');
      if (left) {
        // Ensure style is applied
        left.setAttribute('style', leftColStyle);
        return left.outerHTML;
      }
    } catch (_) {
      // fallthrough to simple wrapper
    }
  }
  // Fallbacks when statement_html is not a flex wrapper
  try {
    const temp = document.createElement('div');
    temp.innerHTML = (rawStatementHtml || '').trim();
    const only = temp.firstElementChild;
    if (only && only.tagName && only.tagName.toLowerCase() === 'div') {
      // Ensure it's not already a flex container
      const st = (only.getAttribute('style') || '').replace(/\s+/g, ' ').trim();
      const isFlex = /display:\s*flex/i.test(st);
      if (!isFlex) {
        // Inject numbering inside the inner div, then apply id and merge style
        const text = (only.textContent || '').trim();
        if (!/^\d+\)\s/.test(text)) {
          const prefixNode = document.createTextNode(`${num}) `);
          const nbspNode = document.createTextNode('\u00A0\u00A0');
          only.insertBefore(prefixNode, only.firstChild);
          only.insertBefore(nbspNode, only.firstChild.nextSibling);
        }
        // id and style
        only.setAttribute('id', `question-${num}`);
        const mergedStyle = st ? `${st}; ${leftColStyle}` : leftColStyle;
        only.setAttribute('style', mergedStyle);
        return only.outerHTML;
      }
    }
  } catch (_) { /* ignore */ }

  // Last-resort simple wrapper
  return `<div id='question-${num}' style='${leftColStyle}'>${num}) ${rawStatementHtml}</div>`;
}

/**
 * Inline styles into SVG elements based on selectors present in data-only.css.
 * Targets within the SVG string:
 * - svg (display:block; max-width:100%; height:auto)
 * - foreignObject (overflow:visible)
 * - foreignObject > div (width/height 100%, flex centering)
 * - .svg-latex (font-size, line-height, text-align)
 * - .svg-latex .katex (font-size: inherit)
 * - .text-sm/.text-xs/.text-2xs (font-size and line-height)
 */
function inlineSvgStylesBasedOnCssRules(svgString) {
  try {
    if (!svgString) return svgString;
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgString, 'image/svg+xml');
    const svg = doc.querySelector('svg');
    if (!svg) return svgString;

    // svg element styles: lock to attribute dimensions to avoid responsive rescaling
    try {
      const s = svg.style;
      if (s) {
        const attrW = svg.getAttribute('width');
        const attrH = svg.getAttribute('height');
        if (attrW) s.width = /px$/.test(attrW) ? attrW : `${parseInt(attrW, 10)}px`;
        if (attrH) s.height = /px$/.test(attrH) ? attrH : `${parseInt(attrH, 10)}px`;
        // Do not set max-width/height:auto; force fixed sizing
        if (s.maxWidth) s.maxWidth = '';
      }
    } catch (_) {}

    // foreignObject styles
    const foreignObjects = svg.querySelectorAll('foreignObject');
    foreignObjects.forEach((fo) => {
      try {
        fo.style.overflow = 'visible';
        // Lock foreignObject to its attribute width/height in px
        const foW = fo.getAttribute('width');
        const foH = fo.getAttribute('height');
        if (foW) fo.style.width = /px$/.test(foW) ? foW : `${parseInt(foW, 10)}px`;
        if (foH) fo.style.height = /px$/.test(foH) ? foH : `${parseInt(foH, 10)}px`;
        // foreignObject > div content should fill its box
        const div = fo.querySelector(':scope > div');
        if (div && div.style) {
          div.style.width = '100%';
          div.style.height = '100%';
          if (!div.style.display) div.style.display = 'flex';
          if (!div.style.alignItems) div.style.alignItems = 'center';
          if (!div.style.justifyContent) div.style.justifyContent = 'center';
        }
      } catch (_) {}
    });

    // .svg-latex styles
    const svgLatexNodes = svg.querySelectorAll('.svg-latex');
    svgLatexNodes.forEach((node) => {
      try {
        const st = node.style;
        if (!st.textAlign) st.textAlign = 'center';
        // font-size will be set by size utility classes below; avoid forcing 14px
      } catch (_) {}
    });
    // .svg-latex .katex
    const katexNodes = svg.querySelectorAll('.svg-latex .katex');
    katexNodes.forEach((node) => {
      try { if (!node.style.fontSize) node.style.fontSize = 'inherit'; } catch (_) {}
    });

    // Text size utility classes (keep rem so re-render environments can scale consistently)
    const map = [
      { sel: '.text-sm', fs: '0.875rem', lh: '1.25rem' },
      { sel: '.text-xs', fs: '0.75rem', lh: '1rem' },
      { sel: '.text-2xs', fs: '0.625rem', lh: '1' },
    ];
    for (const { sel, fs, lh } of map) {
      const nodes = svg.querySelectorAll(sel);
      nodes.forEach((n) => {
        try {
          if (!n.style.fontSize) n.style.fontSize = fs;
          if (!n.style.lineHeight) n.style.lineHeight = lh;
        } catch (_) {}
      });
    }

    const serializer = new XMLSerializer();
    return serializer.serializeToString(svg);
  } catch (_) {
    return svgString;
  }
}

/**
 * Ensure KaTeX_Math font-face is present inside the SVG <style> so math glyph metrics
 * are stable regardless of page CSS. Accepts an SVG string and returns updated string.
 */
function ensureKatexFontFaceInSvg(svgString) {
  try {
    if (!svgString) return svgString;
    const parser = new DOMParser();
    const doc = parser.parseFromString(svgString, 'image/svg+xml');
    const svg = doc.querySelector('svg');
    if (!svg) return svgString;

    const hasKatexFace = /font-family:\s*'KaTeX_Math'/.test(svgString) || /@font-face\s*\{[^}]*KaTeX_Math/i.test(svgString);
    if (hasKatexFace) {
      const serializer = new XMLSerializer();
      return serializer.serializeToString(svg);
    }

    // Inject minimal @font-face using the same data URL as ui.js (cached globally when prerender ran)
    const styleEl = doc.createElementNS('http://www.w3.org/2000/svg', 'style');
    const dataUrl = window?._katexMathItalicDataUrl || '';
    styleEl.textContent = `
@font-face { font-family: 'KaTeX_Math'; font-style: italic; src: url('${dataUrl}') format('woff2'); font-display: swap; }
.katex { font-family: 'KaTeX_Math', 'KaTeX_Main', serif; }
.katex * { font-family: inherit !important; }
`;
    svg.insertBefore(styleEl, svg.firstChild);
    const serializer = new XMLSerializer();
    return serializer.serializeToString(svg);
  } catch (_) {
    return svgString;
  }
}

/**
 * If statement_html is a single <div> wrapper (non-flex), inject id="question-N"
 * on that inner div and prepend the numbering inside it. Return null if the
 * structure is not a single top-level div.
 */
function buildSingleDivWithIdAndNumber(rawStatementHtml, num) {
  if (!rawStatementHtml) return null;
  try {
    const temp = document.createElement('div');
    temp.innerHTML = rawStatementHtml.trim();
    const only = temp.firstElementChild;
    if (!only || only.tagName.toLowerCase() !== 'div') return null;
    // Ensure it's not a flex container (handled elsewhere)
    const style = (only.getAttribute('style') || '').replace(/\s+/g, ' ').trim();
    if (/display:\s*flex/i.test(style)) return null;

    // Prepend numbering inside and set id on this inner div
    const prefix = `${num}) `;
    const text = (only.textContent || '').trim();
    if (!/^\d+\)\s/.test(text)) {
      const span = document.createElement('span');
      span.innerHTML = prefix + '&nbsp;&nbsp;';
      only.insertBefore(span, only.firstChild);
    }
    only.setAttribute('id', `question-${num}`);
    return only.outerHTML;
  } catch (_) {
    return null;
  }
}


