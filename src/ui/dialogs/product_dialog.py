from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt
from decimal import Decimal
from src.models.product import Product
from src.style_config import Theme
from src.utils.logger import Logger


class ProductDialog(QDialog):
    def __init__(self, parent, product_manager, logger: Logger, product=None):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.product = product
        self.setup_dialog()

    def setup_dialog(self):
        btn = Theme.btn()
        form = Theme.form()
        self.setWindowTitle("Edit Product" if self.product else "Add New Product")
        self.setGeometry(0, 0, 300, 235)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()

        # Name field
        layout.addWidget(QLabel("Name:"))
        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet(form)
        if self.product:
            self.name_entry.setText(self.product.name)
        layout.addWidget(self.name_entry)

        # Price field
        layout.addWidget(QLabel("Price:"))
        self.price_entry = QLineEdit()
        self.price_entry.setStyleSheet(form)

        # Capital field
        if self.product:
            self.price_entry.setText(str(self.product.price))
        layout.addWidget(self.price_entry)

        layout.addWidget(QLabel("Capital:"))
        self.capital_entry = QLineEdit()
        self.capital_entry.setStyleSheet(form)

        if self.product:
            self.capital_entry.setText(str(self.product.capital))
        layout.addWidget(self.capital_entry)

        # Stock field
        layout.addWidget(QLabel("Stock:"))
        self.stock_entry = QLineEdit()
        self.stock_entry.setStyleSheet(form)
        if self.product:
            self.stock_entry.setText(str(self.product.stock))
        layout.addWidget(self.stock_entry)

        separator = QLabel()
        separator.setFrameShape(QLabel.HLine)
        separator.setFrameShadow(QLabel.Sunken)
        layout.addWidget(separator)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet(btn)
        save_button.clicked.connect(self.save_product)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.center_dialog()

    def center_dialog(self):
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def save_product(self):
        try:
            name = self.name_entry.text().strip()
            price = Decimal(self.price_entry.text())
            capital = Decimal(self.capital_entry.text())
            stock = int(self.stock_entry.text())

            if not name:
                raise ValueError("Product name is required!")
            if price <= 0:
                raise ValueError("Price must be positive")
            if capital <= 0:
                raise ValueError("Capital must be positive")
            if capital > price:
                raise ValueError("Capital cannot be greater than price")
            if stock < 0:
                raise ValueError("Stock cannot be negative")

            if self.product:
                self.product.name = name
                self.product.price = price
                self.product.capital = capital
                self.product.stock = stock
                if self.product_manager.update_product(self.product):
                    self.logger.log_action(
                        f"Updated product: {name} "
                        f"(ID: {self.product._id}, "
                        f"Price: {price}, Stock: {stock})"
                    )
                    QMessageBox.information(
                        self, "Success", "Product updated successfully!"
                    )
                else:
                    raise ValueError("Failed to update product")
            else:
                new_product = Product(
                    name=name, price=price, stock=stock, capital=capital
                )
                if self.product_manager.create_product(new_product):
                    self.logger.log_action(
                        f"Created new product: {name} "
                        f"(Capital: {new_product.capital}, "
                        f"(ID: {new_product._id}, "
                        f"Price: {price}, Stock: {stock})"
                    )
                    QMessageBox.information(
                        self, "Success", "Product created successfully!"
                    )
                else:
                    raise ValueError("Failed to create product")

            self.accept()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
