from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AgentState(BaseModel):
    system_prompt: str
    temperature: float
    agent_scratchpad_file: str
    agent_scratchpad: List[str]
    goals: List[str]
    research_interests: List[str]
    current_projects: List[str]
    workspace_directory: str
    system_prompt_history: List[str]
    last_message_time: float
    tools: Dict[str, Any]
    mailbox_channel: str
    user_intents: List[Dict[str, Any]] = Field(default_factory=list)
