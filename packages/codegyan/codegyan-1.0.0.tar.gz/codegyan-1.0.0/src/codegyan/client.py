from .compiler import CompilerApiClient  # Import the CompilerApiClient class from .compiler module
from .tools import ToolsApiClient  # Import the ToolsApiClient class from .tools module

class Codegyan:
    def __init__(self, api_key, client_id):
        # Initialize the Codegyan API client with API key and client ID.

        # Args:
        # - api_key (str): The API key for authentication.
        # - client_id (str): The client ID for identification.
        self.api_key = api_key
        self.client_id = client_id

        # Initialize the instances
        self.compilerApiClient = CompilerApiClient(self.api_key, self.client_id)
        self.toolsApiClient = ToolsApiClient(self.api_key, self.client_id)
