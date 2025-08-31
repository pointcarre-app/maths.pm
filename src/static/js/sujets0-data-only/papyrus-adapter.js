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
    const questionId = `question-${num}`;
    const statement = (result?.statement ?? "").trim();
    const statementHtml = `<div>${num}) ${escapeHtmlPreservingMath(statement)}</div>`;

    let html;
    if (result?.graphSvgWithRenderedLatex) {
      // Two-column layout: statement left, SVG right
      const width = result?.graphDict?.svg?.width || 250;
      const containerStyle = "display: flex; gap: 20px; align-items: flex-start;";
      const leftColStyle = "flex: 1;";
      const rightColStyle = `flex: 0 0 ${width}px;`;
      html = (
        `<div style='${containerStyle}'>` +
        `<div style='${leftColStyle}'>${statementHtml}<div></div></div>` +
        `<div style='${rightColStyle}'>${result.graphSvgWithRenderedLatex}</div>` +
        `</div>`
      );
    } else {
      // Single-column layout: statement only
      html = `<div><div>${num}) ${escapeHtmlPreservingMath(statement)}</div><div></div></div>`;
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


