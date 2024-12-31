import tkinter as tk
from tkinter import ttk, messagebox
from bson import ObjectId
from src.ui.dialogs.sale_dialog import SaleDialog


class SalesTab(ttk.Frame):
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
        self.refresh_sales_list()

    def setup_ui(self):
        # Control Frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            control_frame, text="Add Sale", command=self.show_add_sale_dialog
        ).pack(side="left", padx=5)

        ttk.Label(control_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(control_frame)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.refresh_sales_list)

        self.delete_button = ttk.Button(
            control_frame,
            text="Delete",
            command=self.delete_selected_sale,
            state="disabled",
        )
        self.delete_button.pack(side="right", padx=(5, 11))

        self.edit_button = ttk.Button(
            control_frame,
            text="Edit",
            command=self.edit_selected_sale,
            state="disabled",
        )
        self.edit_button.pack(side="right", padx=5)

        # Sales TreeView
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=(11, 0), pady=(0, 5))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Date", "Product", "Quantity", "Total"),
            show="headings",
            style="Custom.Treeview",
        )

        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total", text="Total")

        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Product", width=280)
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Total", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event=None):
        selection = self.tree.selection()
        if selection:
            self.edit_button.config(state="normal")
            self.delete_button.config(state="normal")
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")

    def refresh_sales_list(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_entry.get().strip().lower()
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
                    transaction.product_name,
                    transaction.quantity,
                    f"Rp{transaction.total:,}",
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
        self.wait_window(dialog.dialog)
        self.refresh_sales_list()

    def edit_selected_sale(self):
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
            self.wait_window(dialog.dialog)
            self.refresh_sales_list()

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
                    self.refresh_sales_list()
                    messagebox.showinfo("Success", "Sale deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete sale")
