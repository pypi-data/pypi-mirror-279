from .compiler import CompilerApiClient
# from .tools_api_client import ToolsApiClient
# from .articles_api_client import ArticlesApiClient

class Codegyan:
    def __init__(self, api_key, client_id):
        self.api_key = api_key
        self.client_id = client_id
        self.compilerApiClient = CompilerApiClient(self.api_key, self.client_id)
        # self.toolsApiClient = ToolsApiClient(self.api_key, self.client_id)
        # self.articlesApiClient = ArticlesApiClient(self.api_key, self.client_id)
