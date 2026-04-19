# Changelog

All notable changes to the PayTabs Payment Provider module will be documented in this file.

## [17.0.1.0.0] - 2024-04-19

### Added
- Initial release for Odoo 17
- Payment processing via PayTabs Egypt API
- Support for multiple currencies (EGP, USD, EUR, GBP, SAR)
- Redirect-based payment flow
- Real-time transaction verification
- Automatic transaction status updates
- Server-to-server callback notifications
- Return URL handling for customer redirects
- Refund support (full and partial refunds)
- Comprehensive error handling and logging
- Input validation for Profile ID and Server Key
- Multi-currency configuration option
- Arabic translation
- Complete documentation
- Unit tests for core functionality

### Security
- Server Key stored securely with password field
- HTTPS-only communication with PayTabs API
- Transaction verification via API query
- Proper authentication handling

### Technical Details
- Compatible with Odoo 17.0
- Follows Odoo payment provider architecture
- Uses PayTabs Egypt API endpoints
- Implements payment.provider and payment.transaction models
- Includes post-installation hook for setup
