import requests, json, os
from typing import Optional

def generate_plan(prompt: str, model: str = "gpt4-turbo", temperature: float = 1.0, n: int = 1) -> dict:
    if model not in ["gpt4-turbo", "gpt-4-32k"]:
        model = "gpt4-turbo"
        print(f"Model invoked: {model}. This is not a valid model. Reverting to 'gpt4-turbo")
    
    url = "https://brainchain--planner.modal.run/v1/plans/create"

    data = {"model": model, "prompt": prompt, "temperature": temperature, "n": n}

    response = requests.post(url, json=data)
    
    print(json.dumps(data, indent=2))
    print(json.dumps(response.content.decode('utf-8'), indent=2))

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def improve_plan(user_input: str, model: str = "gpt4-turbo", plan: dict = {"steps": []}, default_prompt: str = "For the following plan: {plan_}, please make the following changes: {user_input}.", temperature: float = 1.0) -> dict:
    url = "https://brainchain--planner.modal.run/v1/plans/create"
    data = {"model": model, "prompt": default_prompt.format(plan_=json.dumps(plan, indent=2), user_input=user_input), "temperature": temperature}
    response = requests.post(url, json=data)
    print(json.dumps(data, indent=2))
    print(json.dumps(json.loads(response.content), indent=2))

    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def execute_plan(prompt: str, model: str = "gpt4-turbo", plan: Optional[dict] = {"steps": []}, temperature: float = 1.0) -> dict:
    url = "https://brainchain--planner.modal.run/v1/plans/execute"
    data = {"model": "gpt4-turbo", "prompt": prompt, "temperature": temperature, "plan": plan}
    response = requests.post(url, json=data)
    print(json.dumps(data, indent=2))
    print(json.dumps(json.loads(response.content), indent=2))
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
