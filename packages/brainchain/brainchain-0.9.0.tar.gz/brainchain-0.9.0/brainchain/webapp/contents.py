from .base import BaseSessionHandler


class Contents(BaseSessionHandler):
    ##------------------- CREATE -------------------

    def create(self, text: str):
        url = f"{self.base_url}/v1/contents/create"
        data = {"text": text}
        response = self.session.post(url, json=data)
        return response.json()

    ##------------------- READ -------------------

    def get_all(self):
        url = f"{self.base_url}/v1/contents/list"
        response = self.session.get(url)
        return response.json()

    def get_by_id(self, content_id: int):
        url = f"{self.base_url}/v1/contents/{content_id}"
        response = self.session.get(url)
        return response.json()

    ##------------------- UPDATE -------------------

    ##------------------- DELETE -------------------

    def delete(self, content_id: int):
        url = f"{self.base_url}/v1/contents/{content_id}delete"
        data = {"content_id": content_id}
        response = self.session.delete(url, json=data)
        return response.json()

    def soft_delete(self, content_id: int):
        url = f"{self.base_url}/v1/contents/{content_id}/soft_delete"
        data = {"content_id": content_id}
        response = self.session.delete(url, json=data)
        return response.json()
