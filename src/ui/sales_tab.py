# src/ui/tabs/sales_tab.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from bson import ObjectId
from datetime import datetime, timedelta
from src.ui.dialogs.sale_dialog import SaleDialog


class SalesTab(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        product_manager,
        transaction_manager,
        logger,
        refresh_callback=None,
    ):
        super().__init__(parent)
        self.product_manager = product_manager
        self.transaction_manager = transaction_manager
        self.logger = logger
        self.refresh_callback = refresh_callback
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # Header
        self.setup_header()

        # Main Content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Split view
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # Setup TreeView panel
        self.setup_treeview(content)

        # Setup Details panel
        self.setup_details_panel(content)

    def setup_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10, pady=10)

        # Left side - Title and New Sale button
        left_frame = ctk.CTkFrame(header)
        left_frame.pack(side="left")

        ctk.CTkLabel(
            left_frame,
            text="Sales Transactions",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(side="left", padx=(0, 20))

        ctk.CTkButton(
            left_frame, text="New Sale", command=self.show_add_sale_dialog, height=32
        ).pack(side="left")

        # Right side - Search and Filter
        filter_frame = ctk.CTkFrame(header)
        filter_frame.pack(side="right")

        # Date filter combobox
        ctk.CTkLabel(filter_frame, text="Filter:", font=ctk.CTkFont(size=12)).pack(
            side="left", padx=5
        )

        self.filter_var = ctk.StringVar(value="All Time")
        filter_combo = ctk.CTkComboBox(
            filter_frame,
            values=["Today", "This Week", "This Month", "All Time"],
            variable=self.filter_var,
            width=120,
            height=32,
            command=self.on_filter_change,
        )
        filter_combo.pack(side="left", padx=5)

        # Search
        ctk.CTkLabel(filter_frame, text="Search:", font=ctk.CTkFont(size=12)).pack(
            side="left", padx=5
        )

        self.search_entry = ctk.CTkEntry(
            filter_frame,
            width=200,
            height=32,
            placeholder_text="Search transactions...",
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.refresh)

    def setup_treeview(self, parent):
        tree_frame = ctk.CTkFrame(parent)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Treeview Style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Helvetica", 10), rowheight=40)
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Create TreeView
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Date", "Time", "Product", "Quantity", "Total", "Status"),
            show="headings",
            style="Custom.Treeview",
        )

        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Qty")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Time", width=80)
        self.tree.column("Product", width=200)
        self.tree.column("Quantity", width=60, anchor="center")
        self.tree.column("Total", width=120)
        self.tree.column("Status", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        # Bind double click
        self.tree.bind("<Double-1>", self.edit_selected_sale)

    def setup_details_panel(self, parent):
        self.details_frame = ctk.CTkFrame(parent)
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Title
        ctk.CTkLabel(
            self.details_frame,
            text="Transaction Details",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=20)

        # Placeholder
        self.placeholder_label = ctk.CTkLabel(
            self.details_frame,
            text="Select a transaction to view details",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        self.placeholder_label.pack(expand=True)

        # Details content (hidden initially)
        self.details_content = ctk.CTkFrame(self.details_frame)

        # Detail fields
        self.detail_labels = {}
        fields = [
            "Transaction ID",
            "Date & Time",
            "Product",
            "Quantity",
            "Price per Unit",
            "Total Amount",
            "Status",
        ]

        for field in fields:
            frame = ctk.CTkFrame(self.details_content)
            frame.pack(fill="x", pady=5, padx=20)

            ctk.CTkLabel(
                frame, text=f"{field}:", font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w")

            self.detail_labels[field] = ctk.CTkLabel(
                frame, text="", font=ctk.CTkFont(size=12)
            )
            self.detail_labels[field].pack(anchor="w")

        # Action buttons
        button_frame = ctk.CTkFrame(self.details_content)
        button_frame.pack(fill="x", pady=20, padx=20)

        self.edit_button = ctk.CTkButton(
            button_frame, text="Edit", command=self.edit_selected_sale, height=32
        )
        self.edit_button.pack(fill="x", pady=(0, 5))

        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self.delete_selected_sale,
            height=32,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
        )
        self.delete_button.pack(fill="x")

        # Print/Export button
        self.print_button = ctk.CTkButton(
            button_frame,
            text="Print Receipt",
            command=self.print_receipt,
            height=32,
            fg_color="transparent",
            border_width=1,
        )
        self.print_button.pack(fill="x", pady=(5, 0))

    def on_select(self, event=None):
        selection = self.tree.selection()

        if selection:
            self.placeholder_label.pack_forget()
            self.details_content.pack(fill="both", expand=True)

            # Get transaction details
            item = selection[0]
            transaction_id = ObjectId(self.tree.item(item)["values"][0])
            transaction = self.transaction_manager.get_transaction_by_id(transaction_id)

            if transaction:
                product = self.product_manager.get_product_by_id(transaction.product_id)
                price_per_unit = (
                    transaction.total / transaction.quantity
                    if transaction.quantity
                    else 0
                )

                # Update detail labels
                self.detail_labels["Transaction ID"].configure(
                    text=str(transaction._id)
                )
                self.detail_labels["Date & Time"].configure(
                    text=transaction.date.strftime("%Y-%m-%d %H:%M")
                )
                self.detail_labels["Product"].configure(text=transaction.product_name)
                self.detail_labels["Quantity"].configure(text=str(transaction.quantity))
                self.detail_labels["Price per Unit"].configure(
                    text=f"Rp{price_per_unit:,.2f}"
                )
                self.detail_labels["Total Amount"].configure(
                    text=f"Rp{transaction.total:,.2f}"
                )
                self.detail_labels["Status"].configure(
                    text="Completed"  # You might want to add actual status handling
                )
        else:
            self.details_content.pack_forget()
            self.placeholder_label.pack(expand=True)

    def on_filter_change(self, choice):
        self.refresh()

    def refresh(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_entry.get().strip().lower()

        # Apply date filter
        filter_choice = self.filter_var.get()
        today = datetime.now().date()

        if filter_choice == "Today":
            transactions = self.transaction_manager.get_transactions_by_date_range(
                today, today
            )
        elif filter_choice == "This Week":
            start = today - timedelta(days=today.weekday())
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start, today
            )
        elif filter_choice == "This Month":
            start = today.replace(day=1)
            transactions = self.transaction_manager.get_transactions_by_date_range(
                start, today
            )
        else:  # All Time
            transactions = self.transaction_manager.get_all_transactions()

        for transaction in transactions:
            if search_text and search_text not in transaction.product_name.lower():
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    str(transaction._id),
                    transaction.date.strftime("%Y-%m-%d"),
                    transaction.date.strftime("%H:%M"),
                    transaction.product_name,
                    transaction.quantity,
                    f"Rp{transaction.total:,}",
                    "Completed",  # You might want to add actual status handling
                ),
            )

    def show_add_sale_dialog(self):
        dialog = SaleDialog(
            self,
            self.product_manager,
            self.transaction_manager,
            self.logger,
            refresh_callback=self.refresh_callback,
        )
        self.wait_window(dialog)
        self.refresh()

    def edit_selected_sale(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        transaction_id = ObjectId(self.tree.item(item)["values"][0])
        transaction = self.transaction_manager.get_transaction_by_id(transaction_id)

        if transaction:
            dialog = SaleDialog(
                self,
                self.product_manager,
                self.transaction_manager,
                self.logger,
                transaction,
                refresh_callback=self.refresh_callback,
            )
            self.wait_window(dialog)
            self.refresh()

    def delete_selected_sale(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        transaction_id = ObjectId(self.tree.item(item)["values"][0])
        transaction = self.transaction_manager.get_transaction_by_id(transaction_id)

        if transaction:
            if messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete this sale?\n"
                f"Transaction ID: {transaction._id}",
            ):
                # Restore product stock
                product = self.product_manager.get_product_by_id(transaction.product_id)
                if product:
                    product.stock += transaction.quantity
                    self.product_manager.update_product(product)

                if self.transaction_manager.delete_transaction(transaction._id):
                    self.logger.log_action(
                        f"Deleted sale: {transaction._id}\n"
                        f"Product: {transaction.product_name}\n"
                        f"Quantity: {transaction.quantity}\n"
                        f"Total: {transaction.total}"
                    )
                    if self.refresh_callback:
                        self.refresh_callback()
                    self.refresh()
                    messagebox.showinfo("Success", "Sale deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete sale")

    def print_receipt(self):
        # Add receipt printing functionality here
        messagebox.showinfo(
            "Print Receipt", "Receipt printing functionality will be added here."
        )
