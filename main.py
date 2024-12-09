import json  # Untuk handle data JSON (save/load)
import os  # Untuk handle file dan folder
import tkinter as tk  # Library utama untuk GUI
from tkinter import ttk, messagebox  # ttk untuk widget, messagebox untuk popup
from datetime import datetime  # Untuk handle tanggal dan waktu
from decimal import Decimal  # Untuk handle angka desimal (uang)
from tkcalendar import DateEntry  # Widget calendar untuk pilih tanggal


class Main:
    def __init__(self):
        # Inisialisasi window utama
        self.root = tk.Tk()
        self.root.title("Inventory System")
        self.root.geometry("1000x600")  # Set ukuran window 1000x600 pixel

        # Inisialisasi dictionary untuk nyimpen data
        self.products = {}  # Untuk data produk
        self.transactions = []  # Untuk data transaksi

        # Bikin folder logs dan inventory kalo belum ada
        for directory in ["logs", "inventory"]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Load data dari file JSON
        self.load_data()

        # Setup User Interface
        self.setup_ui()

        # Refresh tampilan saat startup
        self.refresh_product_list()
        self.refresh_sales_list()

    def load_data(self):
        # Load data produk dari JSON
        if os.path.exists("inventory/products.json"):
            with open("inventory/products.json", "r") as f:
                self.products = json.load(f)
                # Convert harga ke Decimal untuk akurasi
                self.products = {
                    k: {"price": Decimal(str(v["price"])), "stock": v["stock"]}
                    for k, v in self.products.items()
                }

        # Load data transaksi dari JSON
        if os.path.exists("inventory/sales.json"):
            with open("inventory/sales.json", "r") as f:
                self.transactions = json.load(f)
                # Convert data: tanggal ke datetime, total ke Decimal
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
        # Simpan data produk ke JSON
        with open("inventory/products.json", "w") as f:
            json.dump(self.products, f, default=str)

        # Simpan data transaksi ke JSON
        with open("inventory/sales.json", "w") as f:
            json.dump(self.transactions, f, default=str)

    def setup_ui(self):
        # Bikin notebook (container untuk tab)
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

        # Tabel produk dengan scrollbar
        ttk.Label(
            products_frame, text="List Product", font=("Helvetica", 12, "bold")
        ).pack(pady=5)

        tree_frame = ttk.Frame(products_frame)
        tree_frame.pack(fill="both", expand=True, padx=5)

        # Setup tabel produk
        self.products_tree = ttk.Treeview(
            tree_frame, columns=("Name", "Price", "Stock", "Actions"), show="headings"
        )
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Stock", text="Stock")
        self.products_tree.heading("Actions", text="Actions")

        # Set lebar kolom
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Price", width=150)
        self.products_tree.column("Stock", width=100)
        self.products_tree.column("Actions", width=200)

        # Tambah scrollbar ke tabel
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.products_tree.yview
        )
        self.products_tree.configure(yscrollcommand=scrollbar.set)

        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind event double click untuk edit produk
        self.products_tree.bind("<Double-1>", self.on_tree_double_click)

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
            columns=("Date", "Product", "Quantity", "Total"),
            show="headings",
        )
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Product", text="Product")
        self.sales_tree.heading("Quantity", text="Quantity")
        self.sales_tree.heading("Total", text="Total")

        # Set lebar kolom transaksi
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

    def log_action(self, action: str):
        # Fungsi untuk mencatat semua aktivitas ke file log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"logs/inventory_{datetime.now().strftime('%Y%m%d')}.log"
        log_entry = f"[{timestamp}] {action}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def add_product(self):
        try:
            # Ambil input dari form
            name = self.name_entry.get().strip()
            price = Decimal(self.price_entry.get())
            stock = int(self.stock_entry.get())

            # Validasi input
            if not name:
                raise ValueError("Nama product harus diisi!")
            if price <= 0:
                raise ValueError("Price harus bernilai positif")
            if stock < 0:
                raise ValueError("Stock tidak boleh negatif")

            # Simpan ke dictionary products
            self.products[name] = {"price": price, "stock": stock}

            # Catat ke log
            self.log_action(
                f"Produk baru ditambahkan: {name} (Price: Rp {price:,}, Stock: {stock})"
            )

            # Clear form
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)

            # Refresh tampilan & save data
            self.refresh_product_list()
            self.save_data()
            messagebox.showinfo("Success", "Produk berhasil disimpan.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def on_tree_double_click(self, event):
        # Handle double click di tabel produk
        selection = self.products_tree.selection()  # Ambil item yang dipilih
        if not selection:  # Kalo ga ada yang kepilih, stop
            return

        item = selection[0]  # Ambil item pertama yang dipilih
        name = self.products_tree.item(item)["values"][0]  # Ambil nama produk
        self.edit_product(name)  # Buka dialog edit

    def edit_product(self, name):
        # Handle edit produk yang sudah ada
        if name not in self.products:
            return

        # Bikin window dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Ubah Product: {name}")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()  # Bikin dialog modal

        # Form edit
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
                # Ambil input baru
                new_price = Decimal(price_entry.get())
                new_stock = int(stock_entry.get())

                # Validasi
                if new_price <= 0:
                    raise ValueError("Price harus bernilai positif")
                if new_stock < 0:
                    raise ValueError("Stock tidak boleh negatif")

                # Simpan perubahan
                old_values = self.products[name].copy()
                self.products[name]["price"] = new_price
                self.products[name]["stock"] = new_stock

                # Catat ke log
                self.log_action(
                    f"Edited product: {name}\n"
                    f"  Price: Rp {old_values['price']:,} → Rp {new_price:,}\n"
                    f"  Stock: {old_values['stock']} → {new_stock}"
                )

                # Refresh & save
                self.refresh_product_list()
                self.save_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Product berhasil diubah.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        def delete_this_product():
            dialog.destroy()
            self.delete_product(name)

        # Tombol Save dan Delete
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Delete Product", command=delete_this_product).pack(
            side="left", padx=5
        )

    def delete_product(self, name):
        # Handle delete produk
        if name in self.products:
            if messagebox.askyesno(
                "Konfirmasi Penghapusan", f"Apakah kamu yakin ingin menghapus {name}?"
            ):
                product_info = self.products[name]
                del self.products[name]
                # Catat ke log
                self.log_action(
                    f"Deleted product: {name} "
                    f"(Price: Rp {product_info['price']:,}, "
                    f"Stock: {product_info['stock']})"
                )
                self.refresh_product_list()
                self.save_data()
                messagebox.showinfo("Success", "Product berhasil terhapus!")

    def record_sale(self):
        try:
            # Ambil input penjualan
            product_name = self.sale_product_var.get()  # Nama produk dari dropdown
            quantity = int(self.quantity_entry.get())  # Jumlah yang dijual
            sale_date = self.date_picker.get_date()  # Tanggal dari date picker

            # Validasi input
            if not product_name in self.products:
                raise ValueError("Pilih produk yang tersedia")
            if quantity <= 0:
                raise ValueError("Quantity harus bernilai positif")

            # Cek stok cukup tidak
            current_stock = self.products[product_name]["stock"]
            if quantity > current_stock:
                raise ValueError(
                    f"Stock tidak mencukupi!\n"
                    f"Diminta: {quantity}pcs\n"
                    f"Tersedia: {current_stock}pcs"
                )

            # Hitung total penjualan
            total = self.products[product_name]["price"] * quantity

            # Update stok
            old_stock = current_stock
            self.products[product_name]["stock"] -= quantity

            # Catat transaksi
            self.transactions.append(
                {
                    "date": sale_date,
                    "product": product_name,
                    "quantity": quantity,
                    "total": total,
                }
            )

            # Catat ke log file
            self.log_action(
                f"Recorded sale: {product_name}\n"
                f"  Date: {sale_date.strftime('%Y-%m-%d')}\n"
                f"  Quantity: {quantity}\n"
                f"  Total: Rp {total:,}\n"
                f"  Stock: {old_stock} → {self.products[product_name]['stock']}"
            )

            # Clear form input
            self.sale_product_var.set("")
            self.quantity_entry.delete(0, tk.END)

            # Refresh tampilan & save data
            self.refresh_product_list()
            self.refresh_sales_list()
            self.save_data()

            # Tampilkan notifikasi sukses
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
        # Clear semua item di tabel produk
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        # Refresh list produk
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

        # Update nilai di combobox produk
        self.sale_product_combo["values"] = list(self.products.keys())

    def refresh_sales_list(self):
        # Clear semua item di tabel sales
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        # Sort transaksi berdasarkan tanggal terbaru
        sorted_transactions = sorted(
            self.transactions, key=lambda x: x["date"], reverse=True
        )

        # Refresh list penjualan
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
        # Jalankan aplikasi
        self.root.mainloop()


if __name__ == "__main__":
    app = Main()  # Buat instance aplikasi
    app.run()
