# 🔌 PANDUAN KONEKSI HARDWARE LENGKAP

## Sistem Monitoring Detak Jantung dengan MAX30102

---

## 📍 PINOUT RASPBERRY PI (GPIO BCM Mode)

```
     3.3V  (1)  (2)  5V
    GPIO2  (3)  (4)  5V
    GPIO3  (5)  (6)  GND  ← Buzzer (-)
    GPIO4  (7)  (8)  GPIO14
      GND  (9) (10)  GPIO15
   GPIO17 (11) (12)  GPIO18  ← LED Anoda (+) via Resistor
   GPIO27 (13) (14)  GND     ← Buzzer (+)
   GPIO22 (15) (16)  GPIO23
     3.3V (17) (18)  GPIO24
   GPIO10 (19) (20)  GND
    GPIO9 (21) (22)  GPIO25
   GPIO11 (23) (24)  GPIO8
      GND (25) (26)  GPIO7
    GPIO0 (27) (28)  GPIO1
    GPIO5 (29) (30)  GND
    GPIO6 (31) (32)  GPIO12
   GPIO13 (33) (34)  GND
   GPIO19 (35) (36)  GPIO16
   GPIO26 (37) (38)  GPIO20
      GND (39) (40)  GPIO21
```

---

## 🔗 KONEKSI DETAIL SETIAP KOMPONEN

### 1️⃣ MAX30102 Sensor (I2C Communication)

**Spesifikasi:**

- Operating Voltage: 3.3V
- Interface: I2C
- I2C Address: 0x57

**Koneksi:**

```
MAX30102 Pin    Wire Color    Raspberry Pi Pin    Description
-----------     ----------    ----------------    -----------
VIN             Merah         Pin 1 (3.3V)       Power supply
GND             Hitam         Pin 6 (GND)        Ground
SDA             Kuning        Pin 3 (GPIO2)      I2C Data
SCL             Hijau         Pin 5 (GPIO3)      I2C Clock
```

**Diagram:**

```
    MAX30102 Sensor
    ┌─────────────┐
    │   [Sensor]  │
    │   MAX30102  │
    ├─────────────┤
    │ VIN ●───────┼───────→ Raspberry Pi Pin 1 (3.3V)
    │ GND ●───────┼───────→ Raspberry Pi Pin 6 (GND)
    │ SDA ●───────┼───────→ Raspberry Pi Pin 3 (GPIO2 - SDA)
    │ SCL ●───────┼───────→ Raspberry Pi Pin 5 (GPIO3 - SCL)
    └─────────────┘
```

**⚠️ PENTING:**

- Gunakan 3.3V, JANGAN 5V! (Bisa merusak sensor)
- Pastikan koneksi SDA dan SCL tidak terbalik
- Sensor harus menyentuh kulit untuk berfungsi

---

### 2️⃣ LED Indicator

**Spesifikasi:**

- Type: LED 5mm (Merah/Kuning/Orange)
- Forward Voltage: ~2V
- Forward Current: 20mA
- Resistor: 220Ω (untuk membatasi arus)

**Koneksi:**

```
LED Pin         Wire Color    Component          Raspberry Pi
-------         ----------    ---------          ------------
Anoda (+)       Merah         Direct             Pin 11 (GPIO17)
                              ↓
Katoda (-)      Hitam         Resistor 220Ω      Pin 6 (GND)
                              ↓
                              GND
```

**Diagram:**

```
    GPIO17 (Pin 11)
         │
         │  +
    ┌────▼────┐
    │   LED   │  (Merah/Kuning)
    └────┬────┘
         │  -
         │
    ┌────▼────┐
    │ 220Ω    │  (Resistor)
    │Resistor │
    └────┬────┘
         │
         ▼
       GND (Pin 6)
```

**Cara Mengenali Kaki LED:**

```
     Anoda (+)        Katoda (-)
    Kaki Panjang      Kaki Pendek
         │                │
         │                │
         └────┐      ┌────┘
              │      │
          ┌───▼──────▼───┐
          │   🔴  LED    │
          └──────────────┘
           (Bagian pipih di sisi katoda)
```

**⚠️ PENTING:**

- LED punya polaritas! Jangan terbalik!
- Anoda (+) = kaki panjang → ke GPIO17
- Katoda (-) = kaki pendek → ke GND via resistor
- WAJIB pakai resistor untuk melindungi LED!

---

### 3️⃣ Buzzer Alarm

**Spesifikasi:**

- Type: Active Buzzer (atau Passive Buzzer)
- Operating Voltage: 3.3-5V
- Frequency: 2-4 kHz (jika passive)

**Koneksi:**

```
Buzzer Pin      Wire Color    Raspberry Pi Pin    GPIO
----------      ----------    ----------------    ----
Positive (+)    Merah         Pin 13              GPIO27
Negative (-)    Hitam         Pin 14              GND
```

