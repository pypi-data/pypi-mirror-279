import requests

def graph_health_check():
    base_url = "https://brainchain--graph-query.modal.run"
    response = requests.get(f"{base_url}/")
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return response.status_code

def graph_refresh_schema() -> dict:
    base_url = "https://brainchain--graph-query.modal.run"
    response = requests.post(f"{base_url}/refresh-schema")
    response.raise_for_status()
    return response.json()

def graph_get_schema() -> dict:
    base_url = "https://brainchain--graph-query.modal.run"
    response = requests.get(f"{base_url}/schema")
    response.raise_for_status()
    return response.json()

def graph_query(question, results=25, model="gpt-4-32k", temperature=0.0, max_tokens=16384):
    base_url = "https://brainchain--graph-query.modal.run"
    payload = {
        "question": question,
        "results": results,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{base_url}/graph-query", json=payload, headers=headers)
    return response.json()

def execute_cypher_query(query: str) -> dict:
    base_url = "https://brainchain--graph-query.modal.run"
    response = requests.post(f"{base_url}/execute-cypher-query", params={"query": query})
    response.raise_for_status()
    return response.json()