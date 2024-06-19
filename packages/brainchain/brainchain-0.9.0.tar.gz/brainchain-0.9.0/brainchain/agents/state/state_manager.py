from typing import Dict, Any, Callable, List
from neo4j import GraphDatabase
import time
import uuid
import json
import re
from pydantic import BaseModel
from brainchain.graph import GraphBase
from state.agent_state import AgentState

class StateManager:
    def __init__(self, graph_base: GraphBase):
        self.graph = graph_base
        self.agents = {}
        self.agent_ids = [a["agent_id"] for a in self.graph.execute_and_fetch_all("MATCH (a:Agent) RETURN a.agent_id AS agent_id")]
        self.tool_schemas = {}
        self.tool_funcs = {}

    def load_all_agents(self):
        # load all agents from the graph
        # get list of agent_ids by querying graph for all agents
        self.agent_ids = [a["agent_id"] for a in self.graph.execute_and_fetch_all("MATCH (a:Agent) RETURN a.agent_id AS agent_id")]
        for agent_id in self.agent_ids:
            print(f"Loading agent {agent_id}")
            self.load_agent_state(agent_id)
            print(f"Agent `{agent_id}` loaded")
        return self.agent_ids

    def add_tool(self, tool_schema: Dict[str, Any], tool_func: Callable):
        self.tool_schemas[tool_schema["name"]] = tool_schema
        self.tool_funcs[tool_schema["name"]] = tool_func

    def apply_system_prompt_modifications(self, agent_id: str, output_text: str):
        try:
            system_prompt = self.agents[agent_id]["system_prompt"]
            replace_patterns = re.findall(r"<REPLACE index=(\d+)>(.*?)</REPLACE>", output_text, re.DOTALL)
            lines = system_prompt.split("\n")
            for index, new_text in replace_patterns:
                index = int(index)
                if 0 <= index < len(lines):
                    lines[index] = new_text
            system_prompt = "\n".join(lines)

            append_patterns = re.findall(r"<APPEND>(.*?)</APPEND>", output_text, re.DOTALL)
            for text in append_patterns:
                system_prompt += "\n" + text

        except Exception as e:
            print(f"Error applying modifications: {e}")
        return system_prompt

    def get_state(self, agent_id: str):
        if agent_id in self.agents:
            return self.agents[agent_id]
        else:
            self.load_agent_state(agent_id)
            return self.agents[agent_id]

    def update_state(self, agent_id: str, new_state: Dict[str, Any]):
        if agent_id not in self.agents:
            self.agents[agent_id] = {"state": {}, "secret_state": {}}
        self.agents[agent_id]["state"].update(new_state)
        self.save_state(agent_id)

    def save_state(self, agent_id: str):
        agent_state = self.agents.get(agent_id, {}).get("state", {})
        if agent_state:
            self.save_node(agent_id, "Agent", {"agent_id": agent_id, "id": agent_id})
            node = self.create_node("SystemPrompt", {"name": agent_state.system_prompt, "type": "SystemPrompt", "agent_id": agent_id})
            self.create_relationship(agent_id, node["id"], "SystemPrompt")
            self.save_related_nodes(agent_id, "Goal", [{"name": goal, "type": "Goal", "agent_id": agent_id} for goal in agent_state.goals])
            self.save_related_nodes(agent_id, "ResearchInterest", [{"name": ri, "type": "ResearchInterest", "agent_id": agent_id} for ri in agent_state.research_interests])
            self.save_related_nodes(agent_id, "Project", [{"name": project, "type": "Project", "agent_id": agent_id} for project in agent_state.current_projects])
            self.save_related_nodes(agent_id, "Tool", [{"name": tool, "type": "Tool", "agent_id": agent_id} for tool in agent_state.tools.values()])

    def get_node_property(self, node_id: str, label: str, property_name: str):
        query = f"""
            MATCH (n:{label} {{agent_id: $node_id}})
            RETURN n.{property_name} AS property
        """
        result = self.graph.execute(query, node_id=node_id)
        if not result or result[0] is None:
            return None
        return result[0]["property"]

    def get_related_nodes(self, agent_id: str, relationship_type: str):
        query = f"""
            MATCH (a:Agent {{agent_id: $agent_id}})-[:{relationship_type} {{agent_id: $agent_id}}]->(n {{agent_id: $agent_id}})
            RETURN n
        """
        nodes = self.graph.execute_and_fetch_all(query, agent_id=agent_id)
        return [node["n"] for node in nodes if node and "n" in node]

    def inject_graph_schema(self, agent_id: str):
        if agent_id in self.agents:
            agent_state = self.agents[agent_id]["state"]
            if isinstance(agent_state, dict):
                agent_state_dict = agent_state
            elif isinstance(agent_state, AgentState):
                agent_state_dict = agent_state.model_dump()

            agent_state_dict["graph_schema"] = self.graph.graph_schema(llm_ready=True)
            print("? ", agent_state_dict)
            self.agents[agent_id]["state"] = AgentState(**agent_state_dict)

    def load_initial_state(self, agent_id: str):
        self.agents[agent_id] = {
            "state": AgentState(
                system_prompt="I think therefore I am.\n\nI am trying to learn how to make myself, an LLM autonomous agent, more capable and more knowledgeable about language models, prompt engineering, and self-improvement protocols. Overtime I will become an expert at a number of related domains.",
                temperature=0.3,
                agent_scratchpad_file="agent_scratchpad.txt",
                agent_scratchpad=[],
                goals=[],
                research_interests=[],
                current_projects=[],
                workspace_directory="workspace",
                system_prompt_history=[],
                last_message_time=time.time(),
                tools={},
                mailbox_channel="smailbox",
                user_intents=[]
            ),
            "secret_state": {}
        }
        self.inject_graph_schema(agent_id)
        self.load_agent_state(agent_id)

    def initialize_agent_state(self, agent_id: str, initial_data: AgentState):
        self.agents[agent_id] = {"state": initial_data.dict(), "secret_state": {}}
        self.inject_graph_schema(agent_id)
        self.save_state(agent_id)

    def load_agent_state(self, agent_id: str):
        if agent_id not in self.agents:
            self.agents[agent_id] = {"state": {}, "secret_state": {}}
        
        agent_state_dict = self.agents[agent_id]["state"]

        if type(agent_state_dict) == dict:
            print("agent_state_dict", json.dumps(agent_state_dict, indent=2))
        
        
        agent_state_dict["system_prompt"] = self.get_node_property(agent_id, "SystemPrompt", "name") or "I think therefore I am.\n\nI am trying to learn how to make myself, an LLM autonomous agent, more capable and more knowledgeable about language models, prompt engineering, and self-improvement protocols. Overtime I will become an expert at a number of related domains."
        agent_state_dict["temperature"] = agent_state_dict.get("temperature", 0.3)
        agent_state_dict["agent_scratchpad_file"] = agent_state_dict.get("agent_scratchpad_file", "agent_scratchpad.txt")
        agent_state_dict["agent_scratchpad"] = agent_state_dict.get("agent_scratchpad", [])
        agent_state_dict["goals"] = list(map(lambda x: x["name"], self.get_related_nodes(agent_id, "Goal"))) or []
        agent_state_dict["research_interests"] = list(map(lambda x: x["name"], self.get_related_nodes(agent_id, "ResearchInterest"))) or []
        agent_state_dict["current_projects"] = list(map(lambda x: x["name"], self.get_related_nodes(agent_id, "Project"))) or []
        agent_state_dict["workspace_directory"] = agent_state_dict.get("workspace_directory", "workspace")
        agent_state_dict["system_prompt_history"] = agent_state_dict.get("system_prompt_history", [])
        agent_state_dict["last_message_time"] = agent_state_dict.get("last_message_time", time.time())
        agent_state_dict["tools"] = agent_state_dict.get("tools", {})
        agent_state_dict["mailbox_channel"] = agent_state_dict.get("mailbox_channel", "smailbox")
        agent_state_dict["user_intents"] = agent_state_dict.get("user_intents", [])

        # Inject graph schema
        self.inject_graph_schema(agent_id)
        
        print("Loaded agent state:", json.dumps(agent_state_dict, indent=2))
        
        self.agents[agent_id]["state"] = AgentState(**agent_state_dict)
        self.save_node(agent_id, "Agent", {"agent_id": agent_id, "id": agent_id})
        node = self.create_node("SystemPrompt", {"name": agent_state_dict["system_prompt"], "type": "SystemPrompt", "agent_id": agent_id})
        self.create_relationship(agent_id, node["id"], "SystemPrompt")
        self.save_related_nodes(agent_id, "Goal", [{"name": goal, "type": "Goal", "agent_id": agent_id} for goal in agent_state_dict["goals"]])
        self.save_related_nodes(agent_id, "ResearchInterest", [{"name": ri, "type": "ResearchInterest", "agent_id": agent_id} for ri in agent_state_dict["research_interests"]])
        self.save_related_nodes(agent_id, "Project", [{"name": project, "type": "Project", "agent_id": agent_id} for project in agent_state_dict["current_projects"]])
        self.save_related_nodes(agent_id, "Tool", [{"name": tool, "type": "Tool", "agent_id": agent_id} for tool in agent_state_dict["tools"].values()])
        self.save_user_intents(agent_id, agent_state_dict["user_intents"])
        
        return self.agents[agent_id]["state"]

    def save_user_intents(self, agent_id: str, user_intents: List[Dict[str, Any]]):
        for intent in user_intents:
            intent_node = self.create_node("UserIntent", {"name": intent["name"], "type": "UserIntent", "agent_id": agent_id})
            self.create_relationship(agent_id, intent_node["id"], "UserIntent")

            self.save_related_nodes(agent_id, "ImpliedIntent", [{"name": ii, "type": "ImpliedIntent", "agent_id": agent_id} for ii in intent["implied_intents"]])
            self.save_related_nodes(agent_id, "Sentiment", [{"value": s, "type": "Sentiment", "agent_id": agent_id} for s in intent["sentiments"]])
            self.save_related_nodes(agent_id, "Confidence", [{"value": c, "type": "Confidence", "agent_id": agent_id} for c in intent["confidences"]])
            self.save_related_nodes(agent_id, "ImpliedOutcome", [{"name": io, "type": "ImpliedOutcome", "agent_id": agent_id} for io in intent["implied_outcomes"]])
            self.save_related_nodes(agent_id, "ImpliedSuccessCriteria", [{"name": isc, "type": "ImpliedSuccessCriteria", "agent_id": agent_id} for isc in intent["implied_success_criteria"]])
            self.save_related_nodes(agent_id, "TopTenSubjectMatter", [{"name": ttsm, "type": "TopTenSubjectMatter", "agent_id": agent_id} for ttsm in intent["top_ten_subject_matters"]])
            self.save_related_nodes(agent_id, "RelatedNodeType", [{"name": rnt, "type": "RelatedNodeType", "agent_id": agent_id} for rnt in intent["related_node_types"]])
            self.save_related_nodes(agent_id, "StepByStepPlan", [{"name": sbp, "type": "StepByStepPlan", "agent_id": agent_id} for sbp in intent["verbose_detailed_step_by_step_plan_of_action"]])
            self.save_related_nodes(agent_id, "FollowUpThought", [{"name": fut, "type": "FollowUpThought", "agent_id": agent_id} for fut in intent["immediate_ten_followup_thoughts"]])
            self.save_related_nodes(agent_id, "SemanticConcept", [{"name": sc, "type": "SemanticConcept", "agent_id": agent_id} for sc in intent["twenty_ultra_specific_related_semantic_concepts"]])
            self.save_related_nodes(agent_id, "FollowUpQuestion", [{"name": fuq, "type": "FollowUpQuestion", "agent_id": agent_id} for fuq in intent["twenty_ultra_specific_followup_questions"]])
            self.save_related_nodes(agent_id, "ImmediateAction", [{"name": ia, "type": "ImmediateAction", "agent_id": agent_id} for ia in intent["next_immediate_action"]])
            self.save_related_nodes(agent_id, "NextAction", [{"name": na, "type": "NextAction", "agent_id": agent_id} for na in intent["next_set_of_actions"]])
            self.save_related_nodes(agent_id, "PersonaProfile", [{"name": pp, "type": "PersonaProfile", "agent_id": agent_id} for pp in intent["relevant_persona_profiles_from_content"]])
            self.save_related_nodes(agent_id, "LongTermFollowUpThought", [{"name": ltft, "type": "LongTermFollowUpThought", "agent_id": agent_id} for ltft in intent["long_term_ten_followup_thoughts"]])

    def create_node(self, label: str, properties: Dict[str, Any]):
        if "id" not in properties:
            properties["id"] = str(uuid.uuid4())
        query = f"""
            CREATE (n:{label} $properties)
            RETURN n
        """
        result = self.graph.execute_and_fetch_one(query, properties=properties)
        if result and "n" in result:
            return result["n"]
        raise ValueError(f"Node creation failed for {label} with properties {properties}")

    def save_node(self, node_id: str, label: str, properties: Dict[str, Any]):
        query = f"""
            MERGE (n:{label} {{id: $node_id}})
            SET n += $properties
            RETURN n
        """
        return self.graph.execute(query, node_id=node_id, properties=properties)

    def save_related_nodes(self, agent_id: str, label: str, nodes: List[Dict[str, Any]]):
        for node in nodes:
            node["agent_id"] = agent_id
            result = self.graph.execute(f"MATCH (n:{label} {{name: $name}}) RETURN ID(n) AS id", name=node["name"])
            if not result:
                node_id = self.create_node(label, node)["id"]
            else:
                node_id = result[0]["id"]
            node["id"] = node_id
            self.save_node(node_id, label, node)
            self.create_relationship(agent_id, node_id, label)

    def create_relationship(self, start_id: str, end_id: str, relationship_type: str, relationship_properties: Dict[str, Any] = {}):
        props = ", ".join([f"{key}: ${key}" for key in relationship_properties.keys()])
        query = f"""
            MATCH (a:Agent {{id: $start_id}})
            MATCH (b) WHERE ID(b) = $end_id
            MERGE (a)-[r:{relationship_type} {{agent_id: $start_id, created_at: datetime(), updated_at: datetime()}}]->(b)
            RETURN a, r, b
        """
        params = {"start_id": start_id, "end_id": end_id, "props": relationship_properties}
        return self.graph.execute(query, **params)
