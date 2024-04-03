from typing import List, AnyStr, Dict
import numpy as np
from fastapi import HTTPException, status
from ..providers import embedder, vector_db
from ..utils.constants import DEFAULT_EMBEDDING_PROVIDER, DEFAULT_QUERY_LIMIT, DEFAULT_SPACE_NAME


class VectorEmbeddingSchema:
    def __init__(
        self,
        vectors: List[List[float]],
        documents: List[AnyStr],
        payloads: List[Dict],
        provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER,
    ):
        self.vectors = [np.array(vector) for vector in vectors]
        self.documents = documents
        self.payloads = payloads
        self.provider = provider

    @staticmethod
    def from_documents(documents: List[AnyStr], payloads: List[Dict], provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER):
        vectors = embedder.embed(documents, provider)
        return VectorEmbeddingSchema(vectors, documents, payloads, provider)

    @staticmethod
    def from_database(collection: AnyStr, space: AnyStr = DEFAULT_SPACE_NAME):
        records = vector_db.get_all(collection, space)
        vectors = []
        documents = []
        payloads = []
        for record in records:
            vectors.append(record.vector)
            documents.append(record.payload["document"])
            payloads.append(record.payload["payload"])
        return VectorEmbeddingSchema(vectors, documents, payloads)

    def upload(self, collection: AnyStr, space: AnyStr = DEFAULT_SPACE_NAME):
        try:
            return vector_db.insert(collection, space, self.vectors,
                                    self.documents, self.payloads)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to upload vectors: {str(e)}"
            )

    def search(
        self,
        collection: AnyStr,
        space: AnyStr = DEFAULT_SPACE_NAME,
        limit: int = DEFAULT_QUERY_LIMIT,
    ):
        try:
            return vector_db.search(collection, space, self.vectors, limit)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to search vectors: {str(e)}"
            )
