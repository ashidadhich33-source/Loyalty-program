# 🌊 Ocean ERP - GST Workflow Guide

## Overview

Ocean ERP includes comprehensive GST (Goods and Services Tax) implementation for Indian businesses, specifically tailored for kids clothing retail. This guide explains how GST works across all business operations.

## 🏗️ GST System Architecture

### **Core GST Components**
- ✅ **GST Tax Structure**: CGST, SGST, IGST, UTGST, CESS
- ✅ **Tax Groups**: Organized by GST rates (0%, 5%, 12%, 18%, 28%)
- ✅ **HSN/SAC Codes**: Harmonized System of Nomenclature codes
- ✅ **Fiscal Positions**: State-wise GST treatment
- ✅ **GST Returns**: GSTR-1, GSTR-3B, GSTR-9 filing
- ✅ **E-invoicing**: Integration with EDI for e-invoicing

### **Kids Clothing Specific Features**
- ✅ **Age-based GST**: Different GST rates for different age groups
- ✅ **Size-based GST**: GST variations by clothing size
- ✅ **Season-based GST**: Seasonal GST adjustments
- ✅ **Brand-specific GST**: Brand-wise GST configurations

## 💰 GST Tax Structure

### **GST Types**
1. **CGST (Central GST)**: Central government tax
2. **SGST (State GST)**: State government tax  
3. **IGST (Integrated GST)**: Inter-state transactions
4. **UTGST (Union Territory GST)**: Union territory tax
5. **CESS**: Additional cess on specific items

### **GST Rates for Kids Clothing**
- **0%**: Baby essentials (0-2 years)
- **5%**: Basic kids clothing (2-6 years)
- **12%**: Standard kids clothing (6-12 years)
- **18%**: Premium kids clothing (12+ years)
- **28%**: Luxury kids items

## 🛒 GST in Sales Operations

### **Sales Order GST Flow**
```
1. Create Sales Order
   ↓
2. Select Customer & Location
   ↓
3. System Determines GST Treatment:
   - Regular: CGST + SGST (Intra-state)
   - IGST: IGST (Inter-state)
   ↓
4. Apply Product-specific GST Rates
   ↓
5. Calculate GST Amounts
   ↓
6. Generate GST Invoice
```

### **GST Treatment Logic**
- **Intra-state Sales**: CGST + SGST
- **Inter-state Sales**: IGST
- **Export Sales**: Zero-rated GST
- **SEZ Sales**: Zero-rated GST

### **Sales Order GST Fields**
- `gst_treatment`: Regular, Composition, Unregistered, etc.
- `fiscal_position_id`: State-wise fiscal position
- `gst_in`: Customer GST registration number
- `place_of_supply`: Supply location for GST

### **Example Sales Order GST Calculation**
```
Product: Kids T-Shirt (Age: 6-8 years)
Base Price: ₹500
GST Rate: 12%
Location: Maharashtra (Intra-state)

Calculation:
- CGST (6%): ₹30
- SGST (6%): ₹30
- Total GST: ₹60
- Final Price: ₹560
```

## 🛍️ GST in Purchase Operations

### **Purchase Order GST Flow**
```
1. Create Purchase Order
   ↓
2. Select Vendor & Location
   ↓
3. System Determines GST Treatment:
   - Regular: CGST + SGST (Intra-state)
   - IGST: IGST (Inter-state)
   ↓
4. Apply Product-specific GST Rates
   ↓
5. Calculate Input GST
   ↓
6. Generate Purchase Invoice
```

### **Purchase GST Features**
- **Input GST Credit**: Automatic input tax credit calculation
- **Reverse Charge**: Reverse charge mechanism support
- **Import GST**: IGST on imports
- **Composition Scheme**: Special GST treatment

### **Purchase Order GST Fields**
- `gst_treatment`: Regular, Composition, etc.
- `fiscal_position_id`: Vendor fiscal position
- `vendor_gst_in`: Vendor GST registration
- `reverse_charge`: Reverse charge applicability

