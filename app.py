import cv2
import numpy as np
import streamlit as st

# Fungsi untuk menghapus latar belakang dari gambar
def remove_background(image):
    # Proses penghapusan latar belakang (kode dari kode pertama)
    height, width = image.shape[:2]
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (10, 10, width - 30, height - 30)
    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    img1 = image * mask[:, :, np.newaxis]
    background = cv2.absdiff(image, img1)
    background[np.where((background > [0, 0, 0]).all(axis=2))] = [255, 255, 255]
    final = background + img1
    return final

# Tampilan aplikasi menggunakan Streamlit
def main():
    st.title("Aplikasi Penghapusan Latar Belakang")

    # Unggah gambar dari pengguna
    uploaded_image = st.file_uploader("Unggah gambar", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Baca gambar yang diunggah
        image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)

        # Hapus latar belakang
        result_image = remove_background(image)

        # Tampilkan gambar yang telah diproses
        st.image(result_image, caption="Hasil Penghapusan Latar Belakang", use_column_width=True)

if __name__ == "__main__":
    main()
