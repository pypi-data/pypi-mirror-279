import requests
from .exceptions import BemFacilPaymentError, AuthorizationError, InvalidTransactionError


class BemFacilPaymentClient:
    """
    Initializes the BemFacilPaymentClient with the provided username, password, and base URL.
    If no base URL is provided, it defaults to 'https://gws-hml.bemfacil.com.br'.

    Usage:
        client = BemFacilPaymentClient(username, password)

    Parameters:
        username (str): The username for authentication.
        password (str): The password for authentication.
        base_url (str): The base URL for the BemFacil API (default is 'https://gws-hml.bemfacil.com.br').

    Returns:
        None
    """

    def __init__(self, username, password, base_url='https://gws-hml.bemfacil.com.br'):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.api_key = None
        self.refresh_token = None
        self.authenticate()

    def _headers(self):
        """
        Generates and returns the headers required for API requests including Authorization and Content-Type.
        """
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _post(self, endpoint, payload, headers=None):
        """
        Sends a POST request to the specified endpoint with the given payload.

        Parameters:
            endpoint (str): The endpoint to send the POST request to.
            payload (dict): The data to be sent in the POST request.
            headers (dict, optional): Additional headers to include in the request (default is None).

        Returns:
            dict: The JSON response from the POST request.
        """
        url = f'{self.base_url}{endpoint}'
        response = requests.post(url, json=payload, headers=headers or self._headers())
        if response.status_code not in [200, 201]:
            self._handle_error(response)
        return response.json()

    def _put(self, endpoint, payload):
        """
        Sends a PUT request to the specified endpoint with the given payload.

        Parameters:
            endpoint (str): The endpoint to send the PUT request to.
            payload (dict): The data to be sent in the PUT request.

        Returns:
            dict: The JSON response from the PUT request.
        """
        url = f'{self.base_url}{endpoint}'
        response = requests.put(url, json=payload, headers=self._headers())
        if response.status_code not in [200, 201]:
            self._handle_error(response)
        return response.json()

    def _get(self, endpoint):
        """
        Sends a GET request to the specified endpoint with the given URL.

        Parameters:
            endpoint (str): The endpoint to send the GET request to.

        Returns:
            dict: The JSON response from the GET request.
        """
        url = f'{self.base_url}{endpoint}'
        response = requests.get(url, headers=self._headers())
        if response.status_code != 200:
            self._handle_error(response)
        return response.json()

    def _handle_error(self, response):
        """
        Handles different error codes in the response and raises specific errors accordingly.

        Parameters:
            response: The response object containing the error code and message.

        Raises:
            InvalidTransactionError: If the response status code is 400.
            BemFacilPaymentError: If the response status code is 500.
            BemFacilPaymentError: If the response status code is neither 400 nor 500.
        """
        if response.status_code == 400:
            raise InvalidTransactionError(response.json().get('message', 'Bad Request'))
        elif response.status_code == 500:
            raise BemFacilPaymentError(response.json().get('message', 'Internal Server Error'))
        else:
            raise BemFacilPaymentError(response.json().get('message', 'Unknown error occurred'))

    def authenticate(self):
        """
        Sends a request to authenticate the user with the provided username and password.

        Raises:
            AuthorizationError: If the authentication fails.

        Parameters:
            None

        Returns:
            None
        """
        url = f'{self.base_url}/auth'
        payload = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise AuthorizationError(response.json().get('message', 'Authentication failed'))
        data = response.json()
        auth_result = data.get('result').get('AuthenticationResult')
        self.api_key = auth_result.get('AccessToken')
        self.refresh_token = auth_result.get('RefreshToken')

    def refresh_auth_token(self):
        """
        Sends a request to refresh the authentication token using the current refresh token.

        Parameters:
            None

        Returns:
            None
        """
        url = f'{self.base_url}/auth/refresh-token'
        payload = {'token': self.refresh_token}
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise AuthorizationError(response.json().get('message', 'Token refresh failed'))
        self.api_key = response.json().get('access_token')

    def tokenize_card(self, card_number, card_expiry, card_holder_data):
        """
        Sends a request to tokenize a card with the provided card number, expiry date, and card holder data.

        Parameters:
            card_number (str): The card number to tokenize.
            card_expiry (str): The expiry date of the card.
            card_holder_data (dict): The data of the card holder including first name, last name, birth day, phone, email, and address.

        Usage:
            bf_client.tokenize_card("5555666677778884", "12/25", {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": "01/01/1970",
                "phone": "+5511999999999"})

        Returns:
            dict: The JSON response from the POST request to tokenize the card.
        """
        endpoint = '/cards'
        payload = {
            'card': {
                'number': card_number,
                'expiry_date': card_expiry,
                'owner': card_holder_data
            }
        }
        return self._post(endpoint, payload)

    def create_transaction(self, document, amount, payment_method, installments):
        """
        Sends a request to create a transaction with the provided document, amount, payment method, and installments.

        Parameters:
            document (str): The document associated with the transaction.
            amount (int): The amount of the transaction.
            payment_method (str): The payment method used for the transaction.
            installments (int): The number of installments for the transaction.

        Returns:
            dict: The JSON response from the POST request to create the transaction.
        """
        endpoint = '/transaction'
        payload = {
            'document': document,
            'amount': amount,
            'payment_method': payment_method,
            'installments': installments
        }
        return self._post(endpoint, payload)

    def capture_payment(self, transaction_id, card):
        """
        Sends a request to capture a payment for the provided transaction ID using the specified card.

        Parameters:
            transaction_id (str): The ID of the transaction to capture the payment for.
            card (dict): The card details to be used for the payment.

        Returns:
            dict: The JSON response from the PUT request to capture the payment.
        """
        endpoint = f'/transaction/pay/{transaction_id}'
        payload = {'card': card}
        return self._put(endpoint, payload)

    def get_transaction_status(self, transaction_id):
        """
        Sends a request to get the status of a transaction based on the provided transaction ID.

        Parameters:
            transaction_id (str): The ID of the transaction to retrieve the status for.

        Returns:
            dict: The JSON response from the GET request to retrieve the transaction status.
        """
        endpoint = f'/transaction/{transaction_id}'
        return self._get(endpoint)

    def change_password(self, new_password):
        """
        Sends a request to change the user's password to the provided new_password.

        Parameters:
            new_password (str): The new password to set for the user.

        Returns:
            dict: The JSON response from the PUT request to change the password.
        """
        endpoint = '/auth/change-password'
        payload = {'new_password': new_password}
        return self._put(endpoint, payload)
