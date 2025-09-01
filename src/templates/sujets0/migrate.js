      async function arpegeGenerator() {
          console.log("➡️ Arpege:Generator");

          if (!Nagini) {
              console.error("Nagini is not loaded. Cannot generate questions.");
              alert("The Nagini library failed to load. Please check the console for details.");
              return;
          }

          const managerPromise = Nagini.createManager(
              managerBackend,
              packages,
              micropipPackages,
              teachersFilesToLoad,
              pyodideWorkerUrl
          );

          const readyPromise = managerPromise.then((mgr) =>
              Nagini.waitForReady(mgr).then(() => mgr)
          );

          readyPromise
              .then(async (mgr) => {
                  displayIndicatorNaginiIsReady();
                  generatedQuestions = [];

                  // Clear preview holders if they exist
                  const previewHolder = document.getElementById("questions-preview-holder");
                  if (previewHolder) previewHolder.innerHTML = "";

                  const runtimeHolder = document.getElementById("questions-generated-at-runtime-holder");
                  if (runtimeHolder) runtimeHolder.innerHTML = "";

                  //pythonFileUrls.length
                  for (let i = 0; i < 4; i++) {
                      const pythonFileUrl = pythonFileUrls[i];

                      console.log(`➡️ Generating question from ${pythonFileUrl}`);

                      try {
                          const question = await QuestionFactory.createFromPyodide(
                              pythonFileUrl,
                              mgr,
                              includeNaginiResult,
                              includeMetadata
                          );

                          generatedQuestions.push(question);
                          const holder = document.getElementById("questions-generated-at-runtime-holder");
                          if (holder) {
                              renderQuestion(question, holder);
                          }
                      } catch (error) {
                          console.error(`❌ Failed to generate question from ${pythonFileUrl}:`, error);
                          const div = document.createElement("div");
                          div.classList.add("mt-8");
                          div.innerHTML = `
            <div class="card card-error">
              <div class="card-body shadow-lg mb-5">
                    ERRRROR
                    ${error}
                </div>
              </div>
    </div>
          `;
                      }
                  }
                  // Render preview after all questions are generated
                  if (typeof renderQuestionsPreview === 'function') {
                      renderQuestionsPreview(generatedQuestions);
                  }

                  const downloadBtn = document.getElementById("download-pdf-btn");
                  if (downloadBtn) downloadBtn.disabled = false;
              })
              .catch((err) => {
                  console.error(err);
              });
      }

      async function renderQuestion(question, containerEl) {
          const naginiResult = question.naginiResult;
          const div = document.createElement("div");
          div.classList.add("mt-8");
          div.innerHTML = `
          <div class="card">
            <div class="card-body bg-base-200 shadow-lg mb-5">
                <div class="overflow-x-auto">
                    <table class="table table-zebra table-sm">
                        <tbody>

                            <tr><td colspan="2" class="font-mono w-32 align-top text-right bg-primary/10">Metadata</td></tr>
                            <tr><td class="font-mono w-32 align-top">Origin (from factory)</td><td class="align-top"><code>${
                             question.origin
                            }</code></td></tr>
                            <tr><td class="font-mono w-32 align-top">Python File (from factory)</td><td class="font-mono text-xs align-top">${
                                question.pythonFileUrl
                            }</td></tr>
                            <tr><td class="font-mono w-32 align-top">Beacon (from question script)</td><td class="align-top">${
                                question.beacon
                            }</td></tr>
                            <tr><td class="font-mono w-32 align-top">n°copie-seed-n°q°</td><td class="font-mono text-xs align-top">${
                                question.id
                            }</td></tr>
                            <tr><td colspan="2" class="font-mono w-32 align-top text-right bg-primary/10">Question data</td></tr>
                            <tr><td class="font-mono w-32 align-top">Statement</td><td id="statement-${question.id}" class="align-top">${
                                question.statement
                            }</td></tr>
                            <tr><td class="font-mono w-32 align-top bg-base-300">Answer Latex</td><td class="align-top">$${
                                question.answer.latex
                            }$</td></tr>
                            <tr><td class="font-mono w-32 align-top bg-base-300">Answer Simplified Latex</td><td class="align-top">$${
                                question.answer.simplified_latex
                            }$</td></tr>
                            <tr><td class="font-mono w-32 align-top">Answer SymPy Expr Data</td><td class="align-top">
                                <code>${question.answer.sympy_exp_data?.type || "N/A"}</code><br />
                                <code>${question.answer.sympy_exp_data?.["sp.srepr"] || "N/A"}</code><br />
                                <code>${question.answer.sympy_exp_data?.str || "N/A"}</code><br />
                             </td></tr>
                            <tr><td class="font-mono w-32 align-top">Answer Formal Repr</td><td class="align-top">${
                                question.answer.formal_repr
                            }</td></tr>
                        </tbody>
                    </table>
                    <hr />
                    <details>
                        <summary class="font-mono pl-4">Stdout</summary>
                        <pre style="padding: 1rem; border-radius: 0.5rem; overflow-x: auto; white-space: pre-wrap; font-family: monospace;">${
                            naginiResult?.stdout
                        }</pre>
                    </details>
                    <details>
                        <summary class="font-mono pl-4">Stderr</summary>
                        <pre style="padding: 1rem; border-radius: 0.5rem; overflow-x: auto; white-space: pre-wrap; font-family: monospace;">${
                            naginiResult?.stderr
                        }</pre>
                    </details>
                    <details>
                        <summary class="font-mono pl-4">Complete Nagini Result</summary>
                        <pre style="padding: 1rem; border-radius: 0.5rem; overflow-x: auto; white-space: pre-wrap; font-family: monospace;">${
                            JSON.stringify(naginiResult, null, 2)
                        }</pre>
                    </details>
                </div>
    </div>
    </div>
        `;

          containerEl.appendChild(div);

          if (window.renderMathInElement) {
              window.renderMathInElement(div, {
                  delimiters: [{
                      left: "$$",
                      right: "$$",
                      display: true,
                  }, {
                      left: "$",
                      right: "$",
                      display: false,
                  }, {
                      left: "\\(",
                      right: "\\)",
                      display: false,
                  }, {
                      left: "\\[",
                      right: "\\]",
                      display: true,
                  }, ],
              });
          }
      }


      function displayIndicatorNaginiIsReady() {
          const naginiDot = document.getElementById("nagini-dot");
          if (naginiDot) {
              naginiDot.classList.replace("badge-warning", "badge-success");
          }
          const naginiLabel = document.getElementById("nagini-label");
          if (naginiLabel) {
              naginiLabel.textContent = "Nagini ready";
          }
      }

      /**
       * Removes all 'class' attributes from HTML elements in a string, to prevent
       * CSS conflicts from frameworks like DaisyUI during PDF generation.
       * @param {string} htmlString - The HTML string to sanitize.
       * @returns {string} The sanitized HTML string without classes.
       */
      function stripClasses(htmlString) {
          if (!htmlString) return '';
          const parser = new DOMParser();
          const doc = parser.parseFromString(htmlString, 'text/html');
          doc.body.querySelectorAll('*').forEach(node => {
              node.removeAttribute('class');
          });
          return doc.body.innerHTML;
      }

      function generatePdf() {
          console.log("Generating PDF from statements");

          if (generatedQuestions.length === 0) {
              console.error("No questions generated to create a PDF.");
              return;
          }

          // Create an invisible iframe to build the PDF content in total isolation.
          const iframe = document.createElement('iframe');
          iframe.style.position = 'absolute';
          iframe.style.width = '0';
          iframe.style.height = '0';
          iframe.style.border = 'none';
          document.body.appendChild(iframe);

          const iDoc = iframe.contentWindow.document;
          iDoc.open();
          iDoc.write('<html><head></head><body></body></html>');
          iDoc.close();
          iDoc.body.style.margin = "0";
          iDoc.body.style.padding = "0";
          iDoc.documentElement.style.margin = "0";
          iDoc.documentElement.style.padding = "0";

          const style = iDoc.createElement('style');
          style.textContent = `
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                box-sizing: border-box;
                -webkit-print-color-adjust: exact;
                background: #fff;
            }
            * { box-sizing: border-box; }
            p { margin: 0; }
        `;
          iDoc.head.appendChild(style);

          const pdfContent = iDoc.createElement('div');
          pdfContent.style.cssText = `
             box-sizing: border-box;
             width: 190mm;
             font-family: 'Arial', sans-serif;
             line-height: 1.6;
             margin: 0;
             padding: 0;
         `;
          // pdfContent.style.borderTop = "2px solid red"; // Uncomment for debugging
          iDoc.body.appendChild(pdfContent);

          const questionsPerPage = 6;
          for (let i = 0; i < generatedQuestions.length; i += questionsPerPage) {
              const pageQuestions = generatedQuestions.slice(i, i + questionsPerPage);

              const pageDiv = iDoc.createElement('div');
              if (i + questionsPerPage < generatedQuestions.length) {
                  pageDiv.style.pageBreakAfter = 'always';
              }

              const infoDiv = iDoc.createElement('div');
              infoDiv.style.cssText = `border: 0.1px solid #eef2f4; border-radius: 0.5rem; padding: 2mm; margin-bottom: 10mm; background-color: #fefefe; color: #0f1419;`;
              infoDiv.innerHTML = `<table style="width: 100%; font-family: 'Courier New', monospace; border-collapse: collapse;">
                <tbody>
                    <tr>
                        <td style="width: 50%; vertical-align: top;"><div>Nom :</div><div>Prénom :</div></td>
                        <td style="width: 50%; vertical-align: top;">
                            <table style="width: 100%; border-collapse: collapse;">
                                <tbody>
                                    <tr>
                                        <td style="width: 50%; vertical-align: top;"><div>Classe :</div><div>Date :</div></td>
                                        <td style="width: 50%; vertical-align: top;">
                                            <div style="border: 1px solid #eef2f4; border-radius: 0.25rem; padding: 0.1em 0.5em; font-size: 0.8em; font-weight: 100; display: inline-block; margin-bottom: 2px;">BolzanoBleu</div>
                                            <div style="border: 1px solid #eef2f4; border-radius: 0.25rem; padding: 0.1em 0.5em; font-size: 0.8em; font-weight: 100; display: inline-block;">Spé</div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>`;
              pageDiv.appendChild(infoDiv);

              const titleDiv = iDoc.createElement('div');
              titleDiv.style.cssText = `font-size: 1.2rem; margin-bottom: 0mm; font-family: 'Times New Roman', serif;`;
              titleDiv.innerHTML = 'Bac 1ère Spé. Maths : Partie 1 automatismes';
              pageDiv.appendChild(titleDiv);

              const subtitleDiv = iDoc.createElement('div');
              subtitleDiv.style.cssText = `font-size: 1rem; margin-bottom: 10mm; font-family: 'Arial', sans-serif; font-style: italic;`;
              subtitleDiv.innerHTML = 'Questions inspirées des Sujets 0';
              pageDiv.appendChild(subtitleDiv);

              pageQuestions.forEach((question, index) => {
                  let statementContent = question.statement;
                  // Remove all classes from the statement HTML
                  statementContent = stripClasses(statementContent);
                  const tempDiv = iDoc.createElement('div');
                  tempDiv.innerHTML = statementContent;
                  // Optionally, render math here if needed (see previous suggestions)
                  tempDiv.querySelectorAll('[class]').forEach(el => el.removeAttribute('class'));
                  statementContent = tempDiv.innerHTML;

                  const questionWrapper = iDoc.createElement('div');
                  questionWrapper.style.cssText = `font-size: 0.9rem; margin-bottom: 10mm; border: 0.1px solid #eef2f4; border-radius: 0.5rem; padding: 5mm; background-color: #fefefe; color: #0f1419; break-inside: avoid;`;
                  let innerHtml = (i + index + 1) + ") " + statementContent + "<br />";
                  innerHtml += "<hr style='margin: 0.5rem 0; border: 0; border-top: 0.1px solid #eef2f4;' />";
                  innerHtml += "<div style='height:2cm'></div>";
                  questionWrapper.innerHTML = innerHtml;
                  pageDiv.appendChild(questionWrapper);
              });
              pdfContent.appendChild(pageDiv);
          }

          console.log("Final HTML for PDF conversion:", pdfContent.outerHTML);

          const options = {
              margin: 0,
              filename: 'arpege-questions.pdf',
              image: {
                  type: 'jpeg',
                  quality: 0.98
              },
              html2canvas: {
                  scale: 2,
                  useCORS: true,
                  logging: true
              },
              jsPDF: {
                  unit: 'mm',
                  format: 'a4',
                  orientation: 'portrait'
              }
          };

          html2pdf().from(pdfContent).set(options).save()
              .catch(err => {
                  console.error("PDF generation error:", err);
              })
              .finally(() => {
                  console.log("PDF generation finished.");
                  document.body.removeChild(iframe);
              });
      }

      // Wait for DOM to be ready before adding event listeners
      if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', setupEventListeners);
      } else {
          setupEventListeners();
      }

      function setupEventListeners() {
          // Add event listener only if element exists
          const arpegeForm = document.getElementById('arpege-form');
          if (arpegeForm) {
              arpegeForm.addEventListener('submit', function(e) {
                  e.preventDefault();
                  arpegeGenerator();
              });
          }

          // Add download PDF button listener if it exists
          const downloadPdfBtn = document.getElementById('download-pdf-btn');
          if (downloadPdfBtn) {
              downloadPdfBtn.addEventListener('click', function() {
                  generatePdf();
              });
          }
      }