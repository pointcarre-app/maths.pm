/**
 * Sujets0 Question Generator - Comprehensive Script Module
 * Generates mathematics questions using Nagini Python execution engine
 * with KaTeX rendering and graph generation support
 */

// At the very top:
window.delayMathRendering = true;

// TODO : create config.js like in /sujets0-data-only/config.js

console.log("🎯 Sujets0 Question Generator loading...");

// Write a function to extract the config from the URL query parameters
function extractConfigFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  let nbStudents = parseInt(urlParams.get("nbStudents")) || 2;
  let nbQuestions = parseInt(urlParams.get("nbQuestions")) || 12;
  const curriculum = urlParams.get("curriculum");
  const curriculumSlug = urlParams.get("curriculum-slug");

  // Cap values at their limits and show toasts
  if (nbStudents > 50) {
    nbStudents = 50;
    setTimeout(
      () =>
        showToast(
          "📊 Nombre de copies limité à 50 (maximum autorisé)",
          "warning"
        ),
      100
    );
  }
  if (nbStudents < 1) {
    nbStudents = 1;
    setTimeout(
      () =>
        showToast("📊 Nombre de copies ajusté à 1 (minimum requis)", "warning"),
      100
    );
  }

  if (nbQuestions > 12) {
    nbQuestions = 12;
    setTimeout(
      () =>
        showToast(
          "📝 Nombre de questions limité à 12 (maximum de générateurs disponibles)",
          "warning"
        ),
      200
    );
  }
  if (nbQuestions < 1) {
    nbQuestions = 1;
    setTimeout(
      () =>
        showToast(
          "📝 Nombre de questions ajusté à 1 (minimum requis)",
          "warning"
        ),
      200
    );
  }

  return { nbStudents, nbQuestions, curriculum, curriculumSlug };
}

const configFromUrl = extractConfigFromUrl();

function showToast(message, type = "error") {
  const toast = document.createElement("div");
  toast.className = `alert alert-${type} fixed top-4 left-1/2 transform -translate-x-1/2 w-auto max-w-md shadow-lg z-50`;
  toast.innerHTML = `
      <div>
          <span>${message}</span>
      </div>
    `;
  document.body.appendChild(toast);

  // Auto-remove toast after 5 seconds
  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);
    }
  }, 5000);
}

// Config validation and capping is now handled in extractConfigFromUrl()

console.log("🟪🟪🟪 url config", extractConfigFromUrl());

const teachersGitTag = "v0.0.27";

// Configuration constants
const CONFIG = {
  teachersGitTag: teachersGitTag,
  naginiGitTag: "v0.0.21",
  v4PyJsGitTag: "v0.0.27",
  rootSeed: 14,
  nbStudents: configFromUrl.nbStudents,
  nbQuestions: configFromUrl.nbQuestions,
  curriculum: configFromUrl.curriculum,
  curriculumSlug: configFromUrl.curriculumSlug,
  // CDN URLs
  naginiJsUrl:
    "https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js?bundle",
  naginiPyodideWorkerUrl:
    "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js",
  v4PyJsPCAGraphLoaderUrl:
    "https://cdn.jsdelivr.net/gh/pointcarre-app/v4.py.js@v0.0.27/scenery/packaged/PCAGraphLoader.js",

  // Teacher module URLs
  teachersUrlsToPaths: [
    {
      url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/__init__.py`,
      path: "teachers/__init__.py",
    },
    {
      url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/generator.py`,
      path: "teachers/generator.py",
    },
    {
      url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/maths.py`,
      path: "teachers/maths.py",
    },
    { 
      url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/formatting.py`,
      path: "teachers/formatting.py",
    },
    {
      url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/corrector.py`,
      path: "teachers/corrector.py",
    },
    {
      url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/defaults.py`,
      path: "teachers/defaults.py",
    },
  ],

  // Generator files
  generators: [
    // "spe_sujet1_auto_01_question.py",
    // "spe_sujet1_auto_02_question.py",
    // "spe_sujet1_auto_03_question.py",
    // "spe_sujet1_auto_04_question.py",
    // "spe_sujet1_auto_05_question.py",
    // "spe_sujet1_auto_06_question.py",
    // "spe_sujet1_auto_07_question.py",
    // "spe_sujet1_auto_08_question.py",
    // "spe_sujet1_auto_09_question.py",
    // "spe_sujet1_auto_10_question.py",
    // "spe_sujet1_auto_11_question.py",
    // "spe_sujet1_auto_12_question.py",
    "spe_sujet2_auto_01_question.py",
    "spe_sujet2_auto_02_question.py",
    "spe_sujet2_auto_03_question.py",
    "spe_sujet2_auto_04_question.py",
    "spe_sujet2_auto_05_question.py",
    "spe_sujet2_auto_06_question.py",
    "spe_sujet2_auto_07_question.py",
    "spe_sujet2_auto_08_question.py",
    "spe_sujet2_auto_09_question.py",
    "spe_sujet2_auto_10_question.py",
    "spe_sujet2_auto_11_question.py",
    "spe_sujet2_auto_12_question.py",
    "gen_sujet2_auto_01_question.py",
    "gen_sujet2_auto_02_question.py",
    "gen_sujet2_auto_03_question.py",
    "gen_sujet2_auto_04_question.py",
    "gen_sujet2_auto_05_question.py",
    "gen_sujet2_auto_06_question.py",
    "gen_sujet2_auto_07_question.py",
    "gen_sujet2_auto_08_question.py",
    "gen_sujet2_auto_09_question.py",
    "gen_sujet2_auto_10_question.py",
    "gen_sujet2_auto_11_question.py",
    "gen_sujet2_auto_12_question.py",
  ],

  // Graph mappings
  generatorsToGraphs: {
    "spe_sujet1_auto_07_question.py": ["q7_small"],
    "spe_sujet1_auto_08_question.py": ["q8_small"],
    "spe_sujet1_auto_09_question.py": ["q9_small"],
    "spe_sujet1_auto_10_question.py": ["q10_small"],
    "spe_sujet1_auto_11_question.py": [
      "q11_case_a_small",
      "q11_case_b_small",
      "q11_case_c_small",
    ],
    "spe_sujet1_auto_12_question.py": [
      "parabola_s1_a0",
      "parabola_s1_am5",
      "parabola_s1_ap5",
      "parabola_sm1_a0",
      "parabola_sm1_am5",
      "parabola_sm1_ap10",
    ],
  },
};

// Global state
const STATE = {
  nagini: { module: null, manager: null, ready: false },
  pca: { loaderClass: null, loaderInstance: null },
  results: { questionResults: [] },
  ui: { container: null, loading: false },
};

