import json
import os


class ManifestHandler:
    def __init__(self, base_dir):
        self.base_dir = base_dir

        # Default paths in Program Files
        program_files = os.path.join("C:", os.sep, "Program Files")
        app_dir = os.path.join(program_files, "PyStockFlow")
        env_dir = os.path.join(app_dir, "env")

        if not self._ensure_directory_accessible(app_dir):
            app_dir = os.path.join(os.getenv("LOCALAPPDATA"), "PyStockFlow")
            env_dir = os.path.join(app_dir, "env")
            os.makedirs(env_dir, exist_ok=True)

        self.manifest_path = os.path.join(app_dir, "manifest.json")
        self.default_env_path = os.path.join(env_dir, ".env")
        self._load_manifest()

    def _ensure_directory_accessible(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            if os.access(directory, os.W_OK):
                return True
        except (PermissionError, OSError):
            pass
        return False

    def _load_manifest(self):
        """Load or create manifest file"""
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, "r") as f:
                    self.manifest = json.load(f)
            except:
                self.manifest = self._create_default_manifest()
        else:
            self.manifest = self._create_default_manifest()
            self._save_manifest()

    def _create_default_manifest(self):
        """Create default manifest structure"""
        return {"env_path": self.default_env_path, "last_used_env_path": None}

    def _save_manifest(self):
        """Save current manifest to file"""
        try:
            with open(self.manifest_path, "w") as f:
                json.dump(self.manifest, f, indent=4)
        except Exception as e:
            print(f"Error saving manifest: {str(e)}")

    def get_env_path(self):
        """Get current environment file path"""
        return self.manifest.get("env_path", self.default_env_path)

    def set_env_path(self, path):
        """Set new environment file path"""
        if path and os.path.exists(os.path.dirname(path)):
            self.manifest["env_path"] = path
            self.manifest["last_used_env_path"] = path
            self._save_manifest()
            return True
        return False

    def get_key_path(self):
        """Get the path for the encryption key based on the env path"""
        env_dir = os.path.dirname(self.get_env_path())
        key_dir = os.path.join(env_dir, "key", "cryptography")
        os.makedirs(key_dir, exist_ok=True)
        return os.path.join(key_dir, "209feg98xx.key")

    def reset_to_default(self):
        """Reset environment path to default"""
        self.manifest["env_path"] = self.default_env_path
        self._save_manifest()

    def get_last_used_path(self):
        """Get last successfully used env path"""
        return self.manifest.get("last_used_env_path", self.default_env_path)
