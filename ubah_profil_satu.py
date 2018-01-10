import pymysql
def ubah_profil_satu(entity, value, nama_depan):
	# Open database connection
	db = pymysql.connect("localhost","testuser","test123","testdb")

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "update employee set %s='%s' where first_name='%s'" % (entity, value, nama_depan)

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