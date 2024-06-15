## WebSearchApi-tool Library

### Overview

`WebSearchApi` is a simple Python wrapper for the search API. It allows you to search for information using a query string and receive results in a structured format.

### Installation

To install the library, use pip:

```bash
pip install WebSearchApi
```

### Usage

Here's a step-by-step guide on how to use the `WebSearchApi` library:

1. **Import the Library**

   First, import the `SearchAPI` class from the library.

   ```python
   from WebSearchApi import SearchAPI
   ```

2. **Create an Instance of SearchAPI**

   Create an instance of the `SearchAPI` class.

   ```python
   api = SearchAPI()
   ```

3. **Perform a Search**

   Use the `search` method to perform a search with your query string.

   ```python
   results = api.search("data")
   ```

4. **Process the Results**

   The `search` method returns a list of dictionaries, each containing `title`, `snippet`, and `url` of the search results. You can iterate through the results and process them as needed.

   ```python
   for result in results:
       print(f"Title: {result['title']}")
       print(f"Snippet: {result['snippet']}")
       print(f"URL: {result['url']}")
       print()
   ```

### Example

Here's a complete example script that demonstrates how to use the `WebSearchApi-tool` library:

```python
from WebSearchApi import SearchAPI

# Create an instance of SearchAPI
api = SearchAPI()

# Perform a search
results = api.search("data")

# Process the results
for result in results:
    print(f"Title: {result['title']}")
    print(f"Snippet: {result['snippet']}")
    print(f"URL: {result['url']}")
    print()
```

### Exceptions

The `WebSearchApi` library defines two custom exceptions to handle errors:

- **APIError**: Raised when the API returns an error response. This could be due to network issues, invalid endpoints, or server errors.

  ```python
  from WebSearchApi import APIError

  try:
      results = api.search("data")
  except APIError as e:
      print(f"An error occurred with the API: {e}")
  ```

- **InvalidQueryError**: Raised when an invalid query is provided. This could be an empty string or a non-string query.

  ```python
  from WebSearchApi import InvalidQueryError

  try:
      results = api.search("")
  except InvalidQueryError as e:
      print(f"Invalid query: {e}")
  ```

### Project Structure

Here's an overview of the project structure:

```
WebSearchApi/
    __init__.py          # Package initialization
    search.py            # Main class for interacting with the API
    utils.py             # Utility functions
    exceptions.py        # Custom exceptions
    README.md            # Project documentation
    setup.py             # Setup script for packaging
```
