// Simple global log store
window.atlas = {
    logs: [],
    listeners: [],
    
    add(emoji, level, message) {
        const entry = {
            emoji,
            level,
            message,
            timestamp: new Date(),
            id: Date.now() + Math.random()
        };
        
        this.logs.push(entry);
        this.notify(entry);
    },
    
    clear() {
        this.logs = [];
        this.notify(null, 'clear');
    },
    
    sort(compareFn) {
        this.logs.sort(compareFn);
        this.notify(null, 'sort');
    },
    
    notify(entry, action = 'add') {
        this.listeners.forEach(fn => fn(entry, action));
    },
    
    subscribe(fn) {
        this.listeners.push(fn);
    },
    
    getStats() {
        const stats = {
            total: this.logs.length,
            log: 0,
            warn: 0,
            error: 0
        };
        
        this.logs.forEach(entry => {
            if (entry.level === 'log') stats.log++;
            else if (entry.level === 'warn') stats.warn++;
            else if (entry.level === 'error') stats.error++;
        });
        
        return stats;
    }
};

/**
 * Global Path Resolver for @/src aliases
 * Usage: window.atlas.resolvePath("@/src/pyodide/python/pyodide_init.py")
 */
const PathResolver = {
  /**
   * Resolve path with @/ prefix to absolute URL
   * @param {string} path - Path with @/ prefix
   * @returns {string} - Resolved absolute path
   */
  resolve(path) {
    if (path.startsWith('@/src/')) {
      const naginiSettings = document.querySelector('#nagini-settings');
      const naginiEndpoint = naginiSettings ? naginiSettings.getAttribute('data-endpoint') : 'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@0.0.5';
      return path.replace('@/src/', `${naginiEndpoint}/src/`);
    }
    
    if (path.startsWith('@/static/')) {
      // Handle static files served by FastAPI
      return path.replace('@/static/', '/static/');
    }
    
    if (path.startsWith('@/')) {
      const naginiSettings = document.querySelector('#nagini-settings');
      const naginiEndpoint = naginiSettings ? naginiSettings.getAttribute('data-endpoint') : 'https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@0.0.5';
      return path.replace('@/', `${naginiEndpoint}/`);
    }
    
    return path;
  }
};

// Make PathResolver available globally
window.atlas.resolvePath = PathResolver.resolve;


class AtlasLogDisplay {
    constructor() {
        this.container = null;
        this.isVisible = false;
        this.currentFilter = 'all'; // Track current filter
        this.showDataTable = false; // Track data table visibility
        this.createContainer();
        this.setupSubscription();
        this.setupKeyboardShortcut();
    }

    createContainer() {
        // Create bottom-centered log container
        this.container = document.createElement('div');
        this.container.id = 'atlas-log-display';
        this.container.className = 'max-w-4xl sm:px-8 mx-auto';
        this.container.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 64rem;
            z-index: 9999;
            display: none;
        `;
        
        // Create card wrapper
        const cardWrapper = document.createElement('div');
        cardWrapper.className = 'card bg-base-100 shadow-xl border border-base-200 h-[90vh]';
        
        // Add header
        const header = document.createElement('div');
        header.className = 'card-header px-2 sm:px-4 py-3 border-b border-base-200';
        header.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
        `;
        header.innerHTML = `
            <div class="flex items-center gap-4">
                <!-- <h3 class="text-lg font-semibold font-mono"></h3> -->    
                <div id="atlas-stats" class="flex gap-2 text-xs py-2">
                    <!-- Stats will be populated here -->
                </div>
            </div>
            <div class="flex gap-2">
                <button id="atlas-clear-btn" class="btn btn-error btn-soft btn-xs sm:btn-sm">Clear</button>
                <button id="atlas-close-btn" class="btn btn-ghost btn-xs sm:btn-sm">✕</button>
            </div>
        `;
        
        cardWrapper.appendChild(header);
        
        // Add tabs container
        this.tabsContainer = document.createElement('div');
        this.tabsContainer.id = 'atlas-tabs';
        this.tabsContainer.className = 'px-4 py-2 border-b border-base-200 bg-base-300';
        // this.tabsContainer.style.cssText = `
        //     overflow-x: auto;
        // `;
        
        cardWrapper.appendChild(this.tabsContainer);
        
        // Add log container
        this.logContainer = document.createElement('div');
        this.logContainer.id = 'atlas-logs';
        this.logContainer.className = 'card-body p-4';
        this.logContainer.style.cssText = `
            overflow-y: auto;
            font-family: var(--font-mono);
            font-size: 12px;
        `;
        
        // Add data table container (initially hidden)
        this.dataTableContainer = document.createElement('div');
        this.dataTableContainer.id = 'atlas-data-table';
        this.dataTableContainer.className = 'card-body p-4';
        this.dataTableContainer.style.cssText = `
            overflow-y: auto;
            display: none;
        `;
        
        cardWrapper.appendChild(this.logContainer);
        cardWrapper.appendChild(this.dataTableContainer);
        this.container.appendChild(cardWrapper);
        document.body.appendChild(this.container);
        
        // Create invisible footer toggle button
        this.createFooterToggle();
        
        // Add button functionality
        document.getElementById('atlas-clear-btn').addEventListener('click', () => {
            window.atlas.clear();
        });
        
        document.getElementById('atlas-close-btn').addEventListener('click', () => {
            this.hide();
        });
        
        // Initialize tabs and stats
        this.updateTabs();
        this.updateStats();
    }

