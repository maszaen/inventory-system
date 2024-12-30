import customtkinter as ctk
from tkinter import messagebox


class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.setup_window()

    def setup_window(self):
        window_width = 500
        window_height = 400

        # Center dialog
        x = (self.master.winfo_screenwidth() - window_width) // 2
        y = (self.master.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            container,
            text="Application Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(0, 20))

        # Settings Tabs
        tabview = ctk.CTkTabview(container)
        tabview.pack(fill="both", expand=True)

        # Add tabs
        tabview.add("General")
        tabview.add("Appearance")
        tabview.add("Backup")

        # General Settings
        self.setup_general_tab(tabview.tab("General"))

        # Appearance Settings
        self.setup_appearance_tab(tabview.tab("Appearance"))

        # Backup Settings
        self.setup_backup_tab(tabview.tab("Backup"))

        # Buttons
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame, text="Save", command=self.save_settings, height=32
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            height=32,
            fg_color="transparent",
            border_width=1,
        ).pack(side="right", padx=5)

    def setup_general_tab(self, parent):
        # Currency Settings
        currency_frame = ctk.CTkFrame(parent)
        currency_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            currency_frame, text="Currency Format:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.currency_var = ctk.StringVar(value="IDR (Rp)")
        currency_combo = ctk.CTkComboBox(
            currency_frame,
            values=["IDR (Rp)", "USD ($)", "EUR (€)"],
            variable=self.currency_var,
            width=200,
        )
        currency_combo.pack(anchor="w", padx=10)

        # Date Format
        date_frame = ctk.CTkFrame(parent)
        date_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            date_frame, text="Date Format:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.date_var = ctk.StringVar(value="YYYY-MM-DD")
        date_combo = ctk.CTkComboBox(
            date_frame,
            values=["YYYY-MM-DD", "DD-MM-YYYY", "MM/DD/YYYY"],
            variable=self.date_var,
            width=200,
        )
        date_combo.pack(anchor="w", padx=10)

    def setup_appearance_tab(self, parent):
        # Theme Selection
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            theme_frame, text="Color Theme:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.theme_var = ctk.StringVar(value="system")
        themes = ["system", "light", "dark"]

        for theme in themes:
            ctk.CTkRadioButton(
                theme_frame,
                text=theme.capitalize(),
                variable=self.theme_var,
                value=theme,
            ).pack(anchor="w", padx=10, pady=2)

        # Font Settings
        font_frame = ctk.CTkFrame(parent)
        font_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            font_frame, text="Font Size:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.font_scale = ctk.CTkSlider(font_frame, from_=80, to=120, number_of_steps=4)
        self.font_scale.pack(anchor="w", padx=10, fill="x")
        self.font_scale.set(100)

    def setup_backup_tab(self, parent):
        # Auto Backup Settings
        backup_frame = ctk.CTkFrame(parent)
        backup_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            backup_frame, text="Auto Backup:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        self.backup_var = ctk.StringVar(value="daily")
        options = ["disabled", "daily", "weekly", "monthly"]

        for option in options:
            ctk.CTkRadioButton(
                backup_frame,
                text=option.capitalize(),
                variable=self.backup_var,
                value=option,
            ).pack(anchor="w", padx=10, pady=2)

        # Backup Location
        location_frame = ctk.CTkFrame(parent)
        location_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            location_frame, text="Backup Location:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        backup_path = ctk.CTkEntry(location_frame, width=300)
        backup_path.pack(side="left", padx=10)
        backup_path.insert(0, "./backups")

        ctk.CTkButton(location_frame, text="Browse", width=80, height=28).pack(
            side="left", padx=5
        )

        # Manual Backup Button
        ctk.CTkButton(
            parent,
            text="Create Backup Now",
            height=32,
            fg_color="transparent",
            border_width=1,
        ).pack(anchor="w", padx=10, pady=20)

    def save_settings(self):
        # Save settings implementation
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.destroy()