**Diagram:**

```
    GPIO27 (Pin 13)
         │
         │  +
    ┌────▼────┐
    │         │
    │ 🔊      │  (Active Buzzer)
    │ BUZZER  │
    │         │
    └────┬────┘
         │  -
         ▼
       GND (Pin 14)
```

**Perbedaan Active vs Passive Buzzer:**

| Type        | Karakteristik           | Pin   | Kegunaan                            |
| ----------- | ----------------------- | ----- | ----------------------------------- |
| **Active**  | Ada oscillator internal | 2 pin | Bunyi langsung saat diberi tegangan |
| **Passive** | Butuh sinyal PWM        | 2 pin | Bisa atur frekuensi/nada            |

**Cara Membedakan:**

```
Active Buzzer           Passive Buzzer
┌─────────────┐        ┌─────────────┐
│   Tertutup  │        │   Terbuka   │
│  (Sealed)   │        │  (Open)     │
│   [Logo]    │        │ [Circuitry] │
└─────────────┘        └─────────────┘
```

**⚠️ PENTING:**

- Cek polaritas di body buzzer (+/-)
- Active buzzer langsung bunyi saat GPIO HIGH
- Passive buzzer butuh PWM untuk bunyi

---

## 🔧 WIRING DIAGRAM LENGKAP

### Tampilan Atas (Top View)

```
                    RASPBERRY PI 4B
    ╔═══════════════════════════════════════════╗
    ║  USB  USB                    [Ethernet]   ║
    ║  USB  USB                       USB-C     ║
    ╠═══════════════════════════════════════════╣
    ║                                           ║
    ║    ┌─────┐  ┌─────┐  ┌─────┐             ║
    ║    │ 1 2 │  │     │  │     │   GPIO      ║
    ║    │ 3 4 │  │     │  │     │   PINS      ║
    ║    │ 5 6 │  │ CPU │  │ RAM │   ↓↓↓       ║
    ║    │ ... │  │     │  │     │   1──40     ║
    ║    └─────┘  └─────┘  └─────┘             ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
           │ │ │
           │ │ └──→ Pin 6 (GND)
           │ └────→ Pin 3 (GPIO2 - SDA)
           └──────→ Pin 1 (3.3V)
```

### Breadboard Layout

```
                    BREADBOARD
    ┌───────────────────────────────────────┐
    │  + Rail ────────────────── (3.3V)     │
    │  - Rail ────────────────── (GND)      │
    │                                       │
    │     MAX30102                          │
    │    ┌──────┐                           │
    │    │Sensor│                           │
    │    └──┬───┘                           │
    │       ├── VIN → + Rail                │
    │       ├── GND → - Rail                │
    │       ├── SDA → GPIO2                 │
    │       └── SCL → GPIO3                 │
    │                                       │
    │           LED    220Ω                 │
    │     GPIO17 ─┬─ ─▶│ ─┬─ Resistor ─┐  │
    │             └──────┘  │           │   │
    │                       └─────── GND    │
    │                                       │
    │           BUZZER                      │
    │     GPIO27 ─┬─ (+)                   │
    │             └─ (-)─── GND             │
    │                                       │
    └───────────────────────────────────────┘
```

### Schematic Complete

```
┌─────────────────────────────────────────────────────────┐
│                   RASPBERRY PI 4B                       │
│                                                         │
│  Pin 1  (3.3V)  ●──────┬────────→ MAX30102 VIN        │
│  Pin 3  (GPIO2) ●──────┼────────→ MAX30102 SDA        │
│  Pin 5  (GPIO3) ●──────┼────────→ MAX30102 SCL        │
│  Pin 6  (GND)   ●──────┼────┬───→ MAX30102 GND        │
│  Pin 11 (GPIO17)●──────┼────│                          │
│  Pin 13 (GPIO27)●──────┼────│                          │
│  Pin 14 (GND)   ●──────┼────│                          │
└─────────────────────────┼────┼──────────────────────────┘
                         │    │
                         │    └────┬───────────────────┐
                         │         │                   │
                    ┌────▼─────┐  │    ┌───────┐      │
                    │ MAX30102 │  │    │ 220Ω  │      │
                    │  Sensor  │  │    │Resist │      │
                    └──────────┘  │    └───┬───┘      │
                                  │        │          │
                                  │    ┌───▼───┐      │
                                  │    │  LED  │      │
                                  │    └───┬───┘      │
                    GPIO17 ───────┘        │          │
                                           │          │
                    GPIO27 ─────────┬──────┼──────────┘
                                    │      │
                                ┌───▼──┐   │
                                │Buzzer│   │
                                └───┬──┘   │
                                    │      │
                                    └──────┴─────→ GND
```

---

## 🔍 TESTING KONEKSI

### Test I2C Connection

