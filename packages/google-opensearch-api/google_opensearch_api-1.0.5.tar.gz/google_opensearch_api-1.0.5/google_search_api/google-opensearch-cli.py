# google-opensearch-cli.py
import argparse
from google_search_api import GoogleSearchAPI

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="CLI utility for Google queries.")
    parser.add_argument('query', type=str, help='Search query string')
    parser.add_argument('--num_results', type=int, default=10, help='Number of results to fetch')
    
    # Parse arguments
    args = parser.parse_args()

    # Create an instance of GoogleSearchAPI
    api = GoogleSearchAPI()

    # Perform search
    result = api.google_search(args.query, args.num_results)
    print(result)

if __name__ == '__main__':
    main()
