import requests
from typing import Optional, Dict, Any

class SearchServiceV2Client:
    def __init__(self):
        self.base_url = "https://brainchain--search-service-v2.modal.run"

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, params=params, json=json)
        response.raise_for_status()
        return response.json()

    def unroll_search_results(self, query: str) -> Dict:
        return self._make_request("GET", "/results", params={"query": query})

    def shorten_link(self, link: str) -> Dict:
        return self._make_request("POST", "/shrink", params={"link": link})

    def scanner(self, query: str, additional_pages: Optional[int] = 5, shorten: Optional[bool] = False) -> Dict:
        params = {"query": query, "additional_pages": additional_pages, "shorten": shorten}
        return self._make_request("GET", "/scanner", params=params)

    def basic_search(self, query: str, shorten: Optional[bool] = False) -> Dict:
        params = {"query": query, "shorten": shorten}
        return self._make_request("GET", "/basic-search", params=params)

    def search_simple(self, q: str) -> Dict:
        return self._make_request("GET", "/search", params={"q": q})

    def process_webpage(self, url: str) -> Dict:
        return self._make_request("GET", "/process-webpage", params={"url": url})

    def crawl_website(self, url: str, visited: Optional[str] = None, skip_external_links: Optional[bool] = True, single_page_only: Optional[bool] = False, cached: Optional[bool] = False, model: Optional[str] = "gpt-3.5-turbo-16k") -> Dict:
        params = {"url": url, "visited": visited, "skip_external_links": skip_external_links, "single_page_only": single_page_only, "cached": cached, "model": model}
        return self._make_request("GET", "/crawl-website", params=params)
