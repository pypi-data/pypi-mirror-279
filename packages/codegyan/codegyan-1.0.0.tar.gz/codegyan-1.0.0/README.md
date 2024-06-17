# Codegyan Python Library

A Python library to interact with the Codegyan API.

![Language](https://img.shields.io/badge/python-3.7%2B-blue?logo=python&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/codegyan)
![PyPI - License](https://img.shields.io/pypi/l/codegyan)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Codegyan-LLC/codegyan-python/total)


## Installation

```bash
pip install codegyan
```
## Usage
Before using the Pakage, you need to obtain an API key and client ID from Codegyan. Follow these steps to get your API credentials:

1. **Sign Up/Login**: If you don't have an account, sign up for a [Codegyan account](https://codegyan.in/account/signup.php). If you already have an account, log in to your dashboard.

2. **Get Credentials**: Once logged in, navigate to the [Developer Console](https://developer.codegyan.in/) or API settings in your account dashboard. Here, you will find your API key and client ID. Copy these credentials and use them when initializing the Pakage in your code.

Here's an example of how to initialize the npm pakage with your API key and Client ID:

```python
from codegyan import Codegyan

# Define your API credentials
api_key = "YOUR API KEY"
client_id = "YOUR CLIENT ID"

# Initialize the Codegyan client
client = Codegyan(api_key, client_id)

# Define the language and code to be compiled
lang = "python"
code = 'print("Hello, World!")'

# Use the Compiler API to compile the code
result = client.compilerApiClient.compile(lang, code)
print(result)

```
Replace **YOUR_API_KEY** and **YOUR_CLIENT_ID** with your actual API key and Client ID provided by Codegyan. Pass the code you want to compile to the compile function.


## Tests
To run the unit tests, use the following command:

```
python -m unittest discover tests
```
Make sure to replace tests with the actual path to your test directory if it's different.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the **[MIT license](https://opensource.org/licenses/MIT)**. See the LICENSE file for details.