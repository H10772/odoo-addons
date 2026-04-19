# Odoo Addons

Collection of custom Odoo modules.

## Available Modules

### Odoo 17

#### PayTabs Egypt Payment Gateway
Payment gateway integration for PayTabs Egypt.

**Technical Name:** `payment_paytabs_eg`

**Features:**
- Secure payment processing via PayTabs Egypt
- Support for Egyptian Pound (EGP) and multi-currency (USD, EUR, GBP, SAR)
- Full and partial refund support
- Real-time transaction verification
- Server-to-server callbacks
- PCI-DSS compliant
- Arabic translation included

**Installation:**
```bash
git clone -b 17.0 https://github.com/H10772/odoo-addons.git
cp -r odoo-addons/payment_paytabs_eg /path/to/odoo/addons/
```

**Documentation:** See [payment_paytabs_eg/README.md](payment_paytabs_eg/README.md)

## Branches

- `odoo-17` - Modules for Odoo 17
- `main` - General information

## License

Each module has its own license. See individual module directories for details.
