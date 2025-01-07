# PyStockFlow Docs v5.0
> Developed and Maintained by Zaeni Ahmad __(maszaen)__

_Catatan: Aplikasi ini sudah dibungkus menjadi file exe menggunakan pyinstaller, jika ingin mencoba aplikasi ini silakan tonton dokumentasinya terlebih dahulu (dokumentasi belum dibuat)._ <br/>
_Lalu untuk mencoba aplikasinya bisa download file exe pada **repository relases** yang terbaru atau bisa clone project ini (tanpa harus build aplikasi)_

## Arsitektur

- PyQt (pyside6) GUI
- MongoDB Atlas
- Native Python

## Fitur

- Multi-user sistem dengan login dan registrasi
- Manajemen produk (tambah, edit, hapus)
- Pencatatan transaksi penjualan
- Pencarian produk dan transaksi
- Laporan summary berdasarkan periode
- Cloud database dengan MongoDB Atlas

## Alat yang Dibutuhkan

- Python v3.8 keatas
- Akun MongoDB Atlas
- Koneksi Internet (untuk akses database)

## Instalasi

1. Clone repository:
```bash
git clone https://github.com/maszaen/inventory-system.git
cd inventory-system
```

2. Install dependensi:
```bash
pip install -r requirements.txt
```

## Struktur Direktori

```
├── .gitignore
├── build.py
├── inventory.spec
├── requirements.txt
├── logs/
├── assets/
│   └── icon.ico
└── src/
    ├── database/
    │   ├── __init__.py
    │   └── connection.py
    ├── models/
    │   ├── __init__.py
    │   ├── product.py
    │   ├── transaction.py
    │   └── user.py
    ├── ui/
    │   ├── __init__.py
    │   ├── dialogs/
    │   │   ├── change_conn_str.py
    │   │   ├── change_db_dialog.py
    │   │   ├── change_pass_dialog.py
    │   │   ├── db_setup_dialog.py
    │   │   ├── env_path_dialog.py
    │   │   ├── product_dialog.py
    │   │   ├── register_dialog.py
    │   │   └── sale_dialog.py
    │   ├── login_window.py
    │   ├── main_window.py
    │   ├── models/
    │   │   ├── product_table_model.py
    │   │   ├── sales_table_model.py
    │   │   └── __init__.py
    │   ├── tabs/
    │   │   ├── chart_tab.py
    │   │   ├── product_tab.py
    │   │   ├── sales_tab.py
    │   │   └── summary_tab.py
    ├── utils/
    │   ├── __init__.py
    │   ├── calculate_totals.py
    │   ├── logger.py
    │   ├── manifest_handler.py
    │   ├── menu_bar.py
    │   ├── pagination.py
    ├── __init__.py
    ├── style_config.py
    ├── main.py
    └── config.py

```

## Panduan Penggunaan Singkat

1. Jalankan aplikasi:
```bash
python -m src.main
```

2. Setup MongoDB:
   - Buat akun di [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Buat cluster baru
   - Buat database baru, dengan collection pertama users, lalu klik create database
   - Ke tab Cluster, klik Connect pada cluster, lalu pilih drivers, lalu Copy koneksi string
   - Whitelist IP address
   - Jika koneksi string sudah ada, bisa masukkan ke setup database aplikasi pada window awal, lalu pilih database
   - Jika belum paham, bisa cek dokumentasi langsung dari mongodb untuk setup database [MongoDB Documentation](https://www.mongodb.com/docs/)
   
3. Login/Register:
   - Login dengan akun yang sudah ada, atau
   - Klik "Register" untuk membuat akun baru

4. Manajemen Produk:
   - Klik tab "Products"
   - Gunakan tombol "Add Product" untuk menambah produk
   - Klik "Edit" atau "Delete" untuk memodifikasi produk
   - Gunakan search box untuk mencari produk

5. Transaksi Penjualan:
   - Klik tab "Sales"
   - Klik "Add Sale" untuk transaksi baru
   - Pilih produk dan masukkan jumlah
   - Stok akan otomatis terupdate

6. Melihat Summary:
   - Klik tab "Summary"
   - Pilih range tanggal
   - Klik "Generate Summary"

## Penyimpanan Data

1. Cloud (MongoDB):
   - Data produk
   - Data transaksi
   - Data pengguna

2. Lokal:
   - File log (logs/inventory_YYYYMMDD.log)
   - Aktivitas sistem

## Troubleshooting

Masalah biasanya pada koneksi database, coba lakukan cara berikut ini: <br/>
### Hal yang perlu diperhatikan:
   - Pastikan internet aktif
   - Pastikan connection string benar
   - Cek IP di MongoDB apakah sudah di-whitelist

Jika koneksi masih gagal, coba tambahkan nama database default setelah cluster url, contoh: <br/>
```bash
Sebelum:
mongodb+srv://<db_username>:<db_password>@<cluster-url>/?retryWrites=true&w=majority&appName=<appName>

Sesudah:
mongodb+srv://<db_username>:<db_password>@<cluster-url>/<db_name>?retryWrites=true&w=majority&appName=<appName>
```

## Fitur Update v5.0

1. Cloud Integration:

   - Migrasi ke MongoDB
   - Multi-user support
   - Real-time data sync

2. Authentication:
   - Sistem login
   - User registration
   - Password hashing dengan bcrypt

3. UI Improvements: 
   - Migrasi dari Tkinter ke PyQt6 / PySide6
   - UI lebih fleksibel dan mudah didesain atau dimaintenance
   - Improved search
   - Better error handling
   - Auto-refresh data

4. Database Setup: 
   - Fungsi setup database saat pertama kali aplikasi dijalankan
   - Trigger setup database hanya jika file .env belum ada, artinya jika sudah setup, tidak perlu setup lagi

5. Menu Tambahan:
   - Reset password
   - Reset connection string
   - Change database
   - Change connection string
   - Refresh summary

## Contributing

Untuk berkontribusi:
1. Fork repository
2. Buat branch baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## Contact

Untuk saran dan pertanyaan bisa melalui:
- Email: zaeni@students.amikom.ac.id
- GitHub Issues: [Go to repository issues](https://github.com/maszaen/inventory-system/issues)