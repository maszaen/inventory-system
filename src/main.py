import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QWidget,
)
from src.ui.main_window import MainWindow
from src.config import Config
from src.database.connection import DatabaseConnection
from src.ui.login_window import LoginWindow


def main():
    # Create QApplication instance first
    app = QApplication(sys.argv)

    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    try:
        db = DatabaseConnection.get_instance()
        db.get_collection("test").find_one()

        while True:
            login_window = LoginWindow()
            user = login_window.run()

            if user:
                # Pass the app instance to MainWindow and show it
                main_window = MainWindow(user)
                main_window.show()
                app.exec()  # Start the application loop

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
