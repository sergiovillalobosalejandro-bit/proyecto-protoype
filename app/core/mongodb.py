from pymongo import MongoClient
from typing import Generator
from .config import settings

client = MongoClient(settings.mongodb_url)
db = client.clinical_records

def get_mongo_db() -> Generator:
    """Dependency for MongoDB database"""
    try:
        yield db
    finally:
        pass  # MongoDB handles connection pooling
