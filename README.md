# PyStockFlow Docs v5.5
> Developed and Maintained by Zaeni Ahmad __(maszaen)__

Catatan: Aplikasi ini telah dikompilasi menjadi file executable (.exe) menggunakan Nuitka dan dibuat installer menggunakan Inno Setup. Untuk mencoba aplikasi ini, Kamu bisa:

- Download installer PyStockFlow terbaru  [_Disini_](https://github.com/maszaen/inventory-system/releases/download/stable-relase-v5.0/PyStockFlow_Setup.exe).
- Atau clone repository ini dan jalankan aplikasi dari source code (link dokumentasi akan segera dibuat)

Untuk melihat flowchart lengkap dari aplikasi ini, bisa klik [_Disini_](https://github.com/maszaen/inventory-system/releases/download/stable-relase-v5.0/PyStockFlow_Flowcharts.drawio) untuk mendownload file flowchart.

## Introduction
PyStockFlow adalah aplikasi open-source untuk manajemen inventaris dan penjualan yang menggunakan bahasa pemrograman Python, PySide6 untuk GUI, serta MongoDB Atlas sebagai database cloud. Aplikasi ini dirancang untuk membantu bisnis kecil dan menengah dalam mengelola produk, transaksi penjualan, dan laporan secara efisien. Dengan sistem yang mudah digunakan dan fitur multi-user, PyStockFlow memberikan solusi manajemen yang lebih baik dan dapat diakses secara real-time.

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
├── logs/
├── assets/
└── src/
    ├── database/
    ├── models/
    ├── ui/
    │   ├── dialogs/
    │   ├── models/
    │   └── tabs/
    └── utils/
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
   - Whitelist IP address, [Cara Whitelist IP](https://www.mongodb.com/docs/atlas/security/ip-access-list/)
   - Jika koneksi string sudah ada, bisa masukkan ke setup database aplikasi pada window awal, lalu pilih database
   - Jika belum paham, bisa cek dokumentasi langsung dari mongodb untuk setup database [Klik disini](https://www.mongodb.com/docs/)
   - atau bisa gunakan database yg kami sediakan, [Klik disini](https://github.com/maszaen/inventory-system/blob/main/credential-testing.txt)
   
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
