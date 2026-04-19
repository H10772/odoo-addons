from unittest.mock import patch, MagicMock
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestPayTabsPayment(TransactionCase):

    def setUp(self):
        super().setUp()
        
        self.provider = self.env['payment.provider'].create({
            'name': 'PayTabs Test',
            'code': 'paytabs',
            'state': 'test',
            'paytabs_profile_id': '12345',
            'paytabs_server_key': 'test_server_key_1234567890',
        })
        
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@example.com',
            'phone': '+201234567890',
            'street': 'Test Street',
            'city': 'Cairo',
            'zip': '11511',
            'country_id': self.env.ref('base.eg').id,
        })
        
        self.currency = self.env.ref('base.EGP')

    def test_provider_creation(self):
        self.assertEqual(self.provider.code, 'paytabs')
        self.assertEqual(self.provider.paytabs_profile_id, '12345')
        self.assertTrue(self.provider.paytabs_server_key)

    def test_supported_currencies(self):
        supported = self.provider._get_supported_currencies()
        supported_names = supported.mapped('name')
        
        self.assertIn('EGP', supported_names)
        self.assertIn('USD', supported_names)
        self.assertIn('EUR', supported_names)

    def test_profile_id_validation(self):
        with self.assertRaises(ValidationError):
            self.provider.write({'paytabs_profile_id': 'invalid_id'})

    def test_server_key_validation(self):
        with self.assertRaises(ValidationError):
            self.provider.write({'paytabs_server_key': 'short'})

    def test_inline_form_disabled(self):
        result = self.provider._should_build_inline_form()
        self.assertFalse(result)

    def test_default_payment_method_codes(self):
        codes = self.provider._get_default_payment_method_codes()
        self.assertIn('paytabs', codes)

    @patch('odoo.addons.payment_paytabs.models.payment_transaction.requests.post')
    def test_payment_request_creation(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'redirect_url': 'https://secure-egypt.paytabs.com/payment/page/123',
            'tran_ref': 'TST123456789'
        }
        mock_post.return_value = mock_response
        
        tx = self.env['payment.transaction'].create({
            'provider_id': self.provider.id,
            'reference': 'TEST-TX-001',
            'amount': 100.0,
            'currency_id': self.currency.id,
            'partner_id': self.partner.id,
        })
        
        processing_values = {'reference': 'TEST-TX-001'}
        rendering_values = tx._get_specific_rendering_values(processing_values)
        
        self.assertTrue(mock_post.called)
        self.assertIn('api_url', rendering_values)
        self.assertTrue(rendering_values['api_url'].startswith('https://'))

    def test_transaction_reference_extraction(self):
        tx = self.env['payment.transaction'].create({
            'provider_id': self.provider.id,
            'reference': 'TEST-TX-002',
            'amount': 200.0,
            'currency_id': self.currency.id,
            'partner_id': self.partner.id,
        })
        
        notification_data = {'cart_id': 'TEST-TX-002'}
        found_tx = self.env['payment.transaction']._get_tx_from_notification_data(
            'paytabs', notification_data
        )
        self.assertEqual(found_tx.id, tx.id)

    def test_transaction_status_approved(self):
        tx = self.env['payment.transaction'].create({
            'provider_id': self.provider.id,
            'reference': 'TEST-TX-003',
            'amount': 300.0,
            'currency_id': self.currency.id,
            'partner_id': self.partner.id,
            'state': 'pending',
        })
        
        notification_data = {
            'cart_id': 'TEST-TX-003',
            'payment_result': {
                'response_status': 'A',
                'response_message': 'Approved'
            },
            'tran_ref': 'TST987654321'
        }
        
        tx._process_notification_data(notification_data)
        
        self.assertEqual(tx.state, 'done')
        self.assertEqual(tx.provider_reference, 'TST987654321')

    def test_transaction_status_declined(self):
        tx = self.env['payment.transaction'].create({
            'provider_id': self.provider.id,
            'reference': 'TEST-TX-004',
            'amount': 400.0,
            'currency_id': self.currency.id,
            'partner_id': self.partner.id,
            'state': 'pending',
        })
        
        notification_data = {
            'cart_id': 'TEST-TX-004',
            'payment_result': {
                'response_status': 'D',
                'response_message': 'Declined'
            }
        }
        
        tx._process_notification_data(notification_data)
        self.assertEqual(tx.state, 'error')

    def test_missing_reference_error(self):
        with self.assertRaises(ValidationError):
            self.env['payment.transaction']._get_tx_from_notification_data(
                'paytabs', {}
            )

    @patch('odoo.addons.payment_paytabs.models.payment_transaction.requests.post')
    def test_refund_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'payment_result': {
                'response_status': 'A',
                'response_message': 'Refund Approved'
            },
            'tran_ref': 'REF123456789'
        }
        mock_post.return_value = mock_response
        
        tx = self.env['payment.transaction'].create({
            'provider_id': self.provider.id,
            'reference': 'TEST-TX-005',
            'amount': 500.0,
            'currency_id': self.currency.id,
            'partner_id': self.partner.id,
            'state': 'done',
            'provider_reference': 'TST111222333',
        })
        
        refund_tx = tx._send_refund_request(amount_to_refund=500.0)
        
        self.assertTrue(refund_tx)
        self.assertEqual(refund_tx.operation, 'refund')
