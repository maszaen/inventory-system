import tkinter as tk
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ui.main_window import MainWindow
from src.config import Config
from src.database.connection import DatabaseConnection
from src.ui.login_window import LoginWindow


def main():
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    try:
        db = DatabaseConnection.get_instance()
        db.get_collection("test").find_one()

        while True:
            login_window = LoginWindow()
            login_window.root.mainloop()

            user = login_window.current_user
            if user:
                root = tk.Tk()
                _ = MainWindow(root, user)
                root.mainloop()

                if not hasattr(root, "logout_requested"):
                    break
            else:
                break

    except Exception as e:
        tk.messagebox.showerror(
            "Database Error",
            f"Failed to connect to database: {str(e)}\n\n"
            "Please check your connection settings in .env file.",
        )
    finally:
        DatabaseConnection.get_instance().close()


if __name__ == "__main__":
    main()
