from .base import BaseSessionHandler


class Messages(BaseSessionHandler):
    ##------------------- CREATE -------------------

    def create(self, conversation_id, role, content):
        url = f"{self.base_url}/v1/messages/create"
        print(
            f"Creating message in conversation {conversation_id} with role {role} and content {content}"
        )
        print(f"User ID: {self.user_id}")
        print(f"URL: {url}")

        data = {
            "conversation_id": conversation_id,
            "user_id": self.user_id,
            "role": role,
            "content": content,
        }
        response = self.session.post(url, json=data)
        resp = response.json()

        print(resp)

        return response.json()

    ##------------------- READ -------------------

    def get_all(self):
        url = f"{self.base_url}/v1/messages/list"
        response = self.session.get(url)
        return response.json()

    def get_by_id(self, message_id):
        url = f"{self.base_url}/v1/messages/{message_id}"
        response = self.session.get(url)
        return response.json()