// Utility functions
function isSafari() {
  return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

function getBasePath() {
  if (window.location.hostname === "pointcarre-app.github.io") {
    return "/maths.pm";
  } else if (window.location.pathname.startsWith("/maths.pm/")) {
    return "/maths.pm";
  }
  return "";
}

// Core initialization functions
async function loadNagini() {
  try {
    console.log("📦 Loading Nagini...");
    const naginiModule = await import(CONFIG.naginiJsUrl);
    STATE.nagini.module = naginiModule.Nagini;
    window.Nagini = naginiModule.Nagini;

    const manager = await naginiModule.Nagini.createManager(
      "pyodide",
      ["sympy", "pydantic", "strictyaml"],
      [],
      CONFIG.teachersUrlsToPaths,
      CONFIG.naginiPyodideWorkerUrl
    );

    await naginiModule.Nagini.waitForReady(manager);
    STATE.nagini.manager = manager;
    STATE.nagini.ready = true;

    console.log("✅ Nagini loaded and ready");
    return true;
  } catch (error) {
    console.error("❌ Failed to initialize Nagini:", error);
    STATE.nagini.ready = false;
    return false;
  }
}

async function loadPCAGraphLoader() {
  try {
    console.log("📊 Loading PCA Graph Loader...");
    const module = await import(CONFIG.v4PyJsPCAGraphLoaderUrl);
    STATE.pca.loaderClass = module.PCAGraphLoader;

    // Initialize the loader with proper config
    const instance = new module.PCAGraphLoader({
      debug: false,
      graphConfig: {},
      pcaVersion: CONFIG.v4PyJsGitTag,
    });

    await instance.initialize();
    STATE.pca.loaderInstance = instance;
    console.log("✅ PCA Graph Loader ready");
    return true;
  } catch (error) {
    console.error("❌ Failed to load PCA Graph Loader:", error);
    return false;
  }
}

// Question generation functions
async function executeGeneratorWithSeed(filename, seed) {
  const manager = STATE.nagini.manager;
  if (!manager) {
    return { success: false, error: "Nagini manager not initialized" };
  }

  const basePath = getBasePath();
  const url = `${basePath}/static/sujets0/generators/${filename}`;

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);

    let pythonCode = await response.text();

    // Also random.Seed in some generators... TODO sel
    // seems better here only
    // Technically the same seed
    // But this doesnt run in doppel:backend..
    // so duplication for safety locally + ??
    // compare wiyh a new doppel

    // Inject seed
    // Seed injection is done for random in sujets0_question_generator_v1.js
    const seedInjection = `\nimport random\nrandom.seed(${seed})\n\n# Override the default SEED\nimport teachers.defaults\nteachers.defaults.SEED = ${seed}\n\n`;

    pythonCode = pythonCode.replace(
      "components = generate_components(None)",
      `components = generate_components(None, ${seed})`
    );
    pythonCode = seedInjection + pythonCode;

    const result = await manager.executeAsync(filename, pythonCode);
    const success = !result.error && (result.exit_code === 0 || result.missive);

    if (result.missive && success) {
      try {
        const data = JSON.parse(result.missive);
        return {
          success: true,
          statement: data.statement || data.question,
          statementHtml: data.statement_html,
          answer: data.answer,
          data: data,
          stdout: result.stdout,
          stderr: result.stderr,
        };
      } catch (e) {
        return { success: false, error: "Failed to parse output" };
      }
    } else {
      return {
        success: false,
        error: result.error || "Execution failed",
        stdout: result.stdout,
        stderr: result.stderr,
      };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function buildPCAGraph(graphKey, params = {}) {
  if (!STATE.pca.loaderInstance) {
    console.warn("PCA Graph Loader not initialized, skipping graph generation");
    return { svg: null, graphDict: null };
  }

  try {
    // Update config if params provided
    if (params && Object.keys(params).length > 0) {
      STATE.pca.loaderInstance.updateConfig(params);
    }

    const result = await STATE.pca.loaderInstance.renderGraph(graphKey);
    return {
      svg: result.svg,
      graphDict: result.graphDict || result,
    };
  } catch (error) {
    console.error(`Failed to build graph ${graphKey}:`, error);
    return { svg: null, graphDict: null };
  }
}

async function attachGraphToResult(result, generator) {
  try {
    if (generator === "spe_sujet1_auto_07_question.py") {
      const Y_LABEL_FOR_HORIZONTAL_LINE = parseInt(result.data.components.n);
      console.log(
        `🎨 Generating graph q7_small with Y_LABEL_FOR_HORIZONTAL_LINE=${Y_LABEL_FOR_HORIZONTAL_LINE}`
      );
      const svgAndDict = await buildPCAGraph("q7_small", {
        Y_LABEL_FOR_HORIZONTAL_LINE,
      });
      result.graphSvg = svgAndDict.svg;
      result.graphDict = svgAndDict.graphDict;
    } else if (generator === "spe_sujet1_auto_08_question.py") {
      const A_FLOAT_FOR_AFFINE_LINE = parseFloat(
        result.data.components_evaluated.a
      );
      const B_FLOAT_FOR_AFFINE_LINE = parseFloat(
        result.data.components_evaluated.b
      );
      console.log(
        `🎨 Generating graph q8_small with A=${A_FLOAT_FOR_AFFINE_LINE}, B=${B_FLOAT_FOR_AFFINE_LINE}`
      );
      const svgAndDict = await buildPCAGraph("q8_small", {
        A_FLOAT_FOR_AFFINE_LINE,
        B_FLOAT_FOR_AFFINE_LINE,
      });
      result.graphSvg = svgAndDict.svg;
      result.graphDict = svgAndDict.graphDict;
    } else if (generator === "spe_sujet1_auto_10_question.py") {
      const aFromParabola = parseInt(result.data.components.a);
      const cFromParabola = parseInt(result.data.components.c);
      let PARABOLA_GRAPH_KEY;
      const A_SHIFT_MAGNITUDE = Math.abs(cFromParabola);

      if (aFromParabola > 0) {
        if (cFromParabola > 0) PARABOLA_GRAPH_KEY = "parabola_s1_ap";
        else if (cFromParabola < 0) PARABOLA_GRAPH_KEY = "parabola_s1_am";
        else PARABOLA_GRAPH_KEY = "parabola_s1_a0";
      } else {
        if (cFromParabola > 0) PARABOLA_GRAPH_KEY = "parabola_sm1_ap";
        else if (cFromParabola < 0) PARABOLA_GRAPH_KEY = "parabola_sm1_am";
        else PARABOLA_GRAPH_KEY = "parabola_sm1_a0";
      }

      const svgAndDict = await buildPCAGraph(PARABOLA_GRAPH_KEY, {
        A_SHIFT_MAGNITUDE,
      });
      result.graphSvg = svgAndDict.svg;
      result.graphDict = svgAndDict.graphDict;
    } else if (generator === "spe_sujet1_auto_11_question.py") {
      const caseFromGenerator = result.data.components.case;
      let key;
      if (caseFromGenerator === "case_a") key = "q11_case_a_small";
      else if (caseFromGenerator === "case_b") key = "q11_case_b_small";
      else if (caseFromGenerator === "case_c") key = "q11_case_c_small";
      else throw new Error(`Invalid case: ${caseFromGenerator}`);

      const svgAndDict = await buildPCAGraph(key, {});
      result.graphSvg = svgAndDict.svg;
      result.graphDict = svgAndDict.graphDict;
    }
  } catch (error) {
    console.error(`Failed to attach graph for ${generator}:`, error);
  }
}

// SVG Inline Styles Mapping (from pm.css and utility classes)
const SVG_INLINE_STYLES = {
  svg: {
    display: "block",
    "max-width": "100%",
    height: "auto",
  },
  foreignObject: {
    overflow: "visible",
  },
  "foreignObject > div": {
    width: "100%",
    height: "100%",
    display: "flex",
    "align-items": "center",
    "justify-content": "center",
  },
  ".svg-latex": {
    "line-height": "1.2",
    "text-align": "center",
  },
  ".svg-latex .katex": {
    "font-family": "'KaTeX_Main', sans-serif",
  },
  // Font size utility classes
  ".text-sm": {
    "font-size": "0.875rem",
    "line-height": "1.25rem",
  },
  ".text-xs": {
    "font-size": "0.75rem",
    "line-height": "1rem",
  },
  ".text-2xs": {
    "font-size": "0.625rem",
    "line-height": "1rem",
  },
};

// Helper function to apply inline styles to an element
function applyInlineStyles(element, styles) {
  Object.entries(styles).forEach(([property, value]) => {
    // Convert kebab-case to camelCase for style properties
    const camelProperty = property.replace(/-([a-z])/g, (match, letter) =>
      letter.toUpperCase()
    );
    element.style[camelProperty] = value;
  });
}

// Helper function to apply styles based on CSS classes
function applyStylesFromClasses(element) {
  const classList = Array.from(element.classList);

  classList.forEach((className) => {
    const styleKey = `.${className}`;
    if (SVG_INLINE_STYLES[styleKey]) {
      applyInlineStyles(element, SVG_INLINE_STYLES[styleKey]);
    }
  });

  // Also apply to nested elements with these classes
  ["text-sm", "text-xs", "text-2xs"].forEach((textClass) => {
    const elements = element.querySelectorAll(`.${textClass}`);
    elements.forEach((el) => {
      if (SVG_INLINE_STYLES[`.${textClass}`]) {
        applyInlineStyles(el, SVG_INLINE_STYLES[`.${textClass}`]);
      }
    });
  });
}

// SVG KaTeX Processing with Inline Styles (inspired by index-graphs.js)
async function processKatexInSvg(svgString) {
  if (typeof katex === "undefined") {
    console.warn("KaTeX not available for SVG processing");
    return svgString;
  }

  try {
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, "image/svg+xml");
    const svgElement = svgDoc.querySelector("svg");
    if (!svgElement) return svgString;

    // Apply inline styles to SVG element
    svgElement.classList.add("graph-svg-container");
    applyInlineStyles(svgElement, SVG_INLINE_STYLES.svg);
    console.log("🎨 Applied inline styles to SVG element");

    // Find all foreignObject elements and apply styles
    const foreignObjects = svgElement.querySelectorAll("foreignObject");

    foreignObjects.forEach((fo) => {
      // Apply inline styles to foreignObject
      applyInlineStyles(fo, SVG_INLINE_STYLES.foreignObject);

      // Apply styles to direct child divs of foreignObject
      const childDivs = fo.querySelectorAll(":scope > div");
      childDivs.forEach((div) => {
        applyInlineStyles(div, SVG_INLINE_STYLES["foreignObject > div"]);
        // Apply font size classes if present
        applyStylesFromClasses(div);
      });
    });

    foreignObjects.forEach((fo) => {
      // Find div.svg-latex elements (exactly like index-graphs.js)
      const latexDivs = fo.querySelectorAll("div.svg-latex");

      latexDivs.forEach((div) => {
        div.classList.add("svg-latex");
        // Apply inline styles to svg-latex elements
        applyInlineStyles(div, SVG_INLINE_STYLES[".svg-latex"]);
        // Apply font size classes if present
        applyStylesFromClasses(div);

        const latex = div.textContent.trim();
        if (!latex) return;

        try {
          // Preserve original styling
          const bgColor = div.style.backgroundColor;
          const color = div.style.color;

          // Clear and render KaTeX directly (like index-graphs.js line 94-98)
          div.innerHTML = "";
          katex.render(latex, div, {
            throwOnError: false,
            displayMode: false,
          });

          // Apply inline styles to rendered KaTeX elements
          const katexElements = div.querySelectorAll(".katex");
          katexElements.forEach((katexEl) => {
            applyInlineStyles(katexEl, SVG_INLINE_STYLES[".svg-latex .katex"]);

            // Apply font family AND size to all nested elements in KaTeX
            katexEl.querySelectorAll("*").forEach((nestedEl) => {
              nestedEl.style.fontFamily = "'KaTeX_Main', sans-serif";
              // Inherit font size from parent div (which has text-2xs, text-xs, etc.)
              nestedEl.style.fontSize = "inherit";
            });

            // Also ensure the katex root element inherits size
            katexEl.style.fontSize = "inherit";
          });

          // Restore colors (like index-graphs.js line 99-105)
          if (bgColor) div.style.backgroundColor = bgColor;
          if (color) {
            div.querySelectorAll(".katex, .katex *").forEach((el) => {
              el.style.color = color;
            });
          }
        } catch (e) {
          console.error("KaTeX error in SVG:", e);
          div.textContent = latex; // Fallback to original
        }
      });
    });

    // Final pass: apply font size classes to any remaining elements in the entire SVG
    ["text-sm", "text-xs", "text-2xs"].forEach((textClass) => {
      const elements = svgElement.querySelectorAll(`.${textClass}`);
      elements.forEach((el) => {
        if (SVG_INLINE_STYLES[`.${textClass}`]) {
          applyInlineStyles(el, SVG_INLINE_STYLES[`.${textClass}`]);

          // AGGRESSIVE: Force font size on all nested elements too
          const fontSize = SVG_INLINE_STYLES[`.${textClass}`]["font-size"];
          const lineHeight = SVG_INLINE_STYLES[`.${textClass}`]["line-height"];

          el.querySelectorAll("*").forEach((nestedEl) => {
            nestedEl.style.fontSize = fontSize;
            nestedEl.style.lineHeight = lineHeight;
          });

          console.log(
            `🎨 Applied ${textClass} inline styles (${fontSize}) to element and all children`
          );
        }
      });
    });

    // Serialize back to string with processed KaTeX and inlined styles
    const serializer = new XMLSerializer();
    return serializer.serializeToString(svgElement);
  } catch (error) {
    console.error("SVG KaTeX processing failed:", error);
    return svgString; // Return original on error
  }
}

// Print functionality
function addPrintButton(container) {
  // Create Table of Contents container
  const tocAndPrintButtonContainer = document.createElement("div");
  tocAndPrintButtonContainer.className =
    "toc-container w-full mb-4 print-hide mt-6";
  tocAndPrintButtonContainer.innerHTML = `
  <style>
  .list-sujets0-questions-generator-report li {
    margin-bottom: 0.5rem;
    margin-left: 0.5rem;
  }
  </style>
    <button id="print-questions-btn" class="btn btn-primary print-hide mb-6 w-full">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" 
                      d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z">
              </path>
          </svg>
          Imprimer
      </button>
    <details class="teacher-answer-details" open>
        <summary class="teacher-summary">
            Informations
        </summary>
        <div>
            <div class="p-0 mt-4 mb-7 text-sm">
                <ul class="list-none list-sujets0-questions-generator-report">
                    <li>‼️ Lors de l'impression, il faut activer les "Graphiques d'arrière-plan" (ne peut être fait que manuellement dans la fenêtre d'impression). Vous pouvez lire <a class="underline underline-offset-1 hover:underline-offset-4" href="">notre documentation à ce sujet</a>.</li>
                    <li>‼️ Ne fonctionne pas sur Safari <a class="underline underline-offset-1 hover:underline-offset-4" href="">(malgré beaucoup de bonne volonté)</a></li>
                    <li>🟢 Optimisé pour Firefox & Chrome</li>   
                    <li>🟢 Corrigé enseignant inclus</li>
                    <li>🟢 Reproductibilité grâce à la <code>seed</code> <span class="italic">(graine)</span></li>
                    <li>🟢 Possibilité d'ajuster les marges pour l'impression</li>
                </ul>
            </div>
        </div>
    </details>
    <details class="teacher-answer-details toc-details mb-4">
        <summary class="teacher-summary">
            Accès aux éléments imprimables
        </summary>
        <div class="border border-gray-200 rounded-lg p-3 mt-2">
            <div id="toc-links" class="max-h-[300px] overflow-y-auto space-y-1">
                <div class="text-xs text-gray-500 italic">Le sommaire sera généré après le chargement des questions...</div>
            </div>
        </div>
    </details>`;
  container.appendChild(tocAndPrintButtonContainer);
  // Add click handler
  const printBtn = tocAndPrintButtonContainer.querySelector(
    "#print-questions-btn"
  );
  printBtn.addEventListener("click", handlePrint);
}

// <h3 class="text-xl sm:text-2xl font-semibold mb-2 text-gray-800 mt-6">📋 Au sujet de la génération</h3>
// <h3 class="text-xl sm:text-2xl font-semibold mb-2 text-gray-800">🖨️ Au sujet de l'impression</h3>

function handlePrint() {
  // Create print-specific styles if they don't exist
  addPrintStyles();

  // Mark the container for printing
  const pmContainer = document.querySelector(
    ".pm-container .max-w-\\[640px\\]"
  );
  if (pmContainer) {
    pmContainer.classList.add("print-target");
  }

  // Try to use the modern print API with no margins
  if (window.navigator && window.navigator.userAgent.includes("Chrome")) {
    // For Chrome, we can try to influence print settings via CSS
    // The print dialog will open but user may need to select "More settings" > "Margins" > "None"
    console.log(
      '💡 Chrome detected: Please select "More settings" > "Margins" > "None" in print dialog'
    );
  }

  // Small delay to ensure styles are applied
  setTimeout(() => {
    // Trigger print dialog
    window.print();

    // Clean up after print dialog closes
    setTimeout(() => {
      if (pmContainer) {
        pmContainer.classList.remove("print-target");
      }
    }, 1000);
  }, 50);
}

function addPrintStyles() {
  const existingStyles = document.querySelector("#sujets0-print-styles");
  if (existingStyles) return;

  // Add Firefox detection class for browser-specific styling
  if (navigator.userAgent.includes('Firefox')) {
    document.body.classList.add('firefox-print');
  }

  const printStyles = document.createElement("style");
  printStyles.id = "sujets0-print-styles";
  printStyles.textContent = `
        @media print {
            /* Remove all default margins and padding */
            @page {
                margin: 0 !important;
                padding: 1cm !important;
                size: A4;
            }
            
            /* Hide everything by default */
            body * {
                visibility: hidden;
            }
            
            /* Show only the print target and its children */
            .print-target,
            .print-target * {
                visibility: visible;
            }
            
            /* Position the print target with minimal margins */
            .print-target {
                position: absolute;
                left: 0;
                top: 0;
                width: 100% !important;
                max-width: none !important;
                margin: 0 !important;
                padding: 10px !important;
            }
            
            /* Remove body margins */
            body {
                margin: 0 !important;
                padding: 0 !important;
            }
            
            /* Hide print button and other UI elements */
            .print-hide,
            .print-button-container,
            .toc-container,
            .navbar,
            .footer,
            .sidebar-fixed {
                display: none !important;
            }
            
            /* Page break before each h2 EXCEPT the teacher copy */
            .fragment-wrapper[data-f_type="h2_"]:not(:first-of-type) {
                page-break-before: always;
            }
            
            /* Keep header and teacher table together - more specific targeting */
            .fragment-wrapper:first-child,
            .fragment-wrapper:first-child + .fragment-wrapper,
            .fragment-wrapper:nth-child(2),
            .fragment-wrapper:nth-child(3) {
                page-break-before: avoid !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
            }
            
            /* Hide the screen-only details version during print */
            .screen-only {
                display: none !important;
            }
            
            /* Show the print-only teacher table */
            .print-only-teacher-table {
                display: block !important;
                margin-bottom: 1rem !important;
            }
            
            /* Ensure the print table is visible */
            .print-only-teacher-table table {
                display: table !important;
                visibility: visible !important;
                opacity: 1 !important;
            }
            
            /* Style the print-only heading */
            .print-only-teacher-table h3 {
                font-size: 14pt !important;
                font-weight: 600 !important;
                margin-bottom: 0.5rem !important;
                color: black !important;
            }
            
            /* Hide TOC details during print */
            .toc-details {
                display: none !important;
            }
            
            /* Specifically target the teacher answer table to stay with header */
            #teacher-answer-table,
            .teacher-table-section,
            .fragment-wrapper.teacher-table-section,
            .fragment-wrapper:has(#teacher-answer-table),
            .fragment-wrapper[data-f_type="p_"]:has(#teacher-answer-table) {
                page-break-before: avoid !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            
            /* Keep table together with previous content - multiple approaches for browser compatibility */
            .fragment-wrapper[data-f_type="p_"] table,
            table {
                page-break-before: avoid !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            
            /* Force first several fragments to stay together - multiple approaches */
            .fragment-wrapper:nth-child(-n+4) {
                page-break-before: avoid !important;
                page-break-after: avoid !important;
                break-after: avoid !important;
            }
            
            /* Firefox: Try to keep first page content together */
            .firefox-print .fragment-wrapper:first-child {
                page-break-after: avoid !important;
            }
            
            .firefox-print .fragment-wrapper:nth-child(2) {
                page-break-before: avoid !important;
                page-break-after: avoid !important;
            }
            
            .firefox-print .fragment-wrapper:nth-child(3) {
                page-break-before: avoid !important;
            }
            
            /* Alternative approach: explicitly target the sequence we want together */
            .fragment-wrapper:first-of-type ~ .fragment-wrapper.teacher-table-section {
                page-break-before: avoid !important;
                break-before: avoid !important;
            }
            
            /* Ensure the divider after teacher table doesn't force a break */
            .fragment-wrapper[data-f_type="hr_"]:nth-child(-n+5) {
                page-break-before: avoid !important;
                page-break-after: auto;
            }
            
            /* Avoid breaking inside divisions/questions */
            .fragment-wrapper {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Special handling for question blocks with graphs */
            .fragment-wrapper[data-f_type="p_"] {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Ensure graphs don't get cut */
            .graph-svg-container {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Adjust font sizes for print */
            body {
                font-size: 12pt;
                line-height: 1.4;
            }
            
            /* Specific paragraph and content font sizes */
            .print-target p,
            .print-target .fragment p,
            .print-target .fragment-wrapper p,
            .print-target div {
                font-size: 12pt !important;
                line-height: 1.5 !important;
            }
            
            /* Question text in flex containers */
            .print-target .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] > div,
            .print-target .fragment-wrapper[data-f_type="p_"] div > div {
                font-size: 12pt !important;
                line-height: 1.5 !important;
            }
            
            /* Headers */
            h1, .print-target h1 { font-size: 18pt !important; }
            h2, .print-target h2 { foformat: Copy-Seed-Q#nt-size: 16pt !important; }
            h3, .print-target h3 { font-size: 14pt !important; }
            
            /* Math expressions - force base-content/black color for all KaTeX elements */
            .katex, .print-target .katex,
            .katex *, .print-target .katex * {
                font-size: 12pt !important;
                color: var(--color-base-content, black) !important;
            }
            
            /* Ensure SVGs scale properly */
            svg {
                max-width: 100%;
                height: auto;
            }

            /* Utilities */
            .text-primary {
                color: black;
            }

            .text-secondary {
                color: black;
            }

            .text-accent {
                color: black;
            }
            
            /* Hide details styling for print */
            .teacher-answer-details[open] summary::before,
            .teacher-answer-details summary::before {
                display: none !important;
            }
            
            /* Hide the native disclosure triangle for print */
            .teacher-answer-details summary::-webkit-details-marker,
            .teacher-answer-details summary::marker {
                display: none !important;
            }
            
            /* Preserve flex layouts for print - keep question and graph side by side */
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] {
                display: flex !important;
                flex-wrap: wrap !important;
                gap: 15px !important;
                align-items: flex-start !important;
            }
            
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] > div {
                margin-bottom: 0 !important;
            }
            
            /* Ensure text content has proper width in flex */
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] > div:first-child {
                flex: 1 1 250px !important;
                min-width: 250px !important;
            }
            
            /* Ensure graph containers maintain their size */
            .fragment-wrapper[data-f_type="p_"] div[style*="display: flex"] .graph-svg-container {
                flex: 0 1 auto !important;
                max-width: 300px !important;
            }
            
            /* Note: SVG styles are now inlined directly into SVG elements for better print compatibility */
            /* Container wrapper still needs this for layout */
            .graph-svg-container {
                position: relative !important;
                display: block !important;
                overflow: hidden !important;
            }
            
            /* Firefox-specific print fixes - back to combined approach but smarter */
            .firefox-print .fragment-wrapper.firefox-parameters-section {
                page-break-after: avoid !important;
                break-after: avoid !important;
                -moz-column-break-after: avoid !important;
                margin-bottom: 0.25rem !important;
            }
            
            .firefox-print .fragment-wrapper.firefox-teacher-section {
                page-break-before: avoid !important;
                break-before: avoid !important;
                -moz-column-break-before: avoid !important;
                margin-top: 0 !important;
                page-break-inside: auto !important;
            }
            
            /* Firefox: Allow teacher table to break if absolutely necessary */
            .firefox-print .firefox-teacher-table,
            .firefox-print .print-only-teacher-table {
                page-break-inside: auto !important;
                break-inside: auto !important;
            }
            
            /* Firefox: Remove any potential title spacing and force table to top */
            .firefox-print .print-only-teacher-table {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* Firefox: Ensure table starts immediately without gaps */
            .firefox-print .print-only-teacher-table table {
                margin-top: 0 !important;
                border-collapse: collapse !important;
            }
            
            /* Firefox: Make tables more compact to fit together */
            .firefox-print .firefox-parameters-table,
            .firefox-print .print-only-teacher-table table {
                font-size: 11pt !important;
                line-height: 1.3 !important;
            }
            
            .firefox-print .firefox-parameters-table td,
            .firefox-print .print-only-teacher-table td {
                padding: 4px 8px !important;
            }
            
            /* Firefox: Reduce spacing between the two table sections */
            .firefox-print .firefox-parameters-section {
                margin-bottom: 0.5rem !important;
            }
            
            .firefox-print .firefox-teacher-section {
                margin-top: 0 !important;
            }
            
            /* Firefox: Force teacher table to stay together as one unit */
            .firefox-print .print-only-teacher-table {
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                -moz-column-break-inside: avoid !important;
            }
            
            /* Ensure parameters table stays with teacher section in Firefox */
            .firefox-print .fragment-wrapper:has(table):nth-child(-n+3),
            .firefox-print .parameters-table-section,
            .firefox-print .parameters-table-wrapper,
            .firefox-print .parameters-table {
                page-break-after: avoid !important;
                break-after: avoid !important;
                -moz-column-break-after: avoid !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
            }
            
            /* Firefox table handling */
            .firefox-print .fragment-wrapper[data-f_type="p_"]:has(table) {
                break-inside: avoid-page !important;
                page-break-inside: avoid !important;
                -moz-column-break-inside: avoid !important;
            }
            
            /* Orphans and widows control for Firefox */
            .firefox-print .print-only-teacher-table {
                orphans: 4;
                widows: 4;
            }
            
            /* Force teacher section elements to stay together in Firefox */
            .firefox-print .fragment-wrapper:nth-child(-n+4) {
                page-break-before: avoid !important;
                page-break-after: avoid !important;
                break-before: avoid !important;
                break-after: avoid !important;
                -moz-column-break-before: avoid !important;
                -moz-column-break-after: avoid !important;
            }
        }
    `;

  document.head.appendChild(printStyles);
}

// Add screen styles for the details/summary animation
// Transform loading indicator to success state
function transformLoadingToSuccess(loadingDiv, results) {
  // Update to very light success state using custom ghost color
  loadingDiv.className = loadingDiv.className
    .replace("bg-blue-50", "")
    .replace("border-blue-200", "border-success");

  // Apply custom soft success background using CSS custom properties
  loadingDiv.style.backgroundColor =
    "var(--color-success-ghost, color-mix(in oklab, var(--color-success) 8%, var(--color-base-100)))";

  // Get references to elements
  const spinner = loadingDiv.querySelector("#loading-spinner");
  const message = loadingDiv.querySelector("#loading-message");
  const progress = loadingDiv.querySelector("#loading-progress");

  // Replace spinner with success icon
  if (spinner) {
    spinner.className = "w-6 h-6 text-success";
    spinner.innerHTML = `
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z">
        </path>
      </svg>
    `;
  }

  // Update message
  if (message) {
    message.className = "text-success font-medium";
    message.textContent = "Questions générées avec succès !";
  }

  // Update progress with summary
  if (progress && results) {
    progress.className = "mt-2 text-sm text-success min-h-[20px]";
    const successCount = results.filter((r) => r.success).length;
    const totalCount = results.length;
    // • ${CONFIG.nbStudents} copies • ${CONFIG.nbQuestions} questions par copie
    progress.textContent = `${successCount}/${totalCount} questions générées`;
  }
}

// Transform loading indicator to error state
function transformLoadingToError(loadingDiv, error) {
  // Update classes to error state (DaisyUI)
  loadingDiv.className = loadingDiv.className
    .replace("bg-blue-50", "bg-error")
    .replace("border-blue-200", "border-error");

  // Get references to elements
  const spinner = loadingDiv.querySelector("#loading-spinner");
  const message = loadingDiv.querySelector("#loading-message");
  const progress = loadingDiv.querySelector("#loading-progress");

  // Replace spinner with error icon
  if (spinner) {
    spinner.className = "w-6 h-6 text-error-content";
    spinner.innerHTML = `
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z">
        </path>
      </svg>
    `;
  }

  // Update message
  if (message) {
    message.className = "text-error-content font-medium";
    message.textContent = "Erreur lors de la génération";
  }

  // Update progress with error details
  if (progress && error) {
    progress.className = "mt-2 text-sm text-error-content min-h-[20px]";
    progress.textContent = `❌ ${error.message}`;
  }
}

function addScreenStyles() {
  const existingStyles = document.querySelector("#sujets0-screen-styles");
  if (existingStyles) return;

  const screenStyles = document.createElement("style");
  screenStyles.id = "sujets0-screen-styles";
  screenStyles.textContent = `
        /* Hide print-only elements on screen */
        @media screen {
            .print-only-teacher-table {
                display: none !important;
            }
        }
        
        /* Teacher answer details styling */
        .teacher-answer-details {
            padding:0.25rem;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 1rem;
        }
        
        .teacher-summary {
            display: flex;
            align-items: center;
            padding: 0.25rem;
            font-size: 1rem;
            font-weight: 300;
            color: var(--color-base-content);
            opacity: 0.7;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid transparent;
            outline: none;
            position: relative;
            list-style: none;
            user-select: none;
        }
        
        .teacher-answer-details:hover {
            border: 1px solid var(--color-primary) !important;
        }
        
        /* Hide default browser markers */
        .teacher-summary::-webkit-details-marker,
        .teacher-summary::marker {
            display: none;
        }
        
        /* Custom arrow - properly centered */
        .teacher-summary::before {
            content: '▶';
            font-size: 0.875rem;
            color: #6b7280;
            margin-right: 0.75rem;
            transition: transform 0.3s ease, color 0.2s ease;
            transform-origin: center;
            display: inline-block;
            width: 1rem;
            text-align: center;
        }
        
        /* Rotate arrow when open */
        .teacher-answer-details[open] .teacher-summary::before {
            transform: rotate(90deg);
            color: var(--color-base-content);
        }
        
        /* Content styling */
        .teacher-answer-details > div {
            padding: 0;
            background-color: #ffffff;
        }
        
        /* Focus styles for accessibility: TODO sel: needs more understanding of the RG2A */
    `;

  document.head.appendChild(screenStyles);
}

// Table of Contents functionality
function populateTableOfContents() {
  const tocLinksContainer = document.querySelector("#toc-links");
  if (!tocLinksContainer) {
    console.warn("TOC container not found");
    return;
  }

  // Clear the placeholder text
  tocLinksContainer.innerHTML = "";

  let linkCount = 0;

  // Always add the teacher table link (since it's always printed)
  const teacherTable = document.querySelector("#teacher-answer-table");
  const linkElement = document.createElement("div");
  linkElement.className = "toc-link-wrapper";
  linkElement.innerHTML = `
            <a href="#teacher-answer-table" class="toc-link block px-2 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors duration-150 border-l-2 border-transparent hover:border-blue-300">
                Corrigé Enseignant
            </a>
        `;

  tocLinksContainer.appendChild(linkElement);
  linkCount++;

  const link = linkElement.querySelector("a");
  link.addEventListener("click", (e) => {
    e.preventDefault();
    
    // Find the details element - try both screen-only and general selectors
    const detailsElement = document.querySelector(".teacher-answer-details.screen-only") || 
                          document.querySelector(".teacher-answer-details");
    
    // Open the details if it exists and isn't already open
    if (detailsElement && !detailsElement.hasAttribute("open")) {
      detailsElement.setAttribute("open", "");
      console.log("📖 Opened teacher details for TOC navigation");
    }
    
    // Continue with existing scroll behavior
    if (teacherTable) {
      teacherTable.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    } else {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }
  
    // Update URL hash without jumping
    history.pushState(null, null, "#teacher-answer-table");
  });

  // Then, find all H2 elements that were generated as fragments
  const h2Elements = document.querySelectorAll(
    '.fragment-wrapper[data-f_type="h2_"] h2[id]'
  );

  // Create links for each H2
  h2Elements.forEach((h2, index) => {
    const id = h2.getAttribute("id");
    const text = h2.textContent.trim();

    if (id && text) {
      const linkElement = document.createElement("div");
      linkElement.className = "toc-link-wrapper";
      linkElement.innerHTML = `
                <a href="#${id}" class="toc-link block px-2 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors duration-150 border-l-2 border-transparent hover:border-blue-300">
                    ${text}
                </a>
            `;

      tocLinksContainer.appendChild(linkElement);
      linkCount++;

      // Add smooth scroll behavior to the link
      const link = linkElement.querySelector("a");
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const targetElement = document.querySelector(`#${id}`);
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });

          // Update URL hash without jumping
          history.pushState(null, null, `#${id}`);
        }
      });
    }
  });

  // Show message if no links found
  if (linkCount === 0) {
    tocLinksContainer.innerHTML =
      '<div class="text-xs text-gray-500 italic">Aucun titre trouvé</div>';
  }

  console.log(
    `✅ TOC populated with ${linkCount} links (${
      teacherTable ? "1 table + " : ""
    }${h2Elements.length} sections)`
  );
}

