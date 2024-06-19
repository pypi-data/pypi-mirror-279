import json, requests

from dataclasses import dataclass, field, asdict
from typing import List, Any, Optional, Dict
import requests
import json

# Define request/response data classes with proper type hints
@dataclass
class IngestRequest:
    url: str
    document_node_name: str
    backend: str = "opensearch"

    def __post_init__(self):
        valid_backends = {"neo4j", "opensearch", "both"}
        if self.backend not in valid_backends:
            raise ValueError(f"Invalid backend type. Expected one of {valid_backends}")

@dataclass
class SearchIndexRequest:
    url: str = ""
    short_url: str = ""
    index_name: str = ""
    chunk_ids: List[Any] = field(default_factory=list)
    keywords: List[Any] = field(default_factory=list)
    search_field: str = "full_text"
    results: int = 30
    include_neighbor_pages: bool = True

@dataclass
class StructuredDataExtractionRequest:
    url: str = ""
    short_url: Optional[str] = ""
    index_name: Optional[str] = ""
    keywords: List[Any] = field(default_factory=list)
    query: str = ""
    search_field: str = "full_text"
    answers_only: bool = True
    results: int = 1
    dynamic_schema: Dict[str, Any] = field(default_factory=dict)


def _handle_response(response: requests.Response):
        # New internal method to handle responses and errors
        if response.status_code == 422:
            error = response.json()
            raise ValueError(f"Validation Error: {error}")
        response.raise_for_status()
        return response.json()

def fts_url_for_short_url(short_url: str):
    # New method to get full URL from short URL
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    response = session.get(f"{base_url}/url_for_short_url", params={"short_url": short_url})
    return _handle_response(response)

def fts_delete_all_documents():
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    response = session.get(f"{base_url}/delete_all")
    return response.json()

def fts_indices(urlkeys: bool = True):
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    response = session.get(f"{base_url}/indices")
    return response.json()

def fts_ingest_document(url: str, backend: str = "both", document_node_name: str = ""):
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    
    document_node_name = url if document_node_name == "" else document_node_name
    ingest_request = IngestRequest(url=url, document_node_name=document_node_name, backend=backend)
    payload = json.dumps(asdict(ingest_request))
    headers = {'Content-Type': 'application/json'}
    response = session.post(f"{base_url}/ingest_document/", headers=headers, data=payload)
    return response.json()

def fts_search_index(url: str, short_url: str, index_name: str, chunk_ids=None, keywords=None, search_field="full_text", results=2, include_neighbor_pages=False):
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    
    if chunk_ids is None:
        chunk_ids = []
    if keywords is None:
        keywords = []
    search_index_request = SearchIndexRequest(
        url=url,
        short_url=short_url,
        index_name=index_name,
        chunk_ids=chunk_ids,
        keywords=keywords,
        search_field=search_field,
        results=results,
        include_neighbor_pages=include_neighbor_pages
    )
    payload = json.dumps(asdict(search_index_request))
    headers = {'Content-Type': 'application/json'}
    response = session.post(f"{base_url}/search_index/", headers=headers, data=payload)
    return response.json()

def fts_health_check():
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    
    response = session.get(f"{base_url}/health")
    return response.json()

def fts_document_qa(url="", short_url="", index_name="", keywords=None, query="", search_field="full_text", answers_only=True, results=2, dynamic_schema=None):
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    
    if keywords is None:
        keywords = []
    if dynamic_schema is None:
        dynamic_schema = {}
    structured_data_extraction_request = StructuredDataExtractionRequest(
        url=url,
        short_url=short_url,
        index_name=index_name,
        keywords=keywords,
        query=query,
        search_field=search_field,
        answers_only=answers_only,
        results=results,
        dynamic_schema=dynamic_schema
    )
    payload = json.dumps(asdict(structured_data_extraction_request))
    headers = {'Content-Type': 'application/json'}
    response = session.post(f"{base_url}/document_qa/", headers=headers, data=payload)
    print(type(response), "response: ", response)
    return json.loads(response.content)

def fts_extract(url="", short_url="", index_name="", keywords=None, query="", search_field="full_text", answers_only=True, results=1, dynamic_schema=None):
    base_url = "https://brainchain--fts.modal.run"
    session = requests.Session()
    
    if keywords is None:
        keywords = []

    if dynamic_schema is None:
        dynamic_schema = {}
    
    structured_data_extraction_request = StructuredDataExtractionRequest(
        url=url,
        short_url=short_url,
        index_name=index_name,
        keywords=keywords,
        query=query,
        search_field=search_field,
        answers_only=answers_only,
        results=results,
        dynamic_schema=dynamic_schema
    )

    payload = json.dumps(asdict(structured_data_extraction_request))
    headers = {'Content-Type': 'application/json'}
    response = session.post(f"{base_url}/extract/", headers=headers, data=payload)
    return json.loads(response.content)
