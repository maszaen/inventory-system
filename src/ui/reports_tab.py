# src/ui/tabs/reports_tab.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from decimal import Decimal


class ReportsTab(ctk.CTkFrame):
    def __init__(self, parent, transaction_manager):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # Control Frame
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=10, pady=5)

        # Date Filters
        date_frame = ctk.CTkFrame(control_frame)
        date_frame.pack(side="left", padx=5)

        # Quick filters
        ctk.CTkLabel(date_frame, text="Quick Filters:").pack(side="left", padx=5)

        for text, days in [("Today", 0), ("7 Days", 7), ("30 Days", 30)]:
            ctk.CTkButton(
                date_frame,
                text=text,
                width=80,
                height=28,
                command=lambda d=days: self.set_date_range(d),
            ).pack(side="left", padx=2)

        # Custom date range
        custom_frame = ctk.CTkFrame(control_frame)
        custom_frame.pack(side="left", padx=20)

        ctk.CTkLabel(custom_frame, text="From:").pack(side="left", padx=5)
        self.start_date = DateEntry(
            custom_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.start_date.pack(side="left", padx=5)

        ctk.CTkLabel(custom_frame, text="To:").pack(side="left", padx=5)
        self.end_date = DateEntry(
            custom_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.end_date.pack(side="left", padx=5)

        ctk.CTkButton(
            custom_frame, text="Apply", width=60, height=28, command=self.refresh
        ).pack(side="left", padx=5)

        # Content Area
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left side - Summary
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Summary header
        ctk.CTkLabel(
            left_frame, text="Sales Summary", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=10)

        # Summary text area
        self.summary_text = ctk.CTkTextbox(left_frame, wrap="word", height=200)
        self.summary_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Right side - Top Products
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Top products header
        ctk.CTkLabel(
            right_frame, text="Top Products", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=10)

        # Top products tree
        tree_frame = ctk.CTkFrame(right_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Product", "Quantity", "Revenue"),
            show="headings",
            style="Custom.Treeview",
        )

        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Revenue", text="Revenue")

        self.tree.column("Product", width=200)
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Revenue", width=150, anchor="e")

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def set_date_range(self, days):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        self.start_date.set_date(start_date)
        self.end_date.set_date(end_date)
        self.refresh()

    def refresh(self):
        try:
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()

            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

            # Get transactions
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start_date, end_date
            )

            # Calculate statistics
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
            summary = f"Sales Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})\n"
            summary += "=" * 50 + "\n\n"

            if transactions:
                summary += f"Total Transactions: {len(transactions)}\n"
                summary += f"Total Revenue: Rp{total_amount:,.2f}\n"
                avg_transaction = total_amount / len(transactions)
                summary += f"Average Transaction: Rp{avg_transaction:,.2f}\n\n"

                # Daily average
                days = (end_date - start_date).days + 1
                daily_avg = total_amount / days
                summary += f"Daily Average Revenue: Rp{daily_avg:,.2f}\n"

                # Best day
                daily_totals = {}
                for transaction in transactions:
                    date = transaction.date
                    if date not in daily_totals:
                        daily_totals[date] = Decimal("0")
                    daily_totals[date] += transaction.total

                if daily_totals:
                    best_day = max(daily_totals.items(), key=lambda x: x[1])
                    summary += f"Best Day: {best_day[0].strftime('%Y-%m-%d')} (Rp{best_day[1]:,.2f})\n"
            else:
                summary += "No transactions found in this date range."

            # Update summary text
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", summary)

            # Update top products tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Sort products by revenue and show top 10
            sorted_products = sorted(
                product_summary.items(), key=lambda x: x[1]["total"], reverse=True
            )[:10]

            for product_name, data in sorted_products:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        product_name,
                        data["quantity"],
                        f"Rp{data['total']:,.2f}",
                    ),
                )

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
