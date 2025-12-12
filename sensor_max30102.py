"""
Sensor MAX30102 dengan Raspberry Pi
Deteksi detak jantung dengan peak detection manual
GPIO: Buzzer dan LED
API: http://10.229.1.250:5000/kirim
"""

import time
import requests
import RPi.GPIO as GPIO
from max30102 import MAX30102
import numpy as np
from collections import deque

# ==================== KONFIGURASI GPIO ====================
LED_PIN = 17        # Pin GPIO untuk LED (GPIO 17 = Pin 11)
BUZZER_PIN = 27     # Pin GPIO untuk Buzzer (GPIO 27 = Pin 13)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Pastikan LED dan Buzzer mati di awal
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)

print("GPIO Setup selesai!")

# ==================== KONFIGURASI MAX30102 ====================
# Inisialisasi sensor MAX30102
try:
    sensor = MAX30102()
    print("MAX30102 berhasil diinisialisasi!")
except Exception as e:
    print(f"Error inisialisasi MAX30102: {e}")
    GPIO.cleanup()
    exit(1)

# ==================== KONFIGURASI API ====================
API_URL = "http://10.229.1.250:5000/kirim"

# ==================== PEAK DETECTION MANUAL ====================
class HeartRateDetector:
    def __init__(self, sample_rate=100, window_size=4):
        """
        sample_rate: Sampling rate sensor (Hz)
        window_size: Ukuran window dalam detik untuk menghitung BPM
        """
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.max_samples = sample_rate * window_size
        
        # Buffer untuk menyimpan data IR
        self.ir_buffer = deque(maxlen=self.max_samples)
        
        # Parameter untuk peak detection
        self.threshold_multiplier = 0.6
        self.min_distance = int(sample_rate * 0.4)  # Minimal 0.4 detik antar peak (150 BPM max)
        self.last_peak_index = -self.min_distance
        
        # Menyimpan waktu peaks
        self.peak_times = deque(maxlen=10)
        
        self.current_bpm = 0
    
    def add_sample(self, ir_value):
        """Tambahkan sample baru ke buffer"""
        self.ir_buffer.append(ir_value)
    
    def detect_peaks(self):
        """Deteksi peaks dari data IR menggunakan metode sederhana"""
        if len(self.ir_buffer) < 100:
            return []
        
        # Convert ke numpy array
        data = np.array(list(self.ir_buffer))
        
        # Normalisasi data
        data_mean = np.mean(data)
        data_std = np.std(data)
        
        if data_std == 0:
            return []
        
        # Hitung threshold
        threshold = data_mean + (self.threshold_multiplier * data_std)
        
        # Cari peaks
        peaks = []
        for i in range(1, len(data) - 1):
            # Peak: nilai lebih besar dari tetangga dan di atas threshold
            if (data[i] > data[i-1] and 
                data[i] > data[i+1] and 
                data[i] > threshold and
                i - self.last_peak_index >= self.min_distance):
                
                peaks.append(i)
                self.last_peak_index = i
        
        return peaks
    
    def calculate_bpm(self):
        """Hitung BPM dari peaks yang terdeteksi"""
        peaks = self.detect_peaks()
        
        if len(peaks) >= 2:
            # Hitung interval antar peaks
            intervals = []
            for i in range(1, len(peaks)):
                interval = (peaks[i] - peaks[i-1]) / self.sample_rate  # dalam detik
                intervals.append(interval)
            
            # Rata-rata interval
            avg_interval = np.mean(intervals)
            
            # Konversi ke BPM
            bpm = 60 / avg_interval
            
            # Filter BPM yang valid (40-180)
            if 40 <= bpm <= 180:
                self.current_bpm = int(bpm)
                self.peak_times.append(time.time())
                return self.current_bpm
        
        # Jika tidak ada peaks baru, gunakan BPM terakhir
        # tapi cek apakah sudah terlalu lama (> 3 detik)
        if len(self.peak_times) > 0:
            last_peak_time = self.peak_times[-1]
            if time.time() - last_peak_time < 3:
                return self.current_bpm
        
        return 0
    
    def get_bpm(self):
        """Return BPM saat ini"""
        return self.calculate_bpm()


# ==================== KONTROL LED DAN BUZZER ====================
def control_led_buzzer(bpm):
    """
    Kontrol LED dan Buzzer berdasarkan nilai BPM
    - Normal (60-100 BPM): LED dan Buzzer mati
    - Tinggi (101-120 BPM): LED nyala, Buzzer mati
    - Bahaya (>120 atau <60 BPM): LED dan Buzzer nyala
    """
    if bpm == 0:
        # Tidak ada data valid
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    elif 60 <= bpm <= 100:
        # Normal
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    elif 101 <= bpm <= 120:
        # Tinggi - LED nyala
        GPIO.output(LED_PIN, GPIO.HIGH)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    else:
        # Bahaya - LED dan Buzzer nyala
        GPIO.output(LED_PIN, GPIO.HIGH)
        GPIO.output(BUZZER_PIN, GPIO.HIGH)


# ==================== KIRIM DATA KE API ====================
def send_to_api(bpm):
    """Kirim data BPM ke server API"""
    if bpm == 0:
        return  # Jangan kirim jika BPM tidak valid
    
    try:
        payload = {"bpm": bpm}
        response = requests.post(API_URL, json=payload, timeout=2)
        
        if response.status_code == 200:
            print(f"✓ BPM {bpm} berhasil dikirim ke API")
        else:
            print(f"✗ Gagal kirim ke API: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error koneksi API: {e}")


# ==================== MAIN PROGRAM ====================
def main():
    """Program utama untuk membaca sensor dan mengirim data"""
    print("\n" + "="*50)
    print("SISTEM MONITORING DETAK JANTUNG")
    print("Sensor: MAX30102")
    print("API URL:", API_URL)
    print("="*50 + "\n")
    print("Tekan CTRL+C untuk berhenti\n")
    
    # Inisialisasi heart rate detector
    hr_detector = HeartRateDetector(sample_rate=100, window_size=4)
    
    # Counter untuk mengirim data
    sample_count = 0
    send_interval = 100  # Kirim setiap 100 samples (1 detik jika sample_rate = 100)
    
    try:
        while True:
            # Baca data dari sensor
            red, ir = sensor.read_sequential()
            
            # Tambahkan sample ke detector
            if ir is not None:
                hr_detector.add_sample(ir)
                sample_count += 1
                
                # Hitung BPM setiap interval tertentu
                if sample_count >= send_interval:
                    bpm = hr_detector.get_bpm()
                    
                    if bpm > 0:
                        print(f"BPM: {bpm} | Status: ", end="")
                        
                        if 60 <= bpm <= 100:
                            print("NORMAL ✓")
                        elif 101 <= bpm <= 120:
                            print("TINGGI ⚠")
                        else:
                            print("BAHAYA ⚠⚠⚠")
                        
                        # Kontrol LED dan Buzzer
                        control_led_buzzer(bpm)
                        
                        # Kirim ke API
                        send_to_api(bpm)
                    else:
                        print("Menunggu data yang valid...")
                    
                    sample_count = 0
            
            # Delay kecil untuk menghindari overload CPU
            time.sleep(0.01)  # 10ms delay = 100 Hz max
    
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user")
    
    except Exception as e:
        print(f"\nError: {e}")
    
    finally:
        # Cleanup
        print("\nMembersihkan GPIO...")
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("Selesai!")


if __name__ == "__main__":
    main()
