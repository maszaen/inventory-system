from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QHeaderView,
    QMessageBox,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from bson import ObjectId
from src.ui.dialogs.sale_dialog import SaleDialog


from PySide6.QtWidgets import (
    QTableView,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
)

from src.ui.models.sales_table_model import SalesTableModel


class SalesTab(QWidget):
    def __init__(
        self,
        parent,
        product_manager,
        transaction_manager,
        logger,
        refresh_callback=None,
    ):
        super().__init__(parent)
        self.product_manager = product_manager
        self.transaction_manager = transaction_manager
        self.logger = logger
        self.refresh_callback = refresh_callback
        self.setup_ui()
        self.refresh_sales_list()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Control Layout
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # Add Sale Button
        self.add_sale_button = QPushButton("Add Sale")
        self.add_sale_button.clicked.connect(self.show_add_sale_dialog)
        control_layout.addWidget(self.add_sale_button)

        # Search Label and Field
        self.search_label = QLabel("Search:")
        control_layout.addWidget(self.search_label)

        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self.refresh_sales_list)
        control_layout.addWidget(self.search_entry)

        # Delete and Edit Buttons
        self.delete_button = QPushButton("Delete")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_sale)
        control_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_sale)
        control_layout.addWidget(self.edit_button)

        # Sales Table
        self.sales_table = QTableView()
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sales_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sales_table.horizontalHeader().setStretchLastSection(
            True
        )  # Make the last section stretch
        self.sales_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )  # Stretch all sections
        main_layout.addWidget(self.sales_table)

    def refresh_sales_list(self):
        search_text = self.search_entry.text().strip().lower()

        transactions = self.transaction_manager.get_all_transactions()
        filtered_transactions = [
            transaction
            for transaction in transactions
            if search_text in transaction.product_name.lower()
        ]

        self.model = SalesTableModel(filtered_transactions)
        self.sales_table.setModel(self.model)

    def show_add_sale_dialog(self):
        dialog = SaleDialog(
            self,
            self.product_manager,
            self.transaction_manager,
            self.logger,
            refresh_callback=self.refresh_callback,
        )
        dialog.exec()
        self.refresh_sales_list()

    def edit_selected_sale(self):
        selected_row = self.sales_table.selectionModel().selectedRows()[0].row()
        transaction_id = self.sales_table.model().data(
            self.sales_table.model().index(selected_row, 0)
        )
        transaction = self.transaction_manager.get_transaction_by_id(
            ObjectId(transaction_id)
        )

        if transaction:
            dialog = SaleDialog(
                self,
                self.product_manager,
                self.transaction_manager,
                self.logger,
                transaction,
                refresh_callback=self.refresh_callback,
            )
            dialog.exec()
            self.refresh_sales_list()

    def delete_selected_sale(self):
        selected_row = self.sales_table.selectionModel().selectedRows()[0].row()
        transaction_id = self.sales_table.model().data(
            self.sales_table.model().index(selected_row, 0)
        )
        transaction = self.transaction_manager.get_transaction_by_id(
            ObjectId(transaction_id)
        )

        if transaction:
            response = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete this sale?\nTransaction ID: {transaction._id}",
                QMessageBox.Yes | QMessageBox.No,
            )
            if response == QMessageBox.Yes:
                # Restore product stock
                product = self.product_manager.get_product_by_id(transaction.product_id)
                if product:
                    product.stock += transaction.quantity
                    self.product_manager.update_product(product)

                if self.transaction_manager.delete_transaction(transaction._id):
                    self.logger.log_action(
                        f"Deleted sale: {transaction._id} - Product: {transaction.product_name}"
                    )
                    self.refresh_sales_list()
                    QMessageBox.information(
                        self, "Success", "Sale deleted successfully!"
                    )
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete sale")
