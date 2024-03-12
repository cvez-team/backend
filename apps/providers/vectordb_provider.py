from typing import Dict, Any, List, Tuple
import numpy.typing as npt
import uuid
from qdrant_client.http.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue, PointIdsList
from ..configs.qdrant_config import client


class VectorDatabaseProvider:
    '''
    Vector Database Provider wrapper module.
    '''

    def __init__(self, size: int, distance: Distance = Distance.COSINE) -> None:
        self.size = size
        self.distance = distance
        self.available_collections = self.__get_collection()

    def __get_collection(self):
        '''
        Get all available collections.
        '''
        collections = client.get_collections().collections
        return [collection.name for collection in collections]

    def __create_collection(self, collection_name: str):
        '''
        Create a new collection if it does not exist.
        '''
        if collection_name not in self.available_collections:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=self.size,
                    distance=self.distance
                )
            )
            # Append to available collections
            self.available_collections.append(collection_name)

    def get(self, collection_name: str, id: str) -> Tuple[Any, npt.NDArray]:
        '''
        Get the data from the collection by id.
        Return the payload and the vector.
        '''
        record = client.retrieve(
            collection_collection_name=collection_name,
            ids=[id],
            with_vectors=True,
            with_payload=True
        )[0]
        return record.payload, record.vector

    def search(self, collection_name: str, array: npt.NDArray, limit: int = 10) -> List[Tuple[str, float]]:
        '''
        Search the collection for the nearest vectors to the array.
        Return a list of tuples containing the id and score.
        '''
        # Search
        query_results = client.search(
            collection_name=collection_name,
            query_vector=array,
            limit=limit
        )
        # Get results
        results = []
        for result in query_results:
            results.append((result.id, result.score))
        return results

    def query(self, collection_name: str, key: str, value: str) -> List[Tuple[str, Any, npt.NDArray]]:
        '''
        Query the point that match the key with value in payload.
        Return a list of tuples containing the id, payload and vector.
        ''' 
        query_results = client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key=key,
                        condition=MatchValue(
                            value=value
                        )
                    )
                ]
            ),
            limit=100,
            with_payload=True,
            with_vectors=True
        )[0]
        # Get results
        results = []
        for result in query_results:
            results.append((result.id, result.payload, result.vector))
        return results

    def insert(self, collection_name: str, array: npt.NDArray, data: Dict[str, Any] = {}) -> str:
        '''
        Insert data into the collection, and return the id.
        '''
        # Create collection if not exists
        self.__create_collection(collection_name)
        # Generate id
        id = str(uuid.uuid4())
        # Insert data
        client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=id,
                    payload=data,
                    vector=array,
                )
            ]
        )
        return id

    def delete(self, collection_name: str, id: str):
        '''
        Delete data from the collection by id.
        '''
        client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(
                points=[id]
            )
        )
