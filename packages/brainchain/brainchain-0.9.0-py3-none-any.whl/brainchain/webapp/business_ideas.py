from .base import BaseSessionHandler


class BusinessIdeas(BaseSessionHandler):
    def get_all(self):
        url = f"{self.base_url}/v1/business_ideas"
        response = self.session.get(url)
        return response.json()

    def create(
        self,
        id: int,
        name: str,
        description: str,
        business_idea_type_id: int,
        source: str,
        program_id: int,
    ):
        url = f"{self.base_url}/v1/business_ideas"
        data = {
            "id": id,
            "name": name,
            "description": description,
            "business_idea_type_id": business_idea_type_id,
            "source": source,
            "program_id": program_id,
        }
        response = self.session.post(url, json=data)
        return response.json()

    def get_by_id(self, business_idea_id: int):
        url = f"{self.base_url}/v1/business_ideas/{business_idea_id}"
        response = self.session.get(url)
        return response.json()
