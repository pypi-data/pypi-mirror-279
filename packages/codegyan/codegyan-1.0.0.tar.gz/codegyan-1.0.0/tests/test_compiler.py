import unittest
from codegyan import Codegyan

# Define your API credentials
api_key = 'YOUR_API_KEY'
client_id = 'YOUR_CLIENT_ID'

# Define your data for Compiler
lang = 'Enter Languege' # eg : PHP
code = 'Your code'

class TestCompilerApiClient(unittest.TestCase):
    def setUp(self):
        # Set up the test case.
        
        # This method is called before each test method is executed.
        # It initializes the Codegyan client with API credentials and prepares
        # the compilerApiClient instance for testing.

        self.client = Codegyan(api_key, client_id).compilerApiClient

    def test_compile(self):
        # Test the compile method of CompilerApiClient.

        # This method verifies that the compile method of CompilerApiClient
        # returns a response containing the 'output' key after compiling the code.
        
        result = self.client.compile(lang, code)
        self.assertIn('output', result)

if __name__ == '__main__':
    unittest.main()
