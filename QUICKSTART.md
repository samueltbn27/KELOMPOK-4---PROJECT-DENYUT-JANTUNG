# 🚀 QUICK START GUIDE

## Panduan Cepat Menjalankan Sistem Monitoring Detak Jantung

---

## 📋 PERSIAPAN AWAL

### ✅ Checklist Sebelum Memulai

- [ ] XAMPP terinstall (MySQL)
- [ ] Python 3.7+ terinstall
- [ ] Raspberry Pi dengan Raspbian OS (opsional)
- [ ] Komponen hardware tersedia (MAX30102, LED, Buzzer)
- [ ] Koneksi jaringan stabil

---

## 🔥 CARA TERCEPAT (5 Menit)

### Step 1: Setup Database (2 menit)

1. Buka **XAMPP Control Panel**
2. Start **Apache** dan **MySQL**
3. Buka browser: `http://localhost/phpmyadmin`
4. Klik **New** → buat database bernama `sensor_db`
5. Klik database `sensor_db` → tab **SQL**
6. Copy-paste dan jalankan query ini:

```sql
CREATE TABLE detak_jantung (
  id INT AUTO_INCREMENT PRIMARY KEY,
  bpm INT,
  waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 2: Install Dependencies (1 menit)

```bash
# Masuk ke folder project
cd project_pemdas

# Install requirements
pip install -r requirements.txt
```

### Step 3: Test System (1 menit)

```bash
# Jalankan test
python test_system.py
```

Pastikan semua test **✓ PASS** sebelum lanjut!

### Step 4: Jalankan Server (30 detik)

```bash
# Jalankan API server
python api.py
```

Server berjalan di: **http://localhost:5000**

### Step 5: Test dengan Simulator (30 detik)

Buka terminal baru:

```bash
# Jalankan simulator
python simulate_sensor.py
```

### Step 6: Buka Website

Buka browser: **http://localhost:5000**

🎉 **SELESAI!** Website monitoring sudah berjalan!

---

## 🔧 SETUP DENGAN HARDWARE RASPBERRY PI

### Persiapan Raspberry Pi

1. **Enable I2C**

```bash
sudo raspi-config
# Pilih: 3 Interface Options → I5 I2C → Yes → OK
sudo reboot
```

2. **Install Dependencies**

```bash
sudo apt-get update
sudo apt-get install -y python3-pip i2c-tools
sudo pip3 install RPi.GPIO max30102 numpy requests
```

3. **Test I2C**

```bash
sudo i2cdetect -y 1
# MAX30102 harus terdeteksi di 0x57
```

4. **Hubungkan Hardware**

   - Lihat file `WIRING_DIAGRAM.md` untuk detail koneksi
   - MAX30102 → I2C (Pin 1, 3, 5, 6)
   - LED → GPIO17 (Pin 11) + Resistor 220Ω
   - Buzzer → GPIO27 (Pin 13)

5. **Cari IP Address Server**

Di komputer yang menjalankan server:

```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
# atau
ip addr show
```

Catat IP address (contoh: 10.229.1.250)

6. **Edit Konfigurasi di Raspberry Pi**

Edit file `sensor_max30102.py` baris 23:

```python
API_URL = "http://10.229.1.250:5000/kirim"  # Ganti dengan IP server Anda
```

Atau edit file `config.py`:

```python
API_HOST = "10.229.1.250"  # Ganti dengan IP server Anda
```

7. **Jalankan Sensor**

```bash
sudo python3 sensor_max30102.py
```

**PENTING:** Gunakan `sudo` karena mengakses GPIO!

---

## 📱 AKSES DARI PERANGKAT LAIN

### Cari IP Address Server

**Windows:**

```bash
ipconfig
# Cari IPv4 Address di adapter yang aktif
```

**Linux/Mac:**

```bash
hostname -I
```

### Akses dari Perangkat Lain

Di browser perangkat lain (HP/Tablet/PC lain) di jaringan yang sama:

```
http://[IP_ADDRESS]:5000
```

Contoh:

```
http://10.229.1.250:5000
```

---

## 🛠️ COMMAND REFERENCE

### Server Commands

```bash
# Start server
python api.py

# Start server dengan auto-reload (development)
python api.py --debug

# Stop server
Ctrl + C
```

### Simulator Commands

```bash
# Start simulator
python simulate_sensor.py

# Stop simulator
Ctrl + C
```

### Raspberry Pi Commands

```bash
# Test sensor
sudo python3 sensor_max30102.py

# Stop sensor
Ctrl + C

# Check I2C devices
sudo i2cdetect -y 1

# Test GPIO (LED)
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.OUT); GPIO.output(17, GPIO.HIGH)"

# Cleanup GPIO
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.cleanup()"
```

### Database Commands

```bash
# Backup database
mysqldump -u root sensor_db > backup.sql

# Restore database
mysql -u root sensor_db < backup.sql

