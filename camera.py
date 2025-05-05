import torch
import cv2

# Paksa penggunaan CPU
device = torch.device("cpu")
print(f"Using device: {device}")  # Menampilkan device yang digunakan

# Load YOLOv5 model (pastikan path model benar)
model = torch.hub.load('/home/wgg/yolov5', 'custom', 
                       path='/home/wgg/ROSTU_SAS/src/krsbi_2025/scripts/KRSBI_50.pt', 
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
