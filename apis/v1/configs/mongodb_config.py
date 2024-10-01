import os
from pymongo import MongoClient


client = MongoClient(
    host=os.environ.get("MONGO_HOST", "localhost"),
    port=int(os.environ.get("MONGO_PORT", 27017)),
)

db = client[os.environ.get("MONGO_DB", "cvez")]
