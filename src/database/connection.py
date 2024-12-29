from pymongo import MongoClient
from pymongo.collection import Collection
from src.config import Config
import certifi


class DatabaseConnection:
    _instance = None
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI, tlsCAFile=certifi.where())
        self.db = self._client[Config.DB_NAME]

    def get_collection(self, name: str) -> Collection:
        return self.db[name]

    def close(self):
        if self._client:
            self._client.close()
