from . import models
from . import controllers


def _post_init_hook(env):
    """ Create the account.payment.method for PayTabs and link it to the provider's journal. """
    # Ensure the account.payment.method record exists for 'paytabs'
    payment_method = env['account.payment.method'].search(
        [('code', '=', 'paytabs'), ('payment_type', '=', 'inbound')], limit=1
    )
    if not payment_method:
        payment_method = env['account.payment.method'].create({
            'name': 'PayTabs Egypt',
            'code': 'paytabs',
            'payment_type': 'inbound',
        })

    # Link the payment method to the provider's journal
    provider = env['payment.provider'].search([('code', '=', 'paytabs')], limit=1)
    if provider:
        provider._ensure_payment_method_line()