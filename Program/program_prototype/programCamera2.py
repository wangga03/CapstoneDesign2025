import cv2
import time
import serial

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera tidak bisa dibuka.")
    exit()

# Inisialisasi serial ke STM32 (ubah ke port sesuai STM32)
ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)

print("Kamera aktif dan mendeteksi objek...")

while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        continue

    # Deteksi objek berdasarkan warna merah
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = (0, 120, 70)
    upper_red = (10, 255, 255)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Format protokol: #x,y\n
            data = f"#{cx},{cy}\n"
            ser.write(data.encode('utf-8'))
            print(f"Dikirim: {data.strip()}")

            # Visualisasi (opsional)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"{cx},{cy}", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    # Tampilkan hasil (opsional)
    cv2.imshow("Deteksi Kamera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Delay agar mendekati 100Hz
    elapsed = time.time() - start_time
    sleep_time = max(0, 0.01 - elapsed)
    time.sleep(sleep_time)

# Bersihkan
cap.release()
cv2.destroyAllWindows()
ser.close()
