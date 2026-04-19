import logging
import requests
from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'paytabs':
            return res

        payload = self._prepare_paytabs_payment_request()
        headers = {
            "authorization": self.provider_id.paytabs_server_key,
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                "https://secure-egypt.paytabs.com/payment/request",
                json=payload,
                headers=headers,
                timeout=15
            )
            data = response.json()

            if response.status_code == 401:
                raise ValidationError(
                    _("PayTabs authentication failed. Please check your Server Key.")
                )

            if data.get('redirect_url'):
                tran_ref = data.get('tran_ref')
                if tran_ref:
                    self.provider_reference = tran_ref

                return {'api_url': data['redirect_url']}
            else:
                error_msg = data.get('message', 'Unknown error from PayTabs')
                raise ValidationError(_("PayTabs Error: %s") % error_msg)

        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(_("Could not connect to PayTabs: %s") % str(e))

    def _prepare_paytabs_payment_request(self):
        self.ensure_one()
        return {
            "profile_id": int(self.provider_id.paytabs_profile_id),
            "tran_type": "sale",
            "tran_class": "ecom",
            "cart_id": self.reference,
            "cart_currency": self.currency_id.name or "EGP",
            "cart_amount": self.amount,
            "cart_description": f"Payment for {self.reference}",
            "callback": f"{self.provider_id.get_base_url()}/payment/paytabs/callback",
            "return": f"{self.provider_id.get_base_url()}/payment/paytabs/return?ref={self.reference}",
            "customer_details": self._get_paytabs_customer_details(),
        }

    def _get_paytabs_customer_details(self):
        self.ensure_one()
        return {
            "name": self.partner_name or self.partner_id.name or "Customer",
            "email": self.partner_email or self.partner_id.email or "customer@example.com",
            "phone": self.partner_phone or self.partner_id.phone or "",
            "street1": self.partner_address or self.partner_id.street or "N/A",
            "city": self.partner_city or self.partner_id.city or "N/A",
            "state": self.partner_state_id.name if self.partner_state_id else (
                self.partner_id.state_id.name if self.partner_id.state_id else "N/A"
            ),
            "country": self.partner_country_id.code if self.partner_country_id else (
                self.partner_id.country_id.code if self.partner_id.country_id else "EG"
            ),
            "zip": self.partner_zip or self.partner_id.zip or "00000",
        }

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'paytabs' or len(tx) == 1:
            return tx

        reference = (
            notification_data.get('cart_id')
            or notification_data.get('cartId')
            or notification_data.get('ref')
        )
        if not reference:
            raise ValidationError(
                "PayTabs: " + _("Received data with missing reference.")
            )

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'paytabs')])
        if not tx:
            raise ValidationError(
                "PayTabs: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'paytabs':
            return

        payment_result = notification_data.get('payment_result', {})
        status = (
            payment_result.get('response_status')
            or notification_data.get('respStatus')
            or notification_data.get('response_status', '')
        )

        if not status and self.provider_reference:
            status, tran_ref = self._paytabs_verify_transaction()

        tran_ref = notification_data.get('tran_ref') or notification_data.get('tranRef')
        if tran_ref:
            self.provider_reference = tran_ref

        if status == 'A':
            self._set_done()
        elif status in ('D', 'E'):
            error_msg = payment_result.get('response_message', 'Payment declined')
            self._set_error(_("PayTabs: %s") % error_msg)
        elif status == 'V':
            self._set_canceled()
        else:
            self._set_pending()

    def _paytabs_verify_transaction(self):
        self.ensure_one()
        headers = {
            "authorization": self.provider_id.paytabs_server_key,
            "Content-Type": "application/json",
        }
        payload = {
            "profile_id": int(self.provider_id.paytabs_profile_id),
            "tran_ref": self.provider_reference,
        }

        try:
            response = requests.post(
                "https://secure-egypt.paytabs.com/payment/query",
                json=payload,
                headers=headers,
                timeout=15,
            )
            data = response.json()
            payment_result = data.get('payment_result', {})
            status = payment_result.get('response_status', '')
            tran_ref = data.get('tran_ref', '')

            if tran_ref:
                self.provider_reference = tran_ref

            return status, tran_ref

        except Exception:
            return '', ''

    def _send_refund_request(self, amount_to_refund=None):
        if self.provider_code != 'paytabs':
            return super()._send_refund_request(amount_to_refund=amount_to_refund)

        refund_tx = super()._send_refund_request(amount_to_refund=amount_to_refund)
        self._paytabs_refund_transaction(refund_tx, amount_to_refund)
        return refund_tx

    def _paytabs_refund_transaction(self, refund_tx, amount_to_refund):
        self.ensure_one()
        
        if not self.provider_reference:
            refund_tx._set_error(_("PayTabs: Cannot process refund - no transaction reference"))
            return

        headers = {
            "authorization": self.provider_id.paytabs_server_key,
            "Content-Type": "application/json",
        }
        
        payload = {
            "profile_id": int(self.provider_id.paytabs_profile_id),
            "tran_ref": self.provider_reference,
            "tran_type": "refund",
            "tran_class": "ecom",
            "cart_id": refund_tx.reference,
            "cart_currency": self.currency_id.name,
            "cart_amount": amount_to_refund or self.amount,
            "cart_description": f"Refund for {self.reference}",
        }

        try:
            response = requests.post(
                "https://secure-egypt.paytabs.com/payment/request",
                json=payload,
                headers=headers,
                timeout=15,
            )
            data = response.json()

            if response.status_code == 401:
                refund_tx._set_error(_("PayTabs: Refund authentication failed"))
                return

            payment_result = data.get('payment_result', {})
            status = payment_result.get('response_status', '')
            tran_ref = data.get('tran_ref', '')

            if tran_ref:
                refund_tx.provider_reference = tran_ref

            if status == 'A':
                refund_tx._set_done()
            elif status in ('D', 'E'):
                error_msg = payment_result.get('response_message', 'Refund declined')
                refund_tx._set_error(_("PayTabs Refund: %s") % error_msg)
            else:
                refund_tx._set_pending()

        except Exception as e:
            refund_tx._set_error(_("PayTabs: Refund failed - %s") % str(e))
