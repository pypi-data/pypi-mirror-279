import tiktoken
from .brainchain import Brainchain
from transformers import AutoTokenizer, AutoModel
import torch
from .products import ProductsAPI
from .tools.web import web_search, web_content, web_cache, web_scanner
from .tools.coding import python_agent, sql_database_agent, terminal
from .tools.memory import insert_memory, lookup_similar_memories, delete_memories
from .tools.tokens import encode_text, decode_tokens
from .tools.fts import fts_ingest_document, fts_search_index, fts_document_qa, fts_extract, fts_indices, fts_health_check
from .tools.graph import execute_cypher_query, graph_query
from .tools.factual import fact_check
from .tools.diffbot import diffbot_analyze
from .tools.plan import generate_plan, improve_plan, execute_plan
from .graph.schema import GraphSchema
from .graph.base import GraphBase

import asyncio
import functools
import logging
import os
import time
import boto3
import watchtower

from mlx_embedding_models.embedding import EmbeddingModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure AWS credentials
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
aws_region = os.environ.get("AWS_REGION", "us-west-2")

# Configure CloudWatch logging default log group is watchtower
log_group_name = os.environ.get("LOG_GROUP_NAME")
log_stream_name = os.environ.get("LOG_STREAM_NAME")

try:
    # Set up the logger to send logs to CloudWatch
    handler = watchtower.CloudWatchLogHandler(
        log_group=log_group_name, stream_name=log_stream_name
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
except:
    logger.error("Failed to set up logging to CloudWatch")

def log_function_info(func):
    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Log function name and parameters at the beginning
            logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")

            start_time = time.time()

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info(f"{func.__name__} completed in {elapsed_time:.4f} seconds")

            return result

        return async_wrapper
    else:

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")

            start_time = time.time()

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info(f"{func.__name__} completed in {elapsed_time:.4f} seconds")

            return result

        return sync_wrapper

from .assistants import AssistantClient

import os

try:
    BC_EMBEDDING_MODEL = os.getenv("BC_EMBEDDING_MODEL", "bge-m3")
    BC_TOKENIZER_MODEL = os.getenv("BC_TOKEN_ENCODING", "cl100k_base")
except:
    pass

# Load the MLX embedding model
mlx_model = EmbeddingModel.from_registry(BC_EMBEDDING_MODEL)

class Silk(str):
    def __new__(cls, content: str):
        obj = super().__new__(cls, content)
        # Using tiktoken for initial tokenization to count tokens
        obj.tokenizer = tiktoken.get_encoding(BC_TOKENIZER_MODEL)
        obj.tokens = obj.tokenizer.encode(content)
        obj._token_count = len(obj.tokens)
        return obj

    @property
    def token_count(self):
        """Returns the count of tokens."""
        return self._token_count

    def embed(self):
        """Generates embeddings for the string using the MLX model."""
        # Convert tiktoken tokens to a string
        text = self.tokenizer.decode(self.tokens)
        embeddings = mlx_model.encode([text])
        return torch.tensor(embeddings[0])

    def cosim(self, other):
        """Calculates the cosine similarity between two Silk instances."""
        if not isinstance(other, Silk):
            raise ValueError("Both objects must be instances of Silk")
        embedding1 = self.embed()
        embedding2 = other.embed()
        # Calculate the cosine similarity
        cos_sim = torch.nn.functional.cosine_similarity(embedding1, embedding2, dim=0)
        return cos_sim.item()

    def __add__(self, other):
        combined = super().__add__(other)
        return Silk(combined)