```bash
# Install i2c-tools
sudo apt-get install i2c-tools

# Scan I2C devices
sudo i2cdetect -y 1

# Output yang diharapkan:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:          -- -- -- -- -- -- -- -- -- -- -- -- --
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 50: -- -- -- -- -- -- -- 57 -- -- -- -- -- -- -- --  ← MAX30102
# 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 70: -- -- -- -- -- -- -- --
```

### Test LED

```bash
# Nyalakan LED
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(17, GPIO.OUT); GPIO.output(17, GPIO.HIGH); input('Press Enter to turn off...'); GPIO.output(17, GPIO.LOW); GPIO.cleanup()"
```

### Test Buzzer

```bash
# Nyalakan Buzzer
sudo python3 -c "import RPi.GPIO as GPIO; import time; GPIO.setmode(GPIO.BCM); GPIO.setup(27, GPIO.OUT); GPIO.output(27, GPIO.HIGH); time.sleep(1); GPIO.output(27, GPIO.LOW); GPIO.cleanup()"
```

---

## 📦 KOMPONEN YANG DIBUTUHKAN

| No  | Komponen        | Jumlah | Spesifikasi            | Harga (est.)           |
| --- | --------------- | ------ | ---------------------- | ---------------------- |
| 1   | Raspberry Pi 4B | 1      | 2GB/4GB RAM            | Rp 800.000 - 1.200.000 |
| 2   | MAX30102 Module | 1      | Heart rate & SpO2      | Rp 50.000 - 100.000    |
| 3   | LED 5mm         | 1      | Merah/Kuning           | Rp 500                 |
| 4   | Active Buzzer   | 1      | 3.3V - 5V              | Rp 2.000 - 5.000       |
| 5   | Resistor 220Ω   | 1      | 1/4W                   | Rp 100                 |
| 6   | Breadboard      | 1      | 400 tie-points         | Rp 10.000 - 20.000     |
| 7   | Jumper Wires    | 10-15  | Male-Female, Male-Male | Rp 10.000              |
| 8   | MicroSD Card    | 1      | 16GB+ (untuk OS)       | Rp 50.000 - 100.000    |
| 9   | Power Supply    | 1      | 5V 3A USB-C            | Rp 50.000 - 80.000     |

**Total Estimasi:** Rp 1.000.000 - 1.500.000

---

## ⚠️ SAFETY TIPS

1. **Matikan Raspberry Pi** sebelum menghubungkan/melepas komponen
2. **Cek polaritas** LED dan Buzzer sebelum menghubungkan
3. **Jangan hubungkan sensor ke 5V** - gunakan 3.3V!
4. **Gunakan resistor** untuk LED
5. **Periksa koneksi** sebelum menyalakan power
6. **Ground first** - hubungkan ground terlebih dahulu
7. **Test bertahap** - test satu komponen satu per satu

---

## 🐛 TROUBLESHOOTING HARDWARE

| Masalah                   | Kemungkinan Penyebab | Solusi                           |
| ------------------------- | -------------------- | -------------------------------- |
| MAX30102 tidak terdeteksi | Koneksi I2C salah    | Cek SDA/SCL, gunakan `i2cdetect` |
| LED tidak menyala         | Polaritas terbalik   | Balik arah LED                   |
| Buzzer tidak bunyi        | GPIO tidak HIGH      | Cek code, test manual            |
| Sensor tidak baca nilai   | Jari tidak menempel  | Tekan jari ke sensor             |
| Nilai BPM kacau           | Koneksi tidak stabil | Cek kabel jumper                 |

---

## 📸 FOTO REFERENSI

### MAX30102 Pinout

```
    ┌─────────────────┐
    │   MAX30102      │
    │   [Sensor]      │
    │                 │
    │  ┌───────────┐  │
    │  │  [Red ]   │  │  ← Sensor Area (Tempelkan jari di sini)
    │  │  [Infrared│  │
    │  └───────────┘  │
    │                 │
    │  VIN GND SDA SCL│
    │   o   o   o   o │
    └─────────────────┘
```

### LED 5mm

```
        Anoda (+)
    Kaki Panjang
         │
         │
    ┌────▼────┐
    │    ●    │  ← Bulb
    │   ╱ ╲   │
    │  ╱   ╲  │
    │ └─────┘ │
    └────┬────┘
         │
    Kaki Pendek
      Katoda (-)

    Side View:      Top View:
       A            ┌─────┐
       │            │  ○  │  ← Light emitting
       ⚡            │ ╱─╲ │
       │            └─────┘
       K
```

### Active Buzzer

```
    Top View:
    ┌─────────┐
    │    +    │  ← Label tanda (+)
    │         │
    │  [PCB]  │  ← Circuit board terlihat
    │         │
    └────┬────┘
         │
    Bottom View:
    ┌─────────┐
    │ Pin (+) │
    │ Pin (-) │
    └─────────┘
```

---

**💡 TIP:** Print halaman ini sebagai referensi saat melakukan wiring!