// Helper function to inject question number into statementHtml
function injectQuestionNumber(statementHtml, questionNum) {
  if (!statementHtml || !questionNum) return statementHtml;

  // Create a temporary DOM element to parse the HTML
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = statementHtml;

  // Recursive function to find the first text node in the DOM tree
  function findFirstTextLocation(element) {
    for (let child of element.childNodes) {
      if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
        // Found a non-empty text node
        return { textNode: child, parent: element };
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        // Recursively search in child elements
        const result = findFirstTextLocation(child);
        if (result) return result;
      }
    }
    return null;
  }

  // Find the first div and then search for the first text content within it
  const firstDiv = tempDiv.querySelector("div");
  if (firstDiv) {
    const textLocation = findFirstTextLocation(firstDiv);
    if (textLocation) {
      // Prepend question number to the found text node
      textLocation.textNode.textContent = `${questionNum})  ${textLocation.textNode.textContent}`;
    } else {
      // If no text found, insert at the beginning of the first div
      const questionText = document.createTextNode(`${questionNum})  `);
      firstDiv.insertBefore(questionText, firstDiv.firstChild);
    }
    return tempDiv.innerHTML;
  }

  // Fallback: if no div found, just prepend the question number
  return `${questionNum})  ${statementHtml}`;
}

// PM Fragment Generation System
class PMFragmentGenerator {
  static createParagraph(content, classes = []) {
    return {
      f_type: { value: "p_" },
      html: content,
      data: {},
      class_list: classes,
      classes: classes.join(" "),
    };
  }



