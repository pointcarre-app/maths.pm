/**
 * Service Worker Fix Utility
 * Helps resolve JupyterLite service worker caching issues
 */

class ServiceWorkerFix {
    /**
     * Unregister all service workers for current origin
     */
    static async unregisterAllServiceWorkers() {
        if ('serviceWorker' in navigator) {
            try {
                const registrations = await navigator.serviceWorker.getRegistrations();
                console.log(`🔧 Found ${registrations.length} service worker registrations`);
                
                for (const registration of registrations) {
                    console.log(`🗑️ Unregistering service worker: ${registration.scope}`);
                    await registration.unregister();
                }
                
                console.log('✅ All service workers unregistered');
                return true;
            } catch (error) {
                console.error('❌ Failed to unregister service workers:', error);
                return false;
            }
        } else {
            console.log('ℹ️ Service workers not supported in this browser');
            return true;
        }
    }

    /**
     * Clear all caches
     */
    static async clearAllCaches() {
        if ('caches' in window) {
            try {
                const cacheNames = await caches.keys();
                console.log(`🧹 Found ${cacheNames.length} caches to clear`);
                
                for (const cacheName of cacheNames) {
                    console.log(`🗑️ Deleting cache: ${cacheName}`);
                    await caches.delete(cacheName);
                }
                
                console.log('✅ All caches cleared');
                return true;
            } catch (error) {
                console.error('❌ Failed to clear caches:', error);
                return false;
            }
        } else {
            console.log('ℹ️ Cache API not supported in this browser');
            return true;
        }
    }

    /**
     * Complete cleanup: unregister service workers and clear caches
     */
    static async completeCleanup() {
        console.log('🚀 Starting complete service worker cleanup...');
        
        const swResult = await this.unregisterAllServiceWorkers();
        const cacheResult = await this.clearAllCaches();
        
        if (swResult && cacheResult) {
            console.log('🎉 Complete cleanup successful! Refresh the page.');
            return true;
        } else {
            console.log('⚠️ Cleanup partially successful. Try manual browser cache clear.');
            return false;
        }
    }

    /**
     * Check for service worker conflicts
     */
    static async checkServiceWorkerStatus() {
        if ('serviceWorker' in navigator) {
            try {
                const registrations = await navigator.serviceWorker.getRegistrations();
                
                console.log('📊 Service Worker Status Report:');
                console.log(`   Active registrations: ${registrations.length}`);
                
                registrations.forEach((registration, index) => {
                    console.log(`   Registration ${index + 1}:`);
                    console.log(`     Scope: ${registration.scope}`);
                    console.log(`     State: ${registration.active?.state || 'inactive'}`);
                    console.log(`     Script URL: ${registration.active?.scriptURL || 'unknown'}`);
                });
                
                return registrations;
            } catch (error) {
                console.error('❌ Failed to check service worker status:', error);
                return [];
            }
        }
        return [];
    }

    /**
     * Auto-fix common JupyterLite service worker issues
     */
    static async autoFixJupyterLite() {
        console.log('🔧 Auto-fixing JupyterLite service worker issues...');
        
        // Check current status
        const registrations = await this.checkServiceWorkerStatus();
        
        // Look for problematic JupyterLite service workers
        const problematicSW = registrations.filter(reg => 
            reg.scope.includes('jupyterlite') && 
            (reg.active?.scriptURL.includes('5001') || 
             reg.scope.includes('5001'))
        );
        
        if (problematicSW.length > 0) {
            console.log(`⚠️ Found ${problematicSW.length} problematic JupyterLite service workers`);
            await this.completeCleanup();
            
            // Suggest page reload
            if (confirm('Service workers cleaned up! Reload the page now?')) {
                window.location.reload();
            }
        } else {
            console.log('✅ No problematic JupyterLite service workers found');
        }
    }
}

// Auto-run fix on import (optional)
// ServiceWorkerFix.autoFixJupyterLite();

export { ServiceWorkerFix }; 