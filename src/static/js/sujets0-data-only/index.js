import { configSujets0DataOnly, loadModuleDynamically } from "./config.js";

// Import dom-to-image for SVG to PNG conversion
import domtoimage from 'https://cdn.jsdelivr.net/npm/dom-to-image@2.6.0/+esm';

// Global state
let PCAGraphLoader = null;
let Nagini = null;
let naginiManager = null;
let backendSettings = null;

/**
 * Detect if browser is Safari
 * @returns {boolean} True if Safari, false otherwise
 */
function isSafari() {
  return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

export async function buildPCAGraph(graphKey, config = {}) {
  try {
    // Ensure PCAGraphLoader is loaded
    if (!PCAGraphLoader) {
      const module = await loadModuleDynamically(
        configSujets0DataOnly.v4PyJsPCAGraphLoaderUrl
      );
      PCAGraphLoader = module.PCAGraphLoader;
    }

    // Create or reuse loader instance
    if (!window._pcaLoader) {
      window._pcaLoader = new PCAGraphLoader({
        debug: false,
        graphConfig: config,
        pcaVersion: "v0.0.27",
      });
      await window._pcaLoader.initialize();
    } else if (config && Object.keys(config).length > 0) {
      // Update config if provided
      window._pcaLoader.updateConfig(config);
    }
    // Render the graph (returns {svg, graphDict})
    const result = await window._pcaLoader.renderGraph(graphKey);

    return result;
  } catch (error) {
    console.error("PCA Graph Error:", error);
    // Return a fallback structure instead of undefined
    return {
      svg: "<svg></svg>",
      graphDict: {},
    };
  }
}

/**
 * Load Nagini and initialize manager
 * @param {Function} executeAllGenerators - The function to call when Execute button is clicked
 * @returns {Promise<boolean>} Whether initialization was successful
 */
export async function loadNaginiAndInitialize() {
  try {
    console.log("📥 Loading Nagini from:", configSujets0DataOnly.naginiJsUrl);

    // Load Nagini
    const naginiModule = await import(configSujets0DataOnly.naginiJsUrl);
    Nagini = naginiModule.Nagini;
    window.Nagini = Nagini;

    console.log(
      "🔨 Creating Nagini manager with worker:",
      configSujets0DataOnly.naginiPyodideWorkerUrl
    );

    naginiManager = await Nagini.createManager(
      "pyodide",
      ["sympy", "pydantic", "strictyaml"],
      [], //['antlr4-python3-runtime'],
      configSujets0DataOnly.teachersUrlsToPaths,
      configSujets0DataOnly.naginiPyodideWorkerUrl
    );

    await Nagini.waitForReady(naginiManager);
    //displayIndicatorNaginiIsReady();

    return true; // IMPORTANT: Return true on success!
  } catch (error) {
    console.error("Failed to initialize Nagini:", error);
    // showNaginiError();
    return false;
  }
}

/**
 * Get the Nagini manager instance
 * @returns {Object|null} Nagini manager or null if not initialized
 */
export function getNaginiManager() {
  return naginiManager;
}

/**
 * Execute a generator with a specific seed
 * @param {string} filename - Generator filename
 * @param {number} seed - Random seed
 * @returns {Object} Execution result
 */
export async function executeGeneratorWithSeed(filename, seed) {
  // Detect if we're on GitHub Pages or similar static hosting and adjust the URL accordingly
  let basePath = "";

  // Method 1: Check if we're on GitHub Pages
  if (window.location.hostname === "pointcarre-app.github.io") {
    basePath = "/maths.pm";
    console.log("🌐 GitHub Pages detected, using base path:", basePath);
  }
  // Method 2: Check if we're already in a subdirectory (more generic)
  else if (window.location.pathname.startsWith("/maths.pm/")) {
    basePath = "/maths.pm";
    console.log(
      "📁 Subdirectory deployment detected, using base path:",
      basePath
    );
  }

  const url = `${basePath}/static/sujets0/generators/${filename}`;
  console.log("📦 Loading generator from:", url);

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);

    let pythonCode = await response.text();

    // Inject seed and replace generate_components call
    // We need to pass the seed to generate_components function
    const seedInjection = `
import random
random.seed(${seed})

# Override the default SEED
import teachers.defaults
teachers.defaults.SEED = ${seed}

`;

    // Replace generate_components(None) with generate_components(None, seed)
    pythonCode = pythonCode.replace(
      "components = generate_components(None)",
      `components = generate_components(None, ${seed})`
    );

    pythonCode = seedInjection + pythonCode;

    const result = await naginiManager.executeAsync(filename, pythonCode);

    const success = !result.error && (result.exit_code === 0 || result.missive);

    if (result.missive && success) {
      try {
        const data = JSON.parse(result.missive);
        return {
          success: true,
          statement: data.statement || data.question, //TODO:  why not only one ? and the html ?
          answer: data.answer, // Pass the entire answer object to preserve structure
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

/**
 * Randomly select N items from an array
 * @param {Array} array - Source array
 * @param {number} n - Number of items to select
 * @returns {Array} Selected items
 */
export function selectRandomItems(array, n) {
  const shuffled = [...array].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
}

/**
 * Execute all generators with pagination
 */
export async function executeAllGenerators() {
  let config = {
    nbStudents: 2, // Fixed typo: nbEleves -> nbStudents
    nbQuestions: 12,
    sujets0: "Spé.",
  };

  const allGenerators = configSujets0DataOnly.sujets0Spe1Generators;

  // Mostly for documenting the temporary stuff below

  //TODO
  const generatorsToGraphFileMap =
    configSujets0DataOnly.sujets0Spe1GeneratorsToGraphFileMap;

  // Select generators based on question count
  // If all 12 are selected, keep them in order; otherwise randomly select
  //let selectedGenerators;
  //if (config.nbQuestions === 12) {
  //// Keep all generators in their original order
  //selectedGenerators = [...allGenerators];
  //} else {
  //// Randomly select subset of generators
  //selectedGenerators = selectRandomItems(allGenerators, config.nbQuestions);
  //}
  //generationResults.selectedGenerators = selectedGenerators;

  let selectedGenerators = [...allGenerators];
  console.log(`Selected ${config.nbQuestions} generators:`, selectedGenerators);

  const questionResults = [];

  for (let studentNum = 1; studentNum <= config.nbStudents; studentNum++) {
    // const seed = studentNum; // Use student number as seed

    const seed = configSujets0DataOnly.rootSeed + studentNum;

    // Execute each selected generator for this student
    for (const generator of selectedGenerators) {
      try {
        const result = await executeGeneratorWithSeed(generator, seed);
        // TODO : always validate type of the argument

        if (generator === "spe_sujet1_auto_07_question.py") {
          const Y_LABEL_FOR_HORIZONTAL_LINE = parseInt(
            result.data.components.n
          );
          const svgAndDict = await buildPCAGraph("q7_small", {
            Y_LABEL_FOR_HORIZONTAL_LINE: Y_LABEL_FOR_HORIZONTAL_LINE, // Slope
          });

          const graphSvg = svgAndDict.svg;
          const graphDict = svgAndDict.graphDict;

          result.graphSvg = graphSvg;
          result.graphDict = graphDict;

          console.log(
            "💫💫💫💫",
            `graph-${studentNum}-${generator}`,
            graphDict
          );
        } else if (generator === "spe_sujet1_auto_08_question.py") {
          console.log(
            "💫💫💫💫",
            `graph-${studentNum}-${generator}`,
            result.data.components_evaluated
          );

          const A_FLOAT_FOR_AFFINE_LINE = parseFloat(
            result.data.components_evaluated.a
          );
          const B_FLOAT_FOR_AFFINE_LINE = parseFloat(
            result.data.components_evaluated.b
          );
          const svgAndDict = await buildPCAGraph("q8_small", {
            A_FLOAT_FOR_AFFINE_LINE: A_FLOAT_FOR_AFFINE_LINE,
            B_FLOAT_FOR_AFFINE_LINE: B_FLOAT_FOR_AFFINE_LINE,
          });

          const graphSvg = svgAndDict.svg;
          const graphDict = svgAndDict.graphDict;

          result.graphSvg = graphSvg;
          result.graphDict = graphDict;

          console.log(
            "💫💫💫💫",
            `graph-${studentNum}-${generator}`,
            graphDict
          );
        } else if (generator === "spe_sujet1_auto_10_question.py") {
          console.log(
            "💫💫💫💫",
            `graph-${studentNum}-${generator}`,
            result.data.components
          );

          // Very bad naming discrepancy in graph # TODO sel
          // in spe_sujet1_auto_10_question.py, c is the ordonnée à l'origine
          // y=ax^2 + c avec |a| = 1 et c réel
          // A_SHIFT_MAGNITUDE est en fait la valeur absolue de c .....
          const aFromParabola = parseInt(result.data.components.a);
          const cFromParabola = parseInt(result.data.components.c);

          let PARABOLA_GRAPH_KEY;
          // Because each graph then deal with it for displaying the minus if necessary
          let A_SHIFT_MAGNITUDE = Math.abs(cFromParabola);

          if (aFromParabola > 0) {
            // A_SHIFT_MAGNITUDE = cFromParabola;

            if (cFromParabola > 0) {
              // p for plus
              PARABOLA_GRAPH_KEY = "parabola_s1_ap";
            } else if (cFromParabola < 0) {
              // m for minus
              PARABOLA_GRAPH_KEY = "parabola_s1_am";
            } else if (cFromParabola === 0) {
              // 0 for zero
              PARABOLA_GRAPH_KEY = "parabola_s1_a0";
            } else {
              throw new Error(`cFromParabola ${cFromParabola} is not valid`);
            }

            const svgAndDict = await buildPCAGraph(PARABOLA_GRAPH_KEY, {
              A_SHIFT_MAGNITUDE: A_SHIFT_MAGNITUDE,
            });

            const graphSvg = svgAndDict.svg;
            const graphDict = svgAndDict.graphDict;

            result.graphSvg = graphSvg;
            result.graphDict = graphDict;

            console.log(
              "💫💫💫💫",
              `graph-${studentNum}-${generator}`,
              graphDict
            );
          } else {
            // A_SHIFT_MAGNITUDE = -cFromParabola;

            if (cFromParabola > 0) {
              // p for plus
              PARABOLA_GRAPH_KEY = "parabola_sm1_ap";
            } else if (cFromParabola < 0) {
              // m for minus
              PARABOLA_GRAPH_KEY = "parabola_sm1_am";
            } else if (cFromParabola === 0) {
              // 0 for zero
              PARABOLA_GRAPH_KEY = "parabola_sm1_a0";
            } else {
              throw new Error(`cFromParabola ${cFromParabola} is not valid`);
            }

            const svgAndDict = await buildPCAGraph(PARABOLA_GRAPH_KEY, {
              A_SHIFT_MAGNITUDE: A_SHIFT_MAGNITUDE,
            });

            const graphSvg = svgAndDict.svg;
            const graphDict = svgAndDict.graphDict;

            result.graphSvg = graphSvg;
            result.graphDict = graphDict;

            console.log(
              "💫💫💫💫",
              `graph-${studentNum}-${generator}`,
              graphDict
            );
          }

          // const A_SHIFT_MAGNITUDE
        } else if (generator === "spe_sujet1_auto_11_question.py") {
          let caseFromGenerator = result.data.components.case;
          let svgAndDict;

          if (caseFromGenerator === "case_a") {
            svgAndDict = await buildPCAGraph("q11_case_a_small", {});
          } else if (caseFromGenerator === "case_b") {
            svgAndDict = await buildPCAGraph("q11_case_b_small", {});
          } else if (caseFromGenerator === "case_c") {
            svgAndDict = await buildPCAGraph("q11_case_c_small", {});
          } else {
            throw new Error(
              `caseFromGenerator ${caseFromGenerator} is not valid`
            );
          }
          const graphSvg = svgAndDict.svg;
          const graphDict = svgAndDict.graphDict;

          result.graphSvg = graphSvg;
          result.graphDict = graphDict;

          console.log(
            "💫💫💫💫",
            `graph-${studentNum}-${generator}`,
            graphDict
          );
        }

        questionResults.push(result);
        // Store graph dictionary as data attribute for access if needed
        // container.dataset.graphDict = JSON.stringify(result.graphDict);
      } catch (error) {
        console.error(error);
        questionResults.push({
          success: false,
          error: error.message,
          stdout: "",
          stderr: "",
        });
      }
    }

    console.log("questionResults", questionResults);
  }

  console.log("questionResults", questionResults);
  return {
    questionResults: questionResults,
  };
}

export function hasGraph(result) {
  return result.graphSvg !== null && result.graphDict !== null;
}

export async function prerenderLatexInSvg(svgString) {
  // If KaTeX is not available, return original
  if (typeof katex === "undefined") {
    console.warn("KaTeX not available, cannot pre-render LaTeX");
    return svgString;
  }

  try {
    // Parse the SVG
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, "image/svg+xml");
    const svgElement = svgDoc.querySelector("svg");

    if (!svgElement) {
      return svgString;
    }

    // Find all foreign objects with LaTeX
    const foreignObjects = svgElement.querySelectorAll("foreignObject");
    let hasUnrenderedLatex = false;
    let renderedCount = 0;

    foreignObjects.forEach((fo) => {
      const divs = fo.querySelectorAll("div.svg-latex");
      divs.forEach((div) => {
        // Check if already rendered (has .katex class)
        if (div.querySelector(".katex")) {
          // Already rendered, skip
          return;
        }

        const latex = div.textContent.trim();
        if (latex) {
          hasUnrenderedLatex = true;
          try {
            // Preserve original styles
            const bgColor = div.style.backgroundColor;
            const color = div.style.color;

            // Render LaTeX to HTML string
            const rendered = katex.renderToString(latex, {
              throwOnError: false,
              displayMode: false,
            });

            // Set the rendered HTML
            div.innerHTML = rendered;
            renderedCount++;

            // Restore styles
            if (bgColor) div.style.backgroundColor = bgColor;
            if (color) {
              // Apply color to all KaTeX elements
              const katexElements = div.querySelectorAll(".katex, .katex *");
              katexElements.forEach((el) => {
                el.style.color = color;
              });
            }
          } catch (e) {
            console.error("KaTeX rendering error:", e);
            // Keep original LaTeX text on error
          }
        }
      });
    });

    // If no unrendered LaTeX was found, return original
    if (!hasUnrenderedLatex) {
      return svgString;
    }

    if (renderedCount > 0) {
      console.log(`Pre-rendered ${renderedCount} LaTeX expressions in SVG`);
    }

    // Serialize back to string
    const serializer = new XMLSerializer();
    return serializer.serializeToString(svgElement);
  } catch (error) {
    console.error("Error pre-rendering LaTeX in SVG:", error);
    return svgString;
  }
}

// Write a function that prerender the latex in all results with a graph using  hasGraph and  prerenderLatexInSvg
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

/**
 * Convert SVG string to PNG using dom-to-image
 * @param {string} svgString - The SVG HTML string with pre-rendered LaTeX
 * @param {Object} options - Conversion options
 * @returns {Promise<string|null>} PNG data URL or null if failed
 */
async function convertSvgToPngWithDomToImage(svgString, options = {}) {
  try {
    // Default options for high quality
    const scale = options.scale || 2; // 2x for high DPI
    let width = options.width || 340;
    let height = options.height || 340;
    
    // Parse the SVG to get dimensions
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
    const svgElement = svgDoc.querySelector('svg');
    
    if (!svgElement) {
      throw new Error('No SVG element found in the provided string');
    }
    
    // Try to get actual dimensions from the SVG element
    const svgWidth = svgElement.getAttribute('width');
    const svgHeight = svgElement.getAttribute('height');
    const viewBox = svgElement.getAttribute('viewBox');
    
    // If SVG has dimensions, use them
    if (svgWidth && svgHeight) {
      width = parseInt(svgWidth) || width;
      height = parseInt(svgHeight) || height;
    }
    
    // Ensure SVG has explicit dimensions for conversion
    svgElement.setAttribute('width', width);
    svgElement.setAttribute('height', height);
    
    // Ensure viewBox is set if not present
    if (!viewBox) {
      svgElement.setAttribute('viewBox', `0 0 ${width} ${height}`);
    }
    
    // Apply inline styles to ensure they're captured
    svgElement.style.backgroundColor = 'white';
    svgElement.style.fontFamily = "'Lexend', sans-serif";
    
    // Serialize back to string
    const serializer = new XMLSerializer();
    const updatedSvgString = serializer.serializeToString(svgElement);
    
    // Create a temporary container
    const tempDiv = document.createElement('div');
    tempDiv.style.position = 'absolute';
    tempDiv.style.left = '-9999px';
    tempDiv.style.top = '-9999px';
    tempDiv.innerHTML = updatedSvgString;
    document.body.appendChild(tempDiv);
    
    const tempSvgElement = tempDiv.querySelector('svg');
    
    // Wait a bit for rendering to complete
    await new Promise(resolve => setTimeout(resolve, 100));
    

    let pngDataUrl;
    try {
      // Convert to PNG using dom-to-image with CORS-safe options
      pngDataUrl = await domtoimage.toPng(tempSvgElement, {
        width: width * scale,
        height: height * scale,
        style: {
          transform: `scale(${scale})`,
          transformOrigin: 'top left',
          width: `${width}px`,
          height: `${height}px`
        },
        quality: 1.0,
        // Add options to handle CORS issues
        cacheBust: true,
        imagePlaceholder: undefined,
        // Skip external stylesheets that cause CORS issues
        filter: (node) => {
          // Filter out link elements that reference external stylesheets
          if (node.tagName === 'LINK' && node.rel === 'stylesheet') {
            const href = node.href || '';
            // Skip external stylesheets
            if (href.includes('fonts.googleapis.com') || 
                href.includes('cdn.jsdelivr.net') ||
                href.includes('cdnjs.cloudflare.com')) {
              return false;
            }
          }
          return true;
        }
      });
    } catch (error) {
      console.error('Error converting SVG to PNG:', error);
    }
    
    // Clean up
    document.body.removeChild(tempDiv);
    
    return pngDataUrl;
  } catch (error) {
    console.error('Error converting SVG to PNG:', error);
    return null;
  }
}

/**
 * Convert all SVGs with graphs to PNG for non-Safari browsers
 * @param {Array} results - Array of results with potential graphs
 * @returns {Promise<Array>} Results with PNG data URLs added
 */
async function convertAllGraphsToPng(results) {
  // Skip for Safari
  if (isSafari()) {
    console.log('🔍 Safari detected, skipping PNG conversion (will use SVG directly)');
    return results;
  }
  
  console.log('🎨 Converting SVGs to PNGs for non-Safari browser...');
  let convertedCount = 0;
  
  for (const result of results) {
    if (hasGraph(result) && result.graphSvgWithRenderedLatex) {
      try {
        // Get dimensions from graphDict if available
        const dimensions = {
          width: result.graphDict?.svg?.width || 340,
          height: result.graphDict?.svg?.height || 340
        };
        
        // Convert the pre-rendered SVG to PNG
        const pngDataUrl = await convertSvgToPngWithDomToImage(
          result.graphSvgWithRenderedLatex,
          {
            width: dimensions.width,
            height: dimensions.height,
            scale: 2 // 2x for high quality
          }
        );
        
        if (pngDataUrl) {
          // Store PNG and dimensions in result
          result.graphPng = pngDataUrl;
          result.graphDimensions = dimensions;
          convertedCount++;
        } else {
          console.warn('Failed to convert graph to PNG for result:', result);
        }
      } catch (error) {
        console.error('Error converting graph to PNG:', error);
      }
    }
  }
  
  console.log(`✅ Converted ${convertedCount} graphs to PNG`);
  return results;
}

export async function init() {
  // Load both PCAGraphLoader and Nagini in parallel
  const [naginiReady, pcaModule] = await Promise.all([
    loadNaginiAndInitialize(),
    loadModuleDynamically(configSujets0DataOnly.v4PyJsPCAGraphLoaderUrl), // Preload the graph loader
  ]);

  // Set the PCAGraphLoader from the loaded module
  if (pcaModule) {
    PCAGraphLoader = pcaModule.PCAGraphLoader;
  }

  if (naginiReady) {
    console.log("✅ Nagini is ready! You can now call executeAllGenerators()");
    // Make executeAllGenerators available globally for testing
    window.executeTest = async () => {
      const results = await executeAllGenerators();
      console.log("Execution results:", results);
      return results;
    };
    console.log("🚀 Auto-running executeTest()...");
    // Automatically run the test
    const results = await window.executeTest();
    console.log("✅ Auto-execution complete!", results);

    // Extract the questionResults array from the results object
    const questionResults = results.questionResults || [];
    
    // Step 1: Pre-render LaTeX in SVGs
    const resultsLatexRendered = await prerenderLatexInAllResultsWithGraph(
      questionResults
    );
    console.log("✅ Pre-rendering LaTeX complete!", resultsLatexRendered);
    
    // Step 2: Convert SVGs to PNGs for non-Safari browsers
    const finalResults = await convertAllGraphsToPng(resultsLatexRendered);
    console.log("✅ PNG conversion complete!", finalResults);

    return finalResults;
  } else {
    console.error("❌ Failed to initialize Nagini");
  }

  return naginiReady;
}
