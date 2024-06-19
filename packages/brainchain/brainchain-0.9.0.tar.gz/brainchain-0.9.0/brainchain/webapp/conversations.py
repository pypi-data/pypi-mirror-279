from .base import BaseSessionHandler


class Conversations(BaseSessionHandler):
    def get_all_conversations(self):
        url = f"{self.base_url}/v1/conversations/list"
        response = self.session.get(url)
        return response.json()

    def get_conversation_by_id(self, conversation_id):
        url = f"{self.base_url}/v1/conversations/{conversation_id}"
        response = self.session.get(url)
        return response.json()

    def create_conversation(self, messages=[]):
        url = f"{self.base_url}/v1/conversations/"
        data = {"user_id": self.user_id, "messages": messages}
        response = self.session.post(url, json=data)
        return response.json()

    def get_conversation_messages(self, conversation_id):
        url = f"{self.base_url}/v1/conversations/{conversation_id}/messages"
        response = self.session.get(url)
        return response.json()
