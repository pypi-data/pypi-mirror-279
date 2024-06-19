import requests
from typing import Union, List

def encode_text(text: Union[str, List[str]], backend: str = "openai", model: str = "gpt-3.5-turbo-16k", tokenizer: str = "cl100k_base"):
    base_url = "https://brainchain--token-service.modal.run"
    url = f"{base_url}/encode"

    headers = {"Content-Type": "application/json"}
    reqs, responses = [], []

    if isinstance(text, list):
        for text in text:
            requests.append({"url": url, "headers": headers, "json": {"text": text, "backend": backend, "model": model, "tokenizer": tokenizer}})
        
        for data in reqs:
            response = requests.post(data["url"], headers=data["headers"], json=data["json"]).json()
            responses.append(response)
        return responses
    else:
        response = requests.post(url, headers=headers, json={"text": text, "backend": backend, "model": model, "tokenizer": tokenizer}).json()
        return response
    

def decode_tokens(self, tokens: list[int], backend: str = "openai", tokenizer: str = "cl100k_base", model_name: str = "gpt-3.5-turbo-16k"):
    base_url = "https://brainchain--token-service.modal.run"
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
