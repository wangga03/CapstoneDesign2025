import serial
import time
import random

# Ganti port serial sesuai perangkat kamu
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# List class dummy (contoh objek)
classes = ['0', '1']

try:
    while True:
        packet_data = ""  # Buffer untuk menampung semua data sekaligus
        
        for detected_class in classes:
            confidence = round(random.uniform(0.5, 0.99), 2)
            xmin = random.randint(0, 640)
            ymin = random.randint(0, 480)
            xmax = xmin + random.randint(10, 100)
            ymax = ymin + random.randint(10, 100)
            
            # Format data per class
            data_str = f"A{detected_class}B{xmin}C{ymin}D{xmax}E{ymax}"
            packet_data += data_str  # Gabungkan string
        
        # Tambahkan newline di akhir paket
        packet_data += '\n'
        
        # Kirimkan seluruh paket
        ser.write(packet_data.encode('utf-8'))
        print(f"Kirim data: {packet_data.strip()}")
        
        time.sleep(0.01)  # kirim setiap 100ms

except KeyboardInterrupt:
    print("Program dihentikan.")
finally:
    ser.close()
