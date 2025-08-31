import { configSujets0DataOnly, loadModuleDynamically } from "./config.js";
import { S0, setInState, getFromState } from "./state.js";

export async function loadNaginiAndInitialize() {
  try {
    const naginiModule = await import(configSujets0DataOnly.naginiJsUrl);
    setInState("nagini.module", naginiModule.Nagini);
    window.Nagini = naginiModule.Nagini;

    const manager = await naginiModule.Nagini.createManager(
      "pyodide",
      ["sympy", "pydantic", "strictyaml"],
      [],
      configSujets0DataOnly.teachersUrlsToPaths,
      configSujets0DataOnly.naginiPyodideWorkerUrl
    );
    await naginiModule.Nagini.waitForReady(manager);
    setInState("nagini.manager", manager);
    setInState("nagini.ready", true);
    return true;
  } catch (error) {
    console.error("Failed to initialize Nagini:", error);
    setInState("nagini.ready", false);
    return false;
  }
}

export function getNaginiManager() {
  return getFromState("nagini.manager", null);
}

export async function executeGeneratorWithSeed(filename, seed) {
  const manager = getNaginiManager();
  if (!manager) {
    return { success: false, error: "Nagini manager not initialized" };
  }

  let basePath = "";
  if (window.location.hostname === "pointcarre-app.github.io") {
    basePath = "/maths.pm";
  } else if (window.location.pathname.startsWith("/maths.pm/")) {
    basePath = "/maths.pm";
  }

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


