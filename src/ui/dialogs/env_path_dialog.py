import os

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFileDialog,
)
from src.style_config import Theme
from src.config import Config
from src.utils.manifest_handler import ManifestHandler
from cryptography.fernet import Fernet


class EnvironmentPathDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Environment File Settings")
        self.setModal(True)
        self.setFixedSize(500, 150)
        self.setup_ui()

    def setup_ui(self):
        btn = Theme.btn()
        stroke_btn = Theme.border_btn_sec()
        form = Theme.form()
        layout = QVBoxLayout(self)

        # Current path display
        current_label = QLabel("Current Environment Path:")
        self.current_path = QLabel(Config.ENV_FILE_ENC)
        self.current_path.setStyleSheet("color: gray;")

        # New path input
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setStyleSheet(form)
        self.path_input.setPlaceholderText("Select new environment file path...")

        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet(stroke_btn)
        browse_btn.clicked.connect(self.browse_path)

        reset_btn = QPushButton("Reset to Default")
        reset_btn.setStyleSheet(stroke_btn)
        reset_btn.clicked.connect(self.reset_to_default)

        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        path_layout.addWidget(reset_btn)

        # Buttons
        button_layout = QHBoxLayout()

        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet(btn)
        save_btn.clicked.connect(self.save_changes)

        button_layout.addWidget(save_btn)

        # Add all widgets to main layout
        layout.addWidget(current_label)
        layout.addWidget(self.current_path)
        layout.addLayout(path_layout)
        layout.addLayout(button_layout)

    def browse_path(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Environment Folder", Config.manifest.get_last_used_path()
        )

        if folder_path:
            env_path = os.path.join(folder_path, ".env")
            self.path_input.setText(env_path)

    def save_changes(self):
        manifest = ManifestHandler(Config.BASE_DIR)
        new_folder = self.path_input.text().strip()

        if not new_folder:
            QMessageBox.warning(self, "Error", "Please select a folder")
            return

        try:
            os.makedirs(new_folder, exist_ok=True)

            if not os.access(new_folder, os.W_OK):
                raise PermissionError("No write permission for selected folder")

            new_env_path = os.path.join(new_folder, ".env")
            new_logs_dir = os.path.join(new_folder, "logs")

            old_env_path = Config.ENV_FILE_ENC
            if os.path.exists(old_env_path):
                os.remove(old_env_path)

            old_logs_dir = os.path.join(os.path.dirname(old_env_path), "logs")
            if os.path.exists(old_logs_dir):
                import shutil

                shutil.rmtree(old_logs_dir)

            os.makedirs(new_logs_dir, exist_ok=True)

            with open(Config.TEMP_ENV_FILE, "rb") as src:
                plain_data = src.read()

            with open(Config.ENCRYPTION_KEY_PATH, "rb") as key_file:
                encryption_key = key_file.read()
            fernet = Fernet(encryption_key)

            encrypted_data = fernet.encrypt(plain_data)
            with open(new_env_path, "wb") as dst:
                dst.write(encrypted_data)

            if manifest.set_env_path(new_env_path):
                QMessageBox.information(
                    self,
                    "Success",
                    "Environment path updated successfully.\nApplication will now restart.",
                )
                self.parent().close()
            else:
                raise Exception("Invalid path selected")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to update environment path: {str(e)}"
            )

    def reset_to_default(self):
        reply = QMessageBox.question(
            self,
            "Reset Environment Path",
            "Are you sure you want to reset to the default environment path?\nThis will require an application restart.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            Config.manifest.reset_to_default()
            Config.ENV_FILE_ENC = Config.manifest.get_env_path()
            Config.load_env()

            QMessageBox.information(
                self,
                "Success",
                "Environment path reset to default.\nApplication will now restart.",
            )
            self.parent().close()
