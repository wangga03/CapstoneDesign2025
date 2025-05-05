import serial
import struct
import time

def kirim_data_struct(port, sensor1, sensor2, status):
    with serial.Serial(port, 115200, timeout=1) as ser:
        # Struct format: <hfb -> little-endian, int16, float, uint8
        data = struct.pack('<hfb', sensor1, sensor2, status)
        ser.write(data)
        print(f"Dikirim (binary): {data.hex()}")

def baca_data_struct(port):
    with serial.Serial(port, 115200, timeout=1) as ser:
        data = ser.read(7)  # 2+4+1 byte
        if len(data) == 7:
            sensor1, sensor2, status = struct.unpack('<hfb', data)
            print(f"Dibaca (binary): sensor1={sensor1}, sensor2={sensor2:.2f}, status={status}")
        else:
            print("Data tidak lengkap")

# Contoh penggunaan
# kirim_data_struct('COM4', 123, 45.67, 1)
# baca_data_struct('COM4')
