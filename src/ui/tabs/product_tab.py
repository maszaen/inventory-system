import tkinter as tk
from tkinter import ttk, messagebox
from bson import ObjectId
from src.ui.dialogs.product_dialog import ProductDialog


class ProductTab(ttk.Frame):
    def __init__(self, parent, product_manager, logger):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.setup_ui()
        self.refresh_product_list()

    def setup_ui(self):
        # Control Frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            control_frame, text="Add Product", command=self.show_add_product_dialog
        ).pack(side="left", padx=5)

        ttk.Label(control_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(control_frame)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.refresh_product_list)

        self.delete_button = ttk.Button(
            control_frame,
            text="Delete",
            command=self.delete_selected_product,
            state="disabled",
        )
        self.delete_button.pack(side="right", padx=(5, 11))

        self.edit_button = ttk.Button(
            control_frame,
            text="Edit",
            command=self.edit_selected_product,
            state="disabled",
        )
        self.edit_button.pack(side="right", padx=5)

        # Products TreeView
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=(11, 0), pady=(0, 5))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Price", "Stock"),
            show="headings",
            style="Custom.Treeview",
        )

        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=280)
        self.tree.column("Price", width=150)
        self.tree.column("Stock", width=100, anchor="center")

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

    def refresh_product_list(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_entry.get().strip().lower()
        products = self.product_manager.get_all_products()

        for product in products:
            if search_text and search_text not in product.name.lower():
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    str(product._id),
                    product.name,
                    f"Rp{product.price:,}",
                    product.stock,
                ),
            )

    def show_add_product_dialog(self):
        dialog = ProductDialog(self, self.product_manager, self.logger)
        self.wait_window(dialog.dialog)
        self.refresh_product_list()

    def edit_selected_product(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        product_id = ObjectId(self.tree.item(item)["values"][0])
        product = self.product_manager.get_product_by_id(product_id)

        if product:
            dialog = ProductDialog(self, self.product_manager, self.logger, product)
            self.wait_window(dialog.dialog)
            self.refresh_product_list()

    def delete_selected_product(self):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        product_id = ObjectId(self.tree.item(item)["values"][0])
        product = self.product_manager.get_product_by_id(product_id)

        if product:
            if messagebox.askyesno(
                "Confirm Deletion", f"Are you sure you want to delete {product.name}?"
            ):
                if self.product_manager.delete_product(product._id):
                    self.logger.log_action(
                        f"Deleted product: {product.name} " f"(ID: {product._id})"
                    )
                    self.refresh_product_list()
                    messagebox.showinfo("Success", "Product deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete product")
