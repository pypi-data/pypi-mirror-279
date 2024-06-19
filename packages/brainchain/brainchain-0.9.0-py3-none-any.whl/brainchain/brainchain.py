import os
import json
import requests
from getpass import getpass
from .tools.coding import python_agent, sql_database_agent, terminal
from .tools.web import web_search, web_content, web_cache, web_scanner
from .tools.factual import fact_check
from .tools.fts import (
    fts_ingest_document,
    fts_search_index,
    fts_document_qa,
    fts_extract,
    fts_indices,
)
from .tools.graph import execute_cypher_query, graph_query
from .tools.plan import generate_plan, improve_plan, execute_plan
from .tools.tokens import encode_text, decode_tokens
from .tools.memory import insert_memory, lookup_similar_memories, delete_memories
from .tools.diffbot import diffbot_analyze
from .tools.tools import tool_schemas
from .tools.web import WebDataClient
from .assistants import AssistantClient

from .webapp import (
    Agents,
    BusinessIdeas,
    Contents,
    Conversations,
    EmbeddingModels,
    Embeddings,
    Files,
    Health,
    LanguageModels,
    Laws,
    Messages,
    Namespaces,
    Programs,
    Tasks,
    Tools,
    Users,
)

from .products import keepa_datetime_to_int, keepa_int_to_datetime
from .products import ProductsAPI

from .assistants import AssistantClient as AssistantsAPI
class FunctionSchema:
    def __init__(self, name: str, description: str, parameters: dict, returns: dict):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.returns = returns


class Function:
    def __init__(self, name: str, function, schema: FunctionSchema):
        self.name = name
        self.function = function
        self.schema = schema


