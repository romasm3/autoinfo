/*
╔══════════════════════════════════════════════════════════╗
║  AUTOINFO - MAIN JAVASCRIPT                              ║
╠══════════════════════════════════════════════════════════╣
║  LOKACIJA: /autoinfo/apps/core/static/core/js/main.js   ║
║  PASKIRTIS: Frontend interaktyvumas                     ║
╚══════════════════════════════════════════════════════════╝
*/

// ═══════════════════════════════════════════════════════
// WAIT FOR DOM LOAD
// ═══════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function() {

    // Initialize all components
    initMobileMenu();
    initFAQ();
    initFormValidation();
    initAlerts();

    console.log('✅ AutoInfo initialized');
});

// ═══════════════════════════════════════════════════════
// MOBILE MENU
// ═══════════════════════════════════════════════════════
function initMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggle && navLinks) {
        toggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            toggle.classList.toggle('active');
        });
    }
}

// ═══════════════════════════════════════════════════════
// FAQ ACCORDION
// ═══════════════════════════════════════════════════════
function initFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.parentElement;
            const isActive = faqItem.classList.contains('active');

            // Close all FAQ items
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
            });

            // Open clicked item if it wasn't active
            if (!isActive) {
                faqItem.classList.add('active');
            }
        });
    });
}

// ═══════════════════════════════════════════════════════
// FORM VALIDATION
// ═══════════════════════════════════════════════════════
function initFormValidation() {
    // VIN Input - tylko uppercase i max 17 znaków
    const vinInputs = document.querySelectorAll('input[name="vin"]');
    vinInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();

            // Validate VIN format (no I, O, Q letters)
            const invalidChars = /[IOQ]/g;
            if (invalidChars.test(this.value)) {
                this.setCustomValidity('VIN cannot contain letters I, O, or Q');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isValidEmail(this.value)) {
                this.setCustomValidity('Please enter a valid email address');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.name === 'password1') {
            input.addEventListener('input', function() {
                const strength = getPasswordStrength(this.value);
                updatePasswordStrength(this, strength);
            });
        }
    });
}

// ═══════════════════════════════════════════════════════
// EMAIL VALIDATION
// ═══════════════════════════════════════════════════════
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// ═══════════════════════════════════════════════════════
// PASSWORD STRENGTH
// ═══════════════════════════════════════════════════════
function getPasswordStrength(password) {
    let strength = 0;

    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    return strength;
}

function updatePasswordStrength(input, strength) {
    // Remove existing indicator
    let indicator = input.parentElement.querySelector('.password-strength');
    if (indicator) {
        indicator.remove();
    }

    // Create new indicator
    if (input.value.length > 0) {
        indicator = document.createElement('div');
        indicator.className = 'password-strength';

        let text = '';
        let color = '';

        if (strength <= 2) {
            text = 'Weak';
            color = '#dc3545';
        } else if (strength <= 3) {
            text = 'Medium';
            color = '#ffc107';
        } else {
            text = 'Strong';
            color = '#28a745';
        }

        indicator.style.cssText = `
            margin-top: 0.5rem;
            font-size: 0.875rem;
            color: ${color};
            font-weight: 600;
        `;
        indicator.textContent = `Password strength: ${text}`;

        input.parentElement.appendChild(indicator);
    }
}

// ═══════════════════════════════════════════════════════
// AUTO-HIDE ALERTS
// ═══════════════════════════════════════════════════════
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';

            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);

        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            float: right;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: inherit;
            margin-left: 1rem;
        `;

        closeBtn.addEventListener('click', function() {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });

        alert.prepend(closeBtn);
    });
}

// ═══════════════════════════════════════════════════════
// SMOOTH SCROLL
// ═══════════════════════════════════════════════════════
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ═══════════════════════════════════════════════════════
// UTILITIES
// ═══════════════════════════════════════════════════════

// Format number as currency
function formatCurrency(amount, currency = 'PLN') {
    return `${amount.toFixed(2)} ${currency}`;
}

// Format date
function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Export utilities for use in other scripts
window.AutoInfo = {
    formatCurrency,
    formatDate,
    copyToClipboard,
    showNotification
};
