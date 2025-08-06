

/**
 * Simple logger for Mason class
 */
class MasonLogger {
    constructor() {
        this.prefix = '👷🏻‍♂️';
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

// Mason orchestrator class
class Mason {
    constructor() {
        /**
         * Logger instance for this mason
         * @type {MasonLogger}
         * @private
         */
        this.logger = new MasonLogger();
        this.components = new Map(); // Store component references
        this.logger.log('Creating Mason instance');
    }

    // Main initialization method - now accepts data directly
    async init(brickTagName, data = null) {
        this.logger.log('Initializing', brickTagName, 'with data:', data);
        
        // Find the component in the DOM
        const component = document.querySelector(brickTagName);
        
        if (!component) {
            this.logger.error(`Component ${brickTagName} not found`);
            return;
        }

        try {
            // If data is provided, use it directly. Otherwise, load it.
            const componentData = data || await this.loadData();
            
            if (!componentData) {
                throw new Error('No data available for component');
            }
            
            // THIS IS THE KEY PART: Set data property
            // Lit will automatically re-render because 'data' is a reactive property
            component.data = componentData;
            
            // Store reference for later use
            this.components.set(brickTagName, component);
            
            this.logger.log('Successfully initialized', brickTagName);
            
        } catch (error) {
            this.logger.error('Error initializing component:', error);
            // Set error state in the component
            component.data = { error: error.message };
        }
    }

    // Fallback data loading method (for backward compatibility)
    async loadData() {
        this.logger.log('loadData (fallback)');
        
        // Fetch your JSON data
        const response = await fetch('/static/curriculums/puissance_troiz.json');
        const data = await response.json();
        
        this.logger.log('Data loaded', data);
        return data;
    }

    // Helper method to get component reference
    getComponent(selector) {
        return this.components.get(selector);
    }

    // Method to update component data later
    updateComponentData(brickTagName, newData) {
        const component = this.components.get(brickTagName);
        if (component) {
            // Setting this property will trigger automatic re-render
            component.data = newData;
            this.logger.log(`Updated data for ${brickTagName}`);
        }
    }
}

// Export Mason class
// window.Mason = Mason;

// Create a global instance for easy access
window.masonInstance = new Mason();