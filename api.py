# api.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# --- KONEKSI DATABASE XAMPP ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",            # isi jika ada password
    database="sensor_db"
)

# Pastikan tabel:
# CREATE TABLE bpm_data (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   bpm INT,
#   waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# ---------------------- KIRIM DATA DARI RASPBERRY / SIMULATOR ----------------------
@app.route("/kirim", methods=["POST"])
def kirim():
    data = request.json
    bpm = data.get("bpm")

    cursor = db.cursor()
    cursor.execute("INSERT INTO detak_jantung (bpm) VALUES (%s)", (bpm,))
    db.commit()

    return jsonify({"status": "OK", "bpm": bpm})


# ---------------------- AMBIL DATA UNTUK WEBSITE ----------------------
@app.route("/data", methods=["GET"])
def ambil():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detak_jantung ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()

    if row:
        return jsonify(row)
    return jsonify({"status": "NO DATA"})


@app.route("/")
def home():
    return render_template("index.html") 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
