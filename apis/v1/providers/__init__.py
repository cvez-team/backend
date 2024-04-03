from .cache_provider import CacheProvider
from .jwt_provider import JWTProvider
from .db_provider import DatabaseProvider
from .word_embedding_provider import WordEmbeddingProvider
from .vectordb_provider import VectorDatabaseProvider
from ..utils.constants import USER_COLLECTION, PROJECT_COLLECTION, POSITION_COLLECTION


cacher = CacheProvider()
memory_cacher = CacheProvider(in_memory=True)
jwt = JWTProvider()
user_db = DatabaseProvider(collection_name=USER_COLLECTION)
project_db = DatabaseProvider(collection_name=PROJECT_COLLECTION)
position_db = DatabaseProvider(collection_name=POSITION_COLLECTION)
embedder = WordEmbeddingProvider()
vector_db = VectorDatabaseProvider()
