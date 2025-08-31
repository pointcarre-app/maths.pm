import { isSafari, loadModuleDynamically, configSujets0DataOnly } from "./config.js";
import { S0, setInState, getFromState } from "./state.js";
import { convertAllGraphsToPng, convertAllGraphsToPng_canvg, prerenderLatexInAllResultsWithGraph, setDomToImage } from "./graphics.js";

export function createDataTable(results) {
  const table = document.createElement("table");
  table.style.width = "1500px;";
  table.style.borderCollapse = "collapse";

  results.forEach((result) => {
    const row = table.insertRow();

    const statementCell = row.insertCell();
    statementCell.style.width = "300px";
    statementCell.style.border = "1px solid black";
    statementCell.textContent = result.statement || "N/A";

    const svgCell = row.insertCell();
    svgCell.style.width = "300px";
    svgCell.style.border = "1px solid black";
    if (result.graphSvgWithRenderedLatex) {
      const svgElement = document.createElement("div");
      svgElement.classList.add("graph-svg-container");
      svgElement.innerHTML = result.graphSvgWithRenderedLatex;
      svgCell.appendChild(svgElement);
    } else {
      svgCell.textContent = "N/A";
    }

    //const pngCell = row.insertCell();
    //pngCell.style.width = "300px";
    //pngCell.style.border = "1px solid black";
    //if (result.graphPng) {
      //const imgElement = document.createElement("img");
      //imgElement.src = result.graphPng;
      //imgElement.style.width = "100%";
      //pngCell.appendChild(imgElement);
    //} else {
      //pngCell.textContent = "N/A";
    //}

    const answerCell = row.insertCell();
    answerCell.style.width = "300px";
    answerCell.style.border = "1px solid black";
    answerCell.textContent = JSON.stringify(result.answer) || "N/A";
  });

  setInState("ui.tableElement", table);
  return table;
}

export async function renderResultsTable(results) {
  const table = createDataTable(results);
  document.body.appendChild(table);
  if (!isSafari()) {
    // Using the original dom-to-image pipeline (stable for foreignObject/KaTeX)
    // Alternative canvg-based path kept below but disabled due to foreignObject limitations.
    
    // await convertAllGraphsToPng(results); // dom-to-image version

    // await convertAllGraphsToPng_canvg(results); // canvg version (disabled)
    // Update PNG column after conversion
    //results.forEach((result, idx) => {
      //if (result.graphPng) {
        //const pngCell = table.rows[idx].cells[2];
        //const imgElement = document.createElement("img");
        //imgElement.src = result.graphPng;
        //imgElement.style.width = `${result.graphDimensions.width}px`;
        //imgElement.style.height = `${result.graphDimensions.height}px`;
        //pngCell.innerHTML = "";
        //pngCell.appendChild(imgElement);
      //}
    //});

    // Also create a new column with PNGs converted directly from rendered SVGs
    // Using the original dom-to-image table-column renderer.
    // Alternative html-to-image column renderer kept below but disabled due to external stylesheet CORS inlining.
    //await appendPngFromRenderedSvgColumn(table, results); // dom-to-image version
    // await appendPngFromRenderedSvgColumn_htmlToImage(table, results); // html-to-image version (disabled)
  }
  return table;
}


async function ensureDomToImage() {
  if (window._domtoimage) return window._domtoimage;
  const mod = await loadModuleDynamically(configSujets0DataOnly.domtoimageUrl);
  window._domtoimage = mod.default;
  return window._domtoimage;
}

