// mason.js
import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/npm/lit-element@4.2.0/+esm";
import { unsafeHTML } from "https://cdn.jsdelivr.net/npm/lit-html@3.1.0/directives/unsafe-html.js";

/**
 * Simple logger for Brick classes that shows correct line numbers
 */
class BrickLogger {
  constructor() {
    this.prefix = "🧱";
    this.tabChar = "  ";
    this._isFirstLog = true;
  }

  log(...args) {
    const prefix = this._isFirstLog
      ? this.prefix
      : `${this.tabChar}${this.prefix}`;
    if (this._isFirstLog) this._isFirstLog = false;

    if (typeof args[0] === "string") {
      console.log(`${prefix} ${args[0]}`, ...args.slice(1));
      window.atlas.add(
        this.prefix,
        "log",
        `${args[0]} ${args.slice(1).join(" ")}`
      );
    } else {
      console.log(prefix, ...args);
      window.atlas.add(this.prefix, "log", args.join(" "));
    }
  }

  warn(...args) {
    const prefix = this._isFirstLog
      ? this.prefix
      : `${this.tabChar}${this.prefix}`;
    if (this._isFirstLog) this._isFirstLog = false;

    if (typeof args[0] === "string") {
      console.warn(`${prefix} ${args[0]}`, ...args.slice(1));
      window.atlas.add(
        this.prefix,
        "warn",
        `${args[0]} ${args.slice(1).join(" ")}`
      );
    } else {
      console.warn(prefix, ...args);
      window.atlas.add(this.prefix, "warn", args.join(" "));
    }
  }

  error(...args) {
    const prefix = this._isFirstLog
      ? this.prefix
      : `${this.tabChar}${this.prefix}`;
    if (this._isFirstLog) this._isFirstLog = false;

    if (typeof args[0] === "string") {
      console.error(`${prefix} ${args[0]}`, ...args.slice(1));
      window.atlas.add(
        this.prefix,
        "error",
        `${args[0]} ${args.slice(1).join(" ")}`
      );
    } else {
      console.error(prefix, ...args);
      window.atlas.add(this.prefix, "error", args.join(" "));
    }
  }
}

const brickLogger = new BrickLogger();
/**
 * Brick Component Lifecycle:
 *
 * 1. Construction Phase:
 *    - constructor(): Initialize properties, setup logger
 *    - createRenderRoot(): Configure shadow DOM (disabled for DaisyUI compatibility)
 *
 * 2. Connection Phase:
 *    - connectedCallback(): Component attached to DOM
 *      - Super class setup
 *      - Log connection status
 *      - Initialize any external dependencies
 *
 * 3. Update/Render Phase:
 *    - render(): Create the component's view
 *    - firstUpdated(): Called after first render
 *      - Setup MathLive fields
 *      - Initialize event listeners
 *    - updated(): Called after each update
 *      - Process LaTeX rendering
 *      - Handle property changes
 *
 * 4. Disconnection Phase:
 *    - disconnectedCallback(): Component removed from DOM
 *      - Cleanup event listeners
 *      - Reset state if needed
 */

/**
 * Mixin that adds logging capabilities to a brick component.
 * @param {typeof LitElement} Base - The base class to extend from
 * @returns {typeof LitElement} A class with logging capabilities
 */
const LoggedBrickMixin = (Base) =>
  class extends Base {
    constructor() {
      super();
      this.logger = brickLogger;
    }
  };

/**
 * Mixin that adds LaTeX rendering capabilities to a brick component.
 * @param {typeof LitElement} Base - The base class to extend from
 * @returns {typeof LitElement} A class with LaTeX rendering capabilities
 */
const LatexBrickMixin = (Base) =>
  class extends Base {
    static properties = {
      ...super.properties,
      renderLatex: { type: Boolean, attribute: "render-latex" },
    };

    constructor() {
      super();
      this.renderLatex = true;
    }

    updated(changedProperties) {
      super.updated(changedProperties);
      if (this.renderLatex) {
        requestAnimationFrame(() => {
          renderMathInElement(this, {
            delimiters: [
              { left: "$$", right: "$$", display: true },
              { left: "$", right: "$", display: false },
            ],
          });
        });
      }
    }
  };

