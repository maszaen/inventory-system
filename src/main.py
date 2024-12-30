from tkinter import messagebox
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
            user = login_window.run()

            if user:
                # Tampilkan pesan selamat datang
                messagebox.showinfo(
                    title="Success", message=f"Welcome, {user.full_name}!"
                )

                # Buat dan jalankan main window
                app = MainWindow(user=user)
                app.run()

                if not hasattr(app.root, "logout_requested"):
                    break
            else:
                break

    except Exception as e:
        messagebox.showerror(
            title="Database Error",
            message=f"Failed to connect to database: {str(e)}\n\n"
            "Please check your connection settings in .env file.",
        )
    finally:
        DatabaseConnection.get_instance().close()


if __name__ == "__main__":
    main()
