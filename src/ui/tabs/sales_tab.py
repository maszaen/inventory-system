from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTableView,
    QHeaderView,
    QMessageBox,
    QAbstractItemView,
    QMenu,
    QComboBox,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint
from bson import ObjectId
from src.style_config import Theme
from src.ui.dialogs.sale_dialog import SaleDialog
from src.ui.models.sales_table_model import SalesTableModel
from src.utils.pagination import PaginationWidget


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
        self.cached_transactions = []
        self.filtered_transactions = []
        self.setup_ui()
        self.refresh_sales_list()

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
        self.search_entry.textChanged.connect(self.refresh_sales_list)
        control_layout.addWidget(self.search_entry)

        self.sort_combobox = QComboBox()
        self.sort_combobox.addItems(
            [
                "Sort by: Transaction Date (Newest)",
                "Sort by: Transaction Date (Oldest)",
                "Sort by: Created (Newest)",
                "Sort by: Created (Oldest)",
                "Sort by: Amount (Highest)",
                "Sort by: Amount (Lowest)",
                "Sort by: Quantity (Highest)",
                "Sort by: Quantity (Lowest)",
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
        self.sort_combobox.currentIndexChanged.connect(self.refresh_sales_list)
        control_layout.addWidget(self.sort_combobox)

        # Sales Table
        self.sales_table = QTableView()
        self.sales_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sales_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sales_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sales_table.customContextMenuRequested.connect(self.show_context_menu)
        main_layout.addWidget(self.sales_table)

        self.pagination = PaginationWidget()
        self.pagination.pageChanged.connect(self.on_page_changed)
        main_layout.addWidget(self.pagination)

    def refresh_sales_list(self):
        search_text = self.search_entry.text().strip().lower()

        # Update cache jika perlu
        self.cached_transactions = self.transaction_manager.get_all_transactions()

        # Filter dari cache
        self.filtered_transactions = [
            transaction
            for transaction in self.cached_transactions
            if search_text in transaction.product_name.lower()
        ]

        sort_option = self.sort_combobox.currentIndex()
        if sort_option == 0:
            self.filtered_transactions.sort(key=lambda x: x.date, reverse=True)
        elif sort_option == 1:
            self.filtered_transactions.sort(key=lambda x: x.date)
        elif sort_option == 2:
            self.filtered_transactions.sort(key=lambda x: x.created_at, reverse=True)
        elif sort_option == 3:
            self.filtered_transactions.sort(key=lambda x: x.created_at)
        elif sort_option == 4:
            self.filtered_transactions.sort(key=lambda x: x.total, reverse=True)
        elif sort_option == 5:
            self.filtered_transactions.sort(key=lambda x: x.total)
        elif sort_option == 6:
            self.filtered_transactions.sort(key=lambda x: x.quantity, reverse=True)
        elif sort_option == 7:
            self.filtered_transactions.sort(key=lambda x: x.quantity)

        # Update pagination
        self.pagination.set_total_items(len(self.filtered_transactions))

        # Get page data
        self.update_current_page()

    def update_current_page(self):
        # Calculate slice indices
        start_idx = (self.pagination.current_page - 1) * self.pagination.items_per_page
        end_idx = start_idx + self.pagination.items_per_page

        # Get transactions for current page
        page_transactions = self.filtered_transactions[start_idx:end_idx]

        # Update model
        self.model = SalesTableModel(page_transactions)
        self.sales_table.setModel(self.model)

    def on_page_changed(self, page, items_per_page):
        self.update_current_page()

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
                    if self.refresh_callback:
                        self.refresh_callback()
                    QMessageBox.information(
                        self, "Success", "Sale deleted successfully!"
                    )
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete sale")

    def show_context_menu(self, position: QPoint):
        colors = Theme.get_theme_colors()
        indexes = self.sales_table.selectedIndexes()
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
            edit_action = QAction("Edit Sales", self)
            delete_action = QAction("Delete Sales", self)

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            action = menu.exec(self.sales_table.viewport().mapToGlobal(position))

            if action == edit_action:
                self.edit_selected_sale()
            elif action == delete_action:
                self.delete_selected_sale()
