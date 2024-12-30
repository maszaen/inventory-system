# src/ui/tabs/product_tab.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from bson import ObjectId
from src.ui.dialogs.product_dialog import ProductDialog


class ProductTab(ctk.CTkFrame):
    def __init__(self, parent, product_manager, logger):
        super().__init__(parent)
        self.product_manager = product_manager
        self.logger = logger
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # Top Control Frame
        self.setup_header()

        # Main Content Frame
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Split view: TreeView on left, Details on right
        content.grid_columnconfigure(0, weight=3)  # TreeView gets more space
        content.grid_columnconfigure(1, weight=1)  # Details panel
        content.grid_rowconfigure(0, weight=1)

        # Setup TreeView panel
        self.setup_treeview(content)

        # Setup Details panel
        self.setup_details_panel(content)

    def setup_header(self):
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10, pady=10)

        # Left side - Title and Add button
        left_frame = ctk.CTkFrame(header)
        left_frame.pack(side="left")

        ctk.CTkLabel(
            left_frame,
            text="Product Management",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(side="left", padx=(0, 20))

        ctk.CTkButton(
            left_frame,
            text="Add Product",
            command=self.show_add_product_dialog,
            height=32,
        ).pack(side="left")

        # Right side - Search
        search_frame = ctk.CTkFrame(header)
        search_frame.pack(side="right")

        ctk.CTkLabel(search_frame, text="Search:", font=ctk.CTkFont(size=12)).pack(
            side="left", padx=5
        )

        self.search_entry = ctk.CTkEntry(
            search_frame, width=200, height=32, placeholder_text="Search products..."
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
            columns=("ID", "Name", "Price", "Stock", "Status"),
            show="headings",
            style="Custom.Treeview",
        )

        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=250)
        self.tree.column("Price", width=120)
        self.tree.column("Stock", width=80, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        # Bind double click
        self.tree.bind("<Double-1>", self.edit_selected_product)

    def setup_details_panel(self, parent):
        self.details_frame = ctk.CTkFrame(parent)
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Title
        ctk.CTkLabel(
            self.details_frame,
            text="Product Details",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=20)

        # Placeholder when no product is selected
        self.placeholder_label = ctk.CTkLabel(
            self.details_frame,
            text="Select a product to view details",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        self.placeholder_label.pack(expand=True)

        # Details content (hidden initially)
        self.details_content = ctk.CTkFrame(self.details_frame)

        # Will be populated when product is selected
        self.detail_labels = {}
        for field in ["Name", "Price", "Stock", "Status", "Last Updated"]:
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
            button_frame, text="Edit", command=self.edit_selected_product, height=32
        )
        self.edit_button.pack(fill="x", pady=(0, 5))

        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self.delete_selected_product,
            height=32,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
        )
        self.delete_button.pack(fill="x")

    def on_select(self, event=None):
        selection = self.tree.selection()

        # Hide placeholder and show content if product selected
        if selection:
            self.placeholder_label.pack_forget()
            self.details_content.pack(fill="both", expand=True)

            # Get product details
            item = selection[0]
            product_id = ObjectId(self.tree.item(item)["values"][0])
            product = self.product_manager.get_product_by_id(product_id)

            if product:
                # Update detail labels
                self.detail_labels["Name"].configure(text=product.name)
                self.detail_labels["Price"].configure(text=f"Rp{product.price:,}")
                self.detail_labels["Stock"].configure(text=str(product.stock))
                self.detail_labels["Status"].configure(
                    text="In Stock" if product.stock > 0 else "Out of Stock"
                )
                self.detail_labels["Last Updated"].configure(
                    text=product.updated_at.strftime("%Y-%m-%d %H:%M")
                )
        else:
            self.details_content.pack_forget()
            self.placeholder_label.pack(expand=True)

    def refresh(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_entry.get().strip().lower()
        products = self.product_manager.get_all_products()

        for product in products:
            if search_text and search_text not in product.name.lower():
                continue

            status = "In Stock" if product.stock > 0 else "Out of Stock"
            self.tree.insert(
                "",
                "end",
                values=(
                    str(product._id),
                    product.name,
                    f"Rp{product.price:,}",
                    product.stock,
                    status,
                ),
            )

    def show_add_product_dialog(self):
        dialog = ProductDialog(self, self.product_manager, self.logger)
        self.wait_window(dialog)
        self.refresh()

    def edit_selected_product(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return

        item = selection[0]
        product_id = ObjectId(self.tree.item(item)["values"][0])
        product = self.product_manager.get_product_by_id(product_id)

        if product:
            dialog = ProductDialog(self, self.product_manager, self.logger, product)
            self.wait_window(dialog)
            self.refresh()

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
                        f"Deleted product: {product.name} (ID: {product._id})"
                    )
                    self.refresh()
                    messagebox.showinfo("Success", "Product deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete product")