  static createHr(content, classes = []) {
    const allClasses = [...classes, "mb-4", "border-base-200"];
    return {
      f_type: { value: "hr_" },
      html: content,
      data: {},
      class_list:   allClasses,
      classes: allClasses.join(" "),
    };
  }

  static createH2(content, classes = []) {
    const slug = content
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
    const allClasses = [
      ...classes,
      "text-lg",
      "mb-4",
      "pt-2",
      "text-base-content/70",
      // "border-top-1",
      // "border-base-300",
    ];
    return {
      f_type: { value: "h2_" },
      html: content,
      data: { id_href: slug },
      class_list: allClasses,
      classes: allClasses.join(" "),
      slug: slug,
    };
  }

  static createSvg(svgContent, graphDict = {}, classes = []) {
    return {
      f_type: { value: "svg_" },
      html: "",
      data: {
        src: "",
        content: svgContent,
      },
      class_list: classes,
      classes: classes.join(" "),
    };
  }

  static createDivider(classes = []) {
    const allClasses = [...classes, "my-4", "border-base-300"];
    return {
      f_type: { value: "hr_" },
      html: "",
      data: {},
      class_list: allClasses,
      classes: allClasses.join(" "),
    };
  }
}

class PMFragmentRenderer {
  static renderFragment(fragment) {
    const wrapper = document.createElement("div");
    wrapper.className = `fragment-wrapper ${fragment.classes}`;
    wrapper.setAttribute("data-f_type", fragment.f_type.value);

    const fragmentDiv = document.createElement("div");
    fragmentDiv.className = "fragment";
    fragmentDiv.setAttribute("data-f_type", fragment.f_type.value);

    // Render based on fragment type (matching PM templates exactly)
    switch (fragment.f_type.value) {
      case "p_":
        // Apply classes to the fragment div for paragraphs
        if (fragment.classes) {
          fragmentDiv.className += ` ${fragment.classes}`;
        }
        fragmentDiv.innerHTML = fragment.html;
        break;

      case "h2_":
        const h2Classes = fragment.classes
          ? ` class="${fragment.classes}"`
          : "";
        fragmentDiv.innerHTML = `<h2 id="${
          fragment.data.id_href || ""
        }"${h2Classes}>${fragment.html}</h2>`;
        break;

      case "svg_":
        // Apply classes to the fragment div for SVGs
        if (fragment.classes) {
          fragmentDiv.className += ` ${fragment.classes}`;
        }
        fragmentDiv.innerHTML = fragment.data.content;
        break;

      case "hr_":
        const hrClasses = fragment.classes
          ? ` class="${fragment.classes}"`
          : "";
        fragmentDiv.innerHTML = `<hr${hrClasses}>`;
        break;

      default:
        if (fragment.classes) {
          fragmentDiv.className += ` ${fragment.classes}`;
        }
        fragmentDiv.innerHTML = fragment.html;
    }

    wrapper.appendChild(fragmentDiv);
    return wrapper;
  }
}

