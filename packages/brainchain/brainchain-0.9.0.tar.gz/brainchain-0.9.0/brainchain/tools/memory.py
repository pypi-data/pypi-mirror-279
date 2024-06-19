import requests
from typing import Dict, List, Optional

def insert_memory(content: str, tags: Optional[List[str]] = None, metadata: Optional[Dict] = None) -> Dict:
    """Insert a memory."""
    base_url = "https://brainchain--memories.modal.run/insert_memory"
    data = {
        "content": content,
        "tags": tags if tags else [],
        "metadata": metadata if metadata else {}
    }
    response = requests.post(base_url, json=data)
    return response.json()

def delete_memories(query: str) -> Dict:
    """Delete memories based on a query."""
    base_url = "https://brainchain--memories.modal.run/delete_memories"
    data = {"query": query}
    response = requests.delete(base_url, json=data)
    return response.json()

def lookup_similar_memories(query: str) -> Dict:
    """Lookup similar memories based on a query."""
    base_url = "https://brainchain--memories.modal.run/lookup_similar_memories"
    params = {"query": query}
    response = requests.post(base_url, json=params)
    return response.json()
