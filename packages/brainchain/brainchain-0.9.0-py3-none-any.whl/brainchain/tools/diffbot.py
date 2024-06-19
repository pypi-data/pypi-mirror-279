import json
import os
import requests
from pydantic import BaseModel
from typing import List

def diffbot_analyze(url: str, mode: str = None, fallback: str = None, fields: str = None, discussion: bool = None, timeout: int = 30000, proxy: str = None, proxyAuth: str = None, useProxy: str = None) -> dict:
    """
    Makes a request to the Diffbot Analyze API and returns the structured data.
    
    :param url: The URL of the web page to analyze.
    :param mode: Specific Extract API to use (optional).
    :param fallback: Fallback API if an appropriate API cannot be determined (optional).
    :param fields: Specify optional fields to be returned (optional).
    :param discussion: Set to False to disable automatic extraction of comments/reviews (optional).
    :param timeout: Timeout in milliseconds for the request (default 30000).
    :param proxy: Custom proxy IP address (optional).
    :param proxyAuth: Authentication parameters for the custom proxy (optional).
    :param useProxy: Use custom or no proxy (optional).
    :return: A dictionary with the structured data.
    """

    backslash = '''n
        \\
    '''
    url = url
    print(url)
    # Construct the API endpoint
    api_endpoint = "https://api.diffbot.com/v3/analyze"
    params = {
        "url": url.replace("\\", ""),
        "token": os.environ["DIFFBOT_API_KEY"],  # Replace with your actual API token
        "mode": mode,
        "fallback": fallback,
        "fields": fields,
        "discussion": "false" if discussion is False else None,
        "timeout": timeout,
        "proxy": proxy,
        "proxyAuth": proxyAuth,
        "useProxy": useProxy
    }

    import requests

    class TokenizerClient:
        def __init__(self, base_url = "https://brainchain--token-service.modal.run"):
            self.base_url = base_url

        def encode_text(self, text: List[str], backend: str = "openai", model: str = "gpt-3.5-turbo-16k", tokenizer: str = "cl100k_base"):
            url = f"{self.base_url}/encode"
            headers = {"Content-Type": "application/json"}
            data = {
                "texts": [text],
                "backend": backend,
                "model": model,
                "tokenizer": tokenizer
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                raise ValueError("Validation Error: " + response.text)
            else:
                raise ValueError("Error: " + response.text)

        def decode_tokens(self, tokens: list[int], backend: str = "openai", tokenizer: str = "cl100k_base", model_name: str = "gpt-3.5-turbo-16k"):
            url = f"{self.base_url}/decode"
            headers = {"Content-Type": "application/json"}
            data = {
                "backend": backend,
                "tokenizer": tokenizer,
                "model": model_name,
                "tokens": tokens
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 422:
                raise ValueError("Validation Error: " + response.text)
            else:
                raise ValueError("Error: " + response.text)

    tokenizer = TokenizerClient()    
    # Make the GET request
    response = requests.get(api_endpoint, params=params)

    # Check for successful response
    if response.status_code == 200:
        if tokenizer.encode_text(response.text)[0]["token_count"] > 63000:
            return "The response from Diffbot is too large to process. Tell the user to ask the chatbot to upload the file to the FTS Service."
        else:
            return json.loads(response.text)
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return {}
