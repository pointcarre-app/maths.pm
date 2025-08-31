import { configSujets0DataOnly, loadModuleDynamically } from "./config.js";
import { S0, setInState } from "./state.js";
import { loadNaginiAndInitialize } from "./nagini.js";
import { ensurePcaLoaderLoaded } from "./pca.js";
import { prerenderLatexInAllResultsWithGraph } from "./graphics.js";
import { renderResultsTable, renderPapyrusBlocks } from "./ui.js";
import { executeAllGenerators } from "./workflow.js";
import { setDomToImage } from "./graphics.js";
import {
  buildPapyrusBlocksFromS0,
  serializePapyrusBlocks,
} from "./papyrus-adapter.js";

async function loadDomToImage() {
  const module = await loadModuleDynamically(
    configSujets0DataOnly.domtoimageUrl
  );
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

  // 4.5) Render KaTeX in all tables after they're created
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false
      });
    } catch (e) {
      console.error('KaTeX rendering failed:', e);
    }
  } else {
    console.warn('renderMathInElement not available, trying again in 200ms...');
    // Retry after a short delay if KaTeX isn't loaded yet
    setTimeout(() => {
      if (window.renderMathInElement) {
        try {
          window.renderMathInElement(document.body, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false }
            ],
            throwOnError: false
          });
        } catch (e) {
          console.error('KaTeX rendering failed (delayed):', e);
        }
      } else {
        console.error('renderMathInElement still not available after delay');
      }
    }, 200);
  }

  // 5) Build and expose Papyrus blocks JSON for export/printing
  const papyrusBlocks = buildPapyrusBlocksFromS0();
  window.papyrusBlocks = papyrusBlocks;
  window.papyrusBlocksJSON = serializePapyrusBlocks(papyrusBlocks);

  // 6) Display Papyrus preview below using fallback renderer
  // try {
  //   renderPapyrusBlocks(papyrusBlocks);
  // } catch (_) { /* ignore rendering errors in preview */ }


  

    // Generate HTML directly
    // let html = '<div class="page-wrapper"><div class="page-preview"><div class="page-content">';
  
    // const items = papyrusBlocks;
    
    // for (const item of items) {
    //     if (item.html) {
    //         html += item.html;
    //     } else if (item.svg) {
    //         html += `<div style="${item.style || ''}">${item.svg}</div>`;
    //     } else if (item.pngDataUrl) {
    //         html += `<img src="${item.pngDataUrl}" style="${item.style || ''}" alt="Graph">`;
    //     } else if (item.katex) {
    //         // Render KaTeX if available
    //         if (window.katex) {
    //             try {
    //                 const rendered = window.katex.renderToString(item.katex, {
    //                     throwOnError: false,
    //                     displayMode: item.displayMode || false
    //                 });
    //                 html += `<div style="${item.style || ''}">${rendered}</div>`;
    //             } catch (e) {
    //                 html += `<div style="${item.style || ''}">$$${item.katex}$$</div>`;
    //             }
    //         } else {
    //             html += `<div style="${item.style || ''}">$$${item.katex}$$</div>`;
    //         }
    //     }
        
    //     // Add spacing
    //     if (item.marginBottom) {
    //         html += `<div style="height: ${item.marginBottom}"></div>`;
    //     }
        
    //     // Handle page breaks
    //     if (item.pageBreak === 'after') {
    //         html += '</div></div></div>';
    //         html += '<div class="page-wrapper"><div class="page-preview"><div class="page-content">';
    //     }
    // }
    
    // html += '</div></div></div>';
    
    // container.innerHTML = html;


  // console.log(window.papyrusBlocksJSON);

  // document.addEventListener("DOMContentLoaded", function () {
  //   const opts = {
  //     delimiters: [
  //       {
  //         left: "$$",
  //         right: "$$",
  //         display: true,
  //       },
  //       {
  //         left: "$",
  //         right: "$",
  //         display: false,
  //       },
  //       {
  //         left: "\\(",
  //         right: "\\)",
  //         display: false,
  //       },
  //       {
  //         left: "\\[",
  //         right: "\\]",
  //         display: true,
  //       },
  //     ],
  //     throwOnError: false,
  //     strict: false,
  //     displayMode: false,
  //   };

  //   document.querySelectorAll(".statement-wrapper").forEach((element) => {
  //     renderMathInElement(element, opts);
  //   });
  // });

  // Expose for debugging/extension
  window.S0 = S0;
  window.s0Results = withLatex;
  return true;
}
