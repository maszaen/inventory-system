import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from decimal import Decimal
from tkcalendar import DateEntry
import random
import string


class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inventory System")
        self.root.geometry("1000x600")

        self.products = {}
        self.transactions = []

        for directory in ["logs", "inventory"]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        self.load_data()
        self.setup_ui()

    def load_data(self):
        if os.path.exists("inventory/products.json"):
            with open("inventory/products.json", "r") as f:
                self.products = json.load(f)

                for product_data in self.products.values():
                    product_data["price"] = Decimal(str(product_data["price"]))

        if os.path.exists("inventory/sales.json"):
            with open("inventory/sales.json", "r") as f:
                self.transactions = json.load(f)

                for transaction in self.transactions:
                    transaction["date"] = datetime.strptime(
                        transaction["date"], "%Y-%m-%d"
                    ).date()
                    transaction["total"] = Decimal(str(transaction["total"]))

    def save_data(self):
        with open("inventory/products.json", "w") as f:
            json.dump(self.products, f, default=str)

        with open("inventory/sales.json", "w") as f:
            json.dump(self.transactions, f, default=str)

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # === TAB PRODUCTS ===
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="Products")

        # Section tambah produk
        ttk.Label(
            products_frame, text="Tambahkan Product", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        # Form input produk
        input_frame = ttk.Frame(products_frame)
        input_frame.pack(fill="x", padx=5)

        # Field nama produk
        ttk.Label(input_frame, text="Name:").pack(side="left")
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.pack(side="left", padx=5)

        # Field harga
        ttk.Label(input_frame, text="Price:").pack(side="left")
        self.price_entry = ttk.Entry(input_frame)
        self.price_entry.pack(side="left", padx=5)

        # Field stok
        ttk.Label(input_frame, text="Stock:").pack(side="left")
        self.stock_entry = ttk.Entry(input_frame)
        self.stock_entry.pack(side="left", padx=5)

        # Tombol Add Product
        ttk.Button(input_frame, text="Add Product", command=self.add_product).pack(
            side="left", padx=5
        )

        # Tombol Edit Product
        ttk.Button(input_frame, text="Edit Data", command=self.edit_selected_data).pack(
            side="right", padx=5
        )

        # Tabel produk dengan scrollbar
        ttk.Label(
            products_frame, text="List Product", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        tree_frame = ttk.Frame(products_frame)
        tree_frame.pack(fill="both", expand=True, padx=5)

        # Setup tabel produk dengan border
        self.products_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Price", "Stock"),
            show="headings",
            style="Custom.Treeview",
        )
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Stock", text="Stock")

        # Adjust column widths
        self.products_tree.column("ID", width=100)
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Price", width=150)
        self.products_tree.column("Stock", width=100)

        # Tambah scrollbar ke tabel
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.products_tree.yview
        )
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # === TAB SALES ===
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="Sales")

        # Form input penjualan
        sale_input_frame = ttk.Frame(sales_frame)
        sale_input_frame.pack(fill="x", padx=5, pady=5)

        # Field tanggal
        ttk.Label(sale_input_frame, text="Date:").pack(side="left")
        self.date_picker = DateEntry(
            sale_input_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.date_picker.pack(side="left", padx=5)

        # Dropdown pilih produk
        ttk.Label(sale_input_frame, text="Product:").pack(side="left")
        self.sale_product_var = tk.StringVar()
        self.sale_product_combo = ttk.Combobox(
            sale_input_frame, textvariable=self.sale_product_var
        )
        self.sale_product_combo.pack(side="left", padx=5)

        # Field quantity
        ttk.Label(sale_input_frame, text="Quantity:").pack(side="left")
        self.quantity_entry = ttk.Entry(sale_input_frame)
        self.quantity_entry.pack(side="left", padx=5)

        # Tombol Record Sale
        ttk.Button(sale_input_frame, text="Record Sale", command=self.record_sale).pack(
            side="left", padx=5
        )

        # Tabel history transaksi
        ttk.Label(
            sales_frame, text="Riwayat Transaksi", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        sales_tree_frame = ttk.Frame(sales_frame)
        sales_tree_frame.pack(fill="both", expand=True, padx=5)

        # Setup tabel transaksi
        self.sales_tree = ttk.Treeview(
            sales_tree_frame,
            columns=("ID", "Date", "Product", "Quantity", "Total"),
            show="headings",
        )
        self.sales_tree.heading("ID", text="ID")
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Product", text="Product")
        self.sales_tree.heading("Quantity", text="Quantity")
        self.sales_tree.heading("Total", text="Total")

        # Adjust sales column widths
        self.sales_tree.column("ID", width=100)
        self.sales_tree.column("Date", width=150)
        self.sales_tree.column("Product", width=200)
        self.sales_tree.column("Quantity", width=100)
        self.sales_tree.column("Total", width=150)

        # Tambah scrollbar ke tabel transaksi
        sales_scrollbar = ttk.Scrollbar(
            sales_tree_frame, orient="vertical", command=self.sales_tree.yview
        )
        self.sales_tree.configure(yscrollcommand=sales_scrollbar.set)

        self.sales_tree.pack(side="left", fill="both", expand=True)
        sales_scrollbar.pack(side="right", fill="y")

        # Bind event saat ganti tab
        self.notebook.bind("<<NotebookTabChanged>>", self.refresh_product_list)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # === TAB SEARCH ===
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search")

        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill="x", padx=5, pady=5)

        # Dropdown untuk jenis pencarian
        ttk.Label(search_input_frame, text="Search By:").pack(side="left", padx=5)
        self.search_type_var = tk.StringVar(value="Product")
        search_type_combo = ttk.Combobox(
            search_input_frame,
            textvariable=self.search_type_var,
            values=["Product", "Transaction"],
        )
        search_type_combo.pack(side="left", padx=5)

        # Input keyword
        ttk.Label(search_input_frame, text="Keyword:").pack(side="left", padx=5)
        self.search_keyword_entry = ttk.Entry(search_input_frame)
        self.search_keyword_entry.pack(side="left", padx=5)

        # Tombol Search
        ttk.Button(search_input_frame, text="Search", command=self.search_data).pack(
            side="left", padx=5
        )

        # Tabel hasil pencarian
        search_result_frame = ttk.Frame(search_frame)
        search_result_frame.pack(fill="both", expand=True, padx=5)

        self.search_tree = ttk.Treeview(search_result_frame, show="headings")
        self.search_tree.pack(side="left", fill="both", expand=True)

        search_scrollbar = ttk.Scrollbar(
            search_result_frame, orient="vertical", command=self.search_tree.yview
        )
        self.search_tree.configure(yscrollcommand=search_scrollbar.set)
        search_scrollbar.pack(side="right", fill="y")

        # Inisialisasi kolom tabel hasil pencarian
        self.update_search_table("Product")

        # Event handler untuk dropdown search type
        search_type_combo.bind("<<ComboboxSelected>>", self.update_search_table)

        # === TAB SUMMARY ===
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Summary")

        date_frame = ttk.Frame(summary_frame)
        date_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(date_frame, text="Start Date:").pack(side="left", padx=5)
        self.start_date = DateEntry(
            date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.start_date.pack(side="left", padx=5)

        ttk.Label(date_frame, text="End Date:").pack(side="left", padx=5)
        self.end_date = DateEntry(
            date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.end_date.pack(side="left", padx=5)

        ttk.Button(
            date_frame, text="Generate Summary", command=self.generate_summary
        ).pack(side="left", padx=5)

        self.summary_text = tk.Text(summary_frame, height=20, width=60)
        self.summary_text.pack(padx=5, pady=5, fill="both", expand=True)

    def generate_short_id(self, length=6):
        characters = string.ascii_uppercase + string.digits
        return "".join(random.choices(characters, k=length))

    def generate_summary(self):
        try:
            start_date = self.start_date.get_date()
            end_date = self.end_date.get_date()

            if start_date > end_date:
                raise ValueError("Tanggal mulai tidak boleh setelah tanggal akhir.")

            filtered_transactions = [
                transaction
                for transaction in self.transactions
                if start_date <= transaction["date"] <= end_date
            ]

            total_amount = sum(t["total"] for t in filtered_transactions)

            product_summary = {}
            for transaction in filtered_transactions:
                product = transaction["product"]
                if product not in product_summary:
                    product_summary[product] = {"quantity": 0, "total": Decimal("0")}
                product_summary[product]["quantity"] += transaction["quantity"]
                product_summary[product]["total"] += transaction["total"]

            # Clear previous summary
            self.summary_text.delete(1.0, tk.END)

            # Display summary
            summary = f"Summary Report ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})\n"
            summary += "=" * 50 + "\n\n"

            summary += f"Total Transactions: {len(filtered_transactions)}\n"
            summary += f"Total Amount: Rp{total_amount:,}\n\n"

            summary += "Sales Detail:\n"
            summary += "-" * 50 + "\n"
            for product, data in product_summary.items():
                summary += f"\nProduct: {product}\n"
                summary += f"Total Quantity Sold: {data['quantity']}\n"
                summary += f"Total Amount: Rp{data['total']:,}\n"

            self.summary_text.insert(1.0, summary)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def log_action(self, action: str):
        # Fungsi untuk mencatat semua aktivitas ke file log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"logs/inventory_{datetime.now().strftime('%Y%m%d')}.log"
        log_entry = f"[{timestamp}] {action}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def update_search_table(self, event=None):
        search_type = self.search_type_var.get()
        if search_type == "Product":
            self.search_tree["columns"] = ("ID", "Name", "Price", "Stock")
            self.search_tree.heading("ID", text="ID")
            self.search_tree.heading("Name", text="Name")
            self.search_tree.heading("Price", text="Price")
            self.search_tree.heading("Stock", text="Stock")
            self.search_tree.column("ID", width=100)
            self.search_tree.column("Name", width=200)
            self.search_tree.column("Price", width=150)
            self.search_tree.column("Stock", width=100)
        elif search_type == "Transaction":
            self.search_tree["columns"] = ("ID", "Date", "Product", "Quantity", "Total")
            self.search_tree.heading("ID", text="ID")
            self.search_tree.heading("Date", text="Date")
            self.search_tree.heading("Product", text="Product")
            self.search_tree.heading("Quantity", text="Quantity")
            self.search_tree.heading("Total", text="Total")
            self.search_tree.column("ID", width=100)
            self.search_tree.column("Date", width=150)
            self.search_tree.column("Product", width=200)
            self.search_tree.column("Quantity", width=100)
            self.search_tree.column("Total", width=150)

    def search_data(self):
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        search_type = self.search_type_var.get()
        keyword = self.search_keyword_entry.get().strip().lower()

        if search_type == "Product":
            results = []
            for product_id, data in self.products.items():
                if keyword in data["name"].lower():
                    results.append(
                        (
                            product_id[:8],
                            data["name"],
                            f"Rp{data['price']:,}",
                            data["stock"],
                        )
                    )
        elif search_type == "Transaction":
            results = []
            for t in self.transactions:
                if keyword in t["product"].lower():
                    results.append(
                        (
                            t["id"][:8],
                            t["date"].strftime("%Y-%m-%d"),
                            t["product"],
                            t["quantity"],
                            f"Rp{t['total']:,}",
                        )
                    )

        for result in results:
            self.search_tree.insert("", "end", values=result)

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

            # Validasi duplikat data
            for _, data in self.products.items():
                if data["name"].lower() == name.lower():
                    raise ValueError("Product dengan nama tersebut sudah ada!")

            product_id = self.generate_short_id()
            while product_id in self.products:
                product_id = self.generate_short_id()

            self.products[product_id] = {"name": name, "price": price, "stock": stock}

            self.log_action(
                f"Produk baru ditambahkan: {name} (ID: {product_id}, Price: Rp {price:,}, Stock: {stock})"
            )

            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)

            self.refresh_product_list()
            self.save_data()
            messagebox.showinfo("Success", "Produk berhasil disimpan.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def edit_selected_data(self):
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Pilih produk yang ingin diubah.")
            return

        item = selection[0]
        values = self.products_tree.item(item)["values"]
        product_id = values[0]

        if product_id in self.products:
            self.edit_product(product_id)

    def edit_product(self, product_id):
        if product_id not in self.products:
            return

        product_data = self.products[product_id]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Ubah Product: {product_data['name']}")
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.insert(0, product_data["name"])
        name_entry.pack(pady=5)

        ttk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.insert(0, str(product_data["price"]))
        price_entry.pack(pady=5)

        ttk.Label(dialog, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.insert(0, str(product_data["stock"]))
        stock_entry.pack(pady=5)

        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_price = Decimal(price_entry.get())
                new_stock = int(stock_entry.get())

                if not new_name:
                    raise ValueError("Nama product harus diisi!")
                if new_price <= 0:
                    raise ValueError("Price harus bernilai positif")
                if new_stock < 0:
                    raise ValueError("Stock tidak boleh negatif")

                # Check for duplicate names, excluding current product
                for pid, data in self.products.items():
                    if pid != product_id and data["name"].lower() == new_name.lower():
                        raise ValueError("Product dengan nama tersebut sudah ada!")

                old_values = self.products[product_id].copy()
                self.products[product_id].update(
                    {"name": new_name, "price": new_price, "stock": new_stock}
                )

                self.log_action(
                    f"Edited product ID: {product_id}\n"
                    f"  Name: {old_values['name']} → {new_name}\n"
                    f"  Price: Rp {old_values['price']:,} → Rp {new_price:,}\n"
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
            self.delete_product(product_id)

        # Tombol Save dan Delete
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Simpan", command=save_changes).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Hapus Produk", command=delete_this_product).pack(
            side="left", padx=5
        )

    def delete_product(self, product_id):
        if product_id in self.products:
            product_data = self.products[product_id]
            if messagebox.askyesno(
                "Konfirmasi Penghapusan",
                f"Apakah kamu yakin ingin menghapus {product_data['name']}?",
            ):
                # Log deletion before deleting
                self.log_action(
                    f"Deleted product: {product_data['name']} "
                    f"(ID: {product_id}, "
                    f"Price: Rp {product_data['price']:,}, "
                    f"Stock: {product_data['stock']})"
                )
                del self.products[product_id]
                self.refresh_product_list()
                self.save_data()
                messagebox.showinfo("Success", "Product berhasil terhapus!")

    def record_sale(self):
        try:
            product_name = self.sale_product_var.get()
            quantity = int(self.quantity_entry.get())
            sale_date = self.date_picker.get_date()

            # Find product ID by name
            product_id = None
            for pid, data in self.products.items():
                if data["name"] == product_name:
                    product_id = pid
                    break

            if not product_id:
                raise ValueError("Pilih produk yang tersedia")
            if quantity <= 0:
                raise ValueError("Quantity harus bernilai positif")

            current_stock = self.products[product_id]["stock"]
            if quantity > current_stock:
                raise ValueError(
                    f"Stock tidak mencukupi!\n"
                    f"Diminta: {quantity}pcs\n"
                    f"Tersedia: {current_stock}pcs"
                )

            total = self.products[product_id]["price"] * quantity
            old_stock = current_stock
            self.products[product_id]["stock"] -= quantity

            # Generate short transaction ID
            transaction_id = self.generate_short_id()
            while any(t["id"] == transaction_id for t in self.transactions):
                transaction_id = self.generate_short_id()

            self.transactions.append(
                {
                    "id": transaction_id,
                    "date": sale_date,
                    "product_id": product_id,
                    "product": product_name,
                    "quantity": quantity,
                    "total": total,
                }
            )

            self.log_action(
                f"Recorded sale: ID: {transaction_id}\n"
                f"  Product: {product_name} (ID: {product_id})\n"
                f"  Date: {sale_date.strftime('%Y-%m-%d')}\n"
                f"  Quantity: {quantity}\n"
                f"  Total: Rp {total:,}\n"
                f"  Stock: {old_stock} → {self.products[product_id]['stock']}"
            )

            self.sale_product_var.set("")
            self.quantity_entry.delete(0, tk.END)

            self.refresh_product_list()
            self.refresh_sales_list()
            self.save_data()

            messagebox.showinfo(
                "Transaksi Berhasil",
                f"Transaksi berhasil disimpan!\n\n"
                f"Transaction ID: {transaction_id}\n"
                f"Date: {sale_date.strftime('%Y-%m-%d')}\n"
                f"Product: {product_name}\n"
                f"Quantity: {quantity}\n"
                f"Total: Rp{total:,}\n"
                f"Remaining Stock: {self.products[product_id]['stock']}",
            )

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_product_list(self, event=None):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        for product_id, data in self.products.items():
            self.products_tree.insert(
                "",
                "end",
                values=(
                    product_id,  # Now showing full ID since it's already short
                    data["name"],
                    f"Rp{data['price']:,}",
                    data["stock"],
                ),
            )

        # Update combobox with product names
        self.sale_product_combo["values"] = [
            data["name"] for data in self.products.values()
        ]

    def refresh_sales_list(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        sorted_transactions = sorted(
            self.transactions, key=lambda x: x["date"], reverse=True
        )

        for transaction in sorted_transactions:
            self.sales_tree.insert(
                "",
                "end",
                values=(
                    transaction["id"],  # Now showing full ID since it's already short
                    transaction["date"].strftime("%Y-%m-%d"),
                    transaction["product"],
                    transaction["quantity"],
                    f"Rp{transaction['total']:,}",
                ),
            )

    def run(self):
        # Jalankan aplikasi
        self.root.mainloop()


if __name__ == "__main__":
    app = Main()  # Buat instance aplikasi
    app.run()
