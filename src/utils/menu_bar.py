from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMessageBox
from src.style_config import Theme
from src.ui.dialogs.change_conn_str import ChangeConnectionDialog
from src.ui.dialogs.change_db_dialog import ChangeDatabaseDialog
from src.ui.dialogs.change_pass_dialog import ChangePasswordDialog
from src.ui.dialogs.env_path_dialog import EnvironmentPathDialog
from src.ui.dialogs.register_dialog import RegisterDialog


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
                background-color: {colors['base']};
                border-bottom: 1px solid {colors['border']};
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

        # Accounts Menu
        accounts_menu = menubar.addMenu("Accounts")
        accounts_menu.setStyleSheet(menu_style)

        register_user = QAction("Register New User", self.main_window)
        register_user.triggered.connect(self.show_register_dialog)

        change_password = QAction("Change Password", self.main_window)
        change_password.triggered.connect(self.show_change_password_dialog)

        accounts_menu.addAction(register_user)
        accounts_menu.addAction(change_password)

        # Settings Menu
        settings_menu = menubar.addMenu("Settings")
        settings_menu.setStyleSheet(menu_style)

        # Environment Settings
        env_settings = QAction("Environment Settings", self.main_window)
        env_settings.triggered.connect(self.show_env_settings_dialog)

        # Database Settings
        change_database = QAction("Change Database", self.main_window)
        change_database.triggered.connect(self.show_change_database_dialog)

        change_connection = QAction("Change Connection String", self.main_window)
        change_connection.triggered.connect(self.show_change_connection_dialog)

        delete_env = QAction("Delete Environment", self.main_window)
        delete_env.triggered.connect(self.show_delete_env_dialog)

        # Add actions to Settings menu
        settings_menu.addAction(env_settings)
        settings_menu.addSeparator()
        settings_menu.addAction(change_database)
        settings_menu.addAction(change_connection)
        settings_menu.addAction(delete_env)

    def show_env_settings_dialog(self):
        """Show environment settings dialog"""
        if not self.main_window.user:
            QMessageBox.warning(self.main_window, "Error", "Please log in first")
            return

        if self.main_window.user.role != "admin":
            QMessageBox.warning(self.main_window, "Error", "Admin access required")
            return

        dialog = EnvironmentPathDialog(self.main_window)
        dialog.exec()

    def show_register_dialog(self):
        if not self.main_window.user:
            QMessageBox.warning(self.main_window, "Error", "Please log in first")
            return

        if self.main_window.user.role != "admin":
            QMessageBox.warning(self.main_window, "Error", "Admin access required")
            return

        dialog = RegisterDialog(self.main_window, self.main_window.user_manager)
        dialog.exec()

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

    def show_delete_env_dialog(self):
        if not self.main_window.user:
            QMessageBox.warning(self.main_window, "Error", "Please log in first")
            return

        if self.main_window.user.role != "admin":
            QMessageBox.warning(self.main_window, "Error", "Admin access required")
            return

        reply = QMessageBox.question(
            self.main_window,
            "Delete Environment",
            "Are you sure you want to delete the current environment variables? this application will be closed",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.main_window.config.remove_env()
            QMessageBox.information(self.main_window, "Success", "Environment deleted")
