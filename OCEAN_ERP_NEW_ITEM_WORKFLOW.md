# Ocean ERP - New Item Workflow Guide
## Complete Step-by-Step Item Creation Process

---

## 🎯 **OVERVIEW**

The new item workflow in Ocean ERP follows a **Product Template → Product Variant** structure, similar to modern ERP systems, with complete GST integration and retail-specific features.

---

## 📋 **WORKFLOW STRUCTURE**

```
StyleCode (Product Template)
    ├── Variant 1 (Barcode: 685686043632)
    ├── Variant 2 (Barcode: 685686043633)
    ├── Variant 3 (Barcode: 685686043634)
    └── Variant N (Barcode: 685686043635)
```

---

## 🚀 **STEP 1: CREATE PRODUCT TEMPLATE (STYLECODE)**

### **1.1 Access Product Template Creation**
- **Menu**: Products → Product Templates → Create
- **URL**: `/products/product_template/create`

### **1.2 Fill Basic Information**
```yaml
Product Name: "Boys Blue Slim Fit Stretchable Jeans"
StyleCode: "121246526864"  # Internal Reference
Description: "5000 Boys Blue Slim Fit Stretchable Jeans"
Brand: "GINI AND JONY"
Category: "BOTTOM"
Sub Category: "JEANS"
Gender: "BOYS"
```

### **1.3 GST Configuration**
```yaml
HSN Code: "6203"
GST Tax Group: "5% GST"  # Links to tax group
```

### **1.4 Save Template**
- Click **Save** to create the Product Template
- **Status**: Template created but not yet active
- **Inventory**: 0 (no variants created yet)

---

## 🎨 **STEP 2: CREATE PRODUCT VARIANTS (BARCODES)**

### **2.1 Access Variant Creation**
- **From Template**: Click "Create Variant" button
- **Menu**: Products → Product Variants → Create

### **2.2 Fill Variant Information**
```yaml
# Variant 1 (Size 18)
Product Template: "121246526864"
Barcode: "685686043632"
EAN Code: "8907936912167"
Size: "18"
Color/Shade: "BLUE"
MRP: "1499.00"
Cost Price: "843.79"
GST Rate: "5.00"
Sales Price: "1499.00"  # Auto-calculated from MRP
```

### **2.3 Create Multiple Variants**
```yaml
# Variant 2 (Size 20)
Barcode: "685686043633"
EAN Code: "8907936912174"
Size: "20"
Color/Shade: "BLUE"
MRP: "1499.00"
Cost Price: "843.79"
GST Rate: "5.00"

# Variant 3 (Size 22)
Barcode: "685686043634"
EAN Code: "8907936912181"
Size: "22"
Color/Shade: "BLUE"
MRP: "1499.00"
Cost Price: "843.79"
GST Rate: "5.00"

# Variant 4 (Size 24)
Barcode: "685686043635"
EAN Code: "8907936912198"
Size: "24"
Color/Shade: "BLUE"
MRP: "1699.00"  # Different MRP for larger size
Cost Price: "956.37"
GST Rate: "5.00"
```

### **2.4 Save Each Variant**
- Click **Save** for each variant
- **Status**: Variant created but not yet active
- **Inventory**: 0 (no stock received yet)

---

## 📊 **STEP 3: ACTIVATE PRODUCTS**

### **3.1 Activate Template**
- Go to Product Template
- Click **Activate** button
- **Status**: Template becomes active

### **3.2 Activate Variants**
- Go to each Product Variant
- Click **Activate** button
- **Status**: Variant becomes available for sales/purchases

---

## 📦 **STEP 4: RECEIVE INITIAL STOCK (PURCHASE)**

### **4.1 Create Purchase Order**
- **Menu**: Purchase → Purchase Orders → Create
- **Supplier**: Select supplier with location data

### **4.2 Add Purchase Lines**
```yaml
# Purchase Line 1
Product: "685686043632" (Barcode)
Quantity: "10"
Cost Price: "843.79"
GST Treatment: "Included"  # or "Excluded"
GST Rate: "5.00"
```

### **4.3 GST Calculation (Inter-state Example)**
```yaml
Company: Maharashtra, Supplier: Gujarat
Base Amount: ₹8,437.90
CGST: ₹0.00, SGST: ₹0.00
IGST: ₹421.90 (5%)
Total: ₹8,859.80
```

### **4.4 Receive Purchase**
- Click **Receive** button
- **Inventory Update**: +10 units
- **Status**: Purchase completed

---

## 🛒 **STEP 5: SELL PRODUCTS (POS/SALES)**

### **5.1 POS Transaction**
- **Menu**: POS → New Session → Start
- **Customer**: Select customer (mandatory)

### **5.2 Scan Product**
- **Barcode Scanner**: Scan "685686043632"
- **Product**: Boys Blue Slim Fit Stretchable Jeans - Size 18
- **MRP**: ₹1,499.00
- **GST Rate**: 5%

