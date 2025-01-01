import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_TITLE = "Inventory System"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "InventoryDB")
    APP_VERSION = "5.0"
