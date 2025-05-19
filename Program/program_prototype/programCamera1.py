import cv2
import time
import serial

# Setup kamera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera tidak bisa dibuka.")
    exit()

# Setup serial (ubah port sesuai kebutuhan STM32)
ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)  # USB1 untuk komunikasi balik ke STM32

print("Kamera aktif dan mendeteksi objek...")

while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    # --- Deteksi objek sederhana (warna merah dalam HSV) ---
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = (0, 120, 70)
    upper_red = (10, 255, 255)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # Koordinat x pusat objek
            cy = int(M["m01"] / M["m00"])  # Koordinat y pusat objek

            # Kirim koordinat ke STM32
            data = f"{cx},{cy}\n"
            ser.write(data.encode('utf-8'))

            # (Opsional) Tampilkan hasil
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"({cx},{cy})", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    # Tampilkan hasil
    cv2.imshow("Deteksi Kamera", frame)

    # Tunggu maksimal 1 ms untuk keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Jaga agar kecepatan ~100Hz
    elapsed = time.time() - start_time
    sleep_time = max(0, 0.01 - elapsed)
    time.sleep(sleep_time)

cap.release()
cv2.destroyAllWindows()
ser.close()
