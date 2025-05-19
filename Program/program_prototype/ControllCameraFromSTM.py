import serial
import subprocess
import os
import signal

# Konfigurasi port serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# Menyimpan proses kamera
cam_process = None

print("Menunggu perintah dari STM32...")

while True:
    if ser.in_waiting > 0:
        command = ser.readline().decode('utf-8').strip()
        print(f"Perintah diterima: {command}")

        if command == "go":
            subprocess.Popen(["python3", "/home/pi/program_go.py"])

        elif command == "start":
            subprocess.Popen(["python3", "/home/pi/program_start.py"])

        elif command == "cam":
            if cam_process is None or cam_process.poll() is not None:
                cam_process = subprocess.Popen(["python3", "/home/pi/program_cam.py"])
                print("Kamera dinyalakan.")
            else:
                print("Kamera sudah aktif.")

        elif command == "cam_off":
            if cam_process and cam_process.poll() is None:
                cam_process.terminate()  # Kirim sinyal TERM
                try:
                    cam_process.wait(timeout=5)
                    print("Kamera dimatikan.")
                except subprocess.TimeoutExpired:
                    cam_process.kill()
                    print("Kamera dipaksa berhenti.")
                cam_process = None
            else:
                print("Kamera tidak sedang aktif.")
