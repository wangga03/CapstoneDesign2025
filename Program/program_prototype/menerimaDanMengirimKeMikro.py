import socket
import json
import serial

# Setup koneksi serial ke mikrokontroler
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Ganti port & baudrate sesuai kebutuhan

raspi_ip = '0.0.0.0'
raspi_port = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((raspi_ip, raspi_port))
sock.listen(1)
print("Menunggu koneksi...")

conn, addr = sock.accept()
print(f"Koneksi dari {addr}")

buffer = ""
while True:
    data = conn.recv(1024)
    if not data:
        break
    buffer += data.decode('utf-8')
    
    while '\n' in buffer:
        line, buffer = buffer.split('\n', 1)
        if line.strip():
            try:
                # Ambil list deteksi dari YOLO (format: list of dict)
                detections = json.loads(line)

                # Cek apakah data dalam bentuk list
                if isinstance(detections, list):
                    for det in detections:
                        cls = det.get('class')
                        conf = det.get('conf')
                        box = det.get('box')

                        print(f"Class: {cls}, BBox: {box}, Confidence: {conf}")

                        # Format pengiriman: class:x1,y1,x2,y2,confidence
                        message = f"{cls}:{box[0]},{box[1]},{box[2]},{box[3]},{conf}\n"
                        ser.write(message.encode('utf-8'))

                else:
                    print("Format JSON tidak sesuai (bukan list)")

            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)

# Tutup koneksi
conn.close()
ser.close()
sock.close()
