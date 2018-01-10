import cek_hari
import tambah_profil
import lihat_profil

#hari=input("masukan hari: ")
#cek_hari.cek_hari(hari)

print("SELAMAT DATANG DI FAJWA, SILAHKAN PILIH MENU YANG INGIN DIPILIH \n")
print("1. Lihat Profil \n2. Masukan profil baru")
pilihan=input("pilihan: ")

if(pilihan=="1"):
	lihat_profil.lihat_profil()
elif(pilihan=="2"):
	print("---------------------")
	nama_depan=input("masukan nama depan: ")
	nama_belakang=input("masukan nama belakang: ")
	umur=input("masukan umur: ")
	gender=input("masukan gender: ")
	pemasukan=input("masukan pemasukan: ")
	print("----------------------")
	tambah_profil.tambah_profil(nama_depan, nama_belakang, umur, gender, pemasukan)
else:
	print("Anda ngaco, kami males menuruti perintah Anda, bye!")