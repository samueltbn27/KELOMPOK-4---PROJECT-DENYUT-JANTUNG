"""
Konfigurasi untuk sistem monitoring detak jantung
Edit file ini untuk menyesuaikan dengan setup Anda
"""

# ==================== KONFIGURASI API SERVER ====================
# IP Address server Flask (PC/Laptop yang menjalankan api.py)
# Ganti dengan IP address komputer Anda
API_HOST = "10.229.1.250"
API_PORT = 5000
API_URL = f"http://{API_HOST}:{API_PORT}/kirim"

# ==================== KONFIGURASI DATABASE ====================
# Database MySQL (XAMPP)
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""  # Kosongkan jika tidak ada password
DB_NAME = "sensor_db"
DB_TABLE = "detak_jantung"

# ==================== KONFIGURASI GPIO (RASPBERRY PI) ====================
# Pin GPIO untuk LED (BCM mode)
LED_PIN = 17  # GPIO 17 = Pin 11

# Pin GPIO untuk Buzzer (BCM mode)
BUZZER_PIN = 27  # GPIO 27 = Pin 13

# ==================== KONFIGURASI SENSOR MAX30102 ====================
# Sample rate sensor (Hz)
SAMPLE_RATE = 100

# Window size untuk perhitungan BPM (detik)
WINDOW_SIZE = 4

# Threshold multiplier untuk peak detection
# Nilai lebih besar = lebih ketat mendeteksi peak
# Nilai lebih kecil = lebih sensitif mendeteksi peak
THRESHOLD_MULTIPLIER = 0.6

# Minimum jarak antar peak (detik)
# Untuk mencegah false positive
MIN_PEAK_DISTANCE = 0.4  # 0.4 detik = 150 BPM max

# ==================== KONFIGURASI BPM THRESHOLD ====================
# Range BPM untuk menentukan status
BPM_LOW = 60        # Di bawah ini = Bradikardia
BPM_NORMAL = 100    # 60-100 = Normal
BPM_HIGH = 120      # 101-120 = Tinggi
# Di atas 120 = Takikardia (Bahaya)

# ==================== KONFIGURASI PENGIRIMAN DATA ====================
# Interval pengiriman data ke API (detik)
SEND_INTERVAL = 1.0

# Timeout untuk request API (detik)
API_TIMEOUT = 2

# ==================== KONFIGURASI TAMPILAN ====================
# Maksimal data yang ditampilkan di grafik website
MAX_CHART_DATA = 30

# Interval update data di website (milidetik)
UPDATE_INTERVAL = 1000  # 1 detik

# ==================== MODE DEBUG ====================
DEBUG_MODE = True  # Set False untuk production
VERBOSE_LOGGING = True  # Print detail log ke console
