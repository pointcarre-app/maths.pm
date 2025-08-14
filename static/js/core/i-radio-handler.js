/**
 * Interactive Radio Fragment Handler
 * Manages radio button interactions with flag-based validation
 */

class IRadioHandler {
    constructor() {
        this.FLAG_CORRECT = 20;
        this.FLAG_WRONG = 21;
        this.FLAG_COMMENT = -1;
        this.init();
    }

    init() {
        // Initialize all radio fragments on page load
        document.addEventListener('DOMContentLoaded', () => {
            this.attachEventListeners();
        });
    }

    attachEventListeners() {
        // Find all radio fragment wrappers
        const radioWrappers = document.querySelectorAll('[data-f_type="radio_"]');
        
        radioWrappers.forEach((wrapper, index) => {
            const radioInputs = wrapper.querySelectorAll('input[type="radio"]');
            
            radioInputs.forEach(input => {
                input.addEventListener('change', (e) => {
                    this.handleRadioChange(e, wrapper, index);
                });
            });
        });
    }

    handleRadioChange(event, wrapper, fragmentIndex) {
        const selectedInput = event.target;
        const selectedFlag = parseInt(selectedInput.value);
        const radioLabel = selectedInput.closest('label');
        const allLabels = wrapper.querySelectorAll('label.label');
        
        // Reset all labels to default state
        allLabels.forEach(label => {
            const labelInput = label.querySelector('input[type="radio"]');
            if (labelInput && labelInput !== selectedInput) {
                this.resetLabelState(label);
            }
        });
        
        // Apply feedback based on flag value
        this.applyFeedback(radioLabel, selectedFlag);
        
        // Store the answer in local storage
        this.storeAnswer(fragmentIndex, selectedFlag);
        
        // Dispatch custom event for other components to listen to
        this.dispatchAnswerEvent(fragmentIndex, selectedFlag);
    }

    applyFeedback(label, flag) {
        const textSpan = label.querySelector('.label-text');
        
        // Remove existing feedback classes
        textSpan.classList.remove('text-success', 'text-error', 'text-warning');
        
        // Apply new feedback based on flag
        if (flag === this.FLAG_CORRECT) {
            textSpan.classList.add('text-success');
            this.showFeedbackMessage(label, '✅ Correct!', 'success');
        } else if (flag === this.FLAG_WRONG) {
            textSpan.classList.add('text-error');
            this.showFeedbackMessage(label, '❌ Incorrect', 'error');
        }
        
        // Add animation
        label.classList.add('animate-pulse');
        setTimeout(() => {
            label.classList.remove('animate-pulse');
        }, 500);
    }

    resetLabelState(label) {
        const textSpan = label.querySelector('.label-text');
        textSpan.classList.remove('text-success', 'text-error', 'text-warning');
    }

    showFeedbackMessage(label, message, type) {
        // Remove any existing feedback message
        const existingFeedback = label.querySelector('.feedback-message');
        if (existingFeedback) {
            existingFeedback.remove();
        }
        
        // Create feedback element
        const feedback = document.createElement('span');
        feedback.className = `feedback-message ml-2 text-sm badge badge-${type === 'success' ? 'success' : 'error'}`;
        feedback.textContent = message;
        
        // Add feedback to label
        label.appendChild(feedback);
        
        // Auto-hide feedback after 3 seconds
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.classList.add('opacity-0', 'transition-opacity');
                setTimeout(() => feedback.remove(), 300);
            }
        }, 3000);
    }

    storeAnswer(fragmentIndex, flag) {
        const storageKey = `i-radio-answer-${window.location.pathname}-${fragmentIndex}`;
        const answerData = {
            flag: flag,
            timestamp: new Date().toISOString(),
            isCorrect: flag === this.FLAG_CORRECT
        };
        
        localStorage.setItem(storageKey, JSON.stringify(answerData));
    }

    getStoredAnswers() {
        const answers = {};
        const pathPrefix = `i-radio-answer-${window.location.pathname}`;
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(pathPrefix)) {
                const fragmentIndex = key.replace(pathPrefix + '-', '');
                answers[fragmentIndex] = JSON.parse(localStorage.getItem(key));
            }
        }
        
        return answers;
    }

    clearAnswers() {
        const pathPrefix = `i-radio-answer-${window.location.pathname}`;
        const keysToRemove = [];
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(pathPrefix)) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(key => localStorage.removeItem(key));
    }

    dispatchAnswerEvent(fragmentIndex, flag) {
        const event = new CustomEvent('i-radio-answered', {
            detail: {
                fragmentIndex: fragmentIndex,
                flag: flag,
                isCorrect: flag === this.FLAG_CORRECT,
                timestamp: new Date().toISOString()
            }
        });
        
        document.dispatchEvent(event);
    }

    // Calculate score for all answered questions on the page
    calculateScore() {
        const answers = this.getStoredAnswers();
        const totalQuestions = document.querySelectorAll('[data-f_type="radio_"]').length;
        const answeredQuestions = Object.keys(answers).length;
        const correctAnswers = Object.values(answers).filter(a => a.isCorrect).length;
        
        return {
            total: totalQuestions,
            answered: answeredQuestions,
            correct: correctAnswers,
            percentage: totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0
        };
    }

    // Show score summary
    showScoreSummary() {
        const score = this.calculateScore();
        const summaryHTML = `
            <div class="stats shadow">
                <div class="stat">
                    <div class="stat-title">Questions</div>
                    <div class="stat-value">${score.answered}/${score.total}</div>
                    <div class="stat-desc">Answered</div>
                </div>
                <div class="stat">
                    <div class="stat-title">Correct</div>
                    <div class="stat-value text-success">${score.correct}</div>
                    <div class="stat-desc">${score.percentage.toFixed(0)}%</div>
                </div>
            </div>
        `;
        
        // You can append this to a specific container or show in a modal
        console.log('Score:', score);
        return summaryHTML;
    }
}

// Initialize the handler
const iRadioHandler = new IRadioHandler();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IRadioHandler;
}
