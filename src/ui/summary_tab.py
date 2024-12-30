# src/ui/tabs/summary_tab.py
import customtkinter as ctk
from tkcalendar import DateEntry
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from decimal import Decimal


class SummaryTab(ctk.CTkFrame):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()
        self.pack(fill="both", expand=True)

    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Date selection frame
        date_frame = ctk.CTkFrame(main_container)
        date_frame.pack(fill="x", pady=10)

        # Start date
        start_date_frame = ctk.CTkFrame(date_frame)
        start_date_frame.pack(side="left", padx=5)

        ctk.CTkLabel(start_date_frame, text="Start Date:").pack(side="left", padx=5)
        self.start_date = DateEntry(
            start_date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.start_date.pack(side="left", padx=5)

        # End date
        end_date_frame = ctk.CTkFrame(date_frame)
        end_date_frame.pack(side="left", padx=5)

        ctk.CTkLabel(end_date_frame, text="End Date:").pack(side="left", padx=5)
        self.end_date = DateEntry(
            end_date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.end_date.pack(side="left", padx=5)

        # Generate button
        ctk.CTkButton(
            date_frame,
            text="Generate Summary",
            command=self.generate_summary,
            height=32,
        ).pack(side="left", padx=20)

        # Summary text area frame
        text_frame = ctk.CTkFrame(main_container)
        text_frame.pack(fill="both", expand=True, pady=10)

        # Text widget for summary
        self.summary_text = ctk.CTkTextbox(text_frame, wrap="word", height=400)
        self.summary_text.pack(fill="both", expand=True)

    def generate_summary(self):
        try:
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()

            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

            # Get transactions in date range
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )

            # Calculate totals and summary per product
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
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", summary)

        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e))
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
