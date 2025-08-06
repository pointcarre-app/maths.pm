/**
 * @typedef {'api' | 'indexeddb' | 'localstorage'} PersistenceMode
 */

/**
 * @typedef {Object} Question
 * @property {string} id - The unique identifier for the question.
 * @property {string} statement - The question statement.
 * @property {string} answer - The correct answer.
 * @property {string} [answer_simplified] - A simplified version of the answer.
 * @property {any} [other_data] - Any other relevant data.
 */

/**
 * @interface
 */
class StorageStrategy {
    /**
     * Saves a question.
     * @param {Question} question - The question object to save.
     * @returns {Promise<void>}
     */
    async saveQuestion(question) {
        throw new Error("Not implemented");
    }

    /**
     * Retrieves a question by its ID.
     * @param {string} id - The ID of the question to retrieve.
     * @returns {Promise<Question|null>}
     */
    async getQuestionById(id) {
        throw new Error("Not implemented");
    }

    /**
     * Retrieves all questions.
     * @returns {Promise<Question[]>}
     */
    async getAllQuestions() {
        throw new Error("Not implemented");
    }

    /**
     * Deletes a question by its ID.
     * @param {string} id - The ID of the question to delete.
     * @returns {Promise<void>}
     */
    async deleteQuestionById(id) {
        throw new Error("Not implemented");
    }
}

export { StorageStrategy }; 