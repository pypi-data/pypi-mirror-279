import requests
import json
import os

import asyncio
import functools
# import logging
import os
import time
from .tools import *
import time

class AssistantClient:
    def __init__(self, assistants_api_host: str = "https://assistants-api.brainchain.cloud", api_host: str = "https://api.brainchain.cloud", debug: bool = False):
        self.API_HOST = api_host or os.getenv("ASSISTANTS_API_HOST") 
        self.ASSISTANTS_API_HOST = assistants_api_host or os.getenv("API_HOST")
        self.DEBUG = debug
        if self.DEBUG:
            print(f"Brainchain API: {self.API_HOST}")
            print(f"Assistants API: {self.ASSISTANTS_API_HOST}")

    # @log_function_info
    def send_request(self, method, url, data=None, params=None, debug: bool = True, headers: dict = {}):
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            default_headers.update(headers)
        headers = default_headers

        if debug:
            print("Headers: ", headers)
            print("Sending request...")
            print("Method: ", method)
            print("URL: ", url)
            print("Printing request prior to sending...")
            print("headers: ", headers)
            print("data: ", data)
            print("params: ", json.dumps(params, indent=2))

        response = requests.request(method, url, headers=headers, data=json.dumps(data, indent=2), params=params)

        if debug:
            print("response headers...")
            print(response.headers)
            print("response content...")


        try:
            return response.json()
        except Exception as e:
            return "Error: " + str(e)

    # @log_function_info
    def get_user_uuid(self, token):
        # login to get user uuid
        url = f"{self.API_HOST}/v1/users/me"
        #print(url)

        headers = {'accept': 'application/json', "Authorization": f"Bearer {token}"}
        resp = self.send_request("GET", url, headers=headers, debug=False)
        #print(resp)
        return resp
        
    # @log_function_info
    def register_user(self, email: str, username: str, password: str):
        url = f"{self.API_HOST}/v1/users/"
        
        payload = {
            "email": email,
            "password": password,
            "username": username,
        }

        return self.send_request("POST", url, data=payload)

    # @log_function_info
    def login_user(self, email, password):
        url = f"{self.API_HOST}/v1/users/login"
        data = {"email": email, "password": password}
        return self.send_request("POST", url, data=data)
    
    # @log_function_info
    def list_assistants(self):
        url = f"{self.ASSISTANTS_API_HOST}/v1/assistants/"
        return self.send_request("GET", url)
    
    # @log_function_info
    def get_thread(self, thread_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}"
        return self.send_request("GET", url)

    # @log_function_info# 1. Get Assistant
    def get_assistant(self, assistant_id, update: bool = False):
        url = f"{self.ASSISTANTS_API_HOST}/v1/assistants/{assistant_id}"
        return self.send_request("GET", url, params={"update": update})

    
    # 2. Create Assistant
    # @log_function_info
    def create_assistant(self, assistant_data):
        url = f"{self.ASSISTANTS_API_HOST}/v1/assistants"
        return self.send_request("POST", url, data=assistant_data)

    # 3. Create Thread
    # @log_function_info
    def create_thread(self, assistant_id: str = "", user_id: str = ""):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads"
        thread_data = {"assistant_id": assistant_id, "user_id": user_id}
        return self.send_request("POST", url, data=thread_data)

    # @log_function_info
    def retrieve_thread(self, thread_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}"
        return self.send_request("GET", url)

    # 4. Add Message to Thread
    def add_message_to_thread(self, thread_id, content: str, role: str = "user"):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/messages"

        message_data = {
            "thread_id": thread_id,
            "role": role,
            "content": content
        }
        resp = self.send_request("POST", url, data=json.dumps(message_data))
        return resp

    # 5. Create Run
    def create_run(self, thread_id, assistant_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/runs"
        data = {"thread_id": thread_id, "assistant_id": assistant_id}
        return self.send_request("POST", url, params=data)

    # 6. Retrieve Run
    def retrieve_run(self, thread_id, run_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/runs/{run_id}"
        return self.send_request("GET", url)

    def add_message(self, thread_id: str = None, content: str = None, role: str = "user"):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/messages"
        message_data = {
            "thread_id": thread_id,
            "role": role,
            "content": content
        }
        response = self.send_request("POST", url, data=message_data, params={"thread_id": thread_id})
        return response

    # 7. Get Messages for Thread
    def get_messages_for_thread(self, thread_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/messages"
        return self.send_request("GET", url)

    # 12 list threads
    # @log_function_info
    def list_threads(self, user_id: str):
        url = f"{self.ASSISTANTS_API_HOST}/threads/"
        params = {"user_id": user_id}
        return self.send_request("GET", url, params=params)

    # 8. Submit Tool Outputs
    # @log_function_info
    def submit_tool_outputs(self, thread_id, run_id, tool_outputs):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/runs/submit_tool_outputs"
        #print("Tool outputs: \n", json.dumps(tool_outputs, indent=2))
        #print("URL: ", url)
        data = {
            "thread_id": thread_id,
            "run_id": run_id,
            "tool_outputs": tool_outputs
        }
        json.dumps(data, indent=2)
        return self.send_request("POST", url, data=data)

    # add tiktoken counting to output
    # @log_function_info
    def process_run_response(self, run_id, thread_id):
        run_response = self.retrieve_run(thread_id, run_id)
        thread = self.retrieve_thread(thread_id)
        tool_outputs = []
        if type(run_response) is not dict:
            run_response = run_response.model_dump()
        if type(thread) is not dict:
            thread = thread.model_dump()

        run_id = run_response["id"]
        thread_id = thread["id"]
        required_action = run_response["required_action"] if "required_action" in run_response else {}
        if required_action["type"] == "submit_tool_outputs":
            for tool_call in required_action.get("submit_tool_outputs", {}).get("tool_calls", []):
                tool_call_id = tool_call.get("id")
                tool_name = tool_call.get("function", {}).get("name")
                tool_arguments = tool_call.get("function", {}).get("arguments")
                # Dynamically call the function based on tool name
                if tool_name and tool_arguments:
                    print("Tool name: ", tool_name)
                    print("Tool arguments: ", tool_arguments)
                    tool_function = globals().get(tool_name)
                    if tool_function:
                        # Assuming arguments are JSON string, parse them
                        try:
                            tool_args = json.loads(tool_arguments)
                             # check if its an async function
                            output = tool_function(**tool_args)
                            #print(output)
                        except Exception as e:
                            return f"Error: {e}"
                        
                        if type(output) == "dict":
                            output = json.dumps(output,indent=2)
                        else:
                            output = str(output)
                        tool_outputs.append({
                            "tool_call_id": tool_call_id,
                            "output": output
                        })
                    else:
                        return "Tool not found: '{}'".format(tool_name)
        if tool_outputs:
            tool_outputs_submitted = self.submit_tool_outputs(
                run_id=run_id, thread_id=thread_id, tool_outputs=tool_outputs
            )
            json.dumps(tool_outputs_submitted, indent=2)
            return tool_outputs_submitted
        return None
    
    # @log_function_info
    def generate_thread_title(self, thread_id, prompt) -> dict:
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/title"
        data = {
            "prompt": prompt,
            "thread_id": thread_id
        }
        return self.send_request("POST", url, data=data)

    # @log_function_info
    def update_all_untitled_threads(self):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/title-untitled-threads"
        return self.send_request("POST", url)
    
    # @log_function_info
    def get_run_for_thread(self, thread_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/runs"
        return self.send_request("GET", url)
    
    # @log_function_info
    def get_run(self, thread_id, run_id):
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/runs/{run_id}"
        return self.send_request("GET", url)

    # @log_function_info
    def wait_for_completions(self, thread_id, run_id, latest=True):
        retries = 0
        max_retries = 2048  # Maximum number of retries
        initial_delay = 0.3  # Initial delay in seconds
        max_delay = 2.0  # Maximum delay in seconds
        min_delay = 0.125  # Minimum delay in seconds after decay
        delay = initial_delay
        increasing = True  # Flag to indicate if we are in increasing or decreasing phase
        run = self.retrieve_run(thread_id, run_id)

        while run["status"] not in ["completed", "failed", "expired"] and retries < max_retries:
            run = self.retrieve_run(thread_id, run_id)
            print(run["status"])
            if run["status"] == "completed":
                messages = self.get_messages_for_thread(thread_id)
                #print(json.dumps(messages, indent=2))
                #print(messages[-1]['content'])
                try:
                    text_value = json.loads(messages[-1]['content'])[0]["text"]["value"]
                    text_annotations = json.loads(messages[-1]['content'])[0]["text"]["annotations"]
                    if len(text_annotations) > 0:
                        text_value += ' '.join(text_annotations)
                    return text_value
                except:
                    return messages[-1]['content']
            elif run["status"] == "requires_action":
                messages = self.get_messages_for_thread(thread_id)
                self.process_run_response(run_id, thread_id)
            elif run["status"] in ["queued", "running", "in_progress"]:
                # Wait for the current delay period
                time.sleep(delay)
                # Adjust delay based on current phase
                if increasing:
                    delay *= 2.0
                    if delay > max_delay:
                        delay = max_delay
                        increasing = False  # Start decreasing delay
                else:
                    delay /= 1.5
                    if delay < min_delay:
                        delay = min_delay
                        increasing = True  # Reset to increasing phase for next cycle
            elif run["status"] == "expired":
                print("Run expired")
                break
            elif run.get("status") == "failed":
                print("Run failed")
                break
            else:
                print(run["status"])
            retries += 1
        if retries >= max_retries:
            print("Maximum retries reached")

    # @log_function_info
    def cancel_run(self, thread_id: str, run_id: str):
        """
        Cancels a run in a specified thread.

        :param thread_id: The ID of the thread containing the run.
        :param run_id: The ID of the run to cancel.
        :return: The response from the server after attempting to cancel the run.
        """
        url = f"{self.ASSISTANTS_API_HOST}/v1/threads/{thread_id}/runs/{run_id}/cancel"
        return self.send_request("POST", url)

    # @log_function_info        
    def prompt(self, question: str, assistant_id: str = "asst_GQVj4wV8Gd4wSo10aGW6XTs6", thread_id: str = None, execute_run: bool = False):
        if thread_id is None:
            thread = self.create_thread(assistant_id)
            thread_id = thread.get("id")

        request = self.add_message(thread_id, content=question)
        #print("Request: ", request)
        #print("Length of thread now: ", len(self.get_messages_for_thread(thread_id)))
        if execute_run:
            try:
                run = self.create_run(thread_id=thread_id, assistant_id=assistant_id)
                run_id = run.get("id")
            except:
                get_run_to_kill = self.get_run_for_thread(thread_id)
                #print(get_run_to_kill)
                run_id = get_run_to_kill[0]["id"]
                self.cancel_run(thread_id, run_id)
                run = self.create_run(thread_id=thread_id, assistant_id=assistant_id)
                run_id = run.get("id")


            return self.wait_for_completions(thread_id, run_id)
        else:
            return request
