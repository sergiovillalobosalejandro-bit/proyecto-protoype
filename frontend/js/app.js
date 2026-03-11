// Main application controller

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    await initApp();
});

// Initialize application
async function initApp() {
    try {
        // Check authentication
        const isAuthenticated = await checkAuth();
        
        if (isAuthenticated) {
            // Load dashboard by default
            await loadDashboard();
        }
    } catch (error) {
        console.error('App initialization error:', error);
        showError('Error al inicializar la aplicación');
    }
}

// View management
function showView(viewName) {
    // Hide all views
    const views = document.querySelectorAll('.view');
    views.forEach(view => view.classList.remove('active'));
    
    // Show selected view
    const selectedView = document.getElementById(`${viewName}-view`);
    if (selectedView) {
        selectedView.classList.add('active');
    }
    
    // Update navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    const activeNavLink = document.querySelector(`[onclick="showView('${viewName}')"]`);
    if (activeNavLink) {
        activeNavLink.classList.add('active');
    }
    
    // Load view-specific data
    loadViewData(viewName);
}

// Load view-specific data
async function loadViewData(viewName) {
    switch (viewName) {
        case 'dashboard':
            await loadDashboard();
            break;
        case 'search':
            // Search view doesn't need initial data
            break;
        case 'clinical':
            // Clinical view loads when couder is selected
            break;
    }
}

// Tab management
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Show selected tab
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Update tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    const activeTabBtn = document.querySelector(`[onclick="showTab('${tabName}')"]`);
    if (activeTabBtn) {
        activeTabBtn.classList.add('active');
    }
}

// Modal management
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        
        // Reset form if it exists
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Escape key to close modals
    if (event.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            activeModal.classList.remove('active');
        }
    }
    
    // Ctrl+K for quick search
    if (event.ctrlKey && event.key === 'k') {
        event.preventDefault();
        showView('search');
        document.getElementById('cc-search').focus();
    }
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    
    for (const input of inputs) {
        if (!input.value.trim()) {
            input.focus();
            showError(`Por favor complete el campo "${input.previousElementSibling.textContent}"`);
            return false;
        }
    }
    
    return true;
}

// Auto-save functionality
let autoSaveTimer = null;

function setupAutoSave(formId, saveFunction) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                saveFunction();
            }, 2000); // Auto-save after 2 seconds of inactivity
        });
    });
}

// Print functionality
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const printWindow = window.open('', '_blank');
    const clonedElement = element.cloneNode(true);
    
    // Remove buttons and interactive elements
    const buttons = clonedElement.querySelectorAll('button, .btn');
    buttons.forEach(btn => btn.remove());
    
    // Add print styles
    const printStyles = `
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .card { break-inside: avoid; margin-bottom: 20px; }
            .modal-content { max-width: none; margin: 0; }
            @media print {
                .no-print { display: none; }
            }
        </style>
    `;
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Imprimir</title>
            ${printStyles}
        </head>
        <body>
            ${clonedElement.innerHTML}
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}

// Export functionality
function exportToCSV(data, filename) {
    if (!data || data.length === 0) {
        showError('No hay datos para exportar');
        return;
    }
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Notification system
function showNotification(title, message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-header">
            <h4>${title}</h4>
            <button onclick="this.parentElement.parentElement.remove()" class="notification-close">&times;</button>
        </div>
        <div class="notification-body">
            <p>${message}</p>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Theme management
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Load saved theme
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
}

// Initialize theme
loadTheme();

// Performance monitoring
function logPerformance(action, startTime) {
    const duration = performance.now() - startTime;
    console.log(`${action} took ${duration.toFixed(2)} milliseconds`);
    
    // Log slow operations
    if (duration > 1000) {
        console.warn(`Slow operation detected: ${action} took ${duration.toFixed(2)}ms`);
    }
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showError('Ocurrió un error inesperado. Por favor recargue la página.');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showError('Ocurrió un error en una operación asíncrona.');
});

// Service worker registration (for PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 350px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        z-index: 3000;
        animation: slideIn 0.3s ease-out;
    }
    
    .notification-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1rem 0.5rem;
        border-bottom: 1px solid #eee;
    }
    
    .notification-header h4 {
        margin: 0;
        font-size: 1rem;
        color: #333;
    }
    
    .notification-close {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        color: #999;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .notification-close:hover {
        color: #666;
    }
    
    .notification-body {
        padding: 0.5rem 1rem 1rem;
    }
    
    .notification-body p {
        margin: 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    .notification-info { border-left: 4px solid #17a2b8; }
    .notification-success { border-left: 4px solid #28a745; }
    .notification-warning { border-left: 4px solid #ffc107; }
    .notification-error { border-left: 4px solid #dc3545; }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    [data-theme="dark"] {
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --text-primary: #ffffff;
        --text-secondary: #b3b3b3;
        --border-color: #404040;
    }
    
    [data-theme="dark"] body {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    [data-theme="dark"] .card {
        background: var(--bg-secondary);
        border-color: var(--border-color);
    }
    
    [data-theme="dark"] .modal-content {
        background: var(--bg-secondary);
        color: var(--text-primary);
    }
`;
document.head.appendChild(notificationStyles);