async function appendPngFromRenderedSvgColumn(table, results) {
  const domtoimage = await ensureDomToImage();

  for (let idx = 0; idx < results.length; idx++) {
    const row = table.rows[idx];
    if (!row) continue;
    const svgCell = row.cells[1]; // existing SVG column
    const renderedContainer = svgCell ? svgCell.querySelector('.graph-svg-container') : null;

    const newCell = row.insertCell(-1); // append at end
    newCell.style.width = "300px";
    newCell.style.border = "1px solid black";

    if (!renderedContainer) {
      newCell.textContent = "N/A";
      continue;
    }

    const result = results[idx];
    const width = result?.graphDict?.svg?.width || renderedContainer.clientWidth || 340;
    const height = result?.graphDict?.svg?.height || renderedContainer.clientHeight || 340;

    // Clone the rendered container offscreen and inline computed styles to detach from external CSS
    const offscreenWrapper = document.createElement('div');
    offscreenWrapper.style.position = 'absolute';
    offscreenWrapper.style.left = '-99999px';
    offscreenWrapper.style.top = '-99999px';
    const clone = renderedContainer.cloneNode(true);
    offscreenWrapper.appendChild(clone);
    document.body.appendChild(offscreenWrapper);

    // Inline computed styles for KaTeX subtree to ensure fidelity
    inlineComputedStylesForKatex(clone);

    // Ensure text sizing utility classes are available to the clone and inner SVG
    const sizeStyleTag = injectTextSizeStyles(clone);

    // Prefer targeting the inner SVG element for capture
    const targetNode = clone.querySelector('svg') || clone;

    try {
      const dataUrl = await domtoimage.toPng(targetNode, {
        width,
        height,
        style: { width: `${width}px`, height: `${height}px`, backgroundColor: 'white' },
        cacheBust: true,
        quality: 1.0,
      });
      const img = document.createElement('img');
      img.src = dataUrl;
      img.style.width = `${width}px`;
      img.style.height = `${height}px`;
      newCell.appendChild(img);
    } catch (e) {
      // Fallback: render cloned SVG via canvas
      try {
        const svgEl = targetNode.tagName && targetNode.tagName.toLowerCase() === 'svg' ? targetNode : clone.querySelector('svg');
        if (!svgEl) throw e;
        ensureSvgDimensions(svgEl, width, height);
        const serializer = new XMLSerializer();
        const svgStr = serializer.serializeToString(svgEl);
        const dataUrlSvg = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgStr);
        const pngDataUrl = await rasterizeSvgToPng(dataUrlSvg, width, height);
        if (pngDataUrl) {
          const img = document.createElement('img');
          img.src = pngDataUrl;
          img.style.width = `${width}px`;
          img.style.height = `${height}px`;
          newCell.appendChild(img);
        } else {
          newCell.textContent = 'N/A';
        }
      } catch (fallbackErr) {
        console.error('Both dom-to-image and fallback canvas conversion failed:', fallbackErr);
        newCell.textContent = 'N/A';
      }
    } finally {
      if (offscreenWrapper && offscreenWrapper.parentNode) {
        offscreenWrapper.parentNode.removeChild(offscreenWrapper);
      }
    }
  }
}

async function ensureHtmlToImage() {
  if (window._htmlToImage) return window._htmlToImage;
  const mod = await import('https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/+esm');
  window._htmlToImage = mod;
  return window._htmlToImage;
}

async function appendPngFromRenderedSvgColumn_htmlToImage(table, results) {
  const htmlToImage = await ensureHtmlToImage();

  for (let idx = 0; idx < results.length; idx++) {
    const row = table.rows[idx];
    if (!row) continue;
    const svgCell = row.cells[1];
    const renderedContainer = svgCell ? svgCell.querySelector('.graph-svg-container') : null;

    const newCell = row.insertCell(-1);
    newCell.style.width = "300px";
    newCell.style.border = "1px solid black";

    if (!renderedContainer) {
      newCell.textContent = "N/A";
      continue;
    }

    const result = results[idx];
    const width = result?.graphDict?.svg?.width || renderedContainer.clientWidth || 340;
    const height = result?.graphDict?.svg?.height || renderedContainer.clientHeight || 340;

    const offscreenWrapper = document.createElement('div');
    offscreenWrapper.style.position = 'absolute';
    offscreenWrapper.style.left = '-99999px';
    offscreenWrapper.style.top = '-99999px';
    const clone = renderedContainer.cloneNode(true);
    offscreenWrapper.appendChild(clone);
    document.body.appendChild(offscreenWrapper);

    inlineComputedStylesForKatex(clone);
    injectTextSizeStyles(clone);
    const targetNode = clone.querySelector('svg') || clone;

    try {
      const dataUrl = await htmlToImage.toPng(targetNode, {
        width,
        height,
        pixelRatio: Math.max(1, Math.floor(window.devicePixelRatio || 1)),
        cacheBust: true,
        style: { width: `${width}px`, height: `${height}px`, backgroundColor: 'white' },
        // Avoid scanning global stylesheets (CORS cssRules) by overriding font embedding
        fontEmbedCSS: '',
        fontEmbedHTML: '',
        // Additionally, skip link rel=stylesheet nodes inside the clone
        filter: (node) => {
          return !(node.tagName === 'LINK' && node.rel === 'stylesheet');
        },
      });
      const img = document.createElement('img');
      img.src = dataUrl;
      img.style.width = `${width}px`;
      img.style.height = `${height}px`;
      newCell.appendChild(img);
    } catch (e) {
      console.error('html-to-image conversion failed:', e);
      newCell.textContent = 'N/A';
    } finally {
      if (offscreenWrapper && offscreenWrapper.parentNode) {
        offscreenWrapper.parentNode.removeChild(offscreenWrapper);
      }
    }
  }
}

