/**
 * QuestionFactory Usage Examples
 * Shows all the different ways to use the port-independent QuestionFactory
 */

import { QuestionFactory } from '../core/question-factory.js';
import { ImportHelper } from '../utils/import-helper.js';

// Example usage patterns for QuestionFactory

class ExampleUsage {
    
    /**
     * Method 1: Manual Nagini import (most flexible)
     * Use this when you want full control over the import process
     */
    static async method1_ManualImport(pythonFileUrl, naginiManager) {
        try {
            // Import Nagini manually (port-independent)
            const Nagini = await ImportHelper.importNagini();
            
            // Use QuestionFactory with explicit Nagini parameter
            const question = await QuestionFactory.createFromPyodide(
                pythonFileUrl,
                naginiManager,
                Nagini,  // Pass Nagini class explicitly
                true,    // Include Nagini result
                true     // Include metadata
            );
            
            console.log('✅ Method 1 - Manual import:', question);
            return question;
        } catch (error) {
            console.error('❌ Method 1 failed:', error);
            throw error;
        }
    }

    /**
     * Method 2: Auto import (easiest)
     * Use this for the simplest implementation
     */
    static async method2_AutoImport(pythonFileUrl, naginiManager) {
        try {
            // QuestionFactory handles Nagini import automatically
            const question = await QuestionFactory.createFromPyodideAuto(
                pythonFileUrl,
                naginiManager,
                true,    // Include Nagini result
                true     // Include metadata
            );
            
            console.log('✅ Method 2 - Auto import:', question);
            return question;
        } catch (error) {
            console.error('❌ Method 2 failed:', error);
            throw error;
        }
    }

    /**
     * Method 3: Legacy compatibility
     * Use this for backward compatibility with existing code
     */
    static async method3_Legacy(pythonFileUrl, naginiManager) {
        try {
            // Legacy method - tries global Nagini first, then imports
            const question = await QuestionFactory.createFromPyodideLegacy(
                pythonFileUrl,
                naginiManager,
                false,   // Don't include Nagini result
                false    // Don't include metadata
            );
            
            console.log('✅ Method 3 - Legacy:', question);
            return question;
        } catch (error) {
            console.error('❌ Method 3 failed:', error);
            throw error;
        }
    }

    /**
     * Method 4: Pre-imported Nagini (most efficient for multiple calls)
     * Use this when making many question generation calls
     */
    static async method4_PreImported(pythonFileUrl, naginiManager, preImportedNagini) {
        try {
            // Use pre-imported Nagini class (most efficient for bulk operations)
            const question = await QuestionFactory.createFromPyodide(
                pythonFileUrl,
                naginiManager,
                preImportedNagini,  // Use pre-imported Nagini
                false,              // Don't include Nagini result
                false               // Don't include metadata
            );
            
            console.log('✅ Method 4 - Pre-imported:', question);
            return question;
        } catch (error) {
            console.error('❌ Method 4 failed:', error);
            throw error;
        }
    }

    /**
     * Demo: Generate multiple questions efficiently
     */
    static async generateMultipleQuestions(pythonFileUrls, naginiManager) {
        console.log('🚀 Generating multiple questions efficiently...');
        
        // Import Nagini once for all questions (efficient)
        const Nagini = await ImportHelper.importNagini();
        
        const questions = [];
        for (const url of pythonFileUrls) {
            try {
                const question = await QuestionFactory.createFromPyodide(
                    url,
                    naginiManager,
                    Nagini,  // Reuse the same Nagini import
                    false,   // No raw result needed for bulk
                    false    // No metadata needed for bulk
                );
                questions.push(question);
                console.log(`✅ Generated question from: ${url.split('/').pop()}`);
            } catch (error) {
                console.error(`❌ Failed to generate from ${url}:`, error);
            }
        }
        
        console.log(`🎉 Successfully generated ${questions.length} questions`);
        return questions;
    }

    /**
     * Demo: Port-independent URL building
     */
    static demonstratePortIndependence() {
        console.log('🌐 Port-independent URL examples:');
        
        // These work regardless of which port your server is running on
        console.log('Server base URL:', ImportHelper.getServerBaseUrl());
        console.log('Static file URL:', ImportHelper.buildServerUrl('/static/py/example.py'));
        console.log('API endpoint URL:', ImportHelper.buildServerUrl('/api/health'));
        
        // Current location info
        console.log('Current location:', {
            protocol: window.location.protocol,
            host: window.location.host,
            port: window.location.port || 'default',
            pathname: window.location.pathname
        });
    }
}

export { ExampleUsage }; 