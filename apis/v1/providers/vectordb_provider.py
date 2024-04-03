from typing import AnyStr, Dict, Any, List, Union
import numpy.typing as npt
import uuid
from fastapi import HTTPException, status
from qdrant_client.http.models import (
    VectorParams,
    Distance,
    PointStruct,
    SearchRequest,
    Filter,
    FieldCondition,
    MatchValue,
    PointIdsList,
)
from ..configs.qdrant_config import client
from ..utils.constants import DEFAULT_EMBEDDING_DIM, DEFAULT_EMBEDDING_PROVIDER, DEFAULT_QUERY_LIMIT


class VectorDatabaseProvider:
    '''
    Vector Database Provider wrapper module.
    '''

    def __init__(self): ...

    def create_collection(
        self,
        collection_name: AnyStr,
        provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER,
        size: int = DEFAULT_EMBEDDING_DIM,
        distance: Distance = Distance.COSINE
    ):
        '''
        Create a new collection if it does not exist.
        '''
        # Get all collections in the database
        collections_name = [
            collection.name for collection in client.get_collections().collections]

        if collection_name not in collections_name:
            is_success = client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    f"{provider}": VectorParams(
                        size=size,
                        distance=distance
                    )
                }
            )
            if not is_success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to create collection: {collection_name}"
                )

    def delete_collection(self, collection_name: AnyStr):
        '''
        Delete the collection.
        '''
        is_success = client.delete_collection(collection_name=collection_name)
        if not is_success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to delete collection: {collection_name}"
            )

    def get_all(
        self,
        collection_name: AnyStr,
        space_name: AnyStr,
    ):
        '''
        Get all the points in the collection.
        '''
        # Get filter for space
        space_filter = Filter(
            must=[
                FieldCondition(
                    key="space",
                    match=MatchValue(
                        value=space_name
                    )
                )
            ]
        )
        # Search
        return client.scroll(
            collection_name=collection_name,
            scroll_filter=space_filter,
            with_payload=True,
            with_vectors=True,
            limit=999
        )[0]

    def search(
        self,
        collection_name: AnyStr,
        space_name: AnyStr,
        vectors: List[npt.NDArray],
        limit: int = DEFAULT_QUERY_LIMIT
    ):
        '''
        Search the collection for the nearest vectors to the array.
        Return a list of tuples containing the id, score and payload of point.
        '''
        # Get filter for space
        space_filter = Filter(
            must=[
                FieldCondition(
                    key="space",
                    match=MatchValue(
                        value=space_name
                    )
                )
            ]
        )
        # Build query requests
        queries = []
        for array in vectors:
            queries.append(
                SearchRequest(vector=array, limit=limit,
                              filter=space_filter, with_payload=True)
            )
        # Search
        return client.search_batch(
            collection_name=collection_name,
            requests=queries
        )

    def insert(
        self,
        collection_name: AnyStr,
        space_name: AnyStr,
        vectors: List[npt.NDArray],
        documents: List[AnyStr],
        payloads: List[Dict[str, Any]],
    ) -> List[AnyStr]:
        '''
        Insert data into the collection, and return the id.
        '''
        # Create ids
        ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
        # Create points
        vector_points = []
        for _id, vector, document, payload in zip(ids, vectors, documents, payloads):
            vector_points.append(
                PointStruct(
                    id=_id,
                    vector=vector,
                    payload={
                        "space": space_name,
                        "document": document,
                        "payload": payload
                    }
                )
            )
        # Insert data
        client.upsert(
            collection_name=collection_name,
            points=vector_points
        )
        return ids

    def delete(
        self,
        collection_name: AnyStr,
        ids: Union[List[AnyStr], AnyStr]
    ):
        '''
        Delete data from the collection by id.
        '''
        if isinstance(ids, list):
            point_ids = ids
        else:
            point_ids = [ids]

        client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(
                points=point_ids
            )
        )