// Main execution function
async function executeAllGenerators() {
  console.log("🚀 Starting question generation...");

  // Select generators up to the requested amount (capped at 12)
  // Also select only the generator for the seleted curriculum
  // select only the generators for the selected curriculum ie starting by CONFIG.curriculumSlug,
  const selectedGenerators = CONFIG.generators
    .filter((generator) => generator.startsWith(CONFIG.curriculumSlug))
    .slice(0, CONFIG.nbQuestions);
  console.log(`📝 Selected ${selectedGenerators.length} generators`);
  const questionResults = [];

  // For number of students:
  // Generate a string : one mathematician - one color

  const mathematicians = [
    // Women
    "Noether",
    "Mirzakhani",
    "Germain",
    "Lovelace",
    "Uhlenbeck",
    "Daubechies",
    "Strickland",
    "Johnson",
    "Hodgkin",
    "Curie",
    "Mouton",
    "Bath",
    "Goeppert-Mayer",
    "Apgar",
    "Solomon",
    "Franklin",
    "Ball",
    "Merian",
    "Earle",
    "Jemison",
    "Kovalevskaya",
    "Cartwright",
    "Robinson",
    "Oleinik",
    "Morawetz",
    "Granville",
    "Taussky-Todd",
    "Karp",
    "Blum",
    "Blackwell",
    // Men
    "Tao",
    "Gauss",
    "Newton",
    "Euler",
    "Riemann",
    "Ramanujan",
    "Bernoulli",
    "Napier",
    "Archimedes",
    "Arad",
    "Hackbusch",
    "Young",
    "Stilwell",
    "Huppert",
    "Calegari",
    "Britton",
    "Kotelnikov",
    "Carré",
    "Marcolongo",
    "Galois",
    "Poincaré",
    "Fermat",
    "Cauchy",
    "Laplace",
    "Fourier",
    "Lagrange",
    "Leibniz",
    "Descartes",
    "Pascal",
    "Fibonacci",
    "Pythagoras"
  ];

  // in french
  // const colors = [
  //   "rouge", "bleu", "vert", "jaune", "orange",
  //   "violet", "rose", "marron", "gris", "noir",
  //   "blanc", "cyan", "magenta", "turquoise", "indigo",
  // ];

  const colors = [
    "red",
    "blue",
    "green",
    "yellow",
    "orange",
    "violet",
    "rose",
    "marron",
    "gris",
    "noir",
    "blanc",
    "cyan",
    "magenta",
    "turquoise",
    "indigo",
  ];

  // create an an array of unique <mathematician>->color>
  // With randomness
  // While ensuring uniqueness
  // Shuffle the array



  const shuffledMathematicians = [...mathematicians].sort(
    () => Math.random() - 0.5
  );
  const shuffledColors = [...colors].sort(() => Math.random() - 0.5);
  const mathematiciansAndColors = shuffledMathematicians.map(
    (mathematician, index) => ({
      mathematician,
      color: shuffledColors[index % shuffledColors.length],
    })
  );


  // Log total number in variable `mathematiciansAndColors`
  console.log(`Total number of mathematicians and colors: ${mathematiciansAndColors.length}`);

  for (let studentNum = 1; studentNum <= CONFIG.nbStudents; studentNum++) {
    const seed = CONFIG.rootSeed + studentNum ;

    // Build nice identifier for this student using the pre-mapped array
    const pairing =
      mathematiciansAndColors[
        (studentNum - 1) % mathematiciansAndColors.length
      ];
    const niceIdentifier = `${pairing.mathematician}-${pairing.color}`;

    let generatorNum = 1;
    for (const generator of selectedGenerators) {
      try {
        console.log(
          `📝 Generating Q${generatorNum} for Student ${studentNum} (${generator})`
        );
        const result = await executeGeneratorWithSeed(generator, seed);

        result.student = studentNum;
        result.seed = seed;
        result.generator = generator;
        result.generatorNum = generatorNum;
        result.niceIdentifier = niceIdentifier;
        generatorNum++;

        // Attach graphs where needed
        await attachGraphToResult(result, generator);

        // Process KaTeX directly in SVG foreignObjects
        if (result.graphSvg) {
          result.graphSvgWithRenderedLatex = await processKatexInSvg(
            result.graphSvg
          );
        }

        questionResults.push(result);
      } catch (error) {
        console.error(`❌ Error generating Q${generatorNum}:`, error);
        questionResults.push({
          success: false,
          error: error.message,
          student: studentNum,
          generator: generator,
          generatorNum: generatorNum,
          niceIdentifier: niceIdentifier,
        });
        generatorNum++;
      }
    }
  }

  STATE.results.questionResults = questionResults;
  console.log(`✅ Generated ${questionResults.length} questions`);
  return questionResults;
}

