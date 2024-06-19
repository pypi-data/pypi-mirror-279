from .base import BaseSessionHandler


class Health(BaseSessionHandler):
    def get(self):
        url = f"{self.base_url}/v1/monitoring/health"
        response = self.session.get(url)
        return response.json()
