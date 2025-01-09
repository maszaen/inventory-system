import os
import atexit
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from utils.manifest_handler import ManifestHandler


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    APP_TITLE = "PyStockFlow"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    APP_VERSION = "5.0"

    manifest = ManifestHandler(BASE_DIR)
    ENV_FILE_ENC = manifest.get_env_path()
    ENCRYPTION_KEY_PATH = manifest.get_key_path()

    TEMP_DIR = os.path.join(os.path.dirname(ENCRYPTION_KEY_PATH), "temp")
    UNIQUE_ID = "209ixx7"
    TEMP_ENV_FILE = os.path.join(TEMP_DIR, UNIQUE_ID, f"{UNIQUE_ID}.temp")

    LOG_DIR = os.path.join(os.path.dirname(ENV_FILE_ENC), "logs")
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")

    @classmethod
    def load_env(cls):
        """Load environment variables from the temporary decrypted ENV_FILE."""
        if not os.path.exists(cls.ENV_FILE_ENC):
            print(
                f"Encrypted .env file not found at {cls.ENV_FILE_ENC}. Initializing default .env."
            )
            cls._initialize_default_env()

        cls.decrypt_env_file()
        load_dotenv(cls.TEMP_ENV_FILE)

        cls.MONGODB_URI = os.getenv("MONGODB_URI", "")
        cls.DB_NAME = os.getenv("DB_NAME", "PyStockFlow")
        cls.CONNECTION_STRING = (
            os.getenv("CONNECTION_STRING", "false").lower() == "true"
        )

    @classmethod
    def _initialize_default_env(cls):
        if not os.path.exists(cls.ENCRYPTION_KEY_PATH):
            cls.generate_encryption_key()

        default_env = """MONGODB_URI=
        DB_NAME=PyStockFlow
        CONNECTION_STRING=false
        """
        cls._ensure_temp_dir()
        with open(cls.TEMP_ENV_FILE, "w") as f:
            f.write(default_env)

        cls.encrypt_env_file()

    @classmethod
    def decrypt_env_file(cls):
        try:
            with open(cls.ENCRYPTION_KEY_PATH, "rb") as key_file:
                encryption_key = key_file.read()

            fernet = Fernet(encryption_key)

            with open(cls.ENV_FILE_ENC, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            cls._ensure_temp_dir()
            with open(cls.TEMP_ENV_FILE, "wb") as file:
                file.write(decrypted_data)

            print("Decryption successful. Temporary .env file created.")
        except InvalidToken:
            print("Invalid encryption token. Unable to decrypt the .env file.")
            raise
        except Exception as e:
            print(f"Unexpected error during decryption: {str(e)}")
            raise

    @classmethod
    def encrypt_env_file(cls):
        try:
            with open(cls.TEMP_ENV_FILE, "rb") as file:
                plain_data = file.read()

            with open(cls.ENCRYPTION_KEY_PATH, "rb") as key_file:
                encryption_key = key_file.read()

            fernet = Fernet(encryption_key)
            encrypted_data = fernet.encrypt(plain_data)

            with open(cls.ENV_FILE_ENC, "wb") as file:
                file.write(encrypted_data)

            print("Encryption successful.")
        except Exception as e:
            print(f"Error encrypting .env file: {str(e)}")
            raise

    @classmethod
    def generate_encryption_key(cls):
        if not os.path.exists(cls.ENCRYPTION_KEY_PATH):
            try:
                os.makedirs(os.path.dirname(cls.ENCRYPTION_KEY_PATH), exist_ok=True)
                encryption_key = Fernet.generate_key()
                with open(cls.ENCRYPTION_KEY_PATH, "wb") as key_file:
                    key_file.write(encryption_key)
                print(
                    f"Encryption key generated and saved to {cls.ENCRYPTION_KEY_PATH}"
                )
            except Exception as e:
                print(f"Error generating encryption key: {str(e)}")
                raise

    @classmethod
    def save_config(cls, mongodb_uri: str, db_name: str):
        """Save configuration to the current environment file."""
        try:
            cls._ensure_temp_dir()
            with open(cls.TEMP_ENV_FILE, "w") as f:
                f.write(f"MONGODB_URI={mongodb_uri}\n")
                f.write(f"DB_NAME={db_name}\n")
                f.write("CONNECTION_STRING=true\n")

            os.environ["MONGODB_URI"] = mongodb_uri
            os.environ["DB_NAME"] = db_name
            os.environ["CONNECTION_STRING"] = "true"

            cls.encrypt_env_file()
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            raise

    @classmethod
    def _ensure_temp_dir(cls):
        temp_dir_path = os.path.join(cls.TEMP_DIR, cls.UNIQUE_ID)
        os.makedirs(temp_dir_path, exist_ok=True)

    @classmethod
    def cleanup(cls):
        if os.path.exists(cls.TEMP_ENV_FILE):
            os.remove(cls.TEMP_ENV_FILE)
            print("Temporary .env file deleted.")


atexit.register(Config.cleanup)

Config.load_env()
