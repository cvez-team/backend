import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings


embedder = GoogleGenerativeAIEmbeddings(api_key=os.environ.get('GOOGLE_API_KEY'), model="models/embedding-001")

