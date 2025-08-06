
/**
 * Simple logger for Store class
 */
class StoreLogger {
    constructor() {
        this.prefix = '🏪';
    }

    log(...args) {
        console.log(this.prefix, ...args);
        window.atlas.add(this.prefix, 'log', args.join(' '));
    }

    warn(...args) {
        console.warn(this.prefix, ...args);
        window.atlas.add(this.prefix, 'warn', args.join(' '));
    }

    error(...args) {
        console.error(this.prefix, ...args);
        window.atlas.add(this.prefix, 'error', args.join(' '));
    }
}

/**
 * @typedef {Object} StoreOptions
 * @property {boolean} enableCache - Whether to enable caching
 * @property {number} timeout - Request timeout in milliseconds
 */

/**
 * Store class for managing data loading and caching across the application.
 * Handles fetching JSON and text data from multiple URLs with built-in caching.
 * 
 * @class Store
 */
class Store {
    /**
     * Creates a new Store instance with the specified shopping list of URLs.
     * 
     * @param {string[]} shopping_list - Array of URLs to fetch data from
     * @throws {TypeError} If shopping_list is not an array
     */
    constructor(shopping_list = []) {

        if (!Array.isArray(shopping_list)) {
            throw new TypeError('shopping_list must be an array of URLs');
        }

        /**
         * Logger instance for this store
         * @type {StoreLogger}
         * @private
         */
        this.logger = new StoreLogger();
        this.logger.log('Creating Store instance');

        /**
         * List of URLs to fetch data from
         * @type {string[]}
         * @private
         */
        this.shopping_list = shopping_list;

        /**
         * Cache storage for loaded data, keyed by URL
         * @type {Map<string, any>}
         * @private
         */
        this.cache = new Map();
    }

    /**
     * Loads data from all URLs in the shopping list concurrently.
     * 
     * @async
     * @returns {Promise<any[]>} Array of loaded data in the same order as shopping_list
     * @throws {Error} If any URL fails to load (fails fast)
     */
    async letsGoForShopping() {
        this.logger.log('letsGoForShopping');
        
        if (this.shopping_list.length === 0) {
            this.logger.warn('Shopping list is empty');
            return [];
        }

        const promises = this.shopping_list.map(url => this.loadFromUrl(url));
        
        try {
            const results = await Promise.all(promises);
            this.logger.log(`Shopping complete - loaded ${results.length} items`);
            return results;
        } catch (error) {
            this.logger.error('Shopping failed:', error);
            throw error;
        }
    }

    /**
     * Loads data from a single URL with automatic format detection.
     * Results are cached automatically with long TTL.
     * 
     * @async
     * @param {string} url - The URL to fetch data from
     * @returns {Promise<any>} Parsed JSON object or raw text string
     * @throws {Error} If URL is invalid, network request fails, or parsing fails
     */
    async loadFromUrl(url) {
        if (typeof url !== 'string' || url.trim() === '') {
            throw new Error('URL must be a non-empty string');
        }

        this.logger.log(`${url}`);
        
        try {
            const startTime = performance.now();
            const response = await fetch(url, {
                cache: 'force-cache' // Use aggressive browser caching
            });
            const endTime = performance.now();
            const fetchTime = endTime - startTime;
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status} for URL: ${url}`);
            }
            
            // Simple cache hit detection
            if (fetchTime < 10) {
                // this.logger.log(`Cache hit (${fetchTime.toFixed(1)}ms): ${url}`);
            } else {
                // this.logger.log(`Downloaded (${fetchTime.toFixed(1)}ms): ${url}`);
            }
            
            let data;
            if (url.endsWith('.json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            this.cache.set(url, data);
            // this.logger.log(`Data cached: ${url}`);
                                    
            return data;
        } catch (error) {
            this.logger.error(`Error loading data from ${url}:`, error);
            throw error;
        }
    }

    /**
     * Loads data from all URLs and returns as an object with URLs as keys.
     * 
     * @async
     * @returns {Promise<Object<string, any>>} Object mapping URLs to their loaded data or null if failed
     */
    async loadAllDataAsObject() {
        this.logger.log('Loading all data as object');
        
        const results = {};
        
        for (const url of this.shopping_list) {
            try {
                results[url] = await this.loadFromUrl(url);
            } catch (error) {
                this.logger.error(`Failed to load ${url}:`, error);
                results[url] = null;
            }
        }
        
        return results;
    }

    /**
     * Retrieves cached data for a specific URL without making a network request.
     * 
     * @param {string} url - The URL to get cached data for
     * @returns {any|undefined} The cached data, or undefined if not found
     */
    getCachedData(url) {
        if (typeof url !== 'string') {
            this.logger.warn('getCachedData called with non-string URL:', url);
            return undefined;
        }
        return this.cache.get(url);
    }

    /**
     * Returns all cached data as a plain object.
     * 
     * @returns {Object<string, any>} Object containing all cached data keyed by URL
     */
    getAllCachedData() {
        return Object.fromEntries(this.cache);
    }

    /**
     * Gets the current shopping list.
     * 
     * @returns {string[]} Copy of the current shopping list
     */
    getShoppingList() {
        return [...this.shopping_list];
    }

    /**
     * Checks if a URL is in the current shopping list.
     * 
     * @param {string} url - The URL to check
     * @returns {boolean} True if URL is in shopping list
     */
    hasUrl(url) {
        return this.shopping_list.includes(url);
    }

    /**
     * Gets the cache size (number of cached items).
     * 
     * @returns {number} Number of items in cache
     */
    getCacheSize() {
        return this.cache.size;
    }

    /**
     * Checks if data for a specific URL is cached.
     * 
     * @param {string} url - The URL to check
     * @returns {boolean} True if data is cached for this URL
     */
    isCached(url) {
        return this.cache.has(url);
    }

    /**
     * Clears all cached data from the store.
     * 
     * @returns {number} Number of items that were cleared from cache
     */
    clearAllCachedData() {
        const itemsCleared = this.cache.size;
        this.cache.clear();
        this.logger.log(`Cleared ${itemsCleared} items from cache`);
        return itemsCleared;
    }
}

// Make Store globally available for use in other scripts
window.Store = Store;