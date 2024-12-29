import tkinter as tk
from tkinter import ttk, messagebox
from src.models.user import UserManager


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.user_manager = UserManager()
        self.setup_window()
        self.current_user = None

    def setup_window(self):
        self.root.title("Login - Inventory System")
        window_width = 300
        window_height = 245

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Username
        ttk.Label(main_frame, text="Username:").pack(fill=tk.X, pady=(0, 5))
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))

        # Password
        ttk.Label(main_frame, text="Password:").pack(fill=tk.X, pady=(0, 5))
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 20))

        # Login button
        ttk.Button(main_frame, text="Login", command=self.login).pack(
            fill=tk.X, pady=(0, 10)
        )

        # Register button
        ttk.Button(main_frame, text="Register", command=self.show_register_dialog).pack(
            fill=tk.X
        )

        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        try:
            user = self.user_manager.authenticate(username, password)
            if user:
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome, {user.full_name}!")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_register_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Register New User")
        dialog.geometry("300x335")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog
        x = (self.root.winfo_screenwidth() - 300) // 2
        y = (self.root.winfo_screenheight() - 300) // 2
        dialog.geometry(f"+{x}+{y}")

        # Create form
        ttk.Label(dialog, text="Username:").pack(pady=(20, 5))
        username_entry = ttk.Entry(dialog)
        username_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Password:").pack(pady=(0, 5))
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Confirm Password:").pack(pady=(0, 5))
        confirm_password_entry = ttk.Entry(dialog, show="*")
        confirm_password_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Full Name:").pack(pady=(0, 5))
        fullname_entry = ttk.Entry(dialog)
        fullname_entry.pack(pady=(0, 20))

        def register():
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            full_name = fullname_entry.get()

            if not all([username, password, confirm_password, full_name]):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return

            try:
                user = self.user_manager.create_user(username, password, full_name)
                if user:
                    messagebox.showinfo(
                        "Success", "User registered successfully!\nYou can now login."
                    )
                    dialog.destroy()
                else:
                    raise ValueError("Failed to create user")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Register", command=register).pack(fill=tk.X, padx=20)

    def run(self):
        self.root.mainloop()
        return self.current_user
