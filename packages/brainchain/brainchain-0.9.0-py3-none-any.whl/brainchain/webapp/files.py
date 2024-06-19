from .base import BaseSessionHandler
from typing import Any


class Files(BaseSessionHandler):
    def upload_file(self, file_path):
        url = f"{self.base_url}/v1/files/upload/file"
        files = {"file": open(file_path, "rb")}
        response = self.session.post(url, files=files)
        return response.json()

    def upload_url(self, url):
        url = f"{self.base_url}/v1/files/upload/url"
        data = {"url": url}
        response = self.session.post(url, json=data)
        return response.json()

    def get_all_files(self):
        url = f"{self.base_url}/v1/files/list"
        response = self.session.get(url)
        return response.json()

    # def get_file(self, field: str, file_value: Any):  # TODO make vars part of the url
    # 	url = f"{self.base_url}/v1/files/"
    # 	data = {"file_field": file_value, "file_value": field}
    # 	response = self.session.get(url)
    # 	return response.json()

    def fuzzy_search(self, query):
        url = f"{self.base_url}/v1/files/search/title"
        data = {"query": query}
        response = self.session.post(url, json=data)
        return response.json()
