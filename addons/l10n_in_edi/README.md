# Ocean ERP - Indian EDI Addon

## Overview

The `l10n_in_edi` addon provides comprehensive EDI (Electronic Data Interchange) compliance for the Ocean ERP system, specifically designed for kids clothing retail businesses in India. This addon extends the core framework with Indian EDI-specific models, views, and functionality.

## Features

### 📄 Document Management
- **Document Types**: Invoice, Credit Note, Debit Note, Purchase Order, Sales Order, Delivery Note, Receipt, Payment, Remittance
- **EDI Formats**: EDIFACT, X12, XML, JSON, CSV, Custom formats
- **Document Workflow**: Draft → Ready → Sent → Received → Processed
- **Kids Clothing Integration**: Age groups, sizes, seasons, brands, colors

### 💬 Message Management
- **Message Types**: ORDERS Response, ORDERS Report, DESADV, INVOIC, Credit Note, Debit Note, REMDV, Payment Multiple
- **Message Formats**: EDIFACT, X12, XML, JSON, CSV, Custom formats
- **Message Workflow**: Draft → Ready → Sent → Received → Processed
- **Kids Clothing Integration**: Message-specific kids clothing data

### 📡 Transmission Management
- **Transmission Types**: Send, Receive, Bidirectional
- **Protocols**: FTP, SFTP, HTTP, HTTPS, AS2, Email, API, Other
- **Transmission Workflow**: Draft → Ready → Sending → Sent → Received → Processing → Processed
- **Connection Management**: Host, Port, Authentication
- **Kids Clothing Integration**: Transmission-specific kids clothing data

### ✅ Acknowledgment Management
- **Acknowledgment Types**: Technical Acknowledgment, Functional Acknowledgment, Usage Acknowledgment
- **Status Tracking**: Pending → Received → Processed
- **Error Handling**: Comprehensive error tracking and reporting
- **Kids Clothing Integration**: Acknowledgment-specific kids clothing data

## Models

### Core Models
- `edi.document` - EDI Document with localization
- `edi.transaction` - EDI Transaction segments
- `edi.message` - EDI Message with localization
- `edi.envelope` - EDI Envelope structure
- `edi.transmission` - EDI Transmission with localization
- `edi.acknowledgment` - EDI Acknowledgment with localization

## Kids Clothing Integration

All models include kids clothing specific fields:

### Age Groups
- Baby (0-2 years)
- Toddler (2-4 years)
- Pre-school (4-6 years)
- Early School (6-8 years)
- Middle School (8-10 years)
- Late School (10-12 years)
- Teen (12-14 years)
- Young Adult (14-16 years)
- All Age Groups

### Sizes
- XS, S, M, L, XL, XXL, XXXL
- All Sizes

### Seasons
- Summer, Winter, Monsoon
- All Season

### Brands & Colors
- Custom brand and color fields
- Integration with kids clothing business logic

## EDI Document Types

### Invoice
- Standard invoice documents
- Credit and debit notes
- Payment receipts
- Remittance advice

### Orders
- Purchase orders
- Sales orders
- Order responses
- Order reports

### Delivery
- Delivery notes
- Shipping documents
- Receipt confirmations

## EDI Formats

### EDIFACT
- United Nations standard
- International EDI format
- Segment-based structure
- Version D.96A support

### X12
- American National Standards Institute
- Transaction set based
- Interchange structure
- Version 4010 support

### XML
- Extensible Markup Language
- Human-readable format
- Schema validation
- Namespace support

### JSON
- JavaScript Object Notation
- Lightweight format
- Easy parsing
- REST API integration

### CSV
- Comma-Separated Values
- Simple format
- Excel compatibility
- Basic data exchange

## EDI Protocols

### FTP/SFTP
- File Transfer Protocol
- Secure File Transfer Protocol
- Batch processing
- File-based exchange

### HTTP/HTTPS
- Hypertext Transfer Protocol
- Secure HTTP
- Real-time processing
- Web-based exchange

### AS2
- Applicability Statement 2
- Secure messaging
- Digital signatures
- Encryption support

### Email
- Simple Mail Transfer Protocol
- Attachment-based
- Basic exchange
- SMTP integration

### API
- Application Programming Interface
- RESTful services
- Real-time integration
- JSON/XML responses

## Validation

### Document Type Validation
- Valid document types
- Format compatibility
- Business rule validation
- Real-time validation

### EDI Format Validation
- Format-specific validation
- Structure validation
- Segment validation
- Element validation

### Transmission Validation
- Protocol validation
- Host format validation
- Port range validation
- Authentication validation

## Views

### Document Views
- **Tree View**: List EDI documents with status
- **Form View**: Complete document form with workflow
- **Search View**: Advanced search with filters

### Message Views
- **Tree View**: List EDI messages with status
- **Form View**: Complete message form with workflow
- **Search View**: Advanced search with filters

### Transmission Views
- **Tree View**: List EDI transmissions with status
- **Form View**: Complete transmission form with workflow
- **Search View**: Advanced search with filters

### Acknowledgment Views
- **Tree View**: List EDI acknowledgments with status
- **Form View**: Complete acknowledgment form
- **Search View**: Advanced search with filters

## Static Assets