### **Example Purchase Order GST Calculation**
```
Product: Raw Material for Kids Clothing
Base Price: ₹10,000
GST Rate: 18%
Location: Gujarat (Inter-state)

Calculation:
- IGST (18%): ₹1,800
- Total Amount: ₹11,800
- Input Tax Credit: ₹1,800
```

## 🔄 GST in Purchase Returns

### **Purchase Return GST Flow**
```
1. Create Purchase Return
   ↓
2. Reference Original Purchase Order
   ↓
3. System Reverses GST:
   - Reduces Input Tax Credit
   - Creates Credit Note
   ↓
4. Update GST Returns
```

### **Purchase Return GST Features**
- **GST Reversal**: Automatic GST reversal
- **Credit Note**: GST credit note generation
- **Return Period**: GST return period tracking
- **Adjustment**: Input tax credit adjustment

### **Example Purchase Return GST**
```
Original Purchase: ₹11,800 (₹10,000 + ₹1,800 IGST)
Return Amount: ₹2,360 (₹2,000 + ₹360 IGST)
GST Reversal: ₹360
Net Input Credit: ₹1,440 (₹1,800 - ₹360)
```

## 🏪 GST in POS Operations

### **POS GST Flow**
```
1. Start POS Session
   ↓
2. Configure GST Settings:
   - Default GST rates
   - State-wise settings
   ↓
3. Process Sales:
   - Automatic GST calculation
   - Real-time GST display
   ↓
4. Generate GST Receipt
   ↓
5. Update GST Reports
```

### **POS GST Features**
- **Real-time GST**: Live GST calculation
- **Multiple GST Rates**: Different rates per product
- **GST Receipt**: GST-compliant receipts
- **Daily GST Summary**: End-of-day GST reports

### **POS GST Configuration**
- `company_gstin`: Company GST registration
- `default_gst_rate`: Default GST rate
- `gst_enabled`: Enable/disable GST
- `gst_receipt_format`: GST receipt format

### **Example POS GST Calculation**
```
POS Sale:
- Product 1: ₹300 (12% GST) = ₹36 GST
- Product 2: ₹500 (18% GST) = ₹90 GST
- Total GST: ₹126
- Total Amount: ₹926
```

## 📊 GST Reports and Returns

### **GST Return Types**
1. **GSTR-1**: Outward supplies (Sales)
2. **GSTR-2**: Inward supplies (Purchases)
3. **GSTR-3B**: Monthly summary return
4. **GSTR-9**: Annual return

### **GST Report Generation**
```
1. Select Return Period
   ↓
2. Generate Return Data:
   - Sales data (GSTR-1)
   - Purchase data (GSTR-2)
   - Summary data (GSTR-3B)
   ↓
3. Validate GST Data
   ↓
4. Export GST Return
   ↓
5. File with GST Portal
```

### **GST Reports Available**
- **GST Sales Report**: Sales-wise GST summary
- **GST Purchase Report**: Purchase-wise GST summary
- **GST Return Report**: Return-wise GST summary
- **GST Liability Report**: GST liability calculation
- **Input Tax Credit Report**: ITC utilization report

## 🔧 GST Configuration

### **Company GST Settings**
```json
{
  "gst_settings": {
    "company_gstin": "27ABCDE1234F1Z5",
    "gst_enabled": true,
    "default_gst_rate": 18,
    "composition_scheme": false,
    "reverse_charge": false,
    "e_invoicing": true,
    "gst_return_filing": true
  }
}
```

### **Product GST Settings**
- **HSN Code**: Product HSN code
- **GST Rate**: Product-specific GST rate
- **GST Treatment**: Regular, Exempt, Nil-rated
- **Age Group**: Age-specific GST rates
- **Size**: Size-specific GST rates

### **Customer/Vendor GST Settings**
- **GST Registration**: GSTIN number
- **GST Treatment**: Regular, Composition, Unregistered
- **Place of Supply**: Supply location
- **Fiscal Position**: State-wise position

## 📱 GST Integration Features

