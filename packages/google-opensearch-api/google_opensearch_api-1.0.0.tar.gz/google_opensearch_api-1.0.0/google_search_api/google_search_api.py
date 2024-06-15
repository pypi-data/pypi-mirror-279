import requests
from bs4 import BeautifulSoup
import json
import logging
import time

class GoogleSearchAPI:
    def __init__(self):
        self.search_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def fetch_html(self, url, params):
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def google_search(self, query, num_results=10):
        start_time = time.time()
        results = []
        seen_urls = set()
        total_results = 0
        page_size = 10  # Number of results per page
        result_id = 1  # Starting ID for results

        while total_results < num_results:
            params = {"q": query, "num": page_size, "start": total_results}

            html = self.fetch_html(self.search_url, params)
            if not html:
                break

            soup = BeautifulSoup(html, 'html.parser')

            # Find all result containers
            search_results = soup.find_all('div', class_='tF2Cxc')
            additional_results = soup.find_all('div', class_='g')

            all_results = search_results + additional_results

            for g in all_results:
                title_element = g.find('h3')
                link_element = g.find('a')

                # Skip results without a link or title
                if not link_element or not title_element:
                    continue

                link = link_element['href']

                # Skip duplicate URLs
                if link in seen_urls:
                    continue

                seen_urls.add(link)

                # Improved snippet extraction
                snippet = ""
                snippet_element = g.find('div', class_='VwiC3b')
                if not snippet_element:
                    snippet_element = g.find('span', class_='aCOpRe')
                if snippet_element:
                    snippet = snippet_element.get_text()

                title = title_element.text if title_element else "No title available"

                results.append({
                    'id': result_id,
                    'title': title,
                    'link': link,
                    'snippet': snippet if snippet else "No snippet available",
                    'displayed_link': link_element.text if link_element else "No displayed link available"
                })

                result_id += 1
                total_results += 1
                if total_results >= num_results:
                    break

            if len(all_results) == 0:
                break  # No more results to fetch

        # Calculate metadata
        end_time = time.time()
        runtime = end_time - start_time

        metadata = {
            "num_requested": num_results,
            "total_items_fetched": total_results,
            "runtime_seconds": runtime
        }

        return json.dumps({'metadata': metadata, 'results': results}, indent=4)

