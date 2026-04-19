{
    'name': 'PayTabs Payment Provider',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Accept payments via PayTabs Egypt - EGP & Multi-Currency Support',
    'description': """
PayTabs Payment Provider for Odoo 17
=====================================

Accept secure online payments through PayTabs Egypt payment gateway.

Key Features:
-------------
* Secure payment processing via PayTabs Egypt
* Support for Egyptian Pound (EGP) - default for all accounts
* Optional multi-currency support (USD, EUR, GBP, SAR)
* Redirect-based payment flow
* Real-time payment verification
* Automatic transaction status updates
* Full and partial refund support
* Server-to-server callback notifications
* PCI-DSS compliant payment processing
* Mobile-responsive payment experience

Requirements:
-------------
* Active PayTabs Egypt merchant account
* PayTabs Profile ID and Server Key
* SSL certificate (HTTPS) for production

Quick Setup:
------------
1. Install the module from Odoo Apps
2. Go to Invoicing → Configuration → Payment Providers
3. Open PayTabs Egypt provider
4. Enter your Profile ID and Server Key
5. Enable multi-currency if your account supports it
6. Enable the provider and test with a sample transaction

Currency Support:
-----------------
* EGP (Egyptian Pound) - Supported by default on all accounts
* Multi-currency (USD, EUR, GBP, SAR) - Requires activation from PayTabs
* Contact PayTabs support to enable multi-currency on your account

Support:
--------
For technical support, contact the module author.
For PayTabs account issues, contact support@paytabs.com

For detailed documentation, see README.md in the module directory.
    """,
    'author': 'Hager Mohamed',
    'website': '',
    'maintainer': 'Hager Mohamed',
    'support': '',
    'depends': ['payment', 'account_payment'],
    'data': [
        'views/payment_paytabs_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
    ],
    'assets': {},
    'images': ['static/description/icon.png', 'static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': '_post_init_hook',
    'license': 'LGPL-3',
    'price': 0.00,
    'currency': 'EUR',
}