/**
 * Mixin that adds component styling capabilities (injects styles to document head)
 * @param {typeof LitElement} Base - The base class to extend from
 * @returns {typeof LitElement} A class with styling capabilities
 */
const StyledBrickMixin = (Base) =>
  class extends Base {
    constructor() {
      super();
      // Add component styles when component is created
      if (this.getComponentStyles) {
        this.addComponentStyles();
      }
    }

    // Add component-specific styles to document head
    addComponentStyles() {
      const styleId = this.getStyleId();
      if (!document.getElementById(styleId)) {
        const style = document.createElement("style");
        style.id = styleId;
        style.textContent = this.getComponentStyles();
        document.head.appendChild(style);
      }
    }

    // Override these in concrete classes
    getStyleId() {
      return `${this.tagName.toLowerCase()}-styles`;
    }

    getComponentStyles() {
      return "";
    }
  };

/**
 * Factory function to compose multiple mixins cleanly
 * @param {typeof LitElement} Base - The base class
 * @param {...Function} mixins - The mixins to apply
 * @returns {typeof LitElement} A class with all mixins applied
 */
const compose = (Base, ...mixins) => {
  return mixins.reduce((acc, mixin) => mixin(acc), Base);
};

/**
 * Base class for all Brick components with common functionality
 * Explicitly composes all the mixins we need
 */
class BaseBrick extends compose(
  LitElement,
  LoggedBrickMixin,
  LatexBrickMixin,
  StyledBrickMixin
) {
  // Disable shadow DOM so DaisyUI classes work
  createRenderRoot() {
    return this;
  }

  connectedCallback() {
    super.connectedCallback();
    this.logger.log(`${this.constructor.name}: connected`);
  }
}

// Import MathLive
const MATHLIVE_VERSION = "0.105.3";
const mathLiveScript = document.createElement("script");
mathLiveScript.src = `https://cdn.jsdelivr.net/npm/mathlive@${MATHLIVE_VERSION}/mathlive.min.js`;

// Set up MathLive configuration after it loads
mathLiveScript.onload = () => {
  // Configure the virtual keyboard
  window.mathVirtualKeyboard.layouts = ["minimalist"];

  // Disable sounds to prevent 404 errors
  window.MathfieldElement.soundsDirectory = null;
  window.MathfieldElement.keypressVibration = false;
  window.mathVirtualKeyboard.container = document.querySelector("#math-field-virtual-keyboard-container");
};

document.head.appendChild(mathLiveScript);

const mathLiveStyle = document.createElement("link");
mathLiveStyle.rel = "stylesheet";
mathLiveStyle.href = `https://cdn.jsdelivr.net/npm/mathlive@${MATHLIVE_VERSION}/mathlive-static.min.css`;
document.head.appendChild(mathLiveStyle);

// Add style to hide menu toggle
const hideMenuToggleStyle = document.createElement("style");
hideMenuToggleStyle.textContent = `
    math-field::part(menu-toggle) {
        display: none;
    }
`;
document.head.appendChild(hideMenuToggleStyle);

export class CurriculumBrick extends BaseBrick {
  static properties = {
    ...super.properties,
    data: { type: Object },
    activeTab: { type: String },
  };

  constructor() {
    super();
    this.data = null;
    this.activeTab = "";
  }

  // Override to provide component-specific styles
  getComponentStyles() {
    return `
            curriculum-brick {
                display: block;
            }
            
            curriculum-brick #curriculum-select {
                width: 100% !important;
            }
        `;
  }

  // Initialize active tab with first available curriculum
  connectedCallback() {
    super.connectedCallback();
    if (this.data && !this.activeTab) {
      const availableTabs = Object.keys(this.data);
      if (availableTabs.length > 0) {
        this.activeTab = availableTabs[0];
      }
    }
  }

  // Find the programme node in the tree
  findProgrammeNode(node) {
    if (node.name === "programme") {
      return node;
    }
    if (node.children) {
      for (const child of node.children) {
        const found = this.findProgrammeNode(child);
        if (found) return found;
      }
    }
    return null;
  }

