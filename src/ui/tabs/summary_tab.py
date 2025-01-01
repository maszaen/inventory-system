from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QDateEdit,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import QDate
from decimal import Decimal


class SummaryTab(QWidget):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Date selection layout
        date_layout = QHBoxLayout()
        layout.addLayout(date_layout)

        # Start Date
        date_layout.addWidget(QLabel("Start Date:"))
        self.start_date = QDateEdit(self)
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.start_date)

        # End Date
        date_layout.addWidget(QLabel("End Date:"))
        self.end_date = QDateEdit(self)
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        date_layout.addWidget(self.end_date)

        # Generate Summary Button
        self.generate_button = QPushButton("Generate Summary", self)
        self.generate_button.clicked.connect(self.generate_summary)
        layout.addWidget(self.generate_button)

        # Summary Text Area
        self.summary_text = QTextEdit(self)
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)

    def generate_summary(self):
        try:
            start_date = self.start_date.date().toPyDate()
            end_date = self.end_date.date().toPyDate()

            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

            # Get transactions in the date range
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )

            # Calculate total and summary per product
            total_amount = Decimal("0")
            product_summary = {}

            for transaction in transactions:
                total_amount += transaction.total

                if transaction.product_name not in product_summary:
                    product_summary[transaction.product_name] = {
                        "quantity": 0,
                        "total": Decimal("0"),
                    }

                product_summary[transaction.product_name][
                    "quantity"
                ] += transaction.quantity
                product_summary[transaction.product_name]["total"] += transaction.total

            # Generate summary text
            summary = f"Summary Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})\n"
            summary += "=" * 50 + "\n\n"
            summary += f"Total Transactions: {len(transactions)}\n"
            summary += f"Total Amount: Rp{total_amount:,.2f}\n\n"

            if product_summary:
                summary += "Sales Detail:\n"
                summary += "-" * 50 + "\n"

                for product_name, data in product_summary.items():
                    summary += f"\nProduct: {product_name}\n"
                    summary += f"Total Quantity Sold: {data['quantity']}\n"
                    summary += f"Total Amount: Rp{data['total']:,.2f}\n"
            else:
                summary += "No transactions found in this date range."

            # Update text widget
            self.summary_text.setPlainText(summary)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
