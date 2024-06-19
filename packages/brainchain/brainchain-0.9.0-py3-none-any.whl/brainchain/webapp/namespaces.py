from uuid import UUID
from .base import BaseSessionHandler


class Namespaces(BaseSessionHandler):
    ##------------------- CREATE -------------------
    def create(self, namespace_name: str, description: str = ""):
        url = f"{self.base_url}/v1/namespaces/create"
        data = {"name": namespace_name, "description": description}
        response = self.session.post(url, json=data)
        return response.json()

    ##------------------- READ -------------------
    def get_all(self):
        url = f"{self.base_url}/v1/namespaces/list"
        response = self.session.get(url)
        return response.json()

    def get_by_name(self, namespace_name: str):
        url = f"{self.base_url}/v1/namespaces/name/{namespace_name}"
        data = {"namespace_name": namespace_name}
        response = self.session.get(url, json=data)
        return response.json()

    def get_by_uuid(self, namespace_uuid: UUID):
        url = f"{self.base_url}/v1/namespaces/uuid/{namespace_uuid}"
        data = {"namespace_uuid": namespace_uuid}
        response = self.session.get(url, json=data)
        return response.json()

    ##------------------- UPDATE -------------------

    def modify_name(self, namespace_name, new_name: str):
        url = f"{self.base_url}/v1/namespaces/update/name"
        params = {"namespace_name": namespace_name, "new_name": new_name}
        response = self.session.patch(url, params=params)
        return response.json()

    def modify_description(self, namespace_name, new_description: str):
        url = f"{self.base_url}/v1/namespaces/update/description"
        params = {"namespace_name": namespace_name, "new_description": new_description}
        response = self.session.patch(url, params=params)
        return response.json()

    ##------------------- DELETE -------------------
    def delete(self, namespace_name: str):
        url = f"{self.base_url}/v1/namespaces/delete/{namespace_name}"
        response = self.session.delete(url)
        return response.json()

    def soft_delete(self, namespace_name: str):
        url = f"{self.base_url}/v1/namespaces/soft_delete/{namespace_name}"
        response = self.session.delete(url)
        return response.json()
