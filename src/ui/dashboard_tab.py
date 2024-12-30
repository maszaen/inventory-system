import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, timedelta
from decimal import Decimal


class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, value, subtitle=None, icon=None, trend=None):
        super().__init__(parent)
        self.configure(fg_color=("gray90", "gray16"))

        # Container
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Header with icon
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        if icon:
            ctk.CTkLabel(header, text=icon, font=ctk.CTkFont(size=24)).pack(side="left")

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray70"),
        ).pack(side="left", padx=10)

        # Value
        value_frame = ctk.CTkFrame(content, fg_color="transparent")
        value_frame.pack(fill="x")

        ctk.CTkLabel(
            value_frame, text=value, font=ctk.CTkFont(size=28, weight="bold")
        ).pack(side="left")

        if trend:
            trend_color = "#4CAF50" if trend >= 0 else "#F44336"
            trend_icon = "↑" if trend >= 0 else "↓"
            ctk.CTkLabel(
                value_frame,
                text=f" {trend_icon} {abs(trend):.1f}%",
                text_color=trend_color,
                font=ctk.CTkFont(size=14),
            ).pack(side="left", padx=5)

        # Subtitle
        if subtitle:
            ctk.CTkLabel(
                content,
                text=subtitle,
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray70"),
            ).pack(anchor="w", pady=(5, 0))


class QuickActionButton(ctk.CTkButton):
    def __init__(self, parent, text, icon, command=None):
        super().__init__(
            parent,
            text=f"{icon} {text}",
            command=command,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=("gray85", "gray20"),
            text_color=("gray10", "gray90"),
            hover_color=("gray75", "gray30"),
        )


class DashboardTab(ctk.CTkFrame):
    def __init__(self, parent, transaction_manager, product_manager=None):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self.product_manager = product_manager
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # Welcome Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            header, text="Dashboard Overview", font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70"),
        ).pack(anchor="w", pady=(5, 0))

        # Quick Actions
        actions = ctk.CTkFrame(self)
        actions.pack(fill="x", padx=20, pady=(0, 20))

        QuickActionButton(actions, "New Sale", "🛍️", self.new_sale).pack(
            side="left", padx=(0, 10)
        )

        QuickActionButton(actions, "Add Product", "📦", self.add_product).pack(
            side="left", padx=(0, 10)
        )

        QuickActionButton(actions, "Generate Report", "📊", self.generate_report).pack(
            side="left"
        )

        # Stats Grid
        self.stats_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_grid.pack(fill="x", padx=20)

        for i in range(3):
            self.stats_grid.grid_columnconfigure(i, weight=1, pad=10)

        # Recent Transactions
        self.setup_transactions_table()

    def setup_transactions_table(self):
        transactions_frame = ctk.CTkFrame(self)
        transactions_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(transactions_frame, fg_color="transparent")
        header.pack(fill="x", pady=(15, 10))

        ctk.CTkLabel(
            header, text="Recent Transactions", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="View All →",
            font=ctk.CTkFont(size=12),
            width=80,
            height=28,
            fg_color="transparent",
            hover_color=("gray85", "gray30"),
        ).pack(side="right")

        # Treeview style
        style = ttk.Style()
        style.configure(
            "Dashboard.Treeview",
            background=(
                "gray95" if self._get_appearance_mode() == "light" else "gray17"
            ),
            fieldbackground=(
                "gray95" if self._get_appearance_mode() == "light" else "gray17"
            ),
            foreground=(
                "gray10" if self._get_appearance_mode() == "light" else "gray90"
            ),
            rowheight=50,
            font=("Segoe UI", 10),
        )
        style.configure("Dashboard.Treeview.Heading", font=("Segoe UI", 10, "bold"))

        # Treeview
        self.transactions_tree = ttk.Treeview(
            transactions_frame,
            columns=("time", "product", "quantity", "amount", "status"),
            show="headings",
            height=5,
            style="Dashboard.Treeview",
        )

        # Configure columns
        self.transactions_tree.heading("time", text="Time")
        self.transactions_tree.heading("product", text="Product")
        self.transactions_tree.heading("quantity", text="Qty")
        self.transactions_tree.heading("amount", text="Amount")
        self.transactions_tree.heading("status", text="Status")

        self.transactions_tree.column("time", width=100)
        self.transactions_tree.column("product", width=250)
        self.transactions_tree.column("quantity", width=80, anchor="center")
        self.transactions_tree.column("amount", width=120, anchor="e")
        self.transactions_tree.column("status", width=100, anchor="center")

        self.transactions_tree.pack(fill="both", expand=True)

    def refresh(self):
        # Clear previous stats
        for widget in self.stats_grid.winfo_children():
            widget.destroy()

        # Calculate stats
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        today_sales = self.get_sales_stats(today)
        yesterday_sales = self.get_sales_stats(yesterday)

        # Growth calculation
        revenue_growth = 0
        if yesterday_sales["total"] > 0:
            revenue_growth = (
                (today_sales["total"] - yesterday_sales["total"])
                / yesterday_sales["total"]
                * 100
            )

        # Create stat cards
        StatCard(
            self.stats_grid,
            "Today's Revenue",
            f"Rp{today_sales['total']:,.0f}",
            f"{today_sales['count']} transactions today",
            "💰",
            revenue_growth,
        ).grid(row=0, column=0, sticky="nsew")

        StatCard(
            self.stats_grid,
            "Average Order",
            f"Rp{today_sales['average']:,.0f}",
            "Per transaction",
            "📊",
        ).grid(row=0, column=1, sticky="nsew")

        low_stock = self.get_low_stock_count()
        StatCard(
            self.stats_grid,
            "Inventory Status",
            f"{low_stock} items",
            "Low on stock",
            "📦",
        ).grid(row=0, column=2, sticky="nsew")

        # Update transactions
        self.refresh_transactions()

    def refresh_transactions(self):
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        transactions = self.transaction_manager.get_recent_transactions(5)

        for trans in transactions:
            trans_dict = trans
            # Jika trans adalah dictionary dari MongoDB
            if isinstance(trans, dict):
                date = trans.get("date")
                product_name = trans.get("product_name")
                quantity = trans.get("quantity")
                total = trans.get("total")
            # Jika trans adalah Transaction object
            else:
                date = trans.date
                product_name = trans.product_name
                quantity = trans.quantity
                total = trans.total

            self.transactions_tree.insert(
                "",
                "end",
                values=(
                    date.strftime("%H:%M") if date else "N/A",
                    product_name,
                    quantity,
                    f"Rp{total:,.0f}" if total else "Rp0",
                    "Completed",
                ),
            )

    def get_sales_stats(self, date):
        transactions = self.transaction_manager.get_transactions_by_date_range(
            date, date
        )
        total = sum(t.total for t in transactions)
        count = len(transactions)
        average = total / count if count > 0 else 0
        return {"total": total, "count": count, "average": average}

    def get_low_stock_count(self):
        if not self.product_manager:
            return 0
        products = self.product_manager.get_all_products()
        return sum(1 for p in products if p.stock < 10)

    def new_sale(self):
        # Implement navigation to sales tab
        pass

    def add_product(self):
        # Implement navigation to products tab
        pass

    def generate_report(self):
        # Implement navigation to reports tab
        pass
