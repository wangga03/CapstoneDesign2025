import cv2

cap = cv2.VideoCapture('rtsp://192.168.1.41:8554/unicast')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame.")
        break

    cv2.imshow('Stream Kamera Raspi', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
