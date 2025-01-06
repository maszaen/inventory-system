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
        btnmg = Theme.btnmg()
        # grnbtn = Theme.green_btn()
        form = Theme.form()
        self.setWindowTitle("Login - PyStockFlow")
        self.setFixedSize(400, 220)

        layout = QVBoxLayout()

        # Create a vertical form layout for the form fields
        form_layout = QVBoxLayout()

        username_label = QLabel("Username:")
        username_label.setStyleSheet(f"color: {colors['text_primary']};")
        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Enter username...")
        self.username_entry.setStyleSheet(form)

        password_label = QLabel("Password:")
        password_label.setStyleSheet(f"color: {colors['text_primary']};")
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Enter your password...")
        self.password_entry.setStyleSheet(form)
        self.password_entry.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_entry)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_entry)

        layout.addLayout(form_layout)

        login_button = QPushButton("Login", self)
        login_button.setStyleSheet(btnmg)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # autofill_button = QPushButton("Auto Fill", self)
        # autofill_button.setStyleSheet(grnbtn)
        # autofill_button.clicked.connect(self.autofill_credentials)
        # layout.addWidget(autofill_button)

        # register_button = QPushButton("Register", self)
        # register_button.clicked.connect(self.show_register_dialog)
        # layout.addWidget(register_button)

        self.setLayout(layout)

    # def autofill_credentials(self):
    #     self.username_entry.setText("adminzaen")
    #     self.password_entry.setText("Qeonaru209")
    #     self.login()

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

    def run(self):
        result = self.exec()
        return self.current_user if result == QDialog.Accepted else None
