/**
 * Generators Module for Sujets0
 * Handles generator execution logic and management
 */

import { executeGeneratorWithSeed } from "./index-nagini.js";
import { getGeneratorConfig, displayValidationTable } from "./index-form.js";
import { displayStudentResults } from "./index-results.js";
import generationResults, { StudentExerciseSet } from "./index-data-model.js";
import { convertAllGraphsToPng } from "./index-svg-converter.js";

// Export the generationResults for backward compatibility
export { generationResults };

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
  // Check if Nagini is ready (indirectly)
  if (!window.Nagini) {
    // Display error in validation table
    const errorData = {
      copies: { count: "-", isValid: false },
      questions: { perCopy: "-", isValid: false },
      program: { level: null, isValid: false },
      track: { type: null, isValid: false },
      isComplete: false,
      errors: [
        {
          field: "system",
          message:
            "Nagini n'est pas prêt. Veuillez patienter quelques secondes.",
        },
      ],
    };
    displayValidationTable(errorData);
    return;
  }

  // Extract and validate form data (this will display the validation table)
  const config = getGeneratorConfig();
  if (!config) {
    // Validation table already displayed by getGeneratorConfig
    return;
  }

  console.log("Generator configuration:", config);
  generationResults.config = config;

  const executeBtn = document.getElementById("execute-all-generators-btn");
  if (executeBtn) {
    executeBtn.disabled = true;
    executeBtn.textContent = "Génération en cours...";
  }

  const allGenerators = [
    "spe_sujet1_auto_01_question.py",
    "spe_sujet1_auto_02_question.py",
    "spe_sujet1_auto_03_question.py",
    "spe_sujet1_auto_04_question.py",
    "spe_sujet1_auto_05_question.py",
    "spe_sujet1_auto_06_question.py",
    "spe_sujet1_auto_07_question.py",
    "spe_sujet1_auto_08_question.py",
    "spe_sujet1_auto_09_question.py",
    "spe_sujet1_auto_10_question.py",
    "spe_sujet1_auto_11_question.py",
    "spe_sujet1_auto_12_question.py",
  ];

  // Mostly for documenting the temporary stuff below
  const generatorsToGraphFileMap = {
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
  };

  // Select generators based on question count
  // If all 12 are selected, keep them in order; otherwise randomly select
  let selectedGenerators;
  if (config.nbQuestions === 12) {
    // Keep all generators in their original order
    selectedGenerators = [...allGenerators];
  } else {
    // Randomly select subset of generators
    selectedGenerators = selectRandomItems(allGenerators, config.nbQuestions);
  }
  generationResults.selectedGenerators = selectedGenerators;

  console.log(`Selected ${config.nbQuestions} generators:`, selectedGenerators);

  // Reset results using the data model
  generationResults.reset();
  generationResults.setConfig(config);
  generationResults.setSelectedGenerators(selectedGenerators);

  // Update the status message and progress bar
  const generationMessage = document.getElementById("generation-message");
  const generationTime = document.getElementById("generation-time");
  const generationProgress = document.getElementById("generation-progress");
  
  // Get conversion elements early to reset them
  const conversionMessageEl = document.getElementById("conversion-message");
  const conversionTimeEl = document.getElementById("conversion-time");
  const conversionProgressEl = document.getElementById("conversion-progress");
  
  // Temps de début pour calculer la durée d'exécution
  const startTime = performance.now();
  generationResults.startTime = startTime;
  
  if (generationMessage) {
    generationMessage.textContent = `Génération en cours : ${config.nbStudents} copies, ${config.nbQuestions} questions`;
  }
  
  if (generationTime) {
    generationTime.textContent = "0.0s";
  }
  
  if (generationProgress) {
    generationProgress.value = 0;
    generationProgress.max = config.nbStudents;
  }

  // Réinitialiser la barre de conversion également
  if (conversionMessageEl) {
    conversionMessageEl.textContent = "En attente de conversion...";
  }
  
  if (conversionTimeEl) {
    conversionTimeEl.textContent = "0.0s";
  }
  
  if (conversionProgressEl) {
    conversionProgressEl.value = 0;
    conversionProgressEl.max = 100;
  }

  // Get or create results container in the wrapper area
  let resultsContainer = document.getElementById("generator-results-container");
  const wrapper = document.getElementById("generator-results-wrapper");

  if (!resultsContainer) {
    resultsContainer = document.createElement("div");
    resultsContainer.id = "generator-results-container";

    // Place it in the wrapper
    if (wrapper) {
      wrapper.appendChild(resultsContainer);
    } else {
      // Fallback to body if wrapper not found
      document.body.appendChild(resultsContainer);
    }
  }

  resultsContainer.className = "mt-4";
  resultsContainer.innerHTML = ``;

  // Process each student
  for (let studentNum = 1; studentNum <= config.nbStudents; studentNum++) {
    // const seed = studentNum; // Use student number as seed
    const seed = Math.floor(Math.random() * 1_000); // Random seed
    const questionResults = [];

    // Update progress
    const generationProgress = document.getElementById("generation-progress");
    const generationTime = document.getElementById("generation-time");
    if (generationProgress) {
      generationProgress.value = studentNum - 1;
    }
    
    // Mettre à jour le temps d'exécution
    if (generationTime) {
      const elapsedTime = (performance.now() - generationResults.startTime) / 1000;
      generationTime.textContent = `${elapsedTime.toFixed(1)}s`;
    }

    // Execute each selected generator for this student
    for (const generator of selectedGenerators) {
      try {
        const result = await executeGeneratorWithSeed(generator, seed);
        // TODO : always validate type of the argument

        if (generator === "spe_sujet1_auto_07_question.py") {
          //console.log("result.data.components")
          //console.log("result.data.components")
          //console.log("result.data.components")
          //console.log("result.data.components")

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
        }

        else if (generator === "spe_sujet1_auto_11_question.py") {
          let caseFromGenerator = result.data.components.case;
          let svgAndDict;

          if (caseFromGenerator === "case_a") {
             svgAndDict = await buildPCAGraph("q11_case_a_small", {});
          } else if (caseFromGenerator === "case_b") {
             svgAndDict = await buildPCAGraph("q11_case_b_small", {});
          } else if (caseFromGenerator === "case_c") {
             svgAndDict = await buildPCAGraph("q11_case_c_small", {});
          } else {
            throw new Error(`caseFromGenerator ${caseFromGenerator} is not valid`);
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

    // Create and store student exercise set using our data model
    const studentExerciseSet = StudentExerciseSet.fromGeneratorResults(
      studentNum,
      seed,
      questionResults,
      selectedGenerators
    );

    generationResults.addStudent(studentExerciseSet);
  }

  // Update progress status to complete
  if (generationProgress) {
    generationProgress.value = config.nbStudents;
  }
  
  if (generationMessage) {
    generationMessage.textContent = `Génération terminée : ${config.nbStudents} copies, ${config.nbQuestions} questions`;
  }
  
  if (generationTime) {
    const elapsedTime = (performance.now() - generationResults.startTime) / 1000;
    generationTime.textContent = `${elapsedTime.toFixed(1)}s`;
  }
  
  // Convert all SVGs to PNGs for faster printing - references were created earlier
  
  // Enregistrer le temps de début de la conversion
  const conversionStartTime = performance.now();
  generationResults.conversionStartTime = conversionStartTime;
  
  if (conversionTimeEl) {
    conversionTimeEl.textContent = "0.0s";
  }
  
  // Count total graphs to convert
  let totalGraphs = 0;
  generationResults.students.forEach(student => {
    student.questions.forEach(question => {
      if (question.graphSvg) totalGraphs++;
    });
  });
  
  if (totalGraphs > 0) {
    if (conversionMessageEl) {
      conversionMessageEl.textContent = `Conversion de ${totalGraphs} graphiques...`;
    }
    
    if (conversionProgressEl) {
      conversionProgressEl.value = 0;
      conversionProgressEl.max = totalGraphs;
    }
    
    // Convert all graphs with progress callback
    await convertAllGraphsToPng(generationResults, (converted, total) => {
      if (conversionProgressEl) {
        conversionProgressEl.value = converted;
      }
      if (conversionMessageEl) {
        conversionMessageEl.textContent = `Conversion des graphiques : ${converted}/${total}`;
      }
      if (conversionTimeEl) {
        const elapsedTime = (performance.now() - generationResults.conversionStartTime) / 1000;
        conversionTimeEl.textContent = `${elapsedTime.toFixed(1)}s`;
      }
    });
    
    // Update conversion status to complete
    if (conversionMessageEl) {
      conversionMessageEl.textContent = `Conversion des graphiques terminée : ${totalGraphs} / ${totalGraphs}`;
    }
    
    if (conversionProgressEl) {
      conversionProgressEl.value = totalGraphs;
    }
    
    if (conversionTimeEl) {
      const elapsedTime = (performance.now() - generationResults.conversionStartTime) / 1000;
      conversionTimeEl.textContent = `${elapsedTime.toFixed(1)}s`;
    }
  } else {
    // No graphs to convert, ready immediately
    if (conversionMessageEl) {
      conversionMessageEl.textContent = `Pas de graphiques à convertir`;
    }
    
    if (conversionProgressEl) {
      conversionProgressEl.value = 100;
      conversionProgressEl.max = 100;
    }
  }
  
  // Enable print buttons after conversion
  const printCurrentBtn = document.getElementById("print-current-copy-btn");
  const printAllBtn = document.getElementById("print-all-copies-btn");
  
  if (printCurrentBtn) {
    printCurrentBtn.disabled = false;
  }
  
  if (printAllBtn) {
    printAllBtn.disabled = false;
  }
  
  // Create pagination buttons for student preview
  if (typeof window.createPaginationButtons === 'function') {
    window.createPaginationButtons();
    
    // Preview the first student
    if (typeof window.previewStudentCopy === 'function') {
      window.previewStudentCopy(0);
    }
  }

  // Display first student's results
  // displayStudentResults(0);

  // Re-enable button
  if (executeBtn) {
    executeBtn.disabled = false;
    executeBtn.textContent = "Générer";
  }
}
