from .base import BaseSessionHandler


class Tasks(BaseSessionHandler):
    def get_all(self):
        url = f"{self.base_url}/v1/tasks/"
        response = self.session.get(url)
        return response.json()

    def create(self, title: str, description: str):
        url = f"{self.base_url}/v1/tasks/"
        payload = {"title": title, "description": description}
        response = self.session.post(url, json=payload)
        return response.json()

    def get_by_uuid(self, task_uuid: str):
        url = f"{self.base_url}/v1/tasks/{task_uuid}"
        response = self.session.get(url)
        return response.json()
