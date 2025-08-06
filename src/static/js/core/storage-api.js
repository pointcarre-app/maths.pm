import { StorageStrategy } from './storage.js';

/**
 * @implements {StorageStrategy}
 */
class ApiStorage extends StorageStrategy {
    constructor(baseUrl = '') {
        super();
        this.baseUrl = baseUrl;
    }

    /**
     * Saves a question via the API.
     * @param {Question} question - The question object to save.
     * @returns {Promise<Question>}
     */
    async saveQuestion(question) {
        const response = await fetch(`${this.baseUrl}/persistence/questions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(question),
        });

        if (!response.ok) {
            throw new Error(`Failed to save question: ${response.statusText}`);
        }
        return response.json();
    }

    /**
     * Retrieves a question by its ID from the API.
     * @param {string} id - The ID of the question to retrieve.
     * @returns {Promise<Question|null>}
     */
    async getQuestionById(id) {
        const response = await fetch(`${this.baseUrl}/persistence/questions/${id}`);
        if (!response.ok) {
            if (response.status === 404) {
                return null;
            }
            throw new Error(`Failed to get question: ${response.statusText}`);
        }
        return response.json();
    }

    /**
     * Retrieves all questions from the API.
     * @returns {Promise<Question[]>}
     */
    async getAllQuestions() {
        const response = await fetch(`${this.baseUrl}/persistence/questions`);
        if (!response.ok) {
            throw new Error(`Failed to get all questions: ${response.statusText}`);
        }
        return response.json();
    }

    /**
     * Deletes a question by its ID via the API.
     * @param {string} id - The ID of the question to delete.
     * @returns {Promise<void>}
     */
    async deleteQuestionById(id) {
        const response = await fetch(`${this.baseUrl}/persistence/questions/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`Failed to delete question: ${response.statusText}`);
        }
    }
}

export { ApiStorage }; 