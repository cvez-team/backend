from langchain_community.embeddings import HuggingFaceEmbeddings

embedder = HuggingFaceEmbeddings(model_name="mixedbread-ai/mxbai-embed-large-v1")