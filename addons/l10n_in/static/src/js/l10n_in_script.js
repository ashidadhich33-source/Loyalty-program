// Ocean ERP - Indian Localization JavaScript

// Company Management
class CompanyManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadCompanyData();
    }
    
    bindEvents() {
        // PAN validation
        document.addEventListener('DOMContentLoaded', () => {
            const panInputs = document.querySelectorAll('input[name="pan"]');
            panInputs.forEach(input => {
                input.addEventListener('blur', this.validatePAN.bind(this));
            });
            
            // GSTIN validation
            const gstinInputs = document.querySelectorAll('input[name="gstin"]');
            gstinInputs.forEach(input => {
                input.addEventListener('blur', this.validateGSTIN.bind(this));
            });
            
            // CIN validation
            const cinInputs = document.querySelectorAll('input[name="cin"]');
            cinInputs.forEach(input => {
                input.addEventListener('blur', this.validateCIN.bind(this));
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
    
    validateGSTIN(event) {
        const gstin = event.target.value;
        const gstinPattern = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$/;
        
        if (gstin && !gstinPattern.test(gstin)) {
            this.showError(event.target, 'Invalid GSTIN format');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateCIN(event) {
        const cin = event.target.value;
        const cinPattern = /^[A-Z]{1}[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$/;
        
        if (cin && !cinPattern.test(cin)) {
            this.showError(event.target, 'Invalid CIN format');
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
    
    loadCompanyData() {
        // Load company data for dashboard
        fetch('/api/companies/kids-clothing-data')
            .then(response => response.json())
            .then(data => {
                this.updateDashboard(data);
            })
            .catch(error => {
                console.error('Error loading company data:', error);
            });
    }
    
    updateDashboard(data) {
        // Update dashboard with kids clothing specific data
        const dashboard = document.querySelector('.company-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateDashboardHTML(data);
        }
    }
    
    generateDashboardHTML(data) {
        return `
            <div class="dashboard-grid">
                <div class="dashboard-card">
                    <h4>Age Group Distribution</h4>
                    <div class="age-group-stats">
                        ${this.generateAgeGroupStats(data.ageGroups)}
                    </div>
                </div>
                <div class="dashboard-card">
                    <h4>Size Distribution</h4>
                    <div class="size-stats">
                        ${this.generateSizeStats(data.sizes)}
                    </div>
                </div>
                <div class="dashboard-card">
                    <h4>Seasonal Analysis</h4>
                    <div class="season-stats">
                        ${this.generateSeasonStats(data.seasons)}
                    </div>
                </div>
            </div>
        `;
    }
    
    generateAgeGroupStats(ageGroups) {
        return Object.entries(ageGroups).map(([age, count]) => 
            `<div class="stat-item">
                <span class="age-group-badge age-group-${age.replace('-', '-')}">${age}</span>
                <span class="count">${count}</span>
            </div>`
        ).join('');
    }
    
    generateSizeStats(sizes) {
        return Object.entries(sizes).map(([size, count]) => 
            `<div class="stat-item">
                <span class="size-badge size-${size}">${size.toUpperCase()}</span>
                <span class="count">${count}</span>
            </div>`
        ).join('');
    }
    
    generateSeasonStats(seasons) {
        return Object.entries(seasons).map(([season, count]) => 
            `<div class="stat-item">
                <span class="season-badge season-${season}">${season}</span>
                <span class="count">${count}</span>
            </div>`
        ).join('');
    }
}

// Geographic Manager
class GeographicManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadGeographicData();
    }
    
    bindEvents() {
        // State selection
        document.addEventListener('change', (event) => {
            if (event.target.name === 'state_id') {
                this.loadDistricts(event.target.value);
            }
        });
        
        // District selection
        document.addEventListener('change', (event) => {
            if (event.target.name === 'district_id') {
                this.loadTalukas(event.target.value);
            }
        });
        
        // Taluka selection
        document.addEventListener('change', (event) => {
            if (event.target.name === 'taluka_id') {
                this.loadVillages(event.target.value);
            }
        });
    }
    
    loadDistricts(stateId) {
        if (!stateId) return;
        
        fetch(`/api/districts?state_id=${stateId}`)
            .then(response => response.json())
            .then(data => {
                this.updateSelect('district_id', data);
            })
            .catch(error => {
                console.error('Error loading districts:', error);
            });
    }
    
    loadTalukas(districtId) {
        if (!districtId) return;
        
        fetch(`/api/talukas?district_id=${districtId}`)
            .then(response => response.json())
            .then(data => {
                this.updateSelect('taluka_id', data);
            })
            .catch(error => {
                console.error('Error loading talukas:', error);
            });
    }
    
    loadVillages(talukaId) {
        if (!talukaId) return;
        
        fetch(`/api/villages?taluka_id=${talukaId}`)
            .then(response => response.json())
            .then(data => {
                this.updateSelect('village_id', data);
            })
            .catch(error => {
                console.error('Error loading villages:', error);
            });
    }
    
    updateSelect(selectName, data) {
        const select = document.querySelector(`select[name="${selectName}"]`);
        if (select) {
            select.innerHTML = '<option value="">Select...</option>';
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id;
                option.textContent = item.name;
                select.appendChild(option);
            });
        }
    }
    
    loadGeographicData() {
        // Load geographic data for visualization
        fetch('/api/geographic/kids-clothing-data')
            .then(response => response.json())
            .then(data => {
                this.updateGeographicVisualization(data);
            })
            .catch(error => {
                console.error('Error loading geographic data:', error);
            });
    }
    
    updateGeographicVisualization(data) {
        const container = document.querySelector('.geographic-visualization');
        if (container) {
            container.innerHTML = this.generateGeographicHTML(data);
        }
    }
    
    generateGeographicHTML(data) {
        return `
            <div class="geographic-tree">
                <h3>Geographic Distribution</h3>
                ${data.states.map(state => `
                    <div class="state-item">
                        <h4>${state.name}</h4>
                        <div class="age-group-badges">
                            ${state.ageGroups.map(age => 
                                `<span class="age-group-badge age-group-${age.replace('-', '-')}">${age}</span>`
                            ).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// Banking Manager
class BankingManager {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadBankingData();
    }
    
    bindEvents() {
        // IFSC validation
        document.addEventListener('DOMContentLoaded', () => {
            const ifscInputs = document.querySelectorAll('input[name="ifsc_code"]');
            ifscInputs.forEach(input => {
                input.addEventListener('blur', this.validateIFSC.bind(this));
            });
            
            // MICR validation
            const micrInputs = document.querySelectorAll('input[name="micr_code"]');
            micrInputs.forEach(input => {
                input.addEventListener('blur', this.validateMICR.bind(this));
            });
        });
    }
    
    validateIFSC(event) {
        const ifsc = event.target.value;
        const ifscPattern = /^[A-Z]{4}0[A-Z0-9]{6}$/;
        
        if (ifsc && !ifscPattern.test(ifsc)) {
            this.showError(event.target, 'Invalid IFSC format. Format: ABCD0123456');
        } else {
            this.clearError(event.target);
        }
    }
    
    validateMICR(event) {
        const micr = event.target.value;
        const micrPattern = /^[0-9]{9}$/;
        
        if (micr && !micrPattern.test(micr)) {
            this.showError(event.target, 'Invalid MICR format. Should be 9 digits');
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
    
    loadBankingData() {
        // Load banking data for dashboard
        fetch('/api/banking/kids-clothing-data')
            .then(response => response.json())
            .then(data => {
                this.updateBankingDashboard(data);
            })
            .catch(error => {
                console.error('Error loading banking data:', error);
            });
    }
    
    updateBankingDashboard(data) {
        const dashboard = document.querySelector('.banking-dashboard');
        if (dashboard) {
            dashboard.innerHTML = this.generateBankingHTML(data);
        }
    }
    
    generateBankingHTML(data) {
        return `
            <div class="banking-grid">
                ${data.banks.map(bank => `
                    <div class="bank-card">
                        <h4>${bank.name}</h4>
                        <p>Type: ${bank.type}</p>
                        <p>IFSC: ${bank.ifsc}</p>
                        <div class="kids-clothing-info">
                            <span class="age-group-badge age-group-${bank.ageGroup.replace('-', '-')}">${bank.ageGroup}</span>
                            <span class="size-badge size-${bank.size}">${bank.size.toUpperCase()}</span>
                            <span class="season-badge season-${bank.season}">${bank.season}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// Initialize managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CompanyManager();
    new GeographicManager();
    new BankingManager();
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

// Export for use in other modules
window.IndianLocalization = {
    CompanyManager,
    GeographicManager,
    BankingManager,
    formatIndianCurrency,
    formatIndianDate
};