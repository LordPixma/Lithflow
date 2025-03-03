// app/static/js/main.js

/**
 * LithFlow JavaScript Utilities
 * Main JavaScript file for LithFlow application
 */

// Initialize when DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for navigation
    initNavigation();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize data tables
    initDataTables();
    
    // Add event listeners for general interactions
    addEventListeners();
    
    // Setup API response handlers
    setupApiHandlers();
});

/**
 * Initialize responsive navigation
 */
function initNavigation() {
    // Handle mobile navigation toggler
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const target = document.querySelector(this.dataset.target);
            if (target) {
                target.classList.toggle('show');
            }
        });
    }
    
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && (currentPath === href || currentPath.startsWith(href))) {
            link.classList.add('active');
            
            // If in dropdown, also highlight parent
            const parentDropdown = link.closest('.dropdown');
            if (parentDropdown) {
                const dropdownToggle = parentDropdown.querySelector('.dropdown-toggle');
                if (dropdownToggle) {
                    dropdownToggle.classList.add('active');
                }
            }
        }
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    // Initialize all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize data tables
 */
function initDataTables() {
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        // Add sorting functionality if table has sortable headers
        const sortableHeaders = table.querySelectorAll('th.sortable');
        if (sortableHeaders.length > 0) {
            sortableHeaders.forEach(header => {
                header.addEventListener('click', function() {
                    sortTable(table, Array.from(sortableHeaders).indexOf(header));
                });
            });
        }
        
        // Add search functionality if table has search input
        const tableId = table.getAttribute('id');
        if (tableId) {
            const searchInput = document.querySelector(`#${tableId}-search`);
            if (searchInput) {
                searchInput.addEventListener('keyup', function() {
                    searchTable(table, this.value);
                });
            }
        }
    });
}

/**
 * Sort table by column
 * @param {HTMLElement} table - Table element to sort
 * @param {number} columnIndex - Index of column to sort by
 */
function sortTable(table, columnIndex) {
    const headers = table.querySelectorAll('th');
    const header = headers[columnIndex];
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Determine sort direction
    const isAscending = !header.classList.contains('asc');
    
    // Reset all headers
    headers.forEach(h => {
        h.classList.remove('asc', 'desc');
    });
    
    // Set current header sort class
    header.classList.add(isAscending ? 'asc' : 'desc');
    
    // Sort rows
    rows.sort((a, b) => {
        const cellA = a.querySelectorAll('td')[columnIndex].textContent.trim();
        const cellB = b.querySelectorAll('td')[columnIndex].textContent.trim();
        
        // Check if numeric
        const numA = parseFloat(cellA.replace(/[^0-9.-]+/g, ''));
        const numB = parseFloat(cellB.replace(/[^0-9.-]+/g, ''));
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return isAscending ? numA - numB : numB - numA;
        } else {
            return isAscending ? 
                cellA.localeCompare(cellB) : 
                cellB.localeCompare(cellA);
        }
    });
    
    // Re-append rows in new order
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Search table
 * @param {HTMLElement} table - Table element to search
 * @param {string} query - Search query
 */
function searchTable(table, query) {
    const rows = table.querySelectorAll('tbody tr');
    const lowerQuery = query.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.indexOf(lowerQuery) === -1) {
            row.style.display = 'none';
        } else {
            row.style.display = '';
        }
    });
    
    // Show no results message if needed
    const noResults = table.nextElementSibling;
    if (noResults && noResults.classList.contains('no-results')) {
        if (Array.from(rows).every(row => row.style.display === 'none')) {
            noResults.style.display = 'block';
        } else {
            noResults.style.display = 'none';
        }
    }
}

/**
 * Add event listeners for general interactions
 */
function addEventListeners() {
    // Toggle password visibility
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = document.getElementById(this.dataset.target);
            if (input) {
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);
                
                // Update icon
                this.innerHTML = type === 'password' ? 
                    '<i class="fas fa-eye"></i>' : 
                    '<i class="fas fa-eye-slash"></i>';
            }
        });
    });
    
    // Handle filter forms
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const params = new URLSearchParams();
            
            for (const [key, value] of formData.entries()) {
                if (value) {
                    params.append(key, value);
                }
            }
            
            // Get target URL
            const targetUrl = this.dataset.target || window.location.pathname;
            window.location.href = `${targetUrl}?${params.toString()}`;
        });
    });
}

/**
 * Setup API response handlers
 */
function setupApiHandlers() {
    // Handle confirmation modals
    const confirmationModals = document.querySelectorAll('.confirmation-modal');
    confirmationModals.forEach(modal => {
        const confirmBtn = modal.querySelector('.btn-confirm');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function() {
                const targetForm = document.getElementById(this.dataset.target);
                if (targetForm) {
                    targetForm.submit();
                }
            });
        }
    });
}

