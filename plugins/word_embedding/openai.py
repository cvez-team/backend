import os
from langchain_openai import OpenAIEmbeddings


embedder = OpenAIEmbeddings(api_key=os.environ.get('OPENAI_API_KEY'))
