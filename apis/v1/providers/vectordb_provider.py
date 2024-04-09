from typing import AnyStr, Dict, Any, List, Union
import time
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
from ..utils.logger import log_qdrant


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
            _s = time.perf_counter()
            is_success = client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    f"{provider}": VectorParams(
                        size=size,
                        distance=distance
                    )
                }
            )
            _e = time.perf_counter() - _s

            if not is_success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to create collection: {collection_name}"
                )

            log_qdrant(f"Collection {collection_name} created. [{_e:.2f}s]")

    def delete_collection(self, collection_name: AnyStr):
        '''
        Delete the collection.
        '''
        _s = time.perf_counter()
        is_success = client.delete_collection(collection_name=collection_name)
        _e = time.perf_counter() - _s

        log_qdrant(f"Collection {collection_name} deleted. [{_e:.2f}s]")

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
        _s = time.perf_counter()
        searches = client.scroll(
            collection_name=collection_name,
            scroll_filter=space_filter,
            with_payload=True,
            with_vectors=True,
            limit=999
        )[0]
        _e = time.perf_counter() - _s

        log_qdrant(f"Collection {collection_name} read. [{_e:.2f}s]")

        return searches

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
        _s = time.perf_counter()
        seaches = client.search_batch(
            collection_name=collection_name,
            requests=queries
        )
        _e = time.perf_counter() - _s

        log_qdrant(f"Collection {collection_name} searched. [{_e:.2f}s]")

        return seaches

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

        _s = time.perf_counter()
        client.upsert(
            collection_name=collection_name,
            points=vector_points
        )
        _e = time.perf_counter() - _s

        log_qdrant(f"Collection {collection_name} inserted. [{_e:.2f}s]")

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

        _s = time.perf_counter()
        client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(
                points=point_ids
            )
        )
        _e = time.perf_counter() - _s

        log_qdrant(f"Collection {collection_name} deleted. [{_e:.2f}s]")

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

        _s = time.perf_counter()
        searches = client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=filter_conditions
            ),
            with_payload=True,
            with_vectors=True,
            limit=999
        )[0]
        _e = time.perf_counter() - _s

        log_qdrant(
            f"Collection {collection_name} dynamic searched. [{_e:.2f}s]")

        return searches
