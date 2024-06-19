from uuid import UUID
from .base import BaseSessionHandler

embedding_model_name = EMN = "text-embedding-3-large"


class Embeddings(BaseSessionHandler):
    ##------------------- CREATE -------------------

    def text_to_vector(self, text: str, embedding_model_name: str = EMN):
        url = f"{self.base_url}/v1/embeddings/create_vector"
        data = {"text": text, "embedding_model_name": embedding_model_name}
        response = self.session.post(url, json=data)
        return response.json()

    def add(self, text: str, namespace: str):
        url = f"{self.base_url}/v1/embeddings/add"
        data = {"text": text, "namespace": namespace, "embedding_model_name": embedding_model_name}
        response = self.session.post(url, json=data)
        return response.json()

    ##------------------- READ -------------------

    def get_unique_embedding_dimensions(self):
        url = f"{self.base_url}/v1/embeddings/unique_dimensions"
        response = self.session.get(url)
        return response.json()

    def search_all(self, query: str, top_k: int = 5):
        url = f"{self.base_url}/v1/embeddings/search"
        params = {"query": query, "top_k": top_k, "embedding_model_name": embedding_model_name}
        response = self.session.get(url, params=params)
        return response.json()

    def search_conversation(
        self, conversation_uuid: UUID, query: str, top_k: int = 5, embedding_model_name: str = EMN
    ):
        url = f"{self.base_url}/v1/embeddings/search/conversation"
        params = {
            "conversation_uuid": str(conversation_uuid),
            "query": query,
            "top_k": top_k,
            "embedding_model_name": embedding_model_name,
        }
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:  # includes JSONDecodeError
                return {"error": "No JSON content in response"}
        else:
            return {
                "error": "Request failed",
                "status_code": response.status_code,
                "details": response.text,
            }

    def search_namespace(self, namespace_name: str, query: str, top_k: int = 5):
        url = f"{self.base_url}/v1/embeddings/search/namespace"
        params = {
            "namespace_name": namespace_name,
            "query": query,
            "top_k": top_k,
            "embedding_model_name": embedding_model_name,
        }
        response = self.session.get(url, params=params)
        return response.json()

    ##------------------- UPDATE -------------------

    ##------------------- DELETE -------------------
