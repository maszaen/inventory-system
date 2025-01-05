from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
)
from PySide6.QtCore import Qt
import pymongo
from typing import Optional
from config import Config, EnvConfig
from models.user import UserManager


class DatabaseSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Database Setup")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Connection String Input
        conn_layout = QVBoxLayout()
        conn_label = QLabel("MongoDB Connection String:")
        self.conn_input = QLineEdit()
        self.conn_input.setPlaceholderText("mongodb://username:password@host:port/")
        self.conn_input.textChanged.connect(self.validate_inputs)
        conn_layout.addWidget(conn_label)
        conn_layout.addWidget(self.conn_input)

        # Test Connection Button
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        conn_layout.addWidget(self.test_btn)

        # Database Selection
        db_layout = QVBoxLayout()
        db_label = QLabel("Select Database:")
        self.db_combo = QComboBox()
        self.db_combo.setEnabled(False)
        self.db_combo.currentTextChanged.connect(self.validate_inputs)
        db_layout.addWidget(db_label)
        db_layout.addWidget(self.db_combo)

        # Register First User Section
        register_layout = QVBoxLayout()
        register_label = QLabel("Register Administrator Account")
        register_label.setStyleSheet("font-weight: bold; margin-top: 10px;")

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.textChanged.connect(self.validate_inputs)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.validate_inputs)

        # Full Name
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Full Name")
        self.fullname_input.textChanged.connect(self.validate_inputs)

        # Register Button
        self.register_btn = QPushButton("Register and Complete Setup")
        self.register_btn.setEnabled(False)
        self.register_btn.clicked.connect(self.complete_setup)

        register_layout.addWidget(register_label)
        register_layout.addWidget(self.username_input)
        register_layout.addWidget(self.password_input)
        register_layout.addWidget(self.fullname_input)
        register_layout.addWidget(self.register_btn)

        # Login Option
        login_layout = QHBoxLayout()
        login_label = QLabel("Already have an account?")
        login_link = QPushButton("Skip to Login")
        login_link.setFlat(True)
        login_link.setCursor(Qt.PointingHandCursor)
        login_link.setStyleSheet(
            """
            QPushButton {
                border: none;
                color: #2563eb;
                text-decoration: underline;
                padding: 0px;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #1d4ed8;
            }
        """
        )
        login_link.clicked.connect(self.skip_to_login)

        login_layout.addWidget(login_label)
        login_layout.addWidget(login_link)
        login_layout.addStretch()

        # Add all layouts
        layout.addLayout(conn_layout)
        layout.addLayout(db_layout)
        layout.addLayout(register_layout)
        layout.addLayout(login_layout)

        # Set initial state
        self.mongo_client: Optional[pymongo.MongoClient] = None
        self.validate_inputs()

        if EnvConfig.MONGODB_URI:
            self.conn_input.setText(EnvConfig.MONGODB_URI)

    def validate_inputs(self):
        """Enable/disable buttons based on input state"""
        has_connection = bool(self.conn_input.text().strip())
        self.test_btn.setEnabled(has_connection)

        can_register = all(
            [
                self.db_combo.currentText(),
                self.username_input.text().strip(),
                self.password_input.text().strip(),
                self.fullname_input.text().strip(),
            ]
        )
        self.register_btn.setEnabled(can_register)

    def skip_to_login(self):
        """Skip registration and proceed to login"""
        uri = self.conn_input.text().strip()
        db_name = self.db_combo.currentText()

        if not all([uri, db_name]):
            QMessageBox.warning(
                self,
                "Incomplete Setup",
                "Please complete database connection setup first",
            )
            return

        reply = QMessageBox.question(
            self,
            "Skip Registration",
            "Save current database configuration and proceed to login?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                EnvConfig.save_config(uri, db_name)

                Config.save_config(uri, db_name)

                QMessageBox.information(
                    self,
                    "Configuration Saved",
                    "Database configuration saved.\nProceeding to login.",
                )

                self.done(QDialog.Accepted)

            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to save configuration: {str(e)}"
                )

    def test_connection(self):
        """Test MongoDB connection and populate database list"""
        try:
            # Close existing connection if any
            if self.mongo_client:
                self.mongo_client.close()

            uri = self.conn_input.text().strip()
            self.mongo_client = pymongo.MongoClient(uri)

            # Test connection
            self.mongo_client.server_info()

            # Get database list
            db_list = self.mongo_client.list_database_names()

            # Update combobox
            self.db_combo.clear()
            self.db_combo.addItems(db_list)
            self.db_combo.setEnabled(True)

            # Select existing database if configured
            if EnvConfig.DB_NAME in db_list:
                self.db_combo.setCurrentText(EnvConfig.DB_NAME)

            QMessageBox.information(self, "Success", "Connection successful!")

        except Exception as e:
            self.db_combo.clear()
            self.db_combo.setEnabled(False)
            QMessageBox.critical(
                self, "Connection Error", f"Failed to connect: {str(e)}"
            )

    def complete_setup(self):
        try:
            uri = self.conn_input.text().strip()
            db_name = self.db_combo.currentText()

            # Save configuration
            EnvConfig.save_config(uri, db_name)

            Config.save_config(uri, db_name)

            db = self.mongo_client[db_name]

            # Create admin user
            user_manager = UserManager()
            admin_user = user_manager.create_user(
                username=self.username_input.text().strip(),
                password=self.password_input.text().strip(),
                full_name=self.fullname_input.text().strip(),
                role="admin",
            )

            if admin_user:
                QMessageBox.information(
                    self,
                    "Setup Complete",
                    "Database setup and admin registration successful!\n"
                    "Please restart the application.",
                )
                self.accept()
            else:
                raise Exception("Failed to create admin user")

        except Exception as e:
            QMessageBox.critical(self, "Setup Error", f"Setup failed: {str(e)}")

    def closeEvent(self, event):
        if self.mongo_client:
            self.mongo_client.close()
        super().closeEvent(event)
