from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.mongodb_url)
db = client.clinical_records

def get_mongo_db():
    return db
