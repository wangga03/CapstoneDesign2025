import serial

# Gunakan /dev/serial0 yang sudah dikonfigurasi oleh raspi-config
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

print("Menunggu data dari mikrokontroler lewat UART pins...")

try:
    while True:
        line = ser.readline()                  # baca hingga '\n'
        if not line:
            continue
        text = line.decode('utf-8', errors='ignore').strip()
        print(f"Data diterima: {text}")

except KeyboardInterrupt:
    print("\nProgram dihentikan (Ctrl+C).")

finally:
    ser.close()
    print("UART ditutup.")
