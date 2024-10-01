from typing import AnyStr, Dict, Any, List, Union
import numpy.typing as npt
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
    NamedVector
)
from ..configs.qdrant_config import client
from ..utils.constants import DEFAULT_EMBEDDING_DIM, DEFAULT_EMBEDDING_PROVIDER, DEFAULT_QUERY_LIMIT
from ..utils.logger import logger_decorator


class VectorDatabaseProvider:
    '''
    Vector Database Provider wrapper module.
    '''

    def __init__(self): ...

    @logger_decorator(prefix="VECTOR_DATABASE")
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

    @logger_decorator(prefix="VECTOR_DATABASE")
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

    @logger_decorator(prefix="VECTOR_DATABASE")
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
        searches = client.scroll(
            collection_name=collection_name,
            scroll_filter=space_filter,
            with_payload=True,
            with_vectors=True,
            limit=999
        )[0]

        return searches

    @logger_decorator(prefix="VECTOR_DATABASE")
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
            # Define NamedVector
            vector = NamedVector.model_validate({
                "name": DEFAULT_EMBEDDING_PROVIDER,
                "vector": array
            })
            queries.append(
                SearchRequest(
                    vector=vector,
                    limit=limit,
                    filter=space_filter,
                    with_payload=True
                )
            )
        # Search
        seaches = client.search_batch(
            collection_name=collection_name,
            requests=queries
        )

        return seaches

    @logger_decorator(prefix="VECTOR_DATABASE")
    def insert(
        self,
        collection_name: AnyStr,
        space_name: AnyStr,
        ids: List[AnyStr],
        vectors: List[npt.NDArray],
        documents: List[AnyStr],
        payloads: List[Dict[str, Any]],
    ) -> None:
        '''
        Insert data into the collection, and return the id.
        '''
        # Create points
        vector_points = []
        for _id, vector, document, payload in zip(ids, vectors, documents, payloads):
            vector_points.append(
                PointStruct(
                    id=_id,
                    vector={
                        f"{DEFAULT_EMBEDDING_PROVIDER}": vector
                    },
                    payload={
                        "space": space_name,
                        "document": document,
                        "payload": payload
                    }
                )
            )
        # Insert data
        if len(vector_points) == 0:
            return

        client.upsert(
            collection_name=collection_name,
            points=vector_points
        )

    @logger_decorator(prefix="VECTOR_DATABASE")
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

    @logger_decorator(prefix="VECTOR_DATABASE")
    def dynamic_search(self, collection_name: AnyStr, key: AnyStr, value: AnyStr, space: AnyStr = None):
        '''
        Dynamic search by key and value.
        '''
        filter_conditions = [
            FieldCondition(
                key=f"payload.{key}",
                match=MatchValue(
                    value=value
                )
            )
        ]
        # Add space filter
        if space:
            filter_conditions.append(
                FieldCondition(
                    key="space",
                    match=MatchValue(
                        value=space
                    )
                )
            )

        searches = client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=filter_conditions
            ),
            with_payload=True,
            with_vectors=True,
            limit=999
        )[0]

        return searches
