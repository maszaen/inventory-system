from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QLabel,
)
from src.models.user import UserManager
from src.style_config import Theme


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.current_user = None
        self.setup_window()

    def setup_window(self):
        colors = Theme.get_theme_colors()
        self.setWindowTitle("Login - PyStockFlow")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # Create a vertical form layout for the form fields
        form_layout = QVBoxLayout()

        username_label = QLabel("Username:")
        username_label.setStyleSheet(f"color: {colors['text_primary']};")
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Enter username...")
        self.username_entry.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
            }}
            """
        )

        password_label = QLabel("Password:")
        password_label.setStyleSheet(f"color: {colors['text_primary']};")
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Enter your password...")
        self.password_entry.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                margin-bottom: 20px;
                color: {colors['text_primary']};
            }}
            """
        )
        self.password_entry.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_entry)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_entry)

        layout.addLayout(form_layout)

        login_button = QPushButton("Login", self)
        login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            """
        )
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        autofill_button = QPushButton("Auto Fill", self)
        autofill_button.setStyleSheet(
            """
            QPushButton {
            background-color: #4caf50;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            color: white;
            font-weight: bold;
            }
            QPushButton:hover {
            background-color: #388e3c;
            }
            """
        )
        autofill_button.clicked.connect(self.autofill_credentials)
        layout.addWidget(autofill_button)

        # register_button = QPushButton("Register", self)
        # register_button.clicked.connect(self.show_register_dialog)
        # layout.addWidget(register_button)

        self.setLayout(layout)

    def autofill_credentials(self):
        self.username_entry.setText("adminzaen")
        self.password_entry.setText("Qeonaru209")
        self.login()

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if not username or not password:
            QMessageBox.critical(
                self, "Error", "Please enter both username and password"
            )
            return

        try:
            user = self.user_manager.authenticate(username, password)
            if user:
                self.current_user = user
                self.accept()
            else:
                QMessageBox.critical(
                    self, "Error", "Invalid username or password, please try again"
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def show_register_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Register New User")
        dialog.setFixedSize(300, 175)

        form_layout = QFormLayout(dialog)

        self.username_entry_register = QLineEdit(dialog)
        self.password_entry_register = QLineEdit(dialog)
        self.password_entry_register.setEchoMode(QLineEdit.Password)
        self.confirm_password_entry_register = QLineEdit(dialog)
        self.confirm_password_entry_register.setEchoMode(QLineEdit.Password)
        self.fullname_entry_register = QLineEdit(dialog)

        form_layout.addRow("Username:", self.username_entry_register)
        form_layout.addRow("Password:", self.password_entry_register)
        form_layout.addRow("Confirm:", self.confirm_password_entry_register)
        form_layout.addRow("Full Name:", self.fullname_entry_register)

        register_button = QPushButton("Register", dialog)
        register_button.clicked.connect(self.register)
        form_layout.addWidget(register_button)

        dialog.setLayout(form_layout)
        dialog.exec()

    def register(self):
        username = self.username_entry_register.text()
        password = self.password_entry_register.text()
        confirm_password = self.confirm_password_entry_register.text()
        full_name = self.fullname_entry_register.text()

        if not all([username, password, confirm_password, full_name]):
            QMessageBox.critical(self, "Error", "Please fill in all fields")
            return

        if password != confirm_password:
            QMessageBox.critical(self, "Error", "Passwords do not match")
            return

        try:
            user = self.user_manager.create_user(username, password, full_name)
            if user:
                QMessageBox.information(
                    self, "Success", "User registered successfully!\nYou can now login."
                )
                self.close()
            else:
                raise ValueError("Failed to create user")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def run(self):
        result = self.exec()
        return self.current_user if result == QDialog.Accepted else None
