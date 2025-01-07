import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)
from PySide6.QtGui import QIcon
from src.ui.dialogs.db_setup_dialog import DatabaseSetupDialog
from src.ui.main_window import MainWindow
from src.config import Config
from src.database.connection import DatabaseConnection
from src.ui.login_window import LoginWindow


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        # Nuitka
        base_path = os.path.join(os.path.dirname(sys.executable), "assets")
    else:
        # development
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))

    return os.path.join(base_path, relative_path)


def main():
    Config.load_env()
    app = QApplication(sys.argv)

    icon_path = get_resource_path("icon.ico")
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    try:
        if not Config.CONNECTION_STRING:
            setup_dialog = DatabaseSetupDialog()
            if setup_dialog.exec() == DatabaseSetupDialog.Rejected:
                sys.exit(1)

            Config.load_env()

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
