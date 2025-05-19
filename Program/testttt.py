import torch
import cv2
import time

# Device CPU
device = torch.device("cpu")
print(f"Using device: {device}")

# Load YOLOv5 Nano
model = torch.hub.load('/home/cd/yolov5', 'custom', 
                       path='/home/cd/CapstoneDesign2025/Program/yolov5n.pt', source='local')
model.to(device)
model.eval()

# Buka kamera
cap = cv2.VideoCapture(0)
TARGET_SIZE = (100, 100)

prev_time = time.time()
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_resized = cv2.resize(frame, TARGET_SIZE)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    with torch.no_grad():
        results = model(frame_rgb, size=320)

    results.render()
    output_frame = results.ims[0].copy()
    frame_count += 1
    fps = frame_count / (time.time() - prev_time)

    cv2.putText(output_frame, f"FPS: {fps:.2f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('YOLOv5n Live', output_frame)
    cv2.imshow('test camera', frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
