from .schema import GraphSchema
from neo4j import GraphDatabase
from functools import lru_cache
import matplotlib.pyplot as plt
import networkx as nx
import hashlib
import neo4j

import os
import json
GRAPH_URL = os.getenv("GRAPH_URL", "bolt://n4j.brainchain.cloud")
GRAPH_USER = os.getenv("GRAPH_USER", "neo4j")
GRAPH_PASSWORD = os.getenv("GRAPH_PASSWORD")

class GraphBase():
    def __init__(self, uri: str = GRAPH_URL, user: str = GRAPH_USER, password: str = GRAPH_PASSWORD):
        self.schema = GraphSchema(uri, user, password)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session()
        self.default_node_formatters = {
            "GPE": lambda n: n.get("name", "") or n.get("id", ""),
            "FederalAward": lambda n: n.get("id", ""),
            "Material": lambda n: n.get("name", "") or n.get("id", ""),
            "FederalContract": lambda n: n.get("id", ""),
            "FederalPayment": lambda n: n.get("id", ""),
            "FederalSubContract": lambda n: n.get("id", ""),
            "FederalSubGrant": lambda n: n.get("id", ""),
            "Org": lambda n: n.get("name", "") or n.get("id", ""),
            "Component": lambda n: n.get("name", "") or n.get("id", ""),
            "Company": lambda n: n.get("name", "") or n.get("id", ""),
            "FederalIDV": lambda n: n.get("id", ""),
            "Product": lambda n: n.get("name", "") or n.get("id", ""),
            "Country": lambda n: n.get("name", "") or n.get("id", ""),
            "City": lambda n: n.get("name", "") or n.get("id", ""),
            "FederalGrant": lambda n: n.get("id", ""),
            "State": lambda n: n.get("name", "") or n.get("id", ""),
            "Facility": lambda n: n.get("id", ""),  # Assuming no name property for Facility nodes
            "FederalAgency": lambda n: n.get("name", "") or n.get("id", ""),
            "FederalLoan": lambda n: n.get("id", ""),
            "FederalSubagency": lambda n: n.get("name", "") or n.get("id", ""),
            "NAICS": lambda n: n.get("code", "")  # Use NAICS code as label
        }

        self.default_edge_formatters = {
            "IS_IN": lambda r: "",  # Hide edge labels for IS_IN relationships 
            "HAS_LOCATION": lambda r: "", 
            "LOCATED_IN": lambda r: "",
            "HAS_FUNDING_AGENCY": lambda r: "", 
            "HAS_MATERIAL": lambda r: "",
            "HAS_COMPONENT": lambda r: "",
            "IN_NAICS": lambda r: "",
            "HAS_NAICS": lambda r: "",
            "IS_SUBAGENCY": lambda r: "", 
        }

    def close(self):
        self.session.close()
        self.driver.close()

    def graph_schema(self, llm_ready: bool = True):
        if llm_ready:
            return self.schema.grid()+"\n\n"+json.dumps(self.node_relationship_adjacencies(), indent=2)
        else:
            return self.schema.schema
    
    def execute(self, query, **kwargs):
        result = self.session.run(query, **kwargs)
        return [record.data() for record in result]

    def execute_and_fetch_one(self, query, **kwargs):
        result = self.session.run(query, **kwargs)
        return result.single().data()

    def execute_and_fetch_all(self, query, **kwargs):
        result = self.session.run(query, **kwargs)
        return [record.data() for record in result]
    
    def visualize_graph_custom(self, graph_data, node_formatters=None, edge_formatters=None):
        """Visualize the graph with custom formatting for node and edge labels."""

        G = nx.DiGraph()
        nodes = {}
        relationships = []

        # Process nodes and relationships (similar to get_random_subgraph)
        for group in graph_data:
            startNodes = group['startNodes']
            connectedNodes = group['connectedNodes']
            rels = group['relationships']

            # Add nodes to the graph
            for node in startNodes + connectedNodes: 
                try:
                    node_id = self.generate_node_id(node) 
                    if node_id not in nodes:
                        node["id"] = node_id  
                        nodes[node_id] = node
                        label = node.get("name", "") or node.get("description", "") or node_id 
                        G.add_node(node_id, label=label, properties=node)
                except Exception as e:
                    print("Error processing node:", node, e)
                    pass

            # Add relationships to the graph
            for rel_group in rels:
                for rel in rel_group:
                    try:
                        start_node = rel[0]
                        start_node_id = start_node.get("id", self.generate_node_id(start_node)) 
                        end_node = rel[2]
                        end_node_id = end_node.get("id", self.generate_node_id(end_node)) 
                        rel_type = rel[1]
                        G.add_edge(start_node_id, end_node_id, type=rel_type, properties=rel[3] if len(rel) > 3 else {})
                    except Exception as e:
                        print("Error processing relationship:", rel, e)
                        pass

        # Apply formatting functions with defaults
        node_formatters = node_formatters or self.default_node_formatters
        edge_formatters = edge_formatters or self.default_edge_formatters

        node_labels = {}
        for node_id, node in nodes.items():
            label = node.get("name", "") or node.get("description", "") or node_id
            formatter = node_formatters.get(label, lambda n: n) 
            node_labels[node_id] = formatter(node)

        print
        edge_labels = {}
        for rel in relationships:
            formatter = edge_formatters.get(rel.get("type"), lambda r: r.get("type"))
            edge_labels[(rel.start_node["id"], rel.end_node["id"])] = formatter(rel)

        # Visualization with customized labels
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
        nx.draw_networkx_labels(G, pos, labels=node_labels)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.show()

    def generate_node_id(self, node):
        """Generate a unique ID for nodes that don't have an 'id' field."""
        return hashlib.md5(str(node).encode()).hexdigest()
    
    def serialize_neo4j_time(obj):
        """Serialize neo4j.time.Date objects to string."""
        if isinstance(obj, neo4j.time.Date):
            return str(obj)
        return obj

    def serialize_neo4j_node(self, node):
        """Serialize a Neo4j node to a dictionary."""
        return {
            'id': node.id,
            'labels': node.labels,
            'properties': dict(node.items())
        }

    def serialize_neo4j_relationship(self, relationship):
        """Serialize a Neo4j relationship to a dictionary."""
        return {
            'id': relationship.id,
            'type': relationship.type,
            'properties': dict(relationship.items()),
            'start_node': self.serialize_neo4j_node(relationship.start_node),
            'end_node': self.serialize_neo4j_node(relationship.end_node)
        }
    

    def get_random_subgraph(self, start_node_label: str, depth: int = 1, limit: int = 5, visualize: bool = True):
        subgraph_query = f"""
        MATCH (start:{start_node_label})
        WITH start, ID(start) AS start_id
        ORDER BY rand() LIMIT {limit}
        WITH start, start_id, size([(start)-->() | 1]) AS outgoing_count
        ORDER BY outgoing_count DESC LIMIT 1
        CALL {{
            WITH start
            MATCH (start)-[r*0..{depth}]-(connected)
            RETURN ID(start) AS sub_start_id, ID(connected) AS sub_connected_id, start AS sub_start, connected AS sub_connected, collect(r) AS relationships
        }}
        RETURN
            sub_start_id AS start_id,
            sub_connected_id AS connected_id,
            collect(distinct sub_start) AS startNodes,
            collect(distinct sub_connected) AS connectedNodes,
            relationships
        LIMIT {limit}
        """.strip()

        result = self.execute(subgraph_query)

        if visualize:
            self.visualize_graph_custom(result)  # Call the custom visualization method
        return result

    # Advanced Graph Management Functions
    def add_node(self, node_label, properties):
        query = f"CREATE (node:{node_label} $properties) RETURN node"
        return self.execute_and_fetch_one(query, properties=properties)

    def add_relationship(self, start_id, end_id, relationship_type, properties):
        query = f"""
            MATCH (start), (end)
            WHERE ID(start) = $start_id AND ID(end) = $end_id
            CREATE (start)-[rel:{relationship_type} $properties]->(end)
            RETURN start, rel, end
        """
        return self.execute_and_fetch_one(query, start_id=start_id, end_id=end_id, properties=properties)

    def find_nodes_by_text(self, text):
        query = "CALL db.index.fulltext.queryNodes('nodeFullText', $text) YIELD node RETURN node"
        return self.execute_and_fetch_all(query, text=text)

    def find_relationships_by_text(self, text):
        query = "CALL db.index.fulltext.queryRelationships('relationshipFullText', $text) YIELD relationship RETURN relationship"
        return self.execute_and_fetch_all(query, text=text)

    def find_path_between_nodes(self, start_id, end_id):
        query = f"""
            MATCH path = shortestPath((start)-[*..10]-(end))
            WHERE ID(start) = $start_id AND ID(end) = $end_id
            RETURN path
        """
        return self.execute_and_fetch_one(query, start_id=start_id, end_id=end_id)

    def count_nodes(self, node_label):
        query = f"MATCH (node:{node_label}) RETURN count(node) as count"
        return self.execute_and_fetch_one(query)

    def count_relationships(self, relationship_type):
        query = f"MATCH ()-[rel:{relationship_type}]->() RETURN count(rel) as count"
        return self.execute_and_fetch_one(query)

    def get_all_node_labels(self):
        query = "CALL db.labels()"
        return self.execute_and_fetch_all(query)

    def get_all_relationship_types(self):
        query = "CALL db.relationshipTypes()"
        return self.execute_and_fetch_all(query)

    def get_all_property_keys(self):
        query = "CALL db.propertyKeys()"
        return self.execute_and_fetch_all(query)

    def delete_all_nodes_and_relationships(self):
        query = "MATCH (n) DETACH DELETE n"
        return self.execute(query)

    def merge_node(self, node_label, key_property, properties):
        query = f"""
            MERGE (node:{node_label} {{ {key_property}: $properties.{key_property} }})
            ON CREATE SET node = $properties
            ON MATCH SET node += $properties
            RETURN node
        """
        return self.execute_and_fetch_one(query, properties=properties)

    def merge_relationship(self, start_id, end_id, relationship_type, properties):
        query = f"""
            MATCH (start), (end)
            WHERE ID(start) = $start_id AND ID(end) = $end_id
            MERGE (start)-[rel:{relationship_type}]->(end)
            ON CREATE SET rel = $properties
            ON MATCH SET rel += $properties
            RETURN start, rel, end
        """
        return self.execute_and_fetch_one(query, start_id=start_id, end_id=end_id, properties=properties)

    def list_indexes(self):
        query = "CALL db.indexes()"
        return self.execute_and_fetch_all(query)

    def drop_index(self, index_name):
        query = f"DROP INDEX {index_name} IF EXISTS"
        return self.execute(query)

    def list_constraints(self):
        query = "CALL db.constraints()"
        return self.execute_and_fetch_all(query)

    def drop_constraint(self, constraint_name):
        query = f"DROP CONSTRAINT {constraint_name} IF EXISTS"
        return self.execute(query)

    def enable_automatic_indexing(self):
        query = "CALL dbms.setConfigValue('dbms.auto_index.nodes.enabled', 'true')"
        return self.execute(query)

    def disable_automatic_indexing(self):
        query = "CALL dbms.setConfigValue('dbms.auto_index.nodes.disabled', 'true')"
        return self.execute(query)
    
    def upsert_node(self, node_label, key_property, properties):
        query = f"""
            MERGE (node:{node_label} {{{key_property}: $properties.{key_property}}})
            ON CREATE SET node = $properties
            ON MATCH SET node += $properties
            RETURN node
        """
        return self.execute_and_fetch_one(query, properties=properties)

    def upsert_relationship(self, start_id, end_id, relationship_type, key_property, properties):
        query = f"""
            MATCH (start), (end)
            WHERE ID(start) = $start_id AND ID(end) = $end_id
            MERGE (start)-[rel:{relationship_type} {{{key_property}: $properties.{key_property}}}]->(end)
            ON CREATE SET rel = $properties
            ON MATCH SET rel += $properties
            RETURN start, rel, end
        """
        return self.execute_and_fetch_one(query, start_id=start_id, end_id=end_id, properties=properties)

    def compare_nodes(self, node_label, node1_id, node2_id):
        query = f"""
            MATCH (node1:{node_label}), (node2:{node_label})
            WHERE ID(node1) = $node1_id AND ID(node2) = $node2_id
            RETURN apoc.node.compare(node1, node2) AS comparisonResult
        """
        return self.execute_and_fetch_one(query, node1_id=node1_id, node2_id=node2_id)

    def get_node_connectivity_vector(self, start_label, relationship_type):
        """
        Returns a 3D vector representation of node label connectivity.

        Args:
            start_label (str): The starting node label.
            relationship_type (str): The relationship type to traverse.

        Returns:
            list: A list of tuples, where each tuple represents (connected_label, count).
        """

        query = f"""
        MATCH (start:{start_label})-[rel:{relationship_type}]->(end)
        RETURN labels(end)[0] AS connected_label, count(*) AS count
        ORDER BY count DESC
        """

        result = self.execute_and_fetch_all(query)
        return result
    
    @lru_cache(maxsize=None)  # Use LRU cache with unlimited size
    def node_relationship_adjacencies(self, remove_empty: bool = True):
        """
        Calculates node label adjacencies based on relationship types.

        Args:
            remove_empty (bool): Whether to remove empty connections from the result.

        Returns:
            dict: A dictionary representing the connectivity between node labels.
        """

        connections = {}
        node_labels = self.get_all_node_labels()
        rel_types = list(map(lambda x: x["relationshipType"], self.get_all_relationship_types()))

        for label in node_labels:
            label_ = label["label"]
            connections[label_] = {}  # Initialize connections for the label

            for rel in rel_types:
                connected_nodes = self.get_node_connectivity_vector(label_, rel)
                if not remove_empty or connected_nodes:  # Add only if not empty or removal is disabled
                    connections[label_][rel] = connected_nodes

        return connections

    def get_random_nodes_collection(self, node_label, count):
        query = f"""
            MATCH (node:{node_label})
            RETURN node
            ORDER BY rand()
            LIMIT $count
        """
        return self.execute_and_fetch_all(query, count=count)

    def visualize_graph(self, start_node, connected_nodes, relationships):
        G = nx.DiGraph()
        G.add_node(start_node['id'], **start_node)
        for node in connected_nodes:
            G.add_node(node['id'], **node)
        for rel in relationships:
            G.add_edge(rel.start_node['id'], rel.end_node['id'], **rel)
        nx.draw(G, with_labels=True)
        plt.show()

    def expand_node_set(self, node_label, relationship_type, count):
        query = f"""
            MATCH (start:{node_label})-[rel:{relationship_type}]->(end)
            RETURN start, collect(end) AS connectedNodes
            LIMIT $count
        """
        return self.execute_and_fetch_all(query, count=count)

    def path_to_all_related_nodes(self, start_id):
        query = f"""
            MATCH path = (start)-[*]-(related)
            WHERE ID(start) = $start_id
            RETURN path
        """
        return self.execute_and_fetch_all(query, start_id=start_id)

    def detach_delete_node(self, node_id):
        query = f"""
            MATCH (node)
            WHERE ID(node) = $node_id
            DETACH DELETE node
        """
        return self.execute(query, node_id=node_id)

    def delete_relationships_by_type(self, relationship_type):
        query = f"""
            MATCH ()-[rel:{relationship_type}]->()
            DELETE rel
        """
        return self.execute(query)

    # Additional helper methods for complex graph operations

    def create_snapshot(self):
        query = """
            CALL apoc.export.cypher.all('snapshot.cypher', {
                format: 'cypher-shell'
            })
        """
        return self.execute(query)

    def restore_from_snapshot(self, snapshot_file):
        query = f"""
            CALL apoc.cypher.runFile('{snapshot_file}')
        """
        return self.execute(query)

    def analyze_graph(self):
        query = """
            CALL apoc.meta.stats()
            YIELD labels, relTypesCount
            RETURN labels, relTypesCount
        """
        return self.execute_and_fetch_one(query)