### CSS (`static/src/css/l10n_in_edi_style.css`)
- **EDI Document Styles**: Gradient headers, document cards
- **EDI Message Styles**: Message type badges, status indicators
- **EDI Transmission Styles**: Protocol badges, connection status
- **EDI Acknowledgment Styles**: Acknowledgment type badges
- **EDI Data Display**: Monospace formatting, data visualization
- **EDI Validation Styles**: Success, error, warning indicators
- **EDI Dashboard Styles**: Dashboard grids and cards
- **Kids Clothing Styles**: Age group, size, season badges
- **Responsive Design**: Mobile-friendly layouts
- **Animations**: Fade-in effects, hover transitions

### JavaScript (`static/src/js/l10n_in_edi_script.js`)
- **EdiDocumentManager**: Document type validation, EDI format validation
- **EdiMessageManager**: Message type validation, message format validation
- **EdiTransmissionManager**: Protocol validation, host validation, port validation
- **EdiValidationUtility**: EDI data validation, format-specific validation
- **EdiDataProcessingUtility**: EDI data processing, format-specific processing
- **Dashboard Integration**: EDI data visualization
- **Utility Functions**: EDI formatting and validation

## API Endpoints

### Document API
- `GET /api/edi/document-data` - Get EDI document data
- `POST /api/edi/prepare-document` - Prepare EDI document
- `POST /api/edi/send-document` - Send EDI document
- `POST /api/edi/process-document` - Process EDI document

### Message API
- `GET /api/edi/message-data` - Get EDI message data
- `POST /api/edi/prepare-message` - Prepare EDI message
- `POST /api/edi/send-message` - Send EDI message
- `POST /api/edi/process-message` - Process EDI message

### Transmission API
- `GET /api/edi/transmission-data` - Get EDI transmission data
- `POST /api/edi/start-transmission` - Start EDI transmission
- `POST /api/edi/complete-transmission` - Complete EDI transmission
- `POST /api/edi/process-transmission` - Process EDI transmission

### Validation API
- `POST /api/edi/validate-data` - Validate EDI data
- `POST /api/edi/validate-format` - Validate EDI format
- `POST /api/edi/validate-protocol` - Validate EDI protocol

## Installation

1. Copy the `l10n_in_edi` addon to your Ocean ERP addons directory
2. Install the addon using the Ocean ERP CLI:
   ```bash
   ocean-cli addon install l10n_in_edi
   ```
3. The addon will automatically create EDI configurations

## Dependencies

- `core_framework` - Ocean ERP core framework
- `core_base` - Base models and mixins
- `l10n_in` - Indian localization addon

## Usage

### Creating an EDI Document
```python
document_vals = {
    'name': 'Invoice Document',
    'document_type': 'invoice',
    'edi_format': 'edifact',
    'edi_version': 'D.96A',
    'age_group': '4-6',
    'size': 'm',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
}
document = self.env['edi.document'].create(document_vals)
```

### Creating an EDI Transaction
```python
transaction_vals = {
    'name': 'Line Item',
    'document_id': document.id,
    'transaction_type': 'line_item',
    'segment_type': 'LIN',
    'age_group': '4-6',
    'size': 'm',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
}
transaction = self.env['edi.transaction'].create(transaction_vals)
```

### Creating an EDI Transmission
```python
transmission_vals = {
    'name': 'FTP Transmission',
    'transmission_type': 'send',
    'protocol': 'ftp',
    'host': 'ftp.example.com',
    'port': 21,
    'username': 'user',
    'password': 'pass',
    'age_group': '4-6',
    'size': 'm',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
}
transmission = self.env['edi.transmission'].create(transmission_vals)
```

### Document Workflow
```python
# Prepare document
document.action_prepare()
# Document state: draft → ready

# Send document
document.action_send()
# Document state: ready → sent

# Process document
document.action_process()
# Document state: sent → processed
```

### Filtering by Kids Clothing Criteria
```python
# Get documents for specific age group
baby_docs = self.env['edi.document'].get_kids_clothing_documents(age_group='0-2')

# Get documents for specific size
medium_docs = self.env['edi.document'].get_kids_clothing_documents(size='m')

# Get documents for specific season
summer_docs = self.env['edi.document'].get_kids_clothing_documents(season='summer')
```

## EDI Compliance

### Document Processing
1. **Prepare Document**: Generate EDI data from business data
2. **Validate Data**: Check for errors and inconsistencies
3. **Send Document**: Transmit via EDI protocol
4. **Track Status**: Monitor transmission and processing
5. **Process Response**: Handle acknowledgments and responses

### Message Processing
1. **Create Message**: Generate EDI message structure
2. **Validate Message**: Check message format and content
3. **Transmit Message**: Send via EDI transmission
4. **Monitor Status**: Track message processing
5. **Handle Response**: Process acknowledgments

### Transmission Management
1. **Configure Connection**: Set up protocol and authentication
2. **Start Transmission**: Begin data exchange
3. **Monitor Progress**: Track transmission status
4. **Complete Transmission**: Finish data exchange
5. **Process Results**: Handle transmission results

## Testing

Run the test suite:
```bash
python -m pytest addons/l10n_in_edi/tests/
```

### Test Coverage
- Document model tests
- Transaction model tests
- Message model tests
- Transmission model tests
- Acknowledgment model tests
- Validation tests
- Workflow tests
- Kids clothing integration tests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This addon is part of the Ocean ERP system and follows the same licensing terms.

## Support

For support and questions:
- Check the Ocean ERP documentation
- Create an issue in the repository
- Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Complete EDI compliance
- Kids clothing integration
- Comprehensive validation
- EDI documents and messages
- EDI transmission and acknowledgment
- Static assets and JavaScript
- Test coverage