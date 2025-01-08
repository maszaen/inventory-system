import os
from dotenv import load_dotenv
from utils.manifest_handler import ManifestHandler


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    APP_TITLE = "PyStockFlow"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    APP_VERSION = "5.0"

    manifest = ManifestHandler(BASE_DIR)
    ENV_FILE = manifest.get_env_path()

    LOG_DIR = os.path.join(os.path.dirname(ENV_FILE), "logs")

    load_dotenv(ENV_FILE)

    MONGODB_URI = os.getenv("MONGODB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "PyStockFlow")
    CONNECTION_STRING = os.getenv("CONNECTION_STRING", "false").lower() == "true"

    @classmethod
    def set_env_path(cls, path):
        """Set new environment file path"""
        if cls.manifest.set_env_path(path):
            cls.ENV_FILE = path
            cls.LOG_DIR = os.path.join(os.path.dirname(path), "logs")
            cls.load_env()
            return True
        return False

    @classmethod
    def load_env(cls):
        """Load environment variables from current ENV_FILE"""
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
    def remove_env(cls):
        """Remove current environment file and reset to default"""
        try:
            if os.path.exists(cls.ENV_FILE):
                os.remove(cls.ENV_FILE)

            cls.manifest.reset_to_default()
            cls.ENV_FILE = cls.manifest.get_env_path()
            cls.LOG_DIR = os.path.join(os.path.dirname(cls.ENV_FILE), "logs")

            cls.MONGODB_URI = ""
            cls.DB_NAME = "PyStockFlow"
            cls.CONNECTION_STRING = False
            os._exit(0)
        except Exception as e:
            print(f"Error removing config: {str(e)}")
            raise

    @classmethod
    def save_config(cls, mongodb_uri: str, db_name: str):
        """Save configuration to current environment file."""
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
