import os
from datetime import datetime
from src.config import Config


class Logger:
    def __init__(self):
        if not os.path.exists(Config.LOG_DIR):
            os.makedirs(Config.LOG_DIR)

    def log_action(self, action: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = os.path.join(
            Config.LOG_DIR, f"inventory_{datetime.now().strftime('%Y%m%d')}.log"
        )
        log_entry = f"[{timestamp}] {action}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
