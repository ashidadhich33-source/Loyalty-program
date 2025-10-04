// Ocean ERP - Indian GST JavaScript

// GST Tax Manager
class GstTaxManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadGstTaxData();
    }
    
    bindEvents() {
        // HSN code validation
        document.addEventListener('DOMContentLoaded', () => {
            const hsnInputs = document.querySelectorAll('input[name="hsn_code"]');
            hsnInputs.forEach(input => {
                input.addEventListener('blur', this.validateHSN.bind(this));
            });
            
            // SAC code validation
            const sacInputs = document.querySelectorAll('input[name="sac_code"]');
            sacInputs.forEach(input => {
                input.addEventListener('blur', this.validateSAC.bind(this));
            });
            
            // GST rate calculation
            const amountInputs = document.querySelectorAll('input[name="amount"]');
            amountInputs.forEach(input => {
                input.addEventListener('input', this.calculateGstRate.bind(this));
            });
        });
    }
    
    validateHSN(event) {
        const hsn = event.target.value;
        const hsnPattern = /^[0-9]{4,8}$/;
        
        if (hsn && !hsnPattern.test(hsn)) {
            this.showError(event.target, 'Invalid HSN code. Should be 4-8 digits.');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateSAC(event) {
        const sac = event.target.value;
        const sacPattern = /^[0-9]{6}$/;
        
        if (sac && !sacPattern.test(sac)) {
            this.showError(event.target, 'Invalid SAC code. Should be 6 digits.');
        } else {
            this.clearError(event.target);
        }
    }
    
    calculateGstRate(event) {
        const amount = parseFloat(event.target.value) || 0;
        const gstRateField = event.target.closest('form').querySelector('input[name="gst_rate"]');
        
        if (gstRateField) {
            gstRateField.value = amount;
        }
    }
    
    showError(input, message) {
        this.clearError(input);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#dc3545';
        errorDiv.style.fontSize = '12px';
        errorDiv.style.marginTop = '5px';
        input.parentNode.appendChild(errorDiv);
        input.style.borderColor = '#dc3545';
    }
    
    clearError(input) {
        const existingError = input.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        input.style.borderColor = '';
    }
    
    loadGstTaxData() {
        // Load GST tax data for dashboard
        fetch('/api/gst/tax-data')
            .then(response => response.json())
            .then(data => {
                this.updateGstTaxDashboard(data);
            })
            .catch(error => {
                console.error('Error loading GST tax data:', error);
            });
    }
    
    updateGstTaxDashboard(data) {
        const dashboard = document.querySelector('.gst-tax-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateGstTaxHTML(data);
        }
    }
    
    generateGstTaxHTML(data) {
        return `
            <div class="gst-dashboard-grid">
                <div class="gst-dashboard-card">
                    <h4>CGST Taxes</h4>
                    <div class="amount">${data.cgstCount}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>SGST Taxes</h4>
                    <div class="amount">${data.sgstCount}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>IGST Taxes</h4>
                    <div class="amount">${data.igstCount}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>CESS Taxes</h4>
                    <div class="amount">${data.cessCount}</div>
                </div>
            </div>
            <div class="kids-clothing-gst-info">
                <h4>Kids Clothing GST Distribution</h4>
                <div class="kids-clothing-gst-badges">
                    ${this.generateKidsClothingGstBadges(data.kidsClothingData)}
                </div>
            </div>
        `;
    }
    
    generateKidsClothingGstBadges(data) {
        return Object.entries(data).map(([key, value]) => 
            `<span class="gst-type-badge gst-type-${key}">${key.toUpperCase()}: ${value}</span>`
        ).join('');
    }
}

// GST Return Manager
class GstReturnManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadGstReturnData();
    }
    
    bindEvents() {
        // Return period validation
        document.addEventListener('DOMContentLoaded', () => {
            const periodInputs = document.querySelectorAll('input[name="return_period"]');
            periodInputs.forEach(input => {
                input.addEventListener('blur', this.validateReturnPeriod.bind(this));
            });
        });
    }
    
    validateReturnPeriod(event) {
        const period = event.target.value;
        const periodPattern = /^[0-9]{6}$/;
        
        if (period && !periodPattern.test(period)) {
            this.showError(event.target, 'Invalid return period. Format: YYYYMM');
        } else {
            this.clearError(event.target);
        }
    }
    
    showError(input, message) {
        this.clearError(input);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#dc3545';
        errorDiv.style.fontSize = '12px';
        errorDiv.style.marginTop = '5px';
        input.parentNode.appendChild(errorDiv);
        input.style.borderColor = '#dc3545';
    }
    
    clearError(input) {
        const existingError = input.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        input.style.borderColor = '';
    }
    
    loadGstReturnData() {
        // Load GST return data for dashboard
        fetch('/api/gst/return-data')
            .then(response => response.json())
            .then(data => {
                this.updateGstReturnDashboard(data);
            })
            .catch(error => {
                console.error('Error loading GST return data:', error);
            });
    }
    
    updateGstReturnDashboard(data) {
        const dashboard = document.querySelector('.gst-return-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateGstReturnHTML(data);
        }
    }
    
    generateGstReturnHTML(data) {
        return `
            <div class="gst-dashboard-grid">
                <div class="gst-dashboard-card">
                    <h4>GSTR-1</h4>
                    <div class="amount">${data.gstr1Count}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>GSTR-2</h4>
                    <div class="amount">${data.gstr2Count}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>GSTR-3</h4>
                    <div class="amount">${data.gstr3Count}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>GSTR-4</h4>
                    <div class="amount">${data.gstr4Count}</div>
                </div>
            </div>
            <div class="gst-return-status">
                <span class="gst-return-status gst-return-draft">Draft: ${data.draftCount}</span>
                <span class="gst-return-status gst-return-ready">Ready: ${data.readyCount}</span>
                <span class="gst-return-status gst-return-filed">Filed: ${data.filedCount}</span>
                <span class="gst-return-status gst-return-accepted">Accepted: ${data.acceptedCount}</span>
            </div>
        `;
    }
}

