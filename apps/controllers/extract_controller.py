from typing import Dict, List, Tuple, Any, Union
import numpy.typing as npt
from plugins.typing import LLMFmt
from plugins.llm import LLMGenerator
from plugins.word_embedding import WordEmbedding
from ..utils.utils import force_string


# Define the LLM generator and word embedding instances
generator = LLMGenerator()
embedder = WordEmbedding()


_ExtractControlReturnType = Tuple[Dict[str, Any],
                                  Dict[str, Union[List[npt.NDArray], npt.NDArray]]]


def extract_control(system_prompt: str, prompt: str, fmt: LLMFmt) -> _ExtractControlReturnType:
    '''
    Extract any string prompt to structured data and word embeddings.
    '''
    # Update format of generator
    generator.set_parser(fmt=fmt)

    # Extract the data by invoking the model
    extraction = generator.generate(system=system_prompt, prompt=prompt)

    # Generate word embeddings
    word_embeddings = {}
    for key, value in extraction.items():
        if isinstance(value, list):
            word_embeddings[key] = [
                embedder.embed(force_string(item)) for item in value]

        elif isinstance(value, dict):
            word_embeddings[key] = {
                k: embedder.embed(force_string(v)) for k, v in value.items()}

        elif isinstance(value, str):
            word_embeddings[key] = embedder.embed(value)

        else:
            continue

    return extraction, word_embeddings
