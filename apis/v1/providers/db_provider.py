from typing import Any, AnyStr, Dict, List
from .cache_provider import CacheProvider
from ..configs.firebase_config import db


class DatabaseProvider:
    '''
    Provide methods interacting with Firestore database.
    '''

    def __init__(self, collection_name: AnyStr):
        self.collection_name = collection_name
        self.id_field = "id"
        self.collection = db.collection(collection_name)
        self.cacher = CacheProvider()

    def get_all(self) -> List[Dict[str, Any]]:
        '''
        Get all documents from the collection.
        Return a list of documents.
        '''
        docs = self.collection.stream()
        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)
            # Save to cache
            self.cacher.set(
                f"{self.collection_name}:{doc.id}", doc_dict)
        return doc_list

    def get_all_by_ids(self, ids: List[AnyStr]) -> List[Dict[str, Any]]:
        '''
        Get all documents by the list of document ids.
        Return a list of documents.
        '''
        # Get from cache
        doc_list = []
        cache_doc_ids = []
        for _id in ids:
            cache_doc = self.cacher.get(f"{self.collection_name}:{_id}")
            if cache_doc:
                doc_list.append(cache_doc)
                cache_doc_ids.append(_id)

        # Get from database documents not in cache
        doc_refs = [self.collection.document(
            _id) for _id in ids if _id not in cache_doc_ids]
        if len(doc_refs) != 0:
            docs = db.get_all(references=doc_refs)
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict[self.id_field] = doc.id
                doc_list.append(doc_dict)
                # Save to cache
                self.cacher.set(
                    f"{self.collection_name}:{doc.id}", doc_dict)

        return doc_list

    def get_by_id(self, doc_id: AnyStr) -> Dict[str, Any] | None:
        '''
        Get a document from the collection.
        Return the document if it exists, otherwise return None.
        '''
        # Get from cache
        doc = self.cacher.get(f"{self.collection_name}:{doc_id}")
        if not doc:
            doc = self.collection.document(doc_id).get()
            if doc.exists:
                doc_dict = doc.to_dict()
                doc_dict[self.id_field] = doc_id
                # Save to cache
                self.cacher.set(
                    f"{self.collection_name}:{doc_id}", doc_dict)

                return doc_dict
            else:
                return None
        return doc

    def query_equal(self, key: AnyStr, value: AnyStr) -> List[Dict[str, Any]]:
        '''
        Query the collection for documents where the key is equal to the value.
        Return a list of documents.
        '''
        docs = self.collection.where(key, "==", value).stream()
        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)
        return doc_list

    def create(self, data: Dict) -> AnyStr:
        '''
        Create a new document in the collection.
        Return the document id.
        '''
        doc_ref = self.collection.add(data)
        return doc_ref[1].id

    def update(self, doc_id: AnyStr, data: Dict) -> None:
        '''
        Update a document in the collection.
        '''
        # Update data in cache
        self.cacher.set(f"{self.collection_name}:{doc_id}", {
            **self.get_by_id(doc_id), **data
        })
        self.collection.document(doc_id).set(data, merge=True)

    def delete(self, doc_id: AnyStr) -> None:
        '''
        Delete a document from the collection.
        '''
        # Remove data in cache
        self.cacher.remove(f"{self.collection_name}:{doc_id}")
        self.collection.document(doc_id).delete()
