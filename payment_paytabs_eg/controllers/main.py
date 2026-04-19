import logging
import pprint
import requests as py_requests
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayTabsController(http.Controller):
    _return_url = '/payment/paytabs/return'
    _callback_url = '/payment/paytabs/callback'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def paytabs_return(self, **data):
        _logger.info("PayTabs return data received: %s", pprint.pformat(data))

        tran_ref = data.get('tranRef') or data.get('tran_ref')
        cart_id = data.get('cartId') or data.get('cart_id')

        if tran_ref or cart_id:
            tx_sudo = self._find_transaction(cart_id, tran_ref)

            if tx_sudo and tx_sudo.state in ('draft', 'pending'):
                verified_data = self._verify_paytabs_payment(tx_sudo.provider_id, tran_ref)
                if verified_data:
                    request.env['payment.transaction'].sudo()._handle_notification_data(
                        'paytabs', verified_data
                    )
                elif data:
                    request.env['payment.transaction'].sudo()._handle_notification_data(
                        'paytabs', data
                    )
            elif data:
                request.env['payment.transaction'].sudo()._handle_notification_data(
                    'paytabs', data
                )

        return request.redirect('/payment/status')

    @http.route(_callback_url, type='http', auth='public', methods=['POST'], csrf=False)
    def paytabs_callback(self, **data):
        _logger.info("PayTabs callback data received: %s", pprint.pformat(data))

        if data:
            request.env['payment.transaction'].sudo()._handle_notification_data('paytabs', data)

        return request.make_json_response('')

    def _find_transaction(self, cart_id, tran_ref):
        tx_sudo = None
        if cart_id:
            tx_sudo = request.env['payment.transaction'].sudo().search(
                [('reference', '=', cart_id), ('provider_code', '=', 'paytabs')], limit=1
            )
        if not tx_sudo and tran_ref:
            tx_sudo = request.env['payment.transaction'].sudo().search(
                [('provider_reference', '=', tran_ref), ('provider_code', '=', 'paytabs')], limit=1
            )
        return tx_sudo

    def _verify_paytabs_payment(self, provider, tran_ref):
        if not tran_ref:
            return None

        try:
            response = py_requests.post(
                "https://secure-egypt.paytabs.com/payment/query",
                json={
                    "profile_id": int(provider.paytabs_profile_id),
                    "tran_ref": tran_ref,
                },
                headers={
                    "authorization": provider.paytabs_server_key,
                    "Content-Type": "application/json",
                },
                timeout=15,
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            _logger.error("PayTabs verify API error: %s", e)
            return None
