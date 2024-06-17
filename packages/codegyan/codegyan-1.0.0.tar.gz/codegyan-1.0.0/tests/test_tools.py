import unittest
from codegyan import Codegyan

# Define your API credentials
api_key = 'YOUR_API_KEY'
client_id = 'YOUR_CLIENT_ID'

# Define data for Domain Checker 
domain = 'example.com'

# Define data for Currency Converter
from_currency = 'your_currency' # eg: USD
to_currency = 'your_currency' # eg: INR
amount = 'your_amount'  # eg: 100

class TestToolsApiClient(unittest.TestCase):
    def setUp(self):

        # Set up the test case.

        # This method is called before each test method is executed.
        # It initializes the Codegyan client with API credentials and prepares
        # the toolsApiClient instance for testing.
        self.client = Codegyan(api_key, client_id).toolsApiClient 

    # Domain Checker
    def test_domain_check(self):
        # Test the domain_check method of ToolsApiClient.

        # This method verifies that the domain_check method of ToolsApiClient
        # returns a response containing the 'status' key after checking the domain.

        result = self.client.domain_check(domain)
        self.assertIn('status', result)

    # Currency Converter
    def test_currency(self):
        # Test the currency method of ToolsApiClient.

        # This method verifies that the currency method of ToolsApiClient
        # returns a response containing the 'converted_amount' key after converting currency.
    
        result = self.client.currency(from_currency, to_currency, amount)
        self.assertIn('converted_amount', result)

if __name__ == '__main__':
    unittest.main()

 