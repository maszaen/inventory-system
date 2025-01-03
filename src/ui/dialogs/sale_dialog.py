from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QDateEdit,
)
from PySide6.QtCore import Qt, QDate
from src.models.transaction import Transaction
from src.utils.logger import Logger


class SaleDialog(QDialog):
    def __init__(
        self,
        parent,
        product_manager,
        transaction_manager,
        logger: Logger,
        transaction=None,
        refresh_callback=None,
    ):
        super().__init__(parent)
        self.product_manager = product_manager
        self.transaction_manager = transaction_manager
        self.logger = logger
        self.transaction = transaction
        self.refresh_callback = refresh_callback
        self.setup_dialog()

    def setup_dialog(self):
        self.setWindowTitle("Edit Sale" if self.transaction else "Add New Sale")
        self.setGeometry(100, 100, 300, 280)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()

        # Date field
        layout.addWidget(QLabel("Date:"))
        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setStyleSheet(
            """
            QDateEdit {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #3c3c3c;
            }
            """
        )

        # Set default date
        if self.transaction:
            transaction_date = QDate(
                self.transaction.date.year,
                self.transaction.date.month,
                self.transaction.date.day,
            )
            self.date_picker.setDate(transaction_date)
        else:
            self.date_picker.setDate(QDate.currentDate())

        layout.addWidget(self.date_picker)

        # Product field
        layout.addWidget(QLabel("Product:"))
        self.products = self.product_manager.get_all_products()
        product_names = [p.name for p in self.products]

        self.product_combo = QComboBox(self)
        self.product_combo.addItems(product_names)
        self.product_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #3c3c3c;
            }
            """
        )
        if self.transaction:
            self.product_combo.setCurrentText(self.transaction.product_name)
        layout.addWidget(self.product_combo)

        # Stock info
        self.stock_info = QLabel()
        self.stock_info.setStyleSheet(
            "color: #888888; font-size: 12px; margin-top: -5px;"
        )
        layout.addWidget(self.stock_info)

        # Update stock info when product changes
        self.product_combo.currentTextChanged.connect(self.update_stock_info)
        self.update_stock_info(self.product_combo.currentText())

        # Quantity field
        quantity_label = QLabel("Quantity:")
        layout.addWidget(quantity_label)

        self.quantity_entry = QLineEdit(self)
        self.quantity_entry.setStyleSheet(
            """
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            """
        )
        if self.transaction:
            self.quantity_entry.setText(str(self.transaction.quantity))
        layout.addWidget(self.quantity_entry)

        # Save button
        save_button = QPushButton("Save", self)
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            """
        )
        save_button.clicked.connect(self.save_sale)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.center_dialog()

    def center_dialog(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def save_sale(self):
        try:
            sale_date = self.date_picker.date().toPython()
            product_name = self.product_combo.currentText()
            quantity = int(self.quantity_entry.text())

            # Validate input
            if not product_name:
                raise ValueError("Please select a product")
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            # Find selected product
            selected_product = None
            for product in self.products:
                if product.name == product_name:
                    selected_product = product
                    break

            if not selected_product:
                raise ValueError("Product not found")

            # Calculate total
            total = selected_product.price * quantity

            if self.transaction:
                # Mode Edit
                old_product = self.product_manager.get_product_by_id(
                    self.transaction.product_id
                )

                # Cek apakah produk yang dipilih sama dengan produk lama
                if old_product._id == selected_product._id:
                    # Produk sama, cek apakah stok mencukupi
                    available_stock = selected_product.stock + self.transaction.quantity
                    if quantity > available_stock:
                        raise ValueError(
                            f"Insufficient stock!\n"
                            f"Requested: {quantity}\n"
                            f"Available: {available_stock}"
                        )

                    # Update stok
                    selected_product.stock = available_stock - quantity
                else:
                    # Produk berbeda
                    # Kembalikan stok produk lama
                    old_product.stock += self.transaction.quantity
                    if not self.product_manager.update_product(old_product):
                        raise ValueError("Failed to restore old product stock")

                    # Cek stok produk baru
                    if quantity > selected_product.stock:
                        raise ValueError(
                            f"Insufficient stock!\n"
                            f"Requested: {quantity}\n"
                            f"Available: {selected_product.stock}"
                        )

                    # Update stok produk baru
                    selected_product.stock -= quantity

                # Update transaksi
                self.transaction.date = sale_date
                self.transaction.product_id = selected_product._id
                self.transaction.product_name = product_name
                self.transaction.quantity = quantity
                self.transaction.total = total

                # Simpan perubahan
                if not self.transaction_manager.update_transaction(self.transaction):
                    raise ValueError("Failed to update transaction")

                if not self.product_manager.update_product(selected_product):
                    raise ValueError("Failed to update product stock")

                self.logger.log_action(
                    f"Sale updated:\n"
                    f"  Transaction ID: {self.transaction._id}\n"
                    f"  Product: {product_name}\n"
                    f"  Quantity: {quantity}\n"
                    f"  Total: {total}\n"
                    f"  Stock: {available_stock} → {selected_product.stock}"
                )

            else:
                # Mode Add New
                if quantity > selected_product.stock:
                    raise ValueError(
                        f"Insufficient stock!\n"
                        f"Requested: {quantity}\n"
                        f"Available: {selected_product.stock}"
                    )

                transaction = Transaction(
                    product_id=selected_product._id,
                    product_name=product_name,
                    quantity=quantity,
                    total=total,
                    date=sale_date,
                )

                old_stock = selected_product.stock
                selected_product.stock -= quantity

                if not self.transaction_manager.create_transaction(transaction):
                    raise ValueError("Failed to create transaction")

                if not self.product_manager.update_product(selected_product):
                    self.transaction_manager.delete_transaction(transaction._id)
                    raise ValueError("Failed to update product stock")

                self.logger.log_action(
                    f"New sale recorded:\n"
                    f"  Product: {product_name}\n"
                    f"  Quantity: {quantity}\n"
                    f"  Total: {total}\n"
                    f"  Stock: {old_stock} → {selected_product.stock}"
                )

            if self.refresh_callback:
                self.refresh_callback()

            QMessageBox.information(
                self,
                "Success",
                f"{'Sale updated' if self.transaction else 'Sale recorded'} successfully!\n\n"
                f"Product: {product_name}\n"
                f"Quantity: {quantity}\n"
                f"Total: Rp{total:,.2f}",
            )

            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_stock_info(self, product_name):
        selected_product = next(
            (p for p in self.products if p.name == product_name), None
        )

        if selected_product:
            current_stock = selected_product.stock
            if self.transaction and self.transaction.product_name == product_name:
                # Jika dalam mode edit dan produk sama, tambahkan stok yang sedang diedit
                current_stock += self.transaction.quantity

            if current_stock > 0:
                self.stock_info.setText(f"Available stock: {current_stock}")
                self.stock_info.setStyleSheet(
                    "color: #22c55e; font-size: 12px; margin-top: -5px;"
                )  # Hijau untuk stok tersedia
            else:
                self.stock_info.setText(f"Out of stock!")
                self.stock_info.setStyleSheet(
                    "color: #ef4444; font-size: 12px; margin-top: -5px;"
                )  # Merah untuk stok habis
        else:
            self.stock_info.setText("Product not found")
            self.stock_info.setStyleSheet(
                "color: #888888; font-size: 12px; margin-top: -5px;"
            )
