# api.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ---------------------------
# FUNGSI KONEKSI DATABASE
# ---------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sensor_db",
        autocommit=True
    )

# ---------------------- KIRIM DATA BPM ----------------------
@app.route("/kirim", methods=["POST"])
def kirim():
    data = request.json
    bpm = data.get("bpm")

    if bpm is None:
        return jsonify({"error": "bpm kosong"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO detak_jantung (bpm) VALUES (%s)",
        (bpm,)
    )

    cursor.close()
    db.close()

    return jsonify({"status": "OK", "bpm": bpm})


# ---------------------- AMBIL DATA ----------------------
@app.route("/data", methods=["GET"])
def ambil():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM detak_jantung ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()

    cursor.close()
    db.close()

    if row:
        return jsonify(row)
    return jsonify({"status": "NO DATA"})


# ---------------------- HOME ----------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
