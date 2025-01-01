from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QFrame,
)
from PySide6.QtCore import Qt
from src.config import Config
from src.utils.logger import Logger
from src.models.product import ProductManager
from src.models.transaction import TransactionManager
from src.ui.tabs.product_tab import ProductTab
from src.ui.tabs.sales_tab import SalesTab
from src.ui.tabs.summary_tab import SummaryTab
from src.utils.calculate_totals import calculate_totals

from PySide6.QtGui import QGuiApplication


class MainWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.logger = Logger()
        self.product_manager = ProductManager()
        self.transaction_manager = TransactionManager()

        self.setWindowTitle(Config.APP_TITLE)
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.center_window()

        self.main_layout = QHBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setup_sidebar()
        self.setup_notebook()
        self.refresh_all()

        if self.user:
            self.setWindowTitle(f"{Config.APP_TITLE} - {self.user.full_name}")

    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            center = screen_geometry.center()
            frame_geometry = self.frameGeometry()
            frame_geometry.moveCenter(center)
            self.move(frame_geometry.topLeft())

    def setup_sidebar(self):
        sidebar_widget = QWidget(self)
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_widget.setFixedWidth(300)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(8)
        sidebar_widget.setStyleSheet(
            "QWidget { background-color: #1e1e1e; border: 1px solid #3c3c3c; border-radius: 5px; padding: 0px; }"
        )

        # Create cards
        self.totalSales = QLabel("Loading...", self)
        self.totalThisMonth = QLabel("Loading...", self)
        self.totalToday = QLabel("Loading...", self)
        labels = [
            ("Total Sales", self.totalSales),
            ("This Month", self.totalThisMonth),
            ("Today", self.totalToday),
        ]

        for title, value_label in labels:
            card = QFrame(self)
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(
                "QFrame { background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 8px; padding: 0px;}"
            )

            layout = QVBoxLayout(card)
            layout.setSpacing(4)

            title_label = QLabel(title, self)
            title_label.setStyleSheet("border: 0px; color: #888888; font-size: 13px;")
            value_label.setStyleSheet(
                "border: 0px; font-size: 18px; font-weight: bold; color: #ffffff;"
            )

            layout.addWidget(title_label)
            layout.addWidget(value_label)
            sidebar_layout.addWidget(card)

        sidebar_layout.addStretch()
        self.main_layout.addWidget(sidebar_widget)

        # Refresh totals
        self.refresh_sidebar_totals()

    def refresh_sidebar_totals(self):
        transactions = self.transaction_manager.get_all_transactions()
        total_all_sales, total_this_month, total_today = calculate_totals(transactions)

        self.totalSales.setText(f"Rp{total_all_sales:,.2f}")
        self.totalThisMonth.setText(f"Rp{total_this_month:,.2f}")
        self.totalToday.setText(f"Rp{total_today:,.2f}")

    def setup_notebook(self):
        notebook = QTabWidget(self)
        self.main_layout.addWidget(notebook)

        # Initialize tabs
        self.product_tab = ProductTab(self, self.product_manager, self.logger)
        self.sales_tab = SalesTab(
            self,
            self.product_manager,
            self.transaction_manager,
            self.logger,
            refresh_callback=self.refresh_all,
        )
        self.summary_tab = SummaryTab(self, self.transaction_manager)

        # Add tabs to the notebook
        notebook.addTab(self.product_tab, "Products")
        notebook.addTab(self.sales_tab, "Sales")
        notebook.addTab(self.summary_tab, "Summary")

    def refresh_all(self):
        if hasattr(self, "product_tab"):
            self.product_tab.refresh_product_list()
        if hasattr(self, "sales_tab"):
            self.sales_tab.refresh_sales_list()

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.close()
