from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
)

from src.style_config import Theme


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None, user_manager=None, current_user=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.current_user = current_user
        self.setWindowTitle("Change Password")
        self.setFixedSize(400, 305)
        self.setup_ui()

    def setup_ui(self):
        btn = Theme.btn()
        btnmg = Theme.btnmg()
        form = Theme.form()
        layout = QVBoxLayout(self)

        # Current Password
        self.current_pass = QLineEdit()
        self.current_pass.setStyleSheet(form)
        self.current_pass.setPlaceholderText("Current Password")
        self.current_pass.setEchoMode(QLineEdit.Password)

        # New Password
        self.new_pass = QLineEdit()
        self.new_pass.setStyleSheet(form)
        self.new_pass.setPlaceholderText("New Password")
        self.new_pass.setEchoMode(QLineEdit.Password)

        # Confirm New Password
        self.confirm_pass = QLineEdit()
        self.confirm_pass.setStyleSheet(form)
        self.confirm_pass.setPlaceholderText("Confirm New Password")
        self.confirm_pass.setEchoMode(QLineEdit.Password)

        # Change Button
        self.change_btn = QPushButton("Change Password")
        self.change_btn.setStyleSheet(btnmg)
        self.change_btn.clicked.connect(self.change_password)

        # Add to layout
        layout.addWidget(QLabel("Current Password:"))
        layout.addWidget(self.current_pass)
        layout.addWidget(QLabel("New Password:"))
        layout.addWidget(self.new_pass)
        layout.addWidget(QLabel("Confirm New Password:"))
        layout.addWidget(self.confirm_pass)
        layout.addWidget(self.change_btn)

    def change_password(self):
        try:
            current = self.current_pass.text()
            new_pass = self.new_pass.text()
            confirm = self.confirm_pass.text()

            # Validate current password
            if not self.current_user.check_password(current):
                raise ValueError("Current password is incorrect")

            # Validate new password
            if new_pass != confirm:
                raise ValueError("New passwords do not match")

            if len(new_pass) < 6:
                raise ValueError("Password must be at least 6 characters")

            # Update password in database
            success = self.user_manager.update_user_password(
                self.current_user._id, new_pass
            )

            if success:
                QMessageBox.information(
                    self, "Success", "Password changed successfully!"
                )
                self.accept()
            else:
                raise ValueError("Failed to update password")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
