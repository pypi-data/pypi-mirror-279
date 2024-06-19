from .base import BaseSessionHandler


class Users(BaseSessionHandler):
    def get_all_users(self):
        url = f"{self.base_url}/v1/users/"
        response = self.session.get(url)
        return response.json()

    def get_current_user(self):
        url = f"{self.base_url}/v1/users/me"
        response = self.session.get(url)
        return response.json()

    def register_user(self, email, username, password):
        url = f"{self.base_url}/v1/users/"
        data = {"email": email, "username": username, "password": password}
        response = self.session.post(url, json=data)
        return response.json()


# def login_user(self, email, password):
#  pass
