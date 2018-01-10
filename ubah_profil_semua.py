import pymysql
def ubah_profil_semua(nama_depan):
	# Open database connection
	db = pymysql.connect("localhost","testuser","test123","testdb")

	nama_depan_baru=input("masukan nama depan baru: ")
	nama_belakang=input("masukan nama_belakang baru: ")
	gender=input("masukan gender baru: ")
	umur=input("masukan umur baru: ")
	pendapatan=input("masukan pendapatan baru: ")
	
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "update employee set first_name='%s', last_name='%s', age='%s', sex='%s', income='%s' where first_name='%s'" % (nama_depan_baru, nama_belakang, umur, gender, pendapatan, nama_depan)

	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   print("--sukses mengubah data profil--")
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   print("--gagal menambahkan orang--")
	   db.rollback()

	# disconnect from server
	db.close()