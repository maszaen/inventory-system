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
        colors = Theme.get_theme_colors()
        self.setWindowTitle("Edit Product" if self.product else "Add New Product")
        self.setGeometry(0, 0, 300, 235)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()

        # Name field
        layout.addWidget(QLabel("Name:"))
        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet(
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
        if self.product:
            self.name_entry.setText(self.product.name)
        layout.addWidget(self.name_entry)

        # Price field
        layout.addWidget(QLabel("Price:"))
        self.price_entry = QLineEdit()
        self.price_entry.setStyleSheet(
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

        if self.product:
            self.price_entry.setText(str(self.product.price))
        layout.addWidget(self.price_entry)

        # Stock field
        layout.addWidget(QLabel("Stock:"))
        self.stock_entry = QLineEdit()
        self.stock_entry.setStyleSheet(
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
        if self.product:
            self.stock_entry.setText(str(self.product.stock))
        layout.addWidget(self.stock_entry)

        separator = QLabel()
        separator.setFrameShape(QLabel.HLine)
        separator.setFrameShadow(QLabel.Sunken)
        layout.addWidget(separator)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            """
        )
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
            stock = int(self.stock_entry.text())

            if not name:
                raise ValueError("Product name is required!")
            if price <= 0:
                raise ValueError("Price must be positive")
            if stock < 0:
                raise ValueError("Stock cannot be negative")

            if self.product:
                # Update existing product
                self.product.name = name
                self.product.price = price
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
                # Create new product
                new_product = Product(name=name, price=price, stock=stock)
                if self.product_manager.create_product(new_product):
                    self.logger.log_action(
                        f"Created new product: {name} "
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
