import unittest
from bf_sdk_gateway_python.client import BemFacilPaymentClient
from unittest.mock import patch

from bf_sdk_gateway_python.exceptions import InvalidTransactionError, BemFacilPaymentError


class TestBemFacilPaymentClient(unittest.TestCase):
    def setUp(self):
        self.client = BemFacilPaymentClient(username='daniel.nascimento@bemfacil.com.br', password='BemFacil2024@')

    @patch('bf_sdk_gateway_python.client.requests.post')
    def test_authenticate(self, mock_post):
        mock_post.return_value.json.return_value = {'access_token': 'test_token', 'refresh_token': 'refresh_token'}
        mock_post.return_value.status_code = 200

        self.client.authenticate()
        self.assertEqual(self.client.api_key, 'test_token')
        self.assertEqual(self.client.refresh_token, 'refresh_token')

    @patch('bf_sdk_gateway_python.client.requests.post')
    def test_tokenize_card(self, mock_post):
        mock_post.return_value.json.return_value = {'token': 'card_token'}
        mock_post.return_value.status_code = 200

        response = self.client.tokenize_card('5555666677778884', '12/25')
        self.assertIn('token', response)

    @patch('bf_sdk_gateway_python.client.requests.post')
    def test_tokenize_card_bad_request(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {'message': 'Bad Request'}

        with self.assertRaises(InvalidTransactionError) as context:
            self.client.tokenize_card('invalid_card', '12/25')
        self.assertEqual(str(context.exception), 'Bad Request')

    @patch('bf_sdk_gateway_python.client.requests.post')
    def test_tokenize_card_server_error(self, mock_post):
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {'message': 'Internal Server Error'}

        with self.assertRaises(BemFacilPaymentError) as context:
            self.client.tokenize_card('5555666677778884', '12/25')
        self.assertEqual(str(context.exception), 'Internal Server Error')

    @patch('bf_sdk_gateway_python.client.requests.post')
    def test_create_transaction(self, mock_post):
        mock_post.return_value.json.return_value = {'transaction_id': '12345'}
        mock_post.return_value.status_code = 200

        response = self.client.create_transaction('40404040411', 10, 'credit', 1)
        self.assertIn('transaction_id', response)

    @patch('bf_sdk_gateway_python.client.requests.put')
    def test_capture_payment(self, mock_put):
        mock_put.return_value.json.return_value = {'message': 'Payment captured successfully'}
        mock_put.return_value.status_code = 200

        response = self.client.capture_payment('12345')
        self.assertEqual(response['message'], 'Payment captured successfully')

    @patch('bf_sdk_gateway_python.client.requests.get')
    def test_get_transaction_status(self, mock_get):
        mock_get.return_value.json.return_value = {'status': 'approved'}
        mock_get.return_value.status_code = 200

        response = self.client.get_transaction_status('12345')
        self.assertEqual(response['status'], 'approved')

    @patch('bf_sdk_gateway_python.client.requests.put')
    def test_change_password(self, mock_put):
        mock_put.return_value.json.return_value = {'message': 'Password updated successfully'}
        mock_put.return_value.status_code = 200

        response = self.client.change_password('new_password123')
        self.assertEqual(response['message'], 'Password updated successfully')

    @patch('bf_sdk_gateway_python.client.requests.post')
    def test_refresh_auth_token(self, mock_post):
        mock_post.return_value.json.return_value = {'access_token': 'new_test_token'}
        mock_post.return_value.status_code = 200

        self.client.refresh_auth_token()
        self.assertEqual(self.client.api_key, 'new_test_token')


if __name__ == '__main__':
    unittest.main()
