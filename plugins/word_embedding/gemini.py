import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings


embedder = GoogleGenerativeAIEmbeddings(google_api_key=os.environ.get('GOOGLE_API_KEY'), model="models/embedding-001")