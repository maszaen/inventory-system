from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
import pymongo

from src.config import EnvConfig


class ChangeConnectionDialog(QDialog):
    def __init__(self, parent=None, user_manager=None, current_user=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.current_user = current_user
        self.setWindowTitle("Change Connection String")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Password verification
        pass_label = QLabel("Current Password:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)

        # New connection string
        conn_label = QLabel("New Connection String:")
        self.conn_input = QLineEdit()
        self.conn_input.setPlaceholderText("mongodb://username:password@host:port/")

        # Test connection button
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)

        # Save button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setEnabled(False)

        layout.addWidget(pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(conn_label)
        layout.addWidget(self.conn_input)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.save_btn)

    def test_connection(self):
        try:
            # Verify password first
            if not self.current_user.check_password(self.pass_input.text()):
                raise ValueError("Incorrect password")

            # Test new connection
            uri = self.conn_input.text().strip()
            client = pymongo.MongoClient(uri)
            client.server_info()  # This will raise an exception if connection fails
            client.close()

            # Enable save button if connection successful
            self.save_btn.setEnabled(True)
            QMessageBox.information(self, "Success", "Connection test successful!")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(
                self, "Connection Error", f"Failed to connect: {str(e)}"
            )

    def save_changes(self):
        try:
            # Verify password again for security
            if not self.current_user.check_password(self.pass_input.text()):
                raise ValueError("Incorrect password")

            # Konfirmasi perubahan
            reply = QMessageBox.question(
                self,
                "Confirm Change",
                "Changing connection string requires application restart.\nProceed with change?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                # Save new connection string
                EnvConfig.save_config(
                    self.conn_input.text().strip(),
                    EnvConfig.DB_NAME,  # Keep current database
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Connection string changed successfully.\nApplication will now close.\n\nPlease restart the application.",
                )

                # Close main window which will exit application
                self.parent().close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save changes: {str(e)}")
