from typing import Any, AnyStr, Dict, List
import time
from firebase_admin import firestore
from ._cache_init import cacher
from ..configs.firebase_config import db
from ..utils.logger import log_firebase


class DatabaseProvider:
    '''
    Provide methods interacting with Firestore database.
    '''

    def __init__(self, collection_name: AnyStr):
        self.collection_name = collection_name
        self.id_field = "id"
        self.collection = db.collection(collection_name)
        self.cacher = cacher

    def get_all(self) -> List[Dict[str, Any]]:
        '''
        Get all documents from the collection.
        Return a list of documents.
        '''
        _s = time.perf_counter()
        docs = self.collection.stream()
        _e = time.perf_counter() - _s

        doc_list = []
        for doc in docs:
            log_firebase(f"Database read to {doc.id} [{_e:.2f}s]")

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
            _s = time.perf_counter()
            docs = db.get_all(references=doc_refs)
            _e = time.perf_counter() - _s

            for doc in docs:
                log_firebase(f"Database read to {doc.id} [{_e:.2f}s]")

                doc_dict = doc.to_dict()
                if not doc_dict:
                    continue

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
            _s = time.perf_counter()
            doc = self.collection.document(doc_id).get()
            _e = time.perf_counter() - _s

            log_firebase(f"Database read to {doc_id} [{_e:.2f}s]")

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
        _s = time.perf_counter()
        docs = self.collection.where(filter=firestore.firestore.FieldFilter(
            key, "==", value)).stream()
        _e = time.perf_counter() - _s

        doc_list = []
        for doc in docs:
            log_firebase(f"Database read to {doc.id} [{_e:.2f}s]")

            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)
        return doc_list

    def query_similar(self, key: AnyStr, value: AnyStr) -> List[Dict[str, Any]]:
        '''
        Query the collection for documents where the key is similar to the value.
        Return a list of documents.
        '''
        _s = time.perf_counter()
        docs = self.collection.where(filter=firestore.firestore.FieldFilter(
            key, ">=", value)).where(filter=firestore.firestore.FieldFilter(key, "<=", value + "\uf8ff")).stream()
        _e = time.perf_counter() - _s

        doc_list = []
        for doc in docs:
            log_firebase(f"Database read to {doc.id} [{_e:.2f}s]")

            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)
        return doc_list

    def create(self, data: Dict) -> AnyStr:
        '''
        Create a new document in the collection.
        Return the document id.
        '''
        _s = time.perf_counter()
        doc_ref = self.collection.add(data)
        _e = time.perf_counter() - _s

        log_firebase(f"Database created {doc_ref[1].id} [{_e:.2f}s]")
        return doc_ref[1].id

    def update(self, doc_id: AnyStr, data: Dict) -> None:
        '''
        Update a document in the collection.
        '''
        # Update data in cache
        self.cacher.set(f"{self.collection_name}:{doc_id}", {
            **self.get_by_id(doc_id), **data
        })

        _s = time.perf_counter()
        self.collection.document(doc_id).set(data, merge=True)
        _e = time.perf_counter() - _s

        log_firebase(f"Database updated {doc_id} [{_e:.2f}s]")

    def delete(self, doc_id: AnyStr) -> None:
        '''
        Delete a document from the collection.
        '''
        # Remove data in cache
        self.cacher.remove(f"{self.collection_name}:{doc_id}")

        _s = time.perf_counter()
        self.collection.document(doc_id).delete()
        _e = time.perf_counter() - _s

        log_firebase(f"Database deleted {doc_id} [{_e:.2f}s]")
