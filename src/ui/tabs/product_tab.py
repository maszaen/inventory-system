from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QTableView,
    QMenu,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint
from bson import ObjectId
from src.ui.dialogs.product_dialog import ProductDialog
from src.ui.models.product_table_model import ProductTableModel
from src.utils.pagination import PaginationWidget


class ProductTab(QWidget):
    def __init__(self, parent, product_manager, logger):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.cached_products = []
        self.filtered_products = []
        self.setup_ui()
        self.refresh_product_list()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Control Layout
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Add Product Button
        self.add_product_button = QPushButton("+ Add")
        self.add_product_button.clicked.connect(self.show_add_product_dialog)
        control_layout.addWidget(self.add_product_button)

        # Search Label and Field
        self.search_label = QLabel("Search:")
        control_layout.addWidget(self.search_label)

        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self.refresh_product_list)
        control_layout.addWidget(self.search_entry)

        # Product Table
        self.product_table = QTableView()
        self.product_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.product_table.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.product_table)

        self.pagination = PaginationWidget()
        self.pagination.pageChanged.connect(self.on_page_changed)
        main_layout.addWidget(self.pagination)

    def refresh_product_list(self):
        search_text = self.search_entry.text().strip().lower()

        # Update cache jika belum ada
        if not self.cached_products:
            self.cached_products = self.product_manager.get_all_products()

        # Filter dari cache
        self.filtered_products = [
            product
            for product in self.cached_products
            if search_text in product.name.lower()
        ]

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
        self.model = ProductTableModel(page_products)
        self.product_table.setModel(self.model)

    def on_page_changed(self, page, items_per_page):
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
        indexes = self.product_table.selectedIndexes()
        if indexes:
            menu = QMenu()
            menu.setStyleSheet(
                """
                QMenu {
                    background-color: #1e1e1e; 
                    border: 1px solid #3c3c3c; 
                    border-radius: 8px; 
                    color: white; 
                    font-size: 12px;
                }
                QMenu::item {
                    padding: 5px 25px;
                }
                QMenu::item:selected {
                    background-color: #3c3c3c;
                }
                """
            )

            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            action = menu.exec(self.product_table.viewport().mapToGlobal(position))

            if action == edit_action:
                self.edit_selected_product()
            elif action == delete_action:
                self.delete_selected_product()
