import { ApiStorage } from './storage-api.js';
import { IndexedDBStorage } from './storage-indexeddb.js';

/**
 * A manager to provide the correct storage strategy based on the persistence mode.
 */
class StorageManager {
    /**
     * Creates and returns a storage instance based on the specified mode.
     * @param {PersistenceMode} mode - The desired persistence mode.
     * @returns {StorageStrategy} An instance of a class that implements StorageStrategy.
     */
    static createStorage(mode) {
        switch (mode) {
            case 'api':
                // The base URL can be configured here or passed in.
                // For this example, we assume the API is on the same origin.
                return new ApiStorage();
            case 'indexeddb':
                return new IndexedDBStorage();
            case 'localstorage':
                // Note: LocalStorage strategy is not implemented in this example.
                // It could be added here following the same pattern.
                throw new Error("LocalStorage mode is not yet implemented.");
            default:
                throw new Error(`Unknown persistence mode: ${mode}`);
        }
    }
}

export { StorageManager }; 