// Ocean ERP - Indian EDI JavaScript

// EDI Document Manager
class EdiDocumentManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadEdiDocumentData();
    }
    
    bindEvents() {
        // Document type validation
        document.addEventListener('DOMContentLoaded', () => {
            const documentTypeInputs = document.querySelectorAll('select[name="document_type"]');
            documentTypeInputs.forEach(input => {
                input.addEventListener('change', this.validateDocumentType.bind(this));
            });
            
            // EDI format validation
            const ediFormatInputs = document.querySelectorAll('select[name="edi_format"]');
            ediFormatInputs.forEach(input => {
                input.addEventListener('change', this.validateEdiFormat.bind(this));
            });
            
            // Document date validation
            const documentDateInputs = document.querySelectorAll('input[name="document_date"]');
            documentDateInputs.forEach(input => {
                input.addEventListener('blur', this.validateDocumentDate.bind(this));
            });
        });
    }
    
    validateDocumentType(event) {
        const documentType = event.target.value;
        const validTypes = ['invoice', 'credit_note', 'debit_note', 'purchase_order', 'sales_order', 'delivery_note', 'receipt', 'payment', 'remittance', 'other'];
        
        if (documentType && !validTypes.includes(documentType)) {
            this.showError(event.target, 'Invalid document type');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateEdiFormat(event) {
        const ediFormat = event.target.value;
        const validFormats = ['edifact', 'x12', 'xml', 'json', 'csv', 'custom'];
        
        if (ediFormat && !validFormats.includes(ediFormat)) {
            this.showError(event.target, 'Invalid EDI format');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateDocumentDate(event) {
        const documentDate = event.target.value;
        const date = new Date(documentDate);
        const today = new Date();
        
        if (documentDate && date > today) {
            this.showError(event.target, 'Document date cannot be in the future');
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
    
    loadEdiDocumentData() {
        // Load EDI document data for dashboard
        fetch('/api/edi/document-data')
            .then(response => response.json())
            .then(data => {
                this.updateEdiDocumentDashboard(data);
            })
            .catch(error => {
                console.error('Error loading EDI document data:', error);
            });
    }
    
    updateEdiDocumentDashboard(data) {
        const dashboard = document.querySelector('.edi-document-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateEdiDocumentHTML(data);
        }
    }
    
    generateEdiDocumentHTML(data) {
        return `
            <div class="edi-dashboard-grid">
                <div class="edi-dashboard-card">
                    <h4>Invoices</h4>
                    <div class="count">${data.invoiceCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>Credit Notes</h4>
                    <div class="count">${data.creditNoteCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>Debit Notes</h4>
                    <div class="count">${data.debitNoteCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>Purchase Orders</h4>
                    <div class="count">${data.purchaseOrderCount}</div>
                </div>
            </div>
            <div class="kids-clothing-edi-info">
                <h4>Kids Clothing EDI Distribution</h4>
                <div class="kids-clothing-edi-badges">
                    ${this.generateKidsClothingEdiBadges(data.kidsClothingData)}
                </div>
            </div>
        `;
    }
    
    generateKidsClothingEdiBadges(data) {
        return Object.entries(data).map(([key, value]) => 
            `<span class="edi-document-type-badge edi-document-${key}">${key.replace('_', ' ').toUpperCase()}: ${value}</span>`
        ).join('');
    }
}

// EDI Message Manager
class EdiMessageManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadEdiMessageData();
    }
    
    bindEvents() {
        // Message type validation
        document.addEventListener('DOMContentLoaded', () => {
            const messageTypeInputs = document.querySelectorAll('select[name="message_type"]');
            messageTypeInputs.forEach(input => {
                input.addEventListener('change', this.validateMessageType.bind(this));
            });
            
            // Message format validation
            const messageFormatInputs = document.querySelectorAll('select[name="message_format"]');
            messageFormatInputs.forEach(input => {
                input.addEventListener('change', this.validateMessageFormat.bind(this));
            });
        });
    }
    
    validateMessageType(event) {
        const messageType = event.target.value;
        const validTypes = ['ordrsp', 'ordrpt', 'desadv', 'invoic', 'cremte', 'debmte', 'remadv', 'paymul', 'other'];
        
        if (messageType && !validTypes.includes(messageType)) {
            this.showError(event.target, 'Invalid message type');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateMessageFormat(event) {
        const messageFormat = event.target.value;
        const validFormats = ['edifact', 'x12', 'xml', 'json', 'csv', 'custom'];
        
        if (messageFormat && !validFormats.includes(messageFormat)) {
            this.showError(event.target, 'Invalid message format');
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
    
    loadEdiMessageData() {
        // Load EDI message data for dashboard
        fetch('/api/edi/message-data')
            .then(response => response.json())
            .then(data => {
                this.updateEdiMessageDashboard(data);
            })
            .catch(error => {
                console.error('Error loading EDI message data:', error);
            });
    }
    
    updateEdiMessageDashboard(data) {
        const dashboard = document.querySelector('.edi-message-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateEdiMessageHTML(data);
        }
    }
    
    generateEdiMessageHTML(data) {
        return `
            <div class="edi-dashboard-grid">
                <div class="edi-dashboard-card">
                    <h4>ORDERS Response</h4>
                    <div class="count">${data.ordrspCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>ORDERS Report</h4>
                    <div class="count">${data.ordrptCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>DESADV</h4>
                    <div class="count">${data.desadvCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>INVOIC</h4>
                    <div class="count">${data.invoicCount}</div>
                </div>
            </div>
            <div class="edi-message-status">
                <span class="edi-status-badge edi-status-draft">Draft: ${data.draftCount}</span>
                <span class="edi-status-badge edi-status-ready">Ready: ${data.readyCount}</span>
                <span class="edi-status-badge edi-status-sent">Sent: ${data.sentCount}</span>
                <span class="edi-status-badge edi-status-received">Received: ${data.receivedCount}</span>
                <span class="edi-status-badge edi-status-processed">Processed: ${data.processedCount}</span>
            </div>
        `;
    }
}

// EDI Transmission Manager
class EdiTransmissionManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadEdiTransmissionData();
    }
    
    bindEvents() {
        // Protocol validation
        document.addEventListener('DOMContentLoaded', () => {
            const protocolInputs = document.querySelectorAll('select[name="protocol"]');
            protocolInputs.forEach(input => {
                input.addEventListener('change', this.validateProtocol.bind(this));
            });
            
            // Host validation
            const hostInputs = document.querySelectorAll('input[name="host"]');
            hostInputs.forEach(input => {
                input.addEventListener('blur', this.validateHost.bind(this));
            });
            
            // Port validation
            const portInputs = document.querySelectorAll('input[name="port"]');
            portInputs.forEach(input => {
                input.addEventListener('blur', this.validatePort.bind(this));
            });
        });
    }
    
    validateProtocol(event) {
        const protocol = event.target.value;
        const validProtocols = ['ftp', 'sftp', 'http', 'https', 'as2', 'email', 'api', 'other'];
        
        if (protocol && !validProtocols.includes(protocol)) {
            this.showError(event.target, 'Invalid protocol');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateHost(event) {
        const host = event.target.value;
        const hostPattern = /^[a-zA-Z0-9.-]+$/;
        
        if (host && !hostPattern.test(host)) {
            this.showError(event.target, 'Invalid host format');
        } else {
            this.clearError(event.target);
        }
    }
    
    validatePort(event) {
        const port = parseInt(event.target.value);
        
        if (event.target.value && (isNaN(port) || port < 1 || port > 65535)) {
            this.showError(event.target, 'Port must be between 1 and 65535');
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
    
    loadEdiTransmissionData() {
        // Load EDI transmission data for dashboard
        fetch('/api/edi/transmission-data')
            .then(response => response.json())
            .then(data => {
                this.updateEdiTransmissionDashboard(data);
            })
            .catch(error => {
                console.error('Error loading EDI transmission data:', error);
            });
    }
    
    updateEdiTransmissionDashboard(data) {
        const dashboard = document.querySelector('.edi-transmission-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateEdiTransmissionHTML(data);
        }
    }
    
    generateEdiTransmissionHTML(data) {
        return `
            <div class="edi-dashboard-grid">
                <div class="edi-dashboard-card">
                    <h4>FTP</h4>
                    <div class="count">${data.ftpCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>SFTP</h4>
                    <div class="count">${data.sftpCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>HTTP</h4>
                    <div class="count">${data.httpCount}</div>
                </div>
                <div class="edi-dashboard-card">
                    <h4>HTTPS</h4>
                    <div class="count">${data.httpsCount}</div>
                </div>
            </div>
            <div class="edi-transmission-status">
                <span class="edi-status-badge edi-status-draft">Draft: ${data.draftCount}</span>
                <span class="edi-status-badge edi-status-ready">Ready: ${data.readyCount}</span>
                <span class="edi-status-badge edi-status-sending">Sending: ${data.sendingCount}</span>
                <span class="edi-status-badge edi-status-sent">Sent: ${data.sentCount}</span>
                <span class="edi-status-badge edi-status-received">Received: ${data.receivedCount}</span>
                <span class="edi-status-badge edi-status-processed">Processed: ${data.processedCount}</span>
            </div>
        `;
    }
}

// EDI Validation Utility
class EdiValidationUtility {
    static validateEdiData(data, format) {
        const errors = [];
        
        if (!data) {
            errors.push('EDI data is required');
            return errors;
        }
        
        switch (format) {
            case 'edifact':
                return this.validateEdifact(data);
            case 'x12':
                return this.validateX12(data);
            case 'xml':
                return this.validateXml(data);
            case 'json':
                return this.validateJson(data);
            case 'csv':
                return this.validateCsv(data);
            default:
                errors.push('Unsupported EDI format');
                return errors;
        }
    }
    
    static validateEdifact(data) {
        const errors = [];
        
        // Basic EDIFACT validation
        if (!data.includes('UNB')) {
            errors.push('Missing UNB segment (Interchange Header)');
        }
        
        if (!data.includes('UNZ')) {
            errors.push('Missing UNZ segment (Interchange Trailer)');
        }
        
        return errors;
    }
    
    static validateX12(data) {
        const errors = [];
        
        // Basic X12 validation
        if (!data.includes('ISA')) {
            errors.push('Missing ISA segment (Interchange Control Header)');
        }
        
        if (!data.includes('IEA')) {
            errors.push('Missing IEA segment (Interchange Control Trailer)');
        }
        
        return errors;
    }
    
    static validateXml(data) {
        const errors = [];
        
        try {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/xml');
            
            if (doc.getElementsByTagName('parsererror').length > 0) {
                errors.push('Invalid XML format');
            }
        } catch (e) {
            errors.push('XML parsing error: ' + e.message);
        }
        
        return errors;
    }
    
    static validateJson(data) {
        const errors = [];
        
        try {
            JSON.parse(data);
        } catch (e) {
            errors.push('JSON parsing error: ' + e.message);
        }
        
        return errors;
    }
    
    static validateCsv(data) {
        const errors = [];
        
        // Basic CSV validation
        const lines = data.split('\n');
        if (lines.length < 2) {
            errors.push('CSV must have at least 2 lines (header and data)');
        }
        
        return errors;
    }
}

// EDI Data Processing Utility
class EdiDataProcessingUtility {
    static processEdiData(data, format) {
        switch (format) {
            case 'edifact':
                return this.processEdifact(data);
            case 'x12':
                return this.processX12(data);
            case 'xml':
                return this.processXml(data);
            case 'json':
                return this.processJson(data);
            case 'csv':
                return this.processCsv(data);
            default:
                return data;
        }
    }
    
    static processEdifact(data) {
        // Process EDIFACT data
        const segments = data.split('\'');
        const processedData = {
            segments: segments,
            count: segments.length
        };
        
        return JSON.stringify(processedData, null, 2);
    }
    
    static processX12(data) {
        // Process X12 data
        const segments = data.split('~');
        const processedData = {
            segments: segments,
            count: segments.length
        };
        
        return JSON.stringify(processedData, null, 2);
    }
    
    static processXml(data) {
        // Process XML data
        try {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/xml');
            
            const processedData = {
                rootElement: doc.documentElement.tagName,
                childCount: doc.documentElement.children.length
            };
            
            return JSON.stringify(processedData, null, 2);
        } catch (e) {
            return data;
        }
    }
    
    static processJson(data) {
        // Process JSON data
        try {
            const jsonData = JSON.parse(data);
            return JSON.stringify(jsonData, null, 2);
        } catch (e) {
            return data;
        }
    }
    
    static processCsv(data) {
        // Process CSV data
        const lines = data.split('\n');
        const headers = lines[0].split(',');
        const rows = lines.slice(1).map(line => line.split(','));
        
        const processedData = {
            headers: headers,
            rows: rows,
            rowCount: rows.length
        };
        
        return JSON.stringify(processedData, null, 2);
    }
}

// Initialize managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EdiDocumentManager();
    new EdiMessageManager();
    new EdiTransmissionManager();
});

// Utility functions
function formatEdiDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }).format(new Date(date));
}

function formatEdiAmount(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function validateEdiFormat(format) {
    const validFormats = ['edifact', 'x12', 'xml', 'json', 'csv', 'custom'];
    return validFormats.includes(format);
}

function validateEdiProtocol(protocol) {
    const validProtocols = ['ftp', 'sftp', 'http', 'https', 'as2', 'email', 'api', 'other'];
    return validProtocols.includes(protocol);
}

// Export for use in other modules
window.IndianEDI = {
    EdiDocumentManager,
    EdiMessageManager,
    EdiTransmissionManager,
    EdiValidationUtility,
    EdiDataProcessingUtility,
    formatEdiDate,
    formatEdiAmount,
    validateEdiFormat,
    validateEdiProtocol
};