// GST Report Manager
class GstReportManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadGstReportData();
    }
    
    bindEvents() {
        // Date range validation
        document.addEventListener('DOMContentLoaded', () => {
            const dateFromInputs = document.querySelectorAll('input[name="date_from"]');
            const dateToInputs = document.querySelectorAll('input[name="date_to"]');
            
            dateFromInputs.forEach(input => {
                input.addEventListener('change', this.validateDateRange.bind(this));
            });
            
            dateToInputs.forEach(input => {
                input.addEventListener('change', this.validateDateRange.bind(this));
            });
        });
    }
    
    validateDateRange(event) {
        const form = event.target.closest('form');
        const dateFrom = form.querySelector('input[name="date_from"]');
        const dateTo = form.querySelector('input[name="date_to"]');
        
        if (dateFrom.value && dateTo.value) {
            const fromDate = new Date(dateFrom.value);
            const toDate = new Date(dateTo.value);
            
            if (fromDate > toDate) {
                this.showError(dateTo, 'To date must be after from date');
            } else {
                this.clearError(dateTo);
            }
        }
    }
    
    showError(input, message) {
        this.clearError(input);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#dc3545';
        errorDiv.style.fontSize = '12px';
        errorDiv.style.marginTop = '5px';
        input.parentNode.appendChild(errorDiv);
        input.style.borderColor = '#dc3545';
    }
    
    clearError(input) {
        const existingError = input.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        input.style.borderColor = '';
    }
    
    loadGstReportData() {
        // Load GST report data for dashboard
        fetch('/api/gst/report-data')
            .then(response => response.json())
            .then(data => {
                this.updateGstReportDashboard(data);
            })
            .catch(error => {
                console.error('Error loading GST report data:', error);
            });
    }
    
    updateGstReportDashboard(data) {
        const dashboard = document.querySelector('.gst-report-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateGstReportHTML(data);
        }
    }
    
    generateGstReportHTML(data) {
        return `
            <div class="gst-dashboard-grid">
                <div class="gst-dashboard-card">
                    <h4>GST Summary</h4>
                    <div class="amount">${data.summaryCount}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>GST Liability</h4>
                    <div class="amount">${data.liabilityCount}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>GST Input Tax</h4>
                    <div class="amount">${data.inputTaxCount}</div>
                </div>
                <div class="gst-dashboard-card">
                    <h4>GST Output Tax</h4>
                    <div class="amount">${data.outputTaxCount}</div>
                </div>
            </div>
            <div class="gst-report-status">
                <span class="gst-report-type gst-report-summary">Summary: ${data.summaryCount}</span>
                <span class="gst-report-type gst-report-liability">Liability: ${data.liabilityCount}</span>
                <span class="gst-report-type gst-report-input">Input Tax: ${data.inputTaxCount}</span>
                <span class="gst-report-type gst-report-output">Output Tax: ${data.outputTaxCount}</span>
            </div>
        `;
    }
}

