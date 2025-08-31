// Table Enhancer Script Module
// This script demonstrates file-based script modules

console.log('🎨 Table Enhancer script loaded from external file');

document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 Table Enhancer: DOM ready, searching for tables...');
    
    // Find all table fragments
    const tableFragments = document.querySelectorAll('[data-f_type="table_"]');
    
    if (tableFragments.length === 0) {
        console.warn('⚠️ No table fragments found for enhancement');
        return;
    }
    
    console.log(`✅ Found ${tableFragments.length} table(s) to enhance`);
    
    tableFragments.forEach((tableFragment, index) => {
        enhanceTable(tableFragment, index);
    });
});

function enhanceTable(tableFragment, index) {
    const table = tableFragment.querySelector('table');
    if (!table) {
        console.error('❌ No table element found in fragment');
        return;
    }
    
    // Add interactive features to the table
    addTableSorting(table);
    addRowHighlighting(table);
    addTableStats(tableFragment, table, index);
    
    console.log(`🎯 Enhanced table #${index + 1}`);
}

function addTableSorting(table) {
    const headers = table.querySelectorAll('th');
    
    headers.forEach((header, columnIndex) => {
        header.style.cursor = 'pointer';
        header.style.userSelect = 'none';
        header.title = 'Click to sort';
        
        // Add sort indicator
        const sortIcon = document.createElement('span');
        sortIcon.innerHTML = ' ↕️';
        sortIcon.style.fontSize = '0.8em';
        header.appendChild(sortIcon);
        
        header.addEventListener('click', () => {
            sortTable(table, columnIndex);
            
            // Update sort indicators
            headers.forEach(h => {
                const icon = h.querySelector('span');
                if (icon) icon.innerHTML = ' ↕️';
            });
            sortIcon.innerHTML = ' ↑';
        });
    });
}

function addRowHighlighting(table) {
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.backgroundColor = '#f0f9ff';
            row.style.transition = 'background-color 0.2s ease';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.backgroundColor = '';
        });
        
        row.addEventListener('click', () => {
            // Toggle selection
            if (row.classList.contains('selected')) {
                row.classList.remove('selected');
                row.style.backgroundColor = '';
            } else {
                // Remove selection from other rows
                rows.forEach(r => {
                    r.classList.remove('selected');
                    r.style.backgroundColor = '';
                });
                
                row.classList.add('selected');
                row.style.backgroundColor = '#dbeafe';
            }
        });
    });
}

function addTableStats(tableFragment, table, tableIndex) {
    const rows = table.querySelectorAll('tbody tr');
    const columns = table.querySelectorAll('th').length;
    
    // Create stats panel
    const statsPanel = document.createElement('div');
    statsPanel.className = 'table-stats mt-3 p-3 bg-gray-50 rounded border';
    statsPanel.innerHTML = `
        <h4 class="text-sm font-medium text-gray-700 mb-2">📊 Table Statistics (Enhanced by External Script)</h4>
        <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
                <span class="font-medium">Rows:</span> ${rows.length}
            </div>
            <div>
                <span class="font-medium">Columns:</span> ${columns}
            </div>
            <div>
                <span class="font-medium">Total Cells:</span> ${rows.length * columns}
            </div>
            <div>
                <span class="font-medium">Table ID:</span> #${tableIndex + 1}
            </div>
        </div>
        <div class="mt-2">
            <button class="btn-small bg-blue-500 text-white px-2 py-1 rounded text-xs" onclick="exportTableData(${tableIndex})">
                📥 Export Data
            </button>
            <button class="btn-small bg-green-500 text-white px-2 py-1 rounded text-xs ml-2" onclick="addSampleRow(${tableIndex})">
                ➕ Add Row
            </button>
        </div>
    `;
    
    // Insert stats panel after the table fragment
    tableFragment.insertAdjacentElement('afterend', statsPanel);
}

function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try numeric comparison first
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // Fallback to string comparison
        return aValue.localeCompare(bValue);
    });
    
    // Remove existing rows and add sorted ones
    rows.forEach(row => tbody.removeChild(row));
    rows.forEach(row => tbody.appendChild(row));
}

// Global functions for button interactions
window.exportTableData = function(tableIndex) {
    const tableFragment = document.querySelectorAll('[data-f_type="table_"]')[tableIndex];
    const table = tableFragment.querySelector('table');
    
    if (!table) return;
    
    // Simple CSV export
    const rows = table.querySelectorAll('tr');
    let csvContent = '';
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowData = Array.from(cells).map(cell => `"${cell.textContent.trim()}"`);
        csvContent += rowData.join(',') + '\n';
    });
    
    // Create download
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `table_${tableIndex + 1}_data.csv`;
    a.click();
    URL.revokeObjectURL(url);
    
    console.log('📥 Table data exported');
};

window.addSampleRow = function(tableIndex) {
    const tableFragment = document.querySelectorAll('[data-f_type="table_"]')[tableIndex];
    const table = tableFragment.querySelector('table');
    const tbody = table.querySelector('tbody');
    
    if (!tbody) return;
    
    const columnCount = table.querySelectorAll('th').length;
    const newRow = document.createElement('tr');
    
    // Add sample data based on column count
    const sampleData = ['Sample', 'Dynamic', 'Added', 'Data'];
    for (let i = 0; i < columnCount; i++) {
        const cell = document.createElement('td');
        cell.textContent = sampleData[i % sampleData.length] + ` ${i + 1}`;
        cell.style.backgroundColor = '#fef3c7';
        newRow.appendChild(cell);
    }
    
    tbody.appendChild(newRow);
    
    // Animate the new row
    setTimeout(() => {
        newRow.style.transition = 'background-color 0.5s ease';
        newRow.style.backgroundColor = '';
    }, 100);
    
    // Re-add event listeners for the new row
    addRowHighlighting(table);
    
    console.log('➕ Sample row added to table');
};

console.log('🚀 Table Enhancer script module ready');
