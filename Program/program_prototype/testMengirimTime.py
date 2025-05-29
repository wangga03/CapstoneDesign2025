import serial
import time

# Ganti port serial sesuai perangkat kamu
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

try:
    while True:
        # Ambil waktu saat ini (Unix timestamp dalam detik)
        timestamp = time.time()

        # Kirim timestamp sebagai string diikuti newline
        data_str = f"{timestamp:.6f}\n"  # Contoh: 1717077301.123456\n
        ser.write(data_str.encode('utf-8'))
        print(f"Kirim timestamp: {data_str.strip()}")

        time.sleep(1)  # kirim setiap 1 detik

except KeyboardInterrupt:
    print("Program dihentikan.")
finally:
    ser.close()
