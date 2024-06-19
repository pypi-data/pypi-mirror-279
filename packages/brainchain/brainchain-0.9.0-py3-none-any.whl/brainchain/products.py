from pydantic import BaseModel
import requests
import re
from typing import List, Dict
from .tools.web import WebDataClient, ProductFinderParameters, ProductQueryPayload, QueryOptions, DealParameters, BestSellersQueryParams
from datetime import datetime as dt
from datetime import timedelta as td
from urllib.parse import quote  
import json

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

import time
class ProductsAPI():
    def __init__(self, base_url: str = "https://api.brainchain.cloud"):
        self.base_url = base_url
        self.wd = WebDataClient()
        self.session = requests.Session()
    
    @staticmethod
    def _convert_camel_to_snake(name):
        """
        Convert a camelCase name into snake_case.
        Ex: 'camelCase' -> 'camel_case'
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _normalize_query(self, query: str) -> str:
        """
        Normalize the search query.
        
        Args:
            query (str): The search query to normalize.
            
        Returns:
            str: The normalized search query.
        """
        # Add normalization logic here
        return query
    

    def search_keepa_and_save(self, asins: List[str] = [], max_products: int = 5, title: str = "", offers: int = 20, trackingSince_lte: dt = dt.now(), trackingSince_gte: dt = dt.now() - td(days=30), excludeCategories: List[int] = []) -> List[Dict]:
        """
        Searches products on Keepa via WebDataClient and saves them to the database.
        
        Args:
            search_query (str): The search query for finding products.
        
        Returns:
            List[Dict]: A list of dictionaries containing information about the saved products and instances.
        """
        # 1 create product_id from title (search query)
        # 2 search keepa for products with the title
        # 3 create product_instance_id from asin, product_id and title
        # you're going to get a bunch of ASINs from the search results
        # each of those asins, from find_and_query, you'll get back a large dict of asin -> {info: ... , history: price_history... }'
        # 4 create product_instance_price_id from product_instance_id, price, date from the prices for the individual product instances using the existing methods
        # 5 save the product, product_instance, and product_instance_price to the database


        # 1. Create a product
        product_response = self.create_product(name=title)
        # print("Product Response: ", product_response)

        product_info = self.wd.find_and_query(asins=asins, title=title, trackingSince_gte=trackingSince_gte, trackingSince_lte=trackingSince_lte, offers=offers, max_products=max_products, history=False)[0:max_products]
        time.sleep(1)
        asin_product_map = {}

        for product in product_info:
            #print(product)
            history = self.wd.find_and_query(asins=[product["asin"]], title=title, trackingSince_gte=trackingSince_gte, trackingSince_lte=trackingSince_lte, offers=100, history=True)
            #print(history)
            
            asin_product_map[product["asin"]] = {"info": product, "history": history}
            # print(json.dumps(asin_product_map, indent=2))

        for asin, details in asin_product_map.items():
            # 2. Create a product instance
            # KEEPA OUTPUT: 
            #print("product_response: ", product_response)

            instance_data = {
                "product_id": product_response["product_id"],
                "asin": asin,
                "title": title,
                "number_of_items": details["info"]["numberOfItems"],
                "package_height": details["info"]["packageHeight"],
                "package_length": details["info"]["packageLength"],
                "package_width": details["info"]["packageWidth"],
                "package_weight": details["info"]["packageWeight"],
                "description": details["info"]["description"],
                "brand": details["info"]["brand"],
                "features": details["info"]["features"],
                "manufacturer": details["info"]["manufacturer"],
                "categories": list(map(lambda x: str(x), details["info"]["categories"])),
                "category_tree": details["info"]["categoryTree"],
                'listed_since': keepa_int_to_datetime(details["info"]['listedSince']).strftime("%Y-%m-%d %H:%M:%S"),
                'last_update': keepa_int_to_datetime(details["info"]['lastUpdate']).strftime("%Y-%m-%d %H:%M:%S"),
                'last_price_change': keepa_int_to_datetime(details["info"]["lastPriceChange"]).strftime("%Y-%m-%d %H:%M:%S"),
                "ean_list": details["info"]["eanList"],
                "upc_list": details["info"]["upcList"]
            }

            #print("Instance Data: ", instance_data)
            instance_response = self.create_product_instance(instance_data)
            print(instance_response)
            price_history = self.wd.query_product(ProductQueryPayload(items=[asin], options=QueryOptions(history=True)))
            #print(price_history)
            if price_history:
                #print("Price History: ", price_history)
                for price in price_history:
                    # 3. Create a product instance price
                    #print(price)
                    if len(price) == 2:
                        
                        price_data = {
                            "product_instance_uuid": instance_response["uuid"],
                            "price": price[1],
                            "date": price[0],
                        }
                        
                        price_response = self.create_product_instance_price(price_data)
                        print(price_response)
                    else:
                        print("Skipping price data because it's not the right length")
                        print(price)
                        
        return asin_product_map
    
    def get_product_instance_prices(self, product_instance_uuid):
        """
        Retrieve prices for a product instance.
        
        Args:
            product_instance_uuid (str): The unique identifier for the product instance.
            
        Returns:
            dict: The response data containing the product instance prices.
        """
        url = f"{self.base_url}/v1/products/product_instance/prices?product_instance_uuid={quote(product_instance_uuid)}"
        response = self.session.get(url)
        return response.json()



    def create_product(self, name: str):
        """
        Create a new product.
        
        Args:
            product_data (dict): The product information to create.
            
        Returns:
            dict: The response data containing information about the created product.
        """
        url = f"{self.base_url}/v1/products/create"
        response = self.session.post(url, json={"name": name})
        return response.json()

    def create_product_instance(self, instance_data: dict):
        """
        Create a new product instance.
        
        Args:
            instance_data (dict): The product instance information to create.
            
        Returns:
            dict: The response data containing information about the created product instance.
        """
        url = f"{self.base_url}/v1/products/instance/create"
        response = self.session.post(url, json=instance_data)
        return response.json()

    def create_product_instance_price(self, price_data):
        """
        Create a new product instance price.
        
        Args:
            price_data (dict): The product instance price information to create.
            
        Returns:
            dict: The response data containing information about the created product instance price.
        """
        url = f"{self.base_url}/v1/products/instance/price/create"
        response = self.session.post(url, json=price_data)
        return response.json()

    def get_product(self, search_data):
        """
        Retrieve product information.
        
        Args:
            search_data (dict): The search criteria for finding a product.
            
        Returns:
            dict: The response data containing the product information.
        """
        url = f"{self.base_url}/v1/products/product"
        response = self.session.post(url, json=search_data)
        return response.json()

    def get_product_instance(self, instance_id):
        """
        Retrieve a product instance.
        
        Args:
            instance_id (str): The unique identifier for the product instance.
            
        Returns:
            dict: The response data containing the product instance information.
        """
        url = f"{self.base_url}/v1/products/product_instance"
        # Assuming instance_id should be included in the request body. If it should be a query param, adjust accordingly.
        response = self.session.get(url, json={"instance_id": instance_id})
        return response.json()

    def get_product_instance_prices(self, product_instance_uuid):
        """
        Retrieve prices for a product instance.
        
        Args:
            product_instance_uuid (str): The unique identifier for the product instance.
            
        Returns:
            dict: The response data containing the product instance prices.
        """
        url = f"{self.base_url}/v1/products/product_instance/prices?product_instance_uuid={quote(product_instance_uuid)}"
        response = self.session.get(url)
        return response.json()

    def update_product_instance_price(self, instance_price_id, update_data):
        """
        Update a product instance price.
        
        Args:
            instance_price_id (str): The unique identifier for the product instance price to update.
            update_data (dict): The update data for the product instance price.
            
        Returns:
            dict: The response data after updating the product instance price.
        """
        url = f"{self.base_url}/v1/products/instance/price/update"
        # Assuming instance_price_id should be included in the request body. If it should be a query param, adjust accordingly.
        response = self.session.patch(url, json=update_data)
        return response.json()
