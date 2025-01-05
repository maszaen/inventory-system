from pymongo import MongoClient
from pymongo.collection import Collection
from src.config import Config
import certifi


class DatabaseConnection:
    _instance = None
    _client = None

    @classmethod
    def get_instance(cls):
        """Singleton pattern to get a single instance of the database connection."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the database connection."""
        self._refresh_env()
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI, tlsCAFile=certifi.where())
        self.db = self._client[Config.DB_NAME]

    @staticmethod
    def _refresh_env():
        """Reload environment variables from the .env file."""
        Config.load_env()

    def get_collection(self, name: str) -> Collection:
        """Get a MongoDB collection by name."""
        self._refresh_env()  # Refresh env before accessing the collection
        self.db = self._client[Config.DB_NAME]  # Update database if DB_NAME changes
        return self.db[name]

    def close(self):
        """Close the database connection."""
        if self._client:
            self._client.close()
            self._client = None
