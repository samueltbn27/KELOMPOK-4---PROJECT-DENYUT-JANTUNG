# 📡 API DOCUMENTATION

## REST API untuk Sistem Monitoring Detak Jantung

**Base URL:** `http://localhost:5000` atau `http://[IP_ADDRESS]:5000`

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Examples](#examples)

---

## 🔐 Authentication

Saat ini API tidak menggunakan authentication. Untuk production, disarankan menambahkan:

- API Key
- JWT Token
- OAuth 2.0

---

## 🌐 Endpoints

### 1. Health Check

**GET** `/health`

Cek status server dan koneksi database.

**Response:**

```json
{
  "status": "OK",
  "message": "Server dan database berjalan normal",
  "timestamp": "2025-12-12 14:30:00"
}
```

**Status Codes:**

- `200` - Server OK
- `500` - Server/Database error

**Example:**

```bash
curl http://localhost:5000/health
```

---

### 2. Send BPM Data

**POST** `/kirim`

Kirim data BPM dari sensor ke server.

**Headers:**

```
Content-Type: application/json
```

**Request Body:**

```json
{
  "bpm": 75
}
```

**Response Success:**

```json
{
  "status": "OK",
  "bpm": 75
}
```

**Response Error:**

```json
{
  "status": "ERROR",
  "message": "BPM tidak valid"
}
```

**Status Codes:**

- `200` - Data berhasil disimpan
- `400` - Request tidak valid
- `500` - Server error

**Validasi:**

- `bpm` harus integer atau float
- `bpm` harus antara 0 - 300
- Field `bpm` wajib ada

**Example:**

```bash
# curl
curl -X POST http://localhost:5000/kirim \
  -H "Content-Type: application/json" \
  -d '{"bpm": 75}'

# Python
import requests
response = requests.post(
    "http://localhost:5000/kirim",
    json={"bpm": 75}
)
print(response.json())
```

---

### 3. Get Latest Data

**GET** `/data`

Ambil data BPM terbaru (1 record terakhir).

**Response Success:**

```json
{
  "id": 123,
  "bpm": 75,
  "waktu": "2025-12-12 14:30:45"
}
```

**Response No Data:**

```json
{
  "status": "NO DATA"
}
```

**Status Codes:**

- `200` - Success
- `500` - Server error

**Example:**

```bash
curl http://localhost:5000/data
```

---

### 4. Get Historical Data

**GET** `/history?limit=30`

Ambil data historis untuk grafik.

**Query Parameters:**

- `limit` (optional) - Jumlah data yang diambil
  - Default: 30
  - Max: 100
  - Type: integer

**Response:**

```json
[
  {
    "id": 120,
    "bpm": 72,
    "waktu": "2025-12-12 14:30:40"
  },
  {
    "id": 121,
    "bpm": 74,
    "waktu": "2025-12-12 14:30:41"
  },
  ...
]
```

**Note:** Data diurutkan dari lama ke baru (ascending).

**Status Codes:**

- `200` - Success
- `500` - Server error

**Example:**

```bash
# Ambil 30 data terakhir (default)
curl http://localhost:5000/history

# Ambil 50 data terakhir
curl http://localhost:5000/history?limit=50

# Ambil 100 data terakhir (max)
curl http://localhost:5000/history?limit=100
```

---

### 5. Get Statistics

**GET** `/stats`

Ambil statistik data BPM (min, max, avg, total).

**Response:**

```json
{
  "total": 500,
  "min_bpm": 55,
  "max_bpm": 130,
  "avg_bpm": 82.456789
}
```

**Field Description:**

- `total` - Total jumlah record
- `min_bpm` - BPM minimum
- `max_bpm` - BPM maximum
- `avg_bpm` - BPM rata-rata (float)

**Status Codes:**

- `200` - Success
- `500` - Server error

**Example:**

```bash
curl http://localhost:5000/stats
```

---

### 6. Homepage

**GET** `/`

Menampilkan website dashboard monitoring.

**Response:**

- HTML page (templates/index.html)

**Example:**

```bash
# Buka di browser
http://localhost:5000
```

---

## 📊 Data Models

### BPM Data Model

```json
{
  "id": integer,        // Auto increment primary key
  "bpm": integer,       // Heart rate value (40-180 normal)
  "waktu": timestamp    // Auto generated timestamp
}
```

**Database Schema:**

```sql
CREATE TABLE detak_jantung (
  id INT AUTO_INCREMENT PRIMARY KEY,
  bpm INT NOT NULL,
  waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ❌ Error Handling

### Error Response Format

```json
{
  "status": "ERROR",
  "message": "Error description"
}
```

### Common Errors

| Status Code | Message             | Cause                                  |
| ----------- | ------------------- | -------------------------------------- |
| 400         | BPM tidak ditemukan | Field `bpm` tidak ada di request       |
| 400         | BPM tidak valid     | BPM di luar range atau tipe data salah |
| 500         | Database error      | Koneksi database gagal                 |
| 500         | Server error        | Internal server error                  |

---

## ⏱️ Rate Limiting

**Current:** Tidak ada rate limiting

**Recommended untuk Production:**

- Max 60 requests per minute per IP
- Max 1000 requests per hour per IP

**Implementation dengan Flask-Limiter:**

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["60 per minute"]
)

@app.route("/kirim", methods=["POST"])
@limiter.limit("10 per minute")
def kirim():
    # ...
```

---

## 💡 Examples

### Python Client

```python
import requests
import time

API_URL = "http://10.229.1.250:5000"

# 1. Health check
response = requests.get(f"{API_URL}/health")
print("Health:", response.json())

# 2. Send BPM data
bpm_data = {"bpm": 75}
response = requests.post(f"{API_URL}/kirim", json=bpm_data)
print("Send BPM:", response.json())

# 3. Get latest data
response = requests.get(f"{API_URL}/data")
print("Latest:", response.json())

# 4. Get history
response = requests.get(f"{API_URL}/history?limit=10")
print("History:", response.json())

# 5. Get statistics
response = requests.get(f"{API_URL}/stats")
print("Stats:", response.json())
```

### JavaScript Client (Fetch API)

```javascript
const API_URL = "http://10.229.1.250:5000";

// 1. Send BPM data
async function sendBPM(bpm) {
  const response = await fetch(`${API_URL}/kirim`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ bpm: bpm }),
  });
  return await response.json();
}

// 2. Get latest data
async function getLatestData() {
  const response = await fetch(`${API_URL}/data`);
  return await response.json();
}

// 3. Get history
async function getHistory(limit = 30) {
  const response = await fetch(`${API_URL}/history?limit=${limit}`);
  return await response.json();
}

// 4. Get statistics
async function getStats() {
  const response = await fetch(`${API_URL}/stats`);
  return await response.json();
}

// Usage
sendBPM(75).then((data) => console.log("Send result:", data));
getLatestData().then((data) => console.log("Latest:", data));
getHistory(10).then((data) => console.log("History:", data));
getStats().then((data) => console.log("Stats:", data));
```

### Arduino/ESP32 Client

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* apiUrl = "http://10.229.1.250:5000/kirim";

void sendBPM(int bpm) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(apiUrl);
        http.addHeader("Content-Type", "application/json");

        // Create JSON
        StaticJsonDocument<200> doc;
        doc["bpm"] = bpm;
        String jsonString;
        serializeJson(doc, jsonString);

        // Send POST request
        int httpResponseCode = http.POST(jsonString);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Response: " + response);
        } else {
            Serial.println("Error: " + String(httpResponseCode));
        }

        http.end();
    }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");
}

