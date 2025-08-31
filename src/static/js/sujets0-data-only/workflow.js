import { configSujets0DataOnly } from "./config.js";
import { S0 } from "./state.js";
import { buildPCAGraph } from "./pca.js";
import { executeGeneratorWithSeed } from "./nagini.js";

export function selectGenerators(config) {
  const allGenerators = configSujets0DataOnly.sujets0Spe1Generators;
  // For now keep all in order; easy to change later
  return [...allGenerators].slice(0, config.nbQuestions);
}

export async function executeAllGenerators(configOverrides = {}) {
  const config = {
    nbStudents: 2,
    nbQuestions: 12,
    sujets0: "Spé.",
    ...configOverrides,
  };

  const selectedGenerators = selectGenerators(config);
  const questionResults = [];

  for (let studentNum = 1; studentNum <= config.nbStudents; studentNum++) {
    const seed = configSujets0DataOnly.rootSeed + studentNum;
    for (const generator of selectedGenerators) {
      try {
        const result = await executeGeneratorWithSeed(generator, seed);

        // Attach graphs where needed
        if (generator === "spe_sujet1_auto_07_question.py") {
          const Y_LABEL_FOR_HORIZONTAL_LINE = parseInt(
            result.data.components.n
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

        questionResults.push(result);
      } catch (error) {
        questionResults.push({
          success: false,
          error: error.message,
          stdout: "",
          stderr: "",
        });
      }
    }
  }

  S0.results.questionResults = questionResults;


  return { questionResults };
}


