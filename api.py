# api.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- KONEKSI DATABASE XAMPP ---
def get_db_connection():
    """Membuat koneksi database baru"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",            # isi jika ada password
        database="sensor_db"
    )

# ---------------------- KIRIM DATA DARI RASPBERRY / SIMULATOR ----------------------
@app.route("/kirim", methods=["POST"])
def kirim():
    """Endpoint untuk menerima data BPM dari sensor"""
    try:
        data = request.json
        bpm = data.get("bpm")
        
        if bpm is None:
            return jsonify({"status": "ERROR", "message": "BPM tidak ditemukan"}), 400
        
        # Validasi BPM (40-180 adalah range normal untuk manusia)
        if not isinstance(bpm, (int, float)) or bpm < 0 or bpm > 300:
            return jsonify({"status": "ERROR", "message": "BPM tidak valid"}), 400
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO detak_jantung (bpm) VALUES (%s)", (bpm,))
        db.commit()
        cursor.close()
        db.close()
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Data BPM diterima: {bpm}")
        
        return jsonify({"status": "OK", "bpm": bpm})
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"status": "ERROR", "message": "Database error"}), 500
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500


# ---------------------- AMBIL DATA UNTUK WEBSITE ----------------------
@app.route("/data", methods=["GET"])
def ambil():
    """Endpoint untuk mengambil data terbaru untuk ditampilkan di website"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM detak_jantung ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        db.close()
        
        if row:
            return jsonify(row)
        return jsonify({"status": "NO DATA"})
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"status": "ERROR", "message": "Database error"}), 500
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500


# ---------------------- AMBIL DATA HISTORIS ----------------------
@app.route("/history", methods=["GET"])
def history():
    """Endpoint untuk mengambil data historis (untuk grafik yang lebih lengkap)"""
    try:
        # Parameter limit dari query string (default 30)
        limit = request.args.get('limit', default=30, type=int)
        
        # Batasi maksimal 100 data
        if limit > 100:
            limit = 100
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM detak_jantung ORDER BY id DESC LIMIT {limit}")
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        
        # Balik urutan agar dari lama ke baru
        rows.reverse()
        
        return jsonify(rows)
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"status": "ERROR", "message": "Database error"}), 500
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500


# ---------------------- STATISTIK DATA ----------------------
@app.route("/stats", methods=["GET"])
def stats():
    """Endpoint untuk mengambil statistik data BPM"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Ambil statistik
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                MIN(bpm) as min_bpm,
                MAX(bpm) as max_bpm,
                AVG(bpm) as avg_bpm
            FROM detak_jantung
        """)
        stats_data = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        return jsonify(stats_data)
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"status": "ERROR", "message": "Database error"}), 500
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500


# ---------------------- HALAMAN UTAMA ----------------------
@app.route("/")
def home():
    """Halaman utama monitoring"""
    return render_template("index.html") 


# ---------------------- HEALTH CHECK ----------------------
@app.route("/health", methods=["GET"])
def health():
    """Endpoint untuk cek status server"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        db.close()
        
        return jsonify({
            "status": "OK",
            "message": "Server dan database berjalan normal",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SERVER API MONITORING DETAK JANTUNG")
    print("="*60)
    print("Server berjalan di: http://0.0.0.0:5000")
    print("Endpoints:")
    print("  - POST /kirim    : Terima data dari sensor")
    print("  - GET  /data     : Ambil data terbaru")
    print("  - GET  /history  : Ambil data historis")
    print("  - GET  /stats    : Ambil statistik")
    print("  - GET  /health   : Health check")
    print("  - GET  /         : Website monitoring")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
