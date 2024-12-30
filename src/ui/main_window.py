# src/ui/main_window.py
from logging import Logger
import customtkinter as ctk
from tkinter import Menu, messagebox
from src.models.product import ProductManager
from src.utils.config import AppConfig
from src.models.transaction import TransactionManager
from src.ui.theme import AppTheme
from src.ui.styles import Styles


class MainWindow:
    def __init__(self, user=None):
        self.user = user
        self.config = AppConfig()
        self.theme = AppTheme.setup_theme(self.config.get("theme", "dark"))
        self.logger = Logger("main")
        self.product_manager = ProductManager()
        self.transaction_manager = TransactionManager()
        self.setup_window()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Inventory System")
        self.root.geometry("1200x800")
        self.center_window()

        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.setup_menu()
        self.setup_sidebar()
        self.setup_content()
        self.setup_statusbar()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200
        window_height = 800
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Transaction", command=self.new_transaction)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)

        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_radiobutton(
            label="Light Theme", command=lambda: self.change_theme("light")
        )
        view_menu.add_radiobutton(
            label="Dark Theme", command=lambda: self.change_theme("dark")
        )

    def setup_sidebar(self):
        sidebar_width = self.config.get("sidebar_width", 240)
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=sidebar_width,
            **Styles.get_frame_style(self.theme, "secondary"),
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar.grid_propagate(False)

        # User Profile Section
        profile_frame = ctk.CTkFrame(self.sidebar, **Styles.get_frame_style(self.theme))
        profile_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            profile_frame,
            text=self.user.full_name,
            **Styles.get_text_style(self.theme, "subtitle"),
        ).pack(pady=5)

        # Navigation Buttons
        nav_frame = ctk.CTkFrame(self.sidebar, **Styles.get_frame_style(self.theme))
        nav_frame.pack(fill="x", padx=10, expand=True)

        nav_items = [
            ("Dashboard", "dashboard"),
            ("Products", "inventory"),
            ("Sales", "sales"),
            ("Reports", "reports"),
            ("Settings", "settings"),
        ]

        for text, section in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda s=section: self.switch_section(s),
                **Styles.get_button_style(self.theme, "secondary"),
            )
            btn.pack(fill="x", padx=5, pady=3)

        # Logout at bottom
        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            command=self.logout,
            **Styles.get_button_style(self.theme, "secondary"),
        ).pack(side="bottom", fill="x", padx=15, pady=10)

    def setup_content(self):
        self.content = ctk.CTkFrame(self.root, **Styles.get_frame_style(self.theme))
        self.content.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        self.current_section = None
        self.switch_section("dashboard")

    def setup_statusbar(self):
        self.statusbar = ctk.CTkFrame(
            self.root, height=25, **Styles.get_frame_style(self.theme, "secondary")
        )
        self.statusbar.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10)
        )

        self.status_label = ctk.CTkLabel(
            self.statusbar, text="Ready", **Styles.get_text_style(self.theme, "small")
        )
        self.status_label.pack(side="left", padx=10)

    def switch_section(self, section):
        if self.current_section:
            self.current_section.destroy()

        if section == "dashboard":
            from src.ui.dashboard_tab import DashboardTab

            self.current_section = DashboardTab(self.content, self.transaction_manager)
        elif section == "inventory":
            from src.ui.product_tab import ProductTab

            self.current_section = ProductTab(
                self.content, self.product_manager, self.logger
            )
        elif section == "sales":
            from src.ui.sales_tab import SalesTab

            self.current_section = SalesTab(
                self.content,
                self.product_manager,
                self.transaction_manager,
                self.logger,
            )
        elif section == "reports":
            from src.ui.reports_tab import ReportsTab

            self.current_section = ReportsTab(self.content, self.transaction_manager)
        elif section == "settings":
            from src.ui.settings_tab import SettingsTab

            self.current_section = SettingsTab(self.content, self.config)

        self.current_section.pack(fill="both", expand=True)

    def new_transaction(self):
        self.switch_section("sales")
        self.current_section.show_add_sale_dialog()

    def change_theme(self, mode):
        self.config.set("theme", mode)
        self.theme = AppTheme.setup_theme(mode)
        self.refresh_ui()

    def refresh_ui(self):
        # Recreate UI with new theme
        self.setup_window()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.logout_requested = True
            self.root.quit()

    def quit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def show_preferences(self):
        from src.ui.dialogs.preferences_dialog import PreferencesDialog

        PreferencesDialog(self.root, self.config)

    def run(self):
        self.root.mainloop()
