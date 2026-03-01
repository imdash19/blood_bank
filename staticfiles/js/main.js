/**
 * Blood Bank Management System - Main JavaScript
 * Handles animations, form validations, and interactive elements
 */

// ==================== Global Variables ====================
let isScrolling = false;

// ==================== DOM Content Loaded ====================
document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initAnimations();
    initFormValidations();
    initSmoothScroll();
    initCounters();
    initBloodStockCards();
});

// ==================== Navbar Functions ====================
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    const navbarLinks = document.querySelectorAll('.navbar-link');

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    if (navbarToggle) {
        navbarToggle.addEventListener('click', function() {
            navbarMenu.classList.toggle('active');
            const icon = navbarToggle.querySelector('i');
            if (icon) {
                if (navbarMenu.classList.contains('active')) {
                    icon.className = 'fas fa-times';
                } else {
                    icon.className = 'fas fa-bars';
                }
            }
        });
    }

    // Close mobile menu when clicking a link
    navbarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                navbarMenu.classList.remove('active');
                const icon = navbarToggle.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-bars';
                }
            }
        });
    });

    // Set active link based on current page
    const currentPath = window.location.pathname;
    navbarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// ==================== Scroll Animations ====================
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = entry.target.dataset.animation || 'fadeInUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    const animatedElements = document.querySelectorAll('.card, .stat-card, .blood-stock-card, .section-header');
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.dataset.animation = `fadeInUp 0.6s ease-out ${index * 0.1}s forwards`;
        observer.observe(el);
    });
}

// ==================== Smooth Scroll ====================
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const offsetTop = targetElement.offsetTop - 80;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ==================== Counter Animation ====================
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');

    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target') || counter.textContent);
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };

        updateCounter();
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                animateCounter(entry.target);
                entry.target.classList.add('counted');
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => {
        counter.setAttribute('data-target', counter.textContent);
        counter.textContent = '0';
        observer.observe(counter);
    });
}

// ==================== Blood Stock Cards ====================
function initBloodStockCards() {
    const bloodCards = document.querySelectorAll('.blood-stock-card');

    bloodCards.forEach(card => {
        card.addEventListener('click', function() {
            const bloodGroup = this.querySelector('.blood-group').textContent;
            // You can add functionality to filter or show donors with this blood group
            console.log('Selected blood group:', bloodGroup);
        });
    });
}

// ==================== Form Validations ====================
function initFormValidations() {
    const forms = document.querySelectorAll('form[data-validate="true"]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('.form-control[required]');

    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });

    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name || field.id;
    let isValid = true;
    let errorMessage = '';

    // Remove previous error
    removeFieldError(field);

    // Required field validation
    if (field.hasAttribute('required') && !value) {
        errorMessage = 'This field is required';
        isValid = false;
    }

    // Email validation
    else if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            errorMessage = 'Please enter a valid email address';
            isValid = false;
        }
    }

    // Phone validation
    else if (field.type === 'tel' && value) {
        const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
        if (!phoneRegex.test(value)) {
            errorMessage = 'Please enter a valid phone number';
            isValid = false;
        }
    }

    // Password validation
    else if (field.type === 'password' && field.name === 'password' && value) {
        if (value.length < 8) {
            errorMessage = 'Password must be at least 8 characters';
            isValid = false;
        }
    }

    // Confirm password validation
    else if (field.name === 'confirm_password' && value) {
        const password = document.querySelector('input[name="password"]');
        if (password && value !== password.value) {
            errorMessage = 'Passwords do not match';
            isValid = false;
        }
    }

    // Number validation
    else if (field.type === 'number' && value) {
        const min = field.getAttribute('min');
        const max = field.getAttribute('max');
        const numValue = parseFloat(value);

        if (min && numValue < parseFloat(min)) {
            errorMessage = `Value must be at least ${min}`;
            isValid = false;
        } else if (max && numValue > parseFloat(max)) {
            errorMessage = `Value must be at most ${max}`;
            isValid = false;
        }
    }

    if (!isValid) {
        showFieldError(field, errorMessage);
    }

    return isValid;
}

