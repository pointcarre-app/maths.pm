import { configSujets0DataOnly, loadModuleDynamically } from "./config.js";
import { S0, setInState } from "./state.js";
import { loadNaginiAndInitialize } from "./nagini.js";
import { ensurePcaLoaderLoaded } from "./pca.js";
import { prerenderLatexInAllResultsWithGraph } from "./graphics.js";
import { renderResultsTable } from "./ui.js";
import { executeAllGenerators } from "./workflow.js";
import { setDomToImage } from "./graphics.js";
import { buildPapyrusBlocksFromS0, serializePapyrusBlocks } from "./papyrus-adapter.js";

async function loadDomToImage() {
    const module = await loadModuleDynamically(configSujets0DataOnly.domtoimageUrl);
  setDomToImage(module.default);
}

export async function init() {
  // 1) Load core engines in parallel (Nagini, PCA loader, dom-to-image)
  const [naginiReady] = await Promise.all([
    loadNaginiAndInitialize(),
    ensurePcaLoaderLoaded(),
    loadDomToImage(),
  ]);

  if (!naginiReady) {
    console.error("Failed to initialize Nagini");
    return false;
  }

  // 2) Execute generators and collect raw results
      const results = await executeAllGenerators();
    const questionResults = results.questionResults || [];
  S0.results.questionResults = questionResults;

  // 3) Pre-render LaTeX in SVGs
  const withLatex = await prerenderLatexInAllResultsWithGraph(questionResults);

  // 4) Render UI and perform PNG conversion if applicable
  await renderResultsTable(withLatex);

  // 5) Build and expose Papyrus blocks JSON for export/printing
  const papyrusBlocks = buildPapyrusBlocksFromS0();
  window.papyrusBlocks = papyrusBlocks;
  window.papyrusBlocksJSON = serializePapyrusBlocks(papyrusBlocks);
  console.log(window.papyrusBlocksJSON);

  // Expose for debugging/extension
  window.S0 = S0;
  window.s0Results = withLatex;
  return true;
}


