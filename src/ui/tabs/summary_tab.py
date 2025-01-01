from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QDateEdit,
    QHBoxLayout,
    QMessageBox,
    QFrame,
    QScrollArea,
    QFileDialog,
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont
from decimal import Decimal
from datetime import datetime, timedelta
from collections import defaultdict

import xlsxwriter


class SummaryTab(QWidget):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Date Selection Card
        date_card = QFrame(self)
        date_card.setStyleSheet(
            "QFrame { background-color: #2d2d2d; border: 1px solid #3c3c3c; border-radius: 8px; padding: 15px; }"
        )
        date_layout = QHBoxLayout(date_card)

        # Start Date
        start_date_widget = QFrame()
        start_date_widget.setStyleSheet("border: none;")
        start_date_layout = QVBoxLayout(start_date_widget)
        start_date_label = QLabel("Start Date")
        start_date_label.setStyleSheet("color: #888888; font-size: 13px;")
        self.start_date = QDateEdit(self)
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setStyleSheet(
            """
            QDateEdit {
                background-color: #1e1e1e;
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
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(self.start_date)

        # End Date
        end_date_widget = QFrame()
        end_date_widget.setStyleSheet("border: none;")
        end_date_layout = QVBoxLayout(end_date_widget)
        end_date_label = QLabel("End Date")
        end_date_label.setStyleSheet("color: #888888; font-size: 13px;")
        self.end_date = QDateEdit(self)
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(
            """
            QDateEdit {
                background-color: #1e1e1e;
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
        end_date_layout.addWidget(end_date_label)
        end_date_layout.addWidget(self.end_date)

        # Quick Date Buttons
        quick_dates_widget = QFrame()
        quick_dates_widget.setStyleSheet("border: none;")
        quick_dates_layout = QVBoxLayout(quick_dates_widget)
        quick_dates_label = QLabel("Quick Select")
        quick_dates_label.setStyleSheet("color: #888888; font-size: 13px;")

        quick_dates_buttons = QHBoxLayout()

        button_style = """
            QPushButton {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 5px 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """

        today_btn = QPushButton("Today")
        today_btn.setStyleSheet(button_style)
        today_btn.clicked.connect(lambda: self.set_quick_date("today"))

        week_btn = QPushButton("This Week")
        week_btn.setStyleSheet(button_style)
        week_btn.clicked.connect(lambda: self.set_quick_date("week"))

        month_btn = QPushButton("This Month")
        month_btn.setStyleSheet(button_style)
        month_btn.clicked.connect(lambda: self.set_quick_date("month"))

        quick_dates_buttons.addWidget(today_btn)
        quick_dates_buttons.addWidget(week_btn)
        quick_dates_buttons.addWidget(month_btn)

        quick_dates_layout.addWidget(quick_dates_label)
        quick_dates_layout.addLayout(quick_dates_buttons)

        # Add widgets to date layout
        date_layout.addWidget(start_date_widget)
        date_layout.addWidget(end_date_widget)
        date_layout.addWidget(quick_dates_widget)

        button_layout = QHBoxLayout()

        # Generate Button
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.setStyleSheet(
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
        self.generate_button.clicked.connect(self.generate_summary)

        # Export Button
        self.export_button = QPushButton("Export to Excel")
        self.export_button.setStyleSheet(
            """
            QPushButton {
                background-color: #059669;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #047857;
            }
            """
        )
        self.export_button.clicked.connect(self.export_to_excel)

        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.export_button)

        # Scroll Area for Summary
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        self.summary_text = QTextEdit(scroll_content)
        self.summary_text.setReadOnly(True)
        scroll_layout.addWidget(self.summary_text)
        scroll_area.setWidget(scroll_content)

        # Add all to main layout
        main_layout.addWidget(date_card)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(scroll_area)

    def set_quick_date(self, period):
        end_date = QDate.currentDate()
        self.end_date.setDate(end_date)

        if period == "today":
            self.start_date.setDate(end_date)
        elif period == "week":
            self.start_date.setDate(end_date.addDays(-7))
        elif period == "month":
            self.start_date.setDate(end_date.addMonths(-1))

    def calculate_trends(self, transactions):
        """Calculate sales trends"""
        if not transactions:
            return {}

        # Sort transactions by date
        sorted_transactions = sorted(transactions, key=lambda x: x.date)

        # Daily sales trend
        daily_sales = defaultdict(Decimal)
        for trans in transactions:
            date_str = trans.date.strftime("%Y-%m-%d")
            daily_sales[date_str] += trans.total

        # Find peak sales day
        peak_day = max(daily_sales.items(), key=lambda x: x[1])

        # Calculate growth rate
        if len(daily_sales) >= 2:
            first_day_sales = list(daily_sales.values())[0]
            last_day_sales = list(daily_sales.values())[-1]
            if first_day_sales > 0:
                growth_rate = (
                    (last_day_sales - first_day_sales) / first_day_sales
                ) * 100
            else:
                growth_rate = 0
        else:
            growth_rate = 0

        # Most popular products
        product_sales = defaultdict(int)
        for trans in transactions:
            product_sales[trans.product_name] += trans.quantity

        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        return {
            "peak_day": {"date": peak_day[0], "amount": peak_day[1]},
            "growth_rate": growth_rate,
            "top_products": top_products,
            "daily_sales": dict(daily_sales),
        }

    def export_to_excel(self):
        try:
            # Get date range
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()

            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

            # Get transactions
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )

            if not transactions:
                QMessageBox.warning(
                    self, "No Data", "No transactions found in the selected date range."
                )
                return

            # Ask for save location
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Excel File",
                f"sales_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx",
                "Excel Files (*.xlsx)",
            )

            if not file_name:
                return  # User cancelled

            # Create workbook
            workbook = xlsxwriter.Workbook(file_name)
            worksheet = workbook.add_worksheet("Sales Report")

            # Set column widths
            worksheet.set_column("A:A", 12)  # Date
            worksheet.set_column("B:B", 30)  # Product
            worksheet.set_column("C:C", 10)  # Quantity
            worksheet.set_column("D:D", 15)  # Total

            # Add headers
            headers = ["Date", "Product", "Quantity", "Total (Rp)"]
            header_format = workbook.add_format(
                {
                    "bold": True,
                    "bg_color": "#2563eb",
                    "font_color": "white",
                    "border": 1,
                }
            )

            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)

            # Add data
            date_format = workbook.add_format({"num_format": "yyyy-mm-dd"})
            number_format = workbook.add_format({"num_format": "#,##0"})
            currency_format = workbook.add_format({"num_format": "#,##0.00"})

            for row, transaction in enumerate(transactions, start=1):
                worksheet.write(row, 0, transaction.date, date_format)
                worksheet.write(row, 1, transaction.product_name)
                worksheet.write(row, 2, transaction.quantity, number_format)
                worksheet.write(row, 3, float(transaction.total), currency_format)

            # Add summary
            summary_row = len(transactions) + 2
            total_sales = sum(float(t.total) for t in transactions)
            total_quantity = sum(t.quantity for t in transactions)

            bold_format = workbook.add_format({"bold": True})

            worksheet.write(summary_row, 1, "Total", bold_format)
            worksheet.write(summary_row, 2, total_quantity, number_format)
            worksheet.write(summary_row, 3, total_sales, currency_format)

            workbook.close()

            QMessageBox.information(
                self, "Success", f"Report exported successfully to:\n{file_name}"
            )

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An error occurred while exporting: {str(e)}"
            )

    def generate_summary(self):
        try:
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()

            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

            transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )

            # Basic calculations
            total_amount = sum(t.total for t in transactions)
            product_summary = defaultdict(
                lambda: {"quantity": 0, "total": Decimal("0")}
            )

            for transaction in transactions:
                prod_data = product_summary[transaction.product_name]
                prod_data["quantity"] += transaction.quantity
                prod_data["total"] += transaction.total

            # Calculate advanced metrics
            trends = self.calculate_trends(transactions)

            # Generate formatted summary
            summary = self.format_summary_report(
                start_date,
                end_date,
                transactions,
                total_amount,
                product_summary,
                trends,
            )

            # Update text widget with custom formatting
            self.summary_text.setHtml(summary)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def format_summary_report(
        self, start_date, end_date, transactions, total_amount, product_summary, trends
    ):
        """Format the summary report with HTML styling"""

        if not transactions:
            # Return early with "No Data" message if no transactions
            return """
            <style>
                body { font-family: Arial, sans-serif; }
                .header { color: #ffffff; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
                .message { color: #888888; font-size: 14px; text-align: center; margin-top: 20px; }
            </style>
            
            <div class="header">Summary Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})</div>
            <div class="message">No transactions found for this period.</div>
            """

        html = f"""
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .header {{ color: #ffffff; font-size: 18px; font-weight: bold; margin-bottom: 15px; }}
            .section {{ margin-bottom: 20px; }}
            .subheader {{ color: #888888; font-size: 14px; margin: 10px 0; }}
            .data {{ color: #ffffff; margin-left: 20px; }}
            .highlight {{ color: #2563eb; font-weight: bold; }}
        </style>
        
        <div class="header">Summary Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})</div>
        
        <div class="section">
            <div class="subheader">Overview</div>
            <div class="data">
                Total Transactions: <span class="highlight">{len(transactions)}</span><br>
                Total Revenue: <span class="highlight">Rp{total_amount:,.2f}</span><br>
                Average Transaction Value: <span class="highlight">Rp{(total_amount / len(transactions) if transactions else 0):,.2f}</span>
            </div>
        </div>
        """

        # Hanya tampilkan top products jika ada data
        if trends.get("top_products"):
            html += """
            <div class="section">
                <div class="subheader">Top Selling Products</div>
                <div class="data">
            """
            for product, quantity in trends["top_products"]:
                html += (
                    f"{product}: <span class='highlight'>{quantity}</span> units<br>"
                )
            html += "</div></div>"

        # Hanya tampilkan sales analysis jika ada peak day
        if trends.get("peak_day", {}).get("date"):
            html += f"""
            <div class="section">
                <div class="subheader">Sales Analysis</div>
                <div class="data">
                    Peak Sales Day: <span class="highlight">{trends['peak_day']['date']}</span><br>
                    Peak Day Revenue: <span class="highlight">Rp{trends['peak_day']['amount']:,.2f}</span><br>
                    Growth Rate: <span class="highlight">{trends['growth_rate']:.1f}%</span>
                </div>
            </div>
            """

        # Hanya tampilkan product summary jika ada data
        if product_summary:
            html += """
            <div class="section">
                <div class="subheader">Detailed Product Summary</div>
                <div class="data">
            """
            for product_name, data in product_summary.items():
                if data["quantity"] > 0:  # Hanya tampilkan produk yang terjual
                    html += f"""
                    <br><b>{product_name}</b><br>
                    Quantity Sold: <span class="highlight">{data['quantity']}</span><br>
                    Revenue: <span class="highlight">Rp{data['total']:,.2f}</span><br>
                    Average Price: <span class="highlight">Rp{(data['total'] / data['quantity'] if data['quantity'] else 0):,.2f}</span><br>
                    """
            html += "</div></div>"

        return html
