import numpy as np
import numpy.typing as npt
# Import embedder
from .spacy import embedder as spacy_embedder
from .openai import embedder as openai_embedder
# from .gemini import embedder as gemini_embedder


class WordEmbedding:
    '''
    Word Embedding wrapper module.
    '''

    def __init__(self, dtype: npt.DTypeLike = np.float32):
        self.embedder = openai_embedder
        self.dtype = dtype

    def embed(self, data: str) -> npt.NDArray:
        array = self.embedder.embed_query(data)

        # Convert to numpy
        return np.array(array).astype(self.dtype)
