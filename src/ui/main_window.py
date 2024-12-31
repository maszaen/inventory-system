import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.config import Config
from src.utils.logger import Logger
from src.models.product import ProductManager
from src.models.transaction import TransactionManager
from src.ui.tabs.product_tab import ProductTab
from src.ui.tabs.sales_tab import SalesTab
from src.ui.tabs.summary_tab import SummaryTab
from src.style_config import (
    MENU_STYLE,
    SUBMENU_STYLE,
    TREEVIEW_STYLE,
    TREEVIEW_HEADING_STYLE,
    BUTTON_STYLE,
    LABEL_STYLE,
    FRAME_STYLE,
)


class MainWindow:
    def __init__(self, root: tk.Tk, user=None):
        self.root = root
        self.user = user
        self.logger = Logger()
        self.product_manager = ProductManager()
        self.transaction_manager = TransactionManager()

        self.setup_window()
        self.setup_style()
        self.setup_sidebar()
        self.setup_notebook()
        self.refresh_all()

        if self.user:
            self.root.title(f"{Config.APP_TITLE} - {self.user.full_name}")

    def setup_window(self):
        self.root.title(Config.APP_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        x = (self.root.winfo_screenwidth() - Config.WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - Config.WINDOW_HEIGHT) // 2
        self.root.geometry(f"+{x}+{y}")

    #     self.setup_menu()

    # def setup_menu(self):
    #     menubar = tk.Menu(self.root)
    #     self.root.config(menu=menubar)

    #     # User menu
    #     user_menu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="User", menu=user_menu)

    #     # Add user-related menu items
    #     user_menu.add_command(
    #         label=f"Logged in as: {self.user.full_name if self.user else 'Guest'}"
    #     )
    #     user_menu.add_separator()
    #     user_menu.add_command(label="Logout", command=self.logout)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()

    def setup_style(self):
        style = ttk.Style()
        style.configure(
            "Custom.Treeview.Heading",
            font=("Arial", 10, "bold"),
        )
        style.configure(
            "Custom.Treeview",
            font=("Arial", 11),
            rowheight=25,
            padding=(10, 0),
        )
        style.configure("TFrame", background="whitesmoke")
        style.configure(
            "TButton",
            background="whitesmoke",
            font=("Arial", 10),
            padding=1,
        )
        style.configure(
            "TLabel",
            background="whitesmoke",
            font=("Arial", 10),
            padding=1,
        )

    def setup_sidebar(self):
        self.sidebar = ttk.Frame(self.root, width=250, padding=(20, 0), relief="flat")
        self.sidebar.pack(side="left", fill="y")

        # Add sidebar content
        ttk.Label(self.sidebar, text="Sidebar", style="TLabel").pack(pady=10)
        ttk.Button(self.sidebar, text="Button 1", style="TButton").pack(pady=5)
        ttk.Button(self.sidebar, text="Button 2", style="TButton").pack(pady=5)

    def setup_style(self):
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", **TREEVIEW_HEADING_STYLE)
        style.configure("Custom.Treeview", **TREEVIEW_STYLE)
        style.configure("TFrame", **FRAME_STYLE)
        style.configure("TButton", **BUTTON_STYLE)
        style.configure("TLabel", **LABEL_STYLE)

    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Initialize tabs
        self.product_tab = ProductTab(self.notebook, self.product_manager, self.logger)
        self.sales_tab = SalesTab(
            self.notebook,
            self.product_manager,
            self.transaction_manager,
            self.logger,
            refresh_callback=self.refresh_all,
        )
        self.summary_tab = SummaryTab(self.notebook, self.transaction_manager)

        # Add tabs to notebook
        self.notebook.add(self.product_tab, text="Products")
        self.notebook.add(self.sales_tab, text="Sales")
        self.notebook.add(self.summary_tab, text="Summary")

    def refresh_all(self):
        if hasattr(self, "product_tab"):
            self.product_tab.refresh_product_list()
        if hasattr(self, "sales_tab"):
            self.sales_tab.refresh_sales_list()
