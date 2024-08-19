from abc import abstractmethod
from typing import Any, AnyStr, Dict, List


class BaseDatabaseProvider:
    '''
    Provide methods interacting with Database.
    Args:
        collection_name: The name of the collection in the database.
        id_field: The name of the field that is used as the document id.
        collection: The reference to the collection in the database.

    Methods:
        get_all: Get all documents from the collection.
        get_all_by_ids: Get all documents by the list of document ids.
        get_by_id: Get a document from the collection.
        query_equal: Query the collection for documents where the key is equal to the value.
        query_similar: Query the collection for documents where the key is similar to the value.
        create: Create a new document in the collection.
        update: Update a document in the collection.
        delete: Delete a document from the collection.
    '''

    def __init__(self, collection_name: AnyStr):
        self.collection_name = collection_name

    def get_cache_field_by_id(self, doc_id: AnyStr) -> AnyStr:
        """
        Get cache field by document id. Format: {collection_name}:{doc_id}
        """
        return f"{self.collection_name}:{doc_id}"

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        '''
        Get all documents from the collection.
        Return a list of documents.
        '''
        raise NotImplementedError

    @abstractmethod
    def get_all_by_ids(self, ids: List[AnyStr]) -> List[Dict[str, Any]]:
        '''
        Get all documents by the list of document ids.
        Return a list of documents.
        '''
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, doc_id: AnyStr) -> Dict[str, Any] | None:
        '''
        Get a document from the collection.
        Return the document if it exists, otherwise return None.
        '''
        raise NotImplementedError

    @abstractmethod
    def query_equal(self, key: AnyStr, value: AnyStr) -> List[Dict[str, Any]]:
        '''
        Query the collection for documents where the key is equal to the value.
        Return a list of documents.
        '''
        raise NotImplementedError

    @abstractmethod
    def query_similar(self, key: AnyStr, value: AnyStr) -> List[Dict[str, Any]]:
        '''
        Query the collection for documents where the key is similar to the value.
        Return a list of documents.
        '''
        raise NotImplementedError

    @abstractmethod
    def create(self, data: Dict) -> AnyStr:
        '''
        Create a new document in the collection.
        Return the document id.
        '''
        raise NotImplementedError

    @abstractmethod
    def update(self, doc_id: AnyStr, data: Dict, merge: bool) -> None:
        '''
        Update a document in the collection.
        '''
        raise NotImplementedError

    @abstractmethod
    def delete(self, doc_id: AnyStr) -> None:
        '''
        Delete a document from the collection.
        '''
        raise NotImplementedError
