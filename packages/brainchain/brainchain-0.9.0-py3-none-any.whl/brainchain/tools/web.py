from .diffbot import diffbot_analyze
from .fts import fts_ingest_document

import os, requests, json
def web_search(search_query: str, fast: bool = True, get_content: bool = True, links_to_read: int = 2, ingest_into_fts: bool = True, exclusions: list = ['rich_snippet', 'snippet', 'cached_links', 'hourly_forecast', 'precipitation_forecast', 'wind_forecast', 'forecast'], additional_serp_pages: int = 2):
    base_url = 'https://brainchain--search-service-v2.modal.run'
    resp = requests.get(base_url + '/search' + f'?q={search_query}')
    jsonpayload = json.loads(resp.content)
    print(jsonpayload)
    if fast:
        return jsonpayload
    
    if 'content' not in jsonpayload:
        jsonpayload["content"] = {}
        jsonpayload["content"]["by_link"] = {}
    
    
    if additional_serp_pages > 0:
        extra_links = web_scanner(search_query, additional_serp_pages=additional_serp_pages, shorten_links = False)
        jsonpayload["extra_links"] = extra_links
        
    import numpy as np
    unique_links = np.unique(jsonpayload["links"] + jsonpayload["extra_links"])

    if ingest_into_fts:
        ingested_links = [fts_ingest_document(url=link) for link in unique_links[0:links_to_read]]
        jsonpayload["ingested_links"] = ingested_links
    
    cached_links = jsonpayload['cached_links'] if 'cached_links' in jsonpayload else None
    links = jsonpayload['links'] if 'links' in jsonpayload else None

    if 'answer_box' in jsonpayload and jsonpayload['answer_box']:
        for item in jsonpayload['answer_box'].keys():
            if item in exclusions:
                jsonpayload['answer_box'][item] = None
            else:
                print(jsonpayload['answer_box'][item])
        
    if get_content:
        for link in jsonpayload["links"]:
            content = diffbot_analyze(link)
            print(content)
            jsonpayload["content"]["by_link"][link] = content
            
    return jsonpayload

def web_scanner(query: str, additional_serp_pages: int = 4, shorten_links: bool = False):
    url = 'https://brainchain--search-service-v2.modal.run'
    params = {
        "query": query,
        "additional_pages": additional_serp_pages,
        "shorten": shorten_links
    }
    response = requests.get(url + '/scanner', params=params)
    if response.status_code == 200:
        jsonpayload = response.json()

        # Deduplication logic starts here
        # Assuming the JSON payload structure is a list of dictionaries, and each dictionary represents a search result.
        # The deduplication criterion needs to be defined. Let's assume we want to dedupe based on a unique 'url' field in each dictionary.
        seen_urls = set()
        deduped_results = []
        for url in jsonpayload:
            # Adjust the following line according to the actual structure of your JSON payload.
            # Here, it is assumed that each item in the payload has a 'url' field.
            if url not in seen_urls:
                seen_urls.add(url)
                deduped_results.append(url)

        # Replace the original payload with the deduped results
        # Deduplication logic ends here

        return deduped_results
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}

def web_cache(url, get_content: bool = True):
    # figure out google web cache link
    google_cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}"
    if get_content:
        content = diffbot_analyze(google_cache_url)
        return {
            "url": url,
            "google_cache_url": google_cache_url,
            "content": content
        }
    else:
        return {
            "url": url,
            "google_cache_url": google_cache_url
        }

import requests

def web_content(url, ephemeral=True, use_google_web_cache=False, use_browser=True, raw_html=False,
                use_web_archive_api=False, use_jina_reader=False, use_assistants=False,
                tags=None, exclude_tags=None):
    """
    Scrape content from the given URL using various options for content rendering and filtering.
    
    Parameters:
        url (str): The URL to scrape.
        ephemeral (bool): If true, the data will not be stored persistently.
        use_google_web_cache (bool): Use Google's cache to fetch older versions of the site if available.
        use_browser (bool): Use a full browser environment for scraping, enabling JavaScript rendering.
        raw_html (bool): Return raw HTML without any processing.
        use_web_archive_api (bool): Use the Web Archive API to fetch archived versions of the site if available.
        use_jina_reader (bool): Use Jina AI's reader for enhanced processing of the content.
        use_assistants (bool): Use AI assistants for additional processing of the content.
        tags (list[str]): Specific tags to include in the scraped content. Defaults to all tags if not specified.
        exclude_tags (list[str]): Tags to exclude from the scraped content. Defaults to ["html", "script", "style"].

    Returns:
        dict: The JSON response from the API with the scraped data.
    """
    base_url = "https://carnivore.brainchain.cloud"

    # Default values for tags and exclude_tags
    if tags is None:
        tags = ["*"]
    if exclude_tags is None:
        exclude_tags = ["html", "script", "style"]

    # Organize the data to be sent in the POST request
    data = {
        "url": url,
        "ephemeral": ephemeral,
        "use_google_web_cache": use_google_web_cache,
        "use_browser": use_browser,
        "raw_html": raw_html,
        "use_web_archive_api": use_web_archive_api,
        "use_jina_reader": use_jina_reader,
        "use_assistants": use_assistants,
        "tags": tags,
        "exclude_tags": exclude_tags
    }

    # Make the POST request and return the response
    response = requests.post(f"{base_url}/carnivore", json=data)
    return response.json()


import requests
from typing import List, Optional
from pydantic import BaseModel, Field, validator

import requests
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime as dt
from datetime import timedelta as td

