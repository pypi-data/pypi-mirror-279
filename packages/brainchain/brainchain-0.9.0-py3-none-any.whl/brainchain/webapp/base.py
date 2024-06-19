class BaseSessionHandler:
    def __init__(self, session, base_url, user_id):
        self.session = session
        self.base_url = base_url
        self.user_id = user_id
