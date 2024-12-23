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
        self.refresh_product_list()
        self.refresh_sales_list()

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
        style = ttk.Style()
        style.configure(
            "Custom.Treeview.Heading",
            font=("Arial", 10, "bold"),
        )
        style.configure("Custom.Treeview", font=("Arial", 10))
        style.configure("Test.Treeview", font=("Arial", 10), anchor="center")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # === TAB PRODUCTS ===
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="Products")

        # Products control frame
        control_frame = ttk.Frame(products_frame)
        control_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            control_frame, text="Add Product", command=self.show_add_product_dialog
        ).pack(side="left", padx=5)

        ttk.Label(control_frame, text="Search:").pack(side="left", padx=5)
        self.product_search_entry = ttk.Entry(control_frame)
        self.product_search_entry.pack(side="left", padx=5)
        self.product_search_entry.bind("<KeyRelease>", self.refresh_product_list)

        self.delete_product_button = ttk.Button(
            control_frame,
            text="Delete",
            command=self.delete_selected_product,
            state="disabled",
        )
        self.delete_product_button.pack(side="right", padx=5)

        self.edit_product_button = ttk.Button(
            control_frame,
            text="Edit",
            command=self.edit_selected_data,
            state="disabled",
        )
        self.edit_product_button.pack(side="right", padx=5)

        # Products table
        product_tree_frame = ttk.Frame(products_frame)
        product_tree_frame.pack(fill="both", expand=True, padx=5)

        self.products_tree = ttk.Treeview(
            product_tree_frame,
            columns=("ID", "Name", "Price", "Stock"),
            show="headings",
            style="Custom.Treeview",
        )
        self.products_tree.heading("ID", text="ID")
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Price", text="Price")
        self.products_tree.heading("Stock", text="Stock")

        self.products_tree.column("ID", width=100)
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Price", width=150)
        self.products_tree.column("Stock", width=100)

        self.products_tree.bind("<<TreeviewSelect>>", self.on_product_select)

        product_scrollbar = ttk.Scrollbar(
            product_tree_frame, orient="vertical", command=self.products_tree.yview
        )
        self.products_tree.configure(yscrollcommand=product_scrollbar.set)
        self.products_tree.pack(side="left", fill="both", expand=True)
        self.products_tree.tag_configure("center", anchor="center")

        for product_col in self.products_tree["columns"]:
            if product_col == "Stock":
                self.products_tree.column(product_col, anchor="center")

        product_scrollbar.pack(side="right", fill="y")

        # === TAB SALES ===
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="Sales")

        # Sales control frame
        sales_control_frame = ttk.Frame(sales_frame)
        sales_control_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            sales_control_frame, text="Add Sale", command=self.show_add_sale_dialog
        ).pack(side="left", padx=5)

        ttk.Label(sales_control_frame, text="Search:").pack(side="left", padx=5)
        self.sales_search_entry = ttk.Entry(sales_control_frame)
        self.sales_search_entry.pack(side="left", padx=5)
        self.sales_search_entry.bind("<KeyRelease>", self.refresh_sales_list)

        self.delete_sale_button = ttk.Button(
            sales_control_frame,
            text="Delete",
            command=self.delete_selected_sale,
            state="disabled",
        )
        self.delete_sale_button.pack(side="right", padx=5)

        self.edit_sale_button = ttk.Button(
            sales_control_frame,
            text="Edit",
            command=self.edit_selected_sale,
            state="disabled",
        )
        self.edit_sale_button.pack(side="right", padx=5)

        # Sales table
        sales_tree_frame = ttk.Frame(sales_frame)
        sales_tree_frame.pack(fill="both", expand=True, padx=5)

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

        self.sales_tree.column("ID", width=100)
        self.sales_tree.column("Date", width=150)
        self.sales_tree.column("Product", width=200)
        self.sales_tree.column("Quantity", width=100)
        self.sales_tree.column("Total", width=150)

        sales_scrollbar = ttk.Scrollbar(
            sales_tree_frame, orient="vertical", command=self.sales_tree.yview
        )
        self.sales_tree.configure(yscrollcommand=sales_scrollbar.set)
        self.sales_tree.pack(side="left", fill="both", expand=True)
        self.sales_tree.tag_configure("center", anchor="center")

        sales_scrollbar.pack(side="right", fill="y")

        for sale_col in self.sales_tree["columns"]:
            if sale_col == "Quantity":
                self.sales_tree.column(sale_col, anchor="center")

        self.sales_tree.bind("<<TreeviewSelect>>", self.on_sale_select)

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
                raise ValueError("Start date cannot be after end date.")

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

            self.summary_text.delete(1.0, tk.END)

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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = f"logs/inventory_{datetime.now().strftime('%Y%m%d')}.log"
        log_entry = f"[{timestamp}] {action}\n"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def show_add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)

        ttk.Label(dialog, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(dialog)
        price_entry.pack(pady=5)

        ttk.Label(dialog, text="Stock:").pack(pady=5)
        stock_entry = ttk.Entry(dialog)
        stock_entry.pack(pady=5)

        def save_product():
            try:
                name = name_entry.get().strip()
                price = Decimal(price_entry.get())
                stock = int(stock_entry.get())

                if not name:
                    raise ValueError("Product name is required!")
                if price <= 0:
                    raise ValueError("Price must be positive")
                if stock < 0:
                    raise ValueError("Stock cannot be negative")

                for _, data in self.products.items():
                    if data["name"].lower() == name.lower():
                        raise ValueError("Product with this name already exists!")

                product_id = self.generate_short_id()
                while product_id in self.products:
                    product_id = self.generate_short_id()

                self.products[product_id] = {
                    "name": name,
                    "price": price,
                    "stock": stock,
                }

                self.log_action(
                    f"New product added: {name} (ID: {product_id}, Price: Rp {price:,}, Stock: {stock})"
                )

                self.refresh_product_list()
                self.save_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Product saved successfully.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_product).pack(pady=20)

    def show_add_sale_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Sale")
        dialog.geometry("300x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Date:").pack(pady=5)
        date_picker = DateEntry(
            dialog, width=12, background="darkblue", foreground="white", borderwidth=2
        )
        date_picker.pack(pady=5)

        ttk.Label(dialog, text="Product:").pack(pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(
            dialog,
            textvariable=product_var,
            values=[data["name"] for data in self.products.values()],
        )
        product_combo.pack(pady=5)

        ttk.Label(dialog, text="Quantity:").pack(pady=5)
        quantity_entry = ttk.Entry(dialog)
        quantity_entry.pack(pady=5)

        def save_sale():
            try:
                product_name = product_var.get()
                quantity = int(quantity_entry.get())
                sale_date = date_picker.get_date()

                product_id = None
                for pid, data in self.products.items():
                    if data["name"] == product_name:
                        product_id = pid
                        break

                if not product_id:
                    raise ValueError("Please select a product")
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")

                current_stock = self.products[product_id]["stock"]
                if quantity > current_stock:
                    raise ValueError(
                        f"Insufficient stock!\nRequested: {quantity}\nAvailable: {current_stock}"
                    )

                total = self.products[product_id]["price"] * quantity
                old_stock = current_stock
                self.products[product_id]["stock"] -= quantity

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
                    f"Sale recorded: ID: {transaction_id}\n"
                    f"  Product: {product_name} (ID: {product_id})\n"
                    f"  Date: {sale_date.strftime('%Y-%m-%d')}\n"
                    f"  Quantity: {quantity}\n"
                    f"  Total: Rp {total:,}\n"
                    f"  Stock: {old_stock} → {self.products[product_id]['stock']}"
                )

                self.refresh_product_list()
                self.refresh_sales_list()
                self.save_data()
                dialog.destroy()

                messagebox.showinfo(
                    "Success",
                    f"Sale recorded successfully!\n\n"
                    f"Transaction ID: {transaction_id}\n"
                    f"Product: {product_name}\n"
                    f"Quantity: {quantity}\n"
                    f"Total: Rp{total:,}",
                )

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_sale).pack(pady=20)

    def edit_selected_data(self):
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a product to edit.")
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
        dialog.geometry("300x235")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (self.root.winfo_screenwidth() - dialog.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - dialog.winfo_reqheight()) // 2
        dialog.geometry(f"+{x}+{y}")
        dialog.title(f"Edit Product: {product_data['name']}")

        ttk.Label(dialog, text="Name:", width=32).pack()
        name_entry = ttk.Entry(dialog, width=32)
        name_entry.insert(0, product_data["name"])
        name_entry.pack(pady=(0, 7))

        ttk.Label(dialog, text="Price:", width=32).pack()
        price_entry = ttk.Entry(dialog, width=32)
        price_entry.insert(0, str(product_data["price"]))
        price_entry.pack(pady=(0, 7))

        ttk.Label(dialog, text="Stock:", width=32).pack()
        stock_entry = ttk.Entry(dialog, width=32)
        stock_entry.insert(0, str(product_data["stock"]))
        stock_entry.pack(pady=(0, 7))

        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_price = Decimal(price_entry.get())
                new_stock = int(stock_entry.get())

                if not new_name:
                    raise ValueError("Product name is required!")
                if new_price <= 0:
                    raise ValueError("Price must be positive")
                if new_stock < 0:
                    raise ValueError("Stock cannot be negative")

                for pid, data in self.products.items():
                    if pid != product_id and data["name"].lower() == new_name.lower():
                        raise ValueError("Product with this name already exists!")

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
                messagebox.showinfo("Success", "Product updated successfully.")

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_changes).pack(pady=20)

    def edit_selected_sale(self):
        selection = self.sales_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.sales_tree.item(item)["values"]
        transaction_id = values[0]

        transaction = None
        for t in self.transactions:
            if t["id"] == transaction_id:
                transaction = t
                break

        if not transaction:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Sale: {transaction_id}")
        dialog.geometry("300x235")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (self.root.winfo_screenwidth() - dialog.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - dialog.winfo_reqheight()) // 2
        dialog.geometry(f"+{x}+{y}")

        ttk.Label(dialog, text="Date:", width=32).pack()
        date_picker = DateEntry(
            dialog, width=30, background="darkblue", foreground="white", borderwidth=2
        )
        date_picker.set_date(transaction["date"])
        date_picker.pack(pady=(0, 7))

        ttk.Label(dialog, text="Product:", width=32).pack()
        product_var = tk.StringVar(value=transaction["product"])
        product_combo = ttk.Combobox(
            dialog,
            textvariable=product_var,
            width=30,
            values=[data["name"] for data in self.products.values()],
        )
        product_combo.pack(pady=(0, 7))

        ttk.Label(dialog, text="Quantity:", width=32).pack()
        quantity_entry = ttk.Entry(dialog, width=32)
        quantity_entry.insert(0, str(transaction["quantity"]))
        quantity_entry.pack(pady=(0, 7))

        def save_changes():
            try:
                new_product_name = product_var.get()
                new_quantity = int(quantity_entry.get())
                new_date = date_picker.get_date()

                new_product_id = None
                for pid, data in self.products.items():
                    if data["name"] == new_product_name:
                        new_product_id = pid
                        break

                if not new_product_id:
                    raise ValueError("Please select a product")
                if new_quantity <= 0:
                    raise ValueError("Quantity must be positive")

                old_product_id = transaction["product_id"]
                self.products[old_product_id]["stock"] += transaction["quantity"]

                current_stock = self.products[new_product_id]["stock"]
                if new_quantity > current_stock:
                    self.products[old_product_id]["stock"] -= transaction["quantity"]
                    raise ValueError(
                        f"Insufficient stock!\nRequested: {new_quantity}\nAvailable: {current_stock}"
                    )

                new_total = self.products[new_product_id]["price"] * new_quantity
                self.products[new_product_id]["stock"] -= new_quantity

                old_values = {
                    "date": transaction["date"].strftime("%Y-%m-%d"),
                    "product": transaction["product"],
                    "quantity": transaction["quantity"],
                    "total": transaction["total"],
                }

                transaction.update(
                    {
                        "date": new_date,
                        "product_id": new_product_id,
                        "product": new_product_name,
                        "quantity": new_quantity,
                        "total": new_total,
                    }
                )

                self.log_action(
                    f"Edited sale ID: {transaction_id}\n"
                    f"  Date: {old_values['date']} → {new_date.strftime('%Y-%m-%d')}\n"
                    f"  Product: {old_values['product']} → {new_product_name}\n"
                    f"  Quantity: {old_values['quantity']} → {new_quantity}\n"
                    f"  Total: Rp {old_values['total']:,} → Rp {new_total:,}"
                )

                self.refresh_product_list()
                self.refresh_sales_list()
                self.save_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Sale updated successfully!")

            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_changes).pack(pady=20)

    def delete_selected_product(self):
        selection = self.products_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.products_tree.item(item)["values"]
        product_id = values[0]

        if product_id in self.products:
            product_data = self.products[product_id]
            if messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete {product_data['name']}?",
            ):
                self.log_action(
                    f"Deleted product: {product_data['name']} "
                    f"(ID: {product_id}, "
                    f"Price: Rp {product_data['price']:,}, "
                    f"Stock: {product_data['stock']})"
                )
                del self.products[product_id]
                self.refresh_product_list()
                self.save_data()
                messagebox.showinfo("Success", "Product deleted successfully!")

    def delete_selected_sale(self):
        selection = self.sales_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.sales_tree.item(item)["values"]
        transaction_id = values[0]

        transaction = None
        for t in self.transactions:
            if t["id"] == transaction_id:
                transaction = t
                break

        if transaction:
            if messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete this sale?\nTransaction ID: {transaction_id}",
            ):
                # Restore product stock
                product_id = transaction["product_id"]
                self.products[product_id]["stock"] += transaction["quantity"]

                # Remove transaction
                self.transactions.remove(transaction)

                self.log_action(
                    f"Deleted sale: ID: {transaction_id}\n"
                    f"  Product: {transaction['product']}\n"
                    f"  Date: {transaction['date'].strftime('%Y-%m-%d')}\n"
                    f"  Quantity: {transaction['quantity']}\n"
                    f"  Total: Rp {transaction['total']:,}"
                )

                self.refresh_product_list()
                self.refresh_sales_list()
                self.save_data()
                messagebox.showinfo("Success", "Sale deleted successfully!")

    def on_product_select(self, event):
        selection = self.products_tree.selection()
        if selection:
            self.edit_product_button.config(state="normal")
            self.delete_product_button.config(state="normal")
        else:
            self.edit_product_button.config(state="disabled")
            self.delete_product_button.config(state="disabled")

    def on_sale_select(self, event):
        selection = self.sales_tree.selection()
        if selection:
            self.edit_sale_button.config(state="normal")
            self.delete_sale_button.config(state="normal")
        else:
            self.edit_sale_button.config(state="disabled")
            self.delete_sale_button.config(state="disabled")

    def refresh_product_list(self, event=None):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        search_keyword = self.product_search_entry.get().strip().lower()

        for product_id, data in self.products.items():
            if search_keyword and search_keyword not in data["name"].lower():
                continue

            self.products_tree.insert(
                "",
                "end",
                values=(
                    product_id,
                    data["name"],
                    f"Rp{data['price']:,}",
                    data["stock"],
                ),
            )

    def refresh_sales_list(self, event=None):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        search_keyword = self.sales_search_entry.get().strip().lower()

        sorted_transactions = sorted(
            self.transactions, key=lambda x: x["date"], reverse=True
        )

        for transaction in sorted_transactions:
            if search_keyword and search_keyword not in transaction["product"].lower():
                continue

            self.sales_tree.insert(
                "",
                "end",
                values=(
                    transaction["id"],
                    transaction["date"].strftime("%Y-%m-%d"),
                    transaction["product"],
                    transaction["quantity"],
                    f"Rp{transaction['total']:,}",
                ),
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Main()
    app.run()