// Helper function to format answers for teacher table
function formatAnswersForTeacherTable(result, answerType) {
  if (!result.success || !result.answer) {
    return "Erreur";
  }

  const answers = result.answer[answerType];

  // Handle both array and single answer formats
  if (Array.isArray(answers)) {
    // Join multiple answers with semicolon and non-breaking spaces
    return answers.map((answer) => `$${answer}$`).join("&nbsp;;&nbsp;");
  } else {
    // Single answer format (some sujet2 generators)
    return `$${answers}$`;
  }
}

// Pure PM Fragment Generation - No Custom UI
function generateFragmentsFromResults(results) {
  const fragments = [];

  // Detect Firefox for special handling
  const isFirefox = navigator.userAgent.includes('Firefox');

  // Generate teacher answer table content (shared by both Firefox and Chrome)
  let tableContent = `

<table class="table table-zebra w-full border border-gray-300">
  <thead>
      <tr class="bg-gray-200">
          <th class="border border-gray-300 px-3 py-2" style="text-align:left !important; width: 25%; min-width: 200px;">
              Infos
          </th>
          <th class="border border-gray-300 px-3 py-2" style="text-align:right !important; width: 37.5%;">Calcul</th>
          <th class="border border-gray-300 px-3 py-2" style="text-align:right !important; width: 37.5%;">Simplification</th>
      </tr>
  </thead>
  <tbody>`;

  // Sort results by student, then by question number
  const sortedResults = results.slice().sort((a, b) => {
    if (a.student !== b.student) {
      return a.student - b.student;
    }
    return a.generatorNum - b.generatorNum;
  });

  // Add table rows
  sortedResults.forEach((result) => {
    const latexAnswers = formatAnswersForTeacherTable(result, "latex");
    const simplifiedAnswers = formatAnswersForTeacherTable(
      result,
      "simplified_latex"
    );

    // Create combined column content: [StudentNum]-([seed])-[QuestionNum]<br>niceIdentifier<br>generator
    const studentNum = result.student || "N/A";
    const seed = result.seed || "N/A";
    const questionNum = result.generatorNum || "N/A";
    const generator = result.generator || "N/A";
    const niceId = result.niceIdentifier || "";

    // Generate the correct URL for the generator file
    const basePath = getBasePath();
    const generatorUrl = `${basePath}/static/sujets0/generators/${generator}`;

    const combinedInfo = `${studentNum}-(${seed})-${questionNum}${
      niceId ? `<br><span class="text-xs font-semibold">${niceId}</span>` : ""
    }<br><a href="${generatorUrl}" target="_blank" class="font-mono text-xs text-base-content hover:text-base-content underline">${generator}</a>`;

    tableContent += `
            <tr>
                <td class="border border-gray-300 px-3 py-2" style="text-align:left !important; vertical-align:top !important; line-height:1.3;">${combinedInfo}</td>
                <td class="border border-gray-300 px-3 py-2" style="text-align:right !important; vertical-align:middle !important;">${latexAnswers}</td>
                <td class="border border-gray-300 px-3 py-2" style="text-align:right !important; vertical-align:middle !important;">${simplifiedAnswers}</td>
            </tr>
        `;
  });

  tableContent += `
                </tbody>
                    </table>`;

  // For Firefox, we'll combine both tables into one fragment to keep them on the same page
  // For Chrome, keep them separate as before
  
  if (isFirefox) {
    // Firefox: Use same structure as Chrome but with Firefox-specific CSS classes for print compatibility
    
    // First fragment: Parameters table only (like Chrome)
    fragments.push(
      PMFragmentGenerator.createParagraph(`
<div class="print-only-teacher-table parameters-table-section firefox-parameters-section">
    <div style="font-weight: 0.5 !important; font-size: 1rem; margin-top: 1.25rem; margin-bottom: 0.75rem; font-family: var(--font-mono);">Paramètres de la génération</div>
</div>
<div class="overflow-x-auto mt-4 parameters-table-wrapper firefox-parameters-wrapper">
  <table class="table table-zebra parameters-table firefox-parameters-table">
    <tbody>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M15.39 4.39a1 1 0 0 0 1.68-.474 2.5 2.5 0 1 1 3.014 3.015 1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474 2.5 2.5 0 1 0-3.014 3.015 1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474 2.5 2.5 0 1 1-3.014-3.015 1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474 2.5 2.5 0 1 0 3.014-3.015 1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Partie</td>
        <td style="text-align: right !important;"><span class="text-xs sm:text-sm">Première Partie</span></td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Programme</td>
        <td style="text-align: right !important;"><span class="text-xs sm:text-sm">${CONFIG.curriculum}</span></td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M8 13h2"/><path d="M14 13h2"/><path d="M8 17h2"/><path d="M14 17h2"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Copies</td>
        <td class="text-xs sm:text-sm text-right">$${CONFIG.nbStudents}$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M12 17h.01"/><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M9.1 9a3 3 0 0 1 5.82 1c0 2-3 3-3 3"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Questions</td>
        <td class="text-xs sm:text-sm text-right">$${CONFIG.nbQuestions}$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
              fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 12h.01"/><path d="M16 6V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><path d="M22 13a18.15 18.15 0 0 1-20 0"/><rect width="20" height="14" x="2" y="6" rx="2"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Total questions</td>
        <td class="text-xs sm:text-sm text-right">$${CONFIG.nbStudents} \\times ${CONFIG.nbQuestions} = ${CONFIG.nbQuestions * CONFIG.nbStudents}$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3"/><path d="M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4"/><path d="M5 21h14"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Seed</td>
        <td class="text-xs sm:text-sm font-mono text-right">$${CONFIG.rootSeed}$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-stamp-icon lucide-stamp"><path d="M14 13V8.5C14 7 15 7 15 5a3 3 0 0 0-6 0c0 2 1 2 1 3.5V13"/><path d="M20 15.5a2.5 2.5 0 0 0-2.5-2.5h-11A2.5 2.5 0 0 0 4 15.5V17a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1z"/><path d="M5 22h14"/></svg>
        </td>
        <td class="text-xs sm:text-sm">Reproductibilité</td>
        <td class="text-xs md:text-sm font-mono text-right">$N°Copie-(Seed+N°Copie)-N°Question$ </td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-fingerprint-icon lucide-fingerprint"><path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4"/><path d="M14 13.12c0 2.38 0 6.38-1 8.88"/><path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/><path d="M2 12a10 10 0 0 1 18-6"/><path d="M2 16h.01"/><path d="M21.8 16c.2-2 .131-5.354 0-6"/><path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/><path d="M8.65 22c.21-.66.45-1.32.57-2"/><path d="M9 6.8a6 6 0 0 1 9 5.2v2"/></svg>
        </td>
        <td class="text-xs sm:text-sm">Empreinte par copie</td>
        <td class="text-xs sm:text-sm font-mono text-right">Mathématicien·ne - Couleur</td>
      </tr>
    </tbody>
  </table>
</div>`)
    );
    
    // Second fragment: Teacher correction table (like Chrome, but with Firefox classes)
    let tableHtml = `
        <div id="teacher-answer-table" class="mb-6 firefox-teacher-table">
            <!-- Screen version with collapsible details -->
            <details class="teacher-answer-details screen-only">
                <summary class="teacher-summary">
                    Corrigé Enseignant
                </summary>
                <div>
                    ${tableContent}
                </div>
            </details>
            
            <!-- Print version that's always visible during print - NO TITLE for Firefox to prevent page breaks -->
            <div class="print-only-teacher-table">
                ${tableContent}
            </div>
        </div>
    `;
    
    fragments.push(
      PMFragmentGenerator.createParagraph(tableHtml, ["teacher-table-section", "firefox-teacher-section"])
    );
    
  } else {
    // Chrome and other browsers: Keep the original structure with separate fragments
    
    // First fragment: Parameters table
    fragments.push(
      PMFragmentGenerator.createParagraph(`
<div class="print-only-teacher-table parameters-table-section">
    <div style="font-weight: 0.5 !important; font-size: 1rem; margin-top: 1.25rem; margin-bottom: 0.75rem; font-family: var(--font-mono);">Paramètres de la génération</div>
</div>
<div class="overflow-x-auto mt-4 parameters-table-wrapper">
  <table class="table table-zebra parameters-table">
    <tbody>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M15.39 4.39a1 1 0 0 0 1.68-.474 2.5 2.5 0 1 1 3.014 3.015 1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474 2.5 2.5 0 1 0-3.014 3.015 1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474 2.5 2.5 0 1 1-3.014-3.015 1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474 2.5 2.5 0 1 0 3.014-3.015 1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Partie</td>
        <td style="text-align: right !important;"><span class="text-xs sm:text-sm">Première Partie</span></td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Programme</td>
        <td style="text-align: right !important;"><span class="text-xs sm:text-sm">${
          CONFIG.curriculum
        }</span></td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M8 13h2"/><path d="M14 13h2"/><path d="M8 17h2"/><path d="M14 17h2"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Copies</td>
        <td class="text-xs sm:text-sm text-right">$${CONFIG.nbStudents}$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M12 17h.01"/><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M9.1 9a3 3 0 0 1 5.82 1c0 2-3 3-3 3"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Questions</td>
        <td class="text-xs sm:text-sm text-right">$${CONFIG.nbQuestions}$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
              fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 12h.01"/><path d="M16 6V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><path d="M22 13a18.15 18.15 0 0 1-20 0"/><rect width="20" height="14" x="2" y="6" rx="2"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Total questions</td>
        <td class="text-xs sm:text-sm text-right">$${
          CONFIG.nbStudents
        } \\times ${CONFIG.nbQuestions} = ${
        CONFIG.nbQuestions * CONFIG.nbStudents
      }$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content"
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1" 
            stroke-linecap="round" 
            stroke-linejoin="round">
            <path d="M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3"/><path d="M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4"/><path d="M5 21h14"/>
          </svg>
        </td>
        <td class="text-xs sm:text-sm">Seed</td>
        <td class="text-xs sm:text-sm font-mono text-right">$${
          CONFIG.rootSeed
        }$</td>
      </tr>
      <tr>
        <td class="sm:p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-stamp-icon lucide-stamp"><path d="M14 13V8.5C14 7 15 7 15 5a3 3 0 0 0-6 0c0 2 1 2 1 3.5V13"/><path d="M20 15.5a2.5 2.5 0 0 0-2.5-2.5h-11A2.5 2.5 0 0 0 4 15.5V17a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1z"/><path d="M5 22h14"/></svg>
        </td>
        <td class="text-xs sm:text-sm">Reproductibilité</td>
        <td class="text-xs text-right">$N°Copie-(Seed+N°Copie)-N°Question$ </td>
      </tr>
      <tr>
        <td class="sm:p-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-base-content" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-fingerprint-icon lucide-fingerprint"><path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4"/><path d="M14 13.12c0 2.38 0 6.38-1 8.88"/><path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/><path d="M2 12a10 10 0 0 1 18-6"/><path d="M2 16h.01"/><path d="M21.8 16c.2-2 .131-5.354 0-6"/><path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/><path d="M8.65 22c.21-.66.45-1.32.57-2"/><path d="M9 6.8a6 6 0 0 1 9 5.2v2"/></svg>
        </td>
        <td class="text-xs sm:text-sm">Empreinte par copie</td>
        <td class="text-xs sm:text-sm font-mono text-right">Mathématicien·ne - Couleur</td>
      </tr>
    </tbody>
  </table>
</div>`)
    );
    
    // Second fragment: Teacher correction table
    let tableHtml = `
        <div id="teacher-answer-table" class="mb-6">
            <!-- Screen version with collapsible details -->
            <details class="teacher-answer-details screen-only">
                <summary class="teacher-summary">
                    Corrigé Enseignant
                </summary>
                <div>
                    ${tableContent}
                </div>
            </details>
            
            <!-- Print version that's always visible during print -->
            <div class="print-only-teacher-table">
                <div style="font-weight: 0.5 !important; font-size: 1rem; margin-top: 1.25rem; margin-bottom: 0.75rem; font-family: var(--font-mono);">Corrigé Enseignant</div>
                ${tableContent}
            </div>
        </div>
    `;
    
    fragments.push(
      PMFragmentGenerator.createParagraph(tableHtml, ["teacher-table-section"])
    );
  }

  // Add separator between teacher section and student copies
  fragments.push(PMFragmentGenerator.createDivider());

  // Group by student
  const byStudent = results.reduce((acc, r) => {
    const key = r && r.student != null ? String(r.student) : "N/A";
    (acc[key] ||= []).push(r);
    return acc;
  }, {});

  for (const student of Object.keys(byStudent)) {
    // Student header if multiple students


    // We prefer to display the "Copie N°" in all cases (scenery!)
    // if (Object.keys(byStudent).length > 1) {

      // Get the niceIdentifier from the first result for this student
      const niceId = byStudent[student][0]?.niceIdentifier || "";
      const headerText = niceId
        ? `Copie n°${student} (${niceId})`
        : `Copie n°${student}`;

      fragments.push(PMFragmentGenerator.createH2(headerText, ["font-mono"]));
      fragments.push(PMFragmentGenerator.createHr(["font-mono"]));
    // }

    byStudent[student].forEach((result) => {
      // Preprocess statementHtml to inject question number properly
      let processedStatementHtml;
      if (result.success) {
        processedStatementHtml = injectQuestionNumber(
          result.statementHtml,
          result.generatorNum
        );
      } else {
        processedStatementHtml = `${result.generatorNum}) Erreur de génération`;
      }

      // Check if we have a graph to display alongside the question
      if (result.success && result.graphSvgWithRenderedLatex) {
        // DEBUG: Log what we're working with
        console.log("DEBUG processedStatementHtml:", processedStatementHtml);

        // For flex layout, we need to extract the content from the div and put the question number inside the flex text container
        // Use DOM parsing for more reliable content extraction
        let textContent;
        try {
          const parser = new DOMParser();
          const doc = parser.parseFromString(
            `<html><body>${processedStatementHtml}</body></html>`,
            "text/html"
          );
          const firstDiv = doc.querySelector("div");
          textContent = firstDiv ? firstDiv.innerHTML : processedStatementHtml;
          console.log("DEBUG extracted textContent:", textContent);
        } catch (e) {
          console.log("DEBUG DOM parsing failed, using fallback");
          // Fallback to regex if DOM parsing fails
          const contentMatch = processedStatementHtml.match(
            /^<div[^>]*>(.*)<\/div>$/s
          );
          textContent = contentMatch ? contentMatch[1] : processedStatementHtml;
          console.log("DEBUG regex textContent:", textContent);
        }

        // Create combined layout with question text and graph side by side
        const combinedHtml = `
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;">
                        <div style="flex: 1; min-width: 250px;">
                            ${textContent}
                        </div>
                        <div class="graph-svg-container" style="flex: 0 1 auto;">
                            ${result.graphSvgWithRenderedLatex}
                        </div>
                    </div>
                `;
        fragments.push(
          PMFragmentGenerator.createParagraph(combinedHtml, ["py-2"])
        );
      } else {
        // Standard layout without graph
        fragments.push(
          PMFragmentGenerator.createParagraph(processedStatementHtml, ["py-"])
        );
      }

      // Answer fragment if available
      // if (result.success && result.answer) {
      //     fragments.push(PMFragmentGenerator.createParagraph(`**Réponse:** ${result.answer}`));
      // }

      // Divider between questions
      // fragments.push(PMFragmentGenerator.createDivider());
    });
  }

  return fragments;
}

