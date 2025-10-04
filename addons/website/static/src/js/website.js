/* Website JavaScript for Kids Clothing ERP */

// Website Management functionality
class WebsiteManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadWebsiteData();
    }
    
    bindEvents() {
        // Bind website refresh button
        $(document).on('click', '.website-refresh-btn', () => {
            this.refreshWebsiteData();
        });
        
        // Bind website preview button
        $(document).on('click', '.website-preview-btn', (e) => {
            const websiteId = $(e.currentTarget).data('website-id');
            this.previewWebsite(websiteId);
        });
        
        // Bind website analytics button
        $(document).on('click', '.website-analytics-btn', (e) => {
            const websiteId = $(e.currentTarget).data('website-id');
            this.showWebsiteAnalytics(websiteId);
        });
        
        // Bind page preview button
        $(document).on('click', '.page-preview-btn', (e) => {
            const pageId = $(e.currentTarget).data('page-id');
            this.previewPage(pageId);
        });
        
        // Bind page publish button
        $(document).on('click', '.page-publish-btn', (e) => {
            const pageId = $(e.currentTarget).data('page-id');
            this.publishPage(pageId);
        });
        
        // Bind page unpublish button
        $(document).on('click', '.page-unpublish-btn', (e) => {
            const pageId = $(e.currentTarget).data('page-id');
            this.unpublishPage(pageId);
        });
    }
    
    loadWebsiteData() {
        // Load website data via AJAX
        $.ajax({
            url: '/website/get_website_data',
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
        // Update website statistics
        $('.total-websites').text(data.total_websites);
        $('.active-websites').text(data.active_websites);
        $('.total-pages').text(data.total_pages);
        $('.published-pages').text(data.published_pages);
        
        // Update content statistics
        $('.total-content').text(data.total_content);
        $('.published-content').text(data.published_content);
        
        // Update form statistics
        $('.total-forms').text(data.total_forms);
        $('.published-forms').text(data.published_forms);
        $('.total-submissions').text(data.total_submissions);
        
        // Update analytics statistics
        $('.total-visitors').text(data.total_visitors);
        $('.total-page-views').text(data.total_page_views);
        $('.conversion-rate').text(data.conversion_rate + '%');
    }
    
    refreshWebsiteData() {
        this.loadWebsiteData();
        this.showNotification('Website data refreshed', 'success');
    }
    
    previewWebsite(websiteId) {
        // Open website preview in new window
        $.ajax({
            url: '/website/get_website_url',
            type: 'GET',
            data: { website_id: websiteId },
            success: (data) => {
                window.open(data.url, '_blank');
            },
            error: (error) => {
                this.showNotification('Error opening website preview', 'error');
            }
        });
    }
    
    showWebsiteAnalytics(websiteId) {
        // Show website analytics in a modal
        $.ajax({
            url: '/website/get_website_analytics',
            type: 'GET',
            data: { website_id: websiteId },
            success: (analyticsData) => {
                this.displayWebsiteAnalytics(analyticsData);
            },
            error: (error) => {
                this.showNotification('Error loading website analytics', 'error');
            }
        });
    }
    
    displayWebsiteAnalytics(analyticsData) {
        const modal = $(`
            <div class="modal fade" id="websiteAnalyticsModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Website Analytics - ${analyticsData.website_name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Total Visitors</h6>
                                            <h4 class="text-primary">${analyticsData.total_visitors}</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Unique Visitors</h6>
                                            <h4 class="text-info">${analyticsData.unique_visitors}</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Page Views</h6>
                                            <h4 class="text-success">${analyticsData.total_page_views}</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Bounce Rate</h6>
                                            <h4 class="text-warning">${analyticsData.bounce_rate}%</h4>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Conversion Rate</h6>
                                            <h4 class="text-success">${analyticsData.conversion_rate}%</h4>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body">
                                            <h6 class="card-title">Total Revenue</h6>
                                            <h4 class="text-primary">${this.formatCurrency(analyticsData.total_revenue)}</h4>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
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
    
    previewPage(pageId) {
        // Open page preview in new window
        $.ajax({
            url: '/website/get_page_url',
            type: 'GET',
            data: { page_id: pageId },
            success: (data) => {
                window.open(data.url, '_blank');
            },
            error: (error) => {
                this.showNotification('Error opening page preview', 'error');
            }
        });
    }
    
    publishPage(pageId) {
        if (confirm('Are you sure you want to publish this page?')) {
            $.ajax({
                url: '/website/publish_page',
                type: 'POST',
                data: { page_id: pageId },
                success: (response) => {
                    this.showNotification('Page published successfully', 'success');
                    this.loadWebsiteData();
                },
                error: (error) => {
                    this.showNotification('Error publishing page', 'error');
                }
            });
        }
    }
    
    unpublishPage(pageId) {
        if (confirm('Are you sure you want to unpublish this page?')) {
            $.ajax({
                url: '/website/unpublish_page',
                type: 'POST',
                data: { page_id: pageId },
                success: (response) => {
                    this.showNotification('Page unpublished successfully', 'success');
                    this.loadWebsiteData();
                },
                error: (error) => {
                    this.showNotification('Error unpublishing page', 'error');
                }
            });
        }
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="website-notification website-notification-${type} website-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Content Management functionality
class ContentManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind content preview button
        $(document).on('click', '.content-preview-btn', (e) => {
            const contentId = $(e.currentTarget).data('content-id');
            this.previewContent(contentId);
        });
        
        // Bind content publish button
        $(document).on('click', '.content-publish-btn', (e) => {
            const contentId = $(e.currentTarget).data('content-id');
            this.publishContent(contentId);
        });
        
        // Bind content unpublish button
        $(document).on('click', '.content-unpublish-btn', (e) => {
            const contentId = $(e.currentTarget).data('content-id');
            this.unpublishContent(contentId);
        });
        
        // Bind gallery preview button
        $(document).on('click', '.gallery-preview-btn', (e) => {
            const galleryId = $(e.currentTarget).data('gallery-id');
            this.previewGallery(galleryId);
        });
    }
    
    previewContent(contentId) {
        // Open content preview in new window
        $.ajax({
            url: '/website/get_content_preview_url',
            type: 'GET',
            data: { content_id: contentId },
            success: (data) => {
                window.open(data.url, '_blank');
            },
            error: (error) => {
                this.showNotification('Error opening content preview', 'error');
            }
        });
    }
    
    publishContent(contentId) {
        if (confirm('Are you sure you want to publish this content?')) {
            $.ajax({
                url: '/website/publish_content',
                type: 'POST',
                data: { content_id: contentId },
                success: (response) => {
                    this.showNotification('Content published successfully', 'success');
                },
                error: (error) => {
                    this.showNotification('Error publishing content', 'error');
                }
            });
        }
    }
    
    unpublishContent(contentId) {
        if (confirm('Are you sure you want to unpublish this content?')) {
            $.ajax({
                url: '/website/unpublish_content',
                type: 'POST',
                data: { content_id: contentId },
                success: (response) => {
                    this.showNotification('Content unpublished successfully', 'success');
                },
                error: (error) => {
                    this.showNotification('Error unpublishing content', 'error');
                }
            });
        }
    }
    
    previewGallery(galleryId) {
        // Open gallery preview in new window
        $.ajax({
            url: '/website/get_gallery_preview_url',
            type: 'GET',
            data: { gallery_id: galleryId },
            success: (data) => {
                window.open(data.url, '_blank');
            },
            error: (error) => {
                this.showNotification('Error opening gallery preview', 'error');
            }
        });
    }
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="website-notification website-notification-${type} website-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Form Management functionality
class FormManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Bind form preview button
        $(document).on('click', '.form-preview-btn', (e) => {
            const formId = $(e.currentTarget).data('form-id');
            this.previewForm(formId);
        });
        
        // Bind form publish button
        $(document).on('click', '.form-publish-btn', (e) => {
            const formId = $(e.currentTarget).data('form-id');
            this.publishForm(formId);
        });
        
        // Bind form unpublish button
        $(document).on('click', '.form-unpublish-btn', (e) => {
            const formId = $(e.currentTarget).data('form-id');
            this.unpublishForm(formId);
        });
        
        // Bind form submissions button
        $(document).on('click', '.form-submissions-btn', (e) => {
            const formId = $(e.currentTarget).data('form-id');
            this.showFormSubmissions(formId);
        });
    }
    
    previewForm(formId) {
        // Open form preview in new window
        $.ajax({
            url: '/website/get_form_preview_url',
            type: 'GET',
            data: { form_id: formId },
            success: (data) => {
                window.open(data.url, '_blank');
            },
            error: (error) => {
                this.showNotification('Error opening form preview', 'error');
            }
        });
    }
    
    publishForm(formId) {
        if (confirm('Are you sure you want to publish this form?')) {
            $.ajax({
                url: '/website/publish_form',
                type: 'POST',
                data: { form_id: formId },
                success: (response) => {
                    this.showNotification('Form published successfully', 'success');
                },
                error: (error) => {
                    this.showNotification('Error publishing form', 'error');
                }
            });
        }
    }
    
    unpublishForm(formId) {
        if (confirm('Are you sure you want to unpublish this form?')) {
            $.ajax({
                url: '/website/unpublish_form',
                type: 'POST',
                data: { form_id: formId },
                success: (response) => {
                    this.showNotification('Form unpublished successfully', 'success');
                },
                error: (error) => {
                    this.showNotification('Error unpublishing form', 'error');
                }
            });
        }
    }
    
    showFormSubmissions(formId) {
        // Show form submissions in a modal
        $.ajax({
            url: '/website/get_form_submissions',
            type: 'GET',
            data: { form_id: formId },
            success: (submissionsData) => {
                this.displayFormSubmissions(submissionsData);
            },
            error: (error) => {
                this.showNotification('Error loading form submissions', 'error');
            }
        });
    }
    
    displayFormSubmissions(submissionsData) {
        const modal = $(`
            <div class="modal fade" id="formSubmissionsModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Form Submissions - ${submissionsData.form_name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Email</th>
                                            <th>Phone</th>
                                            <th>Date</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${submissionsData.submissions.map(submission => `
                                            <tr>
                                                <td>${submission.contact_name}</td>
                                                <td>${submission.contact_email}</td>
                                                <td>${submission.contact_phone}</td>
                                                <td>${submission.create_date}</td>
                                                <td><span class="badge bg-${submission.state === 'new' ? 'primary' : submission.state === 'processed' ? 'success' : submission.state === 'replied' ? 'info' : 'secondary'}">${submission.state}</span></td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
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
    
    showNotification(message, type = 'info') {
        const notification = $(`
            <div class="website-notification website-notification-${type} website-fade-in">
                ${message}
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize website components when document is ready
$(document).ready(function() {
    // Initialize website manager if element exists
    if ($('.website-management').length) {
        new WebsiteManager();
    }
    
    // Initialize content manager if element exists
    if ($('.content-management').length) {
        new ContentManager();
    }
    
    // Initialize form manager if element exists
    if ($('.form-management').length) {
        new FormManager();
    }
});