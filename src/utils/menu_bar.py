from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMessageBox
from src.style_config import Theme
from src.ui.dialogs.change_conn_str import ChangeConnectionDialog
from src.ui.dialogs.change_db_dialog import ChangeDatabaseDialog
from src.ui.dialogs.change_pass_dialog import ChangePasswordDialog


class MenuBar:
    def __init__(self, main_window):
        self.main_window = main_window
        self.setup_menubar()

    def setup_menubar(self):
        colors = Theme.get_theme_colors()

        menubar = self.main_window.menuBar()
        menubar.setStyleSheet(
            f"""
            QMenuBar {{
                background-color: {colors['card_bg']};
                color: {colors['text_primary']};
            }}
            QMenuBar::item:selected {{
                background-color: {colors['border']};
            }}
        """
        )

        menu_style = f"""
            QMenu {{
                background-color: {colors['card_bg']};
                color: {colors['text_primary']};
            }}
            QMenu::item:selected {{
                background-color: {colors['border']};
            }}
        """

        # Settings Menu
        settings_menu = menubar.addMenu("Settings")
        settings_menu.setStyleSheet(menu_style)

        # User Settings
        change_password = QAction("Change Password", self.main_window)
        change_password.triggered.connect(self.show_change_password_dialog)

        # Database Settings
        change_database = QAction("Change Database", self.main_window)
        change_database.triggered.connect(self.show_change_database_dialog)

        change_connection = QAction("Change Connection String", self.main_window)
        change_connection.triggered.connect(self.show_change_connection_dialog)

        # Add actions to menu
        settings_menu.addAction(change_password)
        settings_menu.addSeparator()
        settings_menu.addAction(change_database)
        settings_menu.addAction(change_connection)

    def show_change_password_dialog(self):
        if self.main_window.user:
            dialog = ChangePasswordDialog(
                self.main_window, self.main_window.user_manager, self.main_window.user
            )
            dialog.exec()
        else:
            QMessageBox.warning(self.main_window, "Error", "Please log in first")

    def show_change_database_dialog(self):
        if not self.main_window.user:
            QMessageBox.warning(self.main_window, "Error", "Please log in first")
            return

        if self.main_window.user.role != "admin":
            QMessageBox.warning(self.main_window, "Error", "Admin access required")
            return

        dialog = ChangeDatabaseDialog(self.main_window)
        dialog.exec()

    def show_change_connection_dialog(self):
        if not self.main_window.user:
            QMessageBox.warning(self.main_window, "Error", "Please log in first")
            return

        if self.main_window.user.role != "admin":
            QMessageBox.warning(self.main_window, "Error", "Admin access required")
            return

        dialog = ChangeConnectionDialog(
            self.main_window, self.main_window.user_manager, self.main_window.user
        )
        dialog.exec()