void loop() {
    int bpm = 75; // Get from sensor
    sendBPM(bpm);
    delay(5000); // Send every 5 seconds
}
```

### Raspberry Pi Pico W Client

```python
import network
import urequests
import ujson
import time

# WiFi configuration
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"
API_URL = "http://10.229.1.250:5000/kirim"

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Connecting to WiFi...")
    time.sleep(1)

print("Connected to WiFi:", wlan.ifconfig())

# Send BPM data
def send_bpm(bpm):
    try:
        data = ujson.dumps({"bpm": bpm})
        headers = {"Content-Type": "application/json"}
        response = urequests.post(API_URL, data=data, headers=headers)
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Error:", e)

# Main loop
while True:
    bpm = 75  # Get from sensor
    send_bpm(bpm)
    time.sleep(5)
```

---

## 🔧 CORS Configuration

API menggunakan Flask-CORS untuk mengizinkan cross-origin requests.

**Current Config:**

```python
from flask_cors import CORS
CORS(app)  # Allow all origins
```

**Recommended untuk Production:**

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://example.com", "http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 📈 Response Time

**Typical Response Times:**

- `/health`: ~10-20ms
- `/data`: ~15-30ms
- `/history`: ~30-100ms (depending on limit)
- `/stats`: ~20-40ms
- `/kirim`: ~50-100ms (database write)

---

## 🧪 Testing API

### Using cURL

```bash
# Test all endpoints
curl http://localhost:5000/health
curl http://localhost:5000/data
curl http://localhost:5000/stats
curl http://localhost:5000/history?limit=10
curl -X POST http://localhost:5000/kirim \
  -H "Content-Type: application/json" \
  -d '{"bpm": 75}'
```

### Using Postman

1. Import collection dari file `api_collection.json` (jika ada)
2. Set environment variable `BASE_URL` = `http://localhost:5000`
3. Run collection

### Using Python Requests

```python
import requests

def test_api():
    base_url = "http://localhost:5000"

    # Test health
    r = requests.get(f"{base_url}/health")
    assert r.status_code == 200
    print("✓ Health check passed")

    # Test send data
    r = requests.post(f"{base_url}/kirim", json={"bpm": 75})
    assert r.status_code == 200
    assert r.json()["status"] == "OK"
    print("✓ Send data passed")

    # Test get data
    r = requests.get(f"{base_url}/data")
    assert r.status_code == 200
    assert "bpm" in r.json()
    print("✓ Get data passed")

    print("\n✓ All tests passed!")

if __name__ == "__main__":
    test_api()
```

---

## 📝 Changelog

### Version 1.0 (Current)

- Initial release
- Basic CRUD operations
- Real-time data support
- Statistics endpoint
- CORS enabled

### Planned Features (v1.1)

- [ ] Authentication (API Key)
- [ ] Rate limiting
- [ ] Data filtering by date range
- [ ] Export data to CSV/Excel
- [ ] WebSocket support for real-time updates
- [ ] Multi-user support
- [ ] Alert/notification system

---

## 🤝 Contributing

Untuk menambahkan endpoint baru:

1. Edit `api.py`
2. Tambahkan route function
3. Update dokumentasi ini
4. Test endpoint
5. Update `test_system.py`

---

## 📞 Support

Jika ada pertanyaan atau issue:

- Cek `README.md` untuk dokumentasi lengkap
- Jalankan `test_system.py` untuk diagnostik
- Cek log error di terminal

---

**Last Updated:** December 12, 2025  
**API Version:** 1.0  
**Author:** Project PEMDAS Team