function showFieldError(field, message) {
    field.classList.add('error');
    field.style.borderColor = 'var(--danger)';

    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = 'var(--danger)';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.style.marginTop = '4px';
    errorDiv.textContent = message;

    field.parentNode.appendChild(errorDiv);
}

function removeFieldError(field) {
    field.classList.remove('error');
    field.style.borderColor = '';

    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// ==================== AJAX Form Submission ====================
function submitFormAjax(form, url, onSuccess) {
    const formData = new FormData(form);
    const csrftoken = getCookie('csrftoken');

    showLoading(form);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(form);
        if (data.success) {
            showAlert('success', data.message || 'Operation successful!');
            if (onSuccess) onSuccess(data);
        } else {
            showAlert('error', data.message || 'An error occurred.');
        }
    })
    .catch(error => {
        hideLoading(form);
        showAlert('error', 'Network error. Please try again.');
        console.error('Error:', error);
    });
}

// ==================== Alert Messages ====================
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '100px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.style.maxWidth = '500px';

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

// ==================== Loading Indicator ====================
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'loading-overlay';
    spinner.innerHTML = '<div class="spinner"></div>';
    spinner.style.position = 'absolute';
    spinner.style.top = '0';
    spinner.style.left = '0';
    spinner.style.width = '100%';
    spinner.style.height = '100%';
    spinner.style.background = 'rgba(255, 255, 255, 0.9)';
    spinner.style.display = 'flex';
    spinner.style.alignItems = 'center';
    spinner.style.justifyContent = 'center';
    spinner.style.zIndex = '1000';

    element.style.position = 'relative';
    element.appendChild(spinner);
}

function hideLoading(element) {
    const overlay = element.querySelector('.loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// ==================== Utility Functions ====================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function debounce(func, wait) {
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

// ==================== Search Functionality ====================
function initSearch(inputId, targetSelector, searchProperties) {
    const searchInput = document.getElementById(inputId);
    if (!searchInput) return;

    const debouncedSearch = debounce(function(value) {
        const targets = document.querySelectorAll(targetSelector);
        const searchTerm = value.toLowerCase();

        targets.forEach(target => {
            let textContent = '';
            searchProperties.forEach(prop => {
                const element = target.querySelector(prop);
                if (element) {
                    textContent += element.textContent.toLowerCase() + ' ';
                }
            });

            if (textContent.includes(searchTerm)) {
                target.style.display = '';
            } else {
                target.style.display = 'none';
            }
        });
    }, 300);

    searchInput.addEventListener('input', function() {
        debouncedSearch(this.value);
    });
}

// ==================== Modal Functions ====================
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// ==================== Filter Functions ====================
function initFilters() {
    const filterButtons = document.querySelectorAll('[data-filter]');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filterValue = this.getAttribute('data-filter');
            const targetSelector = this.getAttribute('data-target');
            const targets = document.querySelectorAll(targetSelector);

            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Filter elements
            targets.forEach(target => {
                if (filterValue === 'all' || target.getAttribute('data-category') === filterValue) {
                    target.style.display = '';
                } else {
                    target.style.display = 'none';
                }
            });
        });
    });
}

// ==================== Date Formatting ====================
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    const dateOptions = { year: 'numeric', month: 'short', day: 'numeric' };
    const timeOptions = { hour: '2-digit', minute: '2-digit' };
    return date.toLocaleDateString('en-US', dateOptions) + ' at ' + date.toLocaleTimeString('en-US', timeOptions);
}

// ==================== Blood Group Compatibility ====================
const bloodCompatibility = {
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-': ['A-', 'B-', 'AB-', 'O-'],
    'O+': ['O+', 'O-'],
    'O-': ['O-']
};

function getCompatibleBloodGroups(bloodGroup) {
    return bloodCompatibility[bloodGroup] || [];
}

// ==================== Export Functions ====================
window.BBMS = {
    showAlert,
    showLoading,
    hideLoading,
    openModal,
    closeModal,
    submitFormAjax,
    formatDate,
    formatDateTime,
    getCompatibleBloodGroups
};