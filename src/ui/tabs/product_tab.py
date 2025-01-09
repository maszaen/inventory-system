from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QTableView,
    QMenu,
    QComboBox,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint
from bson import ObjectId
from src.style_config import Theme
from src.ui.dialogs.product_dialog import ProductDialog
from src.ui.models.product_table_model import ProductTableModel
from src.utils.pagination import PaginationWidget


class ProductTab(QWidget):
    def __init__(self, parent, product_manager, logger):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.user = parent.user
        self.cached_products = []
        self.filtered_products = []
        self.cached_products = self.product_manager.get_all_products()
        self.setup_ui()
        self.refresh_product_list()

    def setup_ui(self):
        colors = Theme.get_theme_colors()
        main_layout = QVBoxLayout(self)

        # Control Layout
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Search Label and Field
        self.search_label = QLabel("Search:")
        self.search_label.setStyleSheet("padding: 5px")
        control_layout.addWidget(self.search_label)

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Type product name...")
        self.search_entry.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
            }}
            """
        )
        self.search_entry.textChanged.connect(self.refresh_product_list)
        control_layout.addWidget(self.search_entry)

        self.sort_combobox = QComboBox()
        self.sort_combobox.addItems(
            [
                "Sort by: Date (Newest)",
                "Sort by: Date (Oldest)",
                "Sort by: Price (Highest)",
                "Sort by: Price (Lowest)",
                "Sort by: Name (A-Z)",
                "Sort by: Name (Z-A)",
                "Sort by: Stock (Highest)",
                "Sort by: Stock (Lowest)",
            ]
        )
        self.sort_combobox.setStyleSheet(
            f"""
            QComboBox {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                color: {colors['text_primary']};
                width: 240px;
            }}
            """
        )
        self.sort_combobox.currentIndexChanged.connect(self.refresh_product_list)
        control_layout.addWidget(self.sort_combobox)

        # Product Table
        self.product_table = QTableView()
        self.product_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.product_table.customContextMenuRequested.connect(self.show_context_menu)
        # self.product_table.setStyleSheet(
        #     f"""
        #     QTableView {{
        #         background-color: {colors['base']};
        #         color: {colors['text_primary']};
        #         padding: 0px;
        #         gridline-color: {colors['border']};
        #         font-size: 12px;
        #     }}

        #     QHeaderView::section {{
        #         background-color: {colors['base']};
        #         color: {colors['text_primary']};
        #     }}

        #     QTableView::item:selected {{
        #         background-color: {colors['background']};
        #         color: {colors['text_primary']};
        #     }}
        #     """
        # )
        main_layout.addWidget(self.product_table)

        self.pagination = PaginationWidget()
        self.pagination.pageChanged.connect(self.on_page_changed)
        main_layout.addWidget(self.pagination)

    def refresh_product_list(self):
        search_text = self.search_entry.text().strip().lower()

        self.cached_products = self.product_manager.get_all_products()

        self.filtered_products = [
            product
            for product in self.cached_products
            if search_text in product.name.lower()
        ]

        sort_option = self.sort_combobox.currentIndex()
        if sort_option == 0:
            self.filtered_products.sort(key=lambda p: p.created_at, reverse=True)
        elif sort_option == 1:
            self.filtered_products.sort(key=lambda p: p.created_at)
        elif sort_option == 2:
            self.filtered_products.sort(key=lambda p: p.price, reverse=True)
        elif sort_option == 3:
            self.filtered_products.sort(key=lambda p: p.price)
        elif sort_option == 4:
            self.filtered_products.sort(key=lambda p: p.name.lower())
        elif sort_option == 5:
            self.filtered_products.sort(key=lambda p: p.name.lower(), reverse=True)
        elif sort_option == 6:
            self.filtered_products.sort(key=lambda p: p.stock, reverse=True)
        elif sort_option == 7:
            self.filtered_products.sort(key=lambda p: p.stock)

        # Update pagination
        self.pagination.set_total_items(len(self.filtered_products))

        # Get page data
        self.update_current_page()

    def update_current_page(self):
        # Calculate slice indices
        start_idx = (self.pagination.current_page - 1) * self.pagination.items_per_page
        end_idx = start_idx + self.pagination.items_per_page

        # Get products for current page
        page_products = self.filtered_products[start_idx:end_idx]

        # Update model
        self.model = ProductTableModel(page_products, self)
        self.product_table.setModel(self.model)

    def on_page_changed(self):
        self.update_current_page()

    def show_add_product_dialog(self):
        dialog = ProductDialog(self, self.product_manager, self.logger)
        dialog.exec()
        self.refresh_product_list()

    def edit_selected_product(self):
        selected_row = self.product_table.selectionModel().selectedRows()[0].row()
        product_id = self.product_table.model().data(
            self.product_table.model().index(selected_row, 0)
        )
        product = self.product_manager.get_product_by_id(ObjectId(product_id))

        if product:
            dialog = ProductDialog(self, self.product_manager, self.logger, product)
            dialog.exec()
            self.refresh_product_list()

    def delete_selected_product(self):
        selected_row = self.product_table.selectionModel().selectedRows()[0].row()
        product_id = self.product_table.model().data(
            self.product_table.model().index(selected_row, 0)
        )
        product = self.product_manager.get_product_by_id(ObjectId(product_id))

        if product:
            response = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete {product.name}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if response == QMessageBox.Yes:
                if self.product_manager.delete_product(product._id):
                    self.logger.log_action(
                        f"Deleted product: {product.name} (ID: {product._id})"
                    )
                    self.refresh_product_list()
                    QMessageBox.information(
                        self, "Success", "Product deleted successfully!"
                    )
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete product")

    def show_context_menu(self, position: QPoint):
        colors = Theme.get_theme_colors()
        indexes = self.product_table.selectedIndexes()
        if indexes:
            menu = QMenu()
            menu.setStyleSheet(
                f"""
                QMenu {{
                    background-color: {colors['base']};
                    border: 1px solid {colors['border']};
                    border-radius: 6px;
                    padding: 0px;
                }}
                QMenu::item {{
                    padding: 4px 24px 4px 8px;
                    color: {colors['text_secondary']};
                    font-size: 13px;
                    border-radius: 6px;
                    margin: 4px 4px;
                }}
                QMenu::item:selected {{
                    background-color: {colors['border']};
                }}
                """
            )

            # Menggunakan simbol monochrome yang lebih profesional
            edit_action = QAction("Edit Product", self)
            delete_action = QAction("Delete Product", self)

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            action = menu.exec(self.product_table.viewport().mapToGlobal(position))

            if action == edit_action:
                self.edit_selected_product()
            elif action == delete_action:
                self.delete_selected_product()
