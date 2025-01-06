from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox

from src.style_config import Theme


class RegisterDialog(QDialog):
    def __init__(self, parent=None, user_manager=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.setup_ui()

    def setup_ui(self):
        form_fields = Theme.form()
        btnmg = Theme.btnmg()
        self.setWindowTitle("Register New User")
        self.setFixedSize(400, 233)

        form_layout = QFormLayout(self)

        # Create input fields
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Enter username...")
        self.username_entry.setStyleSheet(form_fields)
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Enter password...")
        self.password_entry.setStyleSheet(form_fields)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.confirm_password_entry = QLineEdit(self)
        self.confirm_password_entry.setPlaceholderText("Confirm password...")
        self.confirm_password_entry.setStyleSheet(form_fields)
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.fullname_entry = QLineEdit(self)
        self.fullname_entry.setPlaceholderText("Enter full name...")
        self.fullname_entry.setStyleSheet(form_fields)

        # Add fields to form
        form_layout.addRow("Username:", self.username_entry)
        form_layout.addRow("Password:", self.password_entry)
        form_layout.addRow("Confirm:", self.confirm_password_entry)
        form_layout.addRow("Full Name:", self.fullname_entry)

        # Register button
        register_button = QPushButton("Register", self)
        register_button.setStyleSheet(btnmg)

        register_button.clicked.connect(self.register)
        form_layout.addWidget(register_button)

        self.setLayout(form_layout)

    def register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        full_name = self.fullname_entry.text()

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
                self.accept()
            else:
                raise ValueError("Failed to create user")
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