def keepa_int_to_datetime(keepa_timestamp: int) -> dt:
    """
    Convert a Keepa timestamp to a datetime object.
        ...:
    Keepa timestamps are in minutes since January 1st, 1970, with a fixed offset of 21564000 minutes.
    This function corrects for the Keepa-specific representation.
        ...:
    Args:
        keepa_timestamp (int): The Keepa timestamp to convert.
        ...:
    Returns:
        datetime: A datetime object representing the given Keepa timestamp.
    """
    # Correct the conversion process: reverse the Keepa-specific adjustments
    unix_timestamp_seconds = (keepa_timestamp + 21564000) * 60
    # Convert the Unix timestamp (in seconds) to a datetime object
    date_obj = dt.fromtimestamp(unix_timestamp_seconds)
    return date_obj


def keepa_datetime_to_int(date_obj: dt) -> int:
    """
    Convert a datetime object to a Keepa timestamp.
    
    Keepa timestamps are in minutes since January 1st, 1970, with a fixed offset of 21564000 minutes.
    This function corrects for the Keepa-specific representation.
        ...:
    Args:
        date_obj (datetime): The datetime object to convert.
        ...:
    Returns:
        int: A Keepa timestamp representing the given datetime object.
    """
    # Convert the datetime object to a Unix timestamp (in seconds)
    unix_timestamp_seconds = int(date_obj.timestamp())
    # Correct the conversion process: apply the Keepa-specific adjustments
    keepa_timestamp = (unix_timestamp_seconds // 60) - 21564000
    return keepa_timestamp


class WebDataClientException(Exception):
    pass


class QueryOptions(BaseModel):
    history: Optional[bool] = True
    offers: Optional[int] = 100


class ProductQueryPayload(BaseModel):
    items: List[str]
    options: Optional[QueryOptions] = QueryOptions()


class DealParameters(BaseModel):
    domainId: int
    includeCategories: List[int]
    excludeCategories: Optional[List[int]] = []
    page: Optional[int] = 0


class ProductFinderParameters(BaseModel):
    title: Optional[str] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    trackingSince_lte: Optional[str] = None
    trackingSince_gte: Optional[str] = None
    excludeCategories: Optional[List[int]] = []


class BestSellersQueryParams(BaseModel):
    category: str
    domain: Optional[str] = "US"
    wait: Optional[bool] = True


class WebDataClient:
    def __init__(self, service_url: str = "https://brainchain--web-data-service.modal.run"):
        self.service_url = service_url

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = self.service_url + endpoint
        response = requests.request(method, url, **kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            raise WebDataClientException(f"Error {response.status_code} for URL {url}: {response.text}")

    def product_finder(self, params: ProductFinderParameters) -> dict:
        return self._request("POST", "/api/v1/amazon/product/finder", params=params.dict(exclude_none=True))

    def query_product(self, json_data: ProductQueryPayload) -> dict:
        return self._request("POST", "/api/v1/amazon/product/query", json=json_data.dict())

    def find_and_query(
        self,
        title: Optional[str],
        asins: Optional[List[str]] = [],
        trackingSince_gte: Optional[dt] = dt.now() - td(days=30),
        trackingSince_lte: Optional[dt] = dt.now(),
        excludeCategories: Optional[List[int]] = [],
        offers: int = 20,
        max_products: int = 5,
        history: bool = True,
    ) -> dict:
        if title:
            params = ProductFinderParameters(
                title=title, trackingSince_gte=trackingSince_gte.strftime("%Y-%m-%d"), trackingSince_lte=trackingSince_lte.strftime("%Y-%m-%d"), excludeCategories=excludeCategories
            )
            asins = self.product_finder(params)
            print(asins)
            query = ProductQueryPayload(items=asins, options=QueryOptions(offers=offers, history=history))
            print(query)
            x = self.query_product(query)
            print(x)
            return x
        elif asins:
            query = ProductQueryPayload(items=asins, options=QueryOptions(offers=offers, history=history))
            print(query)
            x = self.query_product(query)
            print(x)
        else:
            if title and asins:
                raise ValueError("You must provide a title or a list of ASINs but not both at the same time!")

    def best_sellers(self, params: BestSellersQueryParams) -> dict:
        return self._request("GET", "/api/v1/amazon/best-sellers", params=params.dict())

    def find_deals(self, json_data: DealParameters) -> dict:
        return self._request("POST", "/api/v1/amazon/deals", json=json_data.dict())

    def seller_query(self, seller_id: str, **kwargs) -> dict:
        kwargs["seller_id"] = seller_id
        return self._request("GET", "/api/v1/amazon/seller/query", params=kwargs)

    def category_search(self, searchterm: str, **kwargs) -> dict:
        kwargs["searchterm"] = searchterm
        return self._request("GET", "/api/v1/amazon/category/search", params=kwargs)

    def google_search_simple(self, q: str) -> dict:
        params = {"q": q}
        return self._request("GET", "/api/v1/google/search/simple", params=params)

    def google_scanner(self, q: str, additional_pages: Optional[int] = 3) -> dict:
        params = {"q": q, "additional_pages": additional_pages}
        return self._request("GET", "/api/v1/google/scanner", params=params)

    def twitter_search(self, q: str, **kwargs) -> dict:
        kwargs["q"] = q
        return self._request("GET", "/api/v1/twitter/search", params=kwargs)

    def reddit_search(self, q: str, **kwargs) -> dict:
        kwargs["q"] = q
        return self._request("GET", "/api/v1/reddit/search", params=kwargs)
