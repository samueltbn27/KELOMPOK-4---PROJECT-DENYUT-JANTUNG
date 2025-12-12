# simulate_sensor.py
import requests
import random
import time

API_URL = "http://localhost:5000/kirim"

print("Simulasi sensor BPM berjalan... CTRL + C untuk stop.\n")

while True:
    bpm_random = random.randint(55, 130)

    payload = {"bpm": bpm_random}
    try:
        r = requests.post(API_URL, json=payload)
        print("Kirim BPM:", bpm_random, "| Response:", r.text)
    except:
        print("Gagal mengirim data ke API!")

    time.sleep(3)
