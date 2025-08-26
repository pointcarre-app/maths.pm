/**
 * Settings Module for Sujets0
 * Handles loading and managing backend settings
 */

/**
 * Load backend settings from data attributes
 * @returns {Object|null} Backend settings object or null if not found
 */
export function loadBackendSettings() {
    const settingsElement = document.getElementById('products-settings');
    if (!settingsElement) {
        console.warn('Products settings element not found');
        return null;
    }
    
    // Try to get data-sujets0 attribute
    const sujets0Data = settingsElement.getAttribute('data-sujets0');
    if (!sujets0Data) {
        console.warn('data-sujets0 attribute not found');
        return null;
    }
    
    try {
        // Parse the JSON data (handles HTML entities automatically)
        const settings = JSON.parse(sujets0Data);
        console.log('✅ Backend settings loaded successfully:', settings);
        
        // Log individual components for clarity
        if (settings.nagini) {
            console.log('📦 Nagini Configuration:', {
                endpoint: settings.nagini.endpoint,
                js_url: settings.nagini.js_url,
                pyodide_worker_url: settings.nagini.pyodide_worker_url
            });
        }
        
        return settings;
    } catch (error) {
        console.error('Failed to parse backend settings:', error);
        return null;
    }
}

/**
 * Get all product settings from data attributes
 * @returns {Object} Object containing all parsed data attributes
 */
export function getAllProductSettings() {
    const settingsElement = document.getElementById('products-settings');
    if (!settingsElement) {
        console.warn('Products settings element not found');
        return {};
    }
    
    const settings = {};
    
    // Get all data attributes
    const dataAttributes = settingsElement.dataset;
    
    // Parse each data attribute
    for (const [key, value] of Object.entries(dataAttributes)) {
        try {
            settings[key] = JSON.parse(value);
            console.log(`✅ Parsed data-${key}:`, settings[key]);
        } catch (error) {
            console.warn(`Failed to parse data-${key}:`, error);
            settings[key] = value; // Store as string if parsing fails
        }
    }
    
    return settings;
}

/**
 * Process generator levels from backend settings
 * @param {Object} backendSettings - The backend settings object
 * @returns {Object|null} Processed generator levels or null if not available
 */
export function processGeneratorLevels(backendSettings) {
    if (!backendSettings?.generator_levels) {
        console.warn('⚠️ Generator levels not available from backend settings');
        console.log('Available backend settings:', backendSettings);
        return null;
    }

    const generatorLevels = backendSettings.generator_levels;
    window.GENERATOR_LEVELS = generatorLevels; // Make globally available
    
    console.group('📊 Generator Levels from Backend');
    console.log('Generator levels loaded:', generatorLevels);
    
    // Count by level
    const levelCounts = {};
    for (const [generator, info] of Object.entries(generatorLevels)) {
        const level = info.level || 'N/A';
        levelCounts[level] = (levelCounts[level] || 0) + 1;
    }
    console.log('Levels distribution:', levelCounts);
    
    // List 1ERE level generators (with notes where available)
    const firstYearGenerators = Object.entries(generatorLevels)
        .filter(([name, info]) => info.level === '1ERE')
        .map(([name, info]) => ({
            name, 
            note: info.note || 'Pas de note spécifique'
        }));
    console.log('1ère année generators:', firstYearGenerators);
    
    // List 2DE level generators with notes
    const secondYearWithNotes = Object.entries(generatorLevels)
        .filter(([name, info]) => info.level === '2DE' && info.note)
        .map(([name, info]) => ({name, note: info.note}));
    if (secondYearWithNotes.length > 0) {
        console.log('2nde generators with notes:', secondYearWithNotes);
    }
    
    console.groupEnd();
    
    return generatorLevels;
}
