from .base import BaseSessionHandler


class Programs(BaseSessionHandler):
    def get_programs(self):
        url = f"{self.base_url}/v1/programs/"
        response = self.session.get(url)
        return response.json()

    def create_program(
        self,
        name: str,
        description: str,
        eligibility: str,
        benefits: str,
        incentives: str,
        business_areas: str,
        law_id: int,
    ):
        url = f"{self.base_url}/v1/programs/"
        payload = {
            "name": name,
            "description": description,
            "eligibility": eligibility,
            "benefits": benefits,
            "incentives": incentives,
            "business_areas": business_areas,
            "law_id": law_id,
        }
        response = self.session.post(url, json=payload)
        return response.json()

    def get_program_by_id(self, program_id):
        url = f"{self.base_url}/v1/programs/{program_id}"
        response = self.session.get(url)
        return response.json()
