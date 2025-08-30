/**
 * Safari CSS Loader
 * Detects Safari browser and loads local CSS files to avoid CORS issues
 */

(function() {
    // Detect Safari browser
    const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
    
    if (!isSafari) {
        // Not Safari, use default CDN links
        return;
    }
    
    console.log('🦁 Safari detected, loading local CSS files for CORS compatibility');
    
    // Map of CDN URLs to local URLs
    const cssMapping = {
        // Google Fonts
        'fonts.googleapis.com/css2?family=Comfortaa': '/static/css/safari-local/fonts-comfortaa.css',
        'fonts.googleapis.com/css2?family=Lexend': '/static/css/safari-local/fonts-lexend.css',
        
        // DaisyUI
        'cdn.jsdelivr.net/npm/daisyui@5/dist/full.css': '/static/css/safari-local/daisyui.css',
        'cdn.jsdelivr.net/npm/daisyui@5/themes.css': '/static/css/safari-local/daisyui-themes.css',
        'cdn.jsdelivr.net/npm/daisyui@5': '/static/css/safari-local/daisyui.css',
        
        // KaTeX
        'cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css': '/static/css/safari-local/katex.min.css',
        
        // Papyrus
        'cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/styles/index.css': '/static/css/safari-local/papyrus-index.css',
        'cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/styles/print.css': '/static/css/safari-local/papyrus-print.css',
    };
    
    // Replace existing link tags
    document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
        const href = link.href;
        
        // Check if this CSS needs to be replaced
        for (const [cdnPattern, localPath] of Object.entries(cssMapping)) {
            if (href.includes(cdnPattern)) {
                // Create new link element with local path
                const newLink = document.createElement('link');
                newLink.rel = 'stylesheet';
                newLink.href = localPath;
                newLink.media = link.media || 'all';
                
                // Replace the old link
                link.parentNode.replaceChild(newLink, link);
                console.log(`✅ Replaced ${cdnPattern} with ${localPath}`);
                break;
            }
        }
    });
    
    // Add Safari-specific table print fix CSS
    const tablePrintFix = document.createElement('link');
    tablePrintFix.rel = 'stylesheet';
    tablePrintFix.href = '/static/css/safari-local/safari-table-print-fix.css';
    tablePrintFix.media = 'all';
    document.head.appendChild(tablePrintFix);
    console.log('✅ Added Safari table print fix CSS');
    
    // Also handle dynamically added stylesheets
    const originalAppendChild = document.head.appendChild;
    document.head.appendChild = function(element) {
        if (element.tagName === 'LINK' && element.rel === 'stylesheet') {
            const href = element.href;
            
            // Check if this CSS needs to be replaced
            for (const [cdnPattern, localPath] of Object.entries(cssMapping)) {
                if (href && href.includes(cdnPattern)) {
                    element.href = localPath;
                    console.log(`✅ Intercepted and replaced ${cdnPattern} with ${localPath}`);
                    break;
                }
            }
        }
        
        return originalAppendChild.call(this, element);
    };
})();

// Export for use in modules
export function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

export function getSafariCSSPath(cdnUrl) {
    const cssMapping = {
        'fonts.googleapis.com/css2?family=Comfortaa': '/static/css/safari-local/fonts-comfortaa.css',
        'fonts.googleapis.com/css2?family=Lexend': '/static/css/safari-local/fonts-lexend.css',
        'cdn.jsdelivr.net/npm/daisyui@5/dist/full.css': '/static/css/safari-local/daisyui.css',
        'cdn.jsdelivr.net/npm/daisyui@5/themes.css': '/static/css/safari-local/daisyui-themes.css',
        'cdn.jsdelivr.net/npm/daisyui@5': '/static/css/safari-local/daisyui.css',
        'cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css': '/static/css/safari-local/katex.min.css',
        'cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/styles/index.css': '/static/css/safari-local/papyrus-index.css',
        'cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.11/src/styles/print.css': '/static/css/safari-local/papyrus-print.css',
    };
    
    for (const [cdnPattern, localPath] of Object.entries(cssMapping)) {
        if (cdnUrl.includes(cdnPattern)) {
            return localPath;
        }
    }
    
    return cdnUrl; // Return original if no mapping found
}
