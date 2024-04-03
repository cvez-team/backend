from typing import AnyStr, List
from fastapi import HTTPException, status
from ..configs.word_embedding_config import mxbai_embedder
from ..utils.constants import DEFAULT_EMBEDDING_PROVIDER


class WordEmbeddingProvider:
    '''
    Provide common word embedding features.
    '''

    def __init__(self):
        self.providers = {
            "mxbai": (mxbai_embedder, 1024),
        }

    def embed(self, data: AnyStr | List[AnyStr], provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER) -> List[List[float]]:
        # Get embedding provider
        embedder = self.providers.get(
            provider, self.providers[DEFAULT_EMBEDDING_PROVIDER])[0]

        if isinstance(data, str):
            return [embedder.embed_query(data)]
        elif isinstance(data, list):
            return embedder.embed_documents(data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid data type for embedding. Got: {type(data)}"
            )

    def get_provider(self, provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER):
        if provider in self.providers.keys():
            return provider
        else:
            return DEFAULT_EMBEDDING_PROVIDER

    def get_size(self, provider: AnyStr = DEFAULT_EMBEDDING_PROVIDER) -> int:
        return self.providers.get(provider, self.providers[DEFAULT_EMBEDDING_PROVIDER])[1]
