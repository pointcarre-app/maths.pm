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
      labelRight2: options?.header?.labelRight2 ?? "2nde&1ère|Spé",
      classes: options?.header?.classes ?? ["font-mono"],
      style: options?.header?.style ?? "",
    },
    title: options?.title ?? "Bac 1ère Spé. Maths : Partie 1 automatismes",
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
  const leftText = (left.textContent || '').trim();
  if (!/^\d+\)\s/.test(leftText)) {
    const span = (outer.ownerDocument || document).createElement('span');
    span.textContent = prefix;
    left.insertBefore(span, left.firstChild);
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
  // Fallback simple wrapper
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

    // svg element styles
    try {
      const s = svg.style;
      if (s) {
        if (!s.display) s.display = 'block';
        if (!s.maxWidth) s.maxWidth = '100%';
        // Keep height:auto for layout parity even if width/height attrs exist
        if (!s.height) s.height = 'auto';
      }
    } catch (_) {}

    // foreignObject styles
    const foreignObjects = svg.querySelectorAll('foreignObject');
    foreignObjects.forEach((fo) => {
      try {
        fo.style.overflow = 'visible';
        // foreignObject > div
        const div = fo.querySelector(':scope > div');
        if (div && div.style) {
          if (!div.style.width) div.style.width = '100%';
          if (!div.style.height) div.style.height = '100%';
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
        if (!st.fontSize) st.fontSize = '14px';
        if (!st.lineHeight) st.lineHeight = '1.2';
        if (!st.textAlign) st.textAlign = 'center';
      } catch (_) {}
    });
    // .svg-latex .katex
    const katexNodes = svg.querySelectorAll('.svg-latex .katex');
    katexNodes.forEach((node) => {
      try { if (!node.style.fontSize) node.style.fontSize = 'inherit'; } catch (_) {}
    });

    // Text size utility classes
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
      span.textContent = prefix;
      only.insertBefore(span, only.firstChild);
    }
    only.setAttribute('id', `question-${num}`);
    return only.outerHTML;
  } catch (_) {
    return null;
  }
}


