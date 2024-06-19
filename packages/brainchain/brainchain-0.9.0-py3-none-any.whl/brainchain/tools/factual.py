import requests, os, json

import json, os, requests
from urllib.parse import quote

def fact_check(statement, env="prod"):
    if env == "prod":
        base_url = "https://brainchain--fact-check-service.modal.run"
    elif env == "dev":
        base_url = "https://brainchain--fact-check-service-dev.modal.run"
    else:
        raise ValueError("Invalid env")
    
    url = f"{base_url}/fact-check"
    
    response = requests.post(url, headers={"Accept": "application/json"}, params={"statement": statement})
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()