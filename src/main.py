import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QDialog,
)
from PySide6.QtGui import QIcon
from src.ui.dialogs.db_setup_dialog import DatabaseSetupDialog
from src.ui.main_window import MainWindow
from src.config import Config, EnvConfig
from src.database.connection import DatabaseConnection
from src.ui.login_window import LoginWindow


def restart_app():
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()


def get_resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    app = QApplication(sys.argv)

    icon_path = get_resource_path(os.path.join("assets", "icon.png"))
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    try:
        if not EnvConfig.CONNECTION_STRING:
            setup_dialog = DatabaseSetupDialog()
            if setup_dialog.exec() == QDialog.Rejected:
                sys.exit(1)
            else:
                restart_app()

        _ = DatabaseConnection.get_instance()

        while True:
            login_window = LoginWindow()
            user = login_window.run()

            if user:
                main_window = MainWindow(user)
                main_window.show()
                app.exec()

                if not hasattr(main_window, "logout_requested"):
                    break
            else:
                break

    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error: {str(e)}\n\n")
    finally:
        DatabaseConnection.get_instance().close()


if __name__ == "__main__":
    main()
