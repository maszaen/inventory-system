import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_TITLE = "Inventory System"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    MONGODB_URI = os.getenv("MONGODB_URI", "")
    if not MONGODB_URI:
        load_dotenv()
        MONGODB_URI = os.getenv("MONGODB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "PyStockFlow")
    APP_VERSION = "5.0"

    @classmethod
    def save_config(cls, mongodb_uri: str, db_name: str):
        cls.MONGODB_URI = mongodb_uri
        cls.DB_NAME = db_name


class EnvConfig:
    MONGODB_URI = os.getenv("MONGODB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "PyStockFlow")
    CONNECTION_STRING = os.getenv("CONNECTION_STRING", "false").lower() == "true"

    @classmethod
    def save_config(cls, mongodb_uri: str, db_name: str):
        with open(".env", "w") as f:
            f.write(f"MONGODB_URI={mongodb_uri}\n")
            f.write(f"DB_NAME={db_name}\n")
            f.write("CONNECTION_STRING=true\n")

        cls.MONGODB_URI = mongodb_uri
        cls.DB_NAME = db_name
        cls.CONNECTION_STRING = True
