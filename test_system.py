"""
Script untuk testing koneksi dan konfigurasi sistem
Jalankan script ini untuk memastikan semua komponen berfungsi
"""

import sys
import socket

def test_network():
    """Test koneksi jaringan"""
    print("\n" + "="*60)
    print("1. TEST KONEKSI JARINGAN")
    print("="*60)
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"✓ Hostname: {hostname}")
        print(f"✓ IP Address lokal: {local_ip}")
        
        # Test koneksi internet
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✓ Koneksi internet: OK")
        
        return True
    except Exception as e:
        print(f"✗ Error koneksi jaringan: {e}")
        return False


def test_database():
    """Test koneksi database"""
    print("\n" + "="*60)
    print("2. TEST KONEKSI DATABASE")
    print("="*60)
    
    try:
        import mysql.connector
        
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sensor_db"
        )
        
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM detak_jantung")
        count = cursor.fetchone()[0]
        
        print(f"✓ Koneksi database: OK")
        print(f"✓ Total data di database: {count} records")
        
        cursor.close()
        db.close()
        
        return True
    except ImportError:
        print("✗ Library mysql-connector-python belum terinstall")
        print("  Install dengan: pip install mysql-connector-python")
        return False
    except mysql.connector.Error as e:
        print(f"✗ Error database: {e}")
        print("\nPastikan:")
        print("  - XAMPP MySQL sudah running")
        print("  - Database 'sensor_db' sudah dibuat")
        print("  - Tabel 'detak_jantung' sudah dibuat")
        return False


def test_flask():
    """Test Flask dan dependencies"""
    print("\n" + "="*60)
    print("3. TEST FLASK DAN DEPENDENCIES")
    print("="*60)
    
    missing = []
    
    # Test Flask
    try:
        import flask
        print(f"✓ Flask: {flask.__version__}")
    except ImportError:
        print("✗ Flask belum terinstall")
        missing.append("Flask")
    
    # Test Flask-CORS
    try:
        import flask_cors
        print(f"✓ Flask-CORS: OK")
    except ImportError:
        print("✗ Flask-CORS belum terinstall")
        missing.append("Flask-CORS")
    
    # Test requests
    try:
        import requests
        print(f"✓ requests: {requests.__version__}")
    except ImportError:
        print("✗ requests belum terinstall")
        missing.append("requests")
    
    if missing:
        print(f"\n⚠ Library yang belum terinstall: {', '.join(missing)}")
        print("Install dengan: pip install -r requirements.txt")
        return False
    
    return True


def test_api_server():
    """Test API server"""
    print("\n" + "="*60)
    print("4. TEST API SERVER")
    print("="*60)
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get("http://localhost:5000/health", timeout=3)
        
        if response.status_code == 200:
            print("✓ API Server: Running")
            print(f"✓ Response: {response.json()}")
            return True
        else:
            print(f"✗ API Server response code: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("✗ API Server tidak berjalan")
        print("  Jalankan server dengan: python api.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_raspberry_pi():
    """Test Raspberry Pi components"""
    print("\n" + "="*60)
    print("5. TEST RASPBERRY PI COMPONENTS (Optional)")
    print("="*60)
    
    is_raspberry_pi = False
    
    # Test RPi.GPIO
    try:
        import RPi.GPIO as GPIO
        print("✓ RPi.GPIO: OK")
        is_raspberry_pi = True
    except (ImportError, RuntimeError):
        print("⚠ RPi.GPIO tidak tersedia (Normal jika tidak di Raspberry Pi)")
    
    # Test max30102
    try:
        from max30102 import MAX30102
        print("✓ max30102 library: OK")
        is_raspberry_pi = True
    except ImportError:
        print("⚠ max30102 library tidak tersedia (Normal jika tidak di Raspberry Pi)")
    
    # Test numpy
    try:
        import numpy
        print(f"✓ numpy: {numpy.__version__}")
    except ImportError:
        print("✗ numpy belum terinstall")
        if is_raspberry_pi:
            print("  Install dengan: sudo pip3 install numpy")
    
    return True


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "SYSTEM TEST MONITORING BPM" + " "*16 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Run tests
    results.append(("Koneksi Jaringan", test_network()))
    results.append(("Koneksi Database", test_database()))
    results.append(("Flask Dependencies", test_flask()))
    results.append(("API Server", test_api_server()))
    results.append(("Raspberry Pi Components", test_raspberry_pi()))
    
    # Summary
    print("\n" + "="*60)
    print("RINGKASAN TEST")
    print("="*60)
    
    for name, status in results:
        status_str = "✓ PASS" if status else "✗ FAIL"
        print(f"{name:.<45} {status_str}")
    
    # Overall status
    all_required_passed = all([
        results[0][1],  # Network
        results[1][1],  # Database
        results[2][1],  # Flask
    ])
    
    print("\n" + "="*60)
    if all_required_passed:
        print("✓ SISTEM SIAP DIGUNAKAN!")
        print("\nLangkah selanjutnya:")
        print("1. Jalankan server: python api.py")
        print("2. Buka browser: http://localhost:5000")
        if results[3][1]:
            print("\n⚠ Server sudah berjalan!")
    else:
        print("✗ SISTEM BELUM SIAP!")
        print("\nPerbaiki error di atas sebelum menjalankan sistem.")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest dibatalkan oleh user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)
