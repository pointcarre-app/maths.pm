/**
 * Navbar Active State Manager
 * 
 * Makes the primary button display in outline mode when the current URL
 * matches the button's href or specific routes like /ressources
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get the primary button in the navbar
    const primaryButton = document.querySelector('.navbar-end .btn-primary');
    
    if (!primaryButton) {
        console.warn('Primary button not found in navbar');
        return;
    }

    // Get the current pathname (without domain)
    const currentPath = window.location.pathname;
    
    // Get the button's href attribute
    const buttonHref = primaryButton.getAttribute('href');
    
    // Define the paths where the button should be in outline mode
    const activeOnPaths = [
        '/',           // Root/home page
        '/ressources'  // Resources page
    ];
    
    // Check if current path matches any of the active paths
    const shouldBeActive = activeOnPaths.some(path => {
        // Exact match for root path
        if (path === '/' && currentPath === '/') {
            return true;
        }
        // For other paths, check if current path starts with the target path
        if (path !== '/' && currentPath.startsWith(path)) {
            return true;
        }
        return false;
    });
    
    // Apply outline styling if the button should be active
    if (shouldBeActive) {
        // Remove btn-primary class and add btn-outline and btn-primary together
        // DaisyUI uses btn-outline combined with color classes for outline buttons
        primaryButton.classList.remove('btn-primary');
        primaryButton.classList.add('btn-outline', 'btn-primary');
        
        // Add a custom active state class for additional styling if needed
        primaryButton.classList.add('navbar-button-active');
        
        console.log('Primary button set to outline mode for path:', currentPath);
    } else {
        // Ensure button is in normal mode (remove outline classes if present)
        primaryButton.classList.remove('btn-outline', 'navbar-button-active');
        if (!primaryButton.classList.contains('btn-primary')) {
            primaryButton.classList.add('btn-primary');
        }
        
        console.log('Primary button in normal mode for path:', currentPath);
    }
});