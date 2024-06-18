import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDBClient(MongoClient):
    instance: MongoClient = None

    def __new__(cls) -> MongoClient:
        if not hasattr(cls, 'instance') or cls.instance is None:
            cls.instance = MongoClient(os.environ.get('MONGODB_URI'), server_api=ServerApi('1'))
        return cls.instance
