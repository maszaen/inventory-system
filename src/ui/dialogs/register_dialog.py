import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class RegisterDialog(ctk.CTkToplevel):
    def __init__(self, parent, user_manager):
        super().__init__(parent)
        self.user_manager = user_manager
        self.setup_window()

    def setup_window(self):
        self.title("Register New User")
        window_width = 360
        window_height = 480

        # Center dialog
        x = (self.master.winfo_screenwidth() - window_width) // 2
        y = (self.master.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            container,
            text="Create New Account",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.pack(pady=(0, 20))

        # Form fields
        fields_frame = ctk.CTkFrame(container)
        fields_frame.pack(fill="x", pady=(0, 20))

        # Username
        ctk.CTkLabel(fields_frame, text="Username:").pack(fill="x", pady=(0, 5))
        self.username_entry = ctk.CTkEntry(fields_frame, height=32)
        self.username_entry.pack(fill="x", pady=(0, 10))

        # Password
        ctk.CTkLabel(fields_frame, text="Password:").pack(fill="x", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(fields_frame, show="*", height=32)
        self.password_entry.pack(fill="x", pady=(0, 10))

        # Confirm Password
        ctk.CTkLabel(fields_frame, text="Confirm Password:").pack(fill="x", pady=(0, 5))
        self.confirm_password_entry = ctk.CTkEntry(fields_frame, show="*", height=32)
        self.confirm_password_entry.pack(fill="x", pady=(0, 10))

        # Full Name
        ctk.CTkLabel(fields_frame, text="Full Name:").pack(fill="x", pady=(0, 5))
        self.fullname_entry = ctk.CTkEntry(fields_frame, height=32)
        self.fullname_entry.pack(fill="x", pady=(0, 10))

        # Register button
        ctk.CTkButton(
            container, text="Register", command=self.register, height=38
        ).pack(fill="x", pady=(0, 10))

        # Cancel button
        ctk.CTkButton(
            container,
            text="Cancel",
            command=self.destroy,
            height=38,
            fg_color="transparent",
            border_width=2,
        ).pack(fill="x")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        full_name = self.fullname_entry.get()

        if not all([username, password, confirm_password, full_name]):
            CTkMessagebox(
                title="Error", message="Please fill in all fields", icon="cancel"
            )
            return

        if password != confirm_password:
            CTkMessagebox(
                title="Error", message="Passwords do not match", icon="cancel"
            )
            return

        try:
            user = self.user_manager.create_user(username, password, full_name)
            if user:
                CTkMessagebox(
                    title="Success",
                    message="User registered successfully!\nYou can now login.",
                    icon="check",
                )
                self.destroy()
            else:
                raise ValueError("Failed to create user")
        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
