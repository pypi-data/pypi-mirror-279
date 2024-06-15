# Google Open Search API Python Module

## Overview

The **Google Search API Python Module** is a Python library that allows you to fetch and parse Google search results programmatically. It provides an easy-to-use interface to perform Google searches and retrieve search result data such as titles, URLs, snippets, and displayed links.

## Installation

You can install the `google-opensearch-api` module using pip:

```bash
pip install google-opensearch-api
```

## Usage

### Basic Example

```python
from google_search_api.google_search_api import GoogleSearchAPI

# Initialize GoogleSearchAPI object
google_search_api = GoogleSearchAPI()

# Perform a Google search
query = "Cyber Security"
num_results = 10
search_results = google_search_api.google_search(query, num_results)

# Print search results in JSON format
print(search_results)
```

## Advanced Usage
### Parameters
- `query` (str): The search query to be performed.
- `num_results` (int, optional): Number of search results to retrieve (default is 10).

### CLI Usage

You can use the `google-opensearch` command line tool to perform Google searches:
```python
google-search "cyber security" --num_results 5
```
### Docker Container Usage

You can use the `google-opensearch-api` Docker container to perform Google searches:

```cmd
docker run -it --rm google-opensearch-api "cyber security" --num_results 5
```

### Output

The `google_search` method returns a JSON string containing search results and metadata:

```json
{
    "metadata": {
        "num_requested": 10,
        "total_items_fetched": 10,
        "runtime_seconds": 1.234
    },
    "results": [
        {
            "id": 1,
            "title": "Example Result Title",
            "link": "https://example.com",
            "snippet": "Example result snippet text.",
            "displayed_link": "example.com"
        },
        {
            "id": 2,
            "title": "Another Result Title",
            "link": "https://another-example.com",
            "snippet": "Another result snippet.",
            "displayed_link": "another-example.com"
        },
        ...
    ]
}
```

### Notes
- Duplicates: The module automatically removes duplicate URLs from the search results.
- Snippet: Snippet text may not be available for all results depending on Google's HTML structure.

## Contributing
Contributions to the google-search-api module are welcome! You can contribute by forking the repository, making changes, and submitting a pull request.

## License
The google-search-api module is licensed under the MIT license.

## Support
For any issues or questions related to the google-search-api module, please open an issue on GitHub.

## Acknowledgments
- The google-search-api module utilizes requests and beautifulsoup4 libraries for web scraping and parsing HTML.
- This module was inspired by the Google Search API.

Authors
- CuriousTinker - https://github.com/CuriousTinker

Changelog
- v1.0.0 (2024-06-15)
    - Initial release of the google-search-api module.