    createFooterToggle() {
        // Wait for DOM to be ready and find footer
        const initFooterButton = () => {
            const footer = document.querySelector('footer');
            if (!footer) {
                // Retry if footer not found yet
                setTimeout(initFooterButton, 100);
                return;
            }
            
            // Create visible atlas toggle button
            this.footerToggle = document.createElement('button');
            this.footerToggle.id = 'atlas-footer-toggle';
            this.footerToggle.className = 'btn btn-outline btn-sm opacity-50 hover:opacity-75';
            this.footerToggle.textContent = 'atlas';
            this.footerToggle.style.cssText = `
                position: absolute;
                bottom: 20px;
                right: 0;
                left: 0;
                margin: 0 auto;
                z-index: 10;
                transition: opacity 0.2s ease;
                width:100px;
            `;
            
            // Toggle atlas on click
            this.footerToggle.addEventListener('click', () => {
                this.toggle();
            });
            
            // Append to footer instead of body
            footer.appendChild(this.footerToggle);
        };
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initFooterButton);
        } else {
            initFooterButton();
        }
    }

    setupSubscription() {
        window.atlas.subscribe((entry, action) => {
            if (action === 'clear') {
                this.logContainer.innerHTML = '';
                this.currentFilter = 'all';
                this.updateTabs();
                this.updateStats();
            } else if (action === 'add' && entry) {
                this.updateTabs(); // Update tabs in case of new emoji
                this.updateStats(); // Update stats
                this.addLogEntry(entry);
            }
        });
    }

    setupKeyboardShortcut() {
        let keys = [];
        document.addEventListener('keydown', (e) => {
            keys.push(e.key.toLowerCase());
            if (keys.length > 5) keys.shift();
            
            if (keys.join('') === 'atlas') {
                this.toggle();
                keys = [];
            }
        });
    }

    getUniqueEmojis() {
        const emojis = new Set();
        window.atlas.logs.forEach(log => {
            if (log.emoji) {
                emojis.add(log.emoji);
            }
        });
        return Array.from(emojis).sort();
    }

    updateTabs() {
        const uniqueEmojis = this.getUniqueEmojis();
        
        // Create tabs HTML with data table toggle button on the right
        let tabsHTML = `
            <div class="flex justify-between items-center">
                <div class="flex gap-1 items-center">
                    <button class="atlas-filter-tab btn btn-xs ${this.currentFilter === 'all' ? 'btn-primary' : 'btn-ghost'}" data-filter="all">
                        All
                    </button>
        `;
        
        uniqueEmojis.forEach(emoji => {
            const isActive = this.currentFilter === emoji;
            tabsHTML += `
                    <button class="atlas-filter-tab btn btn-xs ${isActive ? 'btn-primary' : 'btn-ghost'}" data-filter="${emoji}">
                        ${emoji}
                    </button>
            `;
        });
        
        tabsHTML += `
                </div>
                <button id="atlas-data-toggle" class="btn btn-xs ${this.showDataTable ? 'btn-primary' : 'btn-ghost'}">
                    📊 Data
                </button>
            </div>
        `;
        
        this.tabsContainer.innerHTML = tabsHTML;
        
        // Add click handlers to tabs
        this.tabsContainer.querySelectorAll('.atlas-filter-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const filter = e.target.dataset.filter;
                this.setFilter(filter);
            });
        });
        
        // Add click handler for data table toggle
        document.getElementById('atlas-data-toggle').addEventListener('click', () => {
            this.toggleDataTable();
        });
    }

    setFilter(filter) {
        this.currentFilter = filter;
        this.updateTabs(); // Update active tab styling
        this.refreshLogDisplay();
    }

    refreshLogDisplay() {
        // Clear and re-render logs based on current filter
        this.logContainer.innerHTML = '';
        const logsToShow = this.currentFilter === 'all' 
            ? window.atlas.logs.slice(-50)
            : window.atlas.logs.filter(log => log.emoji === this.currentFilter).slice(-50);
        
        logsToShow.forEach(log => this.addLogEntryToDOM(log));
    }

    addLogEntry(entry) {
        // Only add to DOM if it matches current filter
        if (this.currentFilter === 'all' || entry.emoji === this.currentFilter) {
            this.addLogEntryToDOM(entry);
        }
    }

    addLogEntryToDOM(entry) {
        const logElement = document.createElement('div');
        logElement.className = 'mb-2 p-2 rounded bg-base-200 hover:bg-base-300 transition-colors';
        
        const levelBadgeClass = {
            'log': 'badge-outline badge-success',
            'warn': 'badge-outline badge-warning', 
            'error': 'badge-outline badge-error'
        }[entry.level] || 'badge-outline badge-info';
        
        // Format timestamp more compactly: HH:MM:SS.mmm
        const time = entry.timestamp.toTimeString().split(' ')[0];
        const ms = entry.timestamp.getMilliseconds().toString().padStart(3, '0');
        const compactTime = `${time}.${ms}`;
        
        logElement.innerHTML = `
            <div class="flex items-start gap-2 leading-tight">
                <span class="text-sm flex-shrink-0">${entry.emoji}</span>
                <div class="flex-grow min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-xs text-base-content/60 font-mono">${compactTime}</span>
                        <span class="badge ${levelBadgeClass} badge-xs">${entry.level}</span>
                    </div>
                    <div class="text-xs text-base-content break-words leading-relaxed">${entry.message}</div>
                </div>
            </div>
        `;
        
        this.logContainer.appendChild(logElement);
        
        // Auto-scroll to bottom
        this.logContainer.scrollTop = this.logContainer.scrollHeight;
        
        // Limit to last 50 entries for performance
        if (this.logContainer.children.length > 50) {
            this.logContainer.removeChild(this.logContainer.firstChild);
        }
    }

    toggle() {
        this.isVisible = !this.isVisible;
        this.container.style.display = this.isVisible ? 'block' : 'none';
        
        if (this.isVisible) {
            // Update tabs, stats and show logs
            this.updateTabs();
            this.updateStats();
            this.refreshLogDisplay();
        }
    }

    show() {
        if (!this.isVisible) this.toggle();
    }

    hide() {
        if (this.isVisible) this.toggle();
    }

    updateStats() {
        const stats = window.atlas.getStats();
        const statsContainer = document.getElementById('atlas-stats');
        
        if (statsContainer) {
            statsContainer.innerHTML = `
                <span class="badge badge-outline badge-xs sm:badge-sm">
                    Tot: ${stats.total}
                </span>
                <span class="badge badge-outline badge-success badge-xs sm:badge-sm">
                    Logs: ${stats.log}
                </span>
                <span class="badge badge-outline badge-warning badge-xs sm:badge-sm">
                    Warns: ${stats.warn}
                </span>
                <span class="badge badge-outline badge-error badge-xs sm:badge-sm">
                    Errs: ${stats.error}
                </span>
            `;
        }
    }

    toggleDataTable() {
        this.showDataTable = !this.showDataTable;
        
        if (this.showDataTable) {
            this.logContainer.style.display = 'none';
            this.dataTableContainer.style.display = 'block';
            this.renderDataTable();
        } else {
            this.logContainer.style.display = 'block';
            this.dataTableContainer.style.display = 'none';
        }
        
        // Update button state
        this.updateTabs();
    }

    collectDataBrickInfo() {
        const dataBrickContainers = document.querySelectorAll('data-brick');
        const elements = [];
        
        dataBrickContainers.forEach(container => {
            // Get all elements inside this data-brick (specifically divs)
            const divs = container.querySelectorAll('div');
            
            divs.forEach(div => {
                const elementData = {
                    element: div,
                    data: {}
                };
                
                // Get all data attributes
                for (let i = 0; i < div.attributes.length; i++) {
                    const attr = div.attributes[i];
                    if (attr.name.startsWith('data-')) {
                        const key = attr.name.replace('data-', '');
                        let value = attr.value;
                        
                        // Try to detect and parse JSON
                        if (value.startsWith('{') || value.startsWith('[')) {
                            try {
                                const parsed = JSON.parse(value.replace(/&quot;/g, '"'));
                                value = JSON.stringify(parsed, null, 2);
                            } catch (e) {
                                // Keep original value if parsing fails
                            }
                        }
                        
                        elementData.data[key] = value;
                    }
                }
                
                // Add element context
                if (div.id) {
                    elementData.id = div.id;
                }
                elementData.tag = div.tagName.toLowerCase();
                
                if (Object.keys(elementData.data).length > 0) {
                    elements.push(elementData);
                }
            });
        });
        
        return elements;
    }

    renderDataTable() {
        const elements = this.collectDataBrickInfo();
        
        if (elements.length === 0) {
            this.dataTableContainer.innerHTML = `
                <div class="text-center text-base-content/60 py-8">
                    <p class="text-lg mb-2">📊 No Data Found</p>
                    <p class="text-sm">No divs with data attributes found in <code>&lt;data-brick&gt;</code> containers.</p>
                </div>
            `;
            return;
        }
        
        let tablesHTML = '';
        
        elements.forEach((elementInfo, index) => {
            const { data, id, tag } = elementInfo;
            
            // Create header for each element
            const elementTitle = id ? `${tag}#${id}` : `${tag}`;
            
            tablesHTML += `
                <div class="mb-6">
                    <h4 class="text-sm font-bold mb-2 text-primary">${index + 1}. ${elementTitle}</h4>
                    <div class="overflow-x-auto">
                        <table class="table table-zebra table-xs">
                            <!-- 
                            <thead>
                                <tr>
                                    <th class="font-bold text-xs w-1/3">Key</th>
                                    <th class="font-bold text-xs">Value</th>
                                </tr>
                            </thead> 
                            -->
                            <tbody>
            `;
            
            // Add each data attribute as a row
            Object.entries(data).forEach(([key, value]) => {
                // Check if value looks like formatted JSON (multiple lines)
                const isFormattedJSON = typeof value === 'string' && value.includes('\n');
                
                if (isFormattedJSON) {
                    const jsonId = `json-${index}-${key}`;
                    tablesHTML += `
                        <tr>
                            <td class="font-mono text-xs font-bold align-top">${key}</td>
                            <td class="font-mono text-xs">
                                <button class="btn btn-xs btn-outline mb-2" onclick="toggleJson('${jsonId}')">
                                    📄 Show JSON
                                </button>
                                <pre id="${jsonId}" class="text-xs overflow-x-auto bg-base-200 p-2 rounded" style="display: none;">${value}</pre>
                            </td>
                        </tr>
                    `;
                } else {
                    tablesHTML += `
                        <tr>
                            <td class="font-mono text-xs font-bold">${key}</td>
                            <td class="font-mono text-xs break-words">${value}</td>
                        </tr>
                    `;
                }
            });
            
            tablesHTML += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        });
        
        tablesHTML += `
            <div class="mt-4 text-xs text-base-content/60 text-center">
                Found ${elements.length} div(s) with data attributes
            </div>
        `;
        
        this.dataTableContainer.innerHTML = tablesHTML;
    }
}

// Global function to toggle JSON visibility
window.toggleJson = function(jsonId) {
    const jsonElement = document.getElementById(jsonId);
    const button = document.querySelector(`button[onclick="toggleJson('${jsonId}')"]`);
    
    if (jsonElement && button) {
        const isVisible = jsonElement.style.display !== 'none';
        
        if (isVisible) {
            jsonElement.style.display = 'none';
            button.innerHTML = '📄 Show JSON';
            button.classList.remove('btn-primary');
            button.classList.add('btn-outline');
        } else {
            jsonElement.style.display = 'block';
            button.innerHTML = '📄 Hide JSON';
            button.classList.remove('btn-outline');
            button.classList.add('btn-primary');
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    window.atlasDisplay = new AtlasLogDisplay();
});

// To get notified when new logs arrive or whatever else
// window.atlas.subscribe((entry, action) => {
//     if (action === 'add' && entry) {
//         console.log('New log! Total logs:', window.atlas.logs.length);
//         console.log('Latest log:', entry);
//     }
// });