### **E-invoicing Integration**
- **IRN Generation**: Invoice Registration Number
- **QR Code**: GST QR code generation
- **E-invoice Upload**: Automatic upload to GST portal
- **Validation**: E-invoice validation

### **GST Portal Integration**
- **Return Filing**: Direct filing to GST portal
- **Payment Integration**: GST payment integration
- **Status Tracking**: Return filing status
- **Reconciliation**: GST data reconciliation

## 🎯 GST Workflow Examples

### **Scenario 1: Intra-state Sale**
```
Company: Mumbai, Maharashtra
Customer: Pune, Maharashtra
Product: Kids T-Shirt (₹500)

GST Calculation:
- CGST (6%): ₹30
- SGST (6%): ₹30
- Total GST: ₹60
- Final Amount: ₹560
```

### **Scenario 2: Inter-state Sale**
```
Company: Mumbai, Maharashtra
Customer: Bangalore, Karnataka
Product: Kids Jeans (₹800)

GST Calculation:
- IGST (12%): ₹96
- Total GST: ₹96
- Final Amount: ₹896
```

### **Scenario 3: Purchase with Input Credit**
```
Vendor: Delhi, Delhi
Product: Raw Material (₹10,000)

GST Calculation:
- IGST (18%): ₹1,800
- Total Amount: ₹11,800
- Input Tax Credit: ₹1,800
```

### **Scenario 4: POS Sale**
```
POS Location: Mumbai, Maharashtra
Customer: Local walk-in

Products:
- Baby Clothes (₹300): CGST ₹18 + SGST ₹18
- Kids Shoes (₹500): CGST ₹45 + SGST ₹45

Total GST: ₹126
Total Amount: ₹926
```

## 🔍 GST Compliance Features

### **Automatic Compliance**
- ✅ **GST Rate Validation**: Automatic rate validation
- ✅ **HSN Code Validation**: HSN code format validation
- ✅ **GSTIN Validation**: GST registration validation
- ✅ **Return Due Dates**: Automatic due date tracking

### **GST Audit Trail**
- ✅ **Transaction Logging**: Complete GST transaction log
- ✅ **Change Tracking**: GST configuration changes
- ✅ **User Activity**: User-wise GST activities
- ✅ **Data Integrity**: GST data validation

### **GST Error Handling**
- ✅ **Validation Errors**: GST validation error handling
- ✅ **Calculation Errors**: GST calculation error handling
- ✅ **Return Errors**: GST return error handling
- ✅ **Integration Errors**: GST portal integration errors

## 🚀 Getting Started with GST

### **1. Enable GST**
1. Go to **Settings** → **Company** → **GST Settings**
2. Enable GST for the company
3. Enter company GSTIN
4. Configure default GST rates

### **2. Configure GST Rates**
1. Go to **Accounting** → **GST** → **Tax Rates**
2. Create GST tax rates (0%, 5%, 12%, 18%, 28%)
3. Configure CGST, SGST, IGST rates
4. Set up CESS rates if applicable

### **3. Set Up Products**
1. Go to **Products** → **Products**
2. Add HSN codes to products
3. Assign GST tax groups
4. Configure age/size-specific rates

### **4. Configure Customers/Vendors**
1. Go to **Contacts** → **Customers/Vendors**
2. Add GSTIN numbers
3. Set GST treatment
4. Configure fiscal positions

### **5. Generate GST Returns**
1. Go to **Accounting** → **GST** → **Returns**
2. Select return period
3. Generate return data
4. Export and file returns

## 📞 GST Support

### **GST Help Resources**
- **GST Documentation**: Complete GST documentation
- **GST Training**: GST training materials
- **GST Support**: Technical support for GST
- **GST Updates**: Regular GST updates

### **GST Compliance Checklist**
- ✅ Company GSTIN registered
- ✅ GST rates configured
- ✅ Products have HSN codes
- ✅ Customers/Vendors have GSTIN
- ✅ GST returns filed on time
- ✅ E-invoicing enabled
- ✅ GST reports generated

---

**Ocean ERP GST System** - Complete GST compliance for Indian kids clothing retail businesses! 🌊👶👕💰