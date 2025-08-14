import {
    LatexUtils
} from '../utils/latex.js';
import {
    ImportHelper
} from '../utils/import-helper.js';

class QuestionFactory {
    /**
     * Creates a question by executing a Python script in Pyodide.
     *
     * @param {string} pythonFileUrl - The URL of the Python script to execute.
     * @param {object} naginiManager - The Nagini manager instance.
     * @param {object} NaginiClass - The Nagini class (passed as parameter to avoid import dependencies).
     * @param {boolean} [includeRawResult=false] - Whether to include the raw Nagini execution result in the output.
     * @param {boolean} [includeMetadata=false] - Whether to include browser metadata in the output.
     * @returns {Promise<Question & {rawResult?: object}>} A promise that resolves to the created question object.
     */
    static async createFromPyodide(pythonFileUrl, naginiManager, NaginiClass, includeNaginiResult = false, includeMetadata = false) {
        if (!pythonFileUrl || !naginiManager || !NaginiClass) {
            throw new Error("pythonFileUrl, naginiManager, and NaginiClass are required.");
        }

        try {
            const result = await NaginiClass.executeFromUrl(pythonFileUrl, naginiManager);
            console.log(result);
            const question = JSON.parse(result.missive);

            // Enrich the question object
            // better to use a timestamp based + hash of some highly dynamical stuff + randomUUID() ? 
            // gonna be too long
            question.id = crypto.randomUUID();
            question.pythonFileUrl = pythonFileUrl;

            const filename = pythonFileUrl.split('/').pop();
            const originBase = filename.replace('.py', '');
            // The '1ere_' prefix is currently hardcoded as per the user's request.
            question.origin = `1ere_${originBase}`;

            question.statement = LatexUtils.cleanLatex(question.statement);
            question.answer = LatexUtils.cleanLatex(question.answer);
            question.answer_simplified = LatexUtils.cleanLatex(question.answer_simplified || ""); // TODO remove ""

            if (includeMetadata) {
                // Add comprehensive metadata from the window object
                const performanceEntry = window.performance.getEntriesByType("navigation")[0];

                question.metadata = {
                    createdAtUTC: new Date().toISOString(),
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    browserInfo: {
                        userAgent: window.navigator.userAgent,
                        language: window.navigator.language,
                        languages: window.navigator.languages,
                        platform: window.navigator.platform,
                        vendor: window.navigator.vendor,
                        cookiesEnabled: window.navigator.cookieEnabled,
                        doNotTrack: window.navigator.doNotTrack,
                    },
                    screenInfo: {
                        width: window.screen.width,
                        height: window.screen.height,
                        availWidth: window.screen.availWidth,
                        availHeight: window.screen.availHeight,
                        colorDepth: window.screen.colorDepth,
                        pixelDepth: window.screen.pixelDepth,
                        devicePixelRatio: window.devicePixelRatio,
                    },
                    locationInfo: {
                        href: window.location.href,
                        origin: window.location.origin,
                        hostname: window.location.hostname,
                    },
                    connectionInfo: window.navigator.connection ? {
                        effectiveType: window.navigator.connection.effectiveType,
                        downlink: window.navigator.connection.downlink,
                        rtt: window.navigator.connection.rtt,
                    } : {},
                    performanceInfo: performanceEntry ? performanceEntry.toJSON() : {},
                };
            }
            // Conditionally attach raw execution result
            if (includeNaginiResult) {
                question.naginiResult = result;
            }

            return question;
        } catch (error) {
            console.error(`❌ Error creating question from ${pythonFileUrl}:`, error);
            throw error; // Re-throw the error for the caller to handle
        }
    }

    /**
     * Legacy method for backward compatibility.
     * @deprecated Use createFromPyodide with NaginiClass parameter instead.
     */
    static async createFromPyodideLegacy(pythonFileUrl, naginiManager, includeNaginiResult = false, includeMetadata = false) {
        // Try to get Nagini from global scope or import it dynamically
        let NaginiClass;
        
        if (window.Nagini) {
            NaginiClass = window.Nagini;
        } else {
            try {
                NaginiClass = await ImportHelper.importNagini();
            } catch (importError) {
                throw new Error(`Failed to import Nagini: ${importError.message}. Please pass NaginiClass as a parameter or ensure it's available globally.`);
            }
        }
        
        return this.createFromPyodide(pythonFileUrl, naginiManager, NaginiClass, includeNaginiResult, includeMetadata);
    }

    /**
     * Convenience method that automatically imports Nagini (port-independent)
     * @param {string} pythonFileUrl - The URL of the Python script to execute.
     * @param {object} naginiManager - The Nagini manager instance.
     * @param {boolean} [includeRawResult=false] - Whether to include the raw Nagini execution result in the output.
     * @param {boolean} [includeMetadata=false] - Whether to include browser metadata in the output.
     * @returns {Promise<Question & {rawResult?: object}>} A promise that resolves to the created question object.
     */
    static async createFromPyodideAuto(pythonFileUrl, naginiManager, includeNaginiResult = false, includeMetadata = false) {
        const NaginiClass = await ImportHelper.importNagini();
        return this.createFromPyodide(pythonFileUrl, naginiManager, NaginiClass, includeNaginiResult, includeMetadata);
    }
}

export {
    QuestionFactory
}; 