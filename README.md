# Smart Meter Monitor

Monitoring konsumsi listrik real-time berbasis web untuk smart meter Tuya CT Clamp.

## Fitur

- Monitoring real-time: daya (Watt), tegangan (Volt), arus (Ampere), total kWh
- Grafik konsumsi 24 jam dan 30 hari
- Estimasi tagihan listrik
- Alert saat daya melebihi threshold
- Dashboard web responsif

## Persiapan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Konfigurasi Tuya IoT Platform

1. Buat akun di [Tuya IoT Platform](https://iot.tuya.com/)
2. Buat project baru (Cloud Development)
3. Link device smart meter ke project
4. Catat credential:
   - `ACCESS_ID`
   - `ACCESS_SECRET`
   - `DEVICE_ID`
   - `API Endpoint` (sesuaikan region)

### 3. Isi Konfigurasi

Edit `config.py` atau set environment variable:

```bash
# Windows
set TUYA_ACCESS_ID=your_access_id
set TUYA_ACCESS_SECRET=your_access_secret
set TUYA_DEVICE_ID=your_device_id

# Linux/Mac
export TUYA_ACCESS_ID=your_access_id
export TUYA_ACCESS_SECRET=your_access_secret
export TUYA_DEVICE_ID=your_device_id
```

## Menjalankan

### 1. Jalankan Data Collector (Terminal 1)

```bash
python collector.py
```

Script ini akan mengambil data dari API Tuya setiap 5 menit dan menyimpan ke database.

### 2. Jalankan Web Server (Terminal 2)

```bash
python app.py
```

Buka browser ke `http://localhost:5000`

## API Endpoints

| Endpoint | Deskripsi |
|----------|-----------|
| `/api/current` | Data real-time terbaru |
| `/api/history?hours=24` | Data historis (jam) |
| `/api/daily?days=30` | Ringkasan harian |
| `/api/alerts` | Daftar alert |
| `/api/stats` | Statistik ringkas |

## Struktur Proyek

```
smart-meter-monitor/
├── app.py              # Flask backend
├── collector.py        # Data collector
├── config.py           # Konfigurasi
├── database.py         # Database operations
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Dashboard web
├── static/             # Static files (CSS, JS)
├── data/               # SQLite database
└── logs/               # Log files
```

## Troubleshooting

- **Tidak ada data**: Pastikan collector berjalan dan credential Tuya benar
- **Token error**: Cek ACCESS_ID dan ACCESS_SECRET
- **Device not found**: Cek DEVICE_ID dan pastikan device sudah di-link ke project

## Lisensi

MIT License
