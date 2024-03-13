import os
from langchain_openai import ChatOpenAI


model = ChatOpenAI(api_key=os.environ.get('OPENAI_API_KEY'), temperature=0, request_timeout=120)

