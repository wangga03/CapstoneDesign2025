import socket
import json

server = socket.socket()
server.bind(('0.0.0.0', 12345))
server.listen(1)
conn, addr = server.accept()

while True:
    data = conn.recv(4096)
    if not data:
        break
    detections = json.loads(data.decode('utf-8'))
    print("Deteksi:", detections)
