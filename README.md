# PyStockFlow v4.0
> Developed and Maintained by Zaeni Ahmad __(maszaen)__

Sistem manajemen inventori dan penjualan dengan MongoDB Atlas Database.

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
- Cloud database dengan MongoDB
- Logging aktivitas sistem

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

3. Setup MongoDB:
   - Buat akun di [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Buat cluster baru
   - Dapatkan connection string
   - Whitelist IP address Anda
   - Jika belum paham, bisa cek dokumentasi langsung dari mongodb untuk setup database

4. Buat file .env di root folder:
```
MONGODB_URI=<Isi dengan koneksi string mongodb>
DB_NAME=<Isi dengan nama database sesuai yang kamu inginkan>
```

## Struktur Direktori

```
inventory_system/
├── src/
│   ├── database/       # Koneksi database
│   ├── models/         # Model data
│   ├── ui/             # User interface
│   │   ├── dialogs/    # Dialog windows
│   │   └── tabs/       # Tab components
│   └── utils/          # Utility functions
├── logs/               # Log files
└── config/             # Konfigurasi
```

## Panduan Penggunaan

1. Jalankan aplikasi:
```bash
python -m src.main
```

2. Login/Register:
   - Login dengan akun yang sudah ada, atau
   - Klik "Register" untuk membuat akun baru

3. Manajemen Produk:
   - Klik tab "Products"
   - Gunakan tombol "Add Product" untuk menambah produk
   - Klik "Edit" atau "Delete" untuk memodifikasi produk
   - Gunakan search box untuk mencari produk

4. Transaksi Penjualan:
   - Klik tab "Sales"
   - Klik "Add Sale" untuk transaksi baru
   - Pilih produk dan masukkan jumlah
   - Stok akan otomatis terupdate

5. Melihat Summary:
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

1. Koneksi Database:
   - Pastikan connection string benar
   - Cek IP di MongoDB apakah sudah di-whitelist
   - Pastikan internet aktif

2. Login Issues:
   - Cek username dan password
   - Pastikan sudah register

3. Error Log:
   - Cek file log di folder logs/
   - Format: inventory_YYYYMMDD.log

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
   - Improved search
   - Better error handling
   - Auto-refresh data

## Contributing

Untuk berkontribusi:
1. Fork repository
2. Buat branch baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## Contact

Untuk pertanyaan dan dukungan:
- Email: zaeni@students.amikom.ac.id
- GitHub Issues: [Create new issue](https://github.com/maszaen/inventory-system/issues)
