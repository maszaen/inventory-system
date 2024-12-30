import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry

from src.models.transaction import Transaction


class SaleDialog(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        product_manager,
        transaction_manager,
        logger,
        transaction=None,
        refresh_callback=None,
    ):
        super().__init__(parent)
        self.product_manager = product_manager
        self.transaction_manager = transaction_manager
        self.logger = logger
        self.transaction = transaction
        self.refresh_callback = refresh_callback
        self.title("Edit Sale" if transaction else "New Sale")
        self.setup_window()

    def setup_window(self):
        window_width = 400
        window_height = 600

        # Center dialog
        x = (self.master.winfo_screenwidth() - window_width) // 2
        y = (self.master.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            container, text=self.title(), font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))

        # Date and Time
        date_frame = ctk.CTkFrame(container)
        date_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(date_frame, text="Date:", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w"
        )

        self.date_picker = DateEntry(
            date_frame,
            width=20,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.pack(fill="x")
        if self.transaction:
            self.date_picker.set_date(self.transaction.date)

        # Product Selection
        product_frame = ctk.CTkFrame(container)
        product_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            product_frame, text="Product:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        # Get products for dropdown
        self.products = self.product_manager.get_all_products()
        product_names = [p.name for p in self.products]

        self.product_var = ctk.StringVar()
        self.product_combo = ctk.CTkComboBox(
            product_frame,
            values=product_names,
            variable=self.product_var,
            height=32,
            command=self.on_product_select,
        )
        self.product_combo.pack(fill="x")

        if self.transaction:
            self.product_combo.set(self.transaction.product_name)

        # Product Info
        self.info_frame = ctk.CTkFrame(container)
        self.info_frame.pack(fill="x", pady=10)

        self.price_label = ctk.CTkLabel(self.info_frame, text="Price: -")
        self.price_label.pack(anchor="w")

        self.stock_label = ctk.CTkLabel(self.info_frame, text="Available Stock: -")
        self.stock_label.pack(anchor="w")

        # Quantity
        quantity_frame = ctk.CTkFrame(container)
        quantity_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            quantity_frame, text="Quantity:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        self.quantity_entry = ctk.CTkEntry(quantity_frame, height=32)
        self.quantity_entry.pack(fill="x")
        self.quantity_entry.bind("<KeyRelease>", self.calculate_total)

        if self.transaction:
            self.quantity_entry.insert(0, str(self.transaction.quantity))

        # Total
        total_frame = ctk.CTkFrame(container)
        total_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            total_frame, text="Total Amount:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        self.total_label = ctk.CTkLabel(
            total_frame, text="Rp0", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.total_label.pack(anchor="w")

        # Notes
        notes_frame = ctk.CTkFrame(container)
        notes_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(notes_frame, text="Notes:", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w"
        )

        self.notes = ctk.CTkTextbox(notes_frame, height=80)
        self.notes.pack(fill="x")

        # Buttons
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame, text="Save", command=self.save_sale, height=32
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            height=32,
            fg_color="transparent",
            border_width=1,
        ).pack(side="right", padx=5)

        # Update product info if editing
        if self.transaction:
            self.on_product_select(self.transaction.product_name)
            self.calculate_total()

    def on_product_select(self, choice):
        selected_product = None
        for product in self.products:
            if product.name == choice:
                selected_product = product
                break

        if selected_product:
            self.price_label.configure(text=f"Price: Rp{selected_product.price:,}")
            self.stock_label.configure(
                text=f"Available Stock: {selected_product.stock}"
            )
            self.calculate_total()

    def calculate_total(self, event=None):
        try:
            selected_product = None
            for product in self.products:
                if product.name == self.product_var.get():
                    selected_product = product
                    break

            if selected_product and self.quantity_entry.get():
                quantity = int(self.quantity_entry.get())
                total = selected_product.price * quantity
                self.total_label.configure(text=f"Rp{total:,}")
            else:
                self.total_label.configure(text="Rp0")
        except ValueError:
            self.total_label.configure(text="Rp0")

    def save_sale(self):
        try:
            product_name = self.product_var.get()
            quantity = int(self.quantity_entry.get())
            sale_date = self.date_picker.get_date()

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

                if quantity > selected_product.stock + self.transaction.quantity:
                    raise ValueError(
                        f"Insufficient stock!\n"
                        f"Requested: {quantity}\n"
                        f"Available: {selected_product.stock + self.transaction.quantity}"
                    )

                old_quantity = self.transaction.quantity
                self.transaction.date = sale_date
                self.transaction.product_id = selected_product._id
                self.transaction.product_name = product_name
                self.transaction.quantity = quantity
                self.transaction.total = total

                selected_product.stock += old_quantity
                selected_product.stock -= quantity

                if not self.transaction_manager.update_transaction(self.transaction):
                    selected_product.stock += quantity
                    selected_product.stock -= old_quantity
                    self.product_manager.update_product(selected_product)
                    raise ValueError("Failed to update transaction")

                if not self.product_manager.update_product(selected_product):
                    selected_product.stock += quantity
                    selected_product.stock -= old_quantity
                    self.transaction.quantity = old_quantity
                    self.transaction_manager.update_transaction(self.transaction)
                    raise ValueError("Failed to update product stock")

                self.logger.log_action(
                    f"Sale updated:\n"
                    f"  Transaction ID: {self.transaction._id}\n"
                    f"  Product: {product_name}\n"
                    f"  Quantity: {quantity}\n"
                    f"  Total: {total}\n"
                    f"  Stock: {selected_product.stock + old_quantity} → {selected_product.stock}"
                )

            else:
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

            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
