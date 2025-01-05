import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    ENV_FILE = os.path.join(BASE_DIR, ".env")

    APP_TITLE = "PyStockFlow"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    APP_VERSION = "5.0"

    load_dotenv(ENV_FILE)

    MONGODB_URI = os.getenv("MONGODB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "PyStockFlow")
    CONNECTION_STRING = os.getenv("CONNECTION_STRING", "false").lower() == "true"

    @classmethod
    def load_env(cls):
        """Load or create .env file and environment variables."""
        if not os.path.exists(cls.ENV_FILE):
            with open(cls.ENV_FILE, "w") as f:
                f.write("MONGODB_URI=\n")
                f.write("DB_NAME=\n")
                f.write("CONNECTION_STRING=false\n")
        load_dotenv(cls.ENV_FILE)
        cls.MONGODB_URI = os.getenv("MONGODB_URI", "")
        cls.DB_NAME = os.getenv("DB_NAME", "PyStockFlow")
        cls.CONNECTION_STRING = (
            os.getenv("CONNECTION_STRING", "false").lower() == "true"
        )

    @classmethod
    def save_config(cls, mongodb_uri: str, db_name: str):
        """Save configuration to .env file."""
        try:
            with open(cls.ENV_FILE, "w") as f:
                f.write(f"MONGODB_URI={mongodb_uri}\n")
                f.write(f"DB_NAME={db_name}\n")
                f.write("CONNECTION_STRING=true\n")

            os.environ["MONGODB_URI"] = mongodb_uri
            os.environ["DB_NAME"] = db_name
            os.environ["CONNECTION_STRING"] = "true"

            cls.MONGODB_URI = mongodb_uri
            cls.DB_NAME = db_name
            cls.CONNECTION_STRING = True
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            raise


Config.load_env()
