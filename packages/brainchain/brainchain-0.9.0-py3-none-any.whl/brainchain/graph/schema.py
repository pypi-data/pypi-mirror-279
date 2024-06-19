from functools import lru_cache
import matplotlib.pyplot as plt
import networkx as nx
import hashlib, neo4j, logging, json
from neo4j import GraphDatabase, unit_of_work

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
def neo4j_session(uri, user, password):
    """Establish a session with Neo4j."""
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver.session()

class GraphSchema:
    def __init__(self, uri, user, password):
        """Initialize the GraphSchema and fetch schema from Neo4j."""
        self.queries = {}
        self.session = neo4j_session(uri, user, password)
        self.schema_query = 'CALL apoc.meta.schema()'
        self.schema = self.session.run(self.schema_query).single()[0]
        self.view_schema = self.reduce_graph_representation(self.schema)
        self.query_history = []
        self.create_indexes()
        self.create_full_text_search()

    def create_indexes(self, dry_run: bool = True):
        """Create indexes for string properties on all node labels.

        Args:
            dry_run (bool): If True, only print the Cypher queries without executing them.
        """
        for label, info in self.schema.items():
            if info["type"] == "node":
                for prop, prop_info in info["properties"].items():
                    if prop_info["type"] == "STRING":
                        index_name = f"{label}_{prop}_index"
                        query = f"CREATE INDEX {index_name} IF NOT EXISTS FOR (n:{label}) ON (n.{prop})"
                        if dry_run:
                            print(f"[DRY RUN] Cypher query: {query}")
                        else:
                            self.session.run(query)

    def create_full_text_search(self, dry_run: bool = True):
        """Create full-text search indexes for string properties on all node labels.

        Args:
            dry_run (bool): If True, only print the Cypher query without executing it. 
        """
        string_properties = []

        for label, info in self.schema.items():
            if info["type"] == "node":
                for prop, prop_info in info["properties"].items():
                    if prop_info["type"] == "STRING":
                        string_properties.append(f"n.{prop}")

        if string_properties:
            index_name = "node_fulltext_index"
            query = f"CALL db.index.fulltext.createNodeIndex('{index_name}', ['*'], [{','.join(string_properties)}])"
            if dry_run:
                print(f"[DRY RUN] Cypher query: {query}")
            else:
                self.session.run(query)
    
    def close(self):
        self.session.close()
        self.driver.close()

    def markdown(self):
        """Generate a markdown representation of the graph schema."""
        schema_data = self.view_schema
        md_output = []

        def format_properties(properties):
            """Format properties with reduced index and existence information."""
            formatted = []
            for prop, info in properties.items():
                unique = "Unique" if info.get("unique", False) else ""
                prop_type = info.get("type", "Unknown")
                formatted.append(f"- **{prop}** ({prop_type}) {unique}".strip())
            return "\n".join(formatted)

        # Node Labels
        md_output.append("# Node Labels")
        md_output.append(", ".join(schema_data["node_labels"]))
        md_output.append("\n")

        # Edge Labels
        md_output.append("# Edge Labels")
        md_output.append(", ".join(schema_data["edge_labels"]))
        md_output.append("\n")

        # Node Schemas
        md_output.append("# Node Schemas")
        for node, properties in schema_data["node_schemas"].items():
            md_output.append(f"## {node}")
            md_output.append(format_properties(properties))
            md_output.append("\n")

        # Edge Schemas
        md_output.append("# Edge Schemas")
        for edge, schema in schema_data["edge_schemas"].items():
            direction = schema.get("direction", "")
            labels = ", ".join(schema.get("labels", []))
            md_output.append(f"## {edge}")
            md_output.append(f"- Direction: {direction}")
            md_output.append(f"- Labels: {labels}")
            md_output.append("\n")

        return "\n".join(md_output)

    def reduce_graph_representation(self, graph_data):
        """Reduce the graph schema to a structured representation."""
        node_labels = []
        edge_labels = []
        node_schemas = {}
        edge_schemas = {}
        empty_edge_schemas = []

        for name, info in graph_data.items():
            if info["type"] == "node":
                node_labels.append(name)
                node_schemas[name] = info["properties"]

                for rel_name, rel_info in info.get("relationships", {}).items():
                    if rel_name not in edge_schemas:
                        edge_schemas[rel_name] = {"direction": rel_info["direction"], "labels": rel_info["labels"]}
                    if rel_name not in edge_labels:
                        edge_labels.append(rel_name)

            elif info["type"] == "relationship":
                if not info["properties"]:
                    empty_edge_schemas.append(name)
                else:
                    edge_labels.append(name)
                    edge_schemas[name] = info["properties"]

        return {
            "node_labels": node_labels,
            "edge_labels": edge_labels,
            "empty_edge_schemas": empty_edge_schemas,
            "node_schemas": node_schemas,
            "edge_schemas": edge_schemas
        }

    def grid(self):
        """Generate a grid representation of the graph schema."""
        schema_data = self.view_schema
        grid_output = []

        # Function to format properties in grid cells
        def format_property_grid(properties):
            grid_cells = []
            for prop, info in properties.items():
                prop_type = info.get("type", "Unknown")
                unique = "U" if info.get("unique", False) else ""
                grid_cells.append(f"{prop} ({prop_type}) {unique}".strip())
            return " | ".join(grid_cells)

        # Node Schema Grid
        grid_output.append("# Node Schema Grid")
        for node, properties in schema_data["node_schemas"].items():
            grid_output.append(f"### {node}")
            grid_output.append(format_property_grid(properties))
            grid_output.append("\n")

        # Edge Schema Grid with non-empty schemas
        grid_output.append("# Edge Schema Grid")
        for edge, schema in schema_data["edge_schemas"].items():
            direction = schema.get("direction", "")
            labels = ", ".join(schema.get("labels", []))
            grid_output.append(f"### {edge}")
            grid_output.append(f"Direction: {direction} | Labels: {labels}\n")

        # Empty Edge Schema Section
        if schema_data["empty_edge_schemas"]:
            grid_output.append("# Empty Edge Schemas")
            grid_output.append(", ".join(schema_data["empty_edge_schemas"]))
            grid_output.append("\n")

        return "\n".join(grid_output)

    def __repr__(self):
        """Default representation is the markdown schema."""
        return self.markdown()

