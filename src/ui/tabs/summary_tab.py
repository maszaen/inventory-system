import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from decimal import Decimal


class SummaryTab(ttk.Frame):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()

    def setup_ui(self):
        # Date selection frame
        date_frame = ttk.Frame(self)
        date_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(date_frame, text="Start Date:").pack(side="left", padx=5)
        self.start_date = DateEntry(
            date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.start_date.pack(side="left", padx=5)

        ttk.Label(date_frame, text="End Date:").pack(side="left", padx=5)
        self.end_date = DateEntry(
            date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.end_date.pack(side="left", padx=5)

        ttk.Button(
            date_frame, text="Generate Summary", command=self.generate_summary
        ).pack(side="left", padx=5)

        # Summary text area
        self.summary_text = tk.Text(self, height=20, width=60)
        self.summary_text.pack(padx=5, pady=5, fill="both", expand=True)

    def generate_summary(self):
        try:
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()

            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

            # Dapatkan transaksi dalam range tanggal
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )

            # Hitung total dan ringkasan per produk
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
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(1.0, summary)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
