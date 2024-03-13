import os
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(api_key=os.environ.get('GOOGLE_API_KEY'), temperature=0, model="gemini-pro", request_timeout=120)
