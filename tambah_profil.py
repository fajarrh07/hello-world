import pymysql
def tambah_profil(nama_depan, nama_belakang, umur, gender, pemasukan):
	# Open database connection
	db = pymysql.connect("localhost","testuser","test123","testdb" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	sql = "insert into employee(first_name, last_name, age, sex, income) values('%s', '%s', '%s', '%s', '%s')" % (nama_depan, nama_belakang, umur, gender, pemasukan)

	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   print("**sukses menambahkan orang**")
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   print("**gagal menambahkan orang**")
	   db.rollback()

	# disconnect from server
	db.close()