import torch
import cv2

# Paksa penggunaan CPU
device = torch.device("cpu")
print(f"Using device: {device}")  # Menampilkan device yang digunakan

# Load YOLOv5 model (pastikan path model benar)
model = torch.hub.load('/home/cd/yolov5', 'custom', 
                       path='/home/cd/CapstoneDesign2025/PPT5_15BEST.pt', 
                       source='local', force_reload=True)

# Pindahkan model ke CPU
model.to(device)
model.eval()  # Mode evaluasi

# Gunakan FP16 jika model mendukung
# model.half()

# Buka kamera
cap = cv2.VideoCapture(0)

# Variabel FPS
fps_start_time = cv2.getTickCount()
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize untuk mempercepat inferensi di CPU
    frame_resized = cv2.resize(frame, (640, 640))

    # Konversi BGR ke RGB karena YOLO membutuhkan input RGB
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # Inferensi (tanpa gradient untuk efisiensi)
    with torch.no_grad():
        results = model(frame_rgb)

    # Render hasil deteksi dan buat salinan agar bisa dimodifikasi
    frame_output = results.render()[0].copy()
    frame_output.flags.writeable = True  # Pastikan frame bisa dimodifikasi

    # Perhitungan FPS
    frame_count += 1
    fps_end_time = cv2.getTickCount()
    time_elapsed = (fps_end_time - fps_start_time) / cv2.getTickFrequency()
    fps = frame_count / time_elapsed

    # Tampilkan FPS di frame
    cv2.putText(frame_output, f"FPS: {fps:.2f} | Device: CPU", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Tampilkan hasil deteksi
    cv2.imshow('YOLOv5-Lite Live Camera (CPU)', frame_output)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import torch
import cv2
import time

# Gunakan CPU
device = torch.device("cpu")
print(f"Using device: {device}")

# Load YOLOv5 model yang ringan (misalnya: YOLOv5n atau YOLOv5s)
model = torch.hub.load('/home/cd/yolov5', 'custom',
                       path='/home/cd/CapstoneDesign2025/PPT5_15BEST.pt',
                       source='local')  # Jangan force_reload untuk efisiensi
model.to(device)
model.eval()

# Buka kamera
cap = cv2.VideoCapture(0)

# Ukuran frame yang lebih kecil untuk inferensi lebih cepat
TARGET_SIZE = (320, 320)

# Inisialisasi FPS
prev_time = time.time()
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame untuk inferensi cepat
    frame_resized = cv2.resize(frame, TARGET_SIZE)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # Inference
    with torch.no_grad():
        results = model(frame_rgb, size=320)  # Pastikan ukuran sesuai TARGET_SIZE

    # Render hasil deteksi
    results.render()

    # Hitung FPS
    frame_count += 1
    current_time = time.time()
    fps = frame_count / (current_time - prev_time)

    # Tampilkan FPS
    output_frame = results.ims[0]
    cv2.putText(output_frame, f"FPS: {fps:.2f} | CPU", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow('YOLOv5-Lite Live (RasPi)', output_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
