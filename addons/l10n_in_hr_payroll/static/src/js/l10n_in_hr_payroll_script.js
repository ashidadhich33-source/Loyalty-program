// Ocean ERP - Indian HR Payroll JavaScript

// HR Employee Manager
class HrEmployeeManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadHrEmployeeData();
    }
    
    bindEvents() {
        // PAN validation
        document.addEventListener('DOMContentLoaded', () => {
            const panInputs = document.querySelectorAll('input[name="pan"]');
            panInputs.forEach(input => {
                input.addEventListener('blur', this.validatePAN.bind(this));
            });
            
            // Aadhar validation
            const aadharInputs = document.querySelectorAll('input[name="aadhar"]');
            aadharInputs.forEach(input => {
                input.addEventListener('blur', this.validateAadhar.bind(this));
            });
            
            // PF number validation
            const pfInputs = document.querySelectorAll('input[name="pf_number"]');
            pfInputs.forEach(input => {
                input.addEventListener('blur', this.validatePFNumber.bind(this));
            });
            
            // ESI number validation
            const esiInputs = document.querySelectorAll('input[name="esi_number"]');
            esiInputs.forEach(input => {
                input.addEventListener('blur', this.validateESINumber.bind(this));
            });
            
            // UAN validation
            const uanInputs = document.querySelectorAll('input[name="uan"]');
            uanInputs.forEach(input => {
                input.addEventListener('blur', this.validateUAN.bind(this));
            });
        });
    }
    
    validatePAN(event) {
        const pan = event.target.value;
        const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
        
        if (pan && !panPattern.test(pan)) {
            this.showError(event.target, 'Invalid PAN format. Format: ABCDE1234F');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateAadhar(event) {
        const aadhar = event.target.value;
        const aadharPattern = /^[0-9]{12}$/;
        
        if (aadhar && !aadharPattern.test(aadhar)) {
            this.showError(event.target, 'Invalid Aadhar format. Should be 12 digits');
        } else {
            this.clearError(event.target);
        }
    }
    
    validatePFNumber(event) {
        const pfNumber = event.target.value;
        const pfPattern = /^[A-Z]{2}[0-9]{7}[0-9]{3}$/;
        
        if (pfNumber && !pfPattern.test(pfNumber)) {
            this.showError(event.target, 'Invalid PF number format');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateESINumber(event) {
        const esiNumber = event.target.value;
        const esiPattern = /^[0-9]{10}$/;
        
        if (esiNumber && !esiPattern.test(esiNumber)) {
            this.showError(event.target, 'Invalid ESI number format. Should be 10 digits');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateUAN(event) {
        const uan = event.target.value;
        const uanPattern = /^[0-9]{12}$/;
        
        if (uan && !uanPattern.test(uan)) {
            this.showError(event.target, 'Invalid UAN format. Should be 12 digits');
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
    
    loadHrEmployeeData() {
        // Load HR employee data for dashboard
        fetch('/api/hr/employee-data')
            .then(response => response.json())
            .then(data => {
                this.updateHrEmployeeDashboard(data);
            })
            .catch(error => {
                console.error('Error loading HR employee data:', error);
            });
    }
    
    updateHrEmployeeDashboard(data) {
        const dashboard = document.querySelector('.hr-employee-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateHrEmployeeHTML(data);
        }
    }
    
    generateHrEmployeeHTML(data) {
        return `
            <div class="hr-dashboard-grid">
                <div class="hr-dashboard-card">
                    <h4>Total Employees</h4>
                    <div class="count">${data.totalEmployees}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Active Employees</h4>
                    <div class="count">${data.activeEmployees}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Male Employees</h4>
                    <div class="count">${data.maleEmployees}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Female Employees</h4>
                    <div class="count">${data.femaleEmployees}</div>
                </div>
            </div>
            <div class="kids-clothing-hr-info">
                <h4>Kids Clothing Employee Distribution</h4>
                <div class="kids-clothing-hr-badges">
                    ${this.generateKidsClothingHrBadges(data.kidsClothingData)}
                </div>
            </div>
        `;
    }
    
    generateKidsClothingHrBadges(data) {
        return Object.entries(data).map(([key, value]) => 
            `<span class="contract-type-badge contract-type-${key}">${key.replace('_', ' ').toUpperCase()}: ${value}</span>`
        ).join('');
    }
}

// HR Contract Manager
class HrContractManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadHrContractData();
    }
    
    bindEvents() {
        // Contract date validation
        document.addEventListener('DOMContentLoaded', () => {
            const dateStartInputs = document.querySelectorAll('input[name="date_start"]');
            const dateEndInputs = document.querySelectorAll('input[name="date_end"]');
            
            dateStartInputs.forEach(input => {
                input.addEventListener('change', this.validateContractDates.bind(this));
            });
            
            dateEndInputs.forEach(input => {
                input.addEventListener('change', this.validateContractDates.bind(this));
            });
            
            // Wage validation
            const wageInputs = document.querySelectorAll('input[name="wage"]');
            wageInputs.forEach(input => {
                input.addEventListener('blur', this.validateWage.bind(this));
            });
        });
    }
    
    validateContractDates(event) {
        const form = event.target.closest('form');
        const dateStart = form.querySelector('input[name="date_start"]');
        const dateEnd = form.querySelector('input[name="date_end"]');
        
        if (dateStart.value && dateEnd.value) {
            const startDate = new Date(dateStart.value);
            const endDate = new Date(dateEnd.value);
            
            if (startDate > endDate) {
                this.showError(dateEnd, 'End date must be after start date');
            } else {
                this.clearError(dateEnd);
            }
        }
    }
    
    validateWage(event) {
        const wage = parseFloat(event.target.value);
        
        if (event.target.value && (isNaN(wage) || wage < 0)) {
            this.showError(event.target, 'Wage must be a positive number');
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
    
    loadHrContractData() {
        // Load HR contract data for dashboard
        fetch('/api/hr/contract-data')
            .then(response => response.json())
            .then(data => {
                this.updateHrContractDashboard(data);
            })
            .catch(error => {
                console.error('Error loading HR contract data:', error);
            });
    }
    
    updateHrContractDashboard(data) {
        const dashboard = document.querySelector('.hr-contract-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateHrContractHTML(data);
        }
    }
    
    generateHrContractHTML(data) {
        return `
            <div class="hr-dashboard-grid">
                <div class="hr-dashboard-card">
                    <h4>Permanent Contracts</h4>
                    <div class="count">${data.permanentContracts}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Temporary Contracts</h4>
                    <div class="count">${data.temporaryContracts}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Contract Contracts</h4>
                    <div class="count">${data.contractContracts}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Intern Contracts</h4>
                    <div class="count">${data.internContracts}</div>
                </div>
            </div>
            <div class="contract-status">
                <span class="contract-status-badge contract-status-draft">Draft: ${data.draftContracts}</span>
                <span class="contract-status-badge contract-status-open">Running: ${data.openContracts}</span>
                <span class="contract-status-badge contract-status-close">Expired: ${data.closeContracts}</span>
                <span class="contract-status-badge contract-status-cancel">Cancelled: ${data.cancelContracts}</span>
            </div>
        `;
    }
}

// HR Payslip Manager
class HrPayslipManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadHrPayslipData();
    }
    
    bindEvents() {
        // Payslip date validation
        document.addEventListener('DOMContentLoaded', () => {
            const dateFromInputs = document.querySelectorAll('input[name="date_from"]');
            const dateToInputs = document.querySelectorAll('input[name="date_to"]');
            
            dateFromInputs.forEach(input => {
                input.addEventListener('change', this.validatePayslipDates.bind(this));
            });
            
            dateToInputs.forEach(input => {
                input.addEventListener('change', this.validatePayslipDates.bind(this));
            });
        });
    }
    
    validatePayslipDates(event) {
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
    
    loadHrPayslipData() {
        // Load HR payslip data for dashboard
        fetch('/api/hr/payslip-data')
            .then(response => response.json())
            .then(data => {
                this.updateHrPayslipDashboard(data);
            })
            .catch(error => {
                console.error('Error loading HR payslip data:', error);
            });
    }
    
    updateHrPayslipDashboard(data) {
        const dashboard = document.querySelector('.hr-payslip-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateHrPayslipHTML(data);
        }
    }
    
    generateHrPayslipHTML(data) {
        return `
            <div class="hr-dashboard-grid">
                <div class="hr-dashboard-card">
                    <h4>Total Payslips</h4>
                    <div class="count">${data.totalPayslips}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Draft Payslips</h4>
                    <div class="count">${data.draftPayslips}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Verified Payslips</h4>
                    <div class="count">${data.verifiedPayslips}</div>
                </div>
                <div class="hr-dashboard-card">
                    <h4>Done Payslips</h4>
                    <div class="count">${data.donePayslips}</div>
                </div>
            </div>
            <div class="payslip-status">
                <span class="payslip-status-badge payslip-status-draft">Draft: ${data.draftPayslips}</span>
                <span class="payslip-status-badge payslip-status-verify">Waiting: ${data.verifiedPayslips}</span>
                <span class="payslip-status-badge payslip-status-done">Done: ${data.donePayslips}</span>
                <span class="payslip-status-badge payslip-status-cancel">Cancelled: ${data.cancelledPayslips}</span>
            </div>
        `;
    }
}

// Indian Payroll Calculator
class IndianPayrollCalculator {
    static calculatePF(basicWage) {
        // PF is 12% of basic wage, maximum 1800
        return Math.min(basicWage * 0.12, 1800);
    }
    
    static calculateESI(grossSalary) {
        // ESI is 0.75% of gross salary, applicable only if gross <= 21000
        if (grossSalary <= 21000) {
            return grossSalary * 0.0075;
        }
        return 0;
    }
    
    static calculateProfessionalTax(wage) {
        // Professional tax varies by state, using average
        return Math.min(200, wage * 0.01);
    }
    
    static calculateIncomeTax(annualSalary) {
        // Simplified tax calculation
        if (annualSalary <= 250000) {
            return 0; // Below tax exemption limit
        }
        
        const taxableIncome = annualSalary - 250000;
        const taxAmount = Math.min(taxableIncome * 0.05, 12500); // 5% tax rate
        return taxAmount / 12; // Monthly tax
    }
    
    static calculateGrossSalary(basicWage, allowances = 0) {
        return basicWage + allowances;
    }
    
    static calculateNetSalary(basicWage, allowances = 0) {
        const grossSalary = this.calculateGrossSalary(basicWage, allowances);
        const pf = this.calculatePF(basicWage);
        const esi = this.calculateESI(grossSalary);
        const pt = this.calculateProfessionalTax(basicWage);
        const tax = this.calculateIncomeTax(basicWage * 12);
        
        return grossSalary - pf - esi - pt - tax;
    }
    
    static getPayrollBreakdown(basicWage, allowances = 0) {
        const grossSalary = this.calculateGrossSalary(basicWage, allowances);
        const pf = this.calculatePF(basicWage);
        const esi = this.calculateESI(grossSalary);
        const pt = this.calculateProfessionalTax(basicWage);
        const tax = this.calculateIncomeTax(basicWage * 12);
        const netSalary = grossSalary - pf - esi - pt - tax;
        
        return {
            basicWage: basicWage,
            allowances: allowances,
            grossSalary: grossSalary,
            deductions: {
                pf: pf,
                esi: esi,
                professionalTax: pt,
                incomeTax: tax,
                total: pf + esi + pt + tax
            },
            netSalary: netSalary
        };
    }
}

// Initialize managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HrEmployeeManager();
    new HrContractManager();
    new HrPayslipManager();
});

// Utility functions
function formatIndianCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatIndianDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function validatePAN(pan) {
    const panPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
    return panPattern.test(pan);
}

function validateAadhar(aadhar) {
    const aadharPattern = /^[0-9]{12}$/;
    return aadharPattern.test(aadhar);
}

function validatePFNumber(pfNumber) {
    const pfPattern = /^[A-Z]{2}[0-9]{7}[0-9]{3}$/;
    return pfPattern.test(pfNumber);
}

function validateESINumber(esiNumber) {
    const esiPattern = /^[0-9]{10}$/;
    return esiPattern.test(esiNumber);
}

function validateUAN(uan) {
    const uanPattern = /^[0-9]{12}$/;
    return uanPattern.test(uan);
}

// Export for use in other modules
window.IndianHRPayroll = {
    HrEmployeeManager,
    HrContractManager,
    HrPayslipManager,
    IndianPayrollCalculator,
    formatIndianCurrency,
    formatIndianDate,
    validatePAN,
    validateAadhar,
    validatePFNumber,
    validateESINumber,
    validateUAN
};