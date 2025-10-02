/* Kids Clothing ERP - Web Script */

odoo.define('core_web.KidsClothingWeb', function (require) {
    'use strict';

    var core = require('web.core');
    var AbstractController = require('web.AbstractController');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var _t = core._t;

    // Web Utilities
    var WebUtils = {
        // Theme Management
        setTheme: function(theme) {
            document.body.className = document.body.className.replace(/theme-\w+/g, '');
            document.body.classList.add('theme-' + theme);
            localStorage.setItem('kids_clothing_theme', theme);
        },
        
        getTheme: function() {
            return localStorage.getItem('kids_clothing_theme') || 'default';
        },
        
        // User Preferences
        setUserPreference: function(key, value) {
            var preferences = this.getUserPreferences();
            preferences[key] = value;
            localStorage.setItem('kids_clothing_preferences', JSON.stringify(preferences));
        },
        
        getUserPreference: function(key) {
            var preferences = this.getUserPreferences();
            return preferences[key];
        },
        
        getUserPreferences: function() {
            var stored = localStorage.getItem('kids_clothing_preferences');
            return stored ? JSON.parse(stored) : {};
        },
        
        // Responsive Utilities
        isMobile: function() {
            return window.innerWidth <= 768;
        },
        
        isTablet: function() {
            return window.innerWidth > 768 && window.innerWidth <= 1024;
        },
        
        isDesktop: function() {
            return window.innerWidth > 1024;
        },
        
        // Animation Utilities
        fadeIn: function(element, duration = 300) {
            element.style.opacity = '0';
            element.style.display = 'block';
            
            var start = performance.now();
            
            function animate(timestamp) {
                var elapsed = timestamp - start;
                var progress = Math.min(elapsed / duration, 1);
                
                element.style.opacity = progress;
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            }
            
            requestAnimationFrame(animate);
        },
        
        fadeOut: function(element, duration = 300) {
            var start = performance.now();
            var initialOpacity = parseFloat(getComputedStyle(element).opacity);
            
            function animate(timestamp) {
                var elapsed = timestamp - start;
                var progress = Math.min(elapsed / duration, 1);
                
                element.style.opacity = initialOpacity * (1 - progress);
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    element.style.display = 'none';
                }
            }
            
            requestAnimationFrame(animate);
        },
        
        slideDown: function(element, duration = 300) {
            element.style.height = '0';
            element.style.overflow = 'hidden';
            element.style.display = 'block';
            
            var targetHeight = element.scrollHeight;
            var start = performance.now();
            
            function animate(timestamp) {
                var elapsed = timestamp - start;
                var progress = Math.min(elapsed / duration, 1);
                
                element.style.height = (targetHeight * progress) + 'px';
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    element.style.height = 'auto';
                    element.style.overflow = 'visible';
                }
            }
            
            requestAnimationFrame(animate);
        },
        
        slideUp: function(element, duration = 300) {
            var startHeight = element.offsetHeight;
            var start = performance.now();
            
            function animate(timestamp) {
                var elapsed = timestamp - start;
                var progress = Math.min(elapsed / duration, 1);
                
                element.style.height = (startHeight * (1 - progress)) + 'px';
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    element.style.display = 'none';
                    element.style.height = 'auto';
                }
            }
            
            requestAnimationFrame(animate);
        },
        
        // DOM Utilities
        createElement: function(tag, attributes = {}, content = '') {
            var element = document.createElement(tag);
            
            for (var key in attributes) {
                if (key === 'className') {
                    element.className = attributes[key];
                } else if (key === 'innerHTML') {
                    element.innerHTML = attributes[key];
                } else {
                    element.setAttribute(key, attributes[key]);
                }
            }
            
            if (content) {
                element.textContent = content;
            }
            
            return element;
        },
        
        addClass: function(element, className) {
            if (element.classList) {
                element.classList.add(className);
            } else {
                element.className += ' ' + className;
            }
        },
        
        removeClass: function(element, className) {
            if (element.classList) {
                element.classList.remove(className);
            } else {
                element.className = element.className.replace(new RegExp('(^|\\s)' + className + '(\\s|$)', 'g'), ' ');
            }
        },
        
        hasClass: function(element, className) {
            if (element.classList) {
                return element.classList.contains(className);
            } else {
                return new RegExp('(^|\\s)' + className + '(\\s|$)', 'g').test(element.className);
            }
        },
        
        toggleClass: function(element, className) {
            if (this.hasClass(element, className)) {
                this.removeClass(element, className);
            } else {
                this.addClass(element, className);
            }
        },
        
        // Event Utilities
        on: function(element, event, handler) {
            if (element.addEventListener) {
                element.addEventListener(event, handler, false);
            } else if (element.attachEvent) {
                element.attachEvent('on' + event, handler);
            }
        },
        
        off: function(element, event, handler) {
            if (element.removeEventListener) {
                element.removeEventListener(event, handler, false);
            } else if (element.detachEvent) {
                element.detachEvent('on' + event, handler);
            }
        },
        
        // Storage Utilities
        setStorage: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                console.error('Error setting storage:', e);
            }
        },
        
        getStorage: function(key) {
            try {
                var value = localStorage.getItem(key);
                return value ? JSON.parse(value) : null;
            } catch (e) {
                console.error('Error getting storage:', e);
                return null;
            }
        },
        
        removeStorage: function(key) {
            try {
                localStorage.removeItem(key);
            } catch (e) {
                console.error('Error removing storage:', e);
            }
        },
        
        // URL Utilities
        getUrlParameter: function(name) {
            var urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
        },
        
        setUrlParameter: function(name, value) {
            var url = new URL(window.location);
            url.searchParams.set(name, value);
            window.history.pushState({}, '', url);
        },
        
        // Formatting Utilities
        formatCurrency: function(amount, currency = 'INR') {
            var symbols = {
                'INR': '₹',
                'USD': '$',
                'EUR': '€',
                'GBP': '£',
                'JPY': '¥'
            };
            var symbol = symbols[currency] || currency;
            return symbol + ' ' + amount.toLocaleString('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        },
        
        formatDate: function(date, format = 'DD/MM/YYYY') {
            if (!date) return '';
            
            var d = new Date(date);
            var day = d.getDate().toString().padStart(2, '0');
            var month = (d.getMonth() + 1).toString().padStart(2, '0');
            var year = d.getFullYear();
            
            return format
                .replace('DD', day)
                .replace('MM', month)
                .replace('YYYY', year);
        },
        
        formatTime: function(date, format = 'HH:MM:SS') {
            if (!date) return '';
            
            var d = new Date(date);
            var hours = d.getHours().toString().padStart(2, '0');
            var minutes = d.getMinutes().toString().padStart(2, '0');
            var seconds = d.getSeconds().toString().padStart(2, '0');
            
            return format
                .replace('HH', hours)
                .replace('MM', minutes)
                .replace('SS', seconds);
        },
        
        // Validation Utilities
        validateEmail: function(email) {
            var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        },
        
        validatePhone: function(phone) {
            var re = /^[\+]?[1-9][\d]{0,15}$/;
            return re.test(phone);
        },
        
        validateGST: function(gst) {
            if (!gst || gst.length !== 15) return false;
            if (!/^\d+$/.test(gst)) return false;
            
            var stateCode = gst.substring(0, 2);
            var panNumber = gst.substring(2, 12);
            
            if (parseInt(stateCode) < 1 || parseInt(stateCode) > 37) return false;
            if (!/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(panNumber)) return false;
            
            return true;
        },
        
        // Debounce and Throttle
        debounce: function(func, wait) {
            var timeout;
            return function executedFunction() {
                var later = function() {
                    clearTimeout(timeout);
                    func.apply(this, arguments);
                }.bind(this);
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        throttle: function(func, limit) {
            var inThrottle;
            return function() {
                var args = arguments;
                var context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(function() {
                        inThrottle = false;
                    }, limit);
                }
            };
        }
    };

    // Sidebar Management
    var SidebarManager = {
        init: function() {
            this.sidebar = document.querySelector('.o_main_sidebar');
            this.content = document.querySelector('.o_main_content');
            this.toggleBtn = document.querySelector('.sidebar-toggle');
            
            if (this.sidebar && this.toggleBtn) {
                this.bindEvents();
                this.loadState();
            }
        },
        
        bindEvents: function() {
            var self = this;
            
            if (this.toggleBtn) {
                this.toggleBtn.addEventListener('click', function() {
                    self.toggle();
                });
            }
            
            // Close sidebar on mobile when clicking outside
            if (WebUtils.isMobile()) {
                document.addEventListener('click', function(e) {
                    if (self.isOpen() && !self.sidebar.contains(e.target) && !self.toggleBtn.contains(e.target)) {
                        self.close();
                    }
                });
            }
            
            // Handle window resize
            window.addEventListener('resize', WebUtils.debounce(function() {
                self.handleResize();
            }, 250));
        },
        
        toggle: function() {
            if (this.isOpen()) {
                this.close();
            } else {
                this.open();
            }
        },
        
        open: function() {
            if (this.sidebar) {
                WebUtils.addClass(this.sidebar, 'show');
                WebUtils.setStorage('sidebar_open', true);
            }
        },
        
        close: function() {
            if (this.sidebar) {
                WebUtils.removeClass(this.sidebar, 'show');
                WebUtils.setStorage('sidebar_open', false);
            }
        },
        
        isOpen: function() {
            return this.sidebar && WebUtils.hasClass(this.sidebar, 'show');
        },
        
        loadState: function() {
            var isOpen = WebUtils.getStorage('sidebar_open');
            if (isOpen && !WebUtils.isMobile()) {
                this.open();
            }
        },
        
        handleResize: function() {
            if (WebUtils.isMobile()) {
                this.close();
            }
        }
    };

    // Header Management
    var HeaderManager = {
        init: function() {
            this.header = document.querySelector('.o_main_header');
            this.searchInput = document.querySelector('.o_main_header_search input');
            this.notificationBtn = document.querySelector('.btn-notification');
            this.notificationDropdown = document.querySelector('.notification-dropdown');
            this.userBtn = document.querySelector('.btn-user');
            this.userDropdown = document.querySelector('.user-dropdown');
            
            this.bindEvents();
        },
        
        bindEvents: function() {
            var self = this;
            
            // Search functionality
            if (this.searchInput) {
                this.searchInput.addEventListener('input', WebUtils.debounce(function() {
                    self.handleSearch(this.value);
                }, 300));
            }
            
            // Notification dropdown
            if (this.notificationBtn && this.notificationDropdown) {
                this.notificationBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    self.toggleNotificationDropdown();
                });
            }
            
            // User dropdown
            if (this.userBtn && this.userDropdown) {
                this.userBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    self.toggleUserDropdown();
                });
            }
            
            // Close dropdowns when clicking outside
            document.addEventListener('click', function() {
                self.closeDropdowns();
            });
        },
        
        handleSearch: function(query) {
            if (query.length < 2) return;
            
            // Implement search functionality
            console.log('Searching for:', query);
        },
        
        toggleNotificationDropdown: function() {
            if (this.notificationDropdown) {
                WebUtils.toggleClass(this.notificationDropdown, 'show');
                this.closeUserDropdown();
            }
        },
        
        toggleUserDropdown: function() {
            if (this.userDropdown) {
                WebUtils.toggleClass(this.userDropdown, 'show');
                this.closeNotificationDropdown();
            }
        },
        
        closeDropdowns: function() {
            if (this.notificationDropdown) {
                WebUtils.removeClass(this.notificationDropdown, 'show');
            }
            if (this.userDropdown) {
                WebUtils.removeClass(this.userDropdown, 'show');
            }
        },
        
        closeNotificationDropdown: function() {
            if (this.notificationDropdown) {
                WebUtils.removeClass(this.notificationDropdown, 'show');
            }
        },
        
        closeUserDropdown: function() {
            if (this.userDropdown) {
                WebUtils.removeClass(this.userDropdown, 'show');
            }
        }
    };

    // Menu Management
    var MenuManager = {
        init: function() {
            this.menuItems = document.querySelectorAll('.sidebar-menu .nav-link');
            this.bindEvents();
        },
        
        bindEvents: function() {
            var self = this;
            
            this.menuItems.forEach(function(item) {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    self.handleMenuClick(this);
                });
            });
        },
        
        handleMenuClick: function(item) {
            var submenu = item.parentElement.querySelector('.submenu');
            
            if (submenu) {
                // Toggle submenu
                WebUtils.toggleClass(item, 'expanded');
                WebUtils.toggleClass(submenu, 'show');
            } else {
                // Navigate to menu item
                this.navigateToMenuItem(item);
            }
        },
        
        navigateToMenuItem: function(item) {
            var href = item.getAttribute('href');
            if (href && href !== '#') {
                window.location.href = href;
            }
        }
    };

    // Initialize Web Components
    var WebInitializer = {
        init: function() {
            this.initTheme();
            this.initComponents();
            this.bindGlobalEvents();
        },
        
        initTheme: function() {
            var theme = WebUtils.getTheme();
            WebUtils.setTheme(theme);
        },
        
        initComponents: function() {
            SidebarManager.init();
            HeaderManager.init();
            MenuManager.init();
        },
        
        bindGlobalEvents: function() {
            // Handle page load
            document.addEventListener('DOMContentLoaded', function() {
                console.log('Kids Clothing ERP Web Interface Loaded');
            });
            
            // Handle page unload
            window.addEventListener('beforeunload', function() {
                // Save any pending data
            });
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            WebInitializer.init();
        });
    } else {
        WebInitializer.init();
    }

    // Export utilities for use in other modules
    return {
        WebUtils: WebUtils,
        SidebarManager: SidebarManager,
        HeaderManager: HeaderManager,
        MenuManager: MenuManager,
        WebInitializer: WebInitializer
    };
});