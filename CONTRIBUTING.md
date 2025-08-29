# Project Title: `MSTD Dashboard Project`
---
Company: PT Kalbio Global Medika <br>
Start Date: 2025-06-25 <br>
End Date: 2025-07-31 <br>
Objective: Membangun dashboard interaktif yang menyajikan informasi real-time terkait yield produksi dan titik-titik terjadinya yield loss di setiap batch (proses yg terjadi saat ini), untuk membantu MSTD dalam melakukan analisis performa dan pengambilan keputusan berbasis data.

---
## Struktur & Branch

Setiap orang memiliki branch masing-masing:

| Nama     | Branch         | Tugas                        |
|----------|----------------|------------------------------------|
| Alysia     | quality_analyst     | 1. Menentukan aturan validasi data di setiap tahap (input, ETL, DB) <br> 2. Membangun sistem validasi otomatis (range, format, field wajib, dll) <br> 3. Mendesain sistem notifikasi otomatis saat terjadi error validasi (log, alert, popup, atau email) <br> 4. Berkolaborasi dengan ETL dan Integrator untuk memastikan validasi berjalan sesuai rencana     |
| Jeny     | automated_pipeline     | 1. Membangun pipeline otomatis menggunakan Python, cron job, atau Airflow <br> 2. Menangani data kosong atau error pada saat ingest <br> 3. Memproses staging dan memasukkan data ke dalam database <br> 4. Membuat logging proses dan menampilkan pop up pada web jika terjadi kegagalan      |
| Rut     | dashboard_visualization     | 1. Membangun dashboard interaktif (misal menggunakan pychart, dsb) <br> 2. Mengambil data dari database untuk keperluan visualisasi <br> 3. Menyediakan fitur filter (minggu, kategori aktivitas) <br> 4. Menyediakan fitur ekspor data ke format CSV dan PDF <br> 5. Mendokumentasikan fitur dashboard  |
| Riska     | quality_analyst & Backend     | 1. Menentukan aturan validasi data di setiap tahap (input, ETL, DB) <br> 2. Membangun sistem validasi otomatis (range, format, field wajib, dll) <br> 3. Mendesain sistem notifikasi otomatis saat terjadi error validasi (log, alert, popup, atau email) <br> 4. Berkolaborasi dengan ETL dan Integrator untuk memastikan validasi berjalan sesuai rencana 5.Bertanggung jawab dalam pembuatan seluruh proses backend dan logic   |
| Valencia    | database_administrator   | 1. Merancang skema database relasional (master data & transaksi) <br> 2. Menyusun skrip backup rutin dan restore database <br> 3. Memantau konektivitas database ke ETL dan Dashboard <br> 4. Mendukung fitur ekspor data     |

---

## Cara Mulai
### 1. Clone Repositori
```bash
git clone https://github.com/RiskaMellyAgustin/Kalbio-Yield-Project
cd backend
```

### 2. Checkout ke Branch Kalian
```bash
git checkout nama-branch
```
Contoh: `git checkout quality_analyst`

### 3. Pastikan Sudah Masuk ke Branch Kalian
```bash
git branch
```

### 4. Update dan Push
Setelah selesai mengedit atau menambahkan file:
```bash
git add .
git commit -m "Tulis deskripsi perubahan singkat"
git push origin nama-branch
```

---

## Integrasi ke main
Semua pekerjaan akan digabung ke branch main melalui `Pull Request` (PR):
- Buka GitHub
- Buat PR dari branch kalian ke main
- PR akan di-merge

---

## Branch main
- Jangan push langsung ke `main`
- Semua update harus melalui `Pull Request` (PR)
- `main` hanya berisi kode yang sudah stabil dan teruji

---


## Struktur Folder 'main'
```bash
kalbio_dashboard_project/       # Root project folder
├── backend/                    # Contains Django apps and project setup
│   ├── kalbio_dashboard/       # Main Django project (settings, URLs, WSGI)
│   ├── etl/                    # ETL scripts for data staging and preprocessing
│   ├── yieldapp/               # Main Django app: views, models, forms, templates, static, utils, etc.
├── manage.py                   # Django management script
├── .gitignore                  # Specifies files and directories excluded from version control
├── requirements.txt            # Dependencies for the project
└── README.md                   # Project documentation

---

## Tips
- Jangan commit file data besar (gunakan .gitignore)
- Update requirements.txt jika menambah library Python baru.

---
