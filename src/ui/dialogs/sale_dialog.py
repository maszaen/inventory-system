import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from decimal import Decimal
from datetime import datetime
from src.models.transaction import Transaction
from src.utils.logger import Logger


class SaleDialog:
    def __init__(
        self,
        parent,
        product_manager,
        transaction_manager,
        logger: Logger,
        transaction=None,
        refresh_callback=None,
    ):
        self.dialog = tk.Toplevel(parent)
        self.product_manager = product_manager
        self.transaction_manager = transaction_manager
        self.logger = logger
        self.transaction = transaction
        self.refresh_callback = refresh_callback
        self.setup_dialog()

    def setup_dialog(self):
        self.dialog.geometry("300x235")
        self.dialog.transient(self.dialog.master)
        self.dialog.grab_set()

        # Center dialog
        x = (self.dialog.master.winfo_screenwidth() - 300) // 2
        y = (self.dialog.master.winfo_screenheight() - 235) // 2
        self.dialog.geometry(f"+{x}+{y}")

        title = "Edit Sale" if self.transaction else "Add New Sale"
        self.dialog.title(title)

        # Date field
        ttk.Label(self.dialog, text="Date:", width=32).pack()
        self.date_picker = DateEntry(
            self.dialog,
            width=30,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        if self.transaction:
            self.date_picker.set_date(self.transaction.date)
        self.date_picker.pack(pady=(0, 7))

        # Product field
        ttk.Label(self.dialog, text="Product:", width=32).pack()
        self.products = self.product_manager.get_all_products()
        product_names = [p.name for p in self.products]

        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(
            self.dialog, textvariable=self.product_var, width=30, values=product_names
        )
        if self.transaction:
            self.product_combo.set(self.transaction.product_name)
        self.product_combo.pack(pady=(0, 7))

        # Quantity field
        ttk.Label(self.dialog, text="Quantity:", width=32).pack()
        self.quantity_entry = ttk.Entry(self.dialog, width=32)
        if self.transaction:
            self.quantity_entry.insert(0, str(self.transaction.quantity))
        self.quantity_entry.pack(pady=(0, 7))

        # Save button
        ttk.Button(self.dialog, text="Save", command=self.save_sale).pack(pady=20)

    def save_sale(self):
        try:
            sale_date = self.date_picker.get_date()
            product_name = self.product_var.get()
            quantity = int(self.quantity_entry.get())

            # Validate input
            if not product_name:
                raise ValueError("Please select a product")
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            # Find selected product
            selected_product = None
            for product in self.products:
                if product.name == product_name:
                    selected_product = product
                    break

            if not selected_product:
                raise ValueError("Product not found")

            # Calculate total
            total = selected_product.price * quantity

            if self.transaction:
                old_product = self.product_manager.get_product_by_id(
                    self.transaction.product_id
                )
                if old_product:
                    old_product.stock += self.transaction.quantity
                    if not self.product_manager.update_product(old_product):
                        raise ValueError("Failed to restore product stock")

                # Validasi stok untuk transaksi baru
                if quantity > selected_product.stock + self.transaction.quantity:
                    raise ValueError(
                        f"Insufficient stock!\n"
                        f"Requested: {quantity}\n"
                        f"Available: {selected_product.stock + self.transaction.quantity}"
                    )

                # Perbarui transaksi dengan data baru
                old_quantity = self.transaction.quantity
                self.transaction.date = sale_date
                self.transaction.product_id = selected_product._id
                self.transaction.product_name = product_name
                self.transaction.quantity = quantity
                self.transaction.total = total

                # Perbarui stok produk
                selected_product.stock += old_quantity  # Pulihkan stok lama
                selected_product.stock -= quantity  # Kurangi stok dengan kuantitas baru

                # Simpan transaksi dan perbarui stok produk
                if not self.transaction_manager.update_transaction(self.transaction):
                    # Rollback jika pembaruan transaksi gagal
                    selected_product.stock += quantity  # Pulihkan stok baru
                    selected_product.stock -= old_quantity  # Kembalikan stok lama
                    self.product_manager.update_product(selected_product)
                    raise ValueError("Failed to update transaction")

                if not self.product_manager.update_product(selected_product):
                    # Rollback jika pembaruan stok gagal
                    selected_product.stock += quantity  # Pulihkan stok baru
                    selected_product.stock -= old_quantity  # Kembalikan stok lama
                    self.transaction.quantity = (
                        old_quantity  # Kembalikan transaksi lama
                    )
                    self.transaction_manager.update_transaction(self.transaction)
                    raise ValueError("Failed to update product stock")

                # Log perubahan berhasil
                self.logger.log_action(
                    f"Sale updated:\n"
                    f"  Transaction ID: {self.transaction._id}\n"
                    f"  Product: {product_name}\n"
                    f"  Quantity: {quantity}\n"
                    f"  Total: {total}\n"
                    f"  Stock: {selected_product.stock + old_quantity} → {selected_product.stock}"
                )

            else:
                # Check stock availability for new transaction
                if quantity > selected_product.stock:
                    raise ValueError(
                        f"Insufficient stock!\n"
                        f"Requested: {quantity}\n"
                        f"Available: {selected_product.stock}"
                    )

                # Create and save new transaction
                transaction = Transaction(
                    product_id=selected_product._id,
                    product_name=product_name,
                    quantity=quantity,
                    total=total,
                    date=sale_date,
                )

                # Save transaction
                if not self.transaction_manager.create_transaction(transaction):
                    raise ValueError("Failed to create transaction")

                # Update stock
                old_stock = selected_product.stock
                selected_product.stock -= quantity
                if not self.product_manager.update_product(selected_product):
                    # Rollback: delete the transaction if stock update fails
                    self.transaction_manager.delete_transaction(transaction._id)
                    raise ValueError("Failed to update product stock")

                # Log the successful creation
                self.logger.log_action(
                    f"New sale recorded:\n"
                    f"  Product: {product_name}\n"
                    f"  Quantity: {quantity}\n"
                    f"  Total: {total}\n"
                    f"  Stock: {old_stock} → {selected_product.stock}"
                )

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo(
                "Success",
                f"{'Sale updated' if self.transaction else 'Sale recorded'} successfully!\n\n"
                f"Product: {product_name}\n"
                f"Quantity: {quantity}\n"
                f"Total: Rp{total:,.2f}",
            )

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
