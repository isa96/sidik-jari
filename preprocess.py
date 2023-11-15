import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hessian_matrix, hessian_matrix_eigvals

def detect_ridges(gray, sigma=3.0):
	# Fungsi ini menggunakan matriks Hessian untuk mendeteksi tepi (ridge) dalam gambar grayscale.
	H_elems = hessian_matrix(gray, sigma=sigma, order='rc')
	maxima_ridges, minima_ridges = hessian_matrix_eigvals(H_elems)
	return maxima_ridges, minima_ridges

def plot_images(*images): 
	# Fungsi ini digunakan untuk menampilkan dan menyimpan gambar.
	# Ini membuat sebuah gambar dengan gambar-gambar yang ditentukan dan menyimpannya sebagai file PNG.
	images = list(images)
	n = len(images)
	fig, ax = plt.subplots(ncols=n, sharey=True)
	for i, img in enumerate(images):
		ax[i].imshow(img, cmap='gray')
		ax[i].axis('off')
		extent = ax[i].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
		plt.savefig('fig'+str(i)+'.png', bbox_inches=extent)
	plt.subplots_adjust(left=0.03, bottom=0.03, right=0.97, top=0.97)
	plt.show()

def main():
	# -------------------------- Langkah 1: Mengimpor gambar yang latar belakangnya telah dihapus ----------
	# Langkah 1: Gambar input dimuat menggunakan cv2.imread. 
	# Gambar ini seharusnya sudah memiliki latar belakangnya dihapus, seperti yang diindikasikan dalam langkah sebelumnya dalam kode.

	img = cv2.imread("input.jpg",1)

	# -------------------------- Langkah 2: Mengasah gambar ------------------------------------------------
	# Langkah 2: Gambar diasah menggunakan kernel pengasahan untuk meningkatkan tepi.
	kernel = np.array([[-1,-1,-1], 
                   [-1, 9,-1],
                   [-1,-1,-1]])
	sharpened = cv2.filter2D(img, -1, kernel)

	# --------------------------- Langkah 3: Mengonversi gambar menjadi grayscale --------------------------
	# Langkah 3: Gambar yang telah diasah dikonversi menjadi grayscale.
	gray = cv2.cvtColor(sharpened,cv2.COLOR_BGR2GRAY)

	# --------------------------- Langkah 4: Melakukan ekualisasi histogram --------------------------------
	# Langkah 4: Ekualisasi histogram diterapkan pada gambar grayscale untuk meningkatkan kontras.
	hist,bins = np.histogram(gray.flatten(),256,[0,256])
	cdf = hist.cumsum()
	cdf_normalized = cdf * hist.max()/ cdf.max()

	cdf_m = np.ma.masked_equal(cdf,0)
	cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
	cdf = np.ma.filled(cdf_m,0).astype('uint8')

	img2=cdf[gray]

	# ----------------------------- Langkah 5: Filter Deteksi Ridge ----------------------------------------
	# Langkah 5: Fungsi detect_ridges dipanggil pada gambar yang telah diproses untuk mendeteksi tepi,
	# dan hasilnya ditampilkan menggunakan plot_images.
	# sigma = 2.7
	a, b = detect_ridges(img2, sigma=2.7)
	plot_images(a, b)

	# ----------------------------- Langkah 6: Mengonversi gambar menjadi gambar biner ---------------------
	# Langkah 6: Gambar hasil dari Langkah 5 dikonversi menjadi gambar biner,
	# dan berbagai langkah pemrosesan gambar diterapkan.
	img = cv2.imread('fig1.png',0)
	bg = cv2.dilate(img,np.ones((5,5),dtype=np.uint8))
	bg = cv2.GaussianBlur(bg,(5,5),1)
	src_no_bg = 255 - cv2.absdiff(img,bg)
	ret,thresh = cv2.threshold(src_no_bg,240,255,cv2.THRESH_BINARY)

	# --------------------------- Langkah 7: Algoritma Penebalan / Skeletal -------------------------------
	# Langkah 7: Operasi penipisan ("Thinning") dilakukan pada gambar biner,
	# dan hasilnya ditampilkan dan disimpan sebagai "trial-out.png."
	thinned = cv2.ximgproc.thinning(thresh)
	cv2.imshow("thinned",thinned)
	cv2.imwrite("./trial-out.png",thinned)

	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__=='__main__':
	main()
