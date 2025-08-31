import { isSafari } from "./config.js";
import { S0 } from "./state.js";

let domtoimage;

export function setDomToImage(moduleDefault) {
  domtoimage = moduleDefault;
}

export function hasGraph(result) {
  return result.graphSvg !== null && result.graphDict !== null;
}

export async function prerenderLatexInSvg(svgString) {
  if (typeof katex === "undefined") {
    return svgString;
  }

  try {
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, "image/svg+xml");
    const svgElement = svgDoc.querySelector("svg");
    if (!svgElement) return svgString;

    const foreignObjects = svgElement.querySelectorAll("foreignObject");
    let hasUnrenderedLatex = false;

    foreignObjects.forEach((fo) => {
      const divs = fo.querySelectorAll("div.svg-latex");
      divs.forEach((div) => {
        if (div.querySelector(".katex")) return;
        const latex = div.textContent.trim();
        if (!latex) return;
        hasUnrenderedLatex = true;
        try {
          const bgColor = div.style.backgroundColor;
          const color = div.style.color;
          const rendered = katex.renderToString(latex, {
            throwOnError: false,
            displayMode: false,
          });
          div.innerHTML = rendered;
          if (bgColor) div.style.backgroundColor = bgColor;
          if (color) {
            const katexEls = div.querySelectorAll(".katex, .katex *");
            katexEls.forEach((el) => {
              el.style.color = color;
            });
          }
        } catch (e) {
          // keep original
        }
      });
    });

    if (!hasUnrenderedLatex) return svgString;

    // Inject KaTeX font and text-size utilities inside foreignObject content and into SVG
    await injectKatexFontAndSizing(svgElement);

    const serializer = new XMLSerializer();
    return serializer.serializeToString(svgElement);
  } catch (error) {
    return svgString;
  }
}

export async function prerenderLatexInAllResultsWithGraph(results) {
  for (const result of results) {
    if (hasGraph(result)) {
      result.graphSvgWithRenderedLatex = await prerenderLatexInSvg(
        result.graphSvg
      );
    }
  }
  return results;
}

async function convertSvgToPngWithDomToImage(svgString, options = {}) {
  try {
    const scale = options.scale || 1;
    let width = options.width || 340;
    let height = options.height || 340;

    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, "image/svg+xml");
    const svgElement = svgDoc.querySelector("svg");
    if (!svgElement) throw new Error("No SVG element found in string");

    const svgWidth = svgElement.getAttribute("width");
    const svgHeight = svgElement.getAttribute("height");
    const viewBox = svgElement.getAttribute("viewBox");
    if (svgWidth && svgHeight) {
      width = parseInt(svgWidth) || width;
      height = parseInt(svgHeight) || height;
    }
    svgElement.setAttribute("width", width);
    svgElement.setAttribute("height", height);
    if (!viewBox) svgElement.setAttribute("viewBox", `0 0 ${width} ${height}`);

    svgElement.style.backgroundColor = "white";
    //svgElement.style.fontFamily = "'Lexend', sans-serif";

    const serializer = new XMLSerializer();
    const updatedSvgString = serializer.serializeToString(svgElement);

    const tempDiv = document.createElement("div");
    tempDiv.style.position = "absolute";
    tempDiv.style.left = "-9999px";
    tempDiv.style.top = "-9999px";
    tempDiv.innerHTML = updatedSvgString;
    document.body.appendChild(tempDiv);

    const tempSvgElement = tempDiv.querySelector("svg");
    await new Promise((resolve) => setTimeout(resolve, 100));

    let pngDataUrl;
    try {
      pngDataUrl = await domtoimage.toPng(tempSvgElement, {
        width: width * scale,
        height: height * scale,
        style: {
          transform: `scale(${scale})`,
          transformOrigin: "top left",
          width: `${width}px`,
          height: `${height}px`,
        },
        quality: 1.0,
        cacheBust: true,
      });
    } catch (error) {
      console.error("Error converting SVG to PNG:", error);
    }

    if (tempDiv && tempDiv.parentNode) {
      tempDiv.parentNode.removeChild(tempDiv);
    }
    return pngDataUrl || null;
  } catch (error) {
    console.error("Error converting SVG to PNG:", error);
    return null;
  }
}

export async function convertAllGraphsToPng(results) {
  if (isSafari()) return results;
  for (const result of results) {
    if (hasGraph(result) && result.graphSvgWithRenderedLatex) {
      const dimensions = {
        width: result.graphDict?.svg?.width || 340,
        height: result.graphDict?.svg?.height || 340,
      };
      const pngDataUrl = await convertSvgToPngWithDomToImage(
        result.graphSvgWithRenderedLatex,
        { width: dimensions.width, height: dimensions.height }
      );
      if (pngDataUrl) {
        result.graphPng = pngDataUrl;
        result.graphDimensions = dimensions;
      }
    }
  }
  return results;
}


// Alternative implementation using canvg to rasterize SVG strings
export async function convertAllGraphsToPng_canvg(results) {
  if (isSafari()) return results;
  let CanvgMod;
  try {
    CanvgMod = await import('https://cdn.jsdelivr.net/npm/canvg@4.0.1/+esm');
  } catch (e) {
    console.error('Failed to load canvg:', e);
    return results;
  }

  for (const result of results) {
    if (hasGraph(result) && result.graphSvgWithRenderedLatex) {
      const width = result.graphDict?.svg?.width || 340;
      const height = result.graphDict?.svg?.height || 340;

      try {
        const canvas = document.createElement('canvas');
        const ratio = Math.max(1, Math.floor(window.devicePixelRatio || 1));
        canvas.width = width * ratio;
        canvas.height = height * ratio;
        const ctx = canvas.getContext('2d');
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';

        const v = await CanvgMod.Canvg.fromString(ctx, result.graphSvgWithRenderedLatex);
        await v.render();

        result.graphPng = canvas.toDataURL('image/png');
        result.graphDimensions = { width, height };
      } catch (e) {
        console.error('canvg rendering failed:', e);
      }
    }
  }
  return results;
}


// --- Early KaTeX font and sizing injection (applies during prerender) ---

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

async function injectKatexFontAndSizing(svgElement) {
  try {
    const dataUrl = await getKatexMathItalicDataUrl();
    const css = `
@font-face {
  font-family: 'KaTeX_Math';
  font-style: italic;
  src: url('${dataUrl}') format('woff2');
  font-display: swap;
}
.katex { font-family: 'KaTeX_Math', 'KaTeX_Main', serif; }
.katex * { font-family: inherit !important; }
.text-sm { font-size: 0.875rem !important; line-height: 1.25rem !important; }
.text-xs { font-size: 0.75rem !important; line-height: 1rem !important; }
.text-2xs { font-size: 0.625rem !important; line-height: 1 !important; }
.svg-latex .katex { font-size: inherit; }
`;

    // 1) Inject into SVG <style> for baseline availability (use proper SVG namespace)
    const svgStyle = svgElement.ownerDocument.createElementNS('http://www.w3.org/2000/svg', 'style');
    svgStyle.textContent = css;
    svgElement.insertBefore(svgStyle, svgElement.firstChild);
    // NOTE: Avoid injecting <style> tags inside foreignObject HTML to prevent
    // serialization artifacts during PNG rasterization.

    // Ensure font readiness if supported
    try {
      if (document.fonts && document.fonts.load) {
        await document.fonts.load('16px "KaTeX_Math"');
      }
    } catch (_) { /* ignore */ }
  } catch (_) {
    // If injection fails, continue without blocking
  }
}


