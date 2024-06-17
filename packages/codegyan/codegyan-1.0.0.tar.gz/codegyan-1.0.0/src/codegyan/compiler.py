import requests

class CompilerApiClient:
    def __init__(self, api_key, client_id):
        # Initialize the CompilerApiClient with API key and client ID.

        # Args:
        # - api_key (str): The API key for authentication.
        # - client_id (str): The client ID for identification.
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = 'https://api.codegyan.in/v2/compiler'

    def compile(self, lang, code):
        # Compile code using the CodeGyan Compiler API.

        # Args:
        # - lang (str): The programming language of the code (e.g., 'python').
        # - code (str): The code to compile.

        # Returns:
        # - dict: JSON response from the API

        url = f'{self.base_url}/compile'
        headers = {
            'APIKey': self.api_key,
            'ClientID': self.client_id
        }
        data = {
            'lang': lang,
            'code': code
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
