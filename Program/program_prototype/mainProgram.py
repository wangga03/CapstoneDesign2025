import serial
import subprocess
import time
import os

# Konfigurasi port serial (ubah sesuai port Anda)
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)  # Sesuaikan port
print("Menunggu perintah dari mikrokontroler...")

process = None

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Perintah diterima: {data}")

            if data == "otomatis\0":
                print("Masuk sini")
                if process is None or process.poll() is not None:
                    print("Menjalankan menerimaDanMengirimKeMikro.py...")
                    process = subprocess.Popen(['python3', 'streamOtomatisDanMengirimKeMikro2.py'])
                else:
                    print("Program sudah berjalan.")

            elif data == "manual\0":
                if process is not None and process.poll() is None:
                    print("Menghentikan menerimaDanMengirimKeMikro.py...")
                    process.terminate()
                    process.wait()
                    process = None
                else:
                    print("Program tidak sedang berjalan.")

            elif data == "off\0":
                print("Perintah OFF diterima. Raspberry Pi akan dimatikan...")
                if process is not None and process.poll() is None:
                    print("Menghentikan menerimaDanMengirimKeMikro.py sebelum shutdown...")
                    process.terminate()
                    process.wait()
                ser.close()
                os.system("sudo shutdown now")  # Perintah untuk shutdown Raspberry Pi

        time.sleep(0.1)

except KeyboardInterrupt:
    print("monitorSerial.py dihentikan manual (Ctrl+C).")
finally:
    if process is not None and process.poll() is None:
        print("Menghentikan menerimaDanMengirimKeMikro.py sebelum keluar...")
        process.terminate()
        process.wait()
    ser.close()
    print("Serial ditutup.")
