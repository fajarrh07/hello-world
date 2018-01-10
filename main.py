import cek_hari
import tambah_profil
import lihat_profil
import ubah_profil
import ubah_profil_satu
import ubah_profil_semua
import hapus_profil

#hari=input("masukan hari: ")
#cek_hari.cek_hari(hari)
flag=0
print("SELAMAT DATANG DI FAJWA, SILAHKAN PILIH MENU YANG INGIN DIPILIH \n")
print("1. Lihat Profil \n2. Masukan profil baru \n3. Update profil \n4. Hapus profil")
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
elif(pilihan=="3"):
	flag=3
	nama_depan=input("masukan nama depan profil yang ingin diubah: ")
	ubah_profil.ubah_profil(nama_depan)
elif(pilihan=="4"):
	nama_depan=input("masukan nama depan profil yang ingin dihapus: ")
	hapus_profil.hapus_profil(nama_depan)
else:
	print("Anda ngaco, kami males menuruti perintah Anda, bye!")
	
if(flag==3):
	changedEntityNumber=input("Apakah anda ingin mengubah satu bagian data atau seluruhnya?(satu/semua): ")
	if(changedEntityNumber=="satu"):
		changedEntityPart=input("bagian mana yang ingin Anda ubah?(first_name/last_name/age/sex/income): ")
		changedEntityVal=input("%s: " % (changedEntityPart))
		ubah_profil_satu.ubah_profil_satu(changedEntityPart, changedEntityVal, nama_depan)
	elif(changedEntityNumber=="semua"):
		ubah_profil_semua.ubah_profil_semua(nama_depan)
