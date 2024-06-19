from .base import BaseSessionHandler


class Tools(BaseSessionHandler):
    def get_all_tools(self):
        url = f"{self.base_url}/v1/tools/"
        response = self.session.get(url)
        return response.json()

    def create_tool(
        self,
        name: str,
        description: str,
        func: str,
        tool_schema: dict,
        service_url: str,
        service_name: str,
        openapi_schema: dict,
    ):
        url = f"{self.base_url}/v1/tools/"
        payload = {
            "name": name,
            "description": description,
            "func": func,
            "tool_schema": tool_schema,
            "service_url": service_url,
            "service_name": service_name,
            "openapi_schema": openapi_schema,
        }
        response = self.session.post(url, json=payload)
        return response.json()
