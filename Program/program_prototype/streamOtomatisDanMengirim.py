import socket
import json
import subprocess
import threading
import os

# Fungsi untuk menjalankan v4l2rtspserver
def start_rtsp_server():
    print("Menjalankan v4l2rtspserver...")
    home_dir = os.path.expanduser("~")
    rtsp_path = f"{home_dir}/v4l2rtspserver/build/./v4l2rtspserver"
    subprocess.run([rtsp_path, "/dev/video0"])

# Fungsi untuk server socket
def start_socket_server():
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
                    detections = json.loads(line)
                    detected_class = detections.get('class')
                    bbox = detections.get('bbox')
                    confidence = detections.get('confidence')
                    print(f"Class: {detected_class}")
                    print(f"BBox: {bbox}")
                    print(f"Confidence: {confidence}")
                except json.JSONDecodeError as e:
                    print("JSONDecodeError:", e)

# Jalankan v4l2rtspserver di thread terpisah
rtsp_thread = threading.Thread(target=start_rtsp_server)
rtsp_thread.start()

# Jalankan server socket di thread utama
start_socket_server()
