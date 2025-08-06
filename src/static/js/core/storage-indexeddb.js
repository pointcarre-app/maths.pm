import { StorageStrategy } from './storage.js';

const DB_NAME = 'arpege_questions_db';
const DB_VERSION = 1;
const STORE_NAME = 'questions';

/**
 * @implements {StorageStrategy}
 */
class IndexedDBStorage extends StorageStrategy {
    constructor() {
        super();
        this.dbPromise = this._openDb();
    }

    _openDb() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(DB_NAME, DB_VERSION);

            request.onerror = () => reject(new Error("Failed to open IndexedDB."));
            request.onsuccess = () => resolve(request.result);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(STORE_NAME)) {
                    db.createObjectStore(STORE_NAME, { keyPath: 'id' });
                }
            };
        });
    }

    async saveQuestion(question) {
        const db = await this.dbPromise;
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(STORE_NAME, 'readwrite');
            const store = transaction.objectStore(STORE_NAME);
            const request = store.put(question);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(new Error("Failed to save question to IndexedDB."));
        });
    }

    async getQuestionById(id) {
        const db = await this.dbPromise;
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(STORE_NAME, 'readonly');
            const store = transaction.objectStore(STORE_NAME);
            const request = store.get(id);

            request.onsuccess = () => resolve(request.result || null);
            request.onerror = () => reject(new Error("Failed to get question from IndexedDB."));
        });
    }

    async getAllQuestions() {
        const db = await this.dbPromise;
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(STORE_NAME, 'readonly');
            const store = transaction.objectStore(STORE_NAME);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(new Error("Failed to get all questions from IndexedDB."));
        });
    }

    async deleteQuestionById(id) {
        const db = await this.dbPromise;
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(STORE_NAME, 'readwrite');
            const store = transaction.objectStore(STORE_NAME);
            const request = store.delete(id);

            request.onsuccess = () => resolve();
            request.onerror = () => reject(new Error("Failed to delete question from IndexedDB."));
        });
    }
}

export { IndexedDBStorage }; 