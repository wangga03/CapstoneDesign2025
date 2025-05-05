import serial
import time

def kirim_data_ascii(port, sensor1, sensor2, status):
    with serial.Serial(port, 115200, timeout=1) as ser:
        data = f"{sensor1},{sensor2:.2f},{status}\n"
        ser.write(data.encode())
        print(f"Dikirim (ASCII): {data.strip()}")

def baca_data_ascii(port):
    with serial.Serial(port, 115200, timeout=1) as ser:
        line = ser.readline().decode().strip()
        if line:
            try:
                sensor1, sensor2, status = line.split(',')
                print(f"Dibaca (ASCII): sensor1={sensor1}, sensor2={sensor2}, status={status}")
            except ValueError:
                print("Format salah")

def kirim_kalimat(port, *kalimat):
    with serial.Serial(port, 115200, timeout=1) as ser:
        # Gabungkan semua argumen kalimat, pisahkan dengan '|'
        data = '|'.join(kalimat) + '\n'
        ser.write(data.encode())
        print(f"Dikirim (kalimat): {data.strip()}")

def baca_kalimat(port):
    with serial.Serial(port, 115200, timeout=1) as ser:
        line = ser.readline().decode().strip()
        if line:
            kalimat_list = line.split('|')  # Pisahkan berdasarkan delimiter
            print("Dibaca (kalimat):")
            for i, kalimat in enumerate(kalimat_list):
                print(f"  Kalimat {i+1}: {kalimat}")
        else:
            print("Tidak ada data")
# Contoh penggunaan
# kirim_data_ascii('COM4', 123, 45.67, 1)
# baca_data_ascii('COM4')
