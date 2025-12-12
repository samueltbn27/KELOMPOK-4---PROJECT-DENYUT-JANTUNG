# 🫀 Sistem Monitoring Detak Jantung Real-time

## Deteksi Detak Jantung dengan Sensor MAX30102

Sistem monitoring detak jantung real-time menggunakan sensor MAX30102, Raspberry Pi, LED, Buzzer, dan website dashboard berbasis Flask.

---

## 📋 Daftar Isi

- [Fitur](#fitur)
- [Komponen Hardware](#komponen-hardware)
- [Koneksi Hardware](#koneksi-hardware)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Project](#struktur-project)
- [API Endpoints](#api-endpoints)

---

## ✨ Fitur

### Website Dashboard

- 📊 **Grafik Real-time** - Visualisasi detak jantung dalam bentuk grafik line chart
- 💓 **Display BPM Besar** - Tampilan angka BPM yang jelas dan mudah dibaca
- 🎨 **Status Warna**:
  - 🔵 Biru: Bradikardia (< 60 BPM)
  - 🟢 Hijau: Normal (60-100 BPM)
  - 🟠 Orange: Tinggi (101-120 BPM)
  - 🔴 Merah: Takikardia (> 120 BPM)
- 📈 **Statistik**: Min, Max, Rata-rata, Total data
- 💡 **Indikator LED & Buzzer**: Status perangkat ditampilkan di website
- 🔌 **Status Koneksi**: Monitoring koneksi real-time

### Hardware

- 🔍 **Peak Detection Manual** - Deteksi detak jantung tanpa library eksternal
- 💡 **LED Warning** - Menyala saat BPM tinggi
- 🔔 **Buzzer Alarm** - Berbunyi saat BPM berbahaya
- 📡 **Auto Send ke API** - Data otomatis terkirim setiap detik

---

## 🔧 Komponen Hardware

### Yang Dibutuhkan:

1. **Raspberry Pi** (3/4/Zero W)
2. **Sensor MAX30102** - Sensor detak jantung dan SpO2
3. **LED** - 1 buah (warna kuning/merah)
4. **Buzzer** - 1 buah (buzzer aktif/pasif)
5. **Resistor 220Ω** - 1 buah (untuk LED)
6. **Breadboard & Kabel Jumper**

---

## 🔌 Koneksi Hardware

### MAX30102 ke Raspberry Pi (I2C)

```
MAX30102        Raspberry Pi
---------       ------------
VIN      -----> 3.3V (Pin 1)
GND      -----> GND (Pin 6)
SDA      -----> SDA (GPIO 2, Pin 3)
SCL      -----> SCL (GPIO 3, Pin 5)
```

### LED

```
LED              Raspberry Pi
---------        ------------
Anoda (+)  ----> GPIO 17 (Pin 11)
Katoda (-) ----> Resistor 220Ω ----> GND
```

### Buzzer

```
Buzzer           Raspberry Pi
---------        ------------
Positif (+) ---> GPIO 27 (Pin 13)
Negatif (-) ---> GND (Pin 14)
```

### Diagram Koneksi Lengkap:

```
    Raspberry Pi
    ┌─────────────────┐
    │   3.3V ●────────┼──── MAX30102 VIN
    │   SDA  ●────────┼──── MAX30102 SDA
    │   SCL  ●────────┼──── MAX30102 SCL
    │   GND  ●────────┼──── MAX30102 GND
    │                 │
    │  GPIO17●────────┼──── LED Anoda (+)
    │                 │      │
    │   GND  ●────────┼──────┴─── LED Katoda (-) via Resistor
    │                 │
    │  GPIO27●────────┼──── Buzzer (+)
    │   GND  ●────────┼──── Buzzer (-)
    └─────────────────┘
```

---

## 📦 Instalasi

### 1. Setup Raspberry Pi

#### Enable I2C

```bash
sudo raspi-config
# Pilih: Interfacing Options -> I2C -> Enable
sudo reboot
```

#### Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev i2c-tools
```

#### Cek I2C Device

```bash
sudo i2cdetect -y 1
# MAX30102 biasanya terdeteksi di address 0x57
```

### 2. Setup Server (PC/Laptop dengan XAMPP)

#### Install Python Requirements

```bash
cd project_pemdas
pip install -r requirements.txt
```

#### Setup Database MySQL

1. Buka **XAMPP** dan start **Apache** & **MySQL**
2. Buka **phpMyAdmin**: `http://localhost/phpmyadmin`
3. Buat database bernama `sensor_db`
4. Import file `detak_jantung.sql` atau jalankan query:

```sql
CREATE DATABASE sensor_db;
USE sensor_db;

CREATE TABLE detak_jantung (
  id INT AUTO_INCREMENT PRIMARY KEY,
  bpm INT,
  waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Install Library Raspberry Pi

Pada **Raspberry Pi**, install library khusus:

```bash
# Install RPi.GPIO
sudo pip3 install RPi.GPIO

# Install max30102 library
sudo pip3 install max30102

# Install numpy
sudo pip3 install numpy

# Install requests
sudo pip3 install requests
```

---

## 🚀 Cara Penggunaan

### 1. Jalankan Server API (di PC/Laptop)

```bash
cd project_pemdas
python api.py
```

Server akan berjalan di: `http://0.0.0.0:5000`

### 2. Cari IP Address Server

Di PC/Laptop yang menjalankan server, cari IP address:

**Windows:**

```bash
ipconfig
# Cari IPv4 Address, contoh: 10.229.1.250
```

**Linux/Mac:**

```bash
ifconfig
# Atau
ip addr show
```

### 3. Update IP di Raspberry Pi

Edit file `sensor_max30102.py` baris 23, sesuaikan dengan IP server:

```python
API_URL = "http://10.229.1.250:5000/kirim"  # Ganti dengan IP server Anda
```

### 4. Jalankan Sensor di Raspberry Pi

```bash
cd project_pemdas
sudo python3 sensor_max30102.py
```

**Catatan:** Gunakan `sudo` karena menggunakan GPIO!

### 5. Buka Website Dashboard

Di browser, buka:

```
http://10.229.1.250:5000
```

Ganti dengan IP server Anda.

---

## 📁 Struktur Project

```
project_pemdas/
│
├── api.py                    # Flask server API
├── sensor_max30102.py        # Kode Raspberry Pi untuk sensor
├── simulate_sensor.py        # Simulator sensor (testing tanpa hardware)
├── requirements.txt          # Python dependencies
├── README.md                 # Dokumentasi ini
│
└── templates/
    └── index.html           # Website dashboard
```

---

## 🔗 API Endpoints

### 1. POST `/kirim`

**Kirim data BPM dari sensor**

Request:

```json
{
  "bpm": 75
}
```

Response:

```json
{
  "status": "OK",
  "bpm": 75
}
```

### 2. GET `/data`

**Ambil data terbaru**

Response:

```json
{
  "id": 123,
  "bpm": 75,
  "waktu": "2025-12-12 14:30:45"
}
```

### 3. GET `/history?limit=30`

**Ambil data historis**

Response:

```json
[
  {
    "id": 120,
    "bpm": 72,
    "waktu": "2025-12-12 14:30:40"
  },
  ...
]
```

### 4. GET `/stats`

**Ambil statistik**

Response:

```json
{
  "total": 500,
  "min_bpm": 55,
  "max_bpm": 130,
  "avg_bpm": 82.5
}
```

### 5. GET `/health`

**Health check server**

Response:

```json
{
  "status": "OK",
  "message": "Server dan database berjalan normal",
  "timestamp": "2025-12-12 14:30:00"
}
```

---

## 🎯 Cara Kerja Sistem

### 1. Peak Detection Manual

Sistem menggunakan algoritma peak detection sederhana:

- Membaca data IR dari sensor MAX30102
- Menyimpan data dalam buffer (4 detik)
- Menghitung threshold berdasarkan mean + 0.6\*std
- Mendeteksi peaks (nilai maksimum lokal)
- Menghitung interval antar peaks
- Konversi ke BPM (60 / interval)

### 2. Kontrol LED & Buzzer

```
BPM Range       LED      Buzzer    Status
---------       ---      ------    ------
< 60            OFF      OFF       Bradikardia
60 - 100        OFF      OFF       Normal
101 - 120       ON       OFF       Tinggi
> 120           ON       ON        Takikardia
```

### 3. Flow Data

```
MAX30102 → Raspberry Pi → Peak Detection → BPM
                ↓
            GPIO Control (LED/Buzzer)
                ↓
        HTTP POST ke API Server
                ↓
         MySQL Database
                ↓
          Website Dashboard
```

---

## 🧪 Testing Tanpa Hardware

Untuk testing tanpa Raspberry Pi:

```bash
# Jalankan simulator
python simulate_sensor.py
```

Simulator akan mengirim data BPM random setiap 3 detik.

---

## ⚠️ Troubleshooting

### Sensor tidak terdeteksi

```bash
# Cek I2C
sudo i2cdetect -y 1

# Pastikan koneksi kabel SDA/SCL benar
# Pastikan sensor mendapat power 3.3V
```

### Error GPIO

```bash
# Pastikan menjalankan dengan sudo
sudo python3 sensor_max30102.py

# Reset GPIO jika error
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.cleanup()"
```

### Database error

```bash
# Pastikan XAMPP MySQL running
# Cek username/password di api.py
# Pastikan database sensor_db sudah dibuat
```

### Tidak bisa kirim ke API

```bash
# Cek koneksi jaringan Raspberry Pi dan Server
ping 10.229.1.250

# Pastikan firewall tidak memblokir port 5000
# Windows: Control Panel -> Windows Defender Firewall
```

---

## 📊 Range BPM Normal

| Kategori    | BPM Range | Keterangan                 |
| ----------- | --------- | -------------------------- |
| Bradikardia | < 60      | Detak jantung lambat       |
| Normal      | 60 - 100  | Detak jantung normal       |
| Tinggi      | 101 - 120 | Detak jantung cepat        |
| Takikardia  | > 120     | Detak jantung sangat cepat |

---

## 👨‍💻 Developer

Project PEMDAS - Sistem Monitoring Detak Jantung

---

## 📝 Lisensi

Project ini dibuat untuk keperluan edukasi.

---

## 🙏 Acknowledgments

- MAX30102 Library
- Flask Framework
- Chart.js untuk visualisasi
- Font Awesome untuk icons

---

**Selamat Mencoba! 💓**
