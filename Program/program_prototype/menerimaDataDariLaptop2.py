import socket
import json

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
            detections = json.loads(line)
            print(detections)