// GST Calculation Utility
class GstCalculationUtility {
    static calculateGst(baseAmount, gstRate) {
        const gstAmount = baseAmount * (gstRate / 100);
        const totalAmount = baseAmount + gstAmount;
        
        return {
            baseAmount: baseAmount,
            gstAmount: gstAmount,
            totalAmount: totalAmount,
            gstRate: gstRate
        };
    }
    
    static calculateGstBreakdown(baseAmount, gstRate, isInterState = false) {
        const gstAmount = baseAmount * (gstRate / 100);
        
        if (isInterState) {
            return {
                baseAmount: baseAmount,
                igst: gstAmount,
                cgst: 0,
                sgst: 0,
                cess: 0,
                totalAmount: baseAmount + gstAmount
            };
        } else {
            const cgst = gstAmount / 2;
            const sgst = gstAmount / 2;
            
            return {
                baseAmount: baseAmount,
                igst: 0,
                cgst: cgst,
                sgst: sgst,
                cess: 0,
                totalAmount: baseAmount + gstAmount
            };
        }
    }
    
    static formatGstAmount(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }).format(amount);
    }
}

// GST Portal Integration
class GstPortalIntegration {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.checkPortalStatus();
    }
    
    bindEvents() {
        // Portal status check
        document.addEventListener('DOMContentLoaded', () => {
            const statusButton = document.querySelector('.gst-portal-status-check');
            if (statusButton) {
                statusButton.addEventListener('click', this.checkPortalStatus.bind(this));
            }
        });
    }
    
    checkPortalStatus() {
        fetch('/api/gst/portal-status')
            .then(response => response.json())
            .then(data => {
                this.updatePortalStatus(data);
            })
            .catch(error => {
                console.error('Error checking portal status:', error);
            });
    }
    
    updatePortalStatus(data) {
        const statusElement = document.querySelector('.gst-portal-status');
        if (statusElement) {
            statusElement.className = `gst-portal-status gst-portal-${data.status}`;
            statusElement.textContent = data.message;
        }
    }
}

// Initialize managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GstTaxManager();
    new GstReturnManager();
    new GstReportManager();
    new GstPortalIntegration();
});

// Utility functions
function formatGstAmount(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatGstDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function validateGstin(gstin) {
    const gstinPattern = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$/;
    return gstinPattern.test(gstin);
}

function validateHsnCode(hsn) {
    const hsnPattern = /^[0-9]{4,8}$/;
    return hsnPattern.test(hsn);
}

function validateSacCode(sac) {
    const sacPattern = /^[0-9]{6}$/;
    return sacPattern.test(sac);
}

// Export for use in other modules
window.IndianGST = {
    GstTaxManager,
    GstReturnManager,
    GstReportManager,
    GstCalculationUtility,
    GstPortalIntegration,
    formatGstAmount,
    formatGstDate,
    validateGstin,
    validateHsnCode,
    validateSacCode
};