// ======== Chart Utilities ========

/**
 * Create a Chart.js chart
 * @param {string} elementId - HTML element ID for the chart
 * @param {string} type - Chart type (line, bar, pie, etc.)
 * @param {Object} data - Chart data
 * @param {Object} options - Chart options
 * @returns {Chart} - Chart.js instance
 */
function createChart(elementId, type, data, options = {}) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    // Set default options based on chart type
    const defaultOptions = getChartDefaultOptions(type);
    
    // Merge options
    const chartOptions = { ...defaultOptions, ...options };
    
    // Create chart
    return new Chart(ctx, {
        type: type,
        data: data,
        options: chartOptions
    });
}

/**
 * Get default options for chart type
 * @param {string} type - Chart type
 * @returns {Object} - Default options
 */
function getChartDefaultOptions(type) {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        }
    };
    
    // Add type-specific options
    switch (type) {
        case 'line':
            return {
                ...commonOptions,
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return formatNumber(value);
                            }
                        }
                    }
                },
                elements: {
                    line: {
                        tension: 0.2
                    },
                    point: {
                        radius: 3,
                        hoverRadius: 5
                    }
                }
            };
            
        case 'bar':
            return {
                ...commonOptions,
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatNumber(value);
                            }
                        }
                    }
                }
            };
            
        case 'pie':
        case 'doughnut':
            return {
                ...commonOptions,
                plugins: {
                    ...commonOptions.plugins,
                    legend: {
                        position: 'right',
                    }
                },
                cutout: type === 'doughnut' ? '50%' : undefined
            };
            
        default:
            return commonOptions;
    }
}

/**
 * Update chart with new data
 * @param {Chart} chart - Chart.js instance
 * @param {Object} newData - New chart data
 */
function updateChart(chart, newData) {
    // Update data
    chart.data.labels = newData.labels || chart.data.labels;
    
    // Update each dataset
    if (newData.datasets) {
        newData.datasets.forEach((dataset, i) => {
            // If dataset exists, update it
            if (chart.data.datasets[i]) {
                Object.keys(dataset).forEach(key => {
                    chart.data.datasets[i][key] = dataset[key];
                });
            } else {
                // Otherwise add new dataset
                chart.data.datasets.push(dataset);
            }
        });
        
        // Remove extra datasets
        if (chart.data.datasets.length > newData.datasets.length) {
            chart.data.datasets.splice(newData.datasets.length);
        }
    }
    
    // Update chart
    chart.update();
}

/**
 * Create color gradient for chart
 * @param {string} colorStart - Starting color (hex)
 * @param {string} colorEnd - Ending color (hex)
 * @param {number} steps - Number of steps in gradient
 * @returns {Array} - Array of colors
 */
function createColorGradient(colorStart, colorEnd, steps) {
    // Convert hex to RGB
    const start = hexToRgb(colorStart);
    const end = hexToRgb(colorEnd);
    
    // Create gradient steps
    const colors = [];
    for (let i = 0; i < steps; i++) {
        const r = Math.round(start.r + (end.r - start.r) * (i / (steps - 1)));
        const g = Math.round(start.g + (end.g - start.g) * (i / (steps - 1)));
        const b = Math.round(start.b + (end.b - start.b) * (i / (steps - 1)));
        colors.push(`rgb(${r}, ${g}, ${b})`);
    }
    
    return colors;
}

/**
 * Convert hex color to RGB
 * @param {string} hex - Hex color code
 * @returns {Object} - RGB values
 */
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
}

// ======== Data Visualization Utilities ========

/**
 * Format number with commas
 * @param {number} num - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted number
 */
function formatNumber(num, decimals = 0) {
    if (num === null || num === undefined) return '';
    
    // Handle large numbers
    if (Math.abs(num) >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (Math.abs(num) >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    
    // Format with commas and specified decimals
    return num.toLocaleString(undefined, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

/**
 * Format percentage
 * @param {number} value - Value to format as percentage
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted percentage
 */
function formatPercentage(value, decimals = 1) {
    if (value === null || value === undefined) return '';
    
    return value.toLocaleString(undefined, {
        style: 'percent',
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

/**
 * Calculate percentage change
 * @param {number} current - Current value
 * @param {number} previous - Previous value
 * @returns {number} - Percentage change
 */
function calculateChange(current, previous) {
    if (!current || !previous) return 0;
    return (current - previous) / previous;
}

/**
 * Create color-coded indicator for change
 * @param {number} change - Change value (as decimal)
 * @param {boolean} inverted - Whether to invert colors (positive is bad)
 * @returns {string} - HTML for indicator
 */
function createChangeIndicator(change, inverted = false) {
    if (!change) return '';
    
    const absChange = Math.abs(change);
    const formatted = formatPercentage(absChange);
    
    let className, icon;
    
    if (change > 0) {
        className = inverted ? 'text-danger' : 'text-success';
        icon = 'fa-arrow-up';
    } else {
        className = inverted ? 'text-success' : 'text-danger';
        icon = 'fa-arrow-down';
    }
    
    return `<span class="${className}"><i class="fas ${icon} me-1"></i>${formatted}</span>`;
}

/**
 * Download chart as image
 * @param {Chart} chart - Chart.js instance
 * @param {string} filename - Filename for download
 */
function downloadChartImage(chart, filename = 'chart.png') {
    // Create link for download
    const link = document.createElement('a');
    link.download = filename;
    link.href = chart.toBase64Image();
    link.click();
}

/**
 * Export data as CSV
 * @param {Array} data - Array of objects
 * @param {string} filename - Filename for download
 */
function exportCsv(data, filename = 'export.csv') {
    if (!data || !data.length) return;
    
    // Get headers from first object
    const headers = Object.keys(data[0]);
    
    // Create CSV content
    let csvContent = headers.join(',') + '\n';
    
    // Add rows
    data.forEach(item => {
        const row = headers.map(header => {
            const value = item[header];
            // Handle special characters and quotes
            if (typeof value === 'string') {
                return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        });
        csvContent += row.join(',') + '\n';
    });
    
    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ======== API Utilities ========

/**
 * Fetch data from API
 * @param {string} url - API URL
 * @param {Object} options - Fetch options
 * @returns {Promise} - Fetch promise
 */
async function fetchApi(url, options = {}) {
    try {
        const response = await fetch(url, {
            credentials: 'same-origin',
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        
        return response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * Show loading indicator
 * @param {string} elementId - HTML element ID
 * @param {string} message - Loading message
 */
function showLoading(elementId, message = 'Loading...') {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Create loading overlay
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="spinner-container">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-text">${message}</div>
        </div>
    `;
    
    // Add overlay
    element.style.position = 'relative';
    element.appendChild(overlay);
}

/**
 * Hide loading indicator
 * @param {string} elementId - HTML element ID
 */
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // Remove loading overlay
    const overlay = element.querySelector('.loading-overlay');
    if (overlay) {
        element.removeChild(overlay);
    }
}

// ======== Date Utilities ========

/**
 * Format date
 * @param {string|Date} date - Date to format
 * @param {string} format - Date format ('short', 'medium', 'long')
 * @returns {string} - Formatted date
 */
function formatDate(date, format = 'medium') {
    if (!date) return '';
    
    // Convert string to Date
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    // Handle invalid dates
    if (isNaN(dateObj.getTime())) return '';
    
    // Format options
    const options = {
        short: { month: 'numeric', day: 'numeric', year: '2-digit' },
        medium: { month: 'short', day: 'numeric', year: 'numeric' },
        long: { month: 'long', day: 'numeric', year: 'numeric' }
    };
    
    return dateObj.toLocaleDateString(undefined, options[format] || options.medium);
}

/**
 * Get date range for period
 * @param {string} period - Period ('1d', '7d', '30d', '90d', '1y', 'ytd')
 * @returns {Object} - Start and end dates
 */
function getDateRange(period) {
    const end = new Date();
    let start = new Date();
    
    switch (period) {
        case '1d':
            start.setDate(start.getDate() - 1);
            break;
        case '7d':
            start.setDate(start.getDate() - 7);
            break;
        case '30d':
            start.setDate(start.getDate() - 30);
            break;
        case '90d':
            start.setDate(start.getDate() - 90);
            break;
        case '1y':
            start.setFullYear(start.getFullYear() - 1);
            break;
        case 'ytd':
            start = new Date(start.getFullYear(), 0, 1); // January 1 of current year
            break;
        default:
            start.setDate(start.getDate() - 30); // Default to 30 days
    }
    
    return {
        start,
        end
    };
}

// Export utilities for use in other modules
window.LithFlow = {
    charts: {
        create: createChart,
        update: updateChart,
        downloadImage: downloadChartImage,
        createColorGradient: createColorGradient
    },
    formatting: {
        number: formatNumber,
        percentage: formatPercentage,
        date: formatDate,
        changeIndicator: createChangeIndicator
    },
    calculations: {
        change: calculateChange,
        dateRange: getDateRange
    },
    data: {
        exportCsv: exportCsv,
        fetchApi: fetchApi
    },
    ui: {
        showLoading: showLoading,
        hideLoading: hideLoading,
        sortTable: sortTable,
        searchTable: searchTable
    }
};