# src/ui/tabs/settings_tab.py
import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
from src.ui.styles import Styles


class SettingsTab(ctk.CTkFrame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config
        self.theme = self.config.settings
        self.unsaved_changes = {}
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header, text="Settings", font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w")

        # Settings Container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Create tabs for different settings
        tabview = ctk.CTkTabview(container)
        tabview.pack(fill="both", expand=True)

        tabs = [
            ("General", self.setup_general_tab),
            ("Appearance", self.setup_appearance_tab),
            ("Data", self.setup_data_tab),
            ("Advanced", self.setup_advanced_tab),
        ]

        for tab_name, setup_func in tabs:
            tab = tabview.add(tab_name)
            setup_func(tab)

        # Bottom buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            button_frame, text="Save Changes", command=self.save_changes, width=120
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Reset All",
            command=self.reset_settings,
            width=120,
            fg_color="transparent",
            border_width=1,
        ).pack(side="right", padx=5)

    def setup_general_tab(self, parent):
        # Currency Settings
        self.create_section(
            parent,
            "Currency Format",
            [
                {
                    "type": "combobox",
                    "label": "Currency",
                    "key": "currency",
                    "values": ["IDR (Rp)", "USD ($)", "EUR (€)"],
                    "default": self.config.get("currency", "IDR"),
                },
                {
                    "type": "switch",
                    "label": "Show Decimals",
                    "key": "show_decimals",
                    "default": self.config.get("show_decimals", True),
                },
            ],
        )

        # Date & Time Settings
        self.create_section(
            parent,
            "Date & Time",
            [
                {
                    "type": "combobox",
                    "label": "Date Format",
                    "key": "date_format",
                    "values": ["YYYY-MM-DD", "DD-MM-YYYY", "MM/DD/YYYY"],
                    "default": self.config.get("date_format", "YYYY-MM-DD"),
                },
                {
                    "type": "combobox",
                    "label": "Time Format",
                    "key": "time_format",
                    "values": ["24-hour", "12-hour"],
                    "default": self.config.get("time_format", "24-hour"),
                },
            ],
        )

        # Language Settings
        self.create_section(
            parent,
            "Language",
            [
                {
                    "type": "combobox",
                    "label": "Display Language",
                    "key": "language",
                    "values": ["English", "Indonesian"],
                    "default": self.config.get("language", "English"),
                }
            ],
        )

    def setup_appearance_tab(self, parent):
        # Theme Settings
        self.create_section(
            parent,
            "Theme",
            [
                {
                    "type": "combobox",
                    "label": "Color Theme",
                    "key": "theme",
                    "values": ["Light", "Dark", "System"],
                    "default": self.config.get("theme", "System"),
                    "command": self.on_theme_change,
                },
                {
                    "type": "combobox",
                    "label": "Accent Color",
                    "key": "accent_color",
                    "values": ["Blue", "Green", "Purple", "Orange"],
                    "default": self.config.get("accent_color", "Blue"),
                },
            ],
        )

        # Font Settings
        self.create_section(
            parent,
            "Font",
            [
                {
                    "type": "combobox",
                    "label": "Size",
                    "key": "font_size",
                    "values": ["Small", "Medium", "Large"],
                    "default": self.config.get("font_size", "Medium"),
                }
            ],
        )

        # Layout Settings
        self.create_section(
            parent,
            "Layout",
            [
                {
                    "type": "slider",
                    "label": "Sidebar Width",
                    "key": "sidebar_width",
                    "from_": 200,
                    "to": 300,
                    "default": self.config.get("sidebar_width", 240),
                },
                {
                    "type": "switch",
                    "label": "Compact Mode",
                    "key": "compact_mode",
                    "default": self.config.get("compact_mode", False),
                },
            ],
        )

    def setup_data_tab(self, parent):
        # Backup Settings
        self.create_section(
            parent,
            "Backup",
            [
                {
                    "type": "combobox",
                    "label": "Auto Backup",
                    "key": "auto_backup",
                    "values": ["Disabled", "Daily", "Weekly", "Monthly"],
                    "default": self.config.get("auto_backup", "Weekly"),
                }
            ],
        )

        # Backup Location
        location_frame = ctk.CTkFrame(parent)
        location_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            location_frame, text="Backup Location", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(0, 5))

        path_frame = ctk.CTkFrame(location_frame)
        path_frame.pack(fill="x")

        self.backup_path = ctk.CTkEntry(
            path_frame, placeholder_text="Select backup location..."
        )
        self.backup_path.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.backup_path.insert(0, self.config.get("backup_path", "./backups"))

        ctk.CTkButton(
            path_frame, text="Browse", width=80, command=self.browse_backup_location
        ).pack(side="right")

        # Manual Backup
        backup_frame = ctk.CTkFrame(parent)
        backup_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            backup_frame, text="Create Backup Now", command=self.create_backup
        ).pack(fill="x")

    def setup_advanced_tab(self, parent):
        # Performance Settings
        self.create_section(
            parent,
            "Performance",
            [
                {
                    "type": "switch",
                    "label": "Enable Animations",
                    "key": "enable_animations",
                    "default": self.config.get("enable_animations", True),
                },
                {
                    "type": "switch",
                    "label": "Background Processing",
                    "key": "background_processing",
                    "default": self.config.get("background_processing", True),
                },
            ],
        )

        # Developer Options
        self.create_section(
            parent,
            "Developer",
            [
                {
                    "type": "switch",
                    "label": "Debug Mode",
                    "key": "debug_mode",
                    "default": self.config.get("debug_mode", False),
                },
                {
                    "type": "switch",
                    "label": "Show Console",
                    "key": "show_console",
                    "default": self.config.get("show_console", False),
                },
            ],
        )

    def create_section(self, parent, title, fields):
        section = ctk.CTkFrame(parent)
        section.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            section, text=title, font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(10, 5))

        for field in fields:
            field_frame = ctk.CTkFrame(section)
            field_frame.pack(fill="x", pady=2)

            ctk.CTkLabel(field_frame, text=field["label"]).pack(side="left")

            if field["type"] == "combobox":
                widget = ctk.CTkComboBox(
                    field_frame,
                    values=field["values"],
                    width=200,
                    command=lambda v, k=field["key"]: self.on_value_change(k, v),
                )
                widget.set(field["default"])
                widget.pack(side="right")

            elif field["type"] == "switch":
                widget = ctk.CTkSwitch(
                    field_frame,
                    text="",
                    command=lambda: self.on_value_change(field["key"], widget.get()),
                )
                widget.pack(side="right")
                if field["default"]:
                    widget.select()
                else:
                    widget.deselect()

            elif field["type"] == "slider":
                widget = ctk.CTkSlider(
                    field_frame,
                    from_=field["from_"],
                    to=field["to"],
                    command=lambda v: self.on_value_change(field["key"], int(v)),
                )
                widget.pack(side="right", padx=10)
                widget.set(field["default"])

    def on_value_change(self, key, value):
        self.unsaved_changes[key] = value

    def on_theme_change(self, theme):
        self.unsaved_changes["theme"] = theme.lower()

    def browse_backup_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.backup_path.delete(0, "end")
            self.backup_path.insert(0, directory)
            self.unsaved_changes["backup_path"] = directory

    def create_backup(self):
        # Implement backup functionality
        messagebox.showinfo("Backup", "Backup created successfully!")

    def save_changes(self):
        if not self.unsaved_changes:
            messagebox.showinfo("Settings", "No changes to save")
            return

        try:
            for key, value in self.unsaved_changes.items():
                self.config.set(key, value)
            messagebox.showinfo("Settings", "Settings saved successfully!")
            self.unsaved_changes.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def reset_settings(self):
        if messagebox.askyesno(
            "Reset Settings", "Are you sure you want to reset all settings to default?"
        ):
            self.config.settings = self.config.DEFAULT_CONFIG.copy()
            self.config.save_config()
            messagebox.showinfo("Settings", "Settings reset to default")
            # Refresh UI
            self.destroy()
            self.__init__(self.master, self.config)
