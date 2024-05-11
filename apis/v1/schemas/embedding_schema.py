from typing import List, AnyStr, Dict
import uuid
import numpy as np
from fastapi import HTTPException, status
from ..providers import embedder, vector_db
from ..utils.constants import DEFAULT_EMBEDDING_PROVIDER, DEFAULT_QUERY_LIMIT, DEFAULT_SPACE_NAME


class VectorEmbeddingSchema:
    def __init__(
        self,
        ids: List[AnyStr],
        vectors: List[List[float]],
        documents: List[AnyStr],
        payloads: List[Dict],
        provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER,
    ):
        self.ids = ids
        self.vectors = [np.array(vector) for vector in vectors]
        self.documents = documents
        self.payloads = payloads
        self.provider = provider

    def __iter__(self):
        return zip(self.ids, self.vectors, self.documents, self.payloads)

    @staticmethod
    def from_documents(documents: List[AnyStr], payloads: List[Dict], provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER):
        vectors = embedder.embed(documents, provider)
        # Create ids
        ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
        return VectorEmbeddingSchema(ids, vectors, documents, payloads, provider)

    @staticmethod
    def from_database(collection: AnyStr, space: AnyStr = DEFAULT_SPACE_NAME, provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER):
        records = vector_db.get_all(collection, space)
        ids = []
        vectors = []
        documents = []
        payloads = []
        for record in records:
            ids.append(record.id)
            vectors.append(record.vector[provider])
            documents.append(record.payload["document"])
            payloads.append(record.payload["payload"])
        return VectorEmbeddingSchema(ids, vectors, documents, payloads)

    @staticmethod
    def from_query(collection: AnyStr, key: AnyStr, value: AnyStr, space: AnyStr = None, provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER):
        records = vector_db.dynamic_search(collection, key, value, space)
        ids = []
        vectors = []
        documents = []
        payloads = []
        for record in records:
            ids.append(record.id)
            vectors.append(record.vector[provider])
            documents.append(record.payload["document"])
            payloads.append(record.payload["payload"])
        return VectorEmbeddingSchema(ids, vectors, documents, payloads)

    def upload(self, collection: AnyStr, space: AnyStr = DEFAULT_SPACE_NAME):
        try:
            vector_db.insert(collection, space, self.ids, self.vectors,
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

    def delete(self, collection: AnyStr):
        try:
            vector_db.delete(collection, self.ids)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to delete vectors: {str(e)}"
            )