  // Render a tree node with nice DaisyUI styling
  renderTreeNode(node, level = 0) {
    const hasChildren = node.children && node.children.length > 0;

    // Clean up the name - replace underscores with spaces
    const displayName = node.name.replace(/_/g, " ");

    // Different styling based on level
    if (level === 0) {
      // Main sections (algèbre, analyse, etc.) - use cards without white background
      return html`
        <div class="bg-base-200 mb-4 rounded-lg">
          <div class="">
            <h2 class="text-primary text-xl mb-3 font-bold">${displayName}</h2>
            ${hasChildren
              ? html`
                  <div class="space-y-2">
                    ${node.children.map((child) =>
                      this.renderTreeNode(child, level + 1)
                    )}
                  </div>
                `
              : ""}
          </div>
        </div>
      `;
    } else if (level === 1) {
      // Subsections - use smaller cards with white background
      return html`
        <div class="card bg-base-100 border border-base-200 mb-3">
          <div class="card-body p-3">
            <h3 class="font-semibold text-lg text-secondary mb-2">
              ${displayName}
            </h3>
            ${hasChildren
              ? html`
                  <div class="space-y-1 ml-2">
                    ${node.children.map((child) =>
                      this.renderTreeNode(child, level + 1)
                    )}
                  </div>
                `
              : ""}
          </div>
        </div>
      `;
    } else {
      // Leaf items - simple badges or text with white background
      return html`
        <div
          class="flex items-start gap-2 py-3 px-4 rounded-lg hover:bg-base-200 transition-colors bg-base-100 border border-base-300"
        >
          <div class="w-2 h-2 rounded-full bg-accent mt-2 flex-shrink-0"></div>
          <span class="text-sm">${displayName}</span>
        </div>
      `;
    }
  }

  // Handle select change
  handleSelectChange(event) {
    this.activeTab = event.target.value;
    this.logger.log("Curriculum changed to:", this.activeTab);
  }

  // Get the current curriculum data based on active tab
  getCurrentCurriculumData() {
    if (!this.data || !this.activeTab) return null;
    const curriculumInfo = this.data[this.activeTab];
    return curriculumInfo?.data || curriculumInfo; // Support both new and old format
  }

  // Get the display name for a curriculum
  getCurriculumDisplayName(key) {
    const curriculumInfo = this.data[key];
    if (curriculumInfo?.name) {
      return curriculumInfo.name;
    }
    // Fallback to capitalized key
    return key.charAt(0).toUpperCase() + key.slice(1);
  }

  render() {
    if (!this.data || Object.keys(this.data).length === 0) {
      return html`
        <div class="max-w-4xl mx-auto text-center">
          <div class="loading loading-spinner loading-lg"></div>
          <p class="mt-4">Loading curriculum data...</p>
        </div>
      `;
    }

    // Get available curriculum levels
    const availableTabs = Object.keys(this.data);

    // Set default active tab if none set
    if (!this.activeTab && availableTabs.length > 0) {
      this.activeTab = availableTabs[0];
    }

    const currentData = this.getCurrentCurriculumData();

    if (currentData?.error) {
      return html`
        <div class="max-w-4xl mx-auto">
          <div class="alert alert-error">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="stroke-current shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>${currentData.error}</span>
          </div>
        </div>
      `;
    }

    if (!currentData) {
      return html`
        <div class="max-w-4xl mx-auto">
          <div class="alert alert-warning">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="stroke-current shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
            <span>No curriculum data found for ${this.activeTab}</span>
          </div>
        </div>
      `;
    }

    // Find the programme node
    const programmeNode = this.findProgrammeNode(currentData.tree);

    if (!programmeNode) {
      return html`
        <div class="max-w-4xl mx-auto">
          <div class="alert alert-warning">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="stroke-current shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"
              />
            </svg>
            <span>Programme section not found in curriculum data</span>
          </div>
        </div>
      `;
    }

    return html`
      <div class="max-w-4xl mx-auto">
        <!-- Select dropdown for curriculum levels -->
        <div class="mb-6">
          <!-- <div class="mb-2">
                        <span class="text-sm text-gray-600">Choisir le niveau :</span>
                    </div> -->
          <select
            id="curriculum-select"
            class="select select-bordered select-lg select-primary w-[100%] mb-6"
            @change="${this.handleSelectChange}"
            .value="${this.activeTab}"
          >
            ${availableTabs.map(
              (tab) => html`
                <option value="${tab}" ?selected="${this.activeTab === tab}">
                  ${this.getCurriculumDisplayName(tab)}
                </option>
              `
            )}
          </select>
        </div>

        <!-- Header with curriculum info -->
        <!-- <div class="mb-6">
                    <h1 class="text-xl font-bold mb-2">Programme - ${this.getCurriculumDisplayName(
          this.activeTab
        )}</h1>
                    <div class="text-sm text-gray-500 mb-4">
                        Curriculum: ${currentData.metadata?.curriculum ||
        "Unknown"}
                    </div>
                </div> -->

        <!-- Tree content -->
        <div class="space-y-2">
          ${programmeNode.children.map((child) => this.renderTreeNode(child))}
        </div>
      </div>
    `;
  }
}