# Clear all data
mysql -u root -e "TRUNCATE TABLE sensor_db.detak_jantung"
```

---

## 🎯 TESTING CHECKLIST

### Test Server (Tanpa Hardware)

- [ ] Database terhubung (`test_system.py`)
- [ ] Server berjalan (`http://localhost:5000`)
- [ ] Endpoint `/health` response OK
- [ ] Website terbuka
- [ ] Simulator kirim data
- [ ] Website update real-time
- [ ] Grafik bergerak

### Test dengan Hardware

- [ ] I2C terdeteksi (`i2cdetect -y 1`)
- [ ] MAX30102 di address 0x57
- [ ] LED menyala saat test
- [ ] Buzzer bunyi saat test
- [ ] Sensor membaca nilai saat jari ditempel
- [ ] BPM terkirim ke server
- [ ] Website menampilkan BPM
- [ ] LED menyala saat BPM > 100
- [ ] Buzzer bunyi saat BPM > 120

---

## 📊 MONITORING FEATURES

### Di Website Anda Bisa Melihat:

1. **BPM Display** - Angka besar detak jantung real-time
2. **Status Zone**:
   - 🔵 Bradikardia (< 60)
   - 🟢 Normal (60-100)
   - 🟠 Tinggi (101-120)
   - 🔴 Takikardia (> 120)
3. **Grafik Real-time** - 30 data terakhir
4. **Statistik**:
   - Minimum BPM
   - Maximum BPM
   - Rata-rata BPM
   - Total data
5. **Indikator Hardware**:
   - Status LED
   - Status Buzzer
6. **Connection Status** - Online/Offline

---

## 🐛 TROUBLESHOOTING CEPAT

### Server Tidak Bisa Diakses

```bash
# Cek firewall Windows
# Control Panel → Windows Defender Firewall → Allow an app
# Tambahkan Python

# Atau disable firewall sementara (testing only)
netsh advfirewall set allprofiles state off
```

### Database Error

```bash
# Restart MySQL
# Di XAMPP Control Panel: Stop MySQL → Start MySQL

# Atau via command
net stop mysql
net start mysql
```

### Raspberry Pi Tidak Kirim Data

```bash
# Cek koneksi jaringan
ping 10.229.1.250

# Cek apakah port 5000 terbuka
curl http://10.229.1.250:5000/health

# Restart sensor
sudo python3 sensor_max30102.py
```

### MAX30102 Tidak Terdeteksi

```bash
# Reboot Raspberry Pi
sudo reboot

# Cek I2C setelah reboot
sudo i2cdetect -y 1

# Jika masih tidak terdeteksi, cek koneksi kabel
```

---

## 📞 HELP & SUPPORT

### Log Locations

- Server log: Terminal output
- Database log: XAMPP MySQL log
- Sensor log: Terminal output di Raspberry Pi

### API Endpoints untuk Testing

```bash
# Test server health
curl http://localhost:5000/health

# Get latest data
curl http://localhost:5000/data

# Get statistics
curl http://localhost:5000/stats

# Send test data
curl -X POST http://localhost:5000/kirim \
  -H "Content-Type: application/json" \
  -d '{"bpm": 75}'
```

---

## 🎓 NEXT STEPS

Setelah sistem berjalan, Anda bisa:

1. **Kustomisasi Threshold BPM** di `config.py`
2. **Tambah Fitur Notifikasi** (email/WhatsApp)
3. **Export Data ke Excel** untuk analisis
4. **Tambah Multiple Sensors** untuk monitoring banyak orang
5. **Deploy ke Cloud** (Heroku/AWS) untuk akses internet

---

## 📄 FILE REFERENCE

| File                   | Fungsi                            |
| ---------------------- | --------------------------------- |
| `api.py`               | Flask server API                  |
| `sensor_max30102.py`   | Kode Raspberry Pi                 |
| `simulate_sensor.py`   | Simulator untuk testing           |
| `test_system.py`       | Test otomatis sistem              |
| `config.py`            | Konfigurasi (IP, GPIO, threshold) |
| `requirements.txt`     | Python dependencies               |
| `templates/index.html` | Website dashboard                 |
| `README.md`            | Dokumentasi lengkap               |
| `WIRING_DIAGRAM.md`    | Panduan koneksi hardware          |
| `QUICKSTART.md`        | File ini                          |

---

## ✨ TIPS & TRICKS

1. **Gunakan simulator dulu** sebelum hardware untuk memastikan server OK
2. **Test komponen satu per satu** (LED → Buzzer → Sensor)
3. **Print WIRING_DIAGRAM.md** sebagai referensi saat wiring
4. **Backup database** secara berkala
5. **Gunakan UPS** untuk Raspberry Pi agar tidak mati mendadak
6. **Bookmark website** di HP untuk monitoring mobile
7. **Screenshot error** untuk troubleshooting lebih mudah

---

## 🎉 SELAMAT!

Sistem monitoring detak jantung Anda sudah siap digunakan!

Jika ada pertanyaan atau masalah, cek file:

- `README.md` - Dokumentasi lengkap
- `WIRING_DIAGRAM.md` - Panduan hardware
- `test_system.py` - Diagnostik otomatis

**Happy Monitoring! 💓**
