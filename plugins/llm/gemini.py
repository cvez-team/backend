import os
from langchain_google_genai import ChatGoogleGenerativeAI

<<<<<<< HEAD
model = ChatGoogleGenerativeAI(api_key=os.environ.get('GOOGLE_API_KEY'), temperature=0, model="gemini-pro", request_timeout=200) 
=======
model = ChatGoogleGenerativeAI(api_key=os.environ.get('GOOGLE_API_KEY'), temperature=0, model="gemini-pro", request_timeout=120)
>>>>>>> 5a768e8eab427d344af00c173fd762081f580cfc
