# src/utils/config.py
import json
import os


class AppConfig:
    _instance = None
    DEFAULT_CONFIG = {
        "theme": "dark",
        "currency": "IDR",
        "date_format": "%Y-%m-%d",
        "font_size": "medium",
        "sidebar_width": 240,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        config_path = os.path.join("config", "settings.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.DEFAULT_CONFIG
                self.save_config()
        except Exception:
            self.settings = self.DEFAULT_CONFIG

    def save_config(self):
        config_path = os.path.join("config", "settings.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_config()
