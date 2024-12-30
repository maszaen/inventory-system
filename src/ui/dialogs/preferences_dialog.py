# src/ui/dialogs/preferences_dialog.py
import customtkinter as ctk
from tkinter import messagebox
from src.ui.styles import Styles


class PreferencesDialog(ctk.CTkToplevel):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config
        self.theme = self.config.settings
        self.title("Preferences")
        self.setup_window()

    def setup_window(self):
        width, height = 600, 500
        x = (self.master.winfo_screenwidth() - width) // 2
        y = (self.master.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            container, text="Preferences", font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(0, 20))

        # Create tabs
        tabview = ctk.CTkTabview(container)
        tabview.pack(fill="both", expand=True)

        # Add tabs and their content
        appearance_tab = tabview.add("Appearance")
        self.setup_appearance_tab(appearance_tab)

        interface_tab = tabview.add("Interface")
        self.setup_interface_tab(interface_tab)

        advanced_tab = tabview.add("Advanced")
        self.setup_advanced_tab(advanced_tab)

        # Bottom buttons
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame, text="Save", command=self.save_preferences, width=100
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=100,
            fg_color="transparent",
            border_width=1,
        ).pack(side="right", padx=5)

    def setup_appearance_tab(self, parent):
        # Theme selection
        theme_frame = ctk.CTkFrame(parent)
        theme_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(theme_frame, text="Theme", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w", pady=5
        )

        theme_var = ctk.StringVar(value=self.config.get("theme", "system"))
        for theme in ["Light", "Dark", "System"]:
            ctk.CTkRadioButton(
                theme_frame, text=theme, variable=theme_var, value=theme.lower()
            ).pack(anchor="w", pady=2)

        # Color scheme
        color_frame = ctk.CTkFrame(parent)
        color_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            color_frame, text="Accent Color", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=5)

        colors = ["Blue", "Green", "Purple", "Orange", "Red"]
        accent_var = ctk.StringVar(value=self.config.get("accent_color", "Blue"))

        for color in colors:
            ctk.CTkRadioButton(
                color_frame, text=color, variable=accent_var, value=color
            ).pack(anchor="w", pady=2)

        # Font settings
        font_frame = ctk.CTkFrame(parent)
        font_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            font_frame, text="Font Size", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=5)

        font_scale = ctk.CTkSlider(font_frame, from_=80, to=120, number_of_steps=4)
        font_scale.pack(fill="x", padx=10)
        font_scale.set(self.config.get("font_scale", 100))

    def setup_interface_tab(self, parent):
        # Sidebar settings
        sidebar_frame = ctk.CTkFrame(parent)
        sidebar_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            sidebar_frame, text="Sidebar", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=5)

        sidebar_width = ctk.CTkSlider(
            sidebar_frame, from_=200, to=300, number_of_steps=10
        )
        sidebar_width.pack(fill="x", padx=10)
        sidebar_width.set(self.config.get("sidebar_width", 240))

        # Layout options
        layout_frame = ctk.CTkFrame(parent)
        layout_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            layout_frame, text="Layout Options", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=5)

        options = [
            ("Compact Mode", "compact_mode"),
            ("Show Icons", "show_icons"),
            ("Show Status Bar", "show_status_bar"),
        ]

        for label, key in options:
            switch = ctk.CTkSwitch(layout_frame, text=label)
            switch.pack(anchor="w", pady=2)
            if self.config.get(key, False):
                switch.select()

    def setup_advanced_tab(self, parent):
        # Performance settings
        perf_frame = ctk.CTkFrame(parent)
        perf_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            perf_frame, text="Performance", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=5)

        options = [
            ("Enable Animations", "enable_animations"),
            ("Hardware Acceleration", "hardware_acceleration"),
            ("Background Processing", "background_processing"),
        ]

        for label, key in options:
            switch = ctk.CTkSwitch(perf_frame, text=label)
            switch.pack(anchor="w", pady=2)
            if self.config.get(key, True):
                switch.select()

        # Debug options
        debug_frame = ctk.CTkFrame(parent)
        debug_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            debug_frame, text="Debug Options", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=5)

        debug_switch = ctk.CTkSwitch(debug_frame, text="Debug Mode")
        debug_switch.pack(anchor="w", pady=2)
        if self.config.get("debug_mode", False):
            debug_switch.select()

    def save_preferences(self):
        try:
            # Save logic here
            messagebox.showinfo("Success", "Preferences saved successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {str(e)}")
