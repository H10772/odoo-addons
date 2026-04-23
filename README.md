# Odoo Addons

Collection of custom Odoo modules.

## Available Modules

### Odoo 17

#### PayTabs Egypt by Hager
Payment gateway integration for PayTabs Egypt.

**Technical Name:** `payment_paytabs_hager`

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
cp -r odoo-addons/payment_paytabs_hager /path/to/odoo/addons/
```

**Documentation:** See [payment_paytabs_hager/README.md](payment_paytabs_hager/README.md)

## Branches

- `17.0` - Modules for Odoo 17 (recommended)
- `odoo-17` - Modules for Odoo 17 (alternative)
- `main` - General information

## License

Each module has its own license. See individual module directories for details.
