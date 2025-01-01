from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QDialogButtonBox,
    QDialog,
    QTableWidgetItem,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QTableView,
)
from bson import ObjectId
from src.ui.dialogs.product_dialog import ProductDialog
from src.ui.models.product_table_model import ProductTableModel


class ProductTab(QWidget):
    def __init__(self, parent, product_manager, logger):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.setup_ui()
        self.refresh_product_list()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Control Layout
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Add Product Button
        self.add_product_button = QPushButton("Add Product")
        self.add_product_button.clicked.connect(self.show_add_product_dialog)
        control_layout.addWidget(self.add_product_button)

        # Search Label and Field
        self.search_label = QLabel("Search:")
        control_layout.addWidget(self.search_label)

        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self.refresh_product_list)
        control_layout.addWidget(self.search_entry)

        # Delete and Edit Buttons
        self.delete_button = QPushButton("Delete")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_product)
        control_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_product)
        control_layout.addWidget(self.edit_button)

        # Product Table
        self.product_table = QTableView()
        self.product_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.product_table)

    def refresh_product_list(self):
        search_text = self.search_entry.text().strip().lower()

        products = self.product_manager.get_all_products()
        filtered_products = [
            product for product in products if search_text in product.name.lower()
        ]

        self.model = ProductTableModel(filtered_products)
        self.product_table.setModel(self.model)

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
