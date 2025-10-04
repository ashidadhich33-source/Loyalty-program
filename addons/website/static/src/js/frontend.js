/* Frontend JavaScript for Kids Clothing Website */

// Website Frontend functionality
class WebsiteFrontend {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadWebsiteData();
        this.initAnalytics();
    }
    
    bindEvents() {
        // Bind newsletter subscription
        $(document).on('submit', '.newsletter-signup form', (e) => {
            e.preventDefault();
            this.subscribeNewsletter(e.target);
        });
        
        // Bind contact form submission
        $(document).on('submit', '.contact-form form', (e) => {
            e.preventDefault();
            this.submitContactForm(e.target);
        });
        
        // Bind product inquiry form submission
        $(document).on('submit', '.product-inquiry-form', (e) => {
            e.preventDefault();
            this.submitProductInquiry(e.target);
        });
        
        // Bind search functionality
        $(document).on('submit', '.search-form', (e) => {
            e.preventDefault();
            this.performSearch(e.target);
        });
        
        // Bind mobile menu toggle
        $(document).on('click', '.mobile-menu-toggle', () => {
            this.toggleMobileMenu();
        });
        
        // Bind smooth scrolling for anchor links
        $(document).on('click', 'a[href^="#"]', (e) => {
            e.preventDefault();
            this.smoothScroll(e.target.getAttribute('href'));
        });
    }
    
    loadWebsiteData() {
        // Load website data via API
        $.ajax({
            url: '/api/website/data',
            type: 'GET',
            success: (data) => {
                this.updateWebsiteData(data);
            },
            error: (error) => {
                console.error('Error loading website data:', error);
            }
        });
    }
    
    updateWebsiteData(data) {
        // Update website title
        if (data.meta_title) {
            document.title = data.meta_title;
        }
        
        // Update meta description
        if (data.meta_description) {
            $('meta[name="description"]').attr('content', data.meta_description);
        }
        
        // Update contact information
        if (data.contact_email) {
            $('.contact-email').text(data.contact_email);
        }
        
        if (data.contact_phone) {
            $('.contact-phone').text(data.contact_phone);
        }
        
        if (data.contact_address) {
            $('.contact-address').text(data.contact_address);
        }
        
        // Update social media links
        if (data.social_media) {
            if (data.social_media.facebook) {
                $('.social-facebook').attr('href', data.social_media.facebook);
            }
            if (data.social_media.instagram) {
                $('.social-instagram').attr('href', data.social_media.instagram);
            }
            if (data.social_media.twitter) {
                $('.social-twitter').attr('href', data.social_media.twitter);
            }
            if (data.social_media.youtube) {
                $('.social-youtube').attr('href', data.social_media.youtube);
            }
        }
    }
    
    initAnalytics() {
        // Initialize Google Analytics if available
        if (window.gtag) {
            this.trackPageView();
        }
        
        // Initialize Facebook Pixel if available
        if (window.fbq) {
            this.trackPageView();
        }
        
        // Track visitor
        this.trackVisitor();
    }
    
    trackPageView() {
        // Track page view
        $.ajax({
            url: '/api/website/track',
            type: 'POST',
            data: JSON.stringify({
                website_id: this.getWebsiteId(),
                page_id: this.getPageId(),
                visitor_id: this.getVisitorId(),
                country: this.getCountry(),
                state: this.getState(),
                city: this.getCity(),
                device_type: this.getDeviceType(),
                browser: this.getBrowser(),
                operating_system: this.getOperatingSystem(),
                traffic_source: this.getTrafficSource(),
                referrer_url: document.referrer
            }),
            contentType: 'application/json',
            success: (response) => {
                console.log('Page view tracked');
            },
            error: (error) => {
                console.error('Error tracking page view:', error);
            }
        });
    }
    
    trackVisitor() {
        // Track visitor information
        const visitorData = {
            website_id: this.getWebsiteId(),
            visitor_id: this.getVisitorId(),
            country: this.getCountry(),
            state: this.getState(),
            city: this.getCity(),
            device_type: this.getDeviceType(),
            browser: this.getBrowser(),
            operating_system: this.getOperatingSystem()
        };
        
        // Store visitor data in localStorage
        localStorage.setItem('visitor_data', JSON.stringify(visitorData));
    }
    
    subscribeNewsletter(form) {
        const email = $(form).find('input[name="email"]').val();
        
        if (!email) {
            this.showNotification('Please enter your email address', 'error');
            return;
        }
        
        $.ajax({
            url: '/newsletter/subscribe',
            type: 'POST',
            data: { email: email },
            success: (response) => {
                this.showNotification('Thank you for subscribing!', 'success');
                $(form)[0].reset();
            },
            error: (error) => {
                this.showNotification('Error subscribing to newsletter', 'error');
            }
        });
    }
    
    submitContactForm(form) {
        const formData = new FormData(form);
        
        $.ajax({
            url: '/form/submit',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                this.showNotification('Thank you for your message! We\'ll get back to you soon.', 'success');
                form.reset();
            },
            error: (error) => {
                this.showNotification('Error sending message', 'error');
            }
        });
    }
    
    submitProductInquiry(form) {
        const formData = new FormData(form);
        
        $.ajax({
            url: '/form/submit',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                this.showNotification('Thank you for your inquiry! We\'ll get back to you soon.', 'success');
                form.reset();
            },
            error: (error) => {
                this.showNotification('Error sending inquiry', 'error');
            }
        });
    }
    
    performSearch(form) {
        const query = $(form).find('input[name="q"]').val();
        
        if (!query) {
            this.showNotification('Please enter a search term', 'error');
            return;
        }
        
        window.location.href = `/search?q=${encodeURIComponent(query)}`;
    }
    
    toggleMobileMenu() {
        $('.nav-menu').toggleClass('mobile-open');
        $('.mobile-menu-toggle').toggleClass('active');
    }
    
    smoothScroll(target) {
        const element = $(target);
        if (element.length) {
            $('html, body').animate({
                scrollTop: element.offset().top - 100
            }, 800);
        }
    }
    
    getWebsiteId() {
        return $('meta[name="website-id"]').attr('content') || '1';
    }
    
    getPageId() {
        return $('meta[name="page-id"]').attr('content') || null;
    }
    
    getVisitorId() {
        let visitorId = localStorage.getItem('visitor_id');
        if (!visitorId) {
            visitorId = 'visitor_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('visitor_id', visitorId);
        }
        return visitorId;
    }
    
    getCountry() {
        // This would be determined by IP geolocation
        return 'India';
    }
    
    getState() {
        // This would be determined by IP geolocation
        return 'Maharashtra';
    }
    
    getCity() {
        // This would be determined by IP geolocation
        return 'Mumbai';
    }
    
    getDeviceType() {
        const width = window.innerWidth;
        if (width < 768) {
            return 'mobile';
        } else if (width < 1024) {
            return 'tablet';
        } else {
            return 'desktop';
        }
    }
    
    getBrowser() {
        const userAgent = navigator.userAgent;
        if (userAgent.includes('Chrome')) {
            return 'Chrome';
        } else if (userAgent.includes('Firefox')) {
            return 'Firefox';
        } else if (userAgent.includes('Safari')) {
            return 'Safari';
        } else if (userAgent.includes('Edge')) {
            return 'Edge';
        } else {
            return 'Other';
        }
    }
    
    getOperatingSystem() {
        const userAgent = navigator.userAgent;
        if (userAgent.includes('Windows')) {
            return 'Windows';
        } else if (userAgent.includes('Mac')) {
            return 'macOS';
        } else if (userAgent.includes('Linux')) {
            return 'Linux';
        } else if (userAgent.includes('Android')) {
            return 'Android';
        } else if (userAgent.includes('iOS')) {
            return 'iOS';
        } else {
            return 'Other';
        }
    }
    
    getTrafficSource() {
        const referrer = document.referrer;
        if (!referrer) {
            return 'direct';
        } else if (referrer.includes('google') || referrer.includes('bing') || referrer.includes('yahoo')) {
            return 'search';
        } else if (referrer.includes('facebook') || referrer.includes('instagram') || referrer.includes('twitter')) {
            return 'social';
        } else {
            return 'referral';
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="notification notification-${type} notification-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Product functionality
class ProductManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadProducts();
    }
    
    bindEvents() {
        // Bind product filter
        $(document).on('change', '.product-filter', (e) => {
            this.filterProducts(e.target.value);
        });
        
        // Bind product search
        $(document).on('input', '.product-search', (e) => {
            this.searchProducts(e.target.value);
        });
        
        // Bind product inquiry
        $(document).on('click', '.product-inquiry-btn', (e) => {
            const productId = $(e.currentTarget).data('product-id');
            this.showProductInquiry(productId);
        });
    }
    
    loadProducts() {
        // Load products via API
        $.ajax({
            url: '/api/products',
            type: 'GET',
            success: (data) => {
                this.displayProducts(data);
            },
            error: (error) => {
                console.error('Error loading products:', error);
            }
        });
    }
    
    displayProducts(products) {
        const productGrid = $('.product-grid');
        productGrid.empty();
        
        products.forEach(product => {
            const productItem = $(`
                <div class="product-item" data-product-id="${product.id}">
                    <img src="${product.image_url}" alt="${product.name}">
                    <h3>${product.name}</h3>
                    <p>${product.description}</p>
                    <span class="price">${this.formatCurrency(product.price)}</span>
                    <button class="btn btn-primary product-inquiry-btn" data-product-id="${product.id}">Inquiry</button>
                </div>
            `);
            productGrid.append(productItem);
        });
    }
    
    filterProducts(filter) {
        // Filter products based on selected filter
        $('.product-item').each(function() {
            const product = $(this);
            const productCategory = product.data('category');
            
            if (filter === 'all' || productCategory === filter) {
                product.show();
            } else {
                product.hide();
            }
        });
    }
    
    searchProducts(query) {
        // Search products based on query
        $('.product-item').each(function() {
            const product = $(this);
            const productName = product.find('h3').text().toLowerCase();
            const productDescription = product.find('p').text().toLowerCase();
            
            if (productName.includes(query.toLowerCase()) || productDescription.includes(query.toLowerCase())) {
                product.show();
            } else {
                product.hide();
            }
        });
    }
    
    showProductInquiry(productId) {
        // Show product inquiry form
        const modal = $(`
            <div class="modal fade" id="productInquiryModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Product Inquiry</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form class="product-inquiry-form">
                                <input type="hidden" name="form_id" value="product_inquiry">
                                <input type="hidden" name="product_id" value="${productId}">
                                <div class="mb-3">
                                    <label class="form-label">Full Name</label>
                                    <input type="text" class="form-control" name="name" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Email Address</label>
                                    <input type="email" class="form-control" name="email" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Phone Number</label>
                                    <input type="tel" class="form-control" name="phone">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Message</label>
                                    <textarea class="form-control" name="message" rows="4" required></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary">Send Inquiry</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        $('body').append(modal);
        modal.modal('show');
        
        modal.on('hidden.bs.modal', function() {
            modal.remove();
        });
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
}

// Initialize frontend components when document is ready
$(document).ready(function() {
    // Initialize website frontend
    new WebsiteFrontend();
    
    // Initialize product manager if element exists
    if ($('.product-grid').length) {
        new ProductManager();
    }
});