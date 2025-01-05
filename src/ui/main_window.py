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
    QPushButton,
)
from PySide6.QtCore import Qt
from src.config import Config
from src.models.user import UserManager
from src.utils.logger import Logger
from src.models.product import ProductManager
from src.models.transaction import TransactionManager
from src.ui.tabs.product_tab import ProductTab
from src.ui.tabs.sales_tab import SalesTab
from src.ui.tabs.summary_tab import SummaryTab
from src.ui.tabs.chart_tab import ChartTab
from src.utils.calculate_totals import calculate_totals
from PySide6.QtGui import QGuiApplication
from src.style_config import Theme
from src.utils.menu_bar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.logger = Logger()
        self.user_manager = UserManager()
        self.product_manager = ProductManager()
        self.transaction_manager = TransactionManager()

        self.is_dark_mode = Theme.detect_system_theme()

        self.setWindowTitle(Config.APP_TITLE)
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.center_window()

        self.main_layout = QHBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.menu_bar = MenuBar(self)
        self.setup_sidebar()
        self.setup_notebook()
        self.refresh_sidebar_totals()
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
        colors = Theme.get_theme_colors()
        action_button_style = f"""
            QPushButton {{
                background-color: {colors['card_bg']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 8px;
                color: {colors['text_primary']};
                text-align: left;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {colors['border']};
            }}
        """
        sidebar_widget = QWidget(self)
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_widget.setFixedWidth(300)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(8)
        sidebar_widget.setStyleSheet(
            f"QWidget {{ background-color: {colors['background']}; border: 1px solid {colors['border']}; border-radius: 5px; padding: 0px; }}"
        )

        if self.user:
            header_card = QFrame(self)
            header_card.setStyleSheet(
                f"QFrame {{ background-color: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 4px; }}"
            )
            header_layout = QVBoxLayout(header_card)
            header_layout.setSpacing(2)

            welcome_label = QLabel(f"Welcome,", self)
            welcome_label.setStyleSheet(
                f"border: 0px; color: {colors['text_secondary']}; font-size: 13px;"
            )

            user_name = QLabel(self.user.full_name, self)
            user_name.setStyleSheet(
                f"border: 0px; color: {colors['text_primary']}; font-size: 16px; font-weight: bold;"
            )

            role_label = QLabel(
                (
                    f"Role: {self.user.role.title()}"
                    if hasattr(self.user, "role")
                    else "Role: Staff"
                ),
                self,
            )
            role_label.setStyleSheet(
                f"border: 0px; color: {colors['accent']}; font-size: 13px;"
            )

            header_layout.addWidget(welcome_label)
            header_layout.addWidget(user_name)
            header_layout.addWidget(role_label)
            sidebar_layout.addWidget(header_card)

        # Statistics Cards Section
        stats_label = QLabel("Sales Overview", self)
        stats_label.setStyleSheet(
            f"color: {colors['text_secondary']}; font-size: 13px; margin-top: 8px; border: 0px;"
        )
        sidebar_layout.addWidget(stats_label)

        # Refresh Totals Button
        refresh_totals_btn = QPushButton("🔄 Refresh Summary")
        refresh_totals_btn.setStyleSheet(action_button_style)
        refresh_totals_btn.clicked.connect(self.refresh_sidebar_totals)
        sidebar_layout.addWidget(refresh_totals_btn)

        # Sales Statistics Cards
        self.totalSales = QLabel("Loading...", self)
        self.totalThisMonth = QLabel("Loading...", self)
        self.totalToday = QLabel("Loading...", self)

        labels = [
            ("Total Sales", self.totalSales, "📈"),
            ("This Month", self.totalThisMonth, "📅"),
            ("Today", self.totalToday, "💰"),
        ]

        for title, value_label, icon in labels:
            card = QFrame(self)
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(
                f"QFrame {{ background-color: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 4px; }}"
            )

            layout = QVBoxLayout(card)
            layout.setSpacing(4)

            header_layout = QHBoxLayout()
            title_label = QLabel(f"{icon} {title}", self)
            title_label.setStyleSheet(
                f"border: 0px; color: {colors['text_secondary']}; font-size: 13px;"
            )
            header_layout.addWidget(title_label)
            header_layout.addStretch()

            value_label.setStyleSheet(
                f"border: 0px; font-size: 18px; font-weight: bold; color: {colors['text_primary']};"
            )

            layout.addLayout(header_layout)
            layout.addWidget(value_label)
            sidebar_layout.addWidget(card)

        # Quick Actions Section
        actions_label = QLabel("Quick Actions", self)
        actions_label.setStyleSheet(
            f"color: {colors['text_secondary']}; font-size: 13px; margin-top: 8px; border: 0px;"
        )
        sidebar_layout.addWidget(actions_label)

        # Action Buttons

        add_product_btn = QPushButton("➕ Add New Product")
        add_product_btn.setStyleSheet(action_button_style)
        add_product_btn.clicked.connect(
            lambda: self.product_tab.show_add_product_dialog()
        )

        add_sale_btn = QPushButton("💵 New Sale")
        add_sale_btn.setStyleSheet(action_button_style)
        add_sale_btn.clicked.connect(lambda: self.sales_tab.show_add_sale_dialog())

        sidebar_layout.addWidget(add_product_btn)
        sidebar_layout.addWidget(add_sale_btn)

        # Version info at bottom
        version_label = QLabel(f"App Version {Config.APP_VERSION}", self)
        version_label.setStyleSheet("color: #888888; font-size: 12px; padding: 8px 0;")
        version_label.setAlignment(Qt.AlignCenter)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(version_label)

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

        self.product_tab = ProductTab(self, self.product_manager, self.logger)
        self.sales_tab = SalesTab(
            self,
            self.product_manager,
            self.transaction_manager,
            self.logger,
            refresh_callback=self.refresh_all,
        )
        self.summary_tab = SummaryTab(self, self.transaction_manager)
        self.chart_tab = ChartTab(self, self.transaction_manager)

        # Add tabs to the notebook
        notebook.addTab(self.product_tab, "Products")
        notebook.addTab(self.sales_tab, "Sales")
        notebook.addTab(self.summary_tab, "Summary")
        notebook.addTab(self.chart_tab, "Charts")

    def refresh_all(self):
        if hasattr(self, "product_tab"):
            self.product_tab.refresh_product_list()
        if hasattr(self, "sales_tab"):
            self.sales_tab.refresh_sales_list()
        if hasattr(self, "chart_tab"):  # Tambahkan refresh untuk chart
            self.chart_tab.update_chart()

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