function injectFragmentsIntoPM(fragments) {
  // Find PM's main content container
  const pmContainer = document.querySelector(
    ".pm-container .max-w-\\[640px\\]"
  );
  if (!pmContainer) {
    console.error("PM container not found");
    return;
  }

  // Inject first fragment (header) first
  if (fragments.length > 0) {
    const headerFragment = PMFragmentRenderer.renderFragment(fragments[0]);
    pmContainer.appendChild(headerFragment);

    // Add print button and TOC after the header
    addPrintButton(pmContainer);

    // Inject remaining fragments
    fragments.slice(1).forEach((fragment) => {
      const renderedFragment = PMFragmentRenderer.renderFragment(fragment);
      pmContainer.appendChild(renderedFragment);
    });
  } else {
    // Fallback: add print button at the beginning if no fragments
    addPrintButton(pmContainer);
  }

  console.log(`✅ Injected ${fragments.length} fragments into PM system`);
}

// Main initialization and execution
document.addEventListener("DOMContentLoaded", async () => {
  console.log("🎯 Sujets0 Question Generator starting...");

  // Force anchor theme for exercise generation and show toast if needed
  const currentTheme = document.documentElement.getAttribute("data-theme");
  if (currentTheme !== "anchor") {
    // Set theme to 'anchor'
    document.documentElement.setAttribute("data-theme", "anchor");
    localStorage.setItem("theme", "anchor");

    // Show toast notification
    setTimeout(() => {
      showToast(
        "⚡ Le thème anchor est obligatoire pour l'impression des exercices",
        "info"
      );
    }, 500);

    console.log("🎨 Thème forcé à anchor pour la génération d'exercices");
  }

  // Set up mutation observer to keep theme as 'anchor' during exercise generation
  const observeTheme = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === "data-theme") {
        const newTheme = document.documentElement.getAttribute("data-theme");
        if (newTheme !== "anchor") {
          document.documentElement.setAttribute("data-theme", "anchor");
          localStorage.setItem("theme", "anchor");
          showToast(
            "⚡ Le thème anchor doit rester activé pour l'impression des exercices",
            "warning"
          );
          console.log(
            "🎨 Thème forcé à anchor pour maintenir la génération d'exercices"
          );
        }
      }
    });
  });

  // Start observing theme changes
  observeTheme.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });

  // Find target container (look for existing table or create after current script)
  let targetContainer = document.querySelector('[data-f_type="table_"]');
  if (!targetContainer) {
    // Fallback: insert after the script module fragment
    const scriptFragment = document.querySelector(
      '[data-f_type="script_module_"]'
    );
    if (scriptFragment) {
      targetContainer = scriptFragment;
    } else {
      targetContainer = document.body;
    }
  }

  // Show loading indicator with consistent height
  const loadingDiv = document.createElement("div");
  loadingDiv.className =
    "sujets0-loading p-4 bg-blue-50 rounded-lg border border-blue-200 min-h-[80px] print-hide mb-4";
  loadingDiv.innerHTML = `
        <div class="flex items-center space-x-3">
            <div id="loading-spinner" class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <div id="loading-message" class="text-blue-800 font-medium">Chargement du générateur de questions...</div>
        </div>
        <div id="loading-progress" class="mt-2 text-sm text-blue-600 min-h-[20px]"></div>
    `;

  targetContainer.insertAdjacentElement("afterend", loadingDiv);
  STATE.ui.container = loadingDiv;

  const progressEl = loadingDiv.querySelector("#loading-progress");

  try {
    // Add screen styles for details/summary animation
    addScreenStyles();

    // Initialize core components
    progressEl.textContent = "📦 Chargement de Nagini...";
    const naginiReady = await loadNagini();

    if (!naginiReady) {
      throw new Error("Failed to initialize Nagini");
    }

    progressEl.textContent = "📊 Chargement du générateur de graphiques...";
    const pcaReady = await loadPCAGraphLoader();
    if (!pcaReady) {
      console.warn(
        "PCA Graph Loader failed to initialize - graphs will be skipped"
      );
    }

    progressEl.textContent = "🚀 Génération des questions en cours...";

    // Generate questions
    const results = await executeAllGenerators();

    // Generate pure PM fragments
    const fragments = generateFragmentsFromResults(results);

    // Transform loading to success state
    transformLoadingToSuccess(loadingDiv, results);

    // Inject fragments into PM system
    injectFragmentsIntoPM(fragments);

    // Populate table of contents after fragments are rendered
    setTimeout(() => {
      populateTableOfContents();
    }, 50);

    // Fire unified LaTeX rendering for all content (static + dynamic)
    setTimeout(() => {
      console.log("🎯 Triggering unified LaTeX rendering for all content");
      document.dispatchEvent(new CustomEvent("render-math-now"));
    }, 100);

    // Add listener for native browser print (Ctrl+P)
    // No longer need to manipulate details since we have a print-only table
    window.addEventListener("beforeprint", () => {
      console.log("🖨️ Native print triggered - print-only table will be shown");
    });

    window.addEventListener("afterprint", () => {
      console.log("🖨️ Print completed");
    });

    // Expose for debugging
    window.sujets0Results = results;
    window.sujets0State = STATE;

    console.log("🎉 Questions generated as PM fragments with processed SVGs!");
  } catch (error) {
    console.error("❌ Sujets0 Question Generator failed:", error);
    // Transform loading to error state
    transformLoadingToError(loadingDiv, error);
  }
});

console.log("📜 Sujets0 Question Generator script loaded and ready");
