import socket
import json
import serial
import subprocess
import threading
import os

# Fungsi untuk menjalankan v4l2rtspserver
def start_rtsp_server():
    print("Menjalankan v4l2rtspserver...")
    home_dir = os.path.expanduser("~")
    rtsp_path = f"{home_dir}/v4l2rtspserver/build/./v4l2rtspserver"
    subprocess.run([rtsp_path, "/dev/video0"])

# Fungsi untuk server socket + koneksi serial
def start_socket_and_serial_server():
    # Setup koneksi serial ke mikrokontroler
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Ganti port & baudrate sesuai kebutuhan
    print("Serial ke mikrokontroler terbuka")

    raspi_ip = '0.0.0.0'
    raspi_port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((raspi_ip, raspi_port))
    sock.listen(1)
    print("Menunggu koneksi socket...")

    conn, addr = sock.accept()
    print(f"Koneksi socket dari {addr}")

    buffer = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("Koneksi client terputus.")
                break
            buffer += data.decode('utf-8')
            
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip():
                    try:
                        detections = json.loads(line)

                        # Jika data deteksi berupa list
                        if isinstance(detections, list):
                            for det in detections:
                                cls = det.get('class')
                                box = det.get('bbox')
                                conf = det.get('confidence')

                                print(f"Class: {cls}, BBox: {box}, Confidence: {conf}")

                                # Format pengiriman ke mikrokontroler
                                message = f"{cls}:{box[0]},{box[1]},{box[2]},{box[3]},{conf}\n"
                                ser.write(message.encode('utf-8'))

                        # Jika data deteksi berupa dict (single object)
                        elif isinstance(detections, dict):
                            cls = detections.get('class')
                            box = detections.get('bbox')
                            conf = detections.get('confidence')

                            print(f"Class: {cls}, BBox: {box}, Confidence: {conf}")

                            message = f"{cls}:{box[0]},{box[1]},{box[2]},{box[3]},{conf}\n"
                            ser.write(message.encode('utf-8'))

                        else:
                            print("Format JSON tidak sesuai")

                    except json.JSONDecodeError as e:
                        print("JSONDecodeError:", e)

    finally:
        print("Menutup koneksi...")
        conn.close()
        ser.close()
        sock.close()

# Jalankan v4l2rtspserver di thread terpisah
rtsp_thread = threading.Thread(target=start_rtsp_server)
rtsp_thread.start()

# Jalankan server socket + serial di thread utama
start_socket_and_serial_server()
