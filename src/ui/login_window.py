import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from src.models.user import UserManager
from src.ui.dialogs.register_dialog import RegisterDialog


class LoginWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.user_manager = UserManager()
        self.current_user = None
        self.setup_window()

    def setup_window(self):
        self.root.title("Login - Inventory System")
        window_width = 360
        window_height = 400

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            self.main_frame,
            text="Inventory System Login",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.pack(pady=(0, 20))

        # Username
        ctk.CTkLabel(self.main_frame, text="Username:").pack(fill="x", pady=(0, 5))
        self.username_entry = ctk.CTkEntry(self.main_frame, height=32)
        self.username_entry.pack(fill="x", pady=(0, 10))

        # Password
        ctk.CTkLabel(self.main_frame, text="Password:").pack(fill="x", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(self.main_frame, show="*", height=32)
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Buttons
        ctk.CTkButton(
            self.main_frame, text="Login", command=self.login, height=38
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            self.main_frame,
            text="Register",
            command=self.show_register_dialog,
            height=38,
            fg_color="transparent",
            border_width=2,
        ).pack(fill="x")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            CTkMessagebox(
                title="Error", message="Please enter both username and password"
            )
            return

        try:
            user = self.user_manager.authenticate(username, password)
            if user:
                self.current_user = user
                # Pindahkan messagebox welcome ke main.py
                self.root.quit()
            else:
                CTkMessagebox(title="Error", message="Invalid username or password")
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))

    def show_register_dialog(self):
        register_dialog = RegisterDialog(self.root, self.user_manager)
        register_dialog.grab_set()

    def run(self):
        self.root.mainloop()
        if self.root:  # Check if root still exists
            self.root.destroy()  # Destroy setelah mainloop selesai
        return self.current_user
