import cv2

# Inisialisasi kamera (biasanya 0 untuk USB Camera atau kamera Pi default)
cap = cv2.VideoCapture(0)

# Cek apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Kamera tidak bisa diakses.")
    exit()

print("Menampilkan video dari kamera. Tekan 'q' untuk keluar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame dari kamera.")
        break

    # Tampilkan hasil tangkapan kamera
    cv2.imshow("Kamera Live", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepaskan kamera dan tutup jendela
cap.release()
cv2.destroyAllWindows()
