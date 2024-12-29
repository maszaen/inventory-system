import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from src.models.product import Product
from src.utils.logger import Logger


class ProductDialog:
    def __init__(self, parent, product_manager, logger: Logger, product=None):
        self.dialog = tk.Toplevel(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.product = product
        self.setup_dialog()

    def setup_dialog(self):
        self.dialog.geometry("300x235")
        self.dialog.transient(self.dialog.master)
        self.dialog.grab_set()

        # Center dialog
        x = (self.dialog.master.winfo_screenwidth() - 300) // 2
        y = (self.dialog.master.winfo_screenheight() - 235) // 2
        self.dialog.geometry(f"+{x}+{y}")

        title = "Edit Product" if self.product else "Add New Product"
        self.dialog.title(title)

        # Name field
        ttk.Label(self.dialog, text="Name:", width=32).pack()
        self.name_entry = ttk.Entry(self.dialog, width=32)
        if self.product:
            self.name_entry.insert(0, self.product.name)
        self.name_entry.pack(pady=(0, 7))

        # Price field
        ttk.Label(self.dialog, text="Price:", width=32).pack()
        self.price_entry = ttk.Entry(self.dialog, width=32)
        if self.product:
            self.price_entry.insert(0, str(self.product.price))
        self.price_entry.pack(pady=(0, 7))

        # Stock field
        ttk.Label(self.dialog, text="Stock:", width=32).pack()
        self.stock_entry = ttk.Entry(self.dialog, width=32)
        if self.product:
            self.stock_entry.insert(0, str(self.product.stock))
        self.stock_entry.pack(pady=(0, 7))

        # Save button
        ttk.Button(self.dialog, text="Save", command=self.save_product).pack(pady=20)

    def save_product(self):
        try:
            name = self.name_entry.get().strip()
            price = Decimal(self.price_entry.get())
            stock = int(self.stock_entry.get())

            if not name:
                raise ValueError("Product name is required!")
            if price <= 0:
                raise ValueError("Price must be positive")
            if stock < 0:
                raise ValueError("Stock cannot be negative")

            if self.product:
                # Update existing product
                self.product.name = name
                self.product.price = price
                self.product.stock = stock
                if self.product_manager.update_product(self.product):
                    self.logger.log_action(
                        f"Updated product: {name} "
                        f"(ID: {self.product._id}, "
                        f"Price: {price}, Stock: {stock})"
                    )
                    messagebox.showinfo("Success", "Product updated successfully!")
                else:
                    raise ValueError("Failed to update product")
            else:
                # Create new product
                new_product = Product(name=name, price=price, stock=stock)
                if self.product_manager.create_product(new_product):
                    self.logger.log_action(
                        f"Created new product: {name} "
                        f"(ID: {new_product._id}, "
                        f"Price: {price}, Stock: {stock})"
                    )
                    messagebox.showinfo("Success", "Product created successfully!")
                else:
                    raise ValueError("Failed to create product")

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
