from typing_extensions import override
from bson import ObjectId
from .base_provider import BaseDatabaseProvider
from ..cache_provider import cacher
from ...configs.mongodb_config import db
from ...utils.logger import logger_decorator


class MongodbDatabaseProvider(BaseDatabaseProvider):
    def __init__(self, collection_name: str):
        super().__init__(collection_name)
        self.id_field = "_id"
        self.collection = db[collection_name]

    @override
    @logger_decorator(prefix="DATABASE")
    def get_all(self):
        docs = self.collection.find()

        doc_map = {}
        for doc in docs:
            # Convert ObjectId to string
            if doc and isinstance(doc[self.id_field], ObjectId):
                doc[self.id_field] = str(doc[self.id_field])

            doc_map[f"{self.collection_name}:{doc[self.id_field]}"] = doc

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
        docs = self.collection.find({"_id": {"$in": miss_cached_doc_ids}})

        for doc in docs:
            # Convert ObjectId to string
            if doc and isinstance(doc[self.id_field], ObjectId):
                doc[self.id_field] = str(doc[self.id_field])

            cached_docs.append(doc)
            # Save to cache
            cacher.set(f"{self.collection_name}:{doc[self.id_field]}", doc)

        return cached_docs

    @override
    @logger_decorator(prefix="DATABASE")
    def get_by_id(self, doc_id):
        # Get from cache
        doc = cacher.get(f"{self.collection_name}:{doc_id}")

        if not doc:
            doc = self.collection.find_one({self.id_field: doc_id})

            # Convert ObjectId to string
            if doc and isinstance(doc[self.id_field], ObjectId):
                doc[self.id_field] = str(doc[self.id_field])

            # Save to cache
            cacher.set(f"{self.collection_name}:{doc_id}", doc)

        return doc

    @override
    @logger_decorator(prefix="DATABASE")
    def query_equal(self, field, value):
        docs = self.collection.find({field: value})

        doc_map = {}
        for doc in docs:
            # Convert ObjectId to string
            if doc and isinstance(doc[self.id_field], ObjectId):
                doc[self.id_field] = str(doc[self.id_field])

            doc_map[f"{self.collection_name}:{doc[self.id_field]}"] = doc

        # Save to cache
        cacher.sets(doc_map)

        return list(doc_map.values())

    @override
    @logger_decorator(prefix="DATABASE")
    def query_similar(self, field, value):
        docs = self.collection.find(
            {field: {"$regex": value, "$options": "i"}})

        doc_map = {}
        for doc in docs:
            # Convert ObjectId to string
            if doc and isinstance(doc[self.id_field], ObjectId):
                doc[self.id_field] = str(doc[self.id_field])

            doc_map[f"{self.collection_name}:{doc[self.id_field]}"] = doc

        # Save to cache
        cacher.sets(doc_map)

        return list(doc_map.values())

    @override
    @logger_decorator(prefix="DATABASE")
    def create(self, doc):
        doc_id = self.collection.insert_one(doc).inserted_id
        doc[self.id_field] = str(doc_id)
        return doc

    @override
    @logger_decorator(prefix="DATABASE")
    def update(self, doc_id, doc):
        self.collection.update_one({"_id": doc_id}, {"$set": doc})
        doc[self.id_field] = doc_id
        return doc

    @override
    @logger_decorator(prefix="DATABASE")
    def delete(self, doc_id):
        self.collection.delete_one({"_id": doc_id})
        return doc_id
