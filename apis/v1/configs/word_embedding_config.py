from langchain_community.embeddings import HuggingFaceEmbeddings


mxbai_embedder = HuggingFaceEmbeddings(
    model_name="mixedbread-ai/mxbai-embed-large-v1")
