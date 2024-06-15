Certainly! Here is the documentation tailored for the `WebSearchApi` library:

## WebSearchApi Library Documentation

### Overview
The `WebSearchApi` library provides a simple interface to perform web searches using the `SearchAPI` class.

### Installation
To install the `WebSearchApi` library, you can use pip. Assuming the library is available on PyPI, you can install it using the following command:

```sh
pip install WebSearchApi
```

If the library is not on PyPI, you can install it directly from the source by cloning the repository and installing it:

```sh
git clone https://github.com/ConsiousAI/WebSearchApi.git
cd WebSearchApi
pip install .
```

### Usage

#### Importing the Library
First, import the necessary classes from the library:

```python
from WebSearchApi.search import SearchAPI
```

#### Initializing the SearchAPI
Create an instance of the `SearchAPI` class:

```python
search_api = SearchAPI()
```

#### Performing a Search
Use the `search` method to perform a web search. Handle possible exceptions such as `InvalidQueryError` and `APIError`.

```python
try:
    result = search_api.search("OpenAI")
    print(result)
except:
    pass

```

### API Reference

#### `SearchAPI` Class
The `SearchAPI` class provides the interface to perform web searches.

##### Methods

- `search(query: str) -> dict`
  - **Description**: Performs a search query using the web search API.
  - **Parameters**: 
    - `query` (str): The search query string.
  - **Returns**: 
    - `dict`: The JSON response from the API.
  - **Raises**: 
    - `InvalidQueryError`: If the query is invalid.
    - `APIError`: If the API returns an error.


### Example
Here is a complete example demonstrating how to use the `WebSearchApi` library:

```python
from websearchapi.search import SearchAPI

def main():
    search_api = SearchAPI()
    try:
        result = search_api.search("OpenAI")
        print(result)
    except InvalidQueryError as e:
        print(f"Invalid query: {e}")
    except APIError as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    main()
```

### Contributing
If you want to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.
