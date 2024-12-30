# src/ui/dialogs/profile_dialog.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk


class UserProfileDialog(ctk.CTkToplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.title("User Profile")
        self.setup_window()

    def setup_window(self):
        width, height = 500, 600
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Profile Header
        header = ctk.CTkFrame(container)
        header.pack(fill="x", pady=(0, 20))

        # Profile Image Frame
        image_frame = ctk.CTkFrame(header, width=120, height=120)
        image_frame.pack(pady=10)
        image_frame.pack_propagate(False)

        # Placeholder image
        ctk.CTkLabel(image_frame, text="👤", font=ctk.CTkFont(size=48)).pack(
            expand=True
        )

        ctk.CTkButton(
            header,
            text="Change Photo",
            command=self.change_photo,
            height=32,
            fg_color="transparent",
            border_width=1,
        ).pack(pady=5)

        # User Details Section
        details = ctk.CTkFrame(container)
        details.pack(fill="x", pady=10)

        # Personal Info
        self.create_section(
            details,
            "Personal Information",
            [
                ("Full Name", self.user.full_name, True),
                ("Username", self.user.username, False),
                ("Email", "user@example.com", True),
                ("Role", self.user.role.capitalize(), False),
            ],
        )

        # Account Info
        account_info = ctk.CTkFrame(container)
        account_info.pack(fill="x", pady=10)

        ctk.CTkLabel(
            account_info,
            text="Account Information",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", pady=10)

        info_text = f"""
        Account Status: Active
        Member Since: {self.user.created_at.strftime('%B %d, %Y')}
        Last Login: Today
        """

        ctk.CTkLabel(account_info, text=info_text, justify="left").pack(
            anchor="w", padx=10
        )

        # Action Buttons
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame,
            text="Change Password",
            command=self.show_change_password,
            height=32,
        ).pack(fill="x", pady=5)

        ctk.CTkButton(
            button_frame, text="Save Changes", command=self.save_changes, height=32
        ).pack(fill="x", pady=5)

        ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.destroy,
            height=32,
            fg_color="transparent",
            border_width=1,
        ).pack(fill="x", pady=5)

    def create_section(self, parent, title, fields):
        section = ctk.CTkFrame(parent)
        section.pack(fill="x", pady=10)

        ctk.CTkLabel(
            section, text=title, font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=10)

        for label, value, editable in fields:
            field_frame = ctk.CTkFrame(section)
            field_frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(
                field_frame, text=label + ":", font=ctk.CTkFont(weight="bold")
            ).pack(anchor="w")

            if editable:
                entry = ctk.CTkEntry(field_frame, height=32)
                entry.pack(fill="x")
                entry.insert(0, value)
            else:
                ctk.CTkLabel(field_frame, text=value).pack(anchor="w")

    def change_photo(self):
        messagebox.showinfo(
            "Change Photo", "Photo change functionality will be implemented soon."
        )

    def show_change_password(self):
        ChangePasswordDialog(self)

    def save_changes(self):
        messagebox.showinfo("Success", "Profile changes saved successfully!")
        self.destroy()


class ChangePasswordDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Change Password")
        self.setup_window()

    def setup_window(self):
        width, height = 400, 300
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            container, text="Change Password", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))

        # Current Password
        ctk.CTkLabel(container, text="Current Password:").pack(anchor="w")

        self.current_password = ctk.CTkEntry(container, show="*", height=32)
        self.current_password.pack(fill="x", pady=(0, 10))

        # New Password
        ctk.CTkLabel(container, text="New Password:").pack(anchor="w")

        self.new_password = ctk.CTkEntry(container, show="*", height=32)
        self.new_password.pack(fill="x", pady=(0, 10))

        # Confirm Password
        ctk.CTkLabel(container, text="Confirm Password:").pack(anchor="w")

        self.confirm_password = ctk.CTkEntry(container, show="*", height=32)
        self.confirm_password.pack(fill="x", pady=(0, 20))

        # Buttons
        ctk.CTkButton(
            container, text="Change Password", command=self.change_password, height=32
        ).pack(fill="x")

    def change_password(self):
        if not all(
            [
                self.current_password.get(),
                self.new_password.get(),
                self.confirm_password.get(),
            ]
        ):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if self.new_password.get() != self.confirm_password.get():
            messagebox.showerror("Error", "New passwords do not match")
            return

        if len(self.new_password.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return

        # Here you would normally verify current password and update new password
        messagebox.showinfo("Success", "Password changed successfully!")
        self.destroy()
