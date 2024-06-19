def tool_schemas(openai: bool = True, anthropic: bool = False):
    functions_ = [ {
            "type": "function",
            "name": "diffbot_analyze",
            "description": "Performs analysis on a specified URL using the Diffbot Analyze API, returning structured data. This function can be tailored to use specific modes, handle fallbacks, and extract particular fields.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the web page to analyze."
                    },
                    "mode": {
                        "type": "string",
                        "description": "Specific Extract API mode to use, optional."
                    },
                    "fallback": {
                        "type": "string",
                        "description": "Fallback API if an appropriate one cannot be determined, optional."
                    },
                    "fields": {
                        "type": "string",
                        "description": "Specify optional fields to be returned, optional."
                    },
                    "discussion": {
                        "type": "boolean",
                        "description": "Set to false to disable automatic extraction of comments/reviews, optional."
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in milliseconds for the request, default 30000."
                    },
                    "proxy": {
                        "type": "string",
                        "description": "Custom proxy IP address, optional."
                    },
                    "proxyAuth": {
                        "type": "string",
                        "description": "Authentication parameters for the custom proxy, optional."
                    },
                    "useProxy": {
                        "type": "string",
                        "description": "Specify to use custom or no proxy, optional."
                    }
                },
                "required": ["url"]
            },
            "returns": {
                "type": "object",
                "description": "A dictionary with the structured data obtained from the Diffbot analysis."
            }
        },
        {
            "name": "graph_schema",
            "type": "function",
            "description": "Returns the schema of the graph database.",
            "parameters": {
                    "type": "object",
                    "properties": {}
            },
            "returns": {
                "type": "object",
                "description": "A JSON object representing the schema of the graph database.",
            }
        },
        {
            "name": "fact_check",
            "description": "This tool accepts a single string parameter, 'statement', which is a natural language sentence, claim, or even a long paragraph of text. It uses the Brainchain FactCheck service and returns a JSON with the following 4 keys: 1. 'statement' which is the original input statement; 2. 'verdict' which is a natural language description of the veracity of the statement, 3. 'score' which is a numerical score of the veracity of the statement scaled from 0.0 to 1.0;  4. the key 'references' which is a set of references based on the various research and other processing done on the FactCheck service. This is useful to FactCheck statements and check whether things are correct or not, but is just based on relatively simple heuristics, and should not be considered authoritative, only suggestive.",
            "parameters": {
                "type": "object",
                "properties": {
                "statement": {
                    "type": "string",
                    "description": "The statement to fact check."
                }
                },
                "required": [
                "statement"
                ]
            }
        },
        {
            "type": "function",
            "name": "execute_cypher_query",
            "description": "Executes a Cypher query against the graph database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A Cypher query. For example 'MATCH (n:FederalSubagency)-[r]-(m) RETURN n,r,m LIMIT 10' You must always use reasonable limits of no more than 10 per query unless specifically instructed to by the user. "
                    }
                },
                "required": ["query"],
            }
        },
        {
            "type": "function",
            "name": "web_search",
            "description": "Google search results tool: good for typical web searches, weather reports, and other realtime web search query oriented use cases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {
                        "type": "string",
                        "description": "A web search query. For example 'effects of PFAS on the brain' or 'what is the weather in San Francisco'.",
                    },
                },
                "required": ["search_query"],
            },
        },
        {
            "type": "function",
            "name": "web_content",
            "description": "Fetches and returns the content of a given web URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Returns the contents of a page. If its too long, it will be loaded into the FTS service and you will be directed to use that tool."
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "tags you want to extract from the page. Default is ['body']",
                    },
                    "exclude_tags": {
                        "type": "array",
                        "items": {
                                "type": "string"
                        },
                        "description": "tags you want to exclude from the page. Default is ['html', 'script', 'style']",
                    }
                },
                "required": ["url"]
            }
        },
        {
            "type": "function",
            "name": "web_cache",
            "description": "Generates a Google Cache link for a given web URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL for which you want to generate a Google Cache link."
                    }
                },
                "required": ["url"]
            }
        },
        {
            "type": "function",
            "name": "web_scanner",
            "description": "This function will return ((N * 10) + 10) number of links from of Google search result pages for a given N, parametrized. When you are performing research and you want to quickly gets lots of relevant links for a given search query, this will work wonders!",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query for which you want to unroll 10 + ('additional_serp_pages' * 10) google search result links."
                    },
                    "additional_serp_pages": {
                        "type": "integer",
                        "description": "The number of additional search result pages to unroll. Default is 2."
                    },
                },
                "required": ["query", "additional_serp_pages"]
            }
        },
        {
            "type": "function",
            "name": "terminal",
            "description": "Run commands on zsh terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run on the terminal."
                    }
                },
                "required": ["command"]
            }
        },
        {
            "type": "function",
            "name": "python_repl",
            "description": "Run python code in a python console.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to run in the python console."
                    }
                },
                "required": ["code"]
            }
        },
        {
            "type": "function",
            "name": "python_repl_ast",
            "description": "Run python code in a python console.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to run in the python console."
                    }
                },
                "required": ["code"]
            }
        },
        {
            "type": "function",
            "name": "graph_query",
            "description": "Enables you to query the graph database. If you give it a natural language command like 'List 10 federal subagencies', you will get a set of results from the Knowledge Graph.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to run on the graph database."
                    }
                },
                "required": ["query"]
            }
        },
        # FTS function entries
        {
            "type": "function",
            "name": "fts_ingest_document",
            "description": "Ingests a document into the FTS service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the document to ingest."
                    }
                },
                "required": ["url"]
            }
        },
        {
            "type": "function",
            "name": "fts_indices",
            "description": "Returns a mapping of URLs to index_names in the FTS service.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "type": "function",
            "name": "fts_search_index",
            "description": "Searches the index for the given keywords. You should only use this function with results max of 5 or else you will exceed the context length.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The url to associate with the search."
                    },
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of keywords to search for."
                    },
                    "results": {
                        "type": "integer",
                        "description": "The number of results to return. This should be set to a max of 5."
                    },
                    "chunk_indices": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "description": "A list of chunk indices to search for."
                    },
                },
                "required": ["url", "keywords", "results"]
            }
        },
        {
            "type": "function",
            "name": "fts_document_qa",
            "description": "Lets you perform document question answering on ingested URLs, based on a natural language query (which will get applied to all returned document chunks).",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to associate with the QA."
                    },
                    "query": {
                        "type": "string",
                        "description": "The query you are running against the document chunks returned based on the keywords provided for the search."
                    },
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Required keywords to refine the search. The keyword is used to hone in on specific chunks in the document. The query is 'run' against the document chunks that contain the keywords.",
                        "default": []
                    },
                    "dynamic_schema": {
                        "type": "object",
                        "description": "A dictionary of dynamic schema fields to extract from the document. The keys are names of the fields, and the values are the types of the fields. For fts_document_qa, this must always be an empty object, {}",
                        "default": {}

                    }
                },
                "required": ["url", "query", "keywords"]
            }
        },
        {
            "type": "function",
            "name": "fts_extract",
            "description": "Extracts structured data from documents in the index. You must specify a schema (dynamic_schema parameter) to make the most of this tool. This means that you specify a schema for the types of objects you want back, and then it gets wrapped (potentially if you identify multiple items in a chunk of text that are of interest) in a list. For a given text document chunk you need to have a directed set of key values with stuff that you want to extract. If you were doing data extract for a biographic document, you could use: for example, {'name': 'str', 'age': 'int', 'salary': 'Optional[float]'}.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to associate with the extraction."
                    },
                    "query": {
                        "type": "string",
                        "description": "The query you are running against the document chunks returned based on the keywords provided for the search. You must include any keys you want to extract for the dynamic schema."
                    },
                    "keywords": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Keywords to refine the search.",
                        "default": []
                    },
                    "dynamic_schema": {
                        "type": "object",
                        "description": "A dictionary of dynamic schema fields to extract from the document. The keys are names of the fields, and the values are the types of the fields. For example, {'name': 'str', 'age': 'int', 'salary': 'Optional[float]'}. For fts_extract, the sky is the limit. Have fun and be creative with the query and the dynamic_schema. The query must specifically refer to all the fields in the dynamic_schema. For example, {'name': 'str', 'age': 'int', 'salary': 'Optional[float]'} would require a query like 'Extract the name, age, and salary of the person who is the CEO of the company Disney from the document... {document_content}'.",
                        "default": {"summary": "str"}
                    }
                },
                "required": ["url", "query", "keywords", "dynamic_schema"]
            }
        },
        {
            "type": "function",
            "name": "generate_plan",
            "description": "Generates a plan based on a given prompt using a specified model.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Model to use, default should be: 'gpt4-turbo'."},
                    "prompt": {"type": "string", "description": "Prompt to generate the plan from."},
                    "temperature": {"type": "number", "description": "Creativity level, default 1.0."}
                },
                "required": ["prompt"]
            }
        },
        {
            "type": "function",
            "name": "improve_plan",
            "description": "Improves an existing plan based on user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {"type": "string", "description": "User input for improving the plan."},
                    "plan": {"type": "object", "description": "Original plan to be improved."}
                },
                "required": ["user_input", "plan"]
            }
        },
        {
            "type": "function",
            "name": "execute_plan",
            "description": "Executes a given plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "plan": {"type": "object", "description": "Plan to execute."},
                    "model": {"type": "string", "description": "Model to use for execution, Model to use, default should be: 'gpt4-turbo'. Should be either 'gpt4-turbo' or 'gpt-4-32k'."},
                    "prompt": {"type": "string", "description": "Optional prompt for context."},
                    "temperature": {"type": "number", "description": "Creativity level, optional."}
                },
                "required": ["plan", "prompt"]
            }
        },
            {
      "name": "insert_memory",
      "description": "Insert a memory.",
      "parameters": {
        "type": "object",
        "properties": {
          "content": {
            "type": "string",
            "description": "The content of the memory."
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "A list of tags associated with the memory."
          },
          "metadata": {
            "type": "object",
            "additionalProperties": True,
            "description": "Metadata associated with the memory."
          }
        },
        "required": [
          "content"
        ]
      },
      "returns": {
        "type": "object",
        "description": "The JSON response confirming the memory insertion."
      }
    },
    {
      "name": "delete_memories",
      "description": "Delete memories based on a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The query to match memories for deletion."
          }
        },
        "required": [
          "query"
        ]
      },
      "returns": {
        "type": "object",
        "description": "The JSON response confirming the deletion of memories."
      }
    },
    {
      "name": "lookup_similar_memories",
      "description": "Lookup similar memories based on a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The query to find similar memories."
          }
        },
        "required": [
          "query"
        ]
      },
      "returns": {
        "type": "object",
        "description": "The JSON response with similar memories found."
      }
    }
    ]

    if anthropic:
        new_out = []
        for item in functions_:
            new_item = {}
            for k in item:
                if k == "parameters":
                    new_item["input_schema"] = item[k]
                elif k == "type" or k == "returns":
                    pass
                else:
                    new_item[k] = item[k]
            new_out.append(new_item)
        return new_out
    if openai:    
        return functions_