class Brainchain:
    def _init_component(self, component_cls):
        return component_cls(self.session, self.api_host, self.user_id)

    def __init__(
        self,
        env: str = "prod",
        # brainchain_api_key: str = os.environ["BRAINCHAIN_API_KEY"],
        salesintel_api_key: str = os.environ["SALESINTEL_API_KEY"],
        api_host: str = os.getenv("API_HOST", "https://api.brainchain.cloud"),
        assistants_api_host: str = os.getenv("ASSISTANTS_API_HOST", "https://assistants-api.brainchain.cloud"),
        api_key: str = os.environ.get("BRAINCHAIN_API_KEY_", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MTc1NDUxNTF9.Js0qwbk9RS3S0GsjUsmSQ9oreo3d__7Hk3PHr40clLk")
    ):
        access_token = api_key
        self.access_token = api_key

        if not api_key:
            if env=="dev":
                self.api_key = self.enforce_login()
            else:
                print("BRAINCHAIN_API_KEY_ is not set")
        else:
            self.api_key = api_key

        if env == "prod":
            self.api_host = api_host
            self.assistants_api_host = assistants_api_host
            print("Brainchain API URL: ", self.api_host)
            print("Assistants API URL: ", self.assistants_api_host)
            
            if not self.api_key:
                print("BRAINCHAIN_API_KEY_ is not set")
        
        elif env == "dev":
            self.api_host = "http://localhost:8000"
            self.assistants_api_host = "http://localhost:42069"
            print("Brainchain API URL: ", self.api_host)
            print("Assistants API URL: ", self.assistants_api_host)
            
            try:
                if not os.path.exists(os.path.expanduser("~/.config/brainchain")):
                    os.makedirs(os.path.expanduser("~/.config/brainchain"))

                if not os.path.exists(os.path.expanduser("~/.config/brainchain/.access_token")):
                    with open(os.path.expanduser("~/.config/brainchain/.access_token"), "w") as f:
                            payload = self.enforce_login()
                            access_token = payload.get("access_token")
                            f.write(access_token)
                            f.close()
                else:
                    with open(os.path.expanduser("~/.config/brainchain/.access_token"), "r") as f:
                        access_token = f.read()
                        self.access_token = access_token
            except:            
                self.api_key = self.access_token
                
        elif env == "test":
            self.api_host = self.api_host.replace("api", "api-test")
            print("Brainchain API URL: ", self.api_host)
            print("Assistants API URL: ", self.assistants_api_host)

        self.web_data_client = WebDataClient()
        self.session = requests.Session()
        self.access_token = None
        self.user_id = None
        self.user_email = None

        

        
        self.salesintel_api_key = salesintel_api_key

        self.environments = ["prod", "dev"]
        self.tool_schemas = tool_schemas(anthropic=True)
        
        self.tool_functions = {
            "web_search": web_search,
            "web_content": web_content,
            "web_cache": web_cache,
            "web_scanner": web_scanner,
            "terminal": terminal,
            "python_agent": python_agent,
            "sql_database_agent": sql_database_agent,
            "encode_text": encode_text,
            "decode_tokens": decode_tokens,
            "execute_cypher_query": execute_cypher_query,
            "diffbot_analyze": diffbot_analyze,
            "generate_plan": generate_plan,
            "improve_plan": improve_plan,
            "execute_plan": execute_plan,
            "fts_ingest_document": fts_ingest_document,
            "fts_search_index": fts_search_index,
            "fts_document_qa": fts_document_qa,
            "fts_extract": fts_extract,
            "fts_indices": fts_indices,
            "fact_check": fact_check,
            "graph_query": graph_query,
            "insert_memory": insert_memory,
            "lookup_similar_memories": lookup_similar_memories,
            "delete_memories": delete_memories,
            "amazon_product_finder": self.web_data_client.product_finder,
            "amazon_query_product": self.web_data_client.query_product,
            "amazon_best_sellers": self.web_data_client.best_sellers,
            "amazon_find_deals": self.web_data_client.find_deals,
            "amazon_seller_query": self.web_data_client.seller_query,
            "amazon_category_search": self.web_data_client.category_search,
            "google_search_simple": self.web_data_client.google_search_simple,
            "google_scanner": self.web_data_client.google_scanner,
            "twitter_search": self.web_data_client.twitter_search,
            "reddit_search": self.web_data_client.reddit_search,
        }
        webapp_classes = [
            Agents,
            BusinessIdeas,
            Contents,
            Conversations,
            EmbeddingModels,
            Embeddings,
            Files,
            Health,
            LanguageModels,
            Laws,
            Messages,
            Namespaces,
            Programs,
            Tasks,
            Tools,
            Users,
        ]
        for cls in webapp_classes:
            setattr(self, cls.__name__.lower(), self._init_component(cls))

    def set_auth_header(self):
        if self.access_token:
            self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        else:
            self.session.headers.pop("Authorization", None)

    # Authentication
    def login_user(self, email: str = None, password: str = None):
        url = f"{self.api_host}/v1/users/login"
        response = self.session.post(url, json={"email": email, "password": password})
        response_data = response.json()
        self.access_token = response_data.get('access_token')
        self.api_key = self.access_token

        # expanduser
        try:
            with open(os.path.expanduser("~/.config/brainchain/.access_token"), "w") as f:
                f.write(self.access_token)
                f.close()
        except:
            pass
        
        self.user_id = response_data.get("user_id")
        self.user_email = response_data.get("user_email")

        self.set_auth_header()  # Update headers with new token
        return response_data

    # Users API
    def get_users(self):
        url = f"{self.api_host}/v1/users/"
        response = self.session.get(url)
        return response.json()

    # Conversations API
    def get_all_conversations(self):
        url = f"{self.api_host}/v1/conversations/list"
        response = self.session.get(url)
        return response.json()

    def get_conversation_by_id(self, conversation_id):
        url = f"{self.api_host}/v1/conversations/{conversation_id}"
        response = self.session.get(url)
        return response.json()

    # Messages API
    def get_all_messages(self):
        url = f"{self.api_host}/v1/messages/"
        response = self.session.get(url)
        return response.json()

    def get_message_by_id(self, message_id):
        url = f"{self.api_host}/v1/messages/{message_id}"
        response = self.session.get(url)
        return response.json()

    # Tools API
    def get_all_tools(self):
        url = f"{self.api_host}/v1/tools/"
        response = self.session.get(url)
        return response.json()

    # Language Models API
    def get_all_language_models(self):
        url = f"{self.api_host}/v1/language_models/list"
        response = self.session.get(url)
        return response.json()

    # Conversations API
    def create_conversation(self, messages=[]):
        url = f"{self.api_host}/v1/conversations/"
        data = {"user_id": self.user_id, "messages": messages}
        response = self.session.post(url, json=data)
        return response.json()

    # Messages API
    def create_message(self, conversation_uuid, role, content):
        url = f"{self.api_host}/v1/messages/create"
        data = {"conversation_uuid": conversation_uuid, "user_id": self.user_id, "role": role, "content": content}
        response = self.session.post(url, json=data)
        resp = response.json()
        print(resp)
        return response.json()

    def stream_chat_completion(self, language_model_id, conversation_uuid, mode='single_token', **params):
        url = f"{self.api_host}" + "/v1/language_models/chat/completions/stream"
        params = {
            "llm_id": language_model_id,
            "conversation_uuid": conversation_uuid,
            "mode": mode,
            **params,
        }
        with self.session.get(url, stream=True, params=params) as response:
            response.raise_for_status()
            full_completion = []
            try:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8")
                        if "data: " in decoded_line:
                            token = decoded_line.split("data: ")[1]
                            full_completion.append(token)
                            yield json.dumps({"status": "in_progress", "data": token})

            except KeyboardInterrupt:
                # Handle manual interruption
                pass

        yield json.dumps({"status": "done", "data": "".join(full_completion)})

    # Language Models API
    def get_llm_by_id(self, language_model_id):
        url = f"{self.api_host}/v1/language_models/{language_model_id}/"
        response = self.session.get(url)
        return response.json()

    def get_conversation_messages(self, conversation_id):
        """
        Retrieve messages from a specific conversation.

        Args:
            conversation_id (int): The ID of the conversation.

        Returns:
            dict: A JSON response containing the conversation messages.
        """
        url = f"{self.api_host}/v1/conversations/{conversation_id}/messages"
        response = self.session.get(url)
        return response.json()

    def get_llm_by_model_name(self, language_model_name):
        url = f"{self.api_host}/v1/language_models/{language_model_name}/name"
        response = self.session.get(url)
        return response.json()

    def enforce_login(self, api_key: str = None):
        if not self.access_token or self.api_key or api_key:
            try:
                # change this to expanduser
                with open(os.path.expanduser("~/.config/brainchain/.access_token"), "r") as f:
                    self.access_token = f.read()
                    f.close()
            except Exception as e:
                print(f"No access token found. Trying BRAINCHAIN_API_KEY from environment.")
                self.access_token = api_key or self.api_key or os.environ.get("BRAINCHAIN_API_KEY")
            
            if not self.access_token:
                print("No access token found. Please login.")
                get_user_email = input("email: ")
                get_user_password = getpass("password: ")

                login_response = self.login_user(get_user_email, get_user_password)
                access_token = login_response.get("access_token")
                self.access_token = access_token
                self.api_key = access_token
            
            return login_response

