import pymysql
def hapus_profil(nama_depan):
	# Open database connection
	db = pymysql.connect("localhost","testuser","test123","testdb")

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "delete from employee where first_name='%s'" % (nama_depan)

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