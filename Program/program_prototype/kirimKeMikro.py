import socket
import json
import serial
import subprocess
import threading
import os
import struct

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

                        selected_detections = {}

                        # Jika data deteksi berupa list
                        if isinstance(detections, list):
                            for det in detections:
                                cls = det.get('class')
                                if cls not in selected_detections:
                                    selected_detections[cls] = det
                        # Jika data deteksi berupa dict
                        elif isinstance(detections, dict):
                            cls = detections.get('class')
                            selected_detections[cls] = detections
                        else:
                            print("Format JSON tidak sesuai")

                        # Kirim masing-masing class (pertama kali muncul)
                        for cls, det in selected_detections.items():
                            box = det.get('bbox', [0,0,0,0])
                            conf = det.get('confidence', 0.0)
                            class_id = int(cls) if cls.isdigit() else 0

                            # Packing struct: misal format 'B 4H f' (1-byte class, 4x uint16_t, 1x float)
                            data_struct = struct.pack('<B4Hf', class_id,
                                int(box[0]), int(box[1]), int(box[2]), int(box[3]), float(conf))
                            ser.write(data_struct)
                            print(f"Kirim struct ke STM32: class={class_id}, bbox={box}, conf={conf}")

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
