from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

SUPPORTED_CURRENCIES = ['EGP', 'USD', 'EUR', 'GBP', 'SAR']


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytabs_hager', "PayTabs Hager")],
        ondelete={'paytabs_hager': 'set default'}
    )
    paytabs_profile_id = fields.Char(
        string="Profile ID",
        help="The ID of your PayTabs profile."
    )
    paytabs_server_key = fields.Char(
        string="Server Key",
        help="The server key of your PayTabs profile."
    )
    paytabs_multi_currency = fields.Boolean(
        string="Multi-Currency Support",
        default=False,
        help="Enable if your PayTabs account supports multiple currencies (USD, EUR, GBP, SAR). "
             "Most PayTabs Egypt accounts support EGP only by default. "
             "Contact PayTabs to activate multi-currency if needed."
    )

    def _get_supported_currencies(self):
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'paytabs_hager':
            if not self.paytabs_multi_currency:
                supported_currencies = supported_currencies.filtered(
                    lambda c: c.name == 'EGP'
                )
            else:
                supported_currencies = supported_currencies.filtered(
                    lambda c: c.name in SUPPORTED_CURRENCIES
                )
        return supported_currencies

    def _should_build_inline_form(self, is_validation=False):
        if self.code == 'paytabs_hager':
            return False
        return super()._should_build_inline_form(is_validation=is_validation)

    def _get_default_payment_method_codes(self):
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'paytabs_hager':
            return default_codes
        return ['paytabs_hager']

    @api.constrains('paytabs_profile_id', 'paytabs_server_key')
    def _check_paytabs_credentials(self):
        for provider in self:
            if provider.code != 'paytabs_hager':
                continue
            
            if provider.paytabs_profile_id and not provider.paytabs_profile_id.isdigit():
                raise ValidationError(
                    _("PayTabs Profile ID must be a numeric value.")
                )
            
            if provider.paytabs_server_key and len(provider.paytabs_server_key) < 20:
                raise ValidationError(
                    _("PayTabs Server Key seems too short. Please check your credentials.")
                )
