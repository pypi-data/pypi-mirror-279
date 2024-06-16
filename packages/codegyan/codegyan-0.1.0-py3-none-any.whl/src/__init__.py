# codegyan/__init__.py

# Import the main class or functions that you want to expose directly when the package is imported
from .client import Codegyan

# Optionally, you can import specific API clients if needed
# from .compiler import CodeGyanCompilerApiClient
# from .tools import CodeGyanToolsApiClient
# from .articles import CodeGyanArticlesApiClient

# List what should be imported when using "from codegyan import *"
__all__ = ['Codegyan']
