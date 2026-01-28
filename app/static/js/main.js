/**
 * Online Bookstore - Main JavaScript
 * Handles client-side validation, interactivity, and form management
 */

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    initializeFormValidation();

    // Auto-dismiss alerts after 5 seconds
    autoDismissAlerts();

    // Initialize tooltips
    initializeTooltips();

    // Confirmation dialogs
    initializeConfirmDialogs();
});

/**
 * Initialize Bootstrap form validation
 * Adds client-side validation to all forms with 'needs-validation' class
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Auto-dismiss Bootstrap alerts after 5 seconds
 */
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

/**
 * Initialize Bootstrap tooltips on elements with title attribute
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Add confirmation dialog to delete/critical actions
 */
function initializeConfirmDialogs() {
    const deleteButtons = document.querySelectorAll('[onclick*="confirm"]');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const confirmed = confirm(
                this.getAttribute('onclick').match(/'([^']+)'/)[1] ||
                'Are you sure you want to proceed?'
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
}

/**
 * Format currency values in the DOM
 * @param {number} value - The value to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

/**
 * Validate email format
 * @param {string} email - Email address to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show loading indicator
 * Useful for long-running operations
 */
function showLoadingIndicator() {
    const loader = document.createElement('div');
    loader.id = 'loading-indicator';
    loader.className = 'spinner-border';
    loader.role = 'status';
    loader.innerHTML = '<span class="visually-hidden">Loading...</span>';
    document.body.appendChild(loader);
}

/**
 * Hide loading indicator
 */
function hideLoadingIndicator() {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.remove();
    }
}

/**
 * Truncate text to specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} length - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 100) {
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

/**
 * Handle Add to Cart button click
 * Shows user feedback on successful addition
 */
document.addEventListener('click', function(event) {
    if (event.target.closest('.add-to-cart-btn')) {
        const btn = event.target.closest('.add-to-cart-btn');
        const originalText = btn.textContent;
        btn.textContent = '✓ Added to Cart';
        btn.disabled = true;

        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 2000);
    }
});

/**
 * Display toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of notification (success, danger, warning, info)
 * @param {number} duration - Duration in milliseconds (default: 3000)
 */
function showToast(message, type = 'info', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert at the top of the first container
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }

    // Auto-dismiss
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, duration);
}

/**
 * Debounce function for search input
 * Prevents excessive API calls while typing
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Add keyboard shortcuts
 * Alt + S: Search
 * Alt + C: Cart
 * Alt + H: Home
 */
document.addEventListener('keydown', function(event) {
    if (event.altKey) {
        switch (event.key.toLowerCase()) {
            case 's':
                event.preventDefault();
                document.querySelector('input[name="search"]')?.focus();
                break;
            case 'c':
                event.preventDefault();
                window.location.href = '/cart';
                break;
            case 'h':
                event.preventDefault();
                window.location.href = '/';
                break;
        }
    }
});

// Export functions for use in other scripts
window.bookstoreUtils = {
    formatCurrency,
    validateEmail,
    showLoadingIndicator,
    hideLoadingIndicator,
    truncateText,
    showToast,
    debounce
};
