from typing import AnyStr
from typing_extensions import override
from firebase_admin import firestore
from .base_provider import BaseDatabaseProvider
from ..cache_provider import cacher
from ...configs.firebase_config import db
from ...utils.logger import logger_decorator


class FirebaseDatabaseProvider(BaseDatabaseProvider):
    def __init__(self, collection_name: AnyStr):
        super().__init__(collection_name)
        self.id_field = "id"
        self.collection = db.collection(collection_name)

    @override
    @logger_decorator(prefix="DATABASE")
    def get_all(self):
        docs = self.collection.stream()

        doc_map = {}
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_map[f"{self.collection_name}:{doc.id}"] = doc_dict

        # Save to cache
        cacher.sets(doc_map)

        return list(doc_map.values())

    @override
    @logger_decorator(prefix="DATABASE")
    def get_all_by_ids(self, ids):
        # Get from cache
        cached_docs = cacher.gets(
            [f"{self.collection_name}:{_id}" for _id in ids])
        miss_cached_doc_ids = [i for i in range(
            len(cached_docs)) if not cached_docs[i]]

        # Fetch documents not in cache
        doc_refs = [self.collection.document(
            ids[i]) for i in miss_cached_doc_ids]

        if len(doc_refs) != 0:
            docs = db.get_all(references=doc_refs)

            for doc, i in zip(docs, miss_cached_doc_ids):
                doc_dict = doc.to_dict()
                doc_dict[self.id_field] = doc.id
                cached_docs[i] = doc_dict

                # Save to cache
                cacher.set(f"{self.collection_name}:{doc.id}", doc_dict)

        return cached_docs

    @override
    @logger_decorator(prefix="DATABASE")
    def get_by_id(self, doc_id):
        if doc_id is None or doc_id == "":
            return None

        # Get from cache
        doc = cacher.get(f"{self.collection_name}:{doc_id}")

        if not doc:
            query_doc = self.collection.document(doc_id).get()

            if query_doc.exists:
                doc = query_doc.to_dict()
                doc[self.id_field] = doc_id

                # Save to cache
                cacher.set(f"{self.collection_name}:{doc_id}", doc)

        return doc

    @override
    @logger_decorator(prefix="DATABASE")
    def query_equal(self, key, value):
        docs = self.collection.where(filter=firestore.firestore.FieldFilter(
            key, "==", value)).stream()

        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)

        return doc_list

    @override
    @logger_decorator(prefix="DATABASE")
    def query_similar(self, key, value):
        docs = self.collection.where(filter=firestore.firestore.FieldFilter(
            key, ">=", value)).where(filter=firestore.firestore.FieldFilter(key, "<=", value + "\uf8ff")).stream()

        doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict[self.id_field] = doc.id
            doc_list.append(doc_dict)

        return doc_list

    @override
    @logger_decorator(prefix="DATABASE")
    def create(self, data):
        doc_ref = self.collection.add(data)

        # Save to cache
        cacher.set(f"{self.collection_name}:{doc_ref[1].id}", {
            **data, self.id_field: doc_ref[1].id})

        return doc_ref[1].id

    @override
    @logger_decorator(prefix="DATABASE")
    def update(self, doc_id, data, merge=True):
        # Update data in cache
        cacher.set(f"{self.collection_name}:{doc_id}", {
            **(self.get_by_id(doc_id) if merge else {}), **data
        }, merge=merge)

        self.collection.document(doc_id).set(data, merge=merge)

    @override
    @logger_decorator(prefix="DATABASE")
    def delete(self, doc_id):
        # Remove data in cache
        cacher.delete(f"{self.collection_name}:{doc_id}")

        self.collection.document(doc_id).delete()
