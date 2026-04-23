# PayTabs Payment Provider for Odoo 17

## Overview

This module integrates PayTabs payment gateway with Odoo 17, enabling customers to pay for orders using credit and debit cards through PayTabs Egypt secure payment platform.

## Features

- Secure payment processing via PayTabs Egypt
- Support for multiple currencies (EGP, USD, EUR, GBP, SAR)
- Redirect-based payment flow
- Real-time payment verification
- Automatic transaction status updates
- Full and partial refund support
- Server-to-server callback notifications
- Compatible with Odoo 17 payment architecture

## Requirements

- Odoo 17.0 or higher
- Active PayTabs Egypt merchant account
- PayTabs Profile ID and Server Key
- SSL certificate (HTTPS) for production use

## Installation

1. Copy the module to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the "PayTabs Payment Provider" module

## Configuration

### Step 1: Obtain PayTabs Credentials

1. Log in to your PayTabs merchant dashboard
2. Navigate to Developers > API Keys
3. Copy your Profile ID and Server Key

### Step 2: Configure in Odoo

1. Go to Invoicing/Accounting > Configuration > Payment Providers
2. Open the PayTabs Egypt provider
3. Fill in the required fields:
   - Profile ID: Your PayTabs Profile ID
   - Server Key: Your PayTabs Server Key
   - Multi-Currency Support: Enable only if your PayTabs account supports multiple currencies
4. Set the state to "Enabled"
5. Save the configuration

### Step 3: Test the Integration

1. Create a test sales order or invoice
2. Proceed to checkout on your website
3. Select PayTabs as the payment method
4. Complete the payment on the PayTabs page
5. Verify the transaction status in Odoo

## Usage

### For Customers

1. Select "Credit Card (PayTabs)" as payment method during checkout
2. Click "Pay Now"
3. Complete payment on PayTabs secure page
4. Return to the store after payment

### For Administrators

#### View Transactions

Navigate to Invoicing > Payments > Transactions and filter by provider "PayTabs"

#### Process Refunds

1. Open the payment transaction
2. Click the "Refund" button
3. Enter the refund amount (full or partial)
4. Confirm the refund

## Supported Currencies

**Default:** EGP (Egyptian Pound)

**Optional Multi-Currency Support:**
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- SAR (Saudi Riyal)

**Important Notes:**
- Most PayTabs Egypt accounts support EGP only by default
- Multi-currency support requires special activation from PayTabs
- Contact PayTabs support to enable multi-currency on your account
- Enable the "Multi-Currency Support" option in provider settings after activation

## Technical Details

### API Endpoints

- Payment Request: https://secure-egypt.paytabs.com/payment/request
- Payment Query: https://secure-egypt.paytabs.com/payment/query

### Callback URLs

The module automatically configures these URLs:
- Return URL: /payment/paytabs/return
- Callback URL: /payment/paytabs/callback

### Transaction States

- Draft: Transaction created but not yet processed
- Pending: Payment initiated, waiting for confirmation
- Done: Payment successful
- Canceled: Payment canceled by user
- Error: Payment failed or declined

## Troubleshooting

### Payment Not Processing

- Verify PayTabs credentials are correct
- Ensure the payment provider is enabled
- Check Odoo logs for error messages
- Confirm server can reach PayTabs API

### Callback Not Working

- Verify server is publicly accessible
- Check firewall settings
- Ensure callback URL is not blocked

### Currency Not Supported

- Only EGP, USD, EUR, GBP, and SAR are supported
- Configure pricelist to use supported currencies
- Check if multi-currency is enabled in provider settings

## Support

For issues related to:
- Module functionality: Contact the module author
- PayTabs account: Contact PayTabs support at support@paytabs.com
- Odoo configuration: Refer to Odoo documentation

## Credits

Author: Hager Mohamed  
Version: 17.0.1.0.0  
License: LGPL-3

For detailed version history, see CHANGELOG.md
