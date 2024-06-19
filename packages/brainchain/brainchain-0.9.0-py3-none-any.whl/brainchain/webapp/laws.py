from .base import BaseSessionHandler


class Laws(BaseSessionHandler):
    def get_all(self):
        url = f"{self.base_url}/v1/laws"
        response = self.session.get(url)
        return response.json()

    def create(self, id: int, name: str, description: str):
        url = f"{self.base_url}/v1/laws"
        data = {"id": id, "name": name, "description": description}
        response = self.session.post(url, json=data)
        return response.json()

    def get_by_id(self, law_id: int):
        url = f"{self.base_url}/v1/laws/{law_id}"
        response = self.session.get(url)
        return response.json()
