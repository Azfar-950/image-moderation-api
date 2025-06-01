from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    client = MongoClient(os.getenv("MONGODB_URI"))
    return client.get_database()

db = get_database()
tokens_collection = db["tokens"]
usages_collection = db["usages"]