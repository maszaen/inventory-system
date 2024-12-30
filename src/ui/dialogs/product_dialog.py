import customtkinter as ctk
from tkinter import messagebox
from decimal import Decimal
from src.models.product import Product


class ProductDialog(ctk.CTkToplevel):
    def __init__(self, parent, product_manager, logger, product=None):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.product = product
        self.title("Edit Product" if product else "Add New Product")
        self.setup_window()

    def setup_window(self):
        window_width = 400
        window_height = 520

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

        # Form fields
        # Product Name
        name_frame = ctk.CTkFrame(container)
        name_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            name_frame, text="Product Name:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        self.name_entry = ctk.CTkEntry(name_frame, height=32)
        self.name_entry.pack(fill="x")
        if self.product:
            self.name_entry.insert(0, self.product.name)

        # Price
        price_frame = ctk.CTkFrame(container)
        price_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(price_frame, text="Price:", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w"
        )

        self.price_entry = ctk.CTkEntry(price_frame, height=32)
        self.price_entry.pack(fill="x")
        if self.product:
            self.price_entry.insert(0, str(self.product.price))

        # Stock
        stock_frame = ctk.CTkFrame(container)
        stock_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(stock_frame, text="Stock:", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w"
        )

        self.stock_entry = ctk.CTkEntry(stock_frame, height=32)
        self.stock_entry.pack(fill="x")
        if self.product:
            self.stock_entry.insert(0, str(self.product.stock))

        # Category (Optional)
        category_frame = ctk.CTkFrame(container)
        category_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            category_frame, text="Category:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        self.category_var = ctk.StringVar(value="General")
        category_combo = ctk.CTkComboBox(
            category_frame,
            values=["General", "Electronics", "Food", "Beverage", "Other"],
            variable=self.category_var,
            height=32,
        )
        category_combo.pack(fill="x")

        # Description (Optional)
        desc_frame = ctk.CTkFrame(container)
        desc_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            desc_frame, text="Description:", font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w")

        self.description = ctk.CTkTextbox(desc_frame, height=100)
        self.description.pack(fill="x")

        # Buttons
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(
            button_frame, text="Save", command=self.save_product, height=32
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            height=32,
            fg_color="transparent",
            border_width=1,
        ).pack(side="right", padx=5)

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

            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