function ensureSvgDimensions(svgEl, width, height) {
  if (!svgEl.getAttribute('width')) svgEl.setAttribute('width', String(width));
  if (!svgEl.getAttribute('height')) svgEl.setAttribute('height', String(height));
  if (!svgEl.getAttribute('viewBox')) svgEl.setAttribute('viewBox', `0 0 ${width} ${height}`);
}

function rasterizeSvgToPng(svgDataUrl, width, height) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ratio = Math.max(1, Math.floor(window.devicePixelRatio || 1));
      canvas.width = width * ratio;
      canvas.height = height * ratio;
      const ctx = canvas.getContext('2d');
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(img, 0, 0, width, height);
      resolve(canvas.toDataURL('image/png'));
    };
    img.onerror = () => resolve(null);
    img.src = svgDataUrl;
  });
}

function inlineComputedStylesForKatex(root) {
  const nodes = root.querySelectorAll('.katex, .katex *');
  nodes.forEach((node) => inlineStyle(node));
}

function inlineStyle(element) {
  const computed = getComputedStyle(element);
  const style = element.style;
  copyStyleProp(style, computed, 'fontFamily');
  copyStyleProp(style, computed, 'fontSize');
  copyStyleProp(style, computed, 'fontStyle');
  copyStyleProp(style, computed, 'fontWeight');
  copyStyleProp(style, computed, 'lineHeight');
  copyStyleProp(style, computed, 'color');
  copyStyleProp(style, computed, 'backgroundColor');
  copyStyleProp(style, computed, 'letterSpacing');
  copyStyleProp(style, computed, 'wordSpacing');
  copyStyleProp(style, computed, 'textTransform');
  copyStyleProp(style, computed, 'textDecoration');
  copyStyleProp(style, computed, 'display');
  copyStyleProp(style, computed, 'whiteSpace');
  copyStyleProp(style, computed, 'margin');
  copyStyleProp(style, computed, 'padding');
  // borders
  copyStyleProp(style, computed, 'borderTop');
  copyStyleProp(style, computed, 'borderRight');
  copyStyleProp(style, computed, 'borderBottom');
  copyStyleProp(style, computed, 'borderLeft');
}

function copyStyleProp(style, computed, prop) {
  try { style[prop] = computed[prop]; } catch (_) { /* ignore */ }
}

function injectTextSizeStyles(container) {
  const css = `
.text-sm { font-size: 0.875rem !important; line-height: 1.25rem !important; }
.text-xs { font-size: 0.75rem !important; line-height: 1rem !important; }
.text-2xs { font-size: 0.625rem !important; line-height: 1 !important; }
.svg-latex .katex { font-size: inherit; }
`;
  // Only embed into inner SVG to avoid HTML serialization artifacts
  const svg = container.querySelector('svg');
  if (svg) {
    const svgStyle = document.createElementNS('http://www.w3.org/2000/svg', 'style');
    svgStyle.textContent = css;
    svg.insertBefore(svgStyle, svg.firstChild);
    return svgStyle;
  }
  return null;
}


// --- KaTeX Math Italic dynamic font injection helpers (local to ui.js) ---

const KATEX_VERSION = '0.16.9';
const KATEX_MATH_ITALIC_URL = `https://cdn.jsdelivr.net/npm/katex@${KATEX_VERSION}/dist/fonts/KaTeX_Math-Italic.woff2`;

async function fetchAsDataUrl(url, mime = 'font/woff2') {
  const resp = await fetch(url, { cache: 'force-cache' });
  if (!resp.ok) throw new Error(`Failed to fetch ${url}: ${resp.status}`);
  const buffer = await resp.arrayBuffer();
  const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
  return `data:${mime};base64,${base64}`;
}

async function getKatexMathItalicDataUrl() {
  if (window._katexMathItalicDataUrl) return window._katexMathItalicDataUrl;
  const dataUrl = await fetchAsDataUrl(KATEX_MATH_ITALIC_URL, 'font/woff2');
  window._katexMathItalicDataUrl = dataUrl;
  return dataUrl;
}

async function injectKatexMathItalicStyle(container) {
  try {
    const dataUrl = await getKatexMathItalicDataUrl();
    const style = document.createElement('style');
    style.setAttribute('data-temp-katex-css', 'true');
    style.textContent = `
@font-face {
  font-family: 'KaTeX_Math';
  font-style: italic;
  src: url('${dataUrl}') format('woff2');
  font-display: swap;
}
.katex { font-family: 'KaTeX_Math', 'KaTeX_Main', serif; }
.katex * { font-family: inherit !important; }
`;
    container.appendChild(style);
    return style;
  } catch (e) {
    // If injection fails, return null so the capture still proceeds
    return null;
  }
}

async function ensureKatexFontReady() {
  try {
    if (document.fonts && document.fonts.load) {
      await document.fonts.load('16px "KaTeX_Math"');
    }
  } catch (_) {
    // ignore
  }
}


