/**
 * Import Helper - Port-independent dynamic imports
 * Helps avoid hardcoded URLs and makes imports work across different server ports
 */

class ImportHelper {
    /**
     * Dynamically import Nagini from CDN (port-independent)
     * @returns {Promise<object>} Nagini class
     */
    static async importNagini() {
        try {
            const naginiModule = await import('https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@0.0.5/src/nagini.js');
            return naginiModule.Nagini;
        } catch (error) {
            throw new Error(`Failed to import Nagini from CDN: ${error.message}`);
        }
    }

    /**
     * Get current server base URL (port-independent)
     * @returns {string} Base URL like "http://localhost:8000"
     */
    static getServerBaseUrl() {
        return `${window.location.protocol}//${window.location.host}`;
    }

    /**
     * Build a server-relative URL (port-independent)
     * @param {string} path - Path relative to server root
     * @returns {string} Full URL
     */
    static buildServerUrl(path) {
        const baseUrl = this.getServerBaseUrl();
        const cleanPath = path.startsWith('/') ? path : `/${path}`;
        return `${baseUrl}${cleanPath}`;
    }

    /**
     * Dynamically import from current server (port-independent)
     * @param {string} path - Path to the module on current server
     * @returns {Promise<object>} Imported module
     */
    static async importFromServer(path) {
        const url = this.buildServerUrl(path);
        try {
            return await import(url);
        } catch (error) {
            throw new Error(`Failed to import from server ${url}: ${error.message}`);
        }
    }

    /**
     * Try multiple import sources (CDN first, then server fallback)
     * @param {string} cdnUrl - CDN URL
     * @param {string} serverPath - Server path as fallback
     * @returns {Promise<object>} Imported module
     */
    static async importWithFallback(cdnUrl, serverPath) {
        try {
            // Try CDN first
            return await import(cdnUrl);
        } catch (cdnError) {
            console.warn(`CDN import failed (${cdnUrl}), trying server fallback...`);
            try {
                // Fallback to server
                return await this.importFromServer(serverPath);
            } catch (serverError) {
                throw new Error(`Both CDN and server imports failed. CDN: ${cdnError.message}, Server: ${serverError.message}`);
            }
        }
    }
}

export { ImportHelper }; 