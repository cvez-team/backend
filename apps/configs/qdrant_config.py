import os
from qdrant_client import QdrantClient

client = QdrantClient(
    host=os.environ.get("QDRANT_HOST"),
    api_key=os.environ.get("QDRANT_API_KEY"),
)
