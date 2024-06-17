import requests

class ToolsApiClient:
    def __init__(self, api_key, client_id):
        # Initialize the ToolsApiClient with API key and client ID.

        # Args:
        # - api_key (str): The API key for authentication.
        # - client_id (str): The client ID for identification.
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = 'https://api.codegyan.in/v1'

    def domain_check(self, domain):
        # Perform domain check API request.

        # Args:
        # - domain (str): The domain name to check.

        # Returns:
        # - dict: JSON response from the API.
        url = f'{self.base_url}/domain-check'
        headers = {
            'APIKey': self.api_key,
            'ClientID': self.client_id
        }
        data = {
            'domain': domain
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def currency(self, from_currency, to_currency, amount):
        # Perform currency conversion API request.

        # Args:
        # - from_currency (str): The currency to convert from (e.g., 'USD').
        # - to_currency (str): The currency to convert to (e.g., 'EUR').
        # - amount (float): The amount to convert.

        # Returns:
        # - dict: JSON response from the API.
        url = f'{self.base_url}/currency'
        headers = {
            'APIKey': self.api_key,
            'ClientID': self.client_id
        }
        data = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
