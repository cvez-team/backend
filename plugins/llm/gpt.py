import os
from langchain_openai import ChatOpenAI


<<<<<<< HEAD
model = ChatOpenAI(api_key=os.environ.get('OPENAI_API_KEY'), temperature=0, request_timeout=200)
=======
model = ChatOpenAI(api_key=os.environ.get('OPENAI_API_KEY'), temperature=0, request_timeout=120)
>>>>>>> 5a768e8eab427d344af00c173fd762081f580cfc

