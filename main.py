import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal
from tkcalendar import DateEntry


class SimpleInventory:
    def __init__(self):
        # Init main window
        self.root = tk.Tk()
        self.root.title("Simple Inventory System")
        self.root.geometry("1000x600")

        # Data storage
        self.products = {}
        self.transactions = []

        # Buat log baru kalo blum ada
        for directory in ["logs", "inventory"]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Muat data dari file
        self.load_data()

        # Setup UI
        self.setup_ui()

        # Refresh daftar produk saat startup
        self.refresh_product_list()
        self.refresh_sales_list()

    def load_data(self):
        # Muat data produk
        if os.path.exists("inventory/products.json"):
            with open("inventory/products.json", "r") as f:
                self.products = json.load(f)
                self.products = {
                    k: {"price": Decimal(str(v["price"])), "stock": v["stock"]}
                    for k, v in self.products.items()
                }

        # Muat data transaksi
        if os.path.exists("inventory/sales.json"):
            with open("inventory/sales.json", "r") as f:
                self.transactions = json.load(f)
                self.transactions = [
                    {
                        "date": datetime.strptime(t["date"], "%Y-%m-%d").date(),
                        "product": t["product"],
                        "quantity": t["quantity"],
                        "total": Decimal(str(t["total"])),
                    }
                    for t in self.transactions
                ]

    def save_data(self):
        # Simpan data produk
        with open("inventory/products.json", "w") as f:
            json.dump(self.products, f, default=str)

        # Simpan data transaksi
        with open("inventory/sales.json", "w") as f:
            json.dump(self.transactions, f, default=str)

    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Products tab
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="Products")

        # Add product section
        ttk.Label(
            products_frame, text="Tambahkan Product", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        # Product input fields
        input_frame = ttk.Frame(products_frame)
        input_frame.pack(fill="x", padx=5)

        ttk.Label(input_frame, text="Name:").pack(side="left")
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.pack(side="left", padx=5)

        ttk.Label(input_frame, text="Price:").pack(side="left")
        self.price_entry = ttk.Entry(input_frame)
        self.price_entry.pack(side="left", padx=5)

        ttk.Label(input_frame, text="Stock:").pack(side="left")
        self.stock_entry = ttk.Entry(input_frame)
        self.stock_entry.pack(side="left", padx=5)

        ttk.Button(input_frame, text="Add Product", command=self.add_product).pack(
            side="left", padx=5
        )

        # Products list with scrollbar
        ttk.Label(
            products_frame, text="List Product", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        tree_frame = ttk.Frame(products_frame)
        tree_frame.pack(fill="both", expand=True, padx=5)

        self.products_tree = ttk.Treeview(
            tree_frame, columns=("Name", "Price", "Stock", "Actions"), show="headings"
        )
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Stock", text="Stock")
        self.products_tree.heading("Actions", text="Actions")

        # Set column widths
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Price", width=150)
        self.products_tree.column("Stock", width=100)
        self.products_tree.column("Actions", width=200)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.products_tree.yview
        )
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind double click event
        self.products_tree.bind("<Double-1>", self.on_tree_double_click)

        # Sales tab
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="Sales")

        # New sale section
        sale_input_frame = ttk.Frame(sales_frame)
        sale_input_frame.pack(fill="x", padx=5, pady=5)

        # Date picker
        ttk.Label(sale_input_frame, text="Date:").pack(side="left")
        self.date_picker = DateEntry(
            sale_input_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.pack(side="left", padx=5)

        ttk.Label(sale_input_frame, text="Product:").pack(side="left")
        self.sale_product_var = tk.StringVar()
        self.sale_product_combo = ttk.Combobox(
            sale_input_frame, textvariable=self.sale_product_var
        )
        self.sale_product_combo.pack(side="left", padx=5)

        ttk.Label(sale_input_frame, text="Quantity:").pack(side="left")
        self.quantity_entry = ttk.Entry(sale_input_frame)
        self.quantity_entry.pack(side="left", padx=5)

        ttk.Button(sale_input_frame, text="Record Sale", command=self.record_sale).pack(
            side="left", padx=5
        )

        # Sales history
        ttk.Label(
            sales_frame, text="Riwayat Transaksi", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        sales_tree_frame = ttk.Frame(sales_frame)
        sales_tree_frame.pack(fill="both", expand=True, padx=5)

        self.sales_tree = ttk.Treeview(
            sales_tree_frame,
            columns=("Date", "Product", "Quantity", "Total"),
            show="headings",
        )
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Product", text="Product")
        self.sales_tree.heading("Quantity", text="Quantity")
        self.sales_tree.heading("Total", text="Total")

        # Set sales columns width
        self.sales_tree.column("Date", width=150)
        self.sales_tree.column("Product", width=200)
        self.sales_tree.column("Quantity", width=100)
        self.sales_tree.column("Total", width=150)

        sales_scrollbar = ttk.Scrollbar(
            sales_tree_frame, orient="vertical", command=self.sales_tree.yview
        )
        self.sales_tree.configure(yscrollcommand=sales_scrollbar.set)

        self.sales_tree.pack(side="left", fill="both", expand=True)
        sales_scrollbar.pack(side="right", fill="y")

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.refresh_product_list)

    def log_action(self, action: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"logs/inventory_{datetime.now().strftime('%Y%m%d')}.log"
        log_entry = f"[{timestamp}] {action}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def add_product(self):
        try:
            name = self.name_entry.get().strip()
            price = Decimal(self.price_entry.get())
            stock = int(self.stock_entry.get())

            if not name:
                raise ValueError("Nama product harus diisi!")
            if price <= 0:
                raise ValueError("Price harus bernilai positif")
            if stock < 0:
                raise ValueError("Stock tidak boleh negatif")

            self.products[name] = {"price": price, "stock": stock}

            # Catat log
            self.log_action(
                f"Produk baru ditambahkan: {name} (Price: Rp{price:,}, Stock: {stock})"
            )

            # Hapus form input
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)

            self.refresh_product_list()
            self.save_data()
            messagebox.showinfo("Success", "Produk berhasil disimpan.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_tree_double_click(self, event):
        """double click"""
        selection = self.products_tree.selection()

        if not selection:
            return

        item = selection[0]
        name = self.products_tree.item(item)["values"][0]
        self.edit_product(name)

    def edit_product(self, name):
        """Edit existing product"""
        if name not in self.products:
            return

        # buat window edit
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Ubah Product: {name}")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # munculkan form
        ttk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, str(self.products[name]["price"]))
        price_entry.pack(pady=5)

        ttk.Label(dialog, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.insert(0, str(self.products[name]["stock"]))
        stock_entry.pack(pady=5)

        def save_changes():
            try:
                new_price = Decimal(price_entry.get())
                new_stock = int(stock_entry.get())

                if new_price <= 0:
                    raise ValueError("Price harus bernilai positif")
                if new_stock < 0:
                    raise ValueError("Stock tidak boleh negatif")

                old_values = self.products[name].copy()
                self.products[name]["price"] = new_price
                self.products[name]["stock"] = new_stock

                self.log_action(
                    f"Edited product: {name}\n"
                    f"  Price: Rp{old_values['price']:,} → Rp{new_price:,}\n"
                    f"  Stock: {old_values['stock']} → {new_stock}"
                )

                self.refresh_product_list()
                self.save_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Product berhasil diubah.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def delete_this_product():
            dialog.destroy()
            self.delete_product(name)

        # Add buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Delete Product", command=delete_this_product).pack(
            side="left", padx=5
        )

    def delete_product(self, name):
        """Delete product"""
        if name in self.products:
            if messagebox.askyesno(
                "Konfirmasi Penghapusan", f"Apakah kamu yakin ingin menghapus {name}?"
            ):
                product_info = self.products[name]
                del self.products[name]
                self.log_action(
                    f"Deleted product: {name} "
                    f"(Price: Rp{product_info['price']:,}, "
                    f"Stock: {product_info['stock']})"
                )
                self.refresh_product_list()
                self.save_data()
                messagebox.showinfo("Success", "Product berhasil terhapus!")

    def record_sale(self):
        try:
            product_name = self.sale_product_var.get()
            quantity = int(self.quantity_entry.get())
            sale_date = self.date_picker.get_date()

            if not product_name in self.products:
                raise ValueError("Pilih produk yang tersedia")
            if quantity <= 0:
                raise ValueError("Quantity harus bernilai positif")

            current_stock = self.products[product_name]["stock"]
            if quantity > current_stock:
                raise ValueError(
                    f"Stock tidak mencukupi!\n"
                    f"Diminta: {quantity}pcs\n"
                    f"Tersedia: {current_stock}pcs"
                )

            # Calculate total
            total = self.products[product_name]["price"] * quantity

            # Update stock
            old_stock = current_stock
            self.products[product_name]["stock"] -= quantity

            # Record transaction
            self.transactions.append(
                {
                    "date": sale_date,
                    "product": product_name,
                    "quantity": quantity,
                    "total": total,
                }
            )

            # Log the action
            self.log_action(
                f"Recorded sale: {product_name}\n"
                f"  Date: {sale_date.strftime('%Y-%m-%d')}\n"
                f"  Quantity: {quantity}\n"
                f"  Total: Rp{total:,}\n"
                f"  Stock: {old_stock} → {self.products[product_name]['stock']}"
            )

            # Clear entries
            self.sale_product_var.set("")
            self.quantity_entry.delete(0, tk.END)

            self.refresh_product_list()
            self.refresh_sales_list()
            self.save_data()

            messagebox.showinfo(
                "Transaksi Berhasil",
                f"Transaksi berhasil disimpan!\n\n"
                f"Date: {sale_date.strftime('%Y-%m-%d')}\n"
                f"Product: {product_name}\n"
                f"Quantity: {quantity}\n"
                f"Total: Rp{total:,}\n"
                f"Remaining Stock: {self.products[product_name]['stock']}",
            )

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_product_list(self, event=None):
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Refresh products list
        for name, data in self.products.items():
            self.products_tree.insert(
                "",
                "end",
                values=(
                    name,
                    f"Rp{data['price']:,}",
                    data["stock"],
                    "Double-click untuk edit",
                ),
            )

        # Update combobox values
        self.sale_product_combo["values"] = list(self.products.keys())

    def refresh_sales_list(self):
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        # Sort transactions by date, newest first
        sorted_transactions = sorted(
            self.transactions, key=lambda x: x["date"], reverse=True
        )

        # Refresh sales list
        for transaction in sorted_transactions:
            self.sales_tree.insert(
                "",
                "end",
                values=(
                    transaction["date"].strftime("%Y-%m-%d"),
                    transaction["product"],
                    transaction["quantity"],
                    f"Rp{transaction['total']:,}",
                ),
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SimpleInventory()
    app.run()
