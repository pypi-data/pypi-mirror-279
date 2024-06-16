import requests

class CompilerApiClient:
    def __init__(self, api_key, client_id):
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = 'https://api.codegyan.in/v2/compiler'

    def compile(self, lang, code):
        url = f'{self.base_url}/compile'
        headers = {
            'APIKey': self.api_key,
            'ClientID': self.client_id
        }
        data = {
            'language': lang,
            'code': code
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
