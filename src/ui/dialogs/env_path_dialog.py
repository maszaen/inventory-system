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
        self.current_path = QLabel(Config.ENV_FILE)
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
        """Open file dialog to select environment file"""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Select Environment File",
            Config.manifest.get_last_used_path(),
            "Environment Files (*.env);;All Files (*.*)",
        )

        if file_name:
            self.path_input.setText(file_name)

    def save_changes(self):
        """Save new environment file path"""
        new_path = self.path_input.text().strip()

        if not new_path:
            QMessageBox.warning(self, "Error", "Please select a path")
            return

        try:
            if Config.set_env_path(new_path):
                QMessageBox.information(
                    self,
                    "Success",
                    "Environment path updated successfully.\nApplication will now restart.",
                )
                self.parent().close()  # This will trigger application restart
            else:
                raise Exception("Invalid path selected")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to update environment path: {str(e)}"
            )

    def reset_to_default(self):
        """Reset to default environment path"""
        reply = QMessageBox.question(
            self,
            "Reset Environment Path",
            "Are you sure you want to reset to the default environment path?\nThis will require an application restart.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            Config.manifest.reset_to_default()
            Config.ENV_FILE = Config.manifest.get_env_path()
            Config.load_env()

            QMessageBox.information(
                self,
                "Success",
                "Environment path reset to default.\nApplication will now restart.",
            )
            self.parent().close()  # This will trigger application restart
