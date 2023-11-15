import cv2
import numpy as np

# Membaca gambar dari file 'f1.jpeg' menggunakan cv2.imread dan menampilkannya dalam jendela menggunakan cv2.imshow.
imgo = cv2.imread('./input/f1.jpeg')
cv2.imshow("imgo", imgo)

# Menghapus latar belakang
height, width = imgo.shape[:2]  # Kemudian kode ini melanjutkan dengan menghapus latar belakang dari gambar.

# Membuat penahan mask
mask = np.zeros(imgo.shape[:2], np.uint8)

# Menggunakan GrabCut untuk mengisolasi objek
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# Membuat batasan objek (Rect) secara manual
rect = (10, 10, width - 30, height - 30)
cv2.grabCut(imgo, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
img1 = imgo * mask[:, :, np.newaxis]

# Mendapatkan latar belakang
background = cv2.absdiff(imgo, img1)

# Mengubah semua piksel di latar belakang yang bukan hitam menjadi putih
background[np.where((background > [0, 0, 0]).all(axis=2))] = [255, 255, 255]

# Menambahkan latar belakang dan gambar
final = background + img1

# Dalam pengembangan - Melunakkan tepi....

cv2.imshow('image', final)
cv2.imwrite("input.jpg", final)

# Skrip ini menunggu tombol ditekan dengan cv2.waitKey(0) dan kemudian menutup semua jendela OpenCV dengan cv2.destroyAllWindows.
cv2.waitKey(0)
cv2.destroyAllWindows()
