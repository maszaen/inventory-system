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
from src.style_config import Theme
from PySide6.QtCore import QDate
from decimal import Decimal
from collections import defaultdict
import xlsxwriter


class SummaryTab(QWidget):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()

    def setup_ui(self):
        colors = Theme.get_theme_colors()
        date = Theme.datepick()
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)

        date_card = QFrame(self)
        date_card.setStyleSheet(
            f"QFrame {{ background-color: {colors['card_bg']}; border: 1px solid {colors['border']}; border-radius: 8px; padding: 2px; }}"
        )
        date_container = QVBoxLayout(date_card)

        date_layout = QVBoxLayout()

        date_container.addLayout(date_layout)

        date_picker_layout = QHBoxLayout()

        # Start Date
        start_date_widget = QFrame()
        start_date_widget.setStyleSheet("border: none;")
        start_date_layout = QVBoxLayout(start_date_widget)
        start_date_label = QLabel("Start Date")
        start_date_label.setStyleSheet(
            f"color: {colors['text_secondary']}; font-size: 13px;"
        )
        self.start_date = QDateEdit(self)
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setStyleSheet(date)
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(self.start_date)

        # End Date
        end_date_widget = QFrame()
        end_date_widget.setStyleSheet("border: none;")
        end_date_layout = QVBoxLayout(end_date_widget)
        end_date_label = QLabel("End Date")
        end_date_label.setStyleSheet(
            f"color: {colors['text_secondary']}; font-size: 13px;"
        )
        self.end_date = QDateEdit(self)
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(date)
        end_date_layout.addWidget(end_date_label)
        end_date_layout.addWidget(self.end_date)

        # Quick Date Buttons
        quick_dates_widget = QFrame()
        quick_dates_widget.setStyleSheet("border: none;")
        quick_dates_layout = QVBoxLayout(quick_dates_widget)
        quick_dates_label = QLabel("Quick Select")
        quick_dates_label.setStyleSheet(
            f"color: {colors['text_secondary']}; font-size: 13px;"
        )

        quick_dates_buttons = QHBoxLayout()

        button_style = f"""
            QPushButton {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px 10px;
                color: {colors['text_primary']};
            }}
            QPushButton:hover {{
                background-color: {colors['border']};
            }}
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

        # Add all elements to the horizontal layout
        date_picker_layout.addWidget(start_date_widget)
        date_picker_layout.addWidget(end_date_widget)
        date_picker_layout.addWidget(quick_dates_widget)

        date_layout.addLayout(date_picker_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Generate Button
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {colors['accent']};
                border: 0px;
                border-radius: 4px;
                padding: 8px 16px;
                margin-left: 10px;
                margin-bottom: 10px;
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #1d4ed8;
            }}
            """
        )
        self.generate_button.clicked.connect(self.generate_summary)

        self.export_button = QPushButton("Export to Excel")
        self.export_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #22c55e;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                margin-right: 10px;
                margin-bottom: 10px;
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #16a34a;
            }}
            """
        )
        self.export_button.clicked.connect(self.export_to_excel)

        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.export_button)

        date_layout.addLayout(button_layout)

        # Scroll Area for Summary
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()

        scroll_layout = QVBoxLayout(scroll_content)
        self.summary_text = QTextEdit(scroll_content)
        self.summary_text.setReadOnly(True)
        self.summary_text.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: {colors['card_bg']};
                color: {colors['text_primary']};
                border: none;
                border-radius: 4px;
            }}
            """
        )
        scroll_layout.addWidget(self.summary_text)
        scroll_area.setWidget(scroll_content)

        # Add all to main layout
        main_layout.addWidget(date_card)
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
                return

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
        """Format the summary report with HTML styling and consistent spacing"""
        colors = Theme.get_theme_colors()

        html = f"""
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background-color: #f9f9f9; 
            }}
            .header {{ 
                color: {colors['text_secondary']}; 
                font-size: 19px; 
                font-weight: bold; 
                margin-bottom: 20px; 
            }}
            .section {{ 
                margin-bottom: 30px; 
                padding-bottom: 10px; 
                border-bottom: 1px solid {colors['text_secondary']}; 
            }}
            .subheader {{ 
                color: {colors['text_secondary']}; 
                font-size: 16px; 
                margin-bottom: 10px; 
                font-weight: bold;
            }}
            .data {{ 
                color: {colors['text_primary']}; 
                margin-left: 20px;
                margin-bottom: 20px;
                line-height: 1; 
            }}
            .highlight {{ 
                color: {colors['accent']}; 
                font-weight: bold;
            }}
            .transparent {{
                background-color: transparent;
                color: transparent;
                border: none;
            }}
        </style>
        
        <div class="header">Summary Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})</div>
        """

        if not transactions:
            return (
                html
                + f"""
            <div class="section">
                <div class="subheader">No Data Available</div>
                <div class="data">No transactions found for this period.</div>
            </div>
            """
            )

        html += f"""
        <div class="section">
            <div class="subheader">- Overview</div>
            <div class="data">
                Total Transactions: <span class="highlight">{len(transactions)}</span><br>
                Total Revenue: <span class="highlight">Rp{total_amount:,.2f}</span><br>
                Average Transaction Value: <span class="highlight">Rp{(total_amount / len(transactions)):,.2f}</span>
            </div>
        </div>
        """

        sections = [
            {
                "condition": trends.get("top_products"),
                "subheader": "- Top Selling Products",
                "data": "".join(
                    f"{product}: <span class='highlight'>{quantity}</span> units"
                    + ("<br>" if i < len(trends["top_products"]) - 1 else "")
                    for i, (product, quantity) in enumerate(trends["top_products"])
                ),
            },
            {
                "condition": trends.get("peak_day", {}).get("date"),
                "subheader": "- Sales Analysis",
                "data": f"""
                    Peak Sales Day: <span class="highlight">{trends['peak_day']['date']}</span><br>
                    Peak Day Revenue: <span class="highlight">Rp{trends['peak_day']['amount']:,.2f}</span><br>
                    Growth Rate: <span class="highlight">{trends['growth_rate']:.1f}%</span>
                """,
            },
            {
                "condition": product_summary,
                "subheader": "- Detailed Product Summary",
                "data": "".join(
                    f"""
                    <b>{product_name}</b><br>
                    Quantity Sold: <span class="highlight">{data['quantity']}</span><br>
                    Revenue: <span class="highlight">Rp{data['total']:,.2f}</span><br>
                    Average Price: <span class="highlight mb-10">Rp{(data['total'] / data['quantity']):,.2f}</span><br>
                    <span class="transparent">-</span><br>
                    """
                    for product_name, data in product_summary.items()
                    if data["quantity"] > 0
                ),
            },
        ]

        for section in sections:
            if section["condition"]:
                html += f"""
                <div class="section">
                    <div class="subheader">{section['subheader']}</div>
                    <div class="data">{section['data']}</div>
                </div>
                """

        return html
