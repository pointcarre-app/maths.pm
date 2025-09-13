const teachersGitTag = 'v0.0.27';
const v4PyJsGitTag = "v0.0.27";
const naginiGitTag = "v0.0.21";


export const configSujets0DataOnly = {

    domtoimageUrl: 'https://cdn.jsdelivr.net/npm/dom-to-image@2.6.0/+esm',
    // For having a seed for generating the seeds per copy
    // In between 0 and 100 - 14 
    rootSeed: 14,
    teachersGitTag: teachersGitTag,
    teachersUrlsToPaths: [
        { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/__init__.py`, path: "teachers/__init__.py" },
        { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/generator.py`, path: "teachers/generator.py" },
        { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/maths.py`, path: "teachers/maths.py" },
        { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/formatting.py`, path: "teachers/formatting.py" },
        { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/corrector.py`, path: "teachers/corrector.py" },
        { url: `https://cdn.jsdelivr.net/gh/pointcarre-app/teachers@${teachersGitTag}/src/teachers/defaults.py`, path: "teachers/defaults.py" }
    ],

    v4PyJsGitTag: v4PyJsGitTag,
    v4PyJsPCAGraphLoaderUrl: `https://cdn.jsdelivr.net/gh/pointcarre-app/v4.py.js@${v4PyJsGitTag}/scenery/packaged/PCAGraphLoader.js`,


    naginiGitTag: naginiGitTag,
    naginiJsUrl: `https://esm.sh/gh/pointcarre-app/nagini@${naginiGitTag}/src/nagini.js?bundle`,   
    naginiPyodideWorkerUrl:`https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@${naginiGitTag}/src/pyodide/worker/worker-dist.js`,


    sujets0Spe1Generators: [

        
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
        //
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
        //
        // "gen_sujet2_auto_01_question.py",
        // "gen_sujet2_auto_02_question.py",
        // "gen_sujet2_auto_03_question.py",
        // "gen_sujet2_auto_04_question.py",
        // "gen_sujet2_auto_05_question.py",
        // "gen_sujet2_auto_06_question.py",
        // "gen_sujet2_auto_07_question.py",
        // "gen_sujet2_auto_08_question.py",
        // "gen_sujet2_auto_09_question.py",
        // "gen_sujet2_auto_10_question.py",
        // "gen_sujet2_auto_11_question.py",
        // "gen_sujet2_auto_12_question.py",
      ],


    sujets0Spe1GeneratorsToGraphFileMap: {
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
        ]
    }
};


/**
 * Generic function to dynamically load a module from a URL
 * @param {string} url - The URL of the module to load
 * @returns {Promise<any>} The loaded module
 */
export async function loadModuleDynamically(url) {
    try {
        const module = await import(url);
        return module;
    } catch (error) {
        console.error(`Failed to load module from ${url}:`, error);
        throw error;
    }
}


/**
 * Detect if browser is Safari
 * @returns {boolean} True if Safari, false otherwise
 */
export function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
  }
  