customElements.define("curriculum-brick", CurriculumBrick);

export class PronoiaBrick extends BaseBrick {
  static properties = {
    ...super.properties,
    data: { type: Object },
    mathFieldValue: { type: String },
  };

  constructor() {
    super();
    this.data = null;
    this.mathFieldValue = "";
  }

  // Override to provide component-specific styles
  getComponentStyles() {
    return `
            pronoia-brick {
                display: block;
            }
            
            pronoia-brick math-field::part(menu-toggle) {
                display: none;
            }
        `;
  }

  firstUpdated() {
    // Initialize MathLive field after the component is mounted
    const mathField = this.querySelector("math-field");
    if (mathField) {
      mathField.addEventListener("input", (evt) => {
        this.mathFieldValue = evt.target.value;
        this.logger.log("Math input:", this.mathFieldValue);
      });

      // Set up simple keyboard layout when focused
      mathField.addEventListener("focus", () => {
        mathVirtualKeyboard.layouts = {
          rows: [
            [
              { latex: "+" },
              { latex: "-" },
              { latex: "\\times" },
              { latex: "\\div" },
              { latex: "=" },
              { latex: "\\sqrt{#0}" },
              { latex: "#@^{#?}" },
              { latex: "\\frac{#@}{#?}" },
            ],
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
          ],
        };
        mathVirtualKeyboard.visible = true;
      });
    }
  }

  renderSkeleton() {
    return html`
      <div class="max-w-2xl mx-auto p-4">
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <!-- Title skeleton -->
            <div class="h-8 bg-gray-200 rounded-lg w-1/2 mb-6"></div>

            <!-- Statement skeleton -->
            <div class="space-y-3 mb-6">
              <div class="h-4 bg-gray-200 rounded-lg w-full"></div>
              <div class="h-4 bg-gray-200 rounded-lg w-5/6"></div>
              <div class="h-4 bg-gray-200 rounded-lg w-4/6"></div>
            </div>

            <!-- Input field skeleton -->
            <div class="space-y-2">
              <div class="h-4 bg-gray-200 rounded-lg w-24"></div>
              <div class="h-16 bg-gray-200 rounded-lg w-full"></div>
            </div>
          </div>
        </div>

        <!-- Components table skeleton -->
        <div class="overflow-x-auto mt-4">
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body space-y-4">
              <div class="h-6 bg-gray-200 rounded-lg w-32"></div>
              <div class="space-y-3">
                <div class="h-4 bg-gray-200 rounded-lg w-full"></div>
                <div class="h-4 bg-gray-200 rounded-lg w-full"></div>
                <div class="h-4 bg-gray-200 rounded-lg w-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  render() {
    if (!this.data) {
      return this.renderSkeleton();
    }

    const { missive } = this.data;
    if (!missive?.question)
      return html`
        <div class="max-w-2xl mx-auto p-4">
          <div class="alert alert-error">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="stroke-current shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>No question data available</span>
          </div>
        </div>
      `;

    return html`
      <div class="max-w-2xl mx-auto p-4">
        <!-- Question Card -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <p class="text-lg">${missive.question.statement}</p>

            <!-- Math input field -->
            <div class="">
              <label class="label">
                <span class="label-text">Ta réponse :</span>
              </label>
              <math-field
                style="width: 100%; min-height: 60px; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.5rem; font-size: 1.1rem;"
                virtual-keyboard-mode="onfocus"
                .virtual-keyboard-layout=${JSON.stringify({
                  rows: [
                    [
                      { latex: "+" },
                      { latex: "-" },
                      { latex: "\\times" },
                      { latex: "\\div" },
                      { latex: "=" },
                      { latex: "\\sqrt{#0}" },
                      { latex: "#@^{#?}" },
                      { latex: "\\frac{#@}{#?}" },
                    ],
                    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                  ],
                })}
                >${this.mathFieldValue}</math-field
              >
            </div>
          </div>
        </div>

        <!-- Components Card -->
        <div class="card bg-base-100 shadow-xl mt-4">
          <div class="card-body">
            <div class="overflow-x-auto">
              <table class="table">
                <thead>
                  <tr>
                    <th>Component</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="font-medium">base</td>
                    <td>${missive.question.components.base}</td>
                  </tr>
                  <tr>
                    <td class="font-medium">exponent1</td>
                    <td>${missive.question.components.exponent1}</td>
                  </tr>
                  <tr>
                    <td class="font-medium">exponent2</td>
                    <td>${missive.question.components.exponent2}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

customElements.define("pronoia-brick", PronoiaBrick);

export class PronoiaSujets0QcmBrick extends BaseBrick {
  static properties = {
    ...super.properties,
    data: { type: Object },
    mathFieldValue: { type: String },
  };

  constructor() {
    super();
    this.data = null;
    this.mathFieldValue = "";
  }

  // Override to provide component-specific styles
  getComponentStyles() {
    return `
      pronoia-sujets-0-qcm-brick {
        display: block;
      }
      
      pronoia-sujets-0-qcm-brick math-field::part(menu-toggle) {
        display: none;
      }



      
      /* Ensure consistent card height */
      pronoia-sujets-0-qcm-brick .exercise-card {
        min-height: 350px;
        margin: 0 auto;
      }
      
      /* Header tag sizing consistency */
      pronoia-sujets-0-qcm-brick .tag-skeleton {
        height: 18px;
        border-radius: 12px;
      }
      
      /* Question text area consistency */
      pronoia-sujets-0-qcm-brick .question-area {

      }
      
      /* Math field area consistency */
      pronoia-sujets-0-qcm-brick .math-field-area {
      }


      pronoia-sujets-0-qcm-brick .card-body {
        max-width: 100%;
      }

      @media (min-width: 640px) {
        pronoia-sujets-0-qcm-brick .card-body {
          padding: 2rem 4rem;
        }

        pronoia-sujets-0-qcm-brick .card-header {
          padding-left: 4rem;
          padding-right: 4rem;
        }
      }


      pronoia-sujets-0-qcm-brick .badge {
       gap: 0.1rem;
      }

      pronoia-sujets-0-qcm-brick .breadcrumbs {
        font-size: 0.8rem;
      }

      pronoia-sujets-0-qcm-brick .breadcrumbs ul li a{
        gap: 0.1rem;
      }
    `;
  }

  firstUpdated() {
    // Only set up elements if we have data (not showing skeleton)
    if (this.data) {
      this.setupMathField();
      this.setupAnswerButton();
    }
  }

  setupMathField() {
    // Initialize MathLive field after the component is mounted
    const mathField = this.querySelector("math-field");
    if (mathField) {
      mathField.addEventListener("input", (evt) => {
        this.mathFieldValue = evt.target.value;
        this.logger.log("Math input:", this.mathFieldValue);
      });

      // // Set up simple keyboard layout when focused
      // mathField.addEventListener("focus", () => {
      //   mathVirtualKeyboard.layouts = {
      //     rows: [
      //       [
      //         { latex: "+" },
      //         { latex: "-" },
      //         { latex: "\\times" },
      //         { latex: "\\div" },
      //         { latex: "=" },
      //         { latex: "\\sqrt{#0}" },
      //         { latex: "#@^{#?}" },
      //         { latex: "\\frac{#@}{#?}" },
      //       ],
      //       ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
      //     ],
      //   };
      //   mathVirtualKeyboard.visible = true;
      // });
    }
  }

  setupAnswerButton() {
    // Set up answer button event listener
    const answerButton = this.querySelector("#answer-button");
    this.logger.log("Looking for answer button:", answerButton);
    if (answerButton) {
      this.logger.log("Answer button found, attaching event listener");
      // Remove any existing listeners to avoid duplicates
      answerButton.replaceWith(answerButton.cloneNode(true));
      const newButton = this.querySelector("#answer-button");
      newButton.addEventListener("click", () => {
        this.logger.log("answer-button clicked");
        const mathFieldElement = this.querySelector("math-field");
        this.logger.log("math field element:", mathFieldElement);
        if (mathFieldElement) {
          const answer = mathFieldElement.value;
          this.logger.log("answer", answer);
        } else {
          this.logger.error("math field not found");
        }
      });
    } else {
      this.logger.error("Answer button not found");
      // Try again after a short delay
      setTimeout(() => this.setupAnswerButton(), 100);
    }
  }

  updated(changedProperties) {
    super.updated(changedProperties);
    // Set up elements when data becomes available
    if (changedProperties.has('data') && this.data && this.data.missive?.question) {
      setTimeout(() => {
        this.setupMathField();
        this.setupAnswerButton();
      }, 0);
    }
  }

  // PIECE 1 & 2: Skeleton Header with Tag Placeholders
  renderSkeletonHeader() {
    return html`
    
      <div
        class="card-header flex justify-between items-center px-4 py-2 border-b border-base-200"
      >


      <div class="breadcrumbs text-sm">
          <ul>
            <li><a class="tag-skeleton bg-gray-200 w-20"></a></li>
            <li><a class="tag-skeleton bg-gray-200 w-12"></a></li>
            <li><a class="tag-skeleton bg-gray-200 w-16"></a></li>
          </ul>
        </div>
        <!-- <div class="flex gap-2">
          <div class="tag-skeleton h-[1.25rem] bg-gray-200 w-20"></div>
          <div class="tag-skeleton h-[1.25rem] bg-gray-200 w-12"></div>
          <div class="tag-skeleton h-[1.25rem] bg-gray-200 w-16"></div>
        </div>

        <div class="tag-skeleton h-[1.25rem] bg-gray-200 w-24"></div> -->
      </div>
    `;
  }

  // PIECE 3: Rendered Header with Actual Tags
  renderActualHeader() {
    return html`
      <div
        class="card-header flex justify-between items-center px-4 py-2 border-b border-base-200"
      >
        <div class="breadcrumbs text-sm text-base-content/60">
          <ul>
            <li><a>Baccalauréat</a></li>
            <li><a>Automatismes</a></li>
            <li><a>Question A</a></li>
          </ul>
        </div>
        <!-- <div class="flex gap-2">
          <div class="badge badge-accent badge-sm">1<sup>ère</sup></div>
          <div class="badge badge-accent badge-sm">Maths Spé</div>
        </div> -->
        <!-- <div class="flex gap-2">
          <div class="badge badge-outline badge-sm">
            Sujet 0 | <span class="text-primary"> &nbsp;Question A</span>
          </div>
        </div> -->
      </div>
    `;
  }

  // PIECE 4: Question Body Skeleton
  renderSkeletonBody() {
    return html`
      <div class="card-body p-6 flex flex-col justify-center">
        <!-- Question text skeleton - centered in upper half -->
        <div class="question-area flex-1 flex items-center justify-center mb-8">
          <div class="space-y-3 w-full">
            <div class="h-4 bg-gray-200 rounded w-full"></div>
            <div class="h-4 bg-gray-200 rounded w-5/6"></div>
          </div>
        </div>

        <!-- Math field skeleton - centered in lower half -->
        <div class="math-field-area flex-1 flex flex-col justify-center">
          <label class="label mb-1">
            <span class="label-text font-light text-sm"></span>
          </label>
          <div class="h-4 bg-gray-200 rounded w-24 mb-3"></div>
          <div class="h-16 bg-gray-200 rounded w-full mb-4"></div>

          <!-- Clue button skeleton -->
          <div class="flex justify-center">
            <div class="h-8 bg-gray-200 rounded w-20"></div>
          </div>
        </div>
      </div>
    `;
  }

  // PIECE 5: Actual Question Body
  renderActualBody(missive) {
    return html`
      <div class="card-body justify-center">
        <!-- Question text - centered in upper half -->
        <div class="question-area flex-1 flex items-center justify-center mb-0">
          <p class="text-left">
            <span class="text-lg">${missive.question.statement}</span><br>
          </p>
        </div>

        
        <div class="math-field-area flex-1 flex flex-col justify-center mt-0">
        <span class="font-light text-sm italic mb-1">${missive.question.answer_formating}</span>
          <math-field
            style="width: 100%; padding: 0.15rem; border: 1px solid var(--color-primary); background-color: var(--color-base-100); border-radius: var(--radius-selector); font-size: 1.2rem;"
            virtual-keyboard-mode="onfocus"
            >${this.mathFieldValue}</math-field
          >
        </div>


          <!-- Clue button -->
          <div class="flex gap-4  mt-4">
          <button
              id="answer-button"
              class="btn btn-sm btn-soft btn-error"
            >
              Répondre
            </button>
            <button
              class="btn btn-sm btn-soft btn-success ml-auto"
              @click="${this.handleClueClick}"
            >
              Indice
            </button>
            <button
              class="btn btn-sm btn-soft"
              @click="${this.handleClueClick}"
            >
              Pourquoi cette question ?
            </button>
          </div>
      </div>
    `;
  }

  // PIECE 7: Complete Skeleton Layout
  renderSkeleton() {
    return html`
      <div class="mx-auto">
        <h2 class="text-xl px-4 font-bold mb-6">1<sup>ère</sup> Spécialité Mathématiques</h2>
        <div class="card bg-base-100 shadow-lg sm:shadow-xl exercise-card">
          ${this.renderSkeletonHeader()} ${this.renderSkeletonBody()}
        </div>
      </div>
    `;
  }

  // PIECE 7: Complete Rendered Layout
  renderComplete(missive) {
    return html`
      <div class="mx-auto">
        <h2 class="text-xl px-4 font-bold mb-6">1<sup>ère</sup> Spécialité Mathématiques</h2>
        <div class="card bg-base-100 shadow-lg sm:shadow-xl exercise-card">
          ${this.renderActualHeader()} ${this.renderActualBody(missive)}
        </div>
      </div>
    `;
  }

  render() {
    if (!this.data) {
      return this.renderSkeleton();
    }

    const { missive } = this.data;
    if (!missive?.question) {
      return html`
        <div class="max-w-2xl mx-auto p-4">
          <div class="alert alert-error">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="stroke-current shrink-0 h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>No question data available</span>
          </div>
        </div>
      `;
    }

    return this.renderComplete(missive);
  }

  handleClueClick() {
    this.logger.log("Clue button clicked");
    // TODO: Implement clue display logic
    // You can show a modal, expand a section, etc.
  }
}

customElements.define("pronoia-sujets-0-qcm-brick", PronoiaSujets0QcmBrick);

class ToastBrick extends BaseBrick {
  static properties = {
    ...super.properties,
    data: { type: Object },
    closable: { type: Boolean },
    autoHide: { type: Boolean },
    duration: { type: Number },
    semanticClass: { type: String },
  };

  constructor() {
    super();
    this.data = null;
    this.closable = false;
    this.autoHide = false;
    this.duration = 5; // default 5 seconds
    this.autoHideTimer = null;
  }

  connectedCallback() {
    super.connectedCallback();

    // Start auto-hide timer if enabled
    if (this.autoHide && this.duration > 0) {
      this.startAutoHideTimer();
    }
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this.clearAutoHideTimer();
  }

  startAutoHideTimer() {
    this.clearAutoHideTimer();
    this.autoHideTimer = setTimeout(() => {
      this.hideToast();
    }, this.duration * 1000);
  }

  clearAutoHideTimer() {
    if (this.autoHideTimer) {
      clearTimeout(this.autoHideTimer);
      this.autoHideTimer = null;
    }
  }

  hideToast() {
    // Add fade out animation
    this.style.opacity = "0";
    this.style.transition = "opacity 0.3s ease";

    // Remove element after animation
    setTimeout(() => {
      if (this.parentNode) {
        this.parentNode.removeChild(this);
      }
    }, 300);
  }

  handleClose() {
    this.hideToast();
  }

  render() {
    if (!this.data) {
      return html``;
    }

    return html`
      <div class="toast toast-top toast-center">
        <div class="alert alert-${this.semanticClass} mt-18">
          <div class="flex items-center justify-between gap-4">
            <span class="flex-grow">${this.data.message}</span>
            ${this.closable
              ? html`
                  <button
                    class="btn btn-ghost btn-xs"
                    @click="${this.handleClose}"
                    aria-label="Close toast"
                  >
                    ✕
                  </button>
                `
              : ""}
          </div>
        </div>
      </div>
    `;
  }
}

customElements.define("toast-brick", ToastBrick);
