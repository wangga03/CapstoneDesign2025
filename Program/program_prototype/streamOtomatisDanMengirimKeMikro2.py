import socket
import json
import serial
import subprocess
import threading
import os
import signal
import sys
import time

rtsp_process = None  # Handle proses v4l2rtspserver
sock = None         # Socket global agar bisa ditutup di signal handler

# Fungsi untuk menjalankan v4l2rtspserver
def start_rtsp_server():
    global rtsp_process
    print("Menjalankan v4l2rtspserver...")
    home_dir = os.path.expanduser("~")
    rtsp_path = f"{home_dir}/v4l2rtspserver/build/./v4l2rtspserver"
    rtsp_process = subprocess.Popen([rtsp_path, "/dev/video0"])
    # Jangan tunggu di sini, biarkan berjalan di background

# Fungsi untuk menghentikan v4l2rtspserver
def stop_rtsp_server():
    global rtsp_process
    if rtsp_process is not None and rtsp_process.poll() is None:
        print("Menghentikan v4l2rtspserver...")
        rtsp_process.terminate()
        try:
            rtsp_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Proses v4l2rtspserver tidak merespon, membunuh paksa...")
            rtsp_process.kill()
        rtsp_process = None

# Fungsi server socket + koneksi serial
def start_socket_and_serial_server():
    global sock
    ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)  # Sesuaikan port & baudrate
    print("Serial ke mikrokontroler terbuka")

    raspi_ip = '0.0.0.0'
    raspi_port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((raspi_ip, raspi_port))
    sock.listen(1)
    print(f"Socket server berjalan di {raspi_ip}:{raspi_port}")

    while True:
        print("Menunggu koneksi client baru...")
        try:
            conn, addr = sock.accept()
        except OSError:
            # Socket mungkin sudah ditutup dari signal handler
            print("Socket ditutup, keluar dari loop accept")
            break
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

                            if isinstance(detections, list):
                                for det in detections:
                                    cls = det.get('class')
                                    box = det.get('bbox')
                                    conf = det.get('confidence')
                                    message = f"A{cls}B{int(box[0])}C{int(box[1])}D{int(box[2])}E{int(box[3])}\n"
                                    print(message)
                                    ser.write(message.encode('utf-8'))

                            elif isinstance(detections, dict):
                                cls = detections.get('class')
                                box = detections.get('bbox')
                                conf = detections.get('confidence')
                                message = f"A{cls}B{int(box[0])}C{int(box[1])}D{int(box[2])}E{int(box[3])}\n"
                                print(message)
                                ser.write(message.encode('utf-8'))
                            else:
                                print("Format JSON tidak sesuai")

                        except json.JSONDecodeError as e:
                            print("JSONDecodeError:", e)
        except Exception as e:
            print(f"Error koneksi: {e}")
        finally:
            print("Menutup koneksi client.")
            conn.close()

    ser.close()
    sock.close()
    print("Server socket dan serial ditutup.")

# Handler untuk sinyal terminate (Ctrl+C atau kill)
def signal_handler(sig, frame):
    print("\nMenerima sinyal terminate. Membersihkan...")
    global sock
    if sock:
        try:
            sock.close()
            print("Socket server ditutup.")
        except Exception as e:
            print(f"Error saat menutup socket: {e}")
    stop_rtsp_server()
    sys.exit(0)

# Register handler sinyal
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    # Jalankan v4l2rtspserver di thread terpisah
    rtsp_thread = threading.Thread(target=start_rtsp_server, daemon=True)
    rtsp_thread.start()

    try:
        # Jalankan server socket + serial di thread utama
        start_socket_and_serial_server()
    finally:
        stop_rtsp_server()