### **5.3 Apply Discount (Optional)**
```yaml
Discount Type: "Percentage"
Discount Rate: "10%"
Discount Amount: ₹149.90
Discounted Price: ₹1,349.10
```

### **5.4 GST Calculation (POS - Intra-state)**
```yaml
Final Price: ₹1,349.10
Base Amount: ₹1,284.86
CGST: ₹32.12 (2.5%)
SGST: ₹32.12 (2.5%)
IGST: ₹0.00
Total GST: ₹64.24
```

### **5.5 Process Payment**
```yaml
Payment Method: "Cash"
Amount Received: ₹1,349.10
Change: ₹0.00
```

### **5.6 Complete Sale**
- Click **Pay** button
- **Inventory Update**: -1 unit
- **Receipt Generated**: With complete GST breakdown

---

## 📈 **STEP 6: INVENTORY TRACKING**

### **6.1 Real-time Inventory Updates**
```yaml
Initial Stock: 0 units
After Purchase: +10 units
After Sale: -1 unit
Current Stock: 9 units
```

### **6.2 Inventory Reports**
- **Menu**: Inventory → Stock Reports → Product Quantities
- **View**: Real-time stock levels by variant
- **Alerts**: Low stock notifications

---

## 🔄 **STEP 7: BULK IMPORT WORKFLOW**

### **7.1 Prepare Import Data**
```csv
StyleCode,Product Name,Description,Brand,Category,Sub Category,Gender,HSN Code
121246526864,Boys Blue Slim Fit Stretchable Jeans,5000 Boys Blue Slim Fit Stretchable Jeans,GINI AND JONY,BOTTOM,JEANS,BOYS,6203
```

### **7.2 Import Product Templates**
- **Menu**: Tools → Bulk Import → Product Templates
- **Template**: Select "Product Template Import"
- **File**: Upload Excel/CSV file
- **Validation**: Check required fields

### **7.3 Import Product Variants**
```csv
StyleCode,Barcode,EAN Code,Size,Shade,MRP,Cost Price,GST Rate
121246526864,685686043632,8907936912167,18,BLUE,1499.00,843.79,5.00
121246526864,685686043633,8907936912174,20,BLUE,1499.00,843.79,5.00
121246526864,685686043634,8907936912181,22,BLUE,1499.00,843.79,5.00
```

### **7.4 Import Variants**
- **Menu**: Tools → Bulk Import → Product Variants
- **Template**: Select "Product Variant Import"
- **File**: Upload Excel/CSV file
- **Validation**: Check barcode uniqueness

---

## 🎯 **KEY FEATURES OF NEW WORKFLOW**

### **✅ GST Integration**
- **HSN Code**: Product classification
- **GST Rate**: Product-specific rates
- **Location-Based**: Intra-state vs Inter-state calculation
- **Treatment**: Included/Excluded options

### **✅ Retail-Specific**
- **StyleCode**: Product template with multiple variants
- **Barcode**: Unique identifier per variant
- **EAN Code**: International product code
- **Size/Shade**: Variant attributes
- **MRP**: Maximum Retail Price
- **Cost Price**: Purchase price

### **✅ Inventory Management**
- **Real-time Updates**: Purchase increase, Sale decrease
- **Stock Validation**: Insufficient inventory checks
- **Cost Tracking**: Cost price integration
- **Location Support**: Multiple warehouse support

### **✅ Bulk Operations**
- **Template Import**: Excel/CSV support
- **Variant Import**: Batch variant creation
- **Validation**: Data integrity checks
- **Error Handling**: Import error reporting

---

## 📋 **WORKFLOW SUMMARY**

### **Complete Item Creation Process:**
1. **Create Product Template** (StyleCode) with GST fields
2. **Create Product Variants** (Barcodes) with MRP, cost price, GST rate
3. **Activate Products** for sales/purchases
4. **Receive Stock** via purchase orders
5. **Sell Products** via POS/sales with GST calculation
6. **Track Inventory** in real-time
7. **Bulk Import** for mass data entry

### **GST Calculation Examples:**
- **POS (Intra-state)**: CGST + SGST
- **Sales (Inter-state)**: IGST
- **Purchase (Inter-state)**: IGST with Input Tax Credit

### **Inventory Flow:**
- **Purchase**: Inventory increases
- **Sale/POS**: Inventory decreases
- **Purchase Return**: Inventory decreases
- **Sale Return**: Inventory increases

---

## 🎉 **RESULT**

Your Ocean ERP now has a **complete, professional-grade item workflow** that supports:

✅ **Modern ERP Structure** - Template → Variant architecture
✅ **Complete GST Compliance** - Indian tax system integration
✅ **Retail-Specific Features** - Barcode, MRP, size, shade
✅ **Real-time Inventory** - Automatic stock tracking
✅ **Bulk Import** - Mass data entry capabilities
✅ **Location-Based GST** - Intra-state vs Inter-state
✅ **Professional Workflow** - Step-by-step item creation

**Your Ocean ERP is now ready for professional retail operations!** 🌊💰📊🇮